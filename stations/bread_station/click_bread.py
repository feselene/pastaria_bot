import os
import sys

import cv2
import mss
import numpy as np

from utils.click_button import drag_ratios

CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "../../"))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)
ASSETS_DIR = os.path.join(ROOT_DIR, "assets")
OVEN_PATH = os.path.join(ASSETS_DIR, "oven.png")

from utils.get_memu_resolution import get_memu_bounds


def grab_screen_region(x, y, width, height):
    with mss.mss() as sct:
        monitor = {"top": y, "left": x, "width": width, "height": height}
        return np.array(sct.grab(monitor))


def get_best_template_match_center(template_path, threshold=0.75):
    # Load template in grayscale
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
    if template is None:
        raise FileNotFoundError(f"Missing template image: {template_path}")
    tH, tW = template.shape[:2]

    # Get emulator bounds
    left, top, width, height = get_memu_bounds()

    # Capture emulator window
    screenshot = grab_screen_region(left, top, width, height)
    gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    # Define vertical brown belt region (centered)
    belt_left = int(width * 0.30)
    belt_right = int(width * 0.62)
    belt_top = int(height * 0.05)
    belt_bottom = int(height * 0.95)

    cropped = gray[belt_top:belt_bottom, belt_left:belt_right]

    # Save debug image
    debug_output_path = os.path.join(ROOT_DIR, "debug", "search_region.png")
    cv2.imwrite(debug_output_path, cropped)
    print(f"📸 Saved vertical belt search region to: {debug_output_path}")

    best_val = -1
    best_loc = None
    best_scale = None
    best_template = None

    for scale in [1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0]:
        resized_template = cv2.resize(template, (int(tW * scale), int(tH * scale)))
        rH, rW = resized_template.shape[:2]
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

        center_x = left + belt_left + match_x + match_w // 2
        center_y = top + belt_top + match_y + match_h // 2

        print(
            f"✅ Found match at ({center_x}, {center_y}) with scale {best_scale} and confidence {best_val:.3f}"
        )
        return center_x, center_y
    else:
        print(f"❌ No match found. Highest confidence: {best_val:.3f}")
        return None, None


def get_bread_ratios():
    """
    Matches the bread image and returns its (x, y) position as ratios
    relative to the emulator window.

    :return: (x_ratio, y_ratio) if match is found, otherwise (None, None)
    """
    template_path = (
        r"C:\Users\ceo\IdeaProjects\pastaria_bot\debug\debug_bread_cropped.png"
    )
    match_x, match_y = get_best_template_match_center(template_path)

    if match_x is None or match_y is None:
        print("❌ Could not find bread image.")
        return None, None

    memu_left, memu_top, memu_width, memu_height = get_memu_bounds()
    x_ratio = (match_x - memu_left) / memu_width
    y_ratio = (match_y - memu_top) / memu_height

    print(f"📐 Bread matched at ratios: x={x_ratio:.3f}, y={y_ratio:.3f}")
    return x_ratio, y_ratio


def click_bread():
    template_path = (
        r"C:\Users\ceo\IdeaProjects\pastaria_bot\debug\debug_bread_cropped.png"
    )
    x, y = get_bread_ratios()

    drag_ratios(x, y, 0.15, 0.46)


def main():
    print(True)


if __name__ == "__main__":
    main()
