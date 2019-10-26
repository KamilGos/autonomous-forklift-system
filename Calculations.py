import numpy as np
import cv2
import cv2.aruco as aruco
import math
from scipy.spatial import distance
import copy
import matplotlib.pyplot as plt



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

    def Create_Dictionary_Of_Corners(self,corners, ids):
        ids = np.squeeze(ids)
        dict = {}
        iter = 0
        for id in ids:
            dict[str(id)] = corners[iter]
            iter = iter + 1
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
    def Get_Obstacles_Corners(self, id_robot, id_aim, dict):
        obstacles = []
        for dic in dict:
            if dic != str(id_robot) and dic != str(id_aim):
                obstacles.append(dict[dic])
        return obstacles

    # function return id's of *start* and *stop* points
    def Get_Ids_From_Coordinates(self, vor_dict, Rob_center, Aim_center):
        Rob_center = list(Rob_center)
        Aim_center = list(Aim_center)
        id_Rob_center = None
        id_Aim_center = None
        for id in vor_dict:
            if vor_dict[id] == Rob_center:
                id_Rob_center = id
            if vor_dict[id] == Aim_center:
                id_Aim_center = id

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
                distance_tmp = int(distance.euclidean(Rob_center, vor_dict[id]))
                if distance_tmp < min_distance:
                    min_distance = distance_tmp
                    min_distance_id = id
            id_Rob_center = min_distance_id

        return id_Rob_center, id_Aim_center

    # It check if found trajectory is safe by checking if evry point from this path is not closer do
    # frame or some obstacle then range
    def Check_If_Path_Is_Safe(self, shortest_path_corr, boundary, obstacles, range):
        for path in shortest_path_corr:
            for point in boundary:
                if distance.euclidean(tuple(path), tuple(point)) < range:
                    print("Point ", path, "is only ", int(distance.euclidean(tuple(path), tuple(point))), " from frame")
                    return False
            for obs in obstacles:
                for point in obs:
                    if distance.euclidean(tuple(path), tuple(point)) < range:
                        print("Point ", path, "is only ", int(distance.euclidean(tuple(path), tuple(point))),
                              " from obstacle")
                        return False
        return True