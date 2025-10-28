import torch
from torchvision import models, transforms
from PIL import Image
import json

# --- Preload model once ---
model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
model.eval()
labels = models.ResNet18_Weights.DEFAULT.meta["categories"]

transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    ),
])

def classify_image(image_path):
    """Return a dictionary with predicted class"""
    try:
        img = Image.open(image_path).convert("RGB")
        input_tensor = transform(img).unsqueeze(0)
        with torch.no_grad():
            output = model(input_tensor)
            _, predicted = torch.max(output, 1)
            predicted_idx = predicted.item()
            label = labels[predicted_idx]
        return {"image_path": image_path, "predicted_class": label}
    except Exception as e:
        return {"error": str(e)}

# Optional: keep standalone execution
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No image path provided"}))
    else:
        print(json.dumps(classify_image(sys.argv[1])))
