from tkinter import *
import pyaudio
import cv2
import ctypes
import numpy as np
from time import perf_counter
import pyautogui
import threading

recording = False
audio = pyaudio.PyAudio()
CHUNK = 1024
RATE = 44100
FORMAT = pyaudio.paInt16
CHANNELS = 2

def screen_s():
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    dimensions = user32.GetSystemMetrics(0),user32.GetSystemMetrics(1)
    return dimensions

def init():
    global screen_size, fourcc, out
    global outAudio, data, stream, frames
    #VALORES PARA CAPTURA PANTALLA
    screen_size = screen_s()
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    out = cv2.VideoWriter("output.avi", fourcc, 20.0, (screen_size))
    #VALORES PARA SONIDO
    data = ""
    stream = ""
    outAudio = "output.wav"
    stream=audio.open(format=FORMAT,channels=CHANNELS,
                      rate=RATE, input=True,
                      frames_per_buffer=CHUNK)
    frames = []

def record_state():
    global recording
    if recording == True:
        recording = False
    else:
        recording = True
        recorder.configure(text="Parar")
        t1=threading.Thread(target=record)
        t2=threading.Thread(target=audio_record)
        t1.start()
        t2.start()

def record():
    global img, frame, out, num_frame
    while recording == True:
        img = pyautogui.screenshot()
        frame = np.array(img)
        frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        out.write(frame)
    recorder.configure(text="Grabar")
    out.release()

def audio_record():
    global data, stream, frames
    while recording == True:
        data = stream.read(CHUNK)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    audio.terminate()

    waveFile = wave.open(archivo, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()
    data = ""
    stream = ""
    frames = []
    
    
ventana = Tk()
ventana.geometry("150x80")
#ventana.title("Screen Rescorder")
init()

recorder = Button(ventana,text="Grabar",command=record_state)
recorder.pack(padx=10,pady=20)

ventana.mainloop()


