from tkinter import *
import pyaudio
import cv2
import ctypes
import numpy as np
from time import perf_counter
import pyautogui
import threading

recording = False
num_frame=0

def screen_s():
    #global user32
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    dimensions = user32.GetSystemMetrics(0),user32.GetSystemMetrics(1)
    return dimensions

def init():
    global screen_size, fourcc, out
    global audio, FORMAT, CHANNELS, RATE, outAudio
    #VALORES PARA CAPTURA PANTALLA
    screen_size = screen_s()
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    out = cv2.VideoWriter("output.avi", fourcc, 20.0, (screen_size))
    #VALORES PARA SONIDO
    audio = pyaudio.PyAudio()
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    outAudio = "output.wav"

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
    global img, frame, out, num_frame
    while recording == True:
        img = pyautogui.screenshot()
        frame = np.array(img)
        frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        out.write(frame)
        num_frame+=1
        print(num_frame)
    recorder.configure(text="Grabar")
    out.release()
    
    
ventana = Tk()
ventana.geometry("150x80")
#ventana.title("Screen Rescorder")
init()

recorder = Button(ventana,text="Grabar",command=record_state)
recorder.pack(padx=10,pady=20)

ventana.mainloop()

