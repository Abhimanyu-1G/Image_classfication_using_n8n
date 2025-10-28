import os
import requests
import random

# 🔑 Put your Pexels API key here
PEXELS_API_KEY = "BNCdn5loMVXP6JPOEeEjzGMuxlKasM66OCLGSh1dxvhRDjptLqVZ3kFf"

# Folder to save images
save_dir = r"D:\n8n_data\images"
os.makedirs(save_dir, exist_ok=True)

# Categories to fetch
categories = ["cat", "dog", "car", "bird", "flower"]

headers = {
    "Authorization": PEXELS_API_KEY
}

print("🔽 Downloading real images from Pexels...")

for category in categories:
    # Random page to vary results
    page = random.randint(1, 10)
    url = f"https://api.pexels.com/v1/search?query={category}&per_page=2&page={page}"

    try:
        r = requests.get(url, headers=headers, timeout=20)
        if r.status_code == 200:
            data = r.json()
            for i, photo in enumerate(data.get("photos", []), start=1):
                img_url = photo["src"]["medium"]
                file_path = os.path.join(save_dir, f"{category}_{page}_{i}.jpg")

                img = requests.get(img_url, timeout=15)
                if img.status_code == 200:
                    with open(file_path, "wb") as f:
                        f.write(img.content)
                    print(f"✅ Saved {file_path}")
                else:
                    print(f"⚠️ Failed to fetch {category} image (HTTP {img.status_code})")
        else:
            print(f"⚠️ API error for {category}: HTTP {r.status_code}")
    except Exception as e:
        print(f"❌ Error for {category}: {e}")

print("\n✅ Done! Images saved in:", save_dir)
