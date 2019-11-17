import numpy as np
import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg# prepare object points
nx = 8# number of inside corners in x
ny = 6 #number of inside corners in y# Make a list of calibration images
#fname = 'calibration_test.png'
#img = cv2.imread(fname)# Convert to grayscale

tmp = 1
path = ".\pictures_to_calib\ "


cap = cv2.VideoCapture(1)
if cap.isOpened() == True:
    print("OK")

while True:
    ret, img = cap.read()
    frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    copy_frame = frame.copy()
    ret, corners = cv2.findChessboardCorners(frame, (nx, ny), None)  # If found, draw corners
    if ret == True:
        # Draw and display the corners
        cv2.drawChessboardCorners(img, (nx, ny), corners, ret)
    cv2.imshow('frame',img)

    name = path + str(tmp)+".jpg"

    if cv2.waitKey(20) & 0xFF == ord('c'):
        cv2.imwrite(name, copy_frame)
        cv2.imshow("img", copy_frame)
        tmp += 1
        if cv2.waitKey(0) & 0xFF == ord('q'):
            break;

cap.release()
cv2.destroyAllWindows()









