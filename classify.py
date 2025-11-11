import argparse, json
from pathlib import Path
import torch
from torchvision import models
from PIL import Image

# ----- ConvNeXt Base (good accuracy, fits 3050) -----
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
        x = preprocess(img).unsqueeze(0).to(device)
        with torch.no_grad():
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
        return {"image_path": image_path, "error": str(e)}

if __name__ == "__main__":
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

    # one dict if single image; else a list of top-1 dicts
    print(json.dumps(outputs[0] if len(outputs) == 1 else outputs, ensure_ascii=False, indent=2))
