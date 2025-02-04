import cv2
import numpy as np
from read_var import read_var

def calibrated():
# Load checkerboard images for calibration
    dimensions = read_var("dim")
    # CHECKERBOARD = (9,7)
    CHECKERBOARD = dimensions 

# Arrays to store object points and image points
    obj_points = []  # 3D points in real world space
    img_points = []  # 2D points in image plane

# Prepare the object points like (0,0,0), (1,0,0), ..., (6,5,0)
    objp = np.zeros((CHECKERBOARD[0] * CHECKERBOARD[1], 3), np.float32)
    objp[:, :2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)
    num = read_var("num")
    if num == 0:
        raise ValueError("No image in folder!")
# Read calibration images
    images = [cv2.imread(f'images/img{i}.png') for i in range(0,num)]  # Replace with your image paths

    for img in images:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, corners = cv2.findChessboardCorners(gray, CHECKERBOARD, None)

        if ret:
            obj_points.append(objp)
            img_points.append(corners)

# Calibrate the camera
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(obj_points, img_points, gray.shape[::-1], None, None)
    print(f'CameraMatrix: {mtx}')
    print(f'Dist: {dist}')# Undistort the live camera feed

    mean_error = 0
    for i in range(len(obj_points)):
        imgpoints2, _ = cv2.projectPoints(obj_points[i], rvecs[i], tvecs[i], mtx, dist)
        error = cv2.norm(img_points[i], imgpoints2, cv2.NORM_L2)/len(imgpoints2)
        mean_error += error

    print( "total error: {}".format(mean_error/len(obj_points)) )
    return (dist, mtx)

# print(f'CameraMatrix: {mtx}')
# print(f'Dist: {dist}')# Undistort the live camera feed
#
# cap = cv2.VideoCapture(0)
# while True:
#     ret, frame = cap.read()
#     if not ret:
#         break
#
#     # Apply undistortion
#     undistorted = cv2.undistort(frame, mtx, dist, None, mtx)
#
#
#     # Display the frame with detected rectangles
#
#     cv2.imshow('Original', frame)
#     cv2.imshow('Undistorted', undistorted)
#
#     # Press 'q' to exit
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
#
# cap.release()
# cv2.destroyAllWindows()
#
