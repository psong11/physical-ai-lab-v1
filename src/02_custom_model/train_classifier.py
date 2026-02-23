"""
Week 2 — Fine-tune YOLOv8n-cls on desk state classification.

Classes: focused, phone, away
Uses the dataset prepared by prepare_dataset.py.

Usage:
  python src/02_custom_model/train_classifier.py
"""

import os

from ultralytics import YOLO

# --- Config ---
PROJECT_ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))
DATASET_DIR = os.path.join(PROJECT_ROOT, "data", "dataset")
RUNS_DIR = os.path.join(PROJECT_ROOT, "runs")
EPOCHS = 50
IMAGE_SIZE = 224
BATCH_SIZE = 16
MODEL = "yolov8n-cls.pt"  # pretrained classification model (ImageNet)


def main():
    if not os.path.exists(DATASET_DIR):
        print(f"ERROR: Dataset not found at {DATASET_DIR}")
        print("Run prepare_dataset.py first.")
        return

    # Count images
    for split in ["train", "val"]:
        split_path = os.path.join(DATASET_DIR, split)
        for cls in sorted(os.listdir(split_path)):
            cls_path = os.path.join(split_path, cls)
            if os.path.isdir(cls_path):
                count = len(os.listdir(cls_path))
                print(f"  {split}/{cls}: {count}")

    print(f"\nStarting fine-tuning: {MODEL}")
    print(f"  Epochs: {EPOCHS}")
    print(f"  Image size: {IMAGE_SIZE}")
    print(f"  Batch size: {BATCH_SIZE}")
    print()

    model = YOLO(MODEL)

    results = model.train(
        data=DATASET_DIR,
        epochs=EPOCHS,
        imgsz=IMAGE_SIZE,
        batch=BATCH_SIZE,
        project=RUNS_DIR,
        name="desk_state",
        exist_ok=True,
        pretrained=True,
    )

    print("\nTraining complete!")
    print(f"Best model saved to: {RUNS_DIR}/desk_state/weights/best.pt")


if __name__ == "__main__":
    main()
