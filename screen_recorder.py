import cv2
import ctypes
import numpy as np
from time import perf_counter
import pyautogui

def screen_s():
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    width, height = user32.GetSystemMetrics(0),user32.GetSystemMetrics(1)
    return (width,height)

screen_size = screen_s() #1600 900
fourcc = cv2.VideoWriter_fourcc(*"XVID")
out = cv2.VideoWriter("output.avi", fourcc, 20.0, (screen_size))

while True:
    img = pyautogui.screenshot()
    frame = np.array(img)
    frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    out.write(frame)
    #cv2.imshow("screenshot",frame)
    if cv2.waitKey(0) == ord("q"):
        print("END")
        break
    
cv2.destroyAllWindows()
out.release()
