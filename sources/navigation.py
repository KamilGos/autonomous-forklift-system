from PyQt5.QtCore import  QThread,  pyqtSignal, QTimer
import numpy as np
import sources.trajectory_generator as trajectory_generator
import sources.communication as communication
import sources.calculations as calculations
from cv2 import aruco

class Navigation:
    def __init__(self, camera, FPTV_FACTOR, PORT_COM, BAUDRATE):
        """
        Args:
            camera (int): camera descriptor
            FPTV_FACTOR ([int]): destiny of points
            PORT_COM ([string]): name of COM port used to communicate with robot
            BAUDRATE ([int]): COM port baudrate
        """
        self.guide_ready = False
        self.camera = camera
        print(self.camera.initialized)
        self.calculation = calculations.Calculations()
        self.Trajectory = trajectory_generator.Trajectory(FPTV_FACTOR, self.camera.bigwidth, self.camera.bigheight, self.calculation)
        self.communication = communication.Communication()
        self.communication.Initialize(PORT_COM, BAUDRATE)
        if self.camera.initialized == True and self.communication.initializated == True:
            self.guide_ready = True
            print("Guide is ready")

class Navigatio_Thread(QThread):
    sig_Guide_Thread_Frame_With_Road = pyqtSignal(object)
    sig_Guide_Thread_ProgressBar_MaxValue = pyqtSignal(int)
    sig_Guide_Thread_ProgressBar_NewValue = pyqtSignal(int)
    sig_Guide_Thread_Initialized = pyqtSignal(str)
    sig_Guide_Thread_Phase1 = pyqtSignal(int)
    sig_Guide_Thread_Phase2 = pyqtSignal(int)
    sig_Guide_Thread_Errors = pyqtSignal(int)
    sig_Guide_Thread_Error_STOP = pyqtSignal(int)
    sig_Guide_Thread_Update_Warehouse = pyqtSignal(int)
    sig_Guide_Thread_Update_Pallet_Level = pyqtSignal(int)


    def __init__(self, camera, guide_class,id_robot, id_pallet, WAREHOUSE_LEVEL, VIEV_IS_RUNNING):
        QThread.__init__(self)
        self.runperm = True
        self.camera = camera
        self.id_robot = id_robot
        self.id_aim = None
        self.id_pallet = id_pallet
        self.id_warehouse = 26
        self.MIN_DISTANCE_CONST = 50
        self.MIN_DISTANCE_LAST_CONST = 10
        self.MIN_DISTANCE = self.MIN_DISTANCE_CONST
        self.MIN_ANGLE = 2
        self.GuideT = guide_class
        self.VIEW_IS_RUNNING = VIEV_IS_RUNNING
        self.DONE_road = []
        self.deleted_points = []
        self.shortest_path_coor=[]
        self.cpframe = np.zeros((1,1))
        self.point_iterator = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.Send_Frame_To_View3)
        self.timer.start(100)
        self.Warehouse_level = WAREHOUSE_LEVEL
        print("Warehouse level=", self.Warehouse_level)

    def run(self):
        """ Start navigation procedure
        """
        self.sig_Guide_Thread_Initialized.emit(str("OK"))
        print("Start Guide_Thread")
        self.id_aim = self.id_pallet
        self.sig_Guide_Thread_Phase1.emit(1)  # phase 1 running
        if self.Go_From_A_To_B(self.id_aim, self.id_pallet,0) == False:
            self.sig_Guide_Thread_Phase1.emit(3)  # phase 1 error
            self.sig_Guide_Thread_Errors.emit(1)

            print("***** PATH ID DANGEROUS ******")
            self.exit(0)
            self.sig_Guide_Thread_Error_STOP.emit(0)

        self.Calibrate_rotation(self.deleted_points[0])
        self.GuideT.communication.Send_Take_Pallet(1)
        self.camera.DONE_MARKERS = self.camera.DONE_MARKERS + 1
        if self.GuideT.communication.Read_Data_From_Robot()== True:
            self.sig_Guide_Thread_Phase1.emit(2) #phase 1 done
            self.id_aim = self.id_warehouse
            print("okok")
            self.sig_Guide_Thread_Phase2.emit(1)  # phase 2 running
            self.DONE_road = []
            self.deleted_points = []
            self.shortest_path_coor = []
            if self.Go_From_A_To_B(self.id_aim, self.id_pallet,1) == False:
                self.sig_Guide_Thread_Phase2.emit(3)  # phase 2 error
                self.sig_Guide_Thread_Errors.emit(1)

                print("***** PATH ID DANGEROUS ******")
                self.exit(0)
                self.sig_Guide_Thread_Error_STOP.emit(0)

            self.Calibrate_rotation(self.camera.Warehouse_place_center)
            self.GuideT.communication.Send_Put_Pallet(self.Warehouse_level)
            self.sig_Guide_Thread_Update_Pallet_Level.emit(1)
            if self.GuideT.communication.Read_Data_From_Robot() == True:
                self.sig_Guide_Thread_Phase2.emit(2)  # phase 2 done
                self.sig_Guide_Thread_Update_Warehouse.emit(self.id_pallet)
                print("*** PALETISATION DONE ***")
                print(" *** PALLET HAS BEEN PUT ON LEVEL 0 ***")
                self.DONE_road = []
                self.deleted_points = []
                self.shortest_path_coor = []
                self.sig_Guide_Thread_Error_STOP.emit(0)


    def Go_From_A_To_B(self, id_aim, id_pallet, IF_LAST):
        """ Navigate robot from current position to destination
        Args:
            id_aim ([int]): id of destination place
            id_pallet ([int]): id of served pallet 
            IF_LAST ([bool]): True if this movement if the last one
        Returns:
            [bool]: True if navigation procedure has been completed successfully, otherwise False
        """
        try:
            self.point_iterator = 0
            frame, corners, ids = self.Get_Frame_And_Corners_With_Ids()
            try:
                self.shortest_path_coor, is_safe = self.GuideT.Trajectory.Set_Route_Between_Points(corners, ids, self.id_robot,
                                                                                          id_aim, id_pallet)
            except Exception as e:
                print("Path could not be loaded: ", e)
                return False

            if is_safe != True:
                print("Road is not safe!")
                return False
            try:
                if IF_LAST == 0:
                    last_idx = self.GuideT.calculation.Check_Last_Point(self.shortest_path_coor) + 1
                    for i in range(last_idx):
                        self.deleted_points.append(self.shortest_path_coor.pop(len(self.shortest_path_coor) - 1))
                    self.deleted_points.append(self.shortest_path_coor[len(self.shortest_path_coor) - 1])
                    self.sig_Guide_Thread_ProgressBar_MaxValue.emit(((len(self.shortest_path_coor) - 1) - last_idx))
                elif IF_LAST == 1:
                    self.deleted_points = []
                    self.sig_Guide_Thread_ProgressBar_MaxValue.emit((len(self.shortest_path_coor) - 1))
                self.DONE_road.append(self.shortest_path_coor[0])
                self.sig_Guide_Thread_Frame_With_Road.emit(
                    self.camera.Print_Full_Road_On_Frame(frame, self.deleted_points, self.shortest_path_coor,
                                                         self.DONE_road))
            except Exception as e:
                print("Error during navigation procedure: ", e)

            if is_safe == True:
                for point in self.shortest_path_coor:
                    self.point_iterator += 1
                    print("Iterator:", self.point_iterator)
                    if IF_LAST == 0:
                        if self.point_iterator == len(self.shortest_path_coor) - last_idx+1: #ostatni punkt
                            self.MIN_DISTANCE=self.MIN_DISTANCE_LAST_CONST
                            print("Minimal distance has been changed")
                    if IF_LAST == 1:
                        if self.point_iterator == len(self.shortest_path_coor): #ostatni punkt
                            self.MIN_DISTANCE=self.MIN_DISTANCE_LAST_CONST
                            print("Minimal distance has been changed")

                    self.sig_Guide_Thread_ProgressBar_NewValue.emit((self.point_iterator - 2))
                    NEXT_POINT = False
                    try:
                        while NEXT_POINT == False:
                            try:
                                frame, corners, ids, corners_ids_dict, Rob_center = self.Get_Frame_And_Dict()
                                self.DONE_road.append(Rob_center[0])
                                self.sig_Guide_Thread_Frame_With_Road.emit(
                                    self.camera.Print_Full_Road_On_Frame(frame, self.deleted_points, self.shortest_path_coor,
                                                                         self.DONE_road))
                                distance = self.GuideT.calculation.Calculate_Distance_RA(corners_ids_dict[str(self.id_robot)],
                                                                                     point)
                                print("Distance = ", distance)
                            except Exception as e:
                                print("Error during navigation procedure: ", e)

                            try:
                                if distance > self.MIN_DISTANCE:  
                                    print("Distance is too large")
                                    angle, dir = self.GuideT.calculation.Calculate_Angle_RA(corners_ids_dict[str(self.id_robot)],
                                                                                            point)
                                    print("Angle = ", angle)
                                    while angle > self.MIN_ANGLE and angle < (360 - self.MIN_ANGLE): 
                                        print("Wrong angle")
                                        self.GuideT.communication.Send_Rotate(angle, dir)
                                        try:
                                            if self.GuideT.communication.Read_Data_From_Robot() == True:
                                                frame, corners, ids, corners_ids_dict, Rob_center = self.Get_Frame_And_Dict()
                                                self.DONE_road.append(Rob_center[0])
                                                self.sig_Guide_Thread_Frame_With_Road.emit(
                                                    self.camera.Print_Full_Road_On_Frame(frame, self.deleted_points, self.shortest_path_coor,
                                                                                     self.DONE_road))
                                                angle, dir = self.GuideT.calculation.Calculate_Angle_RA(
                                                corners_ids_dict[str(self.id_robot)], point)
                                                print("New angle = ", angle)
                                        except Exception as e:
                                            print("Error during navigation procedure: ", e)

                                    print("Angle is correct")
                                    self.GuideT.communication.Send_Go_Straight(distance)
                                    try:
                                        ACK = self.GuideT.communication.Read_Data_From_Robot()
                                    except Exception as e: 
                                        print("Error during communication with robot: ", e)
                                    print("I got ACK after Go Straight")
                                else:  
                                    print("Taking next point")
                                    NEXT_POINT = True
             
                            except Exception as e:
                                print("Error during navigation procedure: ", e)

                    except Exception as e:
                        print("Error during navigation procedure: ", e)

            else:
                print("Path is dangerous")
                return False
                
            print("Navigation hass been finished")
            self.MIN_DISTANCE = self.MIN_DISTANCE_CONST
            return True
        except:
            print("Error during navigation procedure: ", e)


    def Calibrate_rotation(self, point):
        """ Rotate robot to the specified angle
        Args:
            point ([type]): next point to be reached by robot
        Returns:
            [bool]: True if correct angle has been reached
        """
        try:
            _, _, _, corners_ids_dict, _ = self.Get_Frame_And_Dict()
            angle, dir = self.GuideT.calculation.Calculate_Angle_RA(corners_ids_dict[str(self.id_robot)], point)
            print("Angle = ", angle)
            while angle > 1 and angle < 359:  # musimy się obrócić
                print("Wrong angle")
                self.GuideT.communication.Send_Rotate(angle, dir)
                if self.GuideT.communication.Read_Data_From_Robot() == True:
                    _, _, _, corners_ids_dict, _ = self.Get_Frame_And_Dict()
                    angle, dir = self.GuideT.calculation.Calculate_Angle_RA(
                        corners_ids_dict[str(self.id_robot)], point)
                    print("New angle = ", angle)
            return True
        except Exception as e:
            print("Error during rotating robot: ", e)

    def Get_Frame_And_Corners_With_Ids(self):
        try:
            if self.VIEW_IS_RUNNING == False:
                frame, corners, ids = self.camera.get_frame_while()
            else:  # kamera juz dziala czyli korzysamy z ramek bez pobierania nowych
                ids = []
                while len(ids) != self.GuideT.camera.MARKERS_VAL:
                    frame, corners, ids = self.camera.Detect_Markers_Self()
        except Exception as e:
            print("Error during aquiring new frame: ", e) 
        return frame, corners, ids


    def Get_Frame(self):
        try:
            frame = self.camera.get_frame()
            corners, ids = self.camera.Detect_Markers(frame)
            frame = aruco.drawDetectedMarkers(frame, corners[:-1], ids[:-1])
            return frame
        except Exception as e:
            print("Error during aquiring new frame: ", e) 


    def Get_Frame_And_Dict(self):
        try:
            frame, corners, ids = self.Get_Frame_And_Corners_With_Ids()
            corners, ids = self.GuideT.calculation.Easy_Corners_And_Ids(corners, ids)
            corners_ids_dict = self.GuideT.calculation.Create_Dictionary_Of_Corners(corners, ids)
            Rob_center = self.GuideT.calculation.Get_Centers_Of_Corners(np.array([corners_ids_dict[str(self.id_robot)]]))
            return frame, corners, ids, corners_ids_dict, Rob_center
        except Exception as e:
            print("Error during aquiring new frame: ", e) 

    def Send_Frame_To_View3(self):
        try:
            if len(self.shortest_path_coor)>0:
                self.cpframe = self.GET_FRAME_ONLY()
                self.sig_Guide_Thread_Frame_With_Road.emit(
                    self.camera.Print_Full_Road_On_Frame(self.cpframe, self.deleted_points, self.shortest_path_coor, self.DONE_road))
        except Exception as e:
            print("Error during sending frame to View3: ", e) 
