import _thread
import time
import tkinter as tk
from tkinter import *

import tkinter.ttk as ttk
import cv2
from PIL import Image, ImageTk
import multiprocessing
import camera

import detect

window_width = 960
window_height = 720
image_width = int(window_width * 0.9)
image_height = int(window_height * 0.9)
imagepos_x = 0
imagepos_y = 0
butpos_x = 450
butpos_y = 450

# 选择摄像头
vc1 = cv2.VideoCapture(0)
warning = camera.makeWarning()
start_time = time.perf_counter()


def cnt_time():
    return (time.perf_counter() - start_time) % 2


def tkImage(vc):
    ref, frame = vc.read()
    cvimage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    pilImage = Image.fromarray(cvimage)
    pilImage = pilImage.resize((image_width, image_height), Image.ANTIALIAS)
    pilImage = pilImage.convert('RGBA')
    if cnt_time() < 1:
        pilImage.paste(warning, (800, 00))
    res = pilImage

    tkImage = ImageTk.PhotoImage(image=res)
    return tkImage


def video():
    def video_loop():
        try:
            start = time.perf_counter()
            warning = camera.makeWarning()
            while True:
                picture1 = tkImage(vc1)
                canvas.create_image(0, 0, anchor='nw', image=picture1)
                dif = time.perf_counter() - start
                dif = dif % 2
                win.update_idletasks()
                win.update()
        except:
            pass

    video_loop()
    win.mainloop()
    vc1.release()
    cv2.destroyAllWindows()


win = tk.Tk()
win.title("central console")
ttk.Style().configure("TButton", padding=6, relief="flat",
                      background="#ccc")

btn = ttk.Button(win, command=lambda: camera.backCar(win), text="video")
btn.pack(side="right")
win.geometry(str(window_width) + 'x' + str(window_height))
canvas = Canvas(win, bg='white', width=image_width, height=image_height)
canvas.place(x=imagepos_x, y=imagepos_y)
if __name__ == '__main__':
    p1 = multiprocessing.Process(target=video)
    p1.start()
