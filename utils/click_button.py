import os
import re
import subprocess
import sys
import time

import cv2
import mss
import numpy as np

from utils.get_memu_resolution import get_memu_bounds

ADB_PATH = (
    r"D:\Program Files\Microvirt\MEmu\adb.exe"  # Replace with your ADB path if needed
)
CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "../"))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

ASSETS_DIR = os.path.join(ROOT_DIR, "assets")

def click_from_assets(filename, threshold=0.6):
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

    return click_and_hold(
        template_path, hold_duration=hold_duration, threshold=threshold
    )


def drag_image_to_ratio(
    template_path,
    target_x_ratio=0.15,
    target_y_ratio=0.46,
    threshold=0.5,
    duration_ms=300,
):
    """
    Clicks and drags from the position of a matched template image to a fixed screen ratio.
    Uses only ADB input — does not move your mouse.

    :param template_path: Absolute path to the template image
    :param target_x_ratio: Target X ratio on Android screen
    :param target_y_ratio: Target Y ratio on Android screen
    :param threshold: Match confidence threshold
    :param duration_ms: Duration of drag in milliseconds
    """
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Template not found: {template_path}")

    template = cv2.imread(template_path, 0)
    if template is None:
        raise FileNotFoundError("Template image could not be read.")

    w, h = template.shape[::-1]

    # Get resolution and capture screenshot at 1:1 resolution
    memu_width, memu_height = get_memu_resolution()
    screenshot = grab_screen_region(0, 0, memu_width, memu_height)
    gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    # Match template
    result = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    if max_val < threshold:
        print(f"❌ Match confidence too low: {max_val:.2f}")
        return False

    start_x = max_loc[0] + w // 2
    start_y = max_loc[1] + h // 2

    end_x = int(memu_width * target_x_ratio)
    end_y = int(memu_height * target_y_ratio)

    subprocess.run(
        [
            ADB_PATH,
            "shell",
            "input",
            "swipe",
            str(start_x),
            str(start_y),
            str(end_x),
            str(end_y),
            str(duration_ms),
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    return True


import subprocess

ADB_PATH = r"D:\Program Files\Microvirt\MEmu\adb.exe"  # Update if needed


def drag_ratios(
    start_x_ratio=0.72,
    start_y_ratio=0.46,
    end_x_ratio=0.44,
    end_y_ratio=0.61,
    duration=0.5,
):
    memu_width, memu_height = get_memu_resolution()

    start_x = int(memu_width * start_x_ratio)
    start_y = int(memu_height * start_y_ratio)
    end_x = int(memu_width * end_x_ratio)
    end_y = int(memu_height * end_y_ratio)
    duration_ms = int(duration * 1000)

    subprocess.run(
        [
            ADB_PATH,
            "shell",
            "input",
            "swipe",
            str(start_x),
            str(start_y),
            str(end_x),
            str(end_y),
            str(duration_ms),
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    print(
        f"📱 ADB drag from ({start_x}, {start_y}) to ({end_x}, {end_y}) over {duration_ms}ms"
    )


def grab_screen_region(x, y, width, height):
    with mss.mss() as sct:
        monitor = {"top": y, "left": x, "width": width, "height": height}
        return np.array(sct.grab(monitor))


def get_memu_resolution():
    try:
        result = subprocess.check_output(
            [ADB_PATH, "shell", "wm", "size"], stderr=subprocess.DEVNULL
        )
        match = re.search(r"Physical size:\s*(\d+)x(\d+)", result.decode())
        if match:
            return int(match.group(1)), int(match.group(2))
        raise RuntimeError("Could not parse resolution from ADB output.")
    except Exception as e:
        raise RuntimeError(f"Failed to get MEmu resolution: {e}")


def adb_tap(x, y):
    subprocess.run(
        [ADB_PATH, "shell", "input", "tap", str(x), str(y)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

def adb_tap_ratio(x_ratio, y_ratio):
    """
    Performs an ADB tap at a location defined by screen ratios.

    :param x_ratio: Horizontal position as a ratio of screen width (0.0 to 1.0)
    :param y_ratio: Vertical position as a ratio of screen height (0.0 to 1.0)
    """
    memu_width, memu_height = get_memu_resolution()
    x = int(x_ratio * memu_width)
    y = int(y_ratio * memu_height)
    adb_tap(x, y)
    print(f"🖱️ ADB tapped at ratio ({x_ratio:.2f}, {y_ratio:.2f}) → absolute ({x}, {y})")



def adb_touch_and_hold(x, y, hold_duration=1.0):
    ms = int(hold_duration * 1000)
    subprocess.run(
        [ADB_PATH, "shell", "input", "swipe", str(x), str(y), str(x), str(y), str(ms)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def click_button(template_path, threshold=0.7):
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
        print(
            f"✅ ADB held '{template_path}' at ({screen_x}, {screen_y}) for {hold_duration:.2f}s (confidence {max_val:.2f})"
        )
        return True
    else:
        print(f"❌ Button '{template_path}' not found. Confidence: {max_val:.2f}")
        return False
