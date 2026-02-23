"""
Day 3 — Real-time YOLO detector with decision logic.

Detects people in the webcam feed and logs events with timestamps.
Tracks presence state: logs when a person appears and when they leave.

Press 'q' to quit.
"""

import signal
import sys
import time
from datetime import datetime

import cv2
from ultralytics import YOLO


def handle_exit(sig, frame):
    print("\n" + "-" * 50)
    print("Session ended (Ctrl+C).")
    cap.release()
    cv2.destroyAllWindows()
    sys.exit(0)


signal.signal(signal.SIGINT, handle_exit)

# --- Config ---
CONFIDENCE_THRESHOLD = 0.7
PERSON_CLASS_ID = 0  # "person" in COCO dataset
COOLDOWN_SECONDS = 5  # minimum time between repeated "detected" logs

# Load model
model = YOLO("models/yolov8n.pt")

# Open webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("ERROR: Could not open webcam")
    exit(1)

print("Webcam opened. Press 'q' to quit.")
print(f"Watching for: person (confidence > {CONFIDENCE_THRESHOLD})")
print("-" * 50)

# State tracking
person_present = False
last_log_time = 0.0
prev_time = time.time()

while True:
    ret, frame = cap.read()
    if not ret:
        print("ERROR: Failed to read frame")
        break

    # Run YOLO inference
    results = model(frame, verbose=False)
    detections = results[0].boxes

    # --- Decision Logic ---
    # Check if any detection is a person with high confidence
    person_detected_this_frame = False
    best_confidence = 0.0

    for box in detections:
        cls_id = int(box.cls[0])
        conf = float(box.conf[0])

        if cls_id == PERSON_CLASS_ID and conf >= CONFIDENCE_THRESHOLD:
            person_detected_this_frame = True
            best_confidence = max(best_confidence, conf)

    # State transitions: person appeared or left
    now = time.time()
    timestamp = datetime.now().strftime("%H:%M:%S")

    if person_detected_this_frame and not person_present:
        # Person just appeared
        person_present = True
        last_log_time = now
        print(f"PERSON DETECTED at {timestamp} (confidence: {best_confidence:.2f})")

    elif person_detected_this_frame and person_present:
        # Person still there — log periodically based on cooldown
        if now - last_log_time >= COOLDOWN_SECONDS:
            last_log_time = now
            print(f"  person still present at {timestamp} (confidence: {best_confidence:.2f})")

    elif not person_detected_this_frame and person_present:
        # Person just left
        person_present = False
        print(f"PERSON LEFT at {timestamp}")

    # --- Display ---
    annotated = results[0].plot()

    # FPS
    fps = 1.0 / (now - prev_time) if (now - prev_time) > 0 else 0
    prev_time = now

    # Status overlay
    status = "PERSON PRESENT" if person_present else "No person"
    color = (0, 0, 255) if person_present else (0, 255, 0)

    cv2.putText(annotated, f"FPS: {fps:.1f}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    cv2.putText(annotated, status, (10, 65),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

    cv2.imshow("Detect & Decide", annotated)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
print("-" * 50)
print("Session ended.")
