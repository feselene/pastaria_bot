import numpy as np
import mss
import os
import cv2
import sys

CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = CURRENT_DIR
DEBUG_DIR = os.path.join(ROOT_DIR, "debug")
TOPPINGS_DIR = os.path.join(ROOT_DIR, "toppings")
MATCHES_DIR = os.path.join(ROOT_DIR, "matches")
os.makedirs(MATCHES_DIR, exist_ok=True)  # Ensure the directory exists

if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from utils.gemini_matcher import is_matching, recenter
from utils.get_memu_resolution import get_memu_bounds, get_memu_resolution

ADB_PATH = r"D:\Program Files\Microvirt\MEmu\adb.exe"  # Update if needed

def capture_center_picker_square():
    x_ratio = 0.415
    y_ratio = 0.32
    square_size = 180
    half = square_size / 2
    left, top, width, height = get_memu_bounds()
    center_x = int(left + width * x_ratio)
    center_y = int(top + height * y_ratio)

    region = {
        "left": int(center_x - half),
        "top": int(center_y - half),
        "width": square_size,
        "height": square_size,
    }

    with mss.mss() as sct:
        img = np.array(sct.grab(region))

    output_path = os.path.join(DEBUG_DIR, f"topping_active1.png")
    print(output_path)
    cv2.imwrite(output_path, img)
    return output_path

if __name__ == "__main__":
    capture_center_picker_square()
