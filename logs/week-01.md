# Week 1 — First Light

**Theme:** Get a working perception → decision loop on your laptop.
**Dates:** 2026-02-22 to 2026-02-28

---

## Day 1 — Sunday, Feb 22
**Goal:** Set up repo, Python venv, install OpenCV + Ultralytics YOLO

### What I Did
- Created project directory structure (MASTER_PLAN.md, CLAUDE.md, logs/)
- Installed Python 3.12 via Homebrew (3.14 too new for PyTorch)
- Initialized git repo
- Created venv, installed opencv-python + ultralytics (includes PyTorch)
- Verified all imports: OpenCV 4.13, PyTorch 2.10, MPS (Apple GPU) available
- Ran YOLOv8n on test image — detected bus + 4 people + stop sign
- Froze requirements.txt
- Jetson Orin Nano ordered — arriving Feb 23

### What's Next (Day 2)
- Run YOLOv8n on MacBook webcam with live bounding boxes
- Get real-time FPS display working

### Blockers/Notes
- Jetson arrives tomorrow — unbox and inspect but Phase 1 is laptop-only
- MacBook webcam is sufficient for Phase 1
- MPS (Apple Silicon GPU) is available — will use for faster inference

---

## Day 2 — Monday, Feb 23
**Goal:** Run YOLOv8n on webcam, draw bounding boxes in real-time

### What I Did
- Wrote `src/01_webcam_detector/live_detect.py` — real-time YOLO webcam detector
- Live bounding boxes with class labels and confidence scores working
- FPS overlay working — getting 14-15 FPS (CPU inference)
- Detects person reliably, confidence scores ~0.6-0.9
- Learned: confidence score = model's certainty per detection (0-1 scale)
- Jetson has NOT arrived yet

### What's Next (Day 3)
- Add decision logic: if person detected (confidence > 0.7) → log event with timestamp
- First perception → decision loop

### Blockers/Notes
- 14-15 FPS is CPU-only; could try MPS (GPU) later for speed boost
- No Jetson yet — still laptop-only


---

## Day 3 — Tuesday, Feb 24
**Goal:** Add decision logic — if person detected → log event with timestamp

### What I Did
- Built `src/01_webcam_detector/detect_and_decide.py` — first perception → decision loop
- Decision logic: detects person (COCO class 0, confidence > 0.7), logs with timestamp
- State tracking: logs PERSON DETECTED / PERSON LEFT transitions
- Cooldown (5s) prevents log spam while person is still present
- Added on-screen status overlay (red "PERSON PRESENT" / green "No person")
- Added Ctrl+C handler to both scripts (OpenCV `waitKey` only works when video window is focused)
- Tested and working — detects presence and absence correctly

### What's Next (Day 4)
- Add confidence thresholds (configurable), detection zones (regions of interest)
- Add FPS counter improvements

### Blockers/Notes
- `cv2.waitKey()` only captures keys when the OpenCV window is focused, not the terminal — added signal handler as workaround


---

## Day 4 — Wednesday, Feb 25
**Goal:** Add FPS counter, confidence thresholds, detection zones

### What I Did
- Built `src/01_webcam_detector/detect_zones.py` — upgraded detector with three new features
- Smoothed FPS: rolling average over 30 frames (deque) instead of frame-to-frame jitter
- Detection zone: green rectangle (center 60% of frame) — only person detections with bbox center inside the zone trigger events
- Live keyboard controls: +/- to adjust confidence threshold, z to toggle zone on/off
- Person count overlay: shows how many people are in the zone
- Info panel: FPS, confidence threshold, zone status, presence status all on screen
- Tested and working — zone filtering, threshold adjustment, and state transitions all correct

### What's Next (Day 5)
- Write first architecture doc: sensor → perception → reasoning → action
- Document how the system works end-to-end in `docs/architecture.md`

### Blockers/Notes
- None — on track for Week 1

---

## Day 5 — Thursday, Feb 26
**Goal:** Write first architecture doc: sensor → perception → reasoning → action

### What I Did
- Wrote `docs/architecture.md` — first architecture doc mapping the system to the Physical AI pipeline
- Documented all four stages: Sensor → Perception → Reasoning → Action
- Mapped each script (live_detect, detect_and_decide, detect_zones) to pipeline stages
- Added current limitations table with fix timeline
- Added architecture evolution diagram (Week 1 → Week 12)

### What's Next (Day 6-7)
- Build desk presence detector: track when I'm at desk, log session durations
- Builds on detect_zones.py with session timing logic

### Blockers/Notes
- None — on track for Week 1

---

## Day 6 — Friday, Feb 27
**Goal:** Build desk presence detector with session tracking

### What I Did
- Built `src/01_webcam_detector/desk_tracker.py` — desk presence tracker
- Three-state machine: AWAY → PRESENT → MAYBE_AWAY (grace period) → AWAY
- 15-second grace period prevents short absences (looking away, grabbing coffee) from ending a session
- CSV logging: each session written to `data/desk_sessions.csv` (date, start, end, duration)
- On-screen session timer shows live elapsed time (e.g., "AT DESK — 12m 34s")
- Grace period countdown displayed on screen when person disappears
- Session count overlay on video feed
- Quit summary: total sessions, total time, average/longest/shortest session
- If quit mid-session, that session is still logged

### What's Next (Day 7)
- Test the tracker in a real desk session
- Stretch: add daily/weekly summary stats, or a simple terminal report script

### Blockers/Notes
- None

