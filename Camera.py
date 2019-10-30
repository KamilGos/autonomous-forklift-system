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
        self.height = 318
        self.width  = 452
        self.initialized = False
        self.aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)
        self.aruco_parameters = aruco.DetectorParameters_create()
        self.aruco_parameters.adaptiveThreshConstant = 7
        self.aruco_parameters.polygonalApproxAccuracyRate = 0.03
        self.aruco_parameters.minMarkerPerimeterRate = 0.04
        self.MARKERS_VAL = 3

    def Initialize(self):
        if self.initialized == False:
            print("Initialize camera")
            self.cap = cv2.VideoCapture(self.cam_num)
            if (self.cap.isOpened() == False):
                print("Kamera nieosiagalna")
                self.initialized = False
            else:
                self.initialized = True
                _, self.frame = self.cap.read()

    def close_camera(self):
        print("CAMERA CLOSED")
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
            self.frame = self.get_frame()  # pobieram ramki dopóki nie znajdzie wszystkich aruco
            corners, ids, _ = aruco.detectMarkers(self.frame, self.aruco_dict, parameters=self.aruco_parameters)
            if np.all(ids != None):
                ids_number = len(ids)
                if ids_number != self.MARKERS_VAL: print("No enough markers. Is: ", ids_number, "  SB: ", self.MARKERS_VAL)
        return self.frame, corners, ids

    def Detect_Markers(self, frame):
        corners, ids, _ = aruco.detectMarkers(frame, self.aruco_dict, parameters=self.aruco_parameters)
        return corners, ids

    def Detect_Markers_Self(self):
        corners, ids, _ = aruco.detectMarkers(self.frame, self.aruco_dict, parameters=self.aruco_parameters)
        return self.frame, corners, ids

    def Get_Frame_And_Detect(self):
        self.get_frame()
        corners, ids = self.Detect_Markers(self.frame)
        return self.frame, corners, ids

    def Print_Detected_Markers(self, frame, corners, ids):
        frame = aruco.drawDetectedMarkers(frame, corners, ids)
        return frame

    def Print_Full_Road_On_Frame(self, frame, deleted_points, FULL_road, DONE_road):
        frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
        for point in FULL_road:
            cv2.circle(frame, tuple(point), 2, (255,0,0),2)
        for i in range(0,len(FULL_road)-1):
            cv2.line(frame, tuple(FULL_road[i]), tuple(FULL_road[i+1]), (255,0,0), 1)

        for point in DONE_road:
            cv2.circle(frame, tuple(point), 2, (0,255,0),2)
        if len(DONE_road)>1:
            for i in range(0, len(DONE_road) - 1):
                cv2.line(frame, tuple(DONE_road[i]), tuple(DONE_road[i + 1]), (0, 255, 0), 2)

        for point in deleted_points:
            cv2.circle(frame, tuple(point), 2, (252, 223, 3), 2)
        if len(deleted_points)>1:
            for i in range(0, len(deleted_points) - 1):
                cv2.line(frame, tuple(deleted_points[i]), tuple(deleted_points[i + 1]), (252, 223, 3), 2)

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
            self.msleep(100)
        if self.runperm == False:
            # self.cam.close_camera()
            # cv2.destroyAllWindows()
            print("Stop View1Thread")
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
            self.msleep(100)
        if self.runperm == False:
            # self.cam.close_camera()
            # cv2.destroyAllWindows()
            print("Stop View2Thread")
            self.exit(0)






