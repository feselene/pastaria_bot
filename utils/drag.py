import subprocess

import cv2
import mss
import numpy as np

from utils.get_memu_resolution import get_memu_bounds, get_memu_resolution
from utils.click_button import grab_screen_region

ADB_PATH = r"D:\Program Files\Microvirt\MEmu\adb.exe"  # Update if needed


def adb_swipe(x1, y1, x2, y2, duration_ms=200):
    subprocess.run(
        [
            ADB_PATH,
            "shell",
            "input",
            "swipe",
            str(x1),
            str(y1),
            str(x2),
            str(y2),
            str(duration_ms),
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def drag_between_templates(start_template_path, end_template_path, threshold=0.85):
    start_template = cv2.imread(start_template_path, 0)
    end_template = cv2.imread(end_template_path, 0)
    if start_template is None:
        raise FileNotFoundError(f"Missing start template: {start_template_path}")
    if end_template is None:
        raise FileNotFoundError(f"Missing end template: {end_template_path}")

    start_w, start_h = start_template.shape[::-1]
    end_w, end_h = end_template.shape[::-1]

    left, top, width, height = get_memu_bounds()
    memu_width, memu_height = get_memu_resolution()

    screenshot = grab_screen_region()
    gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    result_start = cv2.matchTemplate(gray, start_template, cv2.TM_CCOEFF_NORMED)
    _, max_val_start, _, max_loc_start = cv2.minMaxLoc(result_start)

    result_end = cv2.matchTemplate(gray, end_template, cv2.TM_CCOEFF_NORMED)
    _, max_val_end, _, max_loc_end = cv2.minMaxLoc(result_end)

    if max_val_start >= threshold and max_val_end >= threshold:
        # Convert from screenshot coordinates to emulator coordinates
        start_screen_x = max_loc_start[0] + start_w // 2
        start_screen_y = max_loc_start[1] + start_h // 2
        end_screen_x = max_loc_end[0] + end_w // 2
        end_screen_y = max_loc_end[1] + end_h // 2

        start_x = int(start_screen_x * memu_width / width)
        start_y = int(start_screen_y * memu_height / height)
        end_x = int(end_screen_x * memu_width / width)
        end_y = int(end_screen_y * memu_height / height)

        adb_swipe(start_x, start_y, end_x, end_y, duration_ms=200)
        print(f"✅ ADB dragged from ({start_x}, {start_y}) to ({end_x}, {end_y})")
        return True
    else:
        print(
            f"❌ Drag failed. Start confidence: {max_val_start:.2f}, End confidence: {max_val_end:.2f}"
        )
        return False