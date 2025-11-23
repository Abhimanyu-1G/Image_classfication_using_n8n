import argparse, json
from pathlib import Path
import torch
from torchvision import models, transforms
from torchvision import models
from PIL import Image
import json

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

Weights = models.ConvNeXt_Base_Weights
weights = Weights.DEFAULT
model = models.convnext_base(weights=weights).eval()

categories = weights.meta["categories"]
preprocess = weights.transforms()

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
torch.backends.cudnn.benchmark = True

def classify_top1(image_path: str):
try:
img = Image.open(image_path).convert("RGB")
        input_tensor = transform(img).unsqueeze(0)
        x = preprocess(img).unsqueeze(0).to(device)
with torch.no_grad():
            output = model(input_tensor)
            _, predicted = torch.max(output, 1)
            predicted_idx = predicted.item()
            label = labels[predicted_idx]
        return {"image_path": image_path, "predicted_class": label}
            with torch.autocast(device_type=device.type, enabled=(device.type == "cuda")):
                logits = model(x)
                probs = torch.softmax(logits, dim=1)
                conf, idx = probs.max(dim=1)
        return {
            "image_path": image_path,
            "predicted_class": categories[idx.item()],
            "confidence": float(conf.item())
        }
except Exception as e:
        return {"error": str(e)}
        return {"image_path": image_path, "error": str(e)}

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No image path provided"}))
    else:
        print(json.dumps(classify_image(sys.argv[1])))
    parser = argparse.ArgumentParser(description="ConvNeXt Base Top-1 Classifier")
    parser.add_argument("images", nargs="+", help="Path(s) to image file(s)")
    parser.add_argument("--cpu", action="store_true", help="Force CPU")
    args = parser.parse_args()

    if args.cpu: 
        global device
        device = torch.device("cpu")
        model.to(device)

    outputs = []
    for p in args.images:
        if not Path(p).exists():
            outputs.append({"image_path": p, "error": "File not found"})
        else:
            outputs.append(classify_top1(p))

    print(json.dumps(outputs[0] if len(outputs) == 1 else outputs, ensure_ascii=False, indent=2))

