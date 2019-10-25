from PyQt5.QtCore import  QThread,  pyqtSignal
import numpy as np
import cv2
import cv2.aruco as aruco

class Camera:
    def __init__(self, cam_num):
        self.cam_num = cam_num
        self.cap = None
        self.frame = np.zeros((1,1))
        self.height = None
        self.width = None
        self.initialized = False

    def initialize(self):
        self.cap = cv2.VideoCapture(self.cam_num)
        if (self.cap.isOpened() == False):
            print("Kamera nieosiagalna")
            self.initialized = False
        else:
            self.initialized = True
            ret, self.frame = self.cap.read()
            self.height, self.width, _ = self.frame.shape  # get size of picture

    def close_camera(self):
        self.cap.release()

    def get_frame(self):
        ret, self.frame = self.cap.read()
        self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        return self.frame

    def __str__(self):
        return  "OpenCV Camera {}".format(self.cam_num)


class VideoStreem_View1_Thread(QThread):
    sig1 = pyqtSignal(object)

    def __init__(self, camera):
        QThread.__init__(self)
        self.cam = camera

    def run(self):
        print("Start View1Thread")
        while True:
            self.frame = self.cam.get_frame()
            self.sig1.emit(self.frame)
            self.msleep(50)









