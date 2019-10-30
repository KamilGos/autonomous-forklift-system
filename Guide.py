# import cv2
# from PyQt5.QtCore import  QThread,  pyqtSignal
# import numpy as np
# import Trajectory
# import Communication
# import Camera
# import Calculations
#
# class Guide:
#     def __init__(self, camera, FPTV_FACTOR, PORT_COM, BAUDRATE):
#         self.guide_ready = False
#         self.camera = camera
#         print(self.camera.initialized)
#         self.calculation = Calculations.Calculations()
#         self.Trajectory = Trajectory.Trajectory(FPTV_FACTOR, self.camera.width, self.camera.height, self.calculation)
#         self.communication = Communication.Communication()
#         self.communication.Initialize(PORT_COM, BAUDRATE)
#         if self.camera.initialized == True and self.communication.initializated == True:
#             self.guide_ready = True
#             print("Guide is ready")
#
#     def Guide_Robot_To_Aim(self, id_robot, id_aim, MIN_DISTANCE, MIN_ANGLE):
#         print("Rozpoczynam Guide Robot To Aim ")
#         frame, corners, ids = self.camera.Get_Frame_And_Detect()
#         print(len(ids))
#         # cv2.imshow("aa", frame)
#         # cv2.waitKey(0)
#
#         shortest_path_coor, is_safe = self.Trajectory.Set_Route_Between_Points(corners, ids, id_robot, id_aim)
#         self.Trajectory.Plot_path()
#         if is_safe == True: #Trasa jest bezpieczna = mozemy rozpocząć sekwencję
#             for point in shortest_path_coor:
#                 NEXT_POINT = False
#                 while NEXT_POINT == False:
#                     frame, corners, ids = self.camera.Get_Frame_And_Detect()
#                     print(len(ids))
#                     corners, ids = self.calculation.Easy_Corners_And_Ids(corners, ids)
#                     corners_ids_dict = self.calculation.Create_Dictionary_Of_Corners(corners, ids)
#                     distance = self.calculation.Calculate_Distance_RA(corners_ids_dict[str(id_robot)], point)
#                     print("Distance = ", distance)
#                     if distance > MIN_DISTANCE: #Trzeba dojechac do tego punktu (nie pomijamy go)
#                         print("Za duży dystans")
#                         angle, dir = self.calculation.Calculate_Angle_RA(corners_ids_dict[str(id_robot)], point)
#                         print("Kąt = ", angle)
#                         while angle > MIN_ANGLE and angle < (360 - MIN_ANGLE):  # musimy się obrócić
#                             print("Zły kąt")
#                             self.communication.Send_Rotate(angle, dir)
#                             if self.communication.Read_Data_From_Robot() == True:
#                                 frame, corners, ids = self.camera.Get_Frame_And_Detect()
#                                 print(len(ids))
#                                 corners, ids = self.calculation.Easy_Corners_And_Ids(corners, ids)
#                                 corners_ids_dict = self.calculation.Create_Dictionary_Of_Corners(corners, ids)
#                                 angle, dir = self.calculation.Calculate_Angle_RA(corners_ids_dict[str(id_robot)], point)
#                                 print("Nowy kąt = ", angle)
#
#                                 cv2.line(frame, tuple(corners_ids_dict[str(id_robot)][3]),tuple(corners_ids_dict[str(id_robot)][0]), (0, 0, 0), 2)
#                                 cv2.line(frame,tuple(self.calculation.Get_Centers_Of_Corners(np.array([corners_ids_dict[str(id_robot)]]))[0]),tuple(point), (0, 0, 0), 2)
#                                 cv2.imshow('Found arucos', frame)
#                                 cv2.waitKey(0)
#                                 cv2.destroyAllWindows()
#
#
#                         print("Poprawny kąt")
#                         self.communication.Send_Go_Straight(distance)
#                         ACK = self.communication.Read_Data_From_Robot()
#                         print("I got ACK after Go Straight")
#                         cv2.line(frame, tuple(corners_ids_dict[str(id_robot)][3]),
#                                  tuple(corners_ids_dict[str(id_robot)][0]), (0, 0, 0), 2)
#                         cv2.line(frame, tuple(
#                             self.calculation.Get_Centers_Of_Corners(np.array([corners_ids_dict[str(id_robot)]]))[0]),
#                                  tuple(point), (0, 0, 0), 2)
#                         cv2.imshow('Found arucos', frame)
#                         cv2.waitKey(0)
#                         cv2.destroyAllWindows()
#                     else: #Dojechał do punktu
#                         print("Biorę kolejny punkt")
#                         NEXT_POINT = True
#         else:
#             print("Trasa niebezpieczna")
#             return False
#         return True
#
#
# class Guide_Thread(QThread):
#
#     def __init__(self, camera, guide_class, FPTV, PORT, BAUDRATE, id_robot, id_aim, MIN_DISTANCE, MIN_ANGLE):
#         QThread.__init__(self)
#         self.runperm = True
#         self.id_robot = id_robot
#         self.id_aim = id_aim
#         self.MIN_DISTANCE = MIN_DISTANCE
#         self.MIN_ANGLE = MIN_ANGLE
#         self.GuideT = guide_class
#         # print("Koniec init")
#
#     def run(self):
#         print("Start Guide_Thread")
#         while self.runperm == True:
#             print("OK")
#             # self.sleep(1)
#             self.GuideT.Guide_Robot_To_Aim(self.id_robot, self.id_aim, self.MIN_DISTANCE, self.MIN_ANGLE)
#             if self.runperm == False:
#                 self.exit(0)
#         print("Kończę wątek paletyzacji")
#         self.exit(1)
#
#
#
# if __name__ == "__main__":
#     cam = Camera.Camera(1)
#     Guide = Guide(cam, 25, "COM14", 9600)
#     Guide.Guide_Robot_To_Aim(0,2,30,3)


import cv2
from PyQt5.QtCore import  QThread,  pyqtSignal
import numpy as np
import Trajectory
import Communication
import Camera
import Calculations

class Guide:
    def __init__(self, camera, FPTV_FACTOR, PORT_COM, BAUDRATE):
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

    # def Guide_Robot_To_Aim(self, id_robot, id_aim, MIN_DISTANCE, MIN_ANGLE):

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
        self.id_aim = id_aim
        self.MIN_DISTANCE = MIN_DISTANCE
        self.MIN_ANGLE = MIN_ANGLE
        self.GuideT = guide_class
        self.VIEW_IS_RUNNING = VIEV_IS_RUNNING
        self.DONE_road = []
        self.point_iterator = 0
        # print("Koniec init")


    def run(self):
        self.sig_Guide_Thread_Initialized.emit(str("OK"))
        print("Start Guide_Thread")
        while self.runperm == True:

            frame, corners, ids = self.GET_FRAME()
            shortest_path_coor, is_safe = self.GuideT.Trajectory.Set_Route_Between_Points(corners, ids, self.id_robot, self.id_aim)
            self.sig_Guide_Thread_ProgressBar_MaxValue.emit((len(shortest_path_coor)-1))

            self.DONE_road.append(shortest_path_coor[0])
            self.sig_Guide_Thread_Frame_With_Road.emit(self.camera.Print_Full_Road_On_Frame(frame,shortest_path_coor, self.DONE_road))

            if is_safe == True:  # Trasa jest bezpieczna = mozemy rozpocząć sekwencję
                for point in shortest_path_coor:
                    self.point_iterator +=1
                    self.sig_Guide_Thread_ProgressBar_NewValue.emit((self.point_iterator-1))
                    NEXT_POINT = False
                    while NEXT_POINT == False:
                        frame, corners, ids, corners_ids_dict, Rob_center = self.GET_FRAME_EASY_AND_CREATE_DICT()
                        self.DONE_road.append(Rob_center[0])
                        self.sig_Guide_Thread_Frame_With_Road.emit(self.camera.Print_Full_Road_On_Frame(frame, shortest_path_coor, self.DONE_road))
                        distance = self.GuideT.calculation.Calculate_Distance_RA(corners_ids_dict[str(self.id_robot)], point)
                        print("Distance = ", distance)
                        if distance > self.MIN_DISTANCE:  # Trzeba dojechac do tego punktu (nie pomijamy go)
                            print("Za duży dystans")
                            angle, dir = self.GuideT.calculation.Calculate_Angle_RA(corners_ids_dict[str(self.id_robot)], point)
                            print("Kąt = ", angle)
                            while angle > self.MIN_ANGLE and angle < (360 - self.MIN_ANGLE):  # musimy się obrócić
                                print("Zły kąt")
                                self.GuideT.communication.Send_Rotate(angle, dir)
                                if self.GuideT.communication.Read_Data_From_Robot() == True:
                                    frame, corners, ids, corners_ids_dict,Rob_center = self.GET_FRAME_EASY_AND_CREATE_DICT()
                                    self.DONE_road.append(Rob_center[0])
                                    self.sig_Guide_Thread_Frame_With_Road.emit(self.camera.Print_Full_Road_On_Frame(frame, shortest_path_coor, self.DONE_road))
                                    angle, dir = self.GuideT.calculation.Calculate_Angle_RA(corners_ids_dict[str(self.id_robot)], point)
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
        if self.runperm == False:
            print("Kończę wątek paletyzacji - WYMUSZONE")
            self.exit(0)
        print("Kończę wątek paletyzacji - DOTARŁ DO CELU")
        return True


    def GET_FRAME(self):
        if self.VIEW_IS_RUNNING == False:
            print("Biorę nową")
            frame, corners, ids = self.camera.get_frame_while()
        else:  # kamera juz dziala czyli korzysamy z ramek bez pobierania nowych
            print("Biorę z klasy")
            ids = []
            while len(ids) != 3:
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