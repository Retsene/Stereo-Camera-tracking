import cv2
import numpy as np
import sys
from read_var import read_var
from update_var import update_var


# Function to perform color filtering
def filter():
    id = read_var("id" + sys.argv[1])
    # Open the webcam
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not access the camera.")
        return

    # Create a window with trackbars for dynamic HSV tuning
    cv2.namedWindow("Trackbars")

    # Trackbar callback function (does nothing)
    def nothing(_):
        pass

    # Create trackbars for HSV ranges
    cv2.createTrackbar("Lower H", "Trackbars", 0, 179, nothing)
    cv2.createTrackbar("Lower S", "Trackbars", 0, 255, nothing)
    cv2.createTrackbar("Lower V", "Trackbars", 0, 255, nothing)
    cv2.createTrackbar("Upper H", "Trackbars", 179, 179, nothing)
    cv2.createTrackbar("Upper S", "Trackbars", 255, 255, nothing)
    cv2.createTrackbar("Upper V", "Trackbars", 255, 255, nothing)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break

        # Convert frame to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Get HSV values from trackbars
        lh = cv2.getTrackbarPos("Lower H", "Trackbars")
        ls = cv2.getTrackbarPos("Lower S", "Trackbars")
        lv = cv2.getTrackbarPos("Lower V", "Trackbars")
        uh = cv2.getTrackbarPos("Upper H", "Trackbars")
        us = cv2.getTrackbarPos("Upper S", "Trackbars")
        uv = cv2.getTrackbarPos("Upper V", "Trackbars")

        lower = (lh,ls,lv)
        higher = (uh,us,uv)
        # Define lower and upper HSV bounds
        lower_bound = np.array([lh, ls, lv])
        upper_bound = np.array([uh, us, uv])

        # Create a mask based on the HSV range
        mask = cv2.inRange(hsv, lower_bound, upper_bound)

        # Apply the mask to the original frame
        filtered_frame = cv2.bitwise_and(frame, frame, mask=mask)

        # Show the original frame, mask, and filtered frame
        cv2.imshow("Mask", mask)
        cv2.imshow("Filtered Frame", filtered_frame)

        k = cv2.waitKey(5)

        if k == ord('q'):
            break
        elif k == ord('1'): 
            update_var("color1_l", str(lower))
            update_var("color1_h", str(higher))
            print("frame color 1 saved!")

        elif k == ord('2'): 
            update_var("color2_l", str(lower))
            update_var("color2_h", str(higher))
            print("frame color 2 saved!")

        elif k == ord('3'): 
            update_var("object_l", str(lower))
            update_var("object_h", str(higher))
            print("object color saved!")

    # Release resources
    cap.release()
    cv2.destroyAllWindows()

filter()
