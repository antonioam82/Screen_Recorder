#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tkinter import Button, Label, Tk
from tkinter import filedialog
import cv2
import ctypes
import glob
import numpy as np
import pyautogui
import threading
import os

recording = False
fourcc = cv2.VideoWriter_fourcc(*"XVID")

def screen_s():
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    dimensions = user32.GetSystemMetrics(0),user32.GetSystemMetrics(1)
    return dimensions

def file_name(tex,ext):
    count = 0
    for i in glob.glob('*'+ext):
        if tex in i:
            count+=1
    if count>0:
        filename=tex+" "+str(count)+ext
    else:
        filename=tex+ext
    return filename

def screen_shoot():
    pyautogui.screenshot(file_name("screenshoot",".jpg"))
    

def record_state():
    global out
    global recording
    if recording == True:
        recording = False
    else:
        recording = True
        out = cv2.VideoWriter(file_name("screenvideo",".mp4"), fourcc, 20.0, (screen_size))
        recorder.configure(text="Stop")
        t1=threading.Thread(target=record)
        t1.start()

def direct():
    directorio=filedialog.askdirectory()
    if directorio!="":
        os.chdir(directorio)

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
ventana.geometry("215x145")
ventana.configure(bg="light gray")
screen_size = screen_s()

label = Label(ventana, text="Screen Record&Shoot",bg="gray",fg="white")
label.pack(padx=10,pady=1)
recorder = Button(ventana,text="Record",bg="light blue",fg="red",width=8,command=record_state)#gray66
recorder.pack(padx=10,pady=10)
shoot = Button(ventana,text="Screenshot",bg="light blue",fg="red",width=8,command=screen_shoot)
shoot.pack(padx=10,pady=0)

folder = Button(ventana,text="Select Folder",bg="gray66",width=10,command=direct)
folder.pack(padx=10,pady=15)

ventana.mainloop()
