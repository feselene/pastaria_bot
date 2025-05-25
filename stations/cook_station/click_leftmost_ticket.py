import os
from time import sleep

import cv2
import mss
import numpy as np
import sys
import time

CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "../../"))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)
TEMPLATE_PATH = os.path.join(ROOT_DIR, "assets", "ticket_full.png")

THRESHOLD = 0.5
ADB_PATH = r"D:\Program Files\Microvirt\MEmu\adb.exe"


from utils.get_memu_resolution import get_memu_bounds, get_memu_resolution
from utils.crop_screenshot_by_ratio import adb_tap_relative


def adb_tap(x, y):
    os.system(f'"{ADB_PATH}" shell input tap {x} {y}')


def grab_emulator_region():
    left, top, width, height = get_memu_bounds()
    with mss.mss() as sct:
        monitor = {"top": top, "left": left, "width": width, "height": height}
        img = np.array(sct.grab(monitor))
    return img, left, top, width, height


def click_leftmost_ticket():
    adb_tap_relative(0.5, 0.03)
    time.sleep(1)
    screenshot, offset_x, offset_y, width, height = grab_emulator_region()
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

    abs_x = offset_x + best_match[0] + w // 2
    abs_y = offset_y + best_match[1] + h // 2

    # Convert to emulator screen coordinates
    memu_width, memu_height = get_memu_resolution()
    tap_x = int((abs_x - offset_x) * memu_width / width)
    tap_y = int((abs_y - offset_y) * memu_height / height)

    adb_tap(tap_x, tap_y)

    print(f"✅ ADB tapped leftmost plus at ({tap_x}, {tap_y})")
    sleep(0.3)
    return True


# Run this when called directly
if __name__ == "__main__":
    click_leftmost_ticket()
