import cv2 as cv
import numpy as np
import time
import os

WINDOW_NAME = "Circle Detection - Almanahil"
cv.namedWindow(WINDOW_NAME, cv.WINDOW_NORMAL)
cv.resizeWindow(WINDOW_NAME, 960, 540)

def nothing(x):
    pass

# 🔧 Tuned default values (better starting point)
cv.createTrackbar("dp x10", WINDOW_NAME, 12, 30, nothing)
cv.createTrackbar("minDist", WINDOW_NAME, 150, 400, nothing)   # increased
cv.createTrackbar("param1", WINDOW_NAME, 100, 300, nothing)
cv.createTrackbar("param2", WINDOW_NAME, 50, 100, nothing)     # increased
cv.createTrackbar("minRadius", WINDOW_NAME, 30, 200, nothing)
cv.createTrackbar("maxRadius", WINDOW_NAME, 300, 500, nothing)
cv.createTrackbar("Blur Ksize", WINDOW_NAME, 3, 10, nothing)

video_capture = cv.VideoCapture(0, cv.CAP_AVFOUNDATION)

if not video_capture.isOpened():
    print("Camera not working")
    exit()

previous_circle = None
lost_frames = 0
MAX_LOST_FRAMES = 8

screenshot_dir = "screenshots"
os.makedirs(screenshot_dir, exist_ok=True)

def sq_distance(x1, y1, x2, y2):
    return (x1 - x2)**2 + (y1 - y2)**2

def put_text_bg(img, text, pos, font_scale=0.6, color=(0,255,0), thickness=1):
    font = cv.FONT_HERSHEY_SIMPLEX
    (tw, th), baseline = cv.getTextSize(text, font, font_scale, thickness)
    x, y = pos
    cv.rectangle(img, (x-2, y-th-4), (x+tw+2, y+baseline), (0,0,0), -1)
    cv.putText(img, text, (x,y), font, font_scale, color, thickness, cv.LINE_AA)

while True:
    ret, frame = video_capture.read()
    if not ret:
        break

    # Trackbars
    dp = max(1, cv.getTrackbarPos("dp x10", WINDOW_NAME)) / 10.0
    minDist = max(1, cv.getTrackbarPos("minDist", WINDOW_NAME))
    param1 = max(1, cv.getTrackbarPos("param1", WINDOW_NAME))
    param2 = max(30, cv.getTrackbarPos("param2", WINDOW_NAME))  # enforce minimum
    minR = cv.getTrackbarPos("minRadius", WINDOW_NAME)
    maxR = cv.getTrackbarPos("maxRadius", WINDOW_NAME)

    blur_k = cv.getTrackbarPos("Blur Ksize", WINDOW_NAME)
    blur_k = blur_k*2 + 1
    blur_k = max(3, blur_k)

    # Preprocessing (stable)
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    blurred = cv.GaussianBlur(gray, (blur_k, blur_k), 0)

    circles = cv.HoughCircles(
        blurred,
        cv.HOUGH_GRADIENT,
        dp=dp,
        minDist=minDist,
        param1=param1,
        param2=param2,
        minRadius=minR,
        maxRadius=maxR
    )

    selected_circle = None

    if circles is not None:
        circles = np.uint16(np.around(circles))
        valid = [c for c in circles[0,:] if minR <= c[2] <= maxR]

        if valid:
            if previous_circle is not None:
                px, py = previous_circle[0], previous_circle[1]
                selected_circle = min(valid, key=lambda c: sq_distance(c[0], c[1], px, py))
            else:
                selected_circle = max(valid, key=lambda c: c[2])

    if selected_circle is not None:
        previous_circle = selected_circle
        lost_frames = 0
    else:
        lost_frames += 1
        if lost_frames <= MAX_LOST_FRAMES and previous_circle is not None:
            selected_circle = previous_circle
        else:
            previous_circle = None

    output = frame.copy()

    if selected_circle is not None:
        x, y, r = int(selected_circle[0]), int(selected_circle[1]), int(selected_circle[2])

        if circles is not None:
            for c in circles[0]:
                cv.circle(output, (c[0], c[1]), c[2], (100,100,100), 1)

        cv.circle(output, (x,y), r, (255,0,255), 3)
        cv.circle(output, (x,y), 4, (0,255,0), -1)

        put_text_bg(output, f"Center: ({x},{y})", (x-r, y-r-30), color=(0,255,255))
        put_text_bg(output, f"Radius: {r}px", (x-r, y-r-10), color=(0,255,255))

    else:
        h, w = output.shape[:2]
        put_text_bg(output, "No circle detected", (w//2 - 100, h//2), color=(0,0,255), thickness=2)

    cv.imshow(WINDOW_NAME, output)

    key = cv.waitKey(1) & 0xFF

    if key == ord('q'):
        break

video_capture.release()
cv.destroyAllWindows()
