"""
Day 6 — Desk presence tracker.

Builds on detect_zones.py to create a useful application:
  - Tracks when you sit down / get up from your desk
  - Logs each session (start, end, duration) to a CSV file
  - Grace period: brief absences (< 15s) don't end the session
  - On-screen timer shows current session length
  - Quit summary: total sessions, total time, average duration

State machine:
  AWAY → person detected → PRESENT (session starts)
  PRESENT → person disappears → MAYBE_AWAY (grace period starts)
  MAYBE_AWAY → person returns within grace period → PRESENT (session continues)
  MAYBE_AWAY → grace period expires → AWAY (session ends, logged to CSV)

Controls:
  q       — quit (prints session summary)
  +/=     — raise confidence threshold by 0.05
  -       — lower confidence threshold by 0.05
  z       — toggle detection zone on/off
"""

import csv
import os
import signal
import sys
import time
from collections import deque
from datetime import datetime
from enum import Enum

import cv2
from ultralytics import YOLO

# --- State machine ---
class State(Enum):
    AWAY = "AWAY"
    PRESENT = "PRESENT"
    MAYBE_AWAY = "MAYBE_AWAY"


def handle_exit(sig, frame):
    """Handle Ctrl+C — print summary and clean up."""
    print("\n" + "-" * 50)
    print("Session ended (Ctrl+C).")
    print_summary()
    cap.release()
    cv2.destroyAllWindows()
    sys.exit(0)


signal.signal(signal.SIGINT, handle_exit)

# --- Config ---
PERSON_CLASS_ID = 0
CONFIDENCE_THRESHOLD_DEFAULT = 0.7
FPS_WINDOW = 30
ZONE_FRAC = (0.2, 0.2, 0.8, 0.8)
GRACE_PERIOD_SECONDS = 15  # how long to wait before ending a session
CSV_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "desk_sessions.csv")

# --- State ---
confidence_threshold = CONFIDENCE_THRESHOLD_DEFAULT
zone_enabled = True
state = State.AWAY
session_start = None       # datetime when current session started
grace_start = None         # time.time() when grace period began
frame_times = deque(maxlen=FPS_WINDOW)

# Session history (for summary)
sessions = []  # list of (start_datetime, end_datetime, duration_seconds)


def ensure_csv():
    """Create the CSV file with headers if it doesn't exist."""
    csv_path = os.path.normpath(CSV_PATH)
    if not os.path.exists(csv_path):
        os.makedirs(os.path.dirname(csv_path), exist_ok=True)
        with open(csv_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["date", "start_time", "end_time", "duration_seconds"])


def log_session(start_dt, end_dt):
    """Append a completed session to the CSV and in-memory list."""
    duration = (end_dt - start_dt).total_seconds()
    sessions.append((start_dt, end_dt, duration))

    csv_path = os.path.normpath(CSV_PATH)
    with open(csv_path, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            start_dt.strftime("%Y-%m-%d"),
            start_dt.strftime("%H:%M:%S"),
            end_dt.strftime("%H:%M:%S"),
            f"{duration:.1f}",
        ])

    print(f"  SESSION LOGGED: {start_dt.strftime('%H:%M:%S')} → "
          f"{end_dt.strftime('%H:%M:%S')} ({format_duration(duration)})")


def format_duration(seconds):
    """Format seconds into a human-readable string."""
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    if h > 0:
        return f"{h}h {m:02d}m {s:02d}s"
    return f"{m}m {s:02d}s"


def print_summary():
    """Print a summary of all sessions from this run."""
    print("\n" + "=" * 50)
    print("DESK TRACKER SUMMARY")
    print("=" * 50)

    if not sessions:
        print("No completed sessions this run.")
        return

    total_seconds = sum(s[2] for s in sessions)
    avg_seconds = total_seconds / len(sessions)

    print(f"Sessions:      {len(sessions)}")
    print(f"Total time:    {format_duration(total_seconds)}")
    print(f"Avg session:   {format_duration(avg_seconds)}")
    print(f"Longest:       {format_duration(max(s[2] for s in sessions))}")
    print(f"Shortest:      {format_duration(min(s[2] for s in sessions))}")
    print()
    for i, (start, end, dur) in enumerate(sessions, 1):
        print(f"  {i}. {start.strftime('%H:%M:%S')} → {end.strftime('%H:%M:%S')}  "
              f"({format_duration(dur)})")
    print("=" * 50)


# --- Setup ---
ensure_csv()

model = YOLO("models/yolov8n.pt")

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("ERROR: Could not open webcam")
    exit(1)

ret, test_frame = cap.read()
if not ret:
    print("ERROR: Could not read initial frame")
    exit(1)
frame_h, frame_w = test_frame.shape[:2]

zone_x1 = int(frame_w * ZONE_FRAC[0])
zone_y1 = int(frame_h * ZONE_FRAC[1])
zone_x2 = int(frame_w * ZONE_FRAC[2])
zone_y2 = int(frame_h * ZONE_FRAC[3])

print("Desk Tracker started.")
print(f"Controls: q=quit, +/-=confidence, z=toggle zone")
print(f"Frame: {frame_w}x{frame_h}  |  Zone: ({zone_x1},{zone_y1})→({zone_x2},{zone_y2})")
print(f"Confidence: {confidence_threshold}  |  Grace period: {GRACE_PERIOD_SECONDS}s")
print(f"CSV: {os.path.normpath(CSV_PATH)}")
print("-" * 50)

prev_time = time.time()

while True:
    ret, frame = cap.read()
    if not ret:
        print("ERROR: Failed to read frame")
        break

    # --- FPS ---
    now = time.time()
    frame_times.append(now - prev_time)
    prev_time = now
    avg_fps = len(frame_times) / sum(frame_times) if sum(frame_times) > 0 else 0

    # --- YOLO inference ---
    results = model(frame, verbose=False)
    detections = results[0].boxes

    # --- Filter: person + confidence + zone ---
    person_in_zone = False
    best_conf = 0.0

    for box in detections:
        cls_id = int(box.cls[0])
        conf = float(box.conf[0])

        if cls_id != PERSON_CLASS_ID or conf < confidence_threshold:
            continue

        x1, y1, x2, y2 = box.xyxy[0].tolist()
        cx, cy = (x1 + x2) / 2, (y1 + y2) / 2

        if zone_enabled and not (zone_x1 <= cx <= zone_x2 and zone_y1 <= cy <= zone_y2):
            continue

        person_in_zone = True
        best_conf = max(best_conf, conf)

    # --- State machine ---
    timestamp = datetime.now()
    ts_str = timestamp.strftime("%H:%M:%S")

    if state == State.AWAY:
        if person_in_zone:
            state = State.PRESENT
            session_start = timestamp
            print(f"SESSION START at {ts_str} (conf: {best_conf:.2f})")

    elif state == State.PRESENT:
        if not person_in_zone:
            state = State.MAYBE_AWAY
            grace_start = now
            print(f"  person disappeared at {ts_str} — grace period ({GRACE_PERIOD_SECONDS}s)...")

    elif state == State.MAYBE_AWAY:
        if person_in_zone:
            # Person came back within grace period
            state = State.PRESENT
            grace_start = None
            print(f"  person returned at {ts_str} — session continues")
        elif now - grace_start >= GRACE_PERIOD_SECONDS:
            # Grace period expired — end session
            session_end = timestamp
            state = State.AWAY
            log_session(session_start, session_end)
            session_start = None
            grace_start = None

    # --- Display ---
    annotated = results[0].plot()

    # Detection zone
    if zone_enabled:
        cv2.rectangle(annotated, (zone_x1, zone_y1), (zone_x2, zone_y2),
                       (0, 255, 0), 2)
        cv2.putText(annotated, "ZONE", (zone_x1 + 5, zone_y1 + 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # Info panel
    y_off = 25
    cv2.putText(annotated, f"FPS: {avg_fps:.1f}", (10, y_off),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    y_off += 30
    cv2.putText(annotated, f"Conf: {confidence_threshold:.2f} (+/-)", (10, y_off),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    y_off += 30
    cv2.putText(annotated, f"Zone: {'ON' if zone_enabled else 'OFF'} (z)", (10, y_off),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    # State + session timer
    y_off += 30
    if state == State.PRESENT:
        elapsed = (timestamp - session_start).total_seconds()
        label = f"AT DESK — {format_duration(elapsed)}"
        color = (0, 0, 255)
    elif state == State.MAYBE_AWAY:
        grace_remaining = GRACE_PERIOD_SECONDS - (now - grace_start)
        label = f"MAYBE AWAY — grace {grace_remaining:.0f}s"
        color = (0, 165, 255)  # orange
    else:
        label = "AWAY"
        color = (0, 255, 0)

    cv2.putText(annotated, label, (10, y_off),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

    # Session count
    y_off += 30
    cv2.putText(annotated, f"Sessions today: {len(sessions)}", (10, y_off),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    cv2.imshow("Desk Tracker", annotated)

    # --- Keyboard controls ---
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
    elif key in (ord("+"), ord("=")):
        confidence_threshold = min(0.95, confidence_threshold + 0.05)
        print(f"  [config] confidence → {confidence_threshold:.2f}")
    elif key == ord("-"):
        confidence_threshold = max(0.1, confidence_threshold - 0.05)
        print(f"  [config] confidence → {confidence_threshold:.2f}")
    elif key == ord("z"):
        zone_enabled = not zone_enabled
        print(f"  [config] zone → {'ON' if zone_enabled else 'OFF'}")

# --- Cleanup ---
# If we were mid-session when quitting, log it
if state in (State.PRESENT, State.MAYBE_AWAY) and session_start:
    log_session(session_start, datetime.now())

cap.release()
cv2.destroyAllWindows()
print("-" * 50)
print_summary()
