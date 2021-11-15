import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt
import sources.calculations as calculations
import sources.voronoi_generator as voronoi_generator
import sources.dijsktra as dijsktra

class Trajectory:
    def __init__(self, FPTV_FACTOR, frame_width, frame_height, Calculations_class):
        self.SAFE_AREA = 1
        self.last_shortest_path_coor = None
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.Calcualtion = Calculations_class
        self.Voronoi = voronoi_generator.Voronoi()
        self.Voronoi.Initialize(FPTV_FACTOR, frame_width, frame_height)
        self.Dijkstra = dijsktra.Dijkstra()

    def Plot_path(self):
        if self.last_shortest_path_coor != None:
            x, y = zip(*self.last_shortest_path_coor)
            plt.xlim((0, self.frame_width))
            plt.ylim((self.frame_height, 0))
            plt.grid(True)
            plt.plot(x, y)
            plt.scatter(x, y)
            plt.show()
        else:
            print("There is no any path to plot")

    def Set_Route_Between_Points(self, aruco_corners, aruco_ids, id_robot, id_aim, id_pallet):
        """Generate shortest path between points
        Args:
            aruco_corners ([list]): corners of aruco markers
            aruco_ids ([list]): list of available arucos's ids
            id_robot ([type]): id of available robot
            id_aim ([type]): if of warehouse
            id_pallet ([type]): if of pallet to be moved

        Returns:
            shortest_path_coor ([list]): coordicates of shortest path
            is_safe ([bool]): True if the path is safe
        """
        corners, ids = self.Calcualtion.Easy_Corners_And_Ids(aruco_corners, aruco_ids)
        corner_ids_dicionary = self.Calcualtion.Create_Dictionary_Of_Corners(corners, ids)
        robot_center, aim_center = self.Calcualtion.Get_Centers_Of_Codes_From_Dictionary(corner_ids_dicionary,
                                                                                         [id_robot, id_aim])
        obstacles_corners = self.Calcualtion.Get_Obstacles_Corners(id_robot, id_aim, id_pallet, corner_ids_dicionary)
        graph_input, calculated_voronoi_dictionary = self.Voronoi.Create_Voronoi_Graph(corners, obstacles_corners)
        id_robot_center, id_aim_center = self.Calcualtion.Get_Ids_From_Coordinates(calculated_voronoi_dictionary,
                                                                                   robot_center, aim_center)
        shortest_path_IDS = self.Dijkstra.Calculate_Dijkstra(graph_input, str(id_robot_center), str(id_aim_center))
        shortest_path_coor = self.Dijkstra.Transrofm_Shortest_Path_Ids_To_Corr(shortest_path_IDS,
                                                                               calculated_voronoi_dictionary)
        is_safe = self.Calcualtion.Check_If_Path_Is_Safe(shortest_path_coor, robot_center, self.Voronoi.frame_points,
                                                         obstacles_corners, self.SAFE_AREA)
        self.last_shortest_path_coor = shortest_path_coor
        return shortest_path_coor, is_safe


if __name__=="__main__":
    corners = [[[[123, 256], [153, 257], [152, 289], [121, 287]]],
               [[[125, 149], [156, 147], [158, 178], [126, 180]]],
               [[[266, 73], [266, 104], [235, 103], [236, 72]]]]
               

    ids = [[1], [2], [0]]
    calc = calculations.Calculations()
    trajectory = Trajectory(25, 452, 314, calc)
    trajectory.Set_Route_Between_Points(corners, ids, 0, 2,1)
    trajectory.Plot_path()
