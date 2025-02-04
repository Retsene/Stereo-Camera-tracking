import numpy as np
import cv2
from read_var import read_var

def camshift_tracking(frame):
# take first frame of the video
    w, h, _ = frame.shape
    track_window = (0, 0, w, h)


    obj_l = read_var("object_l")
    obj_h = read_var("object_h")

    hsv_roi = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv_roi, obj_l, obj_h)
    roi_hist = cv2.calcHist([hsv_roi], [0], mask, [180], [0, 180])
    cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)

# Setup the termination criteria, either 10 iteration or move by at least 1 pt
    term_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)

    x = 0
    y = 0
    tracking_points = []

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    dst = cv2.calcBackProject([hsv], [0], roi_hist, [0, 180], 1)

    # apply camshift to get the new location
    ret, track_window = cv2.CamShift(dst, track_window, term_crit)

    # Draw it on image
    pts = cv2.boxPoints(ret)
    pts = np.intp(pts)

    center = tuple(np.intp(ret[0]))
    x, y = center
    tracking_points.append(center)

    for i in range(1, len(tracking_points)):
        x1, y1 = tracking_points[i - 1]
        x2, y2 = tracking_points[i - 2]

        cv2.line(frame, tracking_points[i - 1], tracking_points[i], (0, 255, 0), 2)

    cv2.polylines(frame, [pts], True, 255, 2)
    cv2.putText(frame, f"{x}, {y}", (x - 5, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        # frame = cv2.flip(frame, 1)
        # cv2.imshow("frame", frame)
        #
        # k = cv2.waitKey(fps) & 0xFF
        # if k == 27:
        #     break
    return (x,y)
