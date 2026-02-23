"""
Week 2 — Data capture tool for Smart Desk Monitor.

Opens the webcam and saves frames to class-specific folders
when you press a key. Use this to build your training dataset.

Controls:
  f  — save frame as "focused" (you working normally)
  d  — save frame as "phone" (holding/looking at phone)
  a  — save frame as "away" (empty desk / not present)
  s  — show current capture counts
  q  — quit

Images are saved to data/raw/<class>/ with timestamps as filenames.
"""

import os
import signal
import sys
import time

import cv2

# --- Config ---
BASE_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "raw")
CLASSES = {
    ord("f"): "focused",
    ord("d"): "phone",
    ord("a"): "away",
}


def handle_exit(sig, frame):
    print("\nQuitting (Ctrl+C).")
    cap.release()
    cv2.destroyAllWindows()
    sys.exit(0)


signal.signal(signal.SIGINT, handle_exit)


def ensure_dirs():
    """Create output directories if they don't exist."""
    for class_name in CLASSES.values():
        path = os.path.normpath(os.path.join(BASE_DIR, class_name))
        os.makedirs(path, exist_ok=True)


def count_existing():
    """Count existing images per class."""
    counts = {}
    for class_name in CLASSES.values():
        path = os.path.normpath(os.path.join(BASE_DIR, class_name))
        if os.path.exists(path):
            counts[class_name] = len([f for f in os.listdir(path) if f.endswith(".jpg")])
        else:
            counts[class_name] = 0
    return counts


def save_frame(frame, class_name):
    """Save a frame to the appropriate class directory."""
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    # Add milliseconds to avoid collisions on rapid captures
    ms = f"{time.time() % 1:.3f}"[2:]
    filename = f"{timestamp}_{ms}.jpg"
    path = os.path.normpath(os.path.join(BASE_DIR, class_name, filename))
    cv2.imwrite(path, frame)
    return filename


# --- Setup ---
ensure_dirs()
counts = count_existing()

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("ERROR: Could not open webcam")
    exit(1)

print("Data Capture Tool — Smart Desk Monitor")
print("=" * 45)
print("Keys:  f=focused  d=phone  a=away  s=stats  q=quit")
print()
print("Existing images:")
for name, count in counts.items():
    print(f"  {name}: {count}")
print("-" * 45)

while True:
    ret, frame = cap.read()
    if not ret:
        print("ERROR: Failed to read frame")
        break

    # Draw key hints on frame
    display = frame.copy()
    cv2.putText(display, "f=focused  d=phone  a=away  q=quit",
                (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # Show counts
    y = 55
    for name in CLASSES.values():
        cv2.putText(display, f"{name}: {counts[name]}",
                    (10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        y += 25

    cv2.imshow("Data Capture", display)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break
    elif key == ord("s"):
        print("\nCurrent counts:")
        for name, count in counts.items():
            print(f"  {name}: {count}")
    elif key in CLASSES:
        class_name = CLASSES[key]
        filename = save_frame(frame, class_name)
        counts[class_name] += 1
        print(f"  [{class_name}] saved ({counts[class_name]} total)")

cap.release()
cv2.destroyAllWindows()

print()
print("=" * 45)
print("Final counts:")
for name, count in counts.items():
    print(f"  {name}: {count}")
print("=" * 45)
