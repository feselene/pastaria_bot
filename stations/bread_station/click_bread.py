import os
import sys

import cv2


CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "../../"))
DEBUG_DIR = os.path.join(ROOT_DIR, "debug")
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from utils.click_button import grab_screen_region
from utils.crop_screenshot_by_ratio import adb_drag_relative

def get_bread_ratio(threshold=0.75):
    template_path = os.path.join(DEBUG_DIR, "bread_icon.png")
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
    if template is None:
        raise FileNotFoundError(f"Missing template image: {template_path}")
    tH, tW = template.shape[:2]

    # Capture screen and prepare search space
    screenshot = grab_screen_region()
    gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    height, width = gray.shape[:2]

    # Define ratio-based crop region
    xratio1, yratio1 = 0.3, 0.0
    xratio2, yratio2 = 0.6, 1.0

    x1 = int(width * xratio1)
    y1 = int(height * yratio1)
    x2 = int(width * xratio2)
    y2 = int(height * yratio2)

    cropped = gray[y1:y2, x1:x2]

    # Matching loop
    best_val = -1
    best_loc = None
    best_scale = None
    best_template = None

    for scale in [1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0]:
        resized_template = cv2.resize(template, (int(tW * scale), int(tH * scale)))
        rH, rW = resized_template.shape[:2]

        if cropped.shape[0] < rH or cropped.shape[1] < rW:
            continue

        result = cv2.matchTemplate(cropped, resized_template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)

        if max_val > best_val:
            best_val = max_val
            best_loc = max_loc
            best_scale = scale
            best_template = resized_template

    if best_val >= threshold:
        match_x, match_y = best_loc
        match_h, match_w = best_template.shape[:2]

        # Final center coordinates in full screenshot
        center_x = x1 + match_x + match_w // 2
        center_y = y1 + match_y + match_h // 2

        # Convert to relative ratios
        x_ratio = center_x / width
        y_ratio = center_y / height
        return x_ratio, y_ratio
    else:
        print(f"❌ No match found. Highest confidence: {best_val:.3f}")
        return None, None


def click_bread():
    x, y = get_bread_ratio()
    adb_drag_relative(x, y, 0.152, 0.44)


def main():
    print(True)


if __name__ == "__main__":
    click_bread()
