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

def file_name():
    count = 0
    grabs = glob.glob('*.avi')
    for i in grabs:
        if "videocapture" in i:
            count+=1
    if count>0:
        filename="videocapture"+"("+str(count)+")"+".avi"
    else:
        filename="videocapture.avi"
    return filename

def record_state():
    global out
    global recording
    if recording == True:
        recording = False
    else:
        recording = True
        out = cv2.VideoWriter(file_name(), fourcc, 20.0, (screen_size))
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
ventana.geometry("190x120")
ventana.configure(bg="light gray")
screen_size = screen_s()
label = Label(ventana, text="Screen Recorder",bg="gray",fg="white")
label.pack(padx=10,pady=1)
recorder = Button(ventana,text="Record",bg="gray66",width=8,command=record_state)
recorder.pack(padx=10,pady=20)
folder = Button(ventana,text="Select Folder",bg="gray66",width=10,command=direct)
folder.pack(padx=10,pady=1)

ventana.mainloop()

