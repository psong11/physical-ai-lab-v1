# Physical AI Lab v1

## Project Summary
12-week hands-on curriculum to build a real-time Physical AI system on edge
hardware (NVIDIA Jetson Orin Nano). Owner: Paul Song. Started: 2026-02-22.

## Quick Context for Each Session
1. Read `MASTER_PLAN.md` for the full 12-week roadmap and weekly/daily breakdown
2. Read the latest file in `logs/` to see where Paul left off
3. Check which week/day he's on and what the next task is
4. Give him a concrete, actionable task for today's session (60-90 min weekday, 2-3 hrs weekend)

## Current Phase
- **Week:** 1
- **Phase:** 1 — Perception Foundations (Weeks 1-3)
- **Focus:** Get real-time YOLO detection running on laptop with decision logic

## Hardware Available
- MacBook (primary dev machine for Phase 1)
- NVIDIA Jetson Orin Nano (arriving 2026-02-23, primary for Phase 2+)
- Raspberry Pi 5 (currently running insidemyroom weather station — leave it alone)
- Arduino Uno + DHT11 + HC-05 Bluetooth (currently used by insidemyroom — leave it)
- USB/CSI camera (comes with Jetson kit or ordered separately — confirm with Paul)

## Project Structure
```
physical-ai-lab-v1/
├── CLAUDE.md              # THIS FILE — session context for Claude
├── MASTER_PLAN.md         # Full 12-week roadmap with daily tasks and phase gates
├── logs/                  # Daily progress logs (one file per week)
│   └── week-01.md         # Current week's log
├── docs/                  # Architecture docs, write-ups, notes
├── src/                   # All source code (organized by week/phase)
└── data/                  # Datasets, images, labels (added later)
```

## Key Decisions Made
- Capstone: TBD (choose by end of Week 2)
- ROS2: excluded from 12-week scope (future Phase 2)
- Training approach: fine-tuning only, no training from scratch
- Insidemyroom project: keep running, don't unplug Pi/Arduino

## Paul's Background (Relevant Context)
- PM role (full-time job, this is a side project)
- Already built: Arduino → Bluetooth → Raspberry Pi → Google Drive → Next.js
  dashboard (insidemyroom project). Understands serial data, IoT pipelines,
  web dashboards, Docker basics.
- Python proficiency: intermediate (can write scripts, use libraries)
- ML proficiency: beginner (understands concepts, limited hands-on)

## How to Guide Paul
- Be concrete: "write this function" > "consider implementing"
- Be honest about scope: flag if something will take longer than expected
- Reference MASTER_PLAN.md for the schedule, logs/ for recent progress
- If he's behind schedule, help him prioritize what to skip vs what matters
- If he's ahead, suggest stretch goals from the plan
