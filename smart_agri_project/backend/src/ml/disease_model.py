# disease_model.py
# PyTorch-based training, evaluation and inference utilities using a pretrained ResNet18.
import os
import torch
import torch.nn as nn
from torchvision import models, transforms, datasets
from torch.utils.data import DataLoader
from pathlib import Path
import json

MODEL_DIR = Path(__file__).resolve().parents[2] / "data" / "models"
MODEL_DIR.mkdir(parents=True, exist_ok=True)
MODEL_PATH = MODEL_DIR / "disease_resnet18.pth"
LABELS_PATH = MODEL_DIR / "disease_labels.json"

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def get_transforms(train=True, img_size=224):
    if train:
        return transforms.Compose([
            transforms.RandomResizedCrop(img_size),
            transforms.RandomHorizontalFlip(),
            transforms.RandomRotation(15),
            transforms.ToTensor(),
            transforms.Normalize([0.485,0.456,0.406],[0.229,0.224,0.225])
        ])
    else:
        return transforms.Compose([
            transforms.Resize((img_size, img_size)),
            transforms.ToTensor(),
            transforms.Normalize([0.485,0.456,0.406],[0.229,0.224,0.225])
        ])

def build_model(num_classes):
    model = models.resnet18(pretrained=True)
    # Replace final layer
    in_features = model.fc.in_features
    model.fc = nn.Linear(in_features, num_classes)
    return model.to(device)

def train_model(data_dir, epochs=5, batch_size=32, lr=1e-4, num_workers=4):
    """
    data_dir should point to processed disease folder with train/val subfolders:
      backend/data/processed/disease/train
      backend/data/processed/disease/val
    """
    data_dir = Path(data_dir)
    train_dir = data_dir / "train"
    val_dir = data_dir / "val"

    train_ds = datasets.ImageFolder(train_dir, transform=get_transforms(train=True))
    val_ds = datasets.ImageFolder(val_dir, transform=get_transforms(train=False))

    num_classes = len(train_ds.classes)
    print("Detected classes:", num_classes)

    train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True, num_workers=num_workers)
    val_loader = DataLoader(val_ds, batch_size=batch_size, shuffle=False, num_workers=num_workers)

    model = build_model(num_classes)
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)

    best_val_acc = 0.0
    for epoch in range(1, epochs + 1):
        model.train()
        running_loss = 0.0
        correct = 0
        total = 0
        for imgs, labels in train_loader:
            imgs, labels = imgs.to(device), labels.to(device)
            optimizer.zero_grad()
            outputs = model(imgs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss += float(loss.item()) * imgs.size(0)
            _, preds = torch.max(outputs, 1)
            correct += (preds == labels).sum().item()
            total += labels.size(0)

        train_loss = running_loss / total
        train_acc = correct / total

        # Validation
        model.eval()
        val_correct = 0
        val_total = 0
        with torch.no_grad():
            for imgs, labels in val_loader:
                imgs, labels = imgs.to(device), labels.to(device)
                outputs = model(imgs)
                _, preds = torch.max(outputs, 1)
                val_correct += (preds == labels).sum().item()
                val_total += labels.size(0)
        val_acc = val_correct / val_total

        print(f"Epoch {epoch}/{epochs} - train_loss: {train_loss:.4f}, train_acc: {train_acc:.4f}, val_acc: {val_acc:.4f}")

        # Save best
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            torch.save({
                "model_state": model.state_dict(),
                "classes": train_ds.classes
            }, MODEL_PATH)
            # also save labels
            json.dump({"classes": train_ds.classes}, open(LABELS_PATH, "w"), indent=2)
            print("Saved best model.")

    print("Training finished. Best val acc:", best_val_acc)
    return MODEL_PATH

def load_model(path=None):
    if path is None:
        path = MODEL_PATH
    checkpoint = torch.load(path, map_location=device)
    classes = checkpoint.get("classes")
    model = build_model(len(classes))
    model.load_state_dict(checkpoint["model_state"])
    model.eval()
    return model, classes

def predict_from_image_bytes(image_bytes, model=None, classes=None, img_size=224):
    from PIL import Image
    t = get_transforms(train=False, img_size=img_size)
    im = Image.open(image_bytes).convert("RGB")
    x = t(im).unsqueeze(0).to(device)
    if model is None:
        model, classes = load_model()
    with torch.no_grad():
        out = model(x)
        probs = torch.nn.functional.softmax(out, dim=1)[0].cpu().numpy()
        idx = int(probs.argmax())
        return {"label": classes[idx], "confidence": float(probs[idx])}