# Physical AI Lab — 12-Week Master Plan

**Owner:** Paul Song
**Start Date:** 2026-02-22
**End Date:** 2026-05-17
**Time Budget:** ~60-90 min weekdays, 2-3 hrs weekends (~110-130 hours total)
**Status:** ACTIVE

---

## Mission

Build a real-world AI system that perceives, reasons, and acts locally on edge
hardware. Ship a portfolio-grade project with a GitHub repo, demo video, and
technical write-up.

This is not ML theory. This is embodied AI: sensors → models → decisions → effects.

---

## Guiding Principles

1. **Vertical slices over horizontal layers** — every week ships something working
2. **Fine-tune, don't train from scratch** — highest ROI for your time budget
3. **Laptop first, edge second** — prove the logic before fighting hardware
4. **One capstone, chosen early** — pick your target by end of Week 2
5. **Build > read** — 80% hands-on, 20% study

---

## Hardware & Software Stack

### Must-Have (Order in Week 1)
- **NVIDIA Jetson Orin Nano Developer Kit** (~$250) — primary edge device
- **USB webcam or CSI camera module** (~$25-50)
- **32GB+ microSD card** (for JetPack OS)
- **5V 4A barrel jack power supply** (check Jetson specs)

### Software
- Python 3.10+, PyTorch, OpenCV, Ultralytics (YOLOv8/v11)
- ONNX Runtime, TensorRT (on Jetson)
- Docker (for containerized deployment)
- MQTT/Mosquitto (for sensor data pipeline, Phase 3)
- Git + GitHub

### Nice-to-Have (Phase 3+)
- DHT22 temperature/humidity sensor + Arduino (if adding multi-sensor fusion)
- USB microphone (if adding audio detection)

---

## The 12-Week Roadmap

---

### PHASE 1: PERCEPTION FOUNDATIONS (Weeks 1-3)
> Goal: Real-time detection running on your laptop with a custom-tuned model.

---

#### Week 1 — First Light
**Theme:** Get a working perception → decision loop on your laptop in < 7 days.

| Day | Focus (60-90 min) | Done When |
|-----|-------------------|-----------|
| 1 | Set up repo, Python venv, install OpenCV + Ultralytics | `python -c "import cv2; from ultralytics import YOLO"` works |
| 2 | Run YOLOv8n on webcam, draw bounding boxes | Live webcam feed with bounding boxes rendering |
| 3 | Add decision logic: if person detected → log event with timestamp | Console prints "PERSON DETECTED at HH:MM:SS" |
| 4 | Add FPS counter, confidence thresholds, detection zones | Overlay shows FPS, only high-confidence detections shown |
| 5 | Write first architecture doc: sensor → perception → reasoning → action | `docs/architecture.md` committed |
| 6-7 | Weekend: build mini use case — desk presence detector (tracks when you're at desk, logs session durations) | Working desk tracker that logs "session started/ended" |

**Week 1 Deliverable:** `01_webcam_detector/` — working real-time detection with decision logic.

**Action Item:** Order Jetson Orin Nano + camera + power supply + SD card TODAY.

---

#### Week 2 — Custom Data & Fine-Tuning
**Theme:** Move from generic detection to YOUR specific use case.

| Day | Focus (60-90 min) | Done When |
|-----|-------------------|-----------|
| 1 | Decide on capstone direction (see Capstone Options below) | Decision documented in `docs/capstone_decision.md` |
| 2 | Collect 100-200 images relevant to your capstone scenario | Images saved in `data/raw/` |
| 3 | Label images using Roboflow (free tier) or CVAT | Annotations exported in YOLO format |
| 4 | Fine-tune YOLOv8n on your custom dataset | Training completes, mAP logged |
| 5 | Evaluate: run fine-tuned model on live webcam | Detections work for your custom classes |
| 6-7 | Weekend: collect more data from edge cases, retrain, improve | mAP improves; model handles tricky cases |

**Week 2 Deliverable:** `02_custom_model/` — fine-tuned model for your capstone domain.

---

#### Week 3 — Model Optimization
**Theme:** Make your model fast and portable.

| Day | Focus (60-90 min) | Done When |
|-----|-------------------|-----------|
| 1 | Export model to ONNX format | `.onnx` file exported and validated |
| 2 | Run ONNX inference on webcam, benchmark vs PyTorch | Comparison table: FPS, latency, model size |
| 3 | Study TensorRT concepts (read NVIDIA docs, watch 1 tutorial) | Can explain: what TensorRT does, INT8 vs FP16 vs FP32 |
| 4 | Try model quantization (FP16) and benchmark again | FP16 model runs faster, accuracy delta measured |
| 5 | Write optimization notes: what worked, what tradeoffs | `docs/optimization_notes.md` committed |
| 6-7 | Weekend: polish Phase 1 code, clean up repo, write Phase 1 README | Phase 1 code is clean, documented, and demo-able |

**Week 3 Deliverable:** `03_optimized_model/` — ONNX-exported, benchmarked, optimized model.

**PHASE 1 GATE:** Before moving on, verify:
- [ ] You have a custom fine-tuned model that runs on your webcam
- [ ] You have ONNX export working
- [ ] You have benchmark numbers (FPS, latency) documented
- [ ] Your Jetson hardware has arrived

---

### PHASE 2: EDGE DEPLOYMENT (Weeks 4-6)
> Goal: Your model running on the Jetson with real-time decision logic.

---

#### Week 4 — Jetson Setup & First Inference
**Theme:** Get your model running on real edge hardware.

| Day | Focus (60-90 min) | Done When |
|-----|-------------------|-----------|
| 1 | Flash JetPack OS onto SD card, boot Jetson | Jetson boots, you can SSH into it |
| 2 | Install Python, OpenCV, PyTorch (JetPack versions) on Jetson | Python imports work on Jetson |
| 3 | Transfer ONNX model to Jetson, run inference on a test image | Model produces correct detections on Jetson |
| 4 | Connect camera to Jetson, run real-time inference | Live detection on Jetson with camera feed |
| 5 | Benchmark: FPS/latency on Jetson vs laptop | Comparison table documented |
| 6-7 | Weekend: convert to TensorRT on Jetson, benchmark again | TensorRT model running, FPS improvement measured |

**Week 4 Deliverable:** `04_jetson_deployment/` — model running on Jetson with benchmarks.

---

#### Week 5 — Decision Logic on Edge
**Theme:** Your Jetson doesn't just see — it decides and acts.

| Day | Focus (60-90 min) | Done When |
|-----|-------------------|-----------|
| 1 | Port your decision logic from laptop to Jetson | Same perception → decision loop runs on Jetson |
| 2 | Add event logging: write detections to local SQLite or CSV | Events persisted to disk with timestamps |
| 3 | Add state management: track objects over time (simple IoU tracker) | System tracks object persistence across frames |
| 4 | Add alert logic: threshold-based triggers (e.g., "person in zone > 30s") | Alerts fire correctly based on temporal rules |
| 5 | Test edge cases: lighting changes, occlusion, multiple objects | Known failure modes documented |
| 6-7 | Weekend: build a simple status endpoint (Flask/FastAPI on Jetson) | `curl http://jetson-ip:8000/status` returns current state |

**Week 5 Deliverable:** `05_edge_decision_loop/` — full perception → decision → action pipeline on Jetson.

---

#### Week 6 — Data Pipeline & Persistence
**Theme:** Connect your edge system to the outside world.

| Day | Focus (60-90 min) | Done When |
|-----|-------------------|-----------|
| 1 | Install Mosquitto MQTT broker on Jetson | `mosquitto_sub -t test` receives messages |
| 2 | Publish detection events to MQTT topics | Events stream to MQTT in real-time |
| 3 | Write a subscriber script that logs MQTT events to a database | Events persisted from MQTT to SQLite/PostgreSQL |
| 4 | Add heartbeat/health monitoring (system temp, CPU, FPS) | Health metrics publishing every 30s |
| 5 | (Optional) Add a second sensor: temperature/humidity via Arduino → MQTT | Multi-sensor data flowing through same pipeline |
| 6-7 | Weekend: Dockerize the full pipeline on Jetson | `docker compose up` starts entire system |

**Week 6 Deliverable:** `06_data_pipeline/` — containerized pipeline with MQTT, persistence, health monitoring.

**PHASE 2 GATE:** Before moving on, verify:
- [ ] Model runs on Jetson with TensorRT optimization
- [ ] Decision logic fires correctly based on detections
- [ ] Events are logged and persisted
- [ ] System runs in Docker containers
- [ ] You can explain your full architecture to someone in 2 minutes

---

### PHASE 3: SYSTEM HARDENING & INTELLIGENCE (Weeks 7-9)
> Goal: Make it production-grade — reliable, measurable, and smart.

---

#### Week 7 — Reliability & Edge Cases
**Theme:** Make it work when the real world gets messy.

| Day | Focus (60-90 min) | Done When |
|-----|-------------------|-----------|
| 1 | Run system for 1+ hour continuously, identify crashes/memory leaks | Stability log with issues documented |
| 2 | Add error handling: camera disconnect recovery, model reload | System recovers gracefully from common failures |
| 3 | Add configuration file (YAML/JSON) for all thresholds/parameters | All magic numbers live in `config.yaml` |
| 4 | Implement graceful startup/shutdown sequence | Clean start and stop, no orphan processes |
| 5 | Write integration tests: feed recorded video, verify outputs | Test script validates expected detections |
| 6-7 | Weekend: run 4+ hour stress test, fix any issues found | System runs stable for 4 hours |

**Week 7 Deliverable:** `07_hardened_system/` — production-stable edge system.

---

#### Week 8 — Performance Profiling & Optimization
**Theme:** Measure everything, optimize what matters.

| Day | Focus (60-90 min) | Done When |
|-----|-------------------|-----------|
| 1 | Profile CPU/GPU/RAM usage during inference (use `jtop` for Jetson) | Resource usage graph over time |
| 2 | Identify bottlenecks: is it capture? inference? post-processing? | Bottleneck identified and documented |
| 3 | Optimize the bottleneck (batch processing, frame skipping, async I/O) | Measurable improvement in throughput |
| 4 | Test different model sizes (nano vs small vs medium) on Jetson | Size vs accuracy vs speed tradeoff table |
| 5 | Document all benchmarks in a performance report | `docs/performance_report.md` with tables and charts |
| 6-7 | Weekend: implement the best configuration, validate end-to-end | System running at optimal config |

**Week 8 Deliverable:** `08_performance/` — benchmark report with optimization results.

---

#### Week 9 — Temporal Intelligence & Multi-Modal
**Theme:** Go beyond single-frame detection — understand patterns over time.

| Day | Focus (60-90 min) | Done When |
|-----|-------------------|-----------|
| 1 | Implement proper object tracking (ByteTrack or similar) | Objects maintain IDs across frames |
| 2 | Add event detection: "object entered zone", "object left zone" | Zone-based events fire correctly |
| 3 | Add temporal rules: "zone occupied for > N minutes" → alert | Time-based alerts working |
| 4 | Build a simple event history/timeline from logged data | Can query: "what happened in the last hour?" |
| 5 | (Optional) Add anomaly detection: "unusual activity pattern" | System flags deviations from baseline |
| 6-7 | Weekend: integrate all intelligence into capstone pipeline | Smart detection pipeline running end-to-end |

**Week 9 Deliverable:** `09_temporal_intelligence/` — tracking, zone logic, temporal reasoning.

**PHASE 3 GATE:** Before moving on, verify:
- [ ] System runs stable for 4+ hours
- [ ] Performance is profiled and optimized
- [ ] Object tracking works across frames
- [ ] Temporal/zone-based logic fires correctly
- [ ] All benchmarks documented

---

### PHASE 4: CAPSTONE & PORTFOLIO (Weeks 10-12)
> Goal: Ship it. Make it portfolio-ready and presentable.

---

#### Week 10 — Capstone Build Sprint
**Theme:** Assemble everything into your final capstone project.

| Day | Focus (60-90 min) | Done When |
|-----|-------------------|-----------|
| 1 | Define capstone scope: exactly what it does, what it doesn't | `capstone/README.md` with clear scope |
| 2 | Assemble all components into capstone directory | Single unified codebase |
| 3 | Build a minimal dashboard: live status page (even just a terminal UI) | Can see system state at a glance |
| 4 | Add notification/action output (email, webhook, GPIO, or log file) | System produces a tangible output action |
| 5 | End-to-end test in real deployment scenario | System works in its intended environment |
| 6-7 | Weekend: fix bugs, polish, run extended test | Capstone runs reliably |

**Week 10 Deliverable:** `capstone/` — working end-to-end system.

---

#### Week 11 — Demo & Documentation
**Theme:** If you can't show it, it doesn't exist.

| Day | Focus (60-90 min) | Done When |
|-----|-------------------|-----------|
| 1 | Record demo video: 2-3 min walkthrough of system in action | Raw footage captured |
| 2 | Edit demo video (keep it tight, show the detection + decision + action) | Polished video under 3 minutes |
| 3 | Write technical write-up: problem, architecture, results | `docs/technical_writeup.md` first draft |
| 4 | Create architecture diagram (draw.io, Excalidraw, or Mermaid) | Clear system diagram |
| 5 | Review and polish write-up | Final draft ready |
| 6-7 | Weekend: polish GitHub repo (README, folder structure, setup instructions) | Repo is presentable to a hiring manager |

**Week 11 Deliverable:** Demo video + technical write-up + polished repo.

---

#### Week 12 — Polish, Reflect, Plan Next
**Theme:** Ship it and plan what's next.

| Day | Focus (60-90 min) | Done When |
|-----|-------------------|-----------|
| 1 | Final repo cleanup: remove dead code, check all READMEs | `git diff` is clean |
| 2 | Write a LinkedIn post or blog post about what you built | Draft written |
| 3 | Record a "lessons learned" reflection | `docs/lessons_learned.md` |
| 4 | Identify gaps: what would you do differently? What's next? | `docs/future_roadmap.md` |
| 5 | Share publicly: push repo, post video, publish write-up | Links are live |
| 6-7 | Weekend: celebrate. Plan Phase 2 (ROS2, multi-agent, or deeper ML) | You're done. |

**FINAL GATE — Portfolio Checklist:**
- [ ] GitHub repo with clean README and setup instructions
- [ ] Working demo video (< 3 minutes)
- [ ] Technical write-up explaining architecture + results
- [ ] Performance benchmarks (FPS, latency, accuracy)
- [ ] Architecture diagram
- [ ] System runs autonomously on Jetson for 1+ hour

---

## Capstone Options (Choose by End of Week 2)

### Option A: Smart Desk Monitor
- Detects: your presence, posture, phone usage
- Decides: are you focused? distracted? away?
- Acts: logs focus sessions, sends break reminders
- **Why:** Personally useful, easy to demo, you ARE the test data

### Option B: Room Occupancy & Activity Tracker
- Detects: people entering/leaving a room, count, dwell time
- Decides: room occupied? how many? unusual pattern?
- Acts: logs occupancy history, alerts on anomalies
- **Why:** Applicable to smart buildings, retail, security

### Option C: Package/Delivery Monitor
- Detects: packages appearing on doorstep/desk
- Decides: new package? removed? tampered?
- Acts: sends notification, logs delivery timeline
- **Why:** Practical home use, clear demo scenario

### Option D: Your Own Idea
- Write it up in the same format: Detects → Decides → Acts → Why

---

## What I Deliberately Excluded (And Why)

| Topic | Why Excluded | When to Learn It |
|-------|-------------|-----------------|
| **ROS2** | Massive ecosystem, easily 12 weeks on its own | Phase 2 (next 12-week block) |
| **Training from scratch** | Fine-tuning gets you 90% of the value in 10% of the time | After you have strong fundamentals |
| **Robot car / actuation** | Scope creep; perception → decision is the hard part | Phase 2, after ROS2 |
| **Cloud deployment** | Contradicts the edge-first philosophy | Add later if needed |
| **Reinforcement learning** | Different paradigm, not needed for perception systems | Separate curriculum |
| **LLM/VLM integration** | Tempting but a distraction from core edge skills | Phase 2 or 3 |

---

## Daily Routine Template

```
WEEKDAY (60-90 min):
├── 5 min  — Read today's task from this plan
├── 10 min — Review yesterday's code/notes
├── 40-60 min — Build (write code, run experiments)
├── 10 min — Commit, push, update progress log
└── 5 min  — Write tomorrow's micro-goal in progress log

WEEKEND (2-3 hrs):
├── 15 min — Review the week's progress
├── 90-120 min — Build (larger feature or integration work)
├── 15 min — Clean up code, write docs
└── 15 min — Update progress log, plan next week
```

---

## Progress Logs

Daily logs live in `logs/week-XX.md` (one file per week). This keeps the
master plan clean and the logs easy to update.

See `CLAUDE.md` for session-start context and project state.

---

## How to Use This Plan With Claude

Each day, tell me:
1. What you did today (or yesterday)
2. Any blockers or confusion
3. "What should I do today?"

I'll read your latest log, check progress against this plan, adjust if
needed, and give you a concrete task for today's session.
