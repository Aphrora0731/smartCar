import _thread
import time
import tkinter as tk
from tkinter import *
import imutils
from threading import Thread
from imutils.video import VideoStream
import tkinter.ttk as ttk
import cv2
from PIL import Image, ImageTk
import multiprocessing
import mylib
import camera
from is_sleep import is_sleep

import detect
import UDPService as udp

window_width = 960
window_height = 720
image_width = int(window_width * 0.9)
image_height = int(window_height * 0.9)
imagepos_x = 0
imagepos_y = 0
butpos_x = 450
butpos_y = 450

# 选择摄像头
warning = camera.makeWarning()
start_time = time.perf_counter()
detect.vs = VideoStream(src=1).start()

#初始化UDP服务
udpS=udp.UDPService('100.150.110.15')

def cnt_time():
    return (time.perf_counter() - start_time) % 2


def video():
    global udpS
    def video_loop():
        global udpS
        try:
            start = time.perf_counter()
            warning = camera.makeWarning()
            i = 0
            while True:
                frame = detect.get_video()
                res = detect.video_object(frame)
                udpS.sendFrame(res)
                (light_detection, light_is_on) = detect.brake_light(frame)
                if light_is_on:
                    light_is_on = False
                    i = i + 1
                    print("light is on", i)
                    end = time.perf_counter()
                    print(end, start)
                    if end - start > 4:
                        t = Thread(target=mylib.sound_alarm)
                        t.deamon = True  # 守护进程
                        t.start()
                        start = time.perf_counter()
                res = cv2.cvtColor(res, cv2.COLOR_BGR2RGB)
                picture1 = Image.fromarray(res)
                picture1 = ImageTk.PhotoImage(picture1)
                canvas.create_image(0, 0, anchor='nw', image=picture1)
                dif = time.perf_counter() - start
                dif = dif % 2
                win.update_idletasks()
                win.update()
        except:
            pass

    video_loop()
    win.mainloop()
    cv2.destroyAllWindows()


def detect_sleep():
    def video_loop():
        try:
            while True:
                frame = detect.get_video()
                res = is_sleep(frame)
                res = cv2.cvtColor(res, cv2.COLOR_BGR2RGB)
                picture1 = Image.fromarray(res)
                picture1 = ImageTk.PhotoImage(picture1)
                canvas2.create_image(0, 0, anchor='nw', image=picture1)
                win.update_idletasks()
                win.update()
        except:
            pass

    video_loop()
    win.mainloop()
    cv2.destroyAllWindows()


win = tk.Tk()
win.title("central console")
ttk.Style().configure("TButton", padding=6, relief="flat",
                      background="#ccc")

win.geometry(str(window_width) + 'x' + str(window_height))
# canvas.place(x=imagepos_x, y=imagepos_y)

tab = ttk.Notebook(win)
canvas = Canvas(tab, bg='white', width=image_width, height=image_height)
tab1 = tab.add(canvas, text="车前摄像头")

canvas2 = Canvas(tab, bg='blue', width=image_width, height=image_height)
tab2 = tab.add(canvas2, text="后方摄像头 ")

frame3 = tk.Frame(tab, bg="green")
tab3 = tab.add(frame3, text="3")

tab.pack(expand=True, fill=tk.BOTH)

# 设置选中tab2
tab.select(canvas)
if __name__ == '__main__':
    video()
    # detect_sleep()
