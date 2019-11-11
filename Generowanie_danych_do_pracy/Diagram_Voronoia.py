import numpy as np
import random
import matplotlib.pyplot as plt
import matplotlib
from scipy.spatial import Voronoi, voronoi_plot_2d


points = np.array([[0, 0], [0, 1], [1, 0], [1, 1], [0.5, 0.5]])

# points = []
# for i in range(25):
#         points.append([random.randrange(1,100,1), random.randrange(1,100,1)])
#

vor = Voronoi(points)
font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 12}
matplotlib.rc('font', **font)
voronoi_plot_2d(vor)

plt.savefig('vor_5pkt.pdf', dpi=95)

plt.show()
