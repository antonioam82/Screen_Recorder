#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import Button, Label, Tk
from tkinter import filedialog
from mhmovie.code import *
import time
import wave###
import pyaudio
import cv2
import ctypes
import glob
import numpy as np
import pyautogui
import threading
import os

recording = False
fourcc = cv2.VideoWriter_fourcc(*"XVID")
contadores = [0,0,0]
frame_counter = 0
finished = False################################################################

def init_recorder():
    global stream, CHUNK, frames, p, RATE, CHANNELS, WAVE_OUTPUT_FILENAME, FORMAT
    #INIT SOUND RECORDER:
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    WAVE_OUTPUT_FILENAME = "output.wav"
    p = pyaudio.PyAudio()
    frames = []

    stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

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
        filename=tex+"_"+str(count)+ext
    else:
        filename=tex+ext
    return filename

def screen_shoot():
    pyautogui.screenshot(file_name("screenshoot",".jpg"))

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
        init_recorder()
        recording = True
        recorder.configure(text="Stop")
        t1=threading.Thread(target=record)
        t = threading.Thread(target=record_sound)
        t1.start()
        t.start()

def merge():
    global WAVE_OUTPUT_FILENAME, OUTPUT_VIDEO, finished
    vid = movie(OUTPUT_VIDEO)
    aud = music(WAVE_OUTPUT_FILENAME)
    while True:########################################################
        if finished == True:
            result = vid+aud
            break
    name = file_name('final_video','.avi')
    print(name)
    result.save(name)
    os.remove(OUTPUT_VIDEO)
    os.remove(WAVE_OUTPUT_FILENAME)
    finished = False##################################################
    
    
def direct():
    directorio=filedialog.askdirectory()
    if directorio!="":
        os.chdir(directorio)
        directorio_actual.set(os.getcwd())

def record():
    global out, frame_counter, OUTPUT_VIDEO
    OUTPUT_VIDEO = "screenvideo.avi"
    out = cv2.VideoWriter(OUTPUT_VIDEO, fourcc, 20.0, (screen_size))#20.0 18.2 #17
    while recording == True:
        try:
            img = pyautogui.screenshot()
            frame = np.array(img)
            frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
            out.write(frame)
            frame_counter+=1
            cuenta(frame_counter)
        except:
            pass
        
    print(frame_counter)
    recorder.configure(text="Record")
    out.release()
    time.sleep(2)
    merge()

def record_sound():
    global stream, CHUNK, frames, p, RATE, CHANNELS, WAVE_OUTPUT_FILENAME, FORMAT, finished
    while recording == True:
        data = stream.read(CHUNK)
        frames.append(data)
    print("STOPPED")
    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    finished = True###############################################
    print("finish")

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
recorder = Button(ventana,text="Record",bg="light blue",fg="red",width=33,command=record_state)#gray66
recorder.place(x=11,y=88)
shoot = Button(ventana,text="Screenshot",bg="light blue",fg="red",width=33,command=screen_shoot)
shoot.place(x=255,y=88)

folder = Button(ventana,text="Select Folder",bg="gray66",width=68,command=direct)
folder.pack(padx=1,side='bottom')

get_dir()

ventana.mainloop()

