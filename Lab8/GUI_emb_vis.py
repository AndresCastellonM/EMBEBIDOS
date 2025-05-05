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
        self.slider_max_hue.setProperty("value", 255)
        self.slider_max_hue.setOrientation(QtCore.Qt.Horizontal)
        self.slider_max_hue.setObjectName("slider_max_hue")
        self.Hue = QtWidgets.QLabel(self.centralwidget)
        self.Hue.setGeometry(QtCore.QRect(560, 50, 81, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.Hue.setFont(font)
        self.Hue.setObjectName("Hue")
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
        self.slider_max_sat.setProperty("value", 255)
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
        self.slider_max_val.setProperty("value", 255)
        self.slider_max_val.setOrientation(QtCore.Qt.Horizontal)
        self.slider_max_val.setObjectName("slider_max_val")
        self.RGB_cBox = QtWidgets.QCheckBox(self.centralwidget)
        self.RGB_cBox.setGeometry(QtCore.QRect(490, 460, 81, 20))
        self.RGB_cBox.setObjectName("RGB_cBox")
        self.HSV_cBox = QtWidgets.QCheckBox(self.centralwidget)
        self.HSV_cBox.setGeometry(QtCore.QRect(490, 480, 81, 20))
        self.HSV_cBox.setObjectName("HSV_cBox")
        self.GRAY_cBox = QtWidgets.QCheckBox(self.centralwidget)
        self.GRAY_cBox.setGeometry(QtCore.QRect(490, 500, 81, 20))
        self.GRAY_cBox.setObjectName("GRAY_cBox")
        self.MOTION_cBox = QtWidgets.QCheckBox(self.centralwidget)
        self.MOTION_cBox.setGeometry(QtCore.QRect(580, 460, 81, 20))
        self.MOTION_cBox.setObjectName("MOTION_cBox")
        self.EDGES_cbox = QtWidgets.QCheckBox(self.centralwidget)
        self.EDGES_cbox.setGeometry(QtCore.QRect(580, 480, 81, 20))
        self.EDGES_cbox.setObjectName("EDGES_cbox")
        self.BLUR_cBox = QtWidgets.QCheckBox(self.centralwidget)
        self.BLUR_cBox.setGeometry(QtCore.QRect(580, 500, 81, 20))
        self.BLUR_cBox.setObjectName("BLUR_cBox")
        self.DOM_COL_cBox = QtWidgets.QCheckBox(self.centralwidget)
        self.DOM_COL_cBox.setGeometry(QtCore.QRect(490, 520, 111, 20))
        self.DOM_COL_cBox.setObjectName("DOM_COL_cBox")
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
        self.Hue.setText(_translate("MainWindow", "LAYER 1"))
        self.label_2.setText(_translate("MainWindow", "min"))
        self.label_3.setText(_translate("MainWindow", "max"))
        self.label_4.setText(_translate("MainWindow", "max"))
        self.label_5.setText(_translate("MainWindow", "LAYER 2"))
        self.label_6.setText(_translate("MainWindow", "min"))
        self.label_7.setText(_translate("MainWindow", "max"))
        self.label_8.setText(_translate("MainWindow", "LAYER 3"))
        self.label_9.setText(_translate("MainWindow", "min"))
        self.RGB_cBox.setText(_translate("MainWindow", "RGB"))
        self.HSV_cBox.setText(_translate("MainWindow", "HSV"))
        self.GRAY_cBox.setText(_translate("MainWindow", "GRAY"))
        self.MOTION_cBox.setText(_translate("MainWindow", "MOTION"))
        self.EDGES_cbox.setText(_translate("MainWindow", "EDGES"))
        self.BLUR_cBox.setText(_translate("MainWindow", "BLUR"))
        self.EDGES_cbox.setText(_translate("MainWindow", "EDGES"))
        self.DOM_COL_cBox.setText(_translate("MainWindow", "DOM_COL"))


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
        self.selected_filters = []
        self.flag_change = 0
        self.handle_slider()

    def conectar_eventos(self):
        self.ui.slider_min_Hue.valueChanged.connect(self.handle_slider)
        self.ui.slider_max_hue.valueChanged.connect(self.handle_slider)
        self.ui.slider_min_sat.valueChanged.connect(self.handle_slider)
        self.ui.slider_max_sat.valueChanged.connect(self.handle_slider)
        self.ui.slider_min_val.valueChanged.connect(self.handle_slider)
        self.ui.slider_max_val.valueChanged.connect(self.handle_slider)
        self.ui.RGB_cBox.stateChanged.connect(self.handleCheckboxChange)
        self.ui.HSV_cBox.stateChanged.connect(self.handleCheckboxChange)
        self.ui.GRAY_cBox.stateChanged.connect(self.handleCheckboxChange)
        self.ui.MOTION_cBox.stateChanged.connect(self.handleCheckboxChange)
        self.ui.EDGES_cbox.stateChanged.connect(self.handleCheckboxChange)
        self.ui.BLUR_cBox.stateChanged.connect(self.handleCheckboxChange)        
        self.ui.DOM_COL_cBox.stateChanged.connect(self.handleCheckboxChange)

    def handle_slider(self):
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
        self.flag_change = 1

    def handleCheckboxChange(self):
        self.selected_filters = []
        if self.ui.RGB_cBox.isChecked():
            self.selected_filters.append("RGB")
        if self.ui.HSV_cBox.isChecked():
            self.selected_filters.append("HSV")
        if self.ui.GRAY_cBox.isChecked():
            self.selected_filters.append("GRAY")
        if self.ui.BLUR_cBox.isChecked():
            self.selected_filters.append("BLUR")
        if self.ui.EDGES_cbox.isChecked():
            self.selected_filters.append("EDGES")
        if self.ui.MOTION_cBox.isChecked():
            self.selected_filters.append("MOTION")
        if self.ui.DOM_COL_cBox.isChecked():
            self.selected_filters.append("DOM_COL")
        self.flag_change = 1
        
        print("Filtros seleccionados:", self.selected_filters)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()   # <-- instancias tu clase personalizada
    window.show()
    sys.exit(app.exec_())
