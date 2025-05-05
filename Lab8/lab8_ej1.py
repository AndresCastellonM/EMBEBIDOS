import cv2
import os
import numpy as np
from abc import ABC, abstractmethod
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import time
import serial
from GUI_emb_vis import *



class VideoCaptureAbs(ABC):
    @abstractmethod
    def display_camera(self): pass
    @abstractmethod
    def stop_display(self): pass
    @abstractmethod
    def camera_visualization(self): pass

class VideoCapture(VideoCaptureAbs):
    
    def __init__(self, camera, gui_ref):
        self.camera = camera
        self.displayed = False
        self.capture_count = 0
        self.gui = gui_ref
        self.modes = 1
        width = self.camera.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.size = (int(width), int(height))
        self.current_mode = "RGB"
        self.config_camera_toggle(127)
        self.toggle_quadrant = 0  # 0: normal, 1: mitad, 2: cuadrantes
        self.bg_subtractor = cv2.createBackgroundSubtractorMOG2()  # Para el modo BORDERS

    def camera_visualization(self):
        while self.displayed:
            ret, frame = self.camera.read()
            if not ret:
                print("[ERROR] No se pudo leer el frame")
                break
            
            if self.gui.flag_change == 1:
                self.active_modes = self.gui.selected_filters
                self.gui.flag_change = 0
            frame = cv2.resize(frame, self.size, interpolation=cv2.INTER_AREA)
            frame = self.camera_toggle(frame)
            frame = self.camera_quadrant(frame)

            key = cv2.waitKey(1) & 0xFF
            if key != 255:
                print(key)
            if key == ord('c'):
                self.save_frame(frame)
                print("c pressed")
            elif key == ord(' '):
                self.toggle_type = (self.toggle_type + 1) % len(self.active_modes)
                self.current_mode = self.active_modes[self.toggle_type]
            elif key == ord('q'):
                self.toggle_quadrant = (self.toggle_quadrant + 1) % 3  # 0,1,2
                print("q pressed")
            elif key == 27:  # ESC
                self.stop_display()

            cv2.imshow("Camera", frame)

    def config_camera_toggle(self, modes):
        self.toggle_type = 0
        self.active_modes = []

        if modes & 0b00000001:  # RGB
            self.active_modes.append("RGB")
        if modes & 0b00000010:  # HSV
            self.active_modes.append("HSV")
        if modes & 0b00000100:  # GRAY
            self.active_modes.append("GRAY")
        if modes & 0b00001000: #BORDERS
            self.active_modes.append("MOTION")
        if modes & 0b00010000: #EDGES
            self.active_modes.append("EDGES")
        if modes & 0b00100000: #BLUR
            self.active_modes.append("BLUR")
        if modes & 0b01000000: #DOM_COL
            self.active_modes.append("DOM_COL")

        if not self.active_modes:
            print("No modes selected.")
        
        self.active_modes = self.gui.selected_filters


    def camera_toggle(self, frame):
        if self.current_mode == "GRAY":
            frame_out = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        elif self.current_mode == "HSV":
            frame_out = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        elif self.current_mode == "MOTION":
            frame_out = self.detect_motion(frame)
        elif self.current_mode == "EDGES":
            frame_out = self.detect_edges(frame)
        elif self.current_mode == "BLUR":
            frame_out = self.apply_blur(frame)
        elif self.current_mode == "DOM_COL":
            frame_out = self.dominant_color(frame)
        else:  # "RGB"
            frame_out = frame

        return frame_out

    def detect_motion(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        fg_mask = self.bg_subtractor.apply(gray)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, kernel)
        fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_CLOSE, kernel)
        contours, _ = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        frame_contours = frame.copy()
        cv2.drawContours(frame_contours, contours, -1, (0, 255, 0), 2)
        return frame_contours

    def detect_edges(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 1.4)
        edges = cv2.Canny(blurred, 50, 150)
        frame_edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)  # Para mantener 3 canales
        return frame_edges

    def apply_blur(self, frame):
        blurred_frame = cv2.GaussianBlur(frame, (15, 15), 0)
        return blurred_frame


    def camera_quadrant(self, frame):
        # --- Según el toggle_quadrant ---
        if self.toggle_quadrant == 0:
            return frame  # Imagen normal

        if self.toggle_quadrant == 1:
            # --- Dos mitades separadas ---
            mid_x = frame.shape[1] // 2
            left = frame[:, :mid_x]
            right = frame[:, mid_x:]
            if self.current_mode == "GRAY":
                sep = 255 * np.ones((frame.shape[0], 50), dtype=np.uint8)
            else:
                sep = 255 * np.ones((frame.shape[0], 50, 3), dtype=np.uint8)
            
            combined = np.hstack((left, sep, right))
            return combined

        if self.toggle_quadrant == 2:
            mid_x = frame.shape[1] // 2
            mid_y = frame.shape[0] // 2

            top_left = frame[:mid_y, :mid_x]
            top_right = frame[:mid_y, mid_x:]
            bottom_left = frame[mid_y:, :mid_x]
            bottom_right = frame[mid_y:, mid_x:]

            if self.current_mode == "GRAY":
                sep_v = 255 * np.ones((mid_y, 10), dtype=np.uint8) 
                sep_h = 255 * np.ones((10, frame.shape[1] + 10), dtype=np.uint8)
            else:
                sep_v = 255 * np.ones((mid_y, 10, 3), dtype=np.uint8) 
                sep_h = 255 * np.ones((10, frame.shape[1] + 10, 3), dtype=np.uint8)

            top = np.hstack((top_left, sep_v, top_right))
            bottom = np.hstack((bottom_left, sep_v, bottom_right))
            combined = np.vstack((top, sep_h, bottom))

            return combined

        return frame

    def display_camera(self):
        self.displayed = True
        self.camera_visualization()

    def stop_display(self):
        self.displayed = False
        cv2.destroyAllWindows()

    def save_frame(self, frame):
        self.capture_count += 1
        filename = f"Captures/image{self.capture_count}.jpg"
        cv2.imwrite(filename, frame)
        print(f"[INFO] Imagen guardada: {filename}")

         
    def camera_colorRangeHSV(self, frame):
        lower = np.array([self.gui.min_h, self.gui.min_s, self.gui.min_v])
        upper = np.array([self.gui.max_h, self.gui.max_s, self.gui.max_v])
        hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
        mask = cv2.inRange(hsv, lower, upper)
        image_masked = cv2.bitwise_and(hsv, hsv, mask=mask)
        image_masked = cv2.cvtColor(image_masked, cv2.COLOR_HSV2RGB)
        return image_masked

    def dominant_color(self, frame):
        # Convertir a HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        red_lower1 = np.array([0, 70, 50])
        red_upper1 = np.array([10, 255, 255])
        red_lower2 = np.array([170, 70, 50])
        red_upper2 = np.array([180, 255, 255])

        yellow_lower = np.array([20, 70, 50])
        yellow_upper = np.array([30, 255, 255])

        green_lower = np.array([40, 70, 50])
        green_upper = np.array([70, 255, 255])

        # Crear máscaras
        mask_red1 = cv2.inRange(hsv, red_lower1, red_upper1)
        mask_red2 = cv2.inRange(hsv, red_lower2, red_upper2)
        mask_red = cv2.bitwise_or(mask_red1, mask_red2)

        mask_yellow = cv2.inRange(hsv, yellow_lower, yellow_upper)
        mask_green = cv2.inRange(hsv, green_lower, green_upper)

        # Sumar píxeles
        sum_red = np.sum(mask_red > 0)
        sum_yellow = np.sum(mask_yellow > 0)
        sum_green = np.sum(mask_green > 0)

        # Encontrar el color dominante
        max_sum = max(sum_red, sum_yellow, sum_green)

        if max_sum == sum_red:
            dominant = "RED"
        elif max_sum == sum_yellow:
            dominant = "YELLOW"
        else:
            dominant = "GREEN"

        print(f"The dominant color is {dominant}")

        # Crear una imagen vacía
        colored_frame = np.zeros_like(frame)

        # Pintar los píxeles según la máscara
        colored_frame[np.where(mask_red > 0)] = (0, 0, 255)       # Rojo en BGR
        colored_frame[np.where(mask_yellow > 0)] = (0, 255, 255)  # Amarillo en BGR
        colored_frame[np.where(mask_green > 0)] = (0, 255, 0)     # Verde en BGR

        return colored_frame



# --- MAIN ---
if __name__ == "__main__":
    
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()

    #ser = serial.Serial('/dev/ttyACM0', 9600)  
    cam = cv2.VideoCapture(0)
    vc = VideoCapture(cam, gui_ref=window)
    #vc.size = (400,600)
    vc.display_camera()

    cam.release()