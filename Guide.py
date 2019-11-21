import cv2
from PyQt5.QtCore import  QThread,  pyqtSignal, QTimer
import numpy as np
import Trajectory
import Communication
import Camera
import Calculations
import copy
from cv2 import aruco
class Guide:
    def __init__(self, camera, FPTV_FACTOR, PORT_COM, BAUDRATE):
        print("Tworzę klasę Guide")
        self.guide_ready = False
        self.camera = camera
        print(self.camera.initialized)
        self.calculation = Calculations.Calculations()
        self.Trajectory = Trajectory.Trajectory(FPTV_FACTOR, self.camera.bigwidth, self.camera.bigheight, self.calculation)
        self.communication = Communication.Communication()
        self.communication.Initialize(PORT_COM, BAUDRATE)
        if self.camera.initialized == True and self.communication.initializated == True:
            self.guide_ready = True
            print("Guide is ready")

class Guide_Thread(QThread):
    sig_Guide_Thread_Frame_With_Road = pyqtSignal(object)
    sig_Guide_Thread_ProgressBar_MaxValue = pyqtSignal(int)
    sig_Guide_Thread_ProgressBar_NewValue = pyqtSignal(int)
    sig_Guide_Thread_Initialized = pyqtSignal(str)
    sig_Guide_Thread_Phase1 = pyqtSignal(int)
    sig_Guide_Thread_Phase2 = pyqtSignal(int)
    sig_Guide_Thread_Errors = pyqtSignal(int)
    sig_Guide_Thread_Error_STOP = pyqtSignal(int)
    sig_Guide_Thread_Update_Warehouse = pyqtSignal(int)

    def __init__(self, camera, guide_class,id_robot, id_pallet, MIN_DISTANCE, MIN_ANGLE, VIEV_IS_RUNNING):
        QThread.__init__(self)
        self.runperm = True
        self.camera = camera
        self.id_robot = id_robot
        self.id_aim = None
        self.id_pallet = id_pallet
        self.id_warehouse = 26
        self.MIN_DISTANCE_CONST = MIN_DISTANCE
        self.MIN_DISTANCE_LAST_CONST = 15
        self.MIN_DISTANCE = self.MIN_DISTANCE_CONST
        self.MIN_ANGLE = MIN_ANGLE
        self.GuideT = guide_class
        self.VIEW_IS_RUNNING = VIEV_IS_RUNNING
        self.DONE_road = []
        self.deleted_points = []
        self.shortest_path_coor=[]
        self.cpframe = np.zeros((1,1))
        self.point_iterator = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.Send_View3_Frame)
        self.timer.start(100)

    def run(self):
        self.sig_Guide_Thread_Initialized.emit(str("OK"))
        print("Start Guide_Thread")
        self.id_aim = self.id_pallet
        self.sig_Guide_Thread_Phase1.emit(1)  # phase 1 running
        if self.GO_FROM_A_TO_B(self.id_aim, self.id_pallet) == False:
            self.sig_Guide_Thread_Phase1.emit(3)  # phase 1 error
            self.sig_Guide_Thread_Errors.emit(1)

            print("***** TRASA NIEBEZPIECZNA ******")
            self.exit(0)
            self.sig_Guide_Thread_Error_STOP.emit(0)

        self.CALIBRATE_ROTATION(self.deleted_points[0])
        self.GuideT.communication.Send_Take_Pallet(0)
        self.camera.MARKERS_VAL=self.camera.MARKERS_VAL-1
        self.DONE_road = []
        self.deleted_points = []
        self.shortest_path_coor = []
        if self.GuideT.communication.Read_Data_From_Robot()== True:
            self.sig_Guide_Thread_Phase1.emit(2) #phase 1 done
            self.id_aim = self.id_warehouse
            print("okok")
            self.sig_Guide_Thread_Phase2.emit(1)  # phase 2 running
            if self.GO_FROM_A_TO_B(self.id_aim, self.id_pallet) == False:
                self.sig_Guide_Thread_Phase2.emit(3)  # phase 2 error
                self.sig_Guide_Thread_Errors.emit(1)

                print("***** TRASA NIEBEZPIECZNA ******")
                self.exit(0)
                self.sig_Guide_Thread_Error_STOP.emit(0)

            self.CALIBRATE_ROTATION(self.deleted_points[0])
            self.GuideT.communication.Send_Put_Pallet(0)
            if self.GuideT.communication.Read_Data_From_Robot() == True:
                self.sig_Guide_Thread_Phase2.emit(2)  # phase 2 done
                self.sig_Guide_Thread_Update_Warehouse.emit(self.id_pallet)
                print("*** ZAKOŃCZONO PROCES PALETYZACJI ***")
                print(" *** PALETA ODŁOŻONA NA POZIOM 0 ***")
                print("  *** ZAMYKAM WĄTEK PALETYZACJI ***")
                self.sig_Guide_Thread_Error_STOP.emit(0)


    def GO_FROM_A_TO_B(self, id_aim, id_pallet):
        print("Rozpoczynam jazdę")
        self.point_iterator = 0
        frame, corners, ids = self.GET_FRAME()
        try:
            self.shortest_path_coor, is_safe = self.GuideT.Trajectory.Set_Route_Between_Points(corners, ids, self.id_robot,
                                                                                      id_aim, id_pallet)
        except:
            print("Błąd wyszukiwania trasy")
            return False

        if is_safe != True:
            print("Road is not safe!")
            return False

        last_idx = self.GuideT.calculation.Check_Last_Point(self.shortest_path_coor) + 1
        for i in range(last_idx):
            self.deleted_points.append(self.shortest_path_coor.pop(len(self.shortest_path_coor) - 1))
        self.deleted_points.append(self.shortest_path_coor[len(self.shortest_path_coor) - 1])
        self.sig_Guide_Thread_ProgressBar_MaxValue.emit(((len(self.shortest_path_coor) - 1) - last_idx))
        self.DONE_road.append(self.shortest_path_coor[0])
        self.sig_Guide_Thread_Frame_With_Road.emit(
            self.camera.Print_Full_Road_On_Frame(frame, self.deleted_points, self.shortest_path_coor, self.DONE_road))


        if is_safe == True:
            for point in self.shortest_path_coor:
                self.point_iterator += 1
                print("Iterator:", self.point_iterator)
                print("MAX:", len(self.shortest_path_coor) - last_idx)
                if self.point_iterator == len(self.shortest_path_coor) - last_idx: #ostatni punkt
                    self.MIN_DISTANCE=self.MIN_DISTANCE_LAST_CONST
                    print("Zmieniam minimalny dystans")
                self.sig_Guide_Thread_ProgressBar_NewValue.emit((self.point_iterator - 2))
                NEXT_POINT = False
                while NEXT_POINT == False:
                    frame, corners, ids, corners_ids_dict, Rob_center = self.GET_FRAME_EASY_AND_CREATE_DICT()
                    self.DONE_road.append(Rob_center[0])
                    self.sig_Guide_Thread_Frame_With_Road.emit(
                        self.camera.Print_Full_Road_On_Frame(frame, self.deleted_points, self.shortest_path_coor,
                                                             self.DONE_road))
                    # print("A=", corners_ids_dict[str(self.id_robot)])
                    # print("B=", point)
                    distance = self.GuideT.calculation.Calculate_Distance_RA(corners_ids_dict[str(self.id_robot)],
                                                                             point)
                    print("Distance = ", distance)
                    if distance > self.MIN_DISTANCE:  # Trzeba dojechac do tego punktu (nie pomijamy go)
                        print("Za duży dystans")
                        angle, dir = self.GuideT.calculation.Calculate_Angle_RA(corners_ids_dict[str(self.id_robot)],
                                                                                point)
                        print("Kąt = ", angle)
                        while angle > self.MIN_ANGLE and angle < (360 - self.MIN_ANGLE):  # musimy się obrócić
                            print("Zły kąt")
                            self.GuideT.communication.Send_Rotate(angle, dir)
                            try:
                                if self.GuideT.communication.Read_Data_From_Robot() == True:
                                    frame, corners, ids, corners_ids_dict, Rob_center = self.GET_FRAME_EASY_AND_CREATE_DICT()
                                    self.DONE_road.append(Rob_center[0])
                                    self.sig_Guide_Thread_Frame_With_Road.emit(
                                        self.camera.Print_Full_Road_On_Frame(frame, self.deleted_points, self.shortest_path_coor,
                                                                         self.DONE_road))
                                    angle, dir = self.GuideT.calculation.Calculate_Angle_RA(
                                    corners_ids_dict[str(self.id_robot)], point)
                                    print("Nowy kąt = ", angle)
                            except:
                                print("Błąd 174")
                        print("Poprawny kąt")
                        self.GuideT.communication.Send_Go_Straight(distance)
                        try:
                            ACK = self.GuideT.communication.Read_Data_From_Robot()
                        except: print("Błąd 179")
                        print("I got ACK after Go Straight")
                    else:  # Dojechał do punktu
                        print("Biorę kolejny punkt")
                        NEXT_POINT = True
        else:
            print("Trasa niebezpieczna")
            return False
        print("Kończę fazę GUIDE")
        self.MIN_DISTANCE = self.MIN_DISTANCE_CONST
        return True

    def CALIBRATE_ROTATION(self, point):
        print("Rozpoczynam kalibrację kąta")
        frame, corners, ids, corners_ids_dict, Rob_center = self.GET_FRAME_EASY_AND_CREATE_DICT()
        angle, dir = self.GuideT.calculation.Calculate_Angle_RA(corners_ids_dict[str(self.id_robot)], point)
        print("Kąt = ", angle)
        while angle > 1 and angle < 359:  # musimy się obrócić
            print("Zły kąt")
            self.GuideT.communication.Send_Rotate(angle, dir)
            if self.GuideT.communication.Read_Data_From_Robot() == True:
                frame, corners, ids, corners_ids_dict, Rob_center = self.GET_FRAME_EASY_AND_CREATE_DICT()
                angle, dir = self.GuideT.calculation.Calculate_Angle_RA(
                    corners_ids_dict[str(self.id_robot)], point)
                print("Nowy kąt = ", angle)
        print("Poprawny kąt. Kończę kalibrację")
        return True

    def GET_FRAME(self):
        if self.VIEW_IS_RUNNING == False:
            frame, corners, ids = self.camera.get_frame_while()
        else:  # kamera juz dziala czyli korzysamy z ramek bez pobierania nowych
            ids = []
            while len(ids) != self.GuideT.camera.MARKERS_VAL:
                frame, corners, ids = self.camera.Detect_Markers_Self()
        return frame, corners, ids


    def GET_FRAME_ONLY(self):
        frame = self.camera.get_frame()
        corners, ids = self.camera.Detect_Markers(frame)
        frame = aruco.drawDetectedMarkers(frame, corners[:-1], ids[:-1])
        return frame

    def GET_FRAME_EASY_AND_CREATE_DICT(self):
        frame, corners, ids = self.GET_FRAME()
        corners, ids = self.GuideT.calculation.Easy_Corners_And_Ids(corners, ids)
        corners_ids_dict = self.GuideT.calculation.Create_Dictionary_Of_Corners(corners, ids)
        Rob_center = self.GuideT.calculation.Get_Centers_Of_Corners(np.array([corners_ids_dict[str(self.id_robot)]]))
        return frame, corners, ids, corners_ids_dict, Rob_center


    def Send_View3_Frame(self):
        if len(self.shortest_path_coor)>0 and len(self.deleted_points)>0 and len(self.DONE_road)>0:
            self.cpframe = self.GET_FRAME_ONLY()
            self.sig_Guide_Thread_Frame_With_Road.emit(
                self.camera.Print_Full_Road_On_Frame(self.cpframe, self.deleted_points, self.shortest_path_coor, self.DONE_road))
        else: print("Brak")


if __name__ == "__main__":
    cam = Camera.Camera(1)
    Guide = Guide(cam, 25, "COM14", 9600)
    Guide.Guide_Robot_To_Aim(0,2,30,3)