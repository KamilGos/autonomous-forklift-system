import pickle
import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg# Read in the saved objpoints and imgpoints
mtx = np.array([[733.65108925, 0,            341.18570973],
       [0,            733.86740229, 229.70186298],
       [0,            0,            1.          ]])
dist = np.array([[-0.00808862, -0.68700529,  0.00278835,  0.00466333,  1.65299464]])


img = cv2.imread('distorted_image.png')
undist = cv2.undistort(img, mtx, dist, None, mtx)

cv2.imshow("ok", img)
cv2.imshow("dist", undist)
if cv2.waitKey(0) & 0xFF == ord('q'):
       exit(0)

# ax1.set_title('Original Image', fontsize=50)
# ax2.imshow(undist)
# ax2.set_title('Undistorted Image', fontsize=50)
# plt.subplots_adjust(left=0., right=1, top=0.9, bottom=0.)