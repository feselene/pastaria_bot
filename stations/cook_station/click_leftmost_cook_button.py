import os
from time import sleep

import cv2
import mss
import numpy as np
import pyautogui

from utils.get_memu_resolution import get_memu_bounds

TEMPLATE_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../assets/plus_template.png")
)
THRESHOLD = 0.85


def grab_emulator_region():
    left, top, width, height = get_memu_bounds()
    with mss.mss() as sct:
        monitor = {"top": top, "left": left, "width": width, "height": height}
        img = np.array(sct.grab(monitor))
    return img, left, top


def click_leftmost_plus_button():
    print("🍳 Opening pot...")
    screenshot, offset_x, offset_y = grab_emulator_region()
    gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(TEMPLATE_PATH, 0)

    if template is None:
        raise FileNotFoundError(f"Template not found at {TEMPLATE_PATH}")

    h, w = template.shape
    result = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)

    matches = np.where(result >= THRESHOLD)
    match_points = list(zip(*matches[::-1]))  # (x, y)

    if not match_points:
        print("❌ No green plus buttons found.")
        return False

    # Sort by x (left to right)
    match_points.sort(key=lambda pt: pt[0])
    best_match = match_points[0]

    center_x = offset_x + best_match[0] + w // 2
    center_y = offset_y + best_match[1] + h // 2

    pyautogui.moveTo(center_x, center_y)
    pyautogui.click()

    print(f"✅ Clicked leftmost plus at ({center_x}, {center_y})")
    sleep(0.3)
    return True


# Run this when called directly
if __name__ == "__main__":
    click_leftmost_plus_button()
