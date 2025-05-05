import cv2
import os
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import time
import serial
#from GUI_emb_vis import *


ruta = 'recursos\\bouncing.mp4'
cap = cv2.VideoCapture(ruta)

if not cap.isOpened():
    print("No se pudo abrir la cámara.")

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    frame = cv2.resize(frame, (640, 360))
    fgbg = cv2.createBackgroundSubtractorKNN(history=1500, dist2Threshold=10.0, detectShadows=True)
    fgmask = fgbg.apply(frame)  # Aplica el sustractor al frame

    cv2.imshow("Original", frame)
    cv2.imshow("mascara", fgmask)

    key = cv2.waitKey(1) & 0xFF
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
