from tkinter import *
import cv2
import ctypes
import numpy as np
from time import perf_counter
import pyautogui
import threading

recording = False
fourcc = cv2.VideoWriter_fourcc(*"XVID")

def screen_s():
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    dimensions = user32.GetSystemMetrics(0),user32.GetSystemMetrics(1)
    return dimensions

def record_state():
    global out
    global recording
    if recording == True:
        recording = False
    else:
        recording = True
        out = cv2.VideoWriter("output.avi", fourcc, 20.0, (screen_size))
        recorder.configure(text="Stop")
        t1=threading.Thread(target=record)
        t1.start()

def record():
    global out
    while recording == True:
        #print("GRABANDO")
        img = pyautogui.screenshot()
        frame = np.array(img)
        frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        out.write(frame)
    #print("FIN")
    recorder.configure(text="Record")
    out.release()

ventana = Tk()
ventana.geometry("150x100")
screen_size = screen_s()
label = Label(ventana, text="Screen Recorder",fg='blue')
label.pack(padx=10,pady=1)
recorder = Button(ventana,text="Record",width=8,command=record_state)
recorder.pack(padx=10,pady=20)

ventana.mainloop()
