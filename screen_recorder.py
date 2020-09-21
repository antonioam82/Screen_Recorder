#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tkinter import Button, Label, Tk
from tkinter import filedialog
import cv2
import ctypes
import time
import glob
import numpy as np
import pyautogui
import threading
import os

recording = False
fourcc = cv2.VideoWriter_fourcc(*"XVID")
contadores = [0,0,0]
frame_counter = 0

def clear_contador():
    global contadores
    contadores = [0,0,0]

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

def cuenta(n):
    #global proceso
    global contadores,frame_counter
    clock['text'] = str(formato(contadores[0]))+":"+str(formato(contadores[1]))+":"+str(formato(contadores[2]))
    if n == 20.0:
        contadores[2]+=1
        frame_counter = 0
        
    if contadores[2]==60:
        contadores[2]=0
        contadores[1]+=1
    if contadores[1]==60:
        contadores[1]=0
        contadores[0]+=1
    #contador+=1
    
    #proceso=time.after(1000, cuenta)
    
def record_state():
    global out
    global recording
    if recording == True:
        recording = False
        #time.after_cancel(proceso)
        #clear_contador()
    else:
        recording = True
        recorder.configure(text="Stop")
        if contadores != [0,0,0]:
            clear_contador()
            clock['text'] = str(formato(contadores[0]))+":"+str(formato(contadores[1]))+":"+str(formato(contadores[2]))
            time.sleep(1)
        t1=threading.Thread(target=record)
        #t=threading.Thread(target=cuenta)
        t1.start()
        #t.start()
        
def direct():
    directorio=filedialog.askdirectory()
    if directorio!="":
        os.chdir(directorio)

def record():
    global out, frame_counter
    out = cv2.VideoWriter(file_name("screenvideo",".mp4"), fourcc, 20.0, (screen_size))#20.0 18.2 #17
    while recording == True:
        img = pyautogui.screenshot()
        frame = np.array(img)
        frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        out.write(frame)
        frame_counter+=1
        cuenta(frame_counter)
        
    print(frame_counter)
    recorder.configure(text="Record")
    out.release()

ventana = Tk()
ventana.geometry("217x165")
ventana.configure(bg="light gray")
screen_size = screen_s()


label = Label(ventana, text="Screen Record&Shoot",bg="light gray")
label.pack(padx=10,pady=1)
clock = Label(ventana, fg='green', width=22, text="00:00:00", bg="black", font=("","10"))#text="00:00:00"
clock.pack()
recorder = Button(ventana,text="Record",bg="light blue",fg="red",width=8,command=record_state)#gray66
recorder.pack(padx=10,pady=10)
shoot = Button(ventana,text="Screenshot",bg="light blue",fg="red",width=8,command=screen_shoot)
shoot.pack(padx=10,pady=0)

folder = Button(ventana,text="Select Folder",bg="gray66",width=10,command=direct)
folder.pack(padx=10,pady=10)

ventana.mainloop()

