from contextlib import nullcontext
import cv2
import numpy as np
from read_var import read_var

# Function to detect yellow squares
def find_colored_square(frame, cam):
    # Convert to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower = (0,0,0)
    higher = (179,255,255)

    if cam == 1:
        lower = read_var("color1_l")
        higher = read_var("color1_h")
    if cam == 2:
        lower = read_var("color2_l")
        higher = read_var("color2_h")

    # Define yellow color range in HSV
    lower_color = np.array(lower)  # Adjust these thresholds
    higher_color = np.array(higher)  # Adjust these thresholds

    # Create a mask for yellow
    yellow_mask = cv2.inRange(hsv, lower_color, higher_color)

    # Apply morphological operations to clean up noise
    kernel = np.ones((5, 5), np.uint8)
    yellow_mask = cv2.morphologyEx(yellow_mask, cv2.MORPH_CLOSE, kernel)

    # Detect edges in the yellow mask
    edges = cv2.Canny(yellow_mask, 50, 150)

    # Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # squares = []
    #
    # for contour in contours:
    #     # Approximate the contour to a polygon
    #     epsilon = 0.04 * cv2.arcLength(contour, True)  # Increase epsilon for more tolerance
    #     approx = cv2.approxPolyDP(contour, epsilon, True)
    #
    #     # Check if it has 4 vertices and is convex
    #     if len(approx) == 4 and cv2.isContourConvex(approx):
    #         # Calculate aspect ratio to ensure it's close to a square
    #         x, y, w, h = cv2.boundingRect(approx)
    #         aspect_ratio = float(w) / h
    #         if 0.8 <= aspect_ratio <= 1.2:  # Allow some tolerance for imperfect squares
    #             area = cv2.contourArea(approx)
    #             if area > 800:  # Filter by minimum area
    #                 squares.append(approx)
    # return squares

    square = None
    for contour in contours:
        # Approximate the contour to a polygon
        epsilon = 0.04 * cv2.arcLength(contour, True)  # Increase epsilon for more tolerance
        approx = cv2.approxPolyDP(contour, epsilon, True)
        area = 800

        # Check if it has 4 vertices and is convex
        if len(approx) == 4 and cv2.isContourConvex(approx):
            # Calculate aspect ratio to ensure it's close to a square
            _ , _, w, h = cv2.boundingRect(approx)
            aspect_ratio = float(w) / h
            contour_area = cv2.contourArea(approx)
            if 0.8 <= aspect_ratio <= 1.2 and contour_area > area:  # Allow some tolerance for imperfect squares
                square = approx

    return square

# Function to correct perspective of detected squares
def correct_perspective(frame, square):
    square = square.reshape(4, 2)
    square = sorted(square, key=lambda x: x[0])  # Sort by x-coordinates

    # Split into left and right halves
    left = sorted(square[:2], key=lambda x: x[1])  # Top-left, Bottom-left
    right = sorted(square[2:], key=lambda x: x[1])  # Top-right, Bottom-right

    # Define points in clockwise order
    square_sorted = np.array([left[0], right[0], right[1], left[1]], dtype="float32")

    # Define the desired square points
    size = max(
        np.linalg.norm(square_sorted[0] - square_sorted[1]),
        np.linalg.norm(square_sorted[1] - square_sorted[2]),
        np.linalg.norm(square_sorted[2] - square_sorted[3]),
        np.linalg.norm(square_sorted[3] - square_sorted[0]),
    )

    dst = np.array([
        [0, 0],
        [size - 1, 0],
        [size - 1, size - 1],
        [0, size - 1]
    ], dtype="float32")

    # Compute perspective transform matrix
    matrix = cv2.getPerspectiveTransform(square_sorted, dst)

    # Apply the perspective warp
    warped = cv2.warpPerspective(frame, matrix, (int(size), int(size)))

    return warped

# Open camera feed
# cap = cv2.VideoCapture(0)
#
# if not cap.isOpened():
#     print("Error: Could not open camera.")
#     exit()
#
# while True:
#     ret, frame = cap.read()
#     if not ret:
#         print("Error: Could not read frame.")
#         break
#
#     # Detect yellow squares
#     squares = find_colored_square(frame,1)
#
#     # Draw and correct perspective of each square
#     for square in squares:
#         corrected = correct_perspective(frame, square)
#         cv2.polylines(frame, [square], True, (0, 255, 0), 3)
#
#         # Show each corrected square in a separate window
#         cv2.imshow('Corrected Square', corrected)
#
#     # Display the frame with detected squares
#     cv2.imshow('Square Detection', frame)
#
#     # Press 'q' to exit
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
#
# cap.release()
# cv2.destroyAllWindows()

