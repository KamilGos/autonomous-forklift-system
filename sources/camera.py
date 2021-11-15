from PyQt5.QtCore import  QThread,  pyqtSignal
import numpy as np
import cv2
import cv2.aruco as aruco
import sources.calculations as calculations
from scipy.spatial import distance
import math

class Camera:
    """Handling all operations of the camera
    """
    def __init__(self, cam_num):
        self.cam_num = cam_num
        self.cap = None
        self.frame = np.zeros((1,1))
        self.bigleft =60 
        self.bigright = 575
        self.bigtop = 70
        self.bigbottom = 440
        self.smallleft = 30  
        self.smallright = 484  
        self.smalltop = 37  
        self.smallbottom = 355 
        self.bigheight = self.bigbottom-self.bigtop
        self.bigwidth  = self.bigright-self.bigleft
        self.initialized = False
        self.aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)
        self.aruco_parameters = aruco.DetectorParameters_create()
        self.aruco_parameters.adaptiveThreshConstant = 7
        self.aruco_parameters.polygonalApproxAccuracyRate = 0.03
        self.aruco_parameters.minMarkerPerimeterRate = 0.04
        self.MARKERS_VAL = 1+1
        self.DONE_MARKERS = 0
        self.Warehouse_corners = np.array([[[350,85],[380,85],[380,115],[350,115]]])
        self.Warehouse_place = np.array([[[420,80],[460,80],[460,120],[420,120]]])
        self.pts1 = np.float32([[33, 23], [485, 24], [485, 337], [27, 340]])
        self.pts2 = np.float32([[0, 0], [455,0], [455, 316], [0, 316]])
        self.TransformMatrix=cv2.getPerspectiveTransform(self.pts1, self.pts2)
        self.SKALA = 2.23  # mm
        self.CAMERA_HEIGHT = 1530  # mm
        self.ROBOT_HEIGHT = 150 # mm
        self.map_center = (int(self.bigwidth / 2), int(self.bigheight / 2))
        print(self.map_center)
        self.Calculations = calculations.Calculations()
        self.Warehouse_place_center = self.Calculations.Get_Centers_Of_Corners(self.Warehouse_place)[0]

        self.callibration_matrix = np.array([[733.65108925, 0, 341.18570973],
                        [0, 733.86740229, 229.70186298],
                        [0, 0, 1.]])
        self.callibration_coef = np.array([[-0.00808862, -0.68700529, 0.00278835, 0.00466333, 1.65299464]])


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
        self.frame = cv2.undistort(self.frame, self.callibration_matrix, self.callibration_coef, None, self.callibration_matrix)

        self.frame = self.frame[self.bigtop:self.bigbottom, self.bigleft:self.bigright]
        cv2.circle(self.frame, tuple(self.map_center), 3, (255,255,255))
        self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        return self.frame

    def get_frame_while(self):
        ids_number = 0
        try:
            while ids_number < (self.MARKERS_VAL-self.DONE_MARKERS):
                self.frame = self.get_frame()  # pobieram ramki dopóki nie znajdzie wszystkich aruco
                corners, ids = self.Detect_Markers(self.frame)
                if np.all(ids != None):
                    ids_number = len(ids)
                    if ids_number < self.MARKERS_VAL: print("No enough markers. Is: ", ids_number, "  SB: ", self.MARKERS_VAL)

            return self.frame, corners, ids
        except:
            print("get frame while error")

    def Detect_Markers(self, frame):
        corners, ids, _ = aruco.detectMarkers(frame, self.aruco_dict, parameters=self.aruco_parameters)
        if np.all(ids != None):
            ecorners, eids = self.Calculations.Easy_Corners_And_Ids(corners, ids)
            dict = self.Calculations.Create_Dictionary_Of_Corners(ecorners, eids)
            ids = ids.tolist()
            if [0] in ids:
                idx = ids.index([0])
                new_corners = np.array(self.Delete_Perspective_ArUcos(dict[str('0')]))
                # print(len(new_corners))
                if len(new_corners)==4:
                    # print(corners)
                    # print("nw", new_corners)
                    corners[idx][0] = new_corners

        corners.append(self.Warehouse_corners)
        ids = np.append(ids, [26])
        for point in self.Warehouse_place[0]:
            cv2.circle(self.frame, tuple(point), 1, (252, 223, 3), 2)
        for i in range(0,3):
            cv2.rectangle(self.frame, tuple(self.Warehouse_place[0][i]), tuple(self.Warehouse_place[0][i+1]),(255,255,255),1)
        cv2.rectangle(self.frame, tuple(self.Warehouse_place[0][0]), tuple(self.Warehouse_place[0][3]),
                      (255, 255, 255), 1)
        cv2.circle(self.frame, tuple(self.Warehouse_place_center), 3, (0,0,0), 3)

        return corners, ids

    def Detect_Markers_Self(self):
        corners, ids = self.Detect_Markers(self.frame, parameters=self.aruco_parameters)
        corners.append(self.Warehouse_corners)
        ids = np.append(ids, [26])
        return self.frame, corners, ids

    def Return_Self_Frame(self):
        return self.frame

    def Get_Frame_And_Detect(self):
        self.get_frame()
        corners, ids = self.Detect_Markers(self.frame)
        return self.frame, corners, ids

    def Print_Detected_Markers(self, frame, corners, ids):
        frame = aruco.drawDetectedMarkers(frame, corners[:-1], ids[:-1])
        frame = cv2.warpPerspective(frame, self.TransformMatrix, (455,316))

        #frame = aruco.drawDetectedMarkers(frame, corners, ids)
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

    def Calculate_Perspective_Error(self, corners):
        try:
            centers = self.Calculations.Get_Centers_Of_Corners([corners])
            dist = int(distance.euclidean(self.map_center, centers[0]))
            real_dist = dist * self.SKALA
            diff = (real_dist * self.ROBOT_HEIGHT) / self.CAMERA_HEIGHT
            diff = diff / self.SKALA
            return diff, centers[0]
        except:
            print("calculate perspective error")

    def Delete_Perspective_ArUcos(self, corners):
        try:
            error, center = self.Calculate_Perspective_Error(corners)
            alpha_angle = self.Calculations.Determine_Angle_XY((center[0] - self.map_center[0]), (center[1] - self.map_center[1]))
            if alpha_angle >= 0 and alpha_angle < 90:  # I ćwiartka
                beta_angle = 90 - alpha_angle
                # print("I")
            elif alpha_angle >= 90 and alpha_angle < 180:  # II ćwiartka
                beta_angle = alpha_angle - 90
                # print("II")
            elif alpha_angle >= 180 and alpha_angle < 270:  # 3 ćwiartka
                beta_angle = 270 - alpha_angle
                # print("III")
            elif alpha_angle >= 270 and alpha_angle <= 360:  # IV ćwiartka
                beta_angle = alpha_angle - 270
                # print("IV")

            X = int(error * math.sin(math.radians(beta_angle)))
            Y = int(error * math.cos(math.radians(beta_angle)))
            #print("X,Y:", X,Y)

            new_corners = []
            for point in corners:
                # print(point[0], point[1])
                if   point[0] >= self.map_center[0] and point[1] <= self.map_center[1]:  # I ćwiartka
                    new_corners.append([int(point[0] - X), int(point[1] + Y)])
                    #print("I")
                elif point[0] <= self.map_center[0] and point[1] <= self.map_center[1]:  # II ćwiartka
                    new_corners.append([int(point[0] + X), int(point[1] + Y)])
                    #print("II")
                elif point[0] <= self.map_center[0] and point[1] >= self.map_center[1]:  # III ćwiartka
                    new_corners.append([int(point[0] + X), int(point[1] - Y)])
                    #print("III")
                elif point[0] >= self.map_center[0] and point[1] >= self.map_center[1]:  # IV ćwiartka
                    new_corners.append([int(point[0] - X), int(point[1] - Y)])
                    # print("IV")
            return new_corners
        except:
            print("delete perspective error")
    def __str__(self):
        return  "OpenCV Camera {}".format(self.cam_num)


class VideoStreem_View1_Thread(QThread):
    """Real, clean view from camera.
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
            print("Stop View2Thread")
            self.exit(0)




