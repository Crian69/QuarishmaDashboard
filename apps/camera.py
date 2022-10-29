import cv2
import tkinter as tk
import PIL.Image, PIL.ImageTk, PIL.Image


class App:
    def __init__(self, window: tk.Tk):
        self.faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        self.window = window
        self.window.title("My Eyes")
        self.window.attributes('-fullscreen', True)
        self.vid = cv2.VideoCapture(0)
        self.lab = tk.Canvas(self.window)
        self.lab.place(x=0, y=0, relwidth=1, relheight=1)
        self.update()

    def update(self):
        _, frame = self.vid.read()
        
        #DETECTS FACE source: https://realpython.com/face-recognition-with-python/
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags = cv2.CASCADE_SCALE_IMAGE
        )
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        ##########

        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        image = PIL.Image.fromarray(frame)
        resized_image = image.resize((self.window.winfo_width(), self.window.winfo_height()), PIL.Image.Resampling.LANCZOS)
        self.photo = PIL.ImageTk.PhotoImage(image = resized_image)
        self.lab.create_image(self.window.winfo_width()/2,self.window.winfo_height()/2, image = self.photo)
        
        self.window.after(10,self.update)


def main():
    app = App(tk.Tk())
    try:
        app.window.mainloop()
    except:
        app.window.destroy()


main()