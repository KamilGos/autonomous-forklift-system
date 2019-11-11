import numpy as np
import cv2
import cv2.aruco as aruco
import math
import copy
from matplotlib import pyplot as plt

def easy_corners_and_ids(corners, ids):
    if np.shape(corners)[0] != 1:
        tmp = np.squeeze(corners, axis=(1))#delete one dimension
        tmp = tmp.astype(int)    #change type
        return tmp[::-1], ids[::-1]
    else:
        tmp = np.squeeze(corners, axis=(1))#delete one dimension
        tmp = tmp.astype(int)
        tmp = np.array([tmp])
        return tmp, ids


cap = cv2.VideoCapture(1)
left = 85
right = 540
top = 85
bottom = 405

for i in range(10):
    ret, frame = cap.read()
frame = frame[top:bottom, left:right]

# frame = cv2.flip(frame, +1)

copy_frame = np.copy(frame)
# copy_frame = copy_frame[80:400, 100:555]
copy_frame = cv2.cvtColor(copy_frame, cv2.COLOR_BGR2GRAY)

aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)
parameters = aruco.DetectorParameters_create()

corners, ids, rejectedImgPoints = aruco.detectMarkers(copy_frame, aruco_dict, parameters=parameters)
copy_corners = copy.deepcopy(corners)
copy_ids = copy.deepcopy(ids)



if len(corners)>0:
    print("Corners:", corners)
    print("shape BF", np.shape(corners))
    corners, ids = easy_corners_and_ids(corners, ids)
    print("AF",corners)
    print("shape AF", np.shape(corners))
    print("Corners1:", corners)

    # cv2.putText(copy_frame, str(round(rotations[0], 2)), (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255),2)
    # print(corners[0][0][0])
    # cv2.putText(copy_frame, str(0), (corners[0][0][0]-20, corners[0][0][1]-6), cv2.FONT_HERSHEY_SIMPLEX, 1,(255, 255, 255),2)
    # cv2.putText(copy_frame, str(1), (corners[0][1][0]-5,    corners[0][1][1]-6), cv2.FONT_HERSHEY_SIMPLEX, 1,(255, 255, 255),2)
    # cv2.putText(copy_frame, str(2), (corners[0][2][0],    corners[0][2][1]+20), cv2.FONT_HERSHEY_SIMPLEX, 1,(255, 255, 255),2)
    # cv2.putText(copy_frame, str(3), (corners[0][3][0]-20, corners[0][3][1]+20), cv2.FONT_HERSHEY_SIMPLEX, 1,(255, 255, 255),2)
    #
    # for i in range(0, len(ids)):
    #     for j in range(4):
    #         cv2.circle(copy_frame, tuple(corners[i][j]), 2, (255,255,255), 2)

    gray = aruco.drawDetectedMarkers(copy_frame, copy_corners, copy_ids)



plt.imshow(copy_frame, cmap='gray', interpolation='bicubic')
plt.xticks([]), plt.yticks([])
plt.savefig('detected3_aruco_clean.pdf', dpi=300)
plt.show()

# cv2.imshow('image',copy_frame)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# When everything done, release the capture

