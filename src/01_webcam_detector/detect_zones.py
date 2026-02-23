"""
Day 4 — Detection zones, smoothed FPS, and adjustable confidence.

Upgrades from detect_and_decide.py:
  - Smoothed FPS (rolling average over 30 frames)
  - Detection zone: only triggers when a person's bbox center is inside the zone
  - Live confidence adjustment with +/- keys
  - Info panel overlay

Controls:
  q       — quit
  +/=     — raise confidence threshold by 0.05
  -       — lower confidence threshold by 0.05
  z       — toggle detection zone on/off

Press 'q' to quit.
"""

import signal
import sys
import time
from collections import deque
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
PERSON_CLASS_ID = 0  # "person" in COCO dataset
COOLDOWN_SECONDS = 5
FPS_WINDOW = 30  # number of frames for rolling FPS average

# Detection zone as fraction of frame (top-left x, y, bottom-right x, y)
# Default: center 60% of the frame
ZONE_FRAC = (0.2, 0.2, 0.8, 0.8)

# --- State ---
confidence_threshold = 0.7
zone_enabled = True
person_present = False
last_log_time = 0.0
frame_times = deque(maxlen=FPS_WINDOW)

# Load model
model = YOLO("models/yolov8n.pt")

# Open webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("ERROR: Could not open webcam")
    exit(1)

# Get frame dimensions for zone calculation
ret, test_frame = cap.read()
if not ret:
    print("ERROR: Could not read initial frame")
    exit(1)
frame_h, frame_w = test_frame.shape[:2]

# Detection zone in pixel coordinates
zone_x1 = int(frame_w * ZONE_FRAC[0])
zone_y1 = int(frame_h * ZONE_FRAC[1])
zone_x2 = int(frame_w * ZONE_FRAC[2])
zone_y2 = int(frame_h * ZONE_FRAC[3])

print("Webcam opened. Controls: q=quit, +/-=confidence, z=toggle zone")
print(f"Frame size: {frame_w}x{frame_h}")
print(f"Detection zone: ({zone_x1},{zone_y1}) to ({zone_x2},{zone_y2})")
print(f"Confidence threshold: {confidence_threshold}")
print("-" * 50)

prev_time = time.time()

while True:
    ret, frame = cap.read()
    if not ret:
        print("ERROR: Failed to read frame")
        break

    # --- FPS (rolling average) ---
    now = time.time()
    frame_times.append(now - prev_time)
    prev_time = now
    avg_fps = len(frame_times) / sum(frame_times) if sum(frame_times) > 0 else 0

    # --- YOLO inference ---
    results = model(frame, verbose=False)
    detections = results[0].boxes

    # --- Filter detections: person + confidence + zone ---
    person_detected_this_frame = False
    best_confidence = 0.0
    persons_in_zone = 0

    for box in detections:
        cls_id = int(box.cls[0])
        conf = float(box.conf[0])

        if cls_id != PERSON_CLASS_ID or conf < confidence_threshold:
            continue

        # Bounding box center
        x1, y1, x2, y2 = box.xyxy[0].tolist()
        cx = (x1 + x2) / 2
        cy = (y1 + y2) / 2

        # Zone check (skip if zone disabled — treat whole frame as zone)
        if zone_enabled:
            if not (zone_x1 <= cx <= zone_x2 and zone_y1 <= cy <= zone_y2):
                continue

        person_detected_this_frame = True
        best_confidence = max(best_confidence, conf)
        persons_in_zone += 1

    # --- State transitions ---
    timestamp = datetime.now().strftime("%H:%M:%S")

    if person_detected_this_frame and not person_present:
        person_present = True
        last_log_time = now
        print(f"PERSON DETECTED at {timestamp} "
              f"(confidence: {best_confidence:.2f}, count: {persons_in_zone})")

    elif person_detected_this_frame and person_present:
        if now - last_log_time >= COOLDOWN_SECONDS:
            last_log_time = now
            print(f"  person still present at {timestamp} "
                  f"(confidence: {best_confidence:.2f}, count: {persons_in_zone})")

    elif not person_detected_this_frame and person_present:
        person_present = False
        print(f"PERSON LEFT at {timestamp}")

    # --- Display ---
    annotated = results[0].plot()

    # Draw detection zone
    if zone_enabled:
        cv2.rectangle(annotated, (zone_x1, zone_y1), (zone_x2, zone_y2),
                       (0, 255, 0), 2)
        cv2.putText(annotated, "ZONE", (zone_x1 + 5, zone_y1 + 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # Info panel (top-left)
    status = "PERSON IN ZONE" if person_present else "No person"
    status_color = (0, 0, 255) if person_present else (0, 255, 0)

    y_offset = 25
    cv2.putText(annotated, f"FPS: {avg_fps:.1f}", (10, y_offset),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    y_offset += 30
    cv2.putText(annotated, f"Conf: {confidence_threshold:.2f} (+/-)", (10, y_offset),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    y_offset += 30
    cv2.putText(annotated, f"Zone: {'ON (z)' if zone_enabled else 'OFF (z)'}",
                (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    y_offset += 30
    cv2.putText(annotated, status, (10, y_offset),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, status_color, 2)
    if person_present:
        y_offset += 30
        cv2.putText(annotated, f"Count: {persons_in_zone}", (10, y_offset),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    cv2.imshow("Detect & Decide (Zones)", annotated)

    # --- Keyboard controls ---
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
    elif key in (ord("+"), ord("=")):
        confidence_threshold = min(0.95, confidence_threshold + 0.05)
        print(f"  [config] confidence threshold → {confidence_threshold:.2f}")
    elif key == ord("-"):
        confidence_threshold = max(0.1, confidence_threshold - 0.05)
        print(f"  [config] confidence threshold → {confidence_threshold:.2f}")
    elif key == ord("z"):
        zone_enabled = not zone_enabled
        print(f"  [config] detection zone → {'ON' if zone_enabled else 'OFF'}")

cap.release()
cv2.destroyAllWindows()
print("-" * 50)
print("Session ended.")
