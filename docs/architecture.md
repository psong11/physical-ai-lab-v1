# System Architecture — Physical AI Lab

## The Physical AI Pipeline

Every Physical AI system follows the same four-stage loop:

```
SENSOR  -->  PERCEPTION  -->  REASONING  -->  ACTION
(raw data)   (understand)     (decide)        (respond)
```

This document maps our current implementation to each stage and outlines how the
architecture will evolve as we move to edge hardware.

---

## Stage 1: Sensor (Data Capture)

**What it does:** Captures raw data from the physical world.

**Current implementation:**
- MacBook webcam via OpenCV (`cv2.VideoCapture(0)`)
- Captures BGR frames at native resolution (typically 1280x720)
- Runs in a continuous `while True` loop — one frame per iteration

**Key detail:** The sensor layer knows nothing about what's in the frame. It just
delivers pixels.

**Future (Jetson):** USB or CSI camera connected to Jetson Orin Nano. Same
OpenCV API, different hardware. May add additional sensors (temperature,
audio) via MQTT in Phase 3.

---

## Stage 2: Perception (Object Detection)

**What it does:** Transforms raw pixels into structured understanding — "what
objects are in this frame, where are they, and how confident am I?"

**Current implementation:**
- **Model:** YOLOv8n (nano) from Ultralytics, pre-trained on COCO (80 classes)
- **Inference:** `model(frame, verbose=False)` — single-shot detection
- **Output per detection:** class ID, confidence score (0-1), bounding box (x1, y1, x2, y2)
- **Performance:** ~14-15 FPS on MacBook CPU

**Key detail:** Perception is stateless — it processes each frame independently
with no memory of previous frames. Temporal awareness comes from the Reasoning
stage.

**Future:** Fine-tuned model for capstone-specific classes (Week 2). ONNX export
and TensorRT optimization for faster inference on Jetson (Week 3-4).

---

## Stage 3: Reasoning (Decision Logic)

**What it does:** Takes structured perception output and applies rules to decide
what's happening and whether to respond.

**Current implementation (three layers of filtering):**

### 3a. Confidence Filtering
- Only consider detections above a confidence threshold (default: 0.70)
- Adjustable at runtime with `+`/`-` keys
- Eliminates false positives from low-confidence detections

### 3b. Spatial Filtering (Detection Zone)
- A rectangular region of interest (default: center 60% of frame)
- Only detections with bounding-box center inside the zone trigger events
- Toggle on/off with `z` key
- Eliminates irrelevant detections outside the area of interest

### 3c. State Tracking & Temporal Logic
- Tracks binary state: `person_present` (True/False)
- **State transitions:**
  - `not present → detected` = log "PERSON DETECTED" with timestamp
  - `present → still present` = periodic update log (5-second cooldown)
  - `present → not detected` = log "PERSON LEFT"
- Cooldown timer prevents log spam during sustained presence

**Key detail:** The reasoning layer is where the system goes from "I see pixels"
to "a person just entered my zone." This is the core of Physical AI — rules
that bridge perception to action.

**Future:** Object tracking across frames (ByteTrack), temporal rules ("person in
zone > 30s"), anomaly detection.

---

## Stage 4: Action (System Response)

**What it does:** Produces an observable effect in response to a reasoning decision.

**Current implementation:**
- **Console logging:** Prints timestamped events (DETECTED / LEFT / still present)
- **Visual overlay:** On-screen status panel showing FPS, confidence, zone status, presence state, person count
- **Visual feedback:** Green "ZONE" rectangle, red/green status text

**Future:** SQLite event logging, MQTT event publishing, webhook/email
notifications, API endpoint (`/status`), dashboard.

---

## How the Stages Connect (Current Code)

```
detect_zones.py — main loop
│
├── SENSOR: cap.read() → raw BGR frame
│
├── PERCEPTION: model(frame) → list of (class, confidence, bbox)
│
├── REASONING:
│   ├── Filter: class == person AND confidence > threshold
│   ├── Filter: bbox center inside detection zone
│   └── State: track person_present transitions + cooldown
│
└── ACTION:
    ├── Console: print timestamped event
    └── Display: annotated frame with info panel
```

---

## Code Map

| File | Stage(s) | Purpose |
|------|----------|---------|
| `src/01_webcam_detector/live_detect.py` | Sensor + Perception | Day 2: basic webcam → YOLO → bounding boxes |
| `src/01_webcam_detector/detect_and_decide.py` | All four | Day 3: added reasoning (state tracking) + action (logging) |
| `src/01_webcam_detector/detect_zones.py` | All four | Day 4: added zones, smoothed FPS, configurable confidence |

---

## Current Limitations

| Limitation | Impact | When We Fix It |
|------------|--------|----------------|
| No object tracking | Same person re-detected each frame as new | Week 9 (ByteTrack) |
| CPU-only inference | ~15 FPS, not real-time | Week 3 (ONNX/TensorRT) |
| No persistence | Events lost when script stops | Week 5 (SQLite) |
| Single sensor | Vision only, no environmental context | Week 6 (MQTT + sensors) |
| Hardcoded rules | Thresholds manual, no learning | Week 9 (temporal intelligence) |

---

## Architecture Evolution

```
WEEK 1 (NOW):
  Webcam → YOLOv8n → Rules → Console log

WEEK 3:
  Webcam → YOLOv8n (ONNX/FP16) → Rules → Console log

WEEK 5:
  Camera → YOLOv8n (TensorRT on Jetson) → Rules + Tracker → SQLite + API

WEEK 9:
  Camera → Fine-tuned model (TensorRT) → Tracker + Temporal logic → MQTT + Dashboard

WEEK 12 (CAPSTONE):
  Multi-sensor → Optimized model → Smart reasoning → Notifications + Dashboard
```
