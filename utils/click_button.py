import cv2
import mss
import numpy as np
import subprocess
import time
import re
import os
import sys

from utils.get_memu_position import get_memu_bounds

ADB_PATH = r"D:\Program Files\Microvirt\MEmu\adb.exe"  # Replace with your ADB path if needed
CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "../"))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

ASSETS_DIR = os.path.join(ROOT_DIR, "assets")

def click_from_assets(filename, threshold=0.8):
    """
    Attempts to click a button by matching the template image from the assets folder.

    :param filename: Filename of the PNG in the assets folder (e.g., 'skip_button_right.png')
    :param threshold: Match confidence threshold
    :return: True if the click was successful, False otherwise
    """
    template_path = os.path.join(ASSETS_DIR, filename)
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"❌ Asset not found: {template_path}")

    return click_button(template_path, threshold=threshold)

def grab_screen_region(x, y, width, height):
    with mss.mss() as sct:
        monitor = {"top": y, "left": x, "width": width, "height": height}
        return np.array(sct.grab(monitor))

def get_memu_resolution():
    try:
        result = subprocess.check_output([ADB_PATH, "shell", "wm", "size"], stderr=subprocess.DEVNULL)
        match = re.search(r'Physical size:\s*(\d+)x(\d+)', result.decode())
        if match:
            return int(match.group(1)), int(match.group(2))
        raise RuntimeError("Could not parse resolution from ADB output.")
    except Exception as e:
        raise RuntimeError(f"Failed to get MEmu resolution: {e}")

def adb_tap(x, y):
    subprocess.run([ADB_PATH, "shell", "input", "tap", str(x), str(y)],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def adb_touch_and_hold(x, y, hold_duration=1.0):
    ms = int(hold_duration * 1000)
    subprocess.run([ADB_PATH, "shell", "input", "swipe", str(x), str(y), str(x), str(y), str(ms)],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def click_button(template_path, threshold=0.85):
    template = cv2.imread(template_path, 0)
    if template is None:
        raise FileNotFoundError(f"Missing template image: {template_path}")

    w, h = template.shape[::-1]
    left, top, width, height = get_memu_bounds()

    screenshot = grab_screen_region(left, top, width, height)
    gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    result = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    if max_val >= threshold:
        memu_width, memu_height = get_memu_resolution()
        screen_x = int((max_loc[0] + w // 2) * memu_width / width)
        screen_y = int((max_loc[1] + h // 2) * memu_height / height)

        adb_tap(screen_x, screen_y)
        print(f"✅ ADB tapped '{template_path}' at ({screen_x}, {screen_y}) with confidence {max_val:.2f}")
        return True
    else:
        print(f"❌ Button '{template_path}' not found. Confidence: {max_val:.2f}")
        return False

def click_and_hold(template_path, hold_duration=1.0, threshold=0.85):
    template = cv2.imread(template_path, 0)
    if template is None:
        raise FileNotFoundError(f"Missing template image: {template_path}")

    w, h = template.shape[::-1]
    left, top, width, height = get_memu_bounds()

    screenshot = grab_screen_region(left, top, width, height)
    gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    result = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    if max_val >= threshold:
        memu_width, memu_height = get_memu_resolution()
        screen_x = int((max_loc[0] + w // 2) * memu_width / width)
        screen_y = int((max_loc[1] + h // 2) * memu_height / height)

        adb_touch_and_hold(screen_x, screen_y, hold_duration)
        print(f"✅ ADB held '{template_path}' at ({screen_x}, {screen_y}) for {hold_duration:.2f}s (confidence {max_val:.2f})")
        return True
    else:
        print(f"❌ Button '{template_path}' not found. Confidence: {max_val:.2f}")
        return False
