from PyQt5.QtCore import  QThread,  pyqtSignal
import numpy as np
import cv2
import cv2.aruco as aruco

class Camera:
    def __init__(self, cam_num):
        print("Tworzę klasę Camera")
        self.cam_num = cam_num
        self.cap = None
        self.frame = np.zeros((1,1))
        self.height = None
        self.width = None
        self.initialized = False
        self.aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)
        self.aruco_parameters = aruco.DetectorParameters_create()
        self.aruco_parameters.adaptiveThreshConstant = 7
        self.aruco_parameters.polygonalApproxAccuracyRate = 0.03
        self.aruco_parameters.minMarkerPerimeterRate = 0.04
        self.MARKERS_VAL = 3

    def Initialize(self):
        self.cap = cv2.VideoCapture(self.cam_num)
        if (self.cap.isOpened() == False):
            print("Kamera nieosiagalna")
            self.initialized = False
        else:
            self.initialized = True
            _, self.frame = self.cap.read()
            self.height, self.width, _ = self.frame.shape  # get size of picture

    def close_camera(self):
        self.cap.release()
        self.initialized = False

    def get_frame(self):
        _,self.frame = self.cap.read()
        self.frame = self.frame[85:403, 80:532]
        self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        return self.frame

    def get_frame_while(self):
        ids_number = 0
        while ids_number != self.MARKERS_VAL:
            frame = self.get_frame()  # pobieram ramki dopóki nie znajdzie wszystkich aruco
            corners, ids, _ = aruco.detectMarkers(frame, self.aruco_dict, parameters=self.parameters)
            if np.all(ids != None):
                ids_number = len(ids)
                if ids_number != self.MARKERS_VAL: print("No enough markers. Is: ", ids_number, "  SB: ", self.MARKERS_VAL)
        return frame, corners, ids

    def Detect_Markers(self, frame):
        corners, ids, _ = aruco.detectMarkers(frame, self.aruco_dict, parameters=self.aruco_parameters)
        return corners, ids

    def Print_Detected_Markers(self, frame, corners, ids):
        frame = aruco.drawDetectedMarkers(frame, corners, ids)
        return frame


    def __str__(self):
        return  "OpenCV Camera {}".format(self.cam_num)


class VideoStreem_View1_Thread(QThread):
    """
    Real, clean view from camera.
    """
    sig_View1_Thread_frame = pyqtSignal(object)

    def __init__(self, camera):
        QThread.__init__(self)
        self.cam = camera
        self.runperm = True

    def run(self):
        print("Start View1Thread")
        while self.runperm:
            self.frame = self.cam.get_frame()
            self.sig_View1_Thread_frame.emit(self.frame)
            self.msleep(50)
        if self.runperm == False:
            self.cam.close_camera()
            cv2.destroyAllWindows()
            self.exit(0)


class VideoStreem_View2_Thread(QThread):
    sig_View2_Thread_frame = pyqtSignal(object)

    def __init__(self, camera):
        QThread.__init__(self)
        self.cam = camera
        self.runperm = True

    def run(self):
        print("Start View2Thread")
        while self.runperm:
            self.frame = self.cam.get_frame()
            corners, ids = self.cam.Detect_Markers(self.frame)
            if np.all(ids!=None):
                self.frame = self.cam.Print_Detected_Markers(self.frame, corners, ids)
            self.sig_View2_Thread_frame.emit(self.frame)
            self.msleep(50)
        if self.runperm == False:
            self.cam.close_camera()
            cv2.destroyAllWindows()
            self.exit(0)






