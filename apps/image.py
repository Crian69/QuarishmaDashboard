import cv2
import argparse
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk


class FullScreen:
    """Full-screen with Tkinter backend"""

    def __init__(self):
        self._root = tk.Tk()
        self._root.config(cursor="none")
        self._root.wm_attributes("-fullscreen", True)

        # set initial image
        img_gray = np.full((self.height, self.width), 127, dtype=np.uint8)
        tk_img_gray = self._cvt_ndarray_to_tkimage(img_gray)
        self._label = tk.Label(self._root, image=tk_img_gray)
        self._label.pack()
        self._root.update()

    @property
    def width(self):
        return self._root.winfo_width()

    @property
    def height(self):
        return self._root.winfo_height()

    @property
    def shape(self):
        return self.height, self.width, 3

    def imshow(self, image: np.ndarray):
        tk_img = self._cvt_ndarray_to_tkimage(image)

        self._label.image = tk_img
        self._label.configure(image=tk_img)

        self._root.update_idletasks()
        self._root.mainloop()

    def _cvt_ndarray_to_tkimage(self, image: np.ndarray) -> ImageTk.PhotoImage:
        """Convert ndarray data to PhotoImage using PIL"""
        if image.ndim == 2:
            img_rgb = np.dstack([image] * 3)  # Gray -> RGB
        else:
            img_rgb = image[:, :, ::-1]  # BGR -> RGB

        pil_img = Image.fromarray(img_rgb, mode="RGB")
        if pil_img.size != (self.width, self.height):
            pil_img = pil_img.resize(
                (self.width, self.height), Image.Resampling.NEAREST
            )

        tk_img = ImageTk.PhotoImage(pil_img)
        return tk_img


f = FullScreen()
parser = argparse.ArgumentParser()
parser.add_argument("filename", metavar="N", type=str, help="file name to use")
args = parser.parse_args()
img = cv2.imread(f"media/images/{args.filename}", 1)
while True:
    try:
        f.imshow(image=img)
    except:
        f._root.destroy()
