import os
import sys

import cv2
import mss
import numpy as np
import pyautogui
import torch
from PIL import Image
from tqdm import tqdm
from transformers import AutoModel, AutoProcessor

CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "../../"))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)
ASSETS_DIR = os.path.join(ROOT_DIR, "assets")
OVEN_PATH = os.path.join(ASSETS_DIR, "oven.png")

# Load DINOv2 model
device = "cuda" if torch.cuda.is_available() else "cpu"
model = AutoModel.from_pretrained("facebook/dinov2-base").to(device).eval()
processor = AutoProcessor.from_pretrained("facebook/dinov2-base")

from utils.get_memu_resolution import get_memu_bounds
ADB_PATH = r"D:\Program Files\Microvirt\MEmu\adb.exe"


def grab_screen_region(x, y, width, height):
    with mss.mss() as sct:
        monitor = {"top": y, "left": x, "width": width, "height": height}
        return np.array(sct.grab(monitor))


def extract_feature(pil_img):
    inputs = processor(images=pil_img, return_tensors="pt").to(device)
    with torch.no_grad():
        features = model(**inputs).last_hidden_state.mean(dim=1)
    return features.squeeze()


# ... (keep all imports and constants as-is) ...

def adb_tap(x, y):
    cmd = f'"{ADB_PATH}" shell input tap {int(x)} {int(y)}'
    os.system(cmd)


def click_best_dino_match(template_path, threshold=0.5):
    # Load template
    template_img = Image.open(template_path).convert("RGB")
    tW, tH = template_img.size
    template_feature = extract_feature(template_img)

    # Get emulator bounds and screenshot
    left, top, width, height = get_memu_bounds()
    screen_np = grab_screen_region(left, top, width, height)
    screen_rgb = cv2.cvtColor(screen_np, cv2.COLOR_BGRA2RGB)

    # Focus on vertical brown belt region
    belt_left = int(width * 0.0)
    belt_right = int(width * 0.8)
    belt_top = int(height * 0.25)
    belt_bottom = int(height * 0.8)
    belt_crop = screen_rgb[belt_top:belt_bottom, belt_left:belt_right]

    screen_h, screen_w = belt_crop.shape[:2]
    stride = int(max(tW, tH) * 0.75)

    regions = []
    coords = []

    print("🔍 Scanning regions for DINOv2 match...")

    for y in tqdm(range(0, screen_h - tH, stride), desc="Rows", leave=False):
        for x in range(0, screen_w - tW, stride):
            crop = belt_crop[y : y + tH, x : x + tW]
            regions.append(Image.fromarray(crop))
            coords.append((belt_left + x + tW // 2, belt_top + y + tH // 2))

    # Batch inference
    print(f"🧠 Running DINOv2 batch inference on {len(regions)} regions...")
    inputs = processor(images=regions, return_tensors="pt").to(device)
    with torch.inference_mode():
        features = model(**inputs).last_hidden_state.mean(dim=1)  # (B, D)

    # Compute similarity
    template_feature = template_feature.unsqueeze(0)  # (1, D)
    sims = torch.nn.functional.cosine_similarity(template_feature, features, dim=1)

    best_score, best_idx = torch.max(sims, dim=0)
    best_score = best_score.item()

    if best_score >= threshold:
        match_x, match_y = coords[best_idx]
        abs_x = left + match_x
        abs_y = top + match_y
        adb_tap(abs_x, abs_y)
        print(
            f"✅ Tapped DINOv2 match at ({abs_x}, {abs_y}) with confidence {best_score:.3f}"
        )
        return True
    else:
        print(f"❌ No match found. Best confidence: {best_score:.3f}")
        return False


def click_jar():
    template_path = (
        r"C:\Users\ceo\IdeaProjects\pastaria_bot\debug\debug_pasta_cropped.png"
    )
    click_best_dino_match(template_path)


def main():
    click_jar()


if __name__ == "__main__":
    main()
