import cv2
from read_var import read_var

def color_tracking(frame):
    obj_l = read_var("object_l")
    obj_h = read_var("object_h")

    hsv_roi = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv_roi, obj_l, obj_h)
    filtered_frame = cv2.bitwise_and(frame, frame, mask=mask)

    # Convert the frame to grayscale
    gray = cv2.cvtColor(filtered_frame, cv2.COLOR_BGR2GRAY)

    # Apply GaussianBlur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Threshold the image to binary
    _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY)

    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    cx = 0 
    cy = 0 

    if contours:
        # Find the largest contour by area
        largest_contour = max(contours, key=cv2.contourArea)

        # Draw the largest contour
        cv2.drawContours(frame, [largest_contour], -1, (0, 255, 0), 2)

        # Draw a bounding box around the largest contour
        x, y, w, h = cv2.boundingRect(largest_contour)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        # Find center of motion
        moments = cv2.moments(largest_contour)
        cx = int(moments["m10"] / moments["m00"])
        cy = int(moments["m01"] / moments["m00"])

        cv2.putText(frame, f"{cx}, {cy}", (x - 5, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        
        # # Optionally display the area of the largest contour
        # contour_area = cv2.contourArea(largest_contour)
        # cv2.putText(frame, f"Area: {int(contour_area)}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    return (cx, cy)





