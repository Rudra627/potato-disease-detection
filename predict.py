import os
import torch
import torch.nn as nn
import torchvision.transforms as transforms
from PIL import Image

classes = [
    "Potato___Early_Blight",
    "Potato___Healthy",
    "Potato___Late_Blight"
]

# ─── Model path & auto-download ────────────────────────────────
MODEL_PATH = os.path.join(os.path.dirname(__file__), "potato_disease_model.pth")

# Google Drive file ID for the model weights
# Replace <YOUR_FILE_ID> with the actual ID from a shareable Google Drive link
# Example link: https://drive.google.com/file/d/XXXXX/view  →  ID = XXXXX
GDRIVE_FILE_ID = os.environ.get("MODEL_GDRIVE_ID", "<YOUR_FILE_ID>")

def _download_model():
    """Download model weights from Google Drive if not present locally."""
    if os.path.exists(MODEL_PATH):
        return
    print("⏬ Model weights not found locally. Downloading from Google Drive...")
    try:
        import gdown
        url = f"https://drive.google.com/uc?id={GDRIVE_FILE_ID}"
        gdown.download(url, MODEL_PATH, quiet=False)
        print("✅ Model downloaded successfully!")
    except Exception as e:
        raise RuntimeError(
            f"Failed to download model weights.\n"
            f"Please either:\n"
            f"  1. Place 'potato_disease_model.pth' in the project root, or\n"
            f"  2. Set the MODEL_GDRIVE_ID environment variable to a valid Google Drive file ID.\n"
            f"Error: {e}"
        )

_download_model()

# Custom CNN matching the architecture used during training
class PotatoDiseaseModel(nn.Module):
    def __init__(self):
        super(PotatoDiseaseModel, self).__init__()
        self.conv_layer = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, padding=1),   # index 0
            nn.ReLU(),                                     # index 1
            nn.MaxPool2d(2, 2),                            # index 2
            nn.Conv2d(32, 64, kernel_size=3, padding=1),   # index 3
            nn.ReLU(),                                     # index 4
            nn.MaxPool2d(2, 2),                            # index 5
            nn.Conv2d(64, 128, kernel_size=3, padding=1),  # index 6
            nn.ReLU(),                                     # index 7
            nn.MaxPool2d(2, 2),                            # index 8
        )
        self.fc_layer = nn.Sequential(
            nn.Linear(128 * 28 * 28, 512),                 # index 0 (100352 -> 512)
            nn.ReLU(),                                     # index 1
            nn.Linear(512, 3),                             # index 2
        )

    def forward(self, x):
        x = self.conv_layer(x)
        x = x.view(x.size(0), -1)
        x = self.fc_layer(x)
        return x

model = PotatoDiseaseModel()
model.load_state_dict(torch.load(MODEL_PATH, map_location="cpu"))
model.eval()

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])

def predict(image):
    image = transform(image).unsqueeze(0)

    with torch.no_grad():
        output = model(image)
        _, pred = torch.max(output, 1)

    return classes[pred.item()]