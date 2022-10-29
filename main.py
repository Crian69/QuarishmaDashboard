import os
import sys
import enum
import time
import subprocess
from typing import Optional
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


class Play(enum.Enum):
    CAMERA = "camera"
    IMAGES = "images"
    VIDEOS = "videos"
    SOUNDS = "sounds"


class QuarishmaPlayer:
    def __init__(self) -> None:
        self.what: Play
        self.where: subprocess.Popen
        self.old_where: subprocess.Popen
        self.isPlaying = False

    def play(self, what: Play, file: Optional[str] = None):
        if self.isPlaying:
            self.old_where = self.where
        self.what = what
        if what == Play.CAMERA:
            self.where = subprocess.Popen(
                [sys.executable, os.path.join(".", "apps", "camera.py")]
            )
        if what == Play.IMAGES:
            self.where = subprocess.Popen(
                [sys.executable, os.path.join(".", "apps", "image.py"), file]
            )
        if self.isPlaying:
            # waiting for new app to open
            time.sleep(1)
            self.stop()

        self.isPlaying = True

    def stop(self):
        # self.isPlaying = False
        self.old_where.terminate()


player = QuarishmaPlayer()


@app.get("/")
def main():
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


@app.post("/")
def p():
    form_resp = request.form
    file_to_play = None
    to_play = form_resp["option"]
    if to_play == "camera":
        to_play = Play.CAMERA
    else:
        file_to_play = form_resp["choose_image"]
        to_play = Play.IMAGES

    player.play(to_play, file_to_play)
    return redirect("/")


@app.post("/stop")
def stop():
    print("Here")
    if player.isPlaying:
        player.where.terminate()
        player.isPlaying = False
    return redirect(url_for("main"))


from werkzeug.utils import secure_filename


@app.route("/upload")
def upload_file():
    return """
        <html>
   <body>
      <form action = "http://localhost:5000/uploader" method = "POST" 
         enctype = "multipart/form-data">
         <input type = "file" name = "file" />
         <input type = "submit"/>
      </form>   
   </body>
</html>
    """


@app.route("/uploader", methods=["GET", "POST"])
def upload_fil():
    if request.method == "POST":
        f = request.files["file"]
        f.save(secure_filename(f.filename))
        return "file uploaded successfully"

2
if __name__ == "__main__":
    try:
        app.run(debug=True, host="0.0.0.0")
    except KeyboardInterrupt:
        player.stop()
        func = request.environ.get("werkzeug.server.shutdown")
        func()
