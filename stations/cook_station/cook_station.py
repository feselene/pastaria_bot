import os
import sys
import cv2
import numpy as np
from time import sleep

# Setup root imports
CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "../../"))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from stations.cook_station.click_leftmost_cook_button import click_leftmost_plus_button
from utils.detect_ticket_from_template import detect_ticket_from_template
from utils.get_memu_position import get_memu_bounds
from utils.remove_background import remove_background_and_crop  # ✅ <-- Importing background remover

import mss
from PIL import Image

def crop_ticket_regions(ticket_img):
    h, w = ticket_img.shape[:2]
    return {
        "order":     ticket_img[int(0.0000*h):int(0.1094*h), :],
        "bread":     ticket_img[int(0.1094*h):int(0.2575*h), :],
        "topping1":  ticket_img[int(0.2575*h):int(0.3687*h), :],
        "topping2":  ticket_img[int(0.3687*h):int(0.4746*h), :],
        "topping3":  ticket_img[int(0.4746*h):int(0.5804*h), :],
        "topping4":  ticket_img[int(0.5804*h):int(0.6862*h), :],
        "sauce":     ticket_img[int(0.6862*h):int(0.7921*h), :],
        "pasta":     ticket_img[int(0.7921*h):int(0.9273*h), :],
        "doneness":  ticket_img[int(0.9273*h):int(1.0000*h), :]
    }

def capture_full_screen():
    with mss.mss() as sct:
        monitor = sct.monitors[1]  # Adjust if needed
        screenshot = np.array(sct.grab(monitor))
        return screenshot, monitor["left"], monitor["top"]

def run_cook_station():
    print("🍳 Opening pot...")
    click_leftmost_plus_button()
    sleep(0.3)

    print("🎟️ Detecting ticket...")
    ticket_img = detect_ticket_from_template()
    if ticket_img is None:
        print("❌ Ticket detection failed.")
        return

    cv2.imwrite("debug_ticket.png", ticket_img)

    print("✂️ Cropping ticket regions...")
    regions = crop_ticket_regions(ticket_img)

    for name, region_img in regions.items():
        print(f"📦 Region: {name}, shape: {region_img.shape}")
        cv2.imwrite(f"debug_{name}.png", region_img)

    pasta_img_bgr = regions["pasta"]
    pasta_img_path = os.path.join(ROOT_DIR, "debug", "debug_pasta_raw.png")
    pasta_out_path = os.path.join(ROOT_DIR, "debug", "debug_pasta_cropped.png")

    os.makedirs(os.path.dirname(pasta_img_path), exist_ok=True)
    cv2.imwrite(pasta_img_path, pasta_img_bgr)

    # ✅ Remove background and crop
    print("🔍 Removing background from pasta icon...")
    remove_background_and_crop(pasta_img_path, pasta_out_path)
    print(f"✅ Pasta icon saved to: {pasta_out_path}")

if __name__ == "__main__":
    run_cook_station()
