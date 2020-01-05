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
contador=0
contador1=0
contador2=0

def clear_contador():
    global contador,contador1,contador2
    contador=0
    contador1=0
    contador2=0

def formato(c):
    if c<10:
        c="0"+str(c)
    return c

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

def cuenta():
    global proceso
    global contador,contador1,contador2
    time['text'] = str(formato(contador1))+":"+str(formato(contador2))+":"+str(formato(contador))
    contador+=1
    if contador==60:
        contador=0
        contador2+=1
    if contador2==60:
        contador2=0
        contador1+=1
    proceso=time.after(1000, cuenta)
    
def record_state():
    global out
    global recording
    if recording == True:
        recording = False
        time.after_cancel(proceso)
        clear_contador()
    else:
        recording = True
        recorder.configure(text="Stop")
        t1=threading.Thread(target=record)
        t=threading.Thread(target=cuenta)
        t1.start()
        t.start()

def direct():
    directorio=filedialog.askdirectory()
    if directorio!="":
        os.chdir(directorio)

def record():
    global out
    out = cv2.VideoWriter(file_name("screenvideo",".mp4"), fourcc, 20.0, (screen_size))
    while recording == True:
        img = pyautogui.screenshot()
        frame = np.array(img)
        frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        out.write(frame)
    recorder.configure(text="Record")
    out.release()

ventana = Tk()
ventana.geometry("217x165")
ventana.configure(bg="light gray")
screen_size = screen_s()


label = Label(ventana, text="Screen Record&Shoot",bg="light gray")
label.pack(padx=10,pady=1)
time = Label(ventana, fg='green', width=22, text="00:00:00", bg="black", font=("","10"))
time.pack()
recorder = Button(ventana,text="Record",bg="light blue",fg="red",width=8,command=record_state)#gray66
recorder.pack(padx=10,pady=10)
shoot = Button(ventana,text="Screenshot",bg="light blue",fg="red",width=8,command=screen_shoot)
shoot.pack(padx=10,pady=0)

folder = Button(ventana,text="Select Folder",bg="gray66",width=10,command=direct)
folder.pack(padx=10,pady=10)

ventana.mainloop()
