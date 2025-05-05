import cv2
import os
import numpy as np
from abc import ABC, abstractmethod
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import time
import serial
#from GUI_emb_vis import *

import cv2
import numpy as np

import cv2
import numpy as np

def detect_shapes(frame, threshold_value=60, blur_kernel=(5, 5), morph_kernel_size=3):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, blur_kernel, 0)
    _, thresh = cv2.threshold(blurred, threshold_value, 255, cv2.THRESH_BINARY)

    # Operaciones morfológicas
    kernel = np.ones((morph_kernel_size, morph_kernel_size), np.uint8)
    opened = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

    contours, _ = cv2.findContours(opened, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    output = frame.copy()

    for c in contours:
        if cv2.contourArea(c) < 300:
            continue

        epsilon = 0.02 * cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, epsilon, True)
        x, y, w, h = cv2.boundingRect(approx)
        shape = "Unknown"

        if len(approx) == 3:
            shape = "Triangle"
        elif len(approx) == 4:
            shape = "Rectangle"
        elif len(approx) == 5:
            shape = "Pentagon"
        elif len(approx) == 6:
            shape = "Hexagon"
        elif len(approx) > 6:
            shape = "Circle"

        cv2.rectangle(output, (x, y), (x + w, y + h), (0, 255, 255), 2)
        cv2.putText(output, shape, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 2)

    opened = cv2.cvtColor(opened, cv2.COLOR_GRAY2BGR)

    return opened, output


cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("No se pudo abrir la cámara.")

while True:
    ret, frame = cap.read()
    if not ret:
        break
    #print(frame.shape)
    #frame = cv2.resize(frame, (480, 640))

    opened1, shapes_default = detect_shapes(frame.copy(), threshold_value=60, blur_kernel=(5, 5), morph_kernel_size=3)
    #opened2, shapes_strong_morph = detect_shapes(frame.copy(), threshold_value=60, blur_kernel=(5, 5), morph_kernel_size=7)
    #opened3, shapes_less_blur = detect_shapes(frame.copy(), threshold_value=60, blur_kernel=(3, 3), morph_kernel_size=3)
    #opened4, shapes_high_thresh = detect_shapes(frame.copy(), threshold_value=100, blur_kernel=(5, 5), morph_kernel_size=3)



    cv2.imshow("Original", frame)
    #cv2.imshow("DetectShapes - Default", np.hstack([opened1,shapes_default]) )
    #cv2.imshow("DetectShapes - Strong Morph", np.hstack([opened2,shapes_strong_morph]))
    #cv2.imshow("DetectShapes - Less Blur", np.hstack([opened3,shapes_less_blur]))
    #cv2.imshow("DetectShapes - High Threshold", np.hstack([opened4,shapes_high_thresh]))

    key = cv2.waitKey(1) & 0xFF
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
