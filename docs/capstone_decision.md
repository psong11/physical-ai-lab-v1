# Capstone Decision: Smart Desk Monitor

**Decided:** Week 2, Day 1
**Option chosen:** A — Smart Desk Monitor

---

## What It Does

A real-time edge AI system that monitors your desk workspace and tracks your focus patterns.

### Detects
- **Presence:** Are you at the desk? (already built in Week 1)
- **Phone usage:** Is a phone visible in your hand / on desk being used?
- **Posture cues:** Leaning in (engaged) vs leaning back (disengaged) — stretch goal

### Decides
- **State classification:** Focused / Distracted / Away
- **Session quality:** How much of a session was focused vs distracted?
- **Patterns:** When are your best focus hours? How often do you check your phone?

### Acts
- Logs focus sessions with quality scores to a database
- Dashboard showing daily/weekly focus trends
- Break reminders after long focused stretches (configurable)
- Daily summary report

---

## Why This Capstone

1. **You are the test data** — no need to recruit people or stage scenarios
2. **Builds on Week 1** — desk_tracker.py is already the foundation
3. **Personally useful** — you'll actually use this while working on this project
4. **Demos well** — clear before/after, easy to explain in 2 minutes
5. **Full pipeline** — covers perception (YOLO), reasoning (state machine), action (alerts + dashboard)

---

## What Needs to Be Fine-Tuned (Week 2)

To go beyond generic YOLO, we need a model that reliably detects:
- `phone_in_hand` — person holding/looking at phone
- `person` — already works with pretrained YOLO

Stretch classes (if time allows):
- `typing` — hands on keyboard (engaged signal)
- `leaning_back` — posture cue (disengaged signal)

---

## Data Collection Plan

- Capture images from the desk webcam in various states (focused, phone, away)
- Aim for 150-200 labeled images for the primary classes
- Use Roboflow for labeling (YOLO format export)
