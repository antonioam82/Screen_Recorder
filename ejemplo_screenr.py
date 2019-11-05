import cv2
import numpy as np
import pyautogui

#FORMATO PARA CREACIÓN DE VIDEO
screen_size = (1600, 900)
fourcc = cv2.VideoWriter_fourcc(*"XVID")
out = cv2.VideoWriter("output.avi", fourcc, 20.0, (screen_size))

while True:
    #CAPTURA DE PANTALLA
    img = pyautogui.screenshot()
    #TRADUCIMOS CAPTURA A UN ARRAY QUE PUEDA LEER "cv2" 
    frame = np.array(img)
    #CONVERTIMOS "frame" DE FORMATO "BGR" A "RGB".
    frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    #AÑADIMOS "frame" AL FUTURO VÍDEO.
    out.write(frame)

    #MOSTRAMOS CAPTURA DE PANTALLA ACTUAL
    cv2.imshow("screenshot", frame)

    #SI PULSAMOS "esc" FINALIZA EL PROCESO.
    if cv2.waitKey(1) == 27:
        print("END")
        break
    
#CERRAMOS TODAS LAS VENTANAS 
cv2.destroyAllWindows()
#CREAMOS VÍDEO.
out.release()

