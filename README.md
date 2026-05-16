# Real-Time Circle Detection using OpenCV

A real-time circle detection system built with Python and OpenCV 
as part of the Computer Vision course at GUtech (April 2026).

## What it does
- Detects circles from a live webcam feed using the Hough Transform
- Tracks the detected circle across frames for stability
- Holds the last known position for up to 8 frames if detection 
  is briefly lost (anti-flicker)
- Rejects false circles by filtering on radius range and selecting 
  the circle closest to the previous frame
- Displays center coordinates, radius, FPS, and circle count 
  in real time

## Interactive Controls
All HoughCircles parameters are exposed as live trackbars:

| Parameter | Effect |
|-----------|--------|
| dp | Accumulator resolution ratio |
| minDist | Minimum distance between circle centres |
| param1 | Canny edge detector upper threshold |
| param2 | Accumulator threshold (higher = fewer, more confident) |
| minRadius | Ignore circles smaller than this |
| maxRadius | Ignore circles larger than this |
| Blur Ksize | Gaussian blur kernel size |

Press `S` to save a screenshot. Press `Q` to quit.

## Requirements
pip install opencv-python numpy

> Note: Uses cv2.CAP_AVFOUNDATION for macOS camera access.
> On Windows/Linux, change cv.VideoCapture(0, cv.CAP_AVFOUNDATION) to cv.VideoCapture(0)

## How to run
python final_tuned_circle.py

## Key improvements over baseline
1. Gaussian blur preprocessing to reduce noise
2. Interactive parameter tuning via trackbars
3. False circle rejection by radius filtering
4. Frame-to-frame stability tracking
5. Anti-flicker mechanism (holds position for 8 frames)
