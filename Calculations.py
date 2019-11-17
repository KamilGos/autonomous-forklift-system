import numpy as np
import cv2
import math
from scipy.spatial import distance




class Calculations:
    def __init__(self):
        print("Tworzę klasę Calculations")


    # function delete one not needed dimension, change elements type on int and reverse elements
    # corners - list of corners to change
    def Easy_Corners_And_Ids(self, corners, ids):
        if np.shape(corners)[0] != 1:
            tmp = np.squeeze(corners, axis=(1))  # delete one dimension
            tmp = tmp.astype(int)  # change type
            return tmp[::-1], ids[::-1]
        else:
            tmp = np.squeeze(corners, axis=(1))  # delete one dimension
            tmp = tmp.astype(int)
            tmp = np.array([tmp])
            return tmp, ids

    # def Create_Dictionary_Of_Corners(self,corners, ids):
    #     ids = np.squeeze(ids)
    #     dict = {}
    #     iter = 0
    #     for id in ids:
    #         dict[str(id)] = corners[iter]
    #         iter = iter + 1
    #     return dict

    def Create_Dictionary_Of_Corners(self,corners, idss):
        ids = np.squeeze(idss)
        dict = {}
        iter = 0
        if len(idss) > 1:
            for id in ids:
                dict[str(id)] = corners[iter]
                iter = iter + 1
        else:
            dict[str(idss[0][0])] = corners[0]
        return dict

    def Get_Centers_Of_Codes_From_Dictionary(self, dictionary_of_corners, ids):
        centers = []
        for id in ids:
            c = dictionary_of_corners[str(id)]
            M = cv2.moments(c)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            centers.append((cX, cY))
        return centers[0], centers[1]

    # Function get corners which are obstacles (all corners except of robot and goal
    def Get_Obstacles_Corners(self, id_robot, id_aim, id_pallet, dict):
        obstacles = []

        if id_aim == id_pallet:
            for dic in dict:
                if dic != str(id_robot) and dic != str(id_aim):
                    obstacles.append(dict[dic])
            return obstacles
        else: #Celem jest magazyn
            for dic in dict:
                if dic != str(id_robot) and dic != str(id_aim) and dic != str(id_pallet):
                    obstacles.append(dict[dic])
            return obstacles

    # function return id's of *start* and *stop* points
    def Get_Ids_From_Coordinates(self, vor_dict, Rob_center, Aim_center):
        id_Rob_center = None
        id_Aim_center = None
        for id in vor_dict:
            if vor_dict[id][0] == Rob_center[0] and vor_dict[id][1] == Rob_center[1]:
                id_Rob_center = id
            if vor_dict[id][0] == Aim_center[0] and vor_dict[id][1] == Aim_center[1]:
                id_Aim_center = id

        #Jeśli wczesniej nie wystąpiło to musimy szukac najbliższego
        if id_Rob_center == None:
            distance_tmp = None
            min_distance = float("inf")
            min_distance_id = None
            for id in vor_dict:
                distance_tmp = int(distance.euclidean(Rob_center, vor_dict[id]))
                if distance_tmp < min_distance:
                    min_distance = distance_tmp
                    min_distance_id = id
            id_Rob_center = min_distance_id

        if id_Aim_center == None:
            distance_tmp = None
            min_distance = float("inf")
            min_distance_id = None
            for id in vor_dict:
                distance_tmp = int(distance.euclidean(Aim_center, vor_dict[id]))
                if distance_tmp < min_distance:
                    min_distance = distance_tmp
                    min_distance_id = id
            id_Aim_center = min_distance_id

        return id_Rob_center, id_Aim_center


    def Get_Ids_Of_Bad_Points_From_Coordinates(self, vor_dict, Point):
        point_ids = []
        for id in vor_dict:
            if int(vor_dict[id][0]) == int(Point[0]) and int(vor_dict[id][1]) == int(Point[1]):
                point_ids.append(id)
        return point_ids

    #It delete every edge where is point_id
    def Delete_Point_From_Graph(self, graph, point_ids):
        new_graph = []
        for edge in graph:
            FLAG = True
            for point_id in point_ids:
                if int(edge[0])==int(point_id) or int(edge[1])==int(point_id):
                    print("Usuwam krawędź: ", edge)
                    FLAG = False
            if FLAG == True:
                new_graph.append(edge)
        return new_graph


    # It check if found trajectory is safe by checking if every point from this path is not closer to
    # frame or some obstacle then range
    def Check_If_Path_Is_Safe(self, shortest_path_corr, robot_center, boundary, obstacles, range):
        for path in shortest_path_corr:
            if tuple(path)!=robot_center:
                for point in boundary:
                    if distance.euclidean(tuple(path), tuple(point)) < range:
                        print("Point ", path, "is only ", int(distance.euclidean(tuple(path), tuple(point))), " from frame")
                        return False, path
                for obs in obstacles:
                    for point in obs:
                        if distance.euclidean(tuple(path), tuple(point)) < range:
                            print("Point ", path, "is only ", int(distance.euclidean(tuple(path), tuple(point))),
                                  " from obstacle")
                            return False, path
        return True

    # Function return touple with centers of qr codes using moments method
    # corners - list of detected markers corners
    def Get_Centers_Of_Corners(self, corners):
        centers = []
        for c in corners:
            M = cv2.moments(c)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            centers.append((cX, cY))
        return centers

    # Return distance from center of aruco code to another point
    def Calculate_Distance_RA(self,Rob, Aim):
        Rob_center = self.Get_Centers_Of_Corners(np.array([Rob]))
        return int(distance.euclidean(Rob_center, Aim))

        # Calculate angle between Robot and Aim (eg. next point). It return this angle and direction 1-left, 0-right

    # It determine angle of vector define by X and Y to X axis
    def Determine_Angle_XY(self, X, Y):
        if X == 0: X = 0.001
        if Y == 0: Y = 0.001

        if X > 0 and Y < 0:  # I ćwiartka
            angle = -1 * np.rad2deg(math.atan(Y / X))
            # print("1 ćwiartka")
        elif X < 0 and Y < 0:  # II ćwiartka
            angle = 180 - np.rad2deg(math.atan(Y / X))
            # print("2 ćwiartka")
        elif X < 0 and Y > 0:  # III ćwiartka
            angle = 180 + (-1 * np.rad2deg(math.atan(Y / X)))
            # print("3 ćwiartka")
        elif X > 0 and Y > 0:  # IV ćwiartka
            angle = 360 - np.rad2deg(math.atan(Y / X))
            # print("4 ćwiartka")
        return angle


    # Rob - corners of aruco marker which define robot
    # Aim - point (x,y) which is aim
    def Calculate_Angle_RA(self, Rob, Aim):
        X = Rob[0][0] - Rob[3][0]
        Y = Rob[0][1] - Rob[3][1]
        Rob_angle = self.Determine_Angle_XY(X, Y)
        # print("Robot angle= ", Rob_angle)
        # Calculate aim angle
        Rob_center = self.Get_Centers_Of_Corners(np.array([Rob]))

        X = Aim[0] - Rob_center[0][0]
        Y = Aim[1] - Rob_center[0][1]
        Aim_angle = self.Determine_Angle_XY(X, Y)

        if Aim_angle > Rob_angle:
            if (Aim_angle - Rob_angle) <= 180:
                return abs(int(Aim_angle - Rob_angle)), 1  # go left
            else:
                return abs(int((360 - Aim_angle) + Rob_angle)), 0  # go right
        elif Aim_angle < Rob_angle:
            if (Rob_angle - Aim_angle) <= 180:
                return abs(int(Rob_angle - Aim_angle)), 0  # go right
            else:
                return abs(int((360 - Rob_angle) + Aim_angle)), 1  # go left

    #It check which point is the one before last
    def Check_Last_Point(self, path):
        max_distance = 20
        path = path[::-1]
        for i in range(0, len(path)-1):
            dist = distance.euclidean(path[i],path[i+1])
            if dist > max_distance:
                return i
