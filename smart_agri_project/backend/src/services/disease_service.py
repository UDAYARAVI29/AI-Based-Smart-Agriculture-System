import torch
import torch.nn as nn
from torchvision import transforms, models
from PIL import Image
import json
import os

# ---------------------------------------------------------
# PATH SETUP
# ---------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "data", "models", "disease_resnet18.pth")
LABELS_PATH = os.path.join(BASE_DIR, "data", "models", "disease_labels.json")

# ---------------------------------------------------------
# DEVICE CONFIGURATION
# ---------------------------------------------------------
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# ---------------------------------------------------------
# LOAD LABELS CORRECTLY
# ---------------------------------------------------------
with open(LABELS_PATH, "r") as f:
    LABELS = json.load(f)["classes"]   # FIXED: extract the list only

# convert to index→label map
IDX_TO_LABEL = {i: label for i, label in enumerate(LABELS)}

# ---------------------------------------------------------
# IMAGE TRANSFORMS
# ---------------------------------------------------------
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

# ---------------------------------------------------------
# MODEL LOADING FUNCTION
# ---------------------------------------------------------
def load_disease_model():
    model = models.resnet18(weights=None)
    model.fc = nn.Linear(512, len(LABELS))   # must be 29, now fixed

    checkpoint = torch.load(MODEL_PATH, map_location=device)

    # Handle both save formats
    if isinstance(checkpoint, dict) and "model_state" in checkpoint:
        state_dict = checkpoint["model_state"]
    else:
        state_dict = checkpoint

    model.load_state_dict(state_dict)
    model.to(device)
    model.eval()
    return model

model = load_disease_model()

# ---------------------------------------------------------
# PREDICTION FUNCTION
# ---------------------------------------------------------
def predict_disease(image_path: str):
    try:
        img = Image.open(image_path).convert("RGB")
    except Exception as e:
        raise ValueError(f"Invalid image file: {str(e)}")

    img_tensor = transform(img).unsqueeze(0).to(device)

    with torch.no_grad():
        outputs = model(img_tensor)
        probabilities = torch.softmax(outputs, dim=1)
        confidence, predicted_idx = torch.max(probabilities, 1)

    predicted_label = IDX_TO_LABEL[predicted_idx.item()]

    return {
        "predicted_class": predicted_label,
        "confidence": float(confidence.item())
    }
