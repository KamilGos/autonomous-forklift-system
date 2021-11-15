from cv2 import aruco
import matplotlib.pyplot as plt
import matplotlib as mpl

aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)

fig = plt.figure()

NUMBER_OF_MARKERS = 3 #How many markers do you want to create?

for i in range(0, NUMBER_OF_MARKERS):
    img = aruco.drawMarker(aruco_dict,i, 700)
    plt.imshow(img, cmap = mpl.cm.gray, interpolation = "nearest")
    plt.axis("off")
    plt.show()
