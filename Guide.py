import cv2
from PyQt5.QtCore import  QThread,  pyqtSignal
import numpy as np
import Trajectory
import Communication
import Camera
import Calculations

class Guide:
    def __init__(self, camera, FPTV_FACTOR, PORT_COM, BAUDRATE):
        print("Tworzę klasę Guide")
        self.guide_ready = False
        self.camera = camera
        print(self.camera.initialized)
        self.calculation = Calculations.Calculations()
        self.Trajectory = Trajectory.Trajectory(FPTV_FACTOR, self.camera.width, self.camera.height, self.calculation)
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


    def __init__(self, camera, guide_class,id_robot, id_aim, MIN_DISTANCE, MIN_ANGLE, VIEV_IS_RUNNING):
        QThread.__init__(self)
        self.runperm = True
        self.camera = camera
        self.id_robot = id_robot
        self.id_aim = None
        self.id_pallet = id_aim
        self.id_warehouse = 26
        self.MIN_DISTANCE = MIN_DISTANCE
        self.MIN_ANGLE = MIN_ANGLE
        self.GuideT = guide_class
        self.VIEW_IS_RUNNING = VIEV_IS_RUNNING
        self.DONE_road = []
        self.point_iterator = 0
        self.deleted_points = []
        # print("Koniec init")


    def run(self):
        self.sig_Guide_Thread_Initialized.emit(str("OK"))
        print("Start Guide_Thread")
        self.id_aim = self.id_pallet
        if self.GO_FROM_A_TO_B(self.id_aim, self.id_pallet) == False:
            print("***** TRASA NIEBEZPIECZNA ******")
            self.exit(0)
        self.CALIBRATE_ROTATION(self.deleted_points[0])
        self.GuideT.communication.Send_Take_Pallet(0)
        if self.GuideT.communication.Read_Data_From_Robot()== True:
            self.id_aim = self.id_warehouse
            self.GO_FROM_A_TO_B(self.id_aim, self.id_pallet)
            self.CALIBRATE_ROTATION(self.deleted_points[0])
            self.GuideT.communication.Send_Put_Pallet(0)
            if self.GuideT.communication.Read_Data_From_Robot() == True:
                print("*** ZAKOŃCZONO PROCES PALETYZACJI ***")
                print(" *** PALETA ODŁOŻONA NA POZIOM 0 ***")
                print("  *** ZAMYKAM WĄTEK PALETYZACJI ***")

    def GO_FROM_A_TO_B(self, id_aim, id_pallet):
        print("Rozpoczynam jazdę")
        self.deleted_points = []
        frame, corners, ids = self.GET_FRAME()
        shortest_path_coor, is_safe = self.GuideT.Trajectory.Set_Route_Between_Points(corners, ids, self.id_robot,
                                                                                      id_aim, id_pallet)

        print("Road is safe? -> ", is_safe)
        last_idx = self.GuideT.calculation.Check_Last_Point(shortest_path_coor) + 1

        for i in range(last_idx):
            self.deleted_points.append(shortest_path_coor.pop(len(shortest_path_coor) - 1))

        self.deleted_points.append(shortest_path_coor[len(shortest_path_coor) - 1])
        self.sig_Guide_Thread_ProgressBar_MaxValue.emit(((len(shortest_path_coor) - 1) - last_idx))

        self.DONE_road.append(shortest_path_coor[0])
        self.sig_Guide_Thread_Frame_With_Road.emit(
            self.camera.Print_Full_Road_On_Frame(frame, self.deleted_points, shortest_path_coor, self.DONE_road))

        if is_safe == True:  # Trasa jest bezpieczna = mozemy rozpocząć sekwencję
            for point in shortest_path_coor:
                self.point_iterator += 1
                self.sig_Guide_Thread_ProgressBar_NewValue.emit((self.point_iterator - 2))
                NEXT_POINT = False
                while NEXT_POINT == False:
                    frame, corners, ids, corners_ids_dict, Rob_center = self.GET_FRAME_EASY_AND_CREATE_DICT()
                    self.DONE_road.append(Rob_center[0])
                    self.sig_Guide_Thread_Frame_With_Road.emit(
                        self.camera.Print_Full_Road_On_Frame(frame, self.deleted_points, shortest_path_coor,
                                                             self.DONE_road))
                    print("A=", corners_ids_dict[str(self.id_robot)])
                    print("B=", point)
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
                            if self.GuideT.communication.Read_Data_From_Robot() == True:
                                frame, corners, ids, corners_ids_dict, Rob_center = self.GET_FRAME_EASY_AND_CREATE_DICT()
                                self.DONE_road.append(Rob_center[0])
                                self.sig_Guide_Thread_Frame_With_Road.emit(
                                    self.camera.Print_Full_Road_On_Frame(frame, self.deleted_points, shortest_path_coor,
                                                                         self.DONE_road))
                                angle, dir = self.GuideT.calculation.Calculate_Angle_RA(
                                    corners_ids_dict[str(self.id_robot)], point)
                                print("Nowy kąt = ", angle)
                        print("Poprawny kąt")
                        self.GuideT.communication.Send_Go_Straight(distance)
                        ACK = self.GuideT.communication.Read_Data_From_Robot()
                        print("I got ACK after Go Straight")
                    else:  # Dojechał do punktu
                        print("Biorę kolejny punkt")
                        NEXT_POINT = True
        else:
            print("Trasa niebezpieczna")
            return False
        print("Kończę fazę GUIDE")
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

    def GET_FRAME_EASY_AND_CREATE_DICT(self):
        frame, corners, ids = self.GET_FRAME()
        corners, ids = self.GuideT.calculation.Easy_Corners_And_Ids(corners, ids)
        corners_ids_dict = self.GuideT.calculation.Create_Dictionary_Of_Corners(corners, ids)
        Rob_center = self.GuideT.calculation.Get_Centers_Of_Corners(np.array([corners_ids_dict[str(self.id_robot)]]))
        return frame, corners, ids, corners_ids_dict, Rob_center


if __name__ == "__main__":
    cam = Camera.Camera(1)
    Guide = Guide(cam, 25, "COM14", 9600)
    Guide.Guide_Robot_To_Aim(0,2,30,3)