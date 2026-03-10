import torch
import torch.nn as nn
import torchvision.transforms as transforms
from PIL import Image

classes = [
    "Potato___Early_Blight",
    "Potato___Healthy",
    "Potato___Late_Blight"
]

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
model.load_state_dict(torch.load("potato_disease_model.pth", map_location="cpu"))
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