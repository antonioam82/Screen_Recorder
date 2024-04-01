#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import Button, Label, Tk
from tkinter import filedialog
import cv2
import ctypes
import glob
import numpy as np
import pyautogui
import threading
from pynput import keyboard
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

def get_dir():
    directorio_actual.set(os.getcwd())

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

def on_press(key):
    global listener
    if key == keyboard.Key.space:
        #return False  # Detiene el listener
        listener.stop()
        print("Stopped")

def listening():
    global listener
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    print("listening")


def cuenta(n):
    global contadores,frame_counter
    clock['text'] = str(contadores[0])+":"+str(formato(contadores[1]))+":"+str(formato(contadores[2]))
    if n == 20.0:
        contadores[2]+=1
        frame_counter = 0
        
    if contadores[2]==60:
        contadores[2]=0
        contadores[1]+=1
    if contadores[1]==60:
        contadores[1]=0
        contadores[0]+=1
    
def record_state():
    global out
    global recording
    if recording == True:
        recording = False
    else:
        clear_contador()
        recording = True
        recorder.configure(text="Stop")
        t1=threading.Thread(target=record)
        t1.start()

        
def direct():
    directorio=filedialog.askdirectory()
    if directorio!="":
        os.chdir(directorio)
        directorio_actual.set(os.getcwd())

def record():
    global out, frame_counter, fail
    fail = False
    frameRate = 30
    out = cv2.VideoWriter(file_name("screenvideo",".mp4"), fourcc, frameRate, (screen_size))#20.0 18.2 #17
    while recording == True:
        try:
            img = pyautogui.screenshot()
            frame = np.array(img)
            frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
            out.write(frame)
            frame_counter+=1
            cuenta(frame_counter)
        except Exception as e:
            #print(str(e))
            fail = True
            break
        
    if fail == False:
        print(frame_counter)
        recorder.configure(text="Record")
        out.release()

ventana = Tk()
ventana.title("Screen Recorder")
ventana.geometry("507x143")
ventana.configure(bg="light gray")
directorio_actual=StringVar()
screen_size = screen_s()


Dirlabel = Entry(ventana,bg="white",width=90,textvariable=directorio_actual)
Dirlabel.pack(padx=1,pady=1)
clock = Label(ventana, fg='green', width=21, text="0:00:00", bg="black", font=("","29"))#text="00:00:00"
clock.pack(pady=10)
recorder = Button(ventana,text="Listen to keyboard",bg="light blue",fg="red",width=33,command=listening)
recorder.place(x=11,y=88)
shoot = Button(ventana,text="Screenshot",bg="light blue",fg="red",width=33,command=screen_shoot)
shoot.place(x=255,y=88)

folder = Button(ventana,text="Select Folder",bg="gray66",width=68,command=direct)
folder.pack(padx=1,side='bottom')

get_dir()

ventana.mainloop()
