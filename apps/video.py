import argparse
import tkinter as tk
from tkVideoPlayer import TkinterVideo


class VideoPlayer:
    """Full Screen video player"""

    def __init__(self, video) -> None:
        self._root = tk.Tk()
        self._root.config(cursor="none")
        self._root.wm_attributes("-fullscreen", True)
        self.player = TkinterVideo(scaled=True, master=self._root)
        self.player.load(f"{video}")
        self.player.pack(expand=True, fill="both")
        self.player.play()
        self.player.bind("<<Ended>>", self.loop)
        self._root.mainloop()
    
    def loop(self, e):
        self.player.play()
        
parser = argparse.ArgumentParser()
parser.add_argument("filename", metavar="N", type=str, help="file name to use")
args = parser.parse_args()
p = VideoPlayer(f"media/videos/{args.filename}")