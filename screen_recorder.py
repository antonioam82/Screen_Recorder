from tkinter import *
import cv2
import ctypes
import numpy as np
from time import perf_counter
import pyautogui
import threading

recording = False

def screen_s():
    #global user32
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    dimensions = user32.GetSystemMetrics(0),user32.GetSystemMetrics(1)
    return dimensions

def init():
    global screen_size, fourcc, out
    screen_size = screen_s()
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    out = cv2.VideoWriter("output.avi", fourcc, 20.0, (screen_size))

def record_state():
    global recording
    if recording == True:
        recording = False
    else:
        recording = True
        recorder.configure(text="Parar")
        t1=threading.Thread(target=record)
        t1.start()

def record():
    global img, frame, out
    while recording == True:
        img = pyautogui.screenshot()
        frame = np.array(img)
        frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        out.write(frame)
    recorder.configure(text="Grabar")
    out.release()
    
    
ventana = Tk()
#ventana.title("Screen Rescorder")
init()

recorder = Button(ventana,text="Grabar",command=record_state)
recorder.pack(padx=10,pady=10)

ventana.mainloop()

