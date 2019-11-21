
import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt

import Calculations
import Voronoi
import Dijsktra
import Dijkstra_heap

class Trajectory:
    def __init__(self, FPTV_FACTOR, frame_width, frame_height, Calculations_class):
        print("Tworzę klasę Trajectory")
        self.SAFE_AREA = 20
        self.last_shortest_path_COOR = None
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.Calcualtion = Calculations_class
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

    # def Set_Route_Between_Points(self, aruco_corners, aruco_ids, id_robot, id_aim):
    #     print("Funkcja Set Route Between Points")
    #     corners, ids = self.Calcualtion.Easy_Corners_And_Ids(aruco_corners, aruco_ids)
    #     corner_ids_dicionary = self.Calcualtion.Create_Dictionary_Of_Corners(corners, ids)
    #     # tutaj mamy rzeczywisty środek kodów(moze go nie byc w voronoi)
    #     robot_center, aim_center = self.Calcualtion.Get_Centers_Of_Codes_From_Dictionary(corner_ids_dicionary, [id_robot, id_aim])
    #     obstacles_corners = self.Calcualtion.Get_Obstacles_Corners(id_robot, id_aim, corner_ids_dicionary)
    #     graph_input, calculated_voronoi_dictionary = self.Voronoi.Create_Voronoi_Graph(corners, obstacles_corners)
    #     id_robot_center, id_aim_center = self.Calcualtion.Get_Ids_From_Coordinates(calculated_voronoi_dictionary, robot_center, aim_center)
    #     print("IDRC ", id_robot_center, " IDAC ", id_aim_center)
    #     ### dotąd jest stałe. Teraz poszukujemy trasy bezpiecznej...
    #
    #     while True:
    #         self.Dijkstra.Load_Edges(graph_input)
    #         print("Ok")
    #         try:
    #             shortest_path_IDS  = self.Dijkstra.Get_Shortest_Path(str(id_robot_center), str(id_aim_center))
    #         except:
    #             print("Błąd")
    #         print("SPIDS", shortest_path_IDS)
    #         print("Len ", len(shortest_path_IDS))
    #         if len(shortest_path_IDS)==0: #nie ma zadnej dostepnej trasy
    #             return None, False
    #         shortest_path_COOR = self.Dijkstra.Transrofm_Shortest_Path_Ids_To_Corr(shortest_path_IDS, calculated_voronoi_dictionary)
    #         self.last_shortest_path_COOR = shortest_path_COOR
    #
    #         print(len(shortest_path_COOR))
    #         print(shortest_path_COOR)
    #         is_safe, bad_point = self.Calcualtion.Check_If_Path_Is_Safe(shortest_path_COOR, robot_center, self.Voronoi.frame_points, obstacles_corners, self.SAFE_AREA)
    #         print("IS, BAD", is_safe, bad_point)
    #         if is_safe == True:
    #             print("Jest bezpieczna. koniec")
    #             self.last_shortest_path_COOR = shortest_path_COOR
    #             return shortest_path_COOR, True
    #         else:
    #             #Wyszukujemy id punktu który jest w niebezpiecznej strefie i usuwamy go z grafu
    #             print("ELSE")
    #             bad_point_ids = self.Calcualtion.Get_Ids_Of_Bad_Points_From_Coordinates(calculated_voronoi_dictionary, bad_point)
    #             print("Bad_point_ids", bad_point_ids)
    #             graph_input = self.Calcualtion.Delete_Point_From_Graph(graph_input, bad_point_ids)
    #             print("New graph", graph_input)

    def Set_Route_Between_Points(self, aruco_corners, aruco_ids, id_robot, id_aim, id_pallet):
        corners, ids = self.Calcualtion.Easy_Corners_And_Ids(aruco_corners, aruco_ids)
        corner_ids_dicionary = self.Calcualtion.Create_Dictionary_Of_Corners(corners, ids)
        # print(corner_ids_dicionary)
        # tutaj mamy rzeczywisty środek kodów(moze go nie byc w voronoi)
        robot_center, aim_center = self.Calcualtion.Get_Centers_Of_Codes_From_Dictionary(corner_ids_dicionary,
                                                                                         [id_robot, id_aim])
        obstacles_corners = self.Calcualtion.Get_Obstacles_Corners(id_robot, id_aim, id_pallet, corner_ids_dicionary)
        # print("przeszkody:", obstacles_corners)
        graph_input, calculated_voronoi_dictionary = self.Voronoi.Create_Voronoi_Graph(corners, obstacles_corners)
        # print(calculated_voronoi_dictionary)
        # print("Robot center: ", robot_center, " Aim center: ", aim_center)
        id_robot_center, id_aim_center = self.Calcualtion.Get_Ids_From_Coordinates(calculated_voronoi_dictionary,
                                                                                   robot_center, aim_center)

        # self.Dijkstra.Load_Edges(graph_input)
        # print("IDRC= ", id_robot_center, "IDAC=", id_aim_center)
        # shortest_path_IDS = self.Dijkstra.Get_Shortest_Path(str(id_robot_center), str(id_aim_center))
        shortest_path_IDS = Dijkstra_heap.dijkstra(graph_input, str(id_robot_center), str(id_aim_center))
        # print(shortest_path_IDS)
        # print(shortest_path_IDS2)
        shortest_path_COOR = self.Dijkstra.Transrofm_Shortest_Path_Ids_To_Corr(shortest_path_IDS,
                                                                               calculated_voronoi_dictionary)
        is_safe = self.Calcualtion.Check_If_Path_Is_Safe(shortest_path_COOR, robot_center, self.Voronoi.frame_points,
                                                         obstacles_corners, self.SAFE_AREA)
        self.last_shortest_path_COOR = shortest_path_COOR
        return shortest_path_COOR, is_safe



if __name__=="__main__":
    corners = [[[[123, 256], [153, 257], [152, 289], [121, 287]]],
               [[[125, 149], [156, 147], [158, 178], [126, 180]]],
               [[[266, 73], [266, 104], [235, 103], [236, 72]]]]

    ids = [[1], [2], [0]]
    calc = Calculations.Calculations()
    trajectory = Trajectory(25, 452, 314, calc)
    trajectory.Set_Route_Between_Points(corners, ids, 0, 2,1)
    trajectory.Plot_path()
