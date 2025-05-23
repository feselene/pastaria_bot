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

def click_and_hold_from_assets(filename, hold_duration=1.0, threshold=0.85):
    """
    Attempts to click and hold a button by matching the template image from the assets folder.

    :param filename: Filename of the PNG in the assets folder (e.g., 'hold_button.png')
    :param hold_duration: Time (in seconds) to hold the tap
    :param threshold: Match confidence threshold
    :return: True if the hold was successful, False otherwise
    """
    template_path = os.path.join(ASSETS_DIR, filename)
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"❌ Asset not found: {template_path}")

    return click_and_hold(template_path, hold_duration=hold_duration, threshold=threshold)

def drag(filename1, filename2, threshold=0.85, duration_ms=300):
    """
    Performs an ADB drag from the center of filename1 to the center of filename2
    using the same coordinate scaling logic as click_button.

    :param filename1: Starting image filename in assets
    :param filename2: Ending image filename in assets
    :param threshold: Template match threshold
    :param duration_ms: Duration of the drag in milliseconds
    :return: True if both templates matched and drag occurred, False otherwise
    """
    f1 = os.path.join(ASSETS_DIR, filename1)
    f2 = os.path.join(ASSETS_DIR, filename2)

    for path in [f1, f2]:
        if not os.path.exists(path):
            raise FileNotFoundError(f"Missing template image: {path}")

    # Load templates
    template1 = cv2.imread(f1, 0)
    template2 = cv2.imread(f2, 0)
    if template1 is None or template2 is None:
        raise FileNotFoundError("One of the templates could not be read.")

    w1, h1 = template1.shape[::-1]
    w2, h2 = template2.shape[::-1]

    # Get MEmu screen bounds and capture
    left, top, width, height = get_memu_bounds()
    screenshot = grab_screen_region(left, top, width, height)
    gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    # Match template 1
    result1 = cv2.matchTemplate(gray, template1, cv2.TM_CCOEFF_NORMED)
    _, val1, _, loc1 = cv2.minMaxLoc(result1)

    # Match template 2
    result2 = cv2.matchTemplate(gray, template2, cv2.TM_CCOEFF_NORMED)
    _, val2, _, loc2 = cv2.minMaxLoc(result2)

    if val1 < threshold or val2 < threshold:
        print(f"❌ Drag failed. Match confidence too low: {val1:.2f}, {val2:.2f}")
        return False

    # Convert to MEmu (Android) coordinate space
    memu_width, memu_height = get_memu_resolution()
    start_x = int((loc1[0] + w1 // 2) * memu_width / width)
    start_y = int((loc1[1] + h1 // 2) * memu_height / height)
    end_x   = int((loc2[0] + w2 // 2) * memu_width / width)
    end_y   = int((loc2[1] + h2 // 2) * memu_height / height)

    subprocess.run([
        ADB_PATH, "shell", "input", "swipe",
        str(start_x), str(start_y), str(end_x), str(end_y), str(duration_ms)
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    print(f"✅ ADB drag from ({start_x}, {start_y}) to ({end_x}, {end_y})")
    return True


import subprocess

ADB_PATH = r"D:\Program Files\Microvirt\MEmu\adb.exe"  # Update if needed

def drag_ratios(start_x_ratio=0.72, start_y_ratio=0.46,
                end_x_ratio=0.44, end_y_ratio=0.61, duration=0.1):
    """
    Drags from a start to an end position using ADB based on ratios of the emulator screen size.

    :param start_x_ratio: Horizontal ratio of the start point (0.0 to 1.0)
    :param start_y_ratio: Vertical ratio of the start point (0.0 to 1.0)
    :param end_x_ratio: Horizontal ratio of the end point (0.0 to 1.0)
    :param end_y_ratio: Vertical ratio of the end point (0.0 to 1.0)
    :param duration: Time in seconds for the drag (converted to milliseconds)
    """
    from utils.get_memu_position import get_memu_bounds
    from utils.click_button import get_memu_resolution  # Assumes you have this defined

    memu_width, memu_height = get_memu_resolution()

    start_x = int(memu_width * start_x_ratio)
    start_y = int(memu_height * start_y_ratio)
    end_x = int(memu_width * end_x_ratio)
    end_y = int(memu_height * end_y_ratio)
    duration_ms = int(duration * 1000)

    subprocess.run([
        ADB_PATH, "shell", "input", "swipe",
        str(start_x), str(start_y), str(end_x), str(end_y), str(duration_ms)
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    print(f"📱 ADB drag from ({start_x}, {start_y}) to ({end_x}, {end_y}) over {duration_ms}ms")


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
