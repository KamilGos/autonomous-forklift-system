from PyQt5.QtCore import Qt, QThread, QTimer, QRect, QMetaObject, QCoreApplication, pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QVBoxLayout, QApplication, QSlider, QHBoxLayout, QMenuBar, QMenu, QAction, QLabel, QSizePolicy
from PyQt5.QtGui import QImage, QColor
from pyqtgraph import ImageView
import numpy as np
import cv2
import cv2.aruco as aruco
from views import Ui_MainWindow

import Camera


class Main_function(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.camera = Camera.Camera(1)
        self.pushButton_View1.clicked.connect(self.start_View1)
        self.View1isRunning = False

    def update_View1_frame(self, frame):
        self.image_view.setImage(frame.T)

    def Terminate_Thread_View1(self):
        self.camera.close_camera()

    def start_View1(self):
        if self.View1isRunning == False:
            if self.camera.initialized == False: self.camera.initialize()
            if self.camera.initialized == True:
                self.View1Thread = Camera.VideoStreem_View1_Thread(self.camera)
                self.View1isRunning = True
                self.pushButton_View1.setText("View1 - Running")
                self.pushButton_View1.setStyleSheet("background-color: #A9F5A9")
                self.pushButton_View2.setEnabled(False)
                self.pushButton_View3.setEnabled(False)
                self.View1Thread.start()
                self.View1Thread.sig1.connect(self.update_View1_frame)

        else:
            self.View1Thread.terminate()
            self.View1isRunning = False
            self.camera.close_camera()
            self.camera.initialized = False
            self.pushButton_View1.setText("View1")
            self.pushButton_View1.setStyleSheet("background-color: DEFAULT <later on>")
            self.pushButton_View2.setEnabled(True)
            self.pushButton_View3.setEnabled(True)


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    MainWindow = Main_function()
    MainWindow.show()
    app.exit(app.exec_())