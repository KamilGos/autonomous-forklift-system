import numpy as np
import cv2
import cv2.aruco as aruco
import math
from scipy.spatial import distance
import copy
import matplotlib.pyplot as plt

import Calculations
import Voronoi
import Dijsktra

class Trajectory:
    def __init__(self, FPTV_FACTOR, frame_width, frame_height):
        print("Tworzę klasę Trajectory")
        self.SAFE_AREA = 1
        self.last_shortest_path_COOR = None
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.Calcualtion = Calculations.Calculations()
        self.Voronoi     = Voronoi.Voronoi_Class()
        self.Voronoi.Initialize(FPTV_FACTOR, frame_width, frame_height)
        self.Dijkstra = Dijsktra.Dijkstra()

    def Plot_path(self):
        if self.last_shortest_path_COOR != None:
            x, y = zip(*self.last_shortest_path_COOR)
            plt.xlim((0, self.frame_width))
            plt.ylim((self.frame_height, 0))
            plt.title("Najkrótsza trasa")
            plt.plot(x, y)
            plt.scatter(x, y)
            plt.show()
        else:
            print("There is no any path to plot")



    def Set_Route_Between_Points(self, aruco_corners, aruco_ids, id_robot, id_aim):
        corners, ids = self.Calcualtion.Easy_Corners_And_Ids(aruco_corners, aruco_ids)
        corner_ids_dicionary = self.Calcualtion.Create_Dictionary_Of_Corners(corners, ids)
        robot_center, aim_center = self.Calcualtion.Get_Centers_Of_Codes_From_Dictionary(corner_ids_dicionary, [id_robot, id_aim])
        obstacles_corners = self.Calcualtion.Get_Obstacles_Corners(id_robot, id_aim, corner_ids_dicionary)
        graph_input, calculated_voronoi_dictionary = self.Voronoi.Create_Voronoi_Graph(corners, obstacles_corners)
        id_robot_center, id_aim_center = self.Calcualtion.Get_Ids_From_Coordinates(calculated_voronoi_dictionary, robot_center, aim_center)
        self.Dijkstra.Load_Edges(graph_input)
        shortest_path_IDS  = self.Dijkstra.Get_Shortest_Path(str(id_robot_center), str(id_aim_center))
        shortest_path_COOR = self.Dijkstra.Transrofm_Shortest_Path_Ids_To_Corr(shortest_path_IDS, calculated_voronoi_dictionary)
        is_safe = self.Calcualtion.Check_If_Path_Is_Safe(shortest_path_COOR, self.Voronoi.frame_points, obstacles_corners, self.SAFE_AREA)
        self.last_shortest_path_COOR = shortest_path_COOR
        return shortest_path_COOR



if __name__=="__main__":
    corners = [[[[123, 256], [153, 257], [152, 289], [121, 287]]],
               [[[125, 149], [156, 147], [158, 178], [126, 180]]],
               [[[266, 73], [266, 104], [235, 103], [236, 72]]]]

    ids = [[1], [2], [0]]
    trajectory = Trajectory(25, 452, 314)
    trajectory.Set_Route_Between_Points(corners, ids, 0, 2)
    trajectory.Plot_path()
