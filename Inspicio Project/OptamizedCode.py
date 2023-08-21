from PIL import ImageGrab
from win32api import GetSystemMetrics
import numpy as np
import cv2
import time
import datetime
from matplotlib import pyplot as plt
from ctypes import windll, create_unicode_buffer
import keyboard
    


def get_active_window_title():
    """Return the tittle of the active window."""
    hWnd = windll.user32.GetForegroundWindow()
    length = windll.user32.GetWindowTextLengthW(hWnd)
    buf = create_unicode_buffer(length + 1)
    windll.user32.GetWindowTextW(hWnd, buf, length + 1)

    if buf.value:
        return buf.value
    else:
        return None
    
def Currenttime():
    x = datetime.datetime.now().strftime('%d-%m-%Y %H-%M-%S')
    return x

def pr():
    delay = datetime.datetime.now().strftime("%f")
    delay = int(delay)
    if delay%25 == 0:
        with open("activity.txt", "a") as f:
            f.write(get_active_window_title() + str(Currenttime()) + "\n")
        print(get_active_window_title(), "  ", Currenttime())
        return
        
def p_detected():
    p = print("Person Detected!!!\t", Currenttime())
    return p

def nop_detected():
    p = print("No Person Detecting, Suspecious Activity!!!!\t", Currenttime())
    return p

width = GetSystemMetrics(0)
height = GetSystemMetrics(1)
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
ScreenCap = cv2.VideoWriter(f'{Currenttime()}screen.mp4', fourcc, 20, (width, height) )

Videocap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')    

detection, timer_started = False, False
detection_stopped= None
StopRecTime = 5
frame_size = (int(Videocap.get(3)), int(Videocap.get(4)))  


while True:

    '''Screen Capture'''
    img = ImageGrab.grab(bbox=(0, 0, width, height))
    img_np = np.array(img)
    img_final = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
    ScreenCap.write(img_final)
    
    '''Video Capture'''
    _, frame = Videocap.read()
    fr_height, fr_width, _ = frame.shape
    grey = cv2.cvtColor(frame , cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(grey, 1.2, 4)

    if len(faces) > 0:
        if detection:
            timer_started =  False
        else:
            detection = True
            FaceRecord = cv2.VideoWriter(f"{Currenttime()}cam.mp4", fourcc, 20, frame_size)
            p_detected()
    
    elif detection:
        if timer_started : 
            if time.time() - detection_stopped >= StopRecTime :
                detection = False
                FaceRecord.release()
                nop_detected()
                
        else:        
            timer_started = True
            detection_stopped = time.time()   
    if detection:
        FaceRecord.write(frame)
        
    if __name__ == "__main__": 
        pr() 

    k = cv2.waitKey(30) & 0xFF
    if keyboard.is_pressed('esc'):
        break    

cv2.destroyAllWindows()    
                       


