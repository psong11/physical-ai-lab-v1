"""
Week 2 — Prepare classification dataset.

Takes images from data/raw/<class>/ and splits them into
data/dataset/train/<class>/ and data/dataset/val/<class>/
with an 80/20 split.

Ultralytics YOLO classify expects this folder structure:
  dataset/
  ├── train/
  │   ├── focused/
  │   ├── phone/
  │   └── away/
  └── val/
      ├── focused/
      ├── phone/
      └── away/
"""

import os
import random
import shutil

# --- Config ---
RAW_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "raw"))
DATASET_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "dataset"))
VAL_SPLIT = 0.2
SEED = 42

CLASSES = ["focused", "phone", "away"]


def main():
    random.seed(SEED)

    # Clean previous dataset if it exists
    if os.path.exists(DATASET_DIR):
        shutil.rmtree(DATASET_DIR)

    # Create directories
    for split in ["train", "val"]:
        for cls in CLASSES:
            os.makedirs(os.path.join(DATASET_DIR, split, cls), exist_ok=True)

    total_train = 0
    total_val = 0

    for cls in CLASSES:
        raw_path = os.path.join(RAW_DIR, cls)
        if not os.path.exists(raw_path):
            print(f"WARNING: {raw_path} not found, skipping")
            continue

        images = [f for f in os.listdir(raw_path) if f.lower().endswith((".jpg", ".jpeg", ".png"))]
        random.shuffle(images)

        val_count = max(1, int(len(images) * VAL_SPLIT))
        val_images = images[:val_count]
        train_images = images[val_count:]

        for img in train_images:
            shutil.copy2(os.path.join(raw_path, img), os.path.join(DATASET_DIR, "train", cls, img))
        for img in val_images:
            shutil.copy2(os.path.join(raw_path, img), os.path.join(DATASET_DIR, "val", cls, img))

        print(f"  {cls}: {len(train_images)} train, {len(val_images)} val")
        total_train += len(train_images)
        total_val += len(val_images)

    print(f"\nTotal: {total_train} train, {total_val} val")
    print(f"Dataset ready at: {DATASET_DIR}")


if __name__ == "__main__":
    main()
