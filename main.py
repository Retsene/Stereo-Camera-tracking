import cv2
from read_var import read_var 
from calibrated import calibrated
from find_square import *
from color_tracking import color_tracking
from camshift_tracking import camshift_tracking 

id1 = read_var("id1")
id2 = read_var("id2")
dist, mtx = calibrated() 

cap1 = cv2.VideoCapture(id1)
cap2 = cv2.VideoCapture(id2)

xco = "no value"
yco = "no value"
zco = "no value"
zco1 = 0 
zco2 = 0

while True:
    ret, frame1 = cap1.read()
    ret, frame2 = cap2.read()
    if not ret:
        break

    frame1 = cv2.undistort(frame1, mtx, dist, None, mtx)
    frame2 = cv2.undistort(frame2, mtx, dist, None, mtx)

    # Display the frame with detected rectangles
    square1 = find_colored_square(frame1,1)
    square2 = find_colored_square(frame2,2)

    # Draw and correct perspective of each square
    if square1 is not None:
        corrected = correct_perspective(frame1, square1)
        cv2.polylines(frame1, [square1], True, (0, 255, 0), 3)
        # cy, cx = color_tracking(corrected)
        cy, cx = camshift_tracking(corrected)
        by, bx = corrected.shape[:2]
        if cx <= 0 or bx <= 0:
            zco1 = "no value"
            xco = "no value"
        else:
            zco1 = round(9 - cx / bx * 8, 3)
            xco = round(cy / by * 8 + 1, 3)
        cv2.imshow('Square 1', corrected)
        # Show each corrected square in a separate window

    if square2 is not None:
        corrected = correct_perspective(frame2, square2)
        cv2.polylines(frame2, [square2], True, (0, 255, 0), 3)
        cy, cx = color_tracking(corrected)
        by, bx = corrected.shape[:2]
        if cx <= 0 or bx <= 0:
            zco2 = "no value"
            yco = "no value"
        else:
            zco2 = round(9 - cx / bx * 8, 3)
            yco = round(9 - cy / by * 8, 3)
        cv2.imshow('Square 2', corrected)

    cv2.putText(frame1, f"x coordinate: {xco}", (10, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    cv2.putText(frame1, f"y coordinate: {yco}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    if zco1 != 0 and zco2 == 0:
        zco = zco1
    elif zco1 == 0 and zco2 != 0: 
        zco = zco2 
    elif zco1 != 0 and zco2 != 0:
        zco = (zco1 + zco2) / 2
    cv2.putText(frame1, f"z coordinate: {zco}", (10, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    cv2.imshow('Camera 1', frame1)
    cv2.imshow('Camera 2', frame2)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()

