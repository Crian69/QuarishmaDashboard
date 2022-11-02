import os
import sys
import enum
import subprocess
from typing import Optional
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, url_for, make_response

app = Flask(__name__)


class Play(enum.Enum):
    CAMERA = "camera"
    IMAGES = "images"
    VIDEOS = "videos"
    SOUNDS = "sounds"


class Player:
    def __init__(self) -> None:
        self.isPlaying = False
        self.to_play = Play
        self.process: subprocess.Popen

    def play(self, _type: Play, file: Optional[str] = None):
        if self.isPlaying:
            self.process.terminate()
        match _type:
            case Play.CAMERA:
                self.process = subprocess.Popen(
                    [sys.executable, os.path.join(".", "apps", "camera.py")]
                )
            case Play.VIDEOS:
                self.process = subprocess.Popen(
                    [sys.executable, os.path.join(".", "apps", "video.py"), file]
                )
            case Play.IMAGES:
                self.process = subprocess.Popen(
                    [sys.executable, os.path.join(".", "apps", "image.py"), file]
                )
            case Play.SOUNDS:
                print("HI")
            case _:
                raise ValueError("Invalid task for player to play")
        self.isPlaying = True

    def stop(self):
        if self.isPlaying:
            self.process.terminate()
            self.isPlaying = False


player = Player()


@app.route("/", methods=["GET", "POST"])
def main():
    if request.method == "GET":
        images = os.listdir(os.path.join(".", "media", "images"))
        videos = os.listdir(os.path.join(".", "media", "videos"))
        sounds = os.listdir(os.path.join(".", "media", "sounds"))
        can_not_stop = "" if player.isPlaying else "disabled"

        return render_template(
            "main.html",
            images=images,
            leni=len(images),
            videos=videos,
            lenv=len(videos),
            sounds=sounds,
            lens=len(sounds),
            can_not_stop=can_not_stop,
        )
    else:
        form_resp = request.form
        file_to_play = None
        to_play = form_resp["option"]
        if to_play == "camera":
            to_play = Play.CAMERA
        elif to_play == "image":
            file_to_play = form_resp["choose_image"]
            to_play = Play.IMAGES
        elif to_play == "video":
            file_to_play = form_resp["choose_video"]
            to_play = Play.VIDEOS
        else:
            return "Invalid Request"

        player.play(to_play, file_to_play)
        return redirect(url_for("main"))


@app.post("/stop")
def stop():
    player.stop()
    return redirect(url_for("main"))


@app.route("/upload")
def upload_file():
    return f'<html><body><form action = "{request.base_url}/uploader" method = "POST" enctype = "multipart/form-data"><input type = "file" name = "file" /><input type = "submit"/></form></body></html>'

@app.route("/uploader", methods=["GET", "POST"])
def upload_fil():
    if request.method == "POST":
        f = request.files["file"]
        f.save(secure_filename(f.filename))
        return "file uploaded successfully"


if __name__ == "__main__":
    try:
        app.run(debug=True, host="0.0.0.0")
    except KeyboardInterrupt:
        player.stop()
        func = request.environ.get("werkzeug.server.shutdown")
        func()