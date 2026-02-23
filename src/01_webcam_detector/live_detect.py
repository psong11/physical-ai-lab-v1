"""
Day 2 — Real-time YOLOv8n webcam detector with FPS display.

Press 'q' to quit.
"""

import signal
import sys
import time

import cv2
from ultralytics import YOLO


def handle_exit(sig, frame):
    print("\nDone (Ctrl+C).")
    cap.release()
    cv2.destroyAllWindows()
    sys.exit(0)


signal.signal(signal.SIGINT, handle_exit)

# Load the model (uses MPS on Apple Silicon automatically)
model = YOLO("models/yolov8n.pt")

# Open webcam (0 = default camera)
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("ERROR: Could not open webcam")
    exit(1)

print("Webcam opened. Press 'q' to quit.")

# FPS tracking
prev_time = time.time()

while True:
    ret, frame = cap.read()
    if not ret:
        print("ERROR: Failed to read frame")
        break

    # Run YOLO inference on the frame
    results = model(frame, verbose=False)

    # Draw bounding boxes + labels on the frame
    annotated = results[0].plot()

    # Calculate and display FPS
    now = time.time()
    fps = 1.0 / (now - prev_time)
    prev_time = now
    cv2.putText(
        annotated,
        f"FPS: {fps:.1f}",
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.0,
        (0, 255, 0),
        2,
    )

    # Show the frame
    cv2.imshow("YOLOv8n Live Detection", annotated)

    # Quit on 'q'
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
print("Done.")
