import os
import sys

import cv2
import mss
import numpy as np
import pyautogui
import torch
from PIL import Image
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

from utils.get_memu_position import get_memu_bounds


def grab_screen_region(x, y, width, height):
    with mss.mss() as sct:
        monitor = {"top": y, "left": x, "width": width, "height": height}
        return np.array(sct.grab(monitor))


def extract_feature(pil_img):
    inputs = processor(images=pil_img, return_tensors="pt").to(device)
    with torch.no_grad():
        features = model(**inputs).last_hidden_state.mean(dim=1)
    return features.squeeze()


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

    best_score = -1
    best_coords = None

    for y in range(0, screen_h - tH, stride):
        for x in range(0, screen_w - tW, stride):
            region = belt_crop[y : y + tH, x : x + tW]
            region_pil = Image.fromarray(region)
            region_feature = extract_feature(region_pil)

            sim = torch.nn.functional.cosine_similarity(
                template_feature, region_feature, dim=0
            ).item()

            if sim > best_score:
                best_score = sim
                best_coords = (belt_left + x + tW // 2, belt_top + y + tH // 2)

    if best_score >= threshold and best_coords:
        abs_x, abs_y = left + best_coords[0], top + best_coords[1]
        pyautogui.moveTo(abs_x, abs_y, duration=0.2)
        pyautogui.click()
        print(
            f"✅ Clicked DINOv2 match at ({abs_x}, {abs_y}) with confidence {best_score:.3f}"
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
