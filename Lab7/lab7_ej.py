import cv2
import os
import numpy as np
from abc import ABC, abstractmethod
from PyQt5 import QtCore, QtGui, QtWidgets
import sys


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.slider_min_Hue = QtWidgets.QSlider(self.centralwidget)
        self.slider_min_Hue.setGeometry(QtCore.QRect(560, 80, 160, 22))
        self.slider_min_Hue.setMaximum(255)
        self.slider_min_Hue.setOrientation(QtCore.Qt.Horizontal)
        self.slider_min_Hue.setObjectName("slider_min_Hue")
        self.slider_max_hue = QtWidgets.QSlider(self.centralwidget)
        self.slider_max_hue.setGeometry(QtCore.QRect(560, 120, 160, 22))
        self.slider_max_hue.setMaximum(255)
        self.slider_max_hue.setOrientation(QtCore.Qt.Horizontal)
        self.slider_max_hue.setObjectName("slider_max_hue")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(560, 50, 55, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(480, 90, 55, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(480, 120, 55, 16))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(480, 260, 55, 16))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(560, 190, 141, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.slider_min_sat = QtWidgets.QSlider(self.centralwidget)
        self.slider_min_sat.setGeometry(QtCore.QRect(560, 220, 160, 22))
        self.slider_min_sat.setMaximum(255)
        self.slider_min_sat.setOrientation(QtCore.Qt.Horizontal)
        self.slider_min_sat.setObjectName("slider_min_sat")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(480, 230, 55, 16))
        self.label_6.setObjectName("label_6")
        self.slider_max_sat = QtWidgets.QSlider(self.centralwidget)
        self.slider_max_sat.setGeometry(QtCore.QRect(560, 260, 160, 22))
        self.slider_max_sat.setMaximum(255)
        self.slider_max_sat.setOrientation(QtCore.Qt.Horizontal)
        self.slider_max_sat.setObjectName("slider_max_sat")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(480, 410, 55, 16))
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(560, 340, 101, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.slider_min_val = QtWidgets.QSlider(self.centralwidget)
        self.slider_min_val.setGeometry(QtCore.QRect(560, 370, 160, 22))
        self.slider_min_val.setMaximum(255)
        self.slider_min_val.setOrientation(QtCore.Qt.Horizontal)
        self.slider_min_val.setObjectName("slider_min_val")
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(480, 380, 55, 16))
        self.label_9.setObjectName("label_9")
        self.slider_max_val = QtWidgets.QSlider(self.centralwidget)
        self.slider_max_val.setGeometry(QtCore.QRect(560, 410, 160, 22))
        self.slider_max_val.setMaximum(255)
        self.slider_max_val.setOrientation(QtCore.Qt.Horizontal)
        self.slider_max_val.setObjectName("slider_max_val")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "HUE"))
        self.label_2.setText(_translate("MainWindow", "min"))
        self.label_3.setText(_translate("MainWindow", "max"))
        self.label_4.setText(_translate("MainWindow", "max"))
        self.label_5.setText(_translate("MainWindow", "SATURATION"))
        self.label_6.setText(_translate("MainWindow", "min"))
        self.label_7.setText(_translate("MainWindow", "max"))
        self.label_8.setText(_translate("MainWindow", "VALUE"))
        self.label_9.setText(_translate("MainWindow", "min"))


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.conectar_eventos()
        self.min_h = 0
        self.max_h = 255
        self.min_s = 0
        self.max_s = 255
        self.min_v = 0
        self.max_v = 255
        self.actualizar_valores()

    def conectar_eventos(self):
        self.ui.slider_min_Hue.valueChanged.connect(self.actualizar_valores)
        self.ui.slider_max_hue.valueChanged.connect(self.actualizar_valores)
        self.ui.slider_min_sat.valueChanged.connect(self.actualizar_valores)
        self.ui.slider_max_sat.valueChanged.connect(self.actualizar_valores)
        self.ui.slider_min_val.valueChanged.connect(self.actualizar_valores)
        self.ui.slider_max_val.valueChanged.connect(self.actualizar_valores)

    def actualizar_valores(self):
        self.min_h = self.ui.slider_min_Hue.value()
        self.max_h = self.ui.slider_max_hue.value()
        self.min_s = self.ui.slider_min_sat.value()
        self.max_s = self.ui.slider_max_sat.value()
        self.min_v = self.ui.slider_min_val.value()
        self.max_v = self.ui.slider_max_val.value()

        self.lower_hsv = np.array([self.min_h, self.min_s, self.min_v])
        self.upper_hsv = np.array([self.max_h, self.max_s, self.max_v])
        print(f"Rango HSV Inferior: {self.lower_hsv}")
        print(f"Rango HSV Superior: {self.upper_hsv}")

# Crea carpeta si no existe
if not os.path.exists("Captures"):
    os.makedirs("Captures")

# --- Punto 1 ---
def show_and_print_color(image_path, color_name):
    img = cv2.imread(image_path)
    #img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_rgb = img
    print(f"The image is {color_name}, average RGB: {np.mean(img_rgb, axis=(0,1)).astype(int)}")
    cv2.imshow(color_name, img_rgb)
    while cv2.waitKey(1) != 27: pass
    cv2.destroyAllWindows()
    return img_rgb

# --- Punto 2 ---
def convert_to_gray(image):
    return cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

# --- Punto 3 ---
class ImageMaster:
    def __init__(self, image):
        self.image = image

    def transform(self):
        image_rgb = self.image
        image_gray = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2GRAY)
        image_hsv = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2HSV)
        return image_rgb, image_gray, image_hsv

# --- Punto 4 y 5 y 6 ---
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

    def display_camera(self):
        self.displayed = True
        self.camera_RGBgray()

    def stop_display(self):
        self.displayed = False
        cv2.destroyAllWindows()

    def save_frame(self, frame):
        self.capture_count += 1
        filename = f"Captures/image{self.capture_count}.jpg"
        cv2.imwrite(filename, frame)
        print(f"[INFO] Imagen guardada: {filename}")

    def camera_visualization(self):
        while self.displayed:
            ret, frame = self.camera.read()
            if not ret:
                print("[ERROR] No se pudo leer el frame")
                break
            cv2.imshow("Camera", frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('c'):
                self.save_frame(frame)
            elif key == 27:  # ESC
                self.stop_display()

    def camera_color(self, color):
        self.displayed = True
        lower, upper = None, None

        if color == "red":
            lower = np.array([0, 100, 100])
            upper = np.array([10, 255, 255])
        elif color == "green":
            lower = np.array([50, 100, 100])
            upper = np.array([70, 255, 255])
        elif color == "blue":
            lower = np.array([100, 100, 100])
            upper = np.array([130, 255, 255])
        else:
            print(f"[ERROR] Color no válido: {color}")
            return

        while self.displayed:
            ret, frame = self.camera.read()
            if not ret:
                break
            hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
            mask = cv2.inRange(hsv, lower, upper)
            image_masked = cv2.bitwise_and(hsv, hsv, mask=mask)
            image_masked = cv2.cvtColor(image_masked, cv2.COLOR_HSV2RGB)
            cv2.imshow(f"Detecting {color}", image_masked)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('c'):
                self.save_frame(image_masked)
            elif key == 27:
                self.stop_display()
    
    def camera_color2(self):
        self.displayed = True

        while self.displayed:
            lower = np.array([self.gui.min_h, self.gui.min_s, self.gui.min_v])
            upper = np.array([self.gui.max_h, self.gui.max_s, self.gui.max_v])
            ret, frame = self.camera.read()
            if not ret:
                break
            hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
            mask = cv2.inRange(hsv, lower, upper)
            image_masked = cv2.bitwise_and(hsv, hsv, mask=mask)
            image_masked = cv2.cvtColor(image_masked, cv2.COLOR_HSV2RGB)
            cv2.imshow(f"Detecting", image_masked)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('c'):
                self.save_frame(image_masked)
            elif key == 27:
                self.stop_display()

    def camera_RGBgray(self):
        toggle = 0
        while self.displayed:
            ret, frame = self.camera.read()
            if not ret:
                break
            if toggle == 0:
                frame_out = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            else:
                frame_out = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame_out = frame
            cv2.imshow("Camera", frame_out)
            key = cv2.waitKey(1) & 0xFF
            if key == ord(' '):
                toggle = (toggle + 1) % 2
            elif key == ord('c'):
                self.save_frame(frame_out)
            elif key == 27:
                self.stop_display()

# --- MAIN ---
if __name__ == "__main__":
    '''
    #red = show_and_print_color("colors/red.jpeg", "Red")
    #blue = show_and_print_color("colors/blue.png", "Blue")
    #green = show_and_print_color("colors/green.jpg", "Green")
    #gray_red = convert_to_gray(red)
    '''

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()  # Esta es tu clase de lógica
    window.show()

    cam = cv2.VideoCapture(0)
    vc = VideoCapture(cam, gui_ref=window)
    vc.display_camera()
    #vc.camera_color("red")
    #vc.camera_color("green")
    #vc.camera_color("blue")

    vc.camera_color2()

    cam.release()
    
    
    sys.exit(app.exec_())