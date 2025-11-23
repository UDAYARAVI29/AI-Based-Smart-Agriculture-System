import os
import shutil
import json
from pathlib import Path
from PIL import Image
from sklearn.model_selection import train_test_split

BASE = Path(__file__).resolve().parents[2]
RAW = BASE / "data" / "training" / "disease" / "raw"
PROC = BASE / "data" / "processed" / "disease"

IMG_SIZE = (224, 224)

def prepare_dirs():
    for split in ["train", "val", "test"]:
        (PROC / split).mkdir(parents=True, exist_ok=True)

def process_images():
    classes = [c.name for c in RAW.iterdir() if c.is_dir()]
    class_map = {name: idx for idx, name in enumerate(classes)}

    all_images = []
    for cls in classes:
        for img_path in (RAW / cls).glob("*"):
            if img_path.suffix.lower() in [".jpg", ".png", ".jpeg"]:
                all_images.append((img_path, cls))

    train_imgs, test_imgs = train_test_split(all_images, test_size=0.15, random_state=42)
    train_imgs, val_imgs = train_test_split(train_imgs, test_size=0.176, random_state=42)  # yields ~70/15/15

    splits = {"train": train_imgs, "val": val_imgs, "test": test_imgs}

    for split, images in splits.items():
        split_dir = PROC / split
        for img, cls in images:
            cls_dir = split_dir / cls
            cls_dir.mkdir(exist_ok=True)
            try:
                im = Image.open(img).convert("RGB")
                im = im.resize(IMG_SIZE)
                im.save(cls_dir / img.name)
            except Exception:
                print(f"Corrupted image skipped: {img}")

    json.dump(class_map, open(PROC / "labels.json", "w"), indent=4)

    json.dump({
        "total_images": len(all_images),
        "train": len(train_imgs),
        "val": len(val_imgs),
        "test": len(test_imgs),
        "classes": class_map
    }, open(PROC / "dataset_info.json", "w"), indent=4)

if __name__ == "__main__":
    prepare_dirs()
    process_images()
    print("Disease dataset processed successfully!")
