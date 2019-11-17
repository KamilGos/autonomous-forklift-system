import numpy as np
import cv2 as cv2
from cv2 import aruco
from scipy.spatial import distance
import math
import copy
print("Starting algorithm")
left = 60
right = 580
top = 50
bottom = 430
height = bottom - top
width =  right  - left
SKALA = 2.23 #mm
CAMERA_HEIGHT = 1530 #mm
ROBOT_HEIGHT = 167 #mm
map_center = (int(width/2), int(height/2))

def Get_Centers_Of_Corners(corners):
    corners=[corners]
    centers = []
    for c in corners:
        M = cv2.moments(c)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        centers.append((cX, cY))
    return centers

def Create_Dictionary_Of_Corners(corners, idss):
    ids = np.squeeze(idss)
    dict = {}
    iter = 0
    if len(idss)>1:
        for id in ids:
            dict[str(id)] = corners[iter]
            iter = iter + 1
    else:
        dict[str(idss[0][0])]=corners[0]
    return dict


def Easy_Corners_And_Ids(corners, ids):
    if np.shape(corners)[0] != 1:
        tmp = np.squeeze(corners, axis=(1))  # delete one dimension
        tmp = tmp.astype(int)  # change type
        return tmp[::-1], ids[::-1]
    else:
        tmp = np.squeeze(corners, axis=(1))  # delete one dimension
        tmp = tmp.astype(int)
        tmp = np.array([tmp])
        return tmp, ids

def Determine_Angle_XY(X, Y):
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

def Calculate_Perspective_Error(corners):
    centers = Get_Centers_Of_Corners(corners)
    dist = int(distance.euclidean(map_center, centers[0]))
    real_dist = dist * SKALA
    diff = (real_dist * ROBOT_HEIGHT) / CAMERA_HEIGHT
    diff = diff/SKALA
    return diff, centers[0]

def Delete_Perspective_ArUcos(corners):
    error, center = Calculate_Perspective_Error(corners)
    alpha_angle = Determine_Angle_XY((center[0]-map_center[0]),(center[1]-map_center[1]))
    if alpha_angle >= 0 and alpha_angle<90: # I ćwiartka
        beta_angle = 90 - alpha_angle
        # print("I")
    elif alpha_angle>=90 and alpha_angle<180: # II ćwiartka
        beta_angle = alpha_angle - 90
        # print("II")
    elif alpha_angle>=180 and alpha_angle<270: # 3 ćwiartka
        beta_angle = 270 - alpha_angle
        # print("III")
    elif alpha_angle>=270 and alpha_angle<=360: # IV ćwiartka
        beta_angle = alpha_angle - 270
        # print("IV")

    X = int(error*math.sin(math.radians(beta_angle)))
    Y = int(error*math.cos(math.radians(beta_angle)))

    new_corners = []
    for point in corners:
        if   point[0] > map_center[0] and point[1] < map_center[1]: # I ćwiartka
            new_corners.append([int(point[0] - X), int(point[1] + Y)])
        elif point[0] < map_center[0] and point[1] < map_center[1]: # II ćwiartka
            new_corners.append([int(point[0] + X), int(point[1] + Y)])
        elif point[0] < map_center[0] and point[1] > map_center[1]:  # III ćwiartka
            new_corners.append([int(point[0] + X), int(point[1] - Y)])
        elif point[0] > map_center[0] and point[1] > map_center[1]:  # IV ćwiartka
            new_corners.append([int(point[0] - X), int(point[1] - Y)])
    return new_corners



mtx = np.array([[733.65108925, 0,            341.18570973],
       [0,            733.86740229, 229.70186298],
       [0,            0,            1.          ]])
dist = np.array([[-0.00808862, -0.68700529,  0.00278835,  0.00466333,  1.65299464]])

cap = cv2.VideoCapture(1)
if cap.isOpened() == True:
    print("OK")

aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)
parameters = aruco.DetectorParameters_create()

while True:
    ret, frame = cap.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = cv2.undistort(frame, mtx, dist, None, mtx)
    frame = frame[top:bottom, left:right]

    corners, ids, rejectedImgPoints = aruco.detectMarkers(frame, aruco_dict, parameters=parameters)

    if np.all(ids != None):
        ids_copy = ids.copy()

        ecorners, eids = Easy_Corners_And_Ids(corners, ids)

        dict = Create_Dictionary_Of_Corners(ecorners, eids)
        ids = ids.tolist()
        if [0] in ids:
            idx = ids.index([0])
            new_corners = np.array(Delete_Perspective_ArUcos(dict[str('0')]))
            corners[idx][0] = new_corners
        frame = aruco.drawDetectedMarkers(frame, corners, ids_copy)

        for point in new_corners:
            cv2.circle(frame, tuple(point), 2, (255,255,255), 2)


    #
        # new_dict = Repleace_Corners_In_Dict(corners, Delete_Perspective_ArUcos(dict[str('0')]), 0)
        #q
        #



    cv2.circle(frame, map_center, 2, (0,0,0), 2)
    cv2.imshow('frame',frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()