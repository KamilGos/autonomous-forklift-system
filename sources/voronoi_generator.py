import scipy
import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt
import numpy as np
from scipy.spatial import distance

class Voronoi:
    def __init__(self):
        self.FPTV_FACTOR = None
        self.frame_width = None
        self.frame_height = None
        self.voronoi_to_print = None
        self.frame_points = None

    def Initialize(self, FPTV_FACTOR, frame_width, frame_height):
        self.FPTV_FACTOR = FPTV_FACTOR
        self.frame_width = frame_width
        self.frame_height = frame_height


    def Create_Frame_Points(self):        
        """ This function create additional point around frame
        :return: List with points
        """
        frame_points = []
        for i in range(25, 484, self.FPTV_FACTOR):
            frame_points.append(np.array([i, 37])) #góra
            frame_points.append(np.array([i, 355])) #dół
        for i in range(37, 355, self.FPTV_FACTOR):
            frame_points.append(np.array([25, i])) #prawo
            frame_points.append(np.array([484, i])) #lewo
        self.frame_points = frame_points
        return frame_points


    def Corners_To_Voronoi(self, corners):
        """ This function return corners array in specific format which is needed for voronoi function.
        :return: Corners in specific format
        """
        frame_points = self.Create_Frame_Points()
        new = []
        for cor in corners:
            for corl2 in cor:
                new.append(corl2)
        for i in frame_points:
            new.append(i)
        return new

    def Calculate_Voronoi(self, corners):
        """ calculate points by voronoi method
        """
        vor = scipy.spatial.Voronoi(corners)
        clean_vertices = []
        for ver in vor.ridge_vertices:
            if ver[0] != -1:
                clean_vertices.append(ver)
        self.voronoi_to_print = vor
        return vor, clean_vertices

    def Check_If_Point_Is_Inside_Marker(self, cor1, cor2, point):
        """ Checks if point is inside rectangle describe by two point (two corners)
        Args:
            cor1 (list): coordiantes of rectangle's upper-left corner
            cor2 (list): coordinates of rectangle's bottom-right corner
            point (list): coordinated of point to check
        Returns:
            [bool]: True if point is inside rectangle, Otherwise False
        """
        if (point[0] > cor1[0] and point[0] < cor2[0] and
                point[1] > cor1[1] and point[1] < cor2[1]):
            return True
        else:
            return False


    def Get_Points_Ids_From_Obstacles(self, vor, obstacles):
        """ removes vertices which are inside obstacles
        Args:
            vor (list): Voronoi vertices
            obstacles (list): obstacles coordinates

        Returns:
            [list]: new vertices array and ids of removed points
        """
        ids = []
        for i in range(0, len(vor.vertices)):
            for obs in obstacles:
                if (self.Check_If_Point_Is_Inside_Marker(obs[0], obs[2], vor.vertices[i]) == True) or (self.Check_If_Point_Is_Inside_Marker(obs[1], obs[3],vor.vertices[i]) == True):
                    ids.append(i)
        return ids


    def Check_If_number_Is_Inside_array(self, number, arrray):
        """ check if in ids array is some number equal to i
        """
        for id in arrray:
            if number == id:
                return True
        return False

    # Function 
    def Create_Dictionary(self, vor, ids):
        """ create dictionary to connect points which ids
        Args:
            vor (list): Voronoi vertices
            ids (list): Points ids
        Returns:
            [dict]: required dictionary
        """
        dict = {}
        for i in range(0, len(vor.vertices)):
            if self.Check_If_number_Is_Inside_array(i, ids) == False:
                dict[str(i)] = [int(vor.vertices[i][0]), int(vor.vertices[i][1])]
        return dict


    def Check_If_Any_Equal(self, a,b):
        """ check if in set A is some element also in set B
        Returns:
            [bool]: True if any element is equal
        """

        for A in a:
            for B in b:
                if A == B:
                    return True
        return False


    def Calculate_Distances_And_Make_Graph_Input(self, clean_ver, dict, removed_ids):
        """ calculate distances between two nodes and and create data for graph in specific format
        """
        graph_input = []
        for conn in clean_ver:
            if self.Check_If_Any_Equal(conn, removed_ids) == False:
                tmp_dist = distance.euclidean(dict.get(str(conn[0])), dict.get(str(conn[1])))
                if tmp_dist < 1: tmp_dist = 1
                graph_input.append(tuple([str(conn[0]), str(conn[1]), int(tmp_dist)]))
                graph_input.append(tuple([str(conn[1]), str(conn[0]), int(tmp_dist)]))
        return graph_input


    def Plot_Voronoi_Diagram(self):
        if self.voronoi_to_print != None:
            scipy.spatial.voronoi_plot_2d(self.voronoi_to_print)
            plt.xlim((0, self.frame_width))
            plt.ylim((self.frame_height, 0))
            plt.show()

    def Create_Voronoi_Graph(self, corners, obstacles):
        points_to_voronoi = self.Corners_To_Voronoi(corners)
        calculated_voronoi, clean_vertices = self.Calculate_Voronoi(points_to_voronoi)
        removed_points_ids = self.Get_Points_Ids_From_Obstacles(calculated_voronoi, obstacles)
        calculated_voronoi_dictionary = self.Create_Dictionary(calculated_voronoi, removed_points_ids)
        return self.Calculate_Distances_And_Make_Graph_Input(clean_vertices, calculated_voronoi_dictionary, removed_points_ids), calculated_voronoi_dictionary


if __name__=="__main__":

    corners = [[[266,73],[266,104],[235,103],[236,72]],
               [[125,149],[156,147],[158,178],[126,180]],
               [[123,256],[153,257],[152,289],[121,287]]]
    obstacles = np.array([[[123, 256],[153, 257],[152, 289],[121, 287]]])
    Voronoi = Voronoi()
    Voronoi.Initialize(25, 452, 314)
    graph, dict = Voronoi.Create_Voronoi_Graph(corners, obstacles)
    Voronoi.Plot_Voronoi_Diagram()
    print("Graph: ", graph , "\nDict: ", dict)
