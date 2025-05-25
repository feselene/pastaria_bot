import os
import subprocess
import sys

import cv2
from dotenv import load_dotenv

CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "../../"))
ASSETS_DIR = os.path.join(ROOT_DIR, "assets")
DEBUG_DIR = os.path.join(ROOT_DIR, "debug")
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from utils.click_button import grab_screen_region
from utils.get_memu_resolution import get_memu_resolution

load_dotenv()
ADB_PATH = os.getenv("ADB_PATH")

def adb_tap(x, y):
    subprocess.run(
        [ADB_PATH, "shell", "input", "tap", str(x), str(y)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def click_best_template_match(template_path, threshold=0.6):
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
    if template is None:
        raise FileNotFoundError(f"Missing template image: {template_path}")
    tH, tW = template.shape[:2]

    screenshot = grab_screen_region()
    gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    height, width = gray.shape[:2]

    # Define search region by ratios
    xratio1, yratio1 = 0.0, 0.0  # top-left
    xratio2, yratio2 = 0.8, 0.5  # bottom-right

    # Convert ratios to absolute pixel bounds
    x1 = int(width * xratio1)
    y1 = int(height * yratio1)
    x2 = int(width * xratio2)
    y2 = int(height * yratio2)

    # Crop search region
    cropped = gray[y1:y2, x1:x2]

    # Debug save
    debug_output_path = os.path.join(ROOT_DIR, "debug", "search_region.png")
    cv2.imwrite(debug_output_path, cropped)
    print(f"📸 Saved vertical belt search region to: {debug_output_path}")

    # Template matching loop
    best_val = -1
    best_loc = None
    best_template = None

    for scale in [1.5, 1.6, 1.7, 1.8, 1.9, 2, 2.1, 2.3, 2.4, 2.5]:
        resized_template = cv2.resize(template, (int(tW * scale), int(tH * scale)))
        if (
            resized_template.shape[0] > cropped.shape[0]
            or resized_template.shape[1] > cropped.shape[1]
        ):
            continue  # Skip templates larger than search region

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

        # Compute final screen coordinates using ratios
        memu_width, memu_height = get_memu_resolution()

        # Offset within the cropped region → back to screen space
        center_x = x1 + match_x + match_w // 2
        center_y = y1 + match_y + match_h // 2

        screen_x = int(center_x * memu_width / width)
        screen_y = int(center_y * memu_height / height)

        adb_tap(screen_x, screen_y)
        return True
    else:
        print(f"❌ No match found. Highest confidence: {best_val:.3f}")
        return False


def click_jar():
    template_path = os.path.join(DEBUG_DIR, "sauce_icon.png")
    click_best_template_match(template_path)


def main():
    click_jar()


if __name__ == "__main__":
    main()
