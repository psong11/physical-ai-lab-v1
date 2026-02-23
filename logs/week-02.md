# Week 2 — Custom Data & Fine-Tuning

**Theme:** Move from generic detection to YOUR specific use case.
**Dates:** 2026-03-01 to 2026-03-07

---

## Day 1 — Sunday, Mar 1
**Goal:** Choose capstone, start data collection

### What I Did
- Chose capstone: **Smart Desk Monitor** (Option A)
  - Detects: presence, focus state, phone usage (via posture, not phone object)
  - Decides: focused / distracted / away
  - Acts: logs sessions, break reminders, daily summary
- Key pivot: switched from **object detection to image classification**
  - Phone isn't visible on camera (held below frame), so detecting the phone object doesn't work
  - Instead, classify the whole frame based on body posture/position
  - Classes: `focused`, `phone`, `away`
- Built `src/02_custom_model/capture_data.py` — webcam capture tool (f/d/a keys to save to class folders)
- Captured 67 images (34 focused, 16 phone, 17 away) — all nighttime lighting
- Built `src/02_custom_model/prepare_dataset.py` — 80/20 train/val splitter
- Built `src/02_custom_model/train_classifier.py` — fine-tunes YOLOv8n-cls (pretrained on ImageNet)
- Trained first model: 100% val accuracy — promising but likely overfitting on small dataset
- Learned: train/val splits, pretrained models, confusion matrices, loss curves
- Skipped Roboflow labeling — folder structure IS the labels for classification

### What's Next (Day 2)
- Test the classifier live on webcam (build real-time inference script)
- Collect more images in daylight for better generalization

### Blockers/Notes
- 67 images is a small dataset — model will need more data to be robust
- Daylight images will help with lighting variation
- Roboflow was used briefly but not needed — auto-labeler produced segmentation polygons, not useful for classification
