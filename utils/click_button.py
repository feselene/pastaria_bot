import os
import re
import sys

import cv2

from utils.crop_screenshot_by_ratio import adb_tap_relative
from utils.get_memu_resolution import get_memu_bounds
from dotenv import load_dotenv

load_dotenv()
ADB_PATH = os.getenv("ADB_PATH")
CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "../"))
ASSETS_DIR = os.path.join(ROOT_DIR, "assets")

if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)


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
    screenshot = grab_screen_region()
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


def click_and_hold_ratios(x_ratio, y_ratio, hold_duration=1.0):
    """
    Performs an ADB touch-and-hold at a screen position defined by ratios.

    :param x_ratio: Horizontal position as a ratio (0.0 to 1.0)
    :param y_ratio: Vertical position as a ratio (0.0 to 1.0)
    :param hold_duration: Duration in seconds to hold the touch
    :return: True always (for consistency with other click_* functions)
    """
    memu_width, memu_height = get_memu_resolution()
    x = int(x_ratio * memu_width)
    y = int(y_ratio * memu_height)
    adb_touch_and_hold(x, y, hold_duration)
    return True


import io
import subprocess

import numpy as np
from PIL import Image


def grab_screen_region():
    """
    Captures a screenshot from the Android emulator/device using ADB
    and returns it as a NumPy RGB image array.

    :return: NumPy array of shape (H, W, 3) in RGB format
    """
    try:
        result = subprocess.check_output(["adb", "exec-out", "screencap", "-p"])
        image = Image.open(io.BytesIO(result)).convert("RGB")
        img_np = np.array(image)
        return img_np
    except Exception as e:
        print(f"❌ Failed to capture or convert ADB screenshot: {e}")
        return None


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


def adb_touch_and_hold(x, y, hold_duration=1.0):
    ms = int(hold_duration * 1000)
    subprocess.run(
        [ADB_PATH, "shell", "input", "swipe", str(x), str(y), str(x), str(y), str(ms)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def click_ratios(x_ratio, y_ratio):
    """
    ADB taps the screen at a given (x_ratio, y_ratio).

    :param x_ratio: Horizontal position as a ratio (0.0 to 1.0)
    :param y_ratio: Vertical position as a ratio (0.0 to 1.0)
    :return: True always (for consistent return behavior with other click_* functions)
    """
    memu_width, memu_height = get_memu_resolution()
    x = int(x_ratio * memu_width)
    y = int(y_ratio * memu_height)
    adb_tap(x, y)
    return True


def print_pixel_color_ratio(x_ratio, y_ratio):
    """
    Captures a full screen image via ADB and prints the color at a given screen ratio.

    :param x_ratio: Horizontal position as a ratio (0.0 to 1.0)
    :param y_ratio: Vertical position as a ratio (0.0 to 1.0)
    """
    try:
        memu_width, memu_height = get_memu_resolution()
        x = int(x_ratio * memu_width)
        y = int(y_ratio * memu_height)

        result = subprocess.check_output([ADB_PATH, "exec-out", "screencap", "-p"])
        image = Image.open(io.BytesIO(result)).convert("RGB")

        r, g, b = image.getpixel((x, y))
        print(
            f"🎨 Pixel at ratio ({x_ratio:.3f}, {y_ratio:.3f}) → ({x}, {y}): "
            f"RGB = ({r}, {g}, {b}) | BGR = ({b}, {g}, {r})"
        )

    except Exception as e:
        print(f"❌ Failed to get pixel color: {e}")


def click_button(template_path, threshold=0.7):
    # Load grayscale template (at correct size)
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
    if template is None:
        raise FileNotFoundError(f"Missing template image: {template_path}")
    tW, tH = template.shape[::-1]

    # Capture screen and convert
    screenshot = grab_screen_region()
    if screenshot is None:
        return False

    # Save raw screenshot for debug
    gray = cv2.cvtColor(screenshot, cv2.COLOR_RGB2GRAY)

    # Get image dimensions from screenshot
    height, width = gray.shape[:2]

    # Match once at original scale
    result = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    if max_val >= threshold:
        match_x, match_y = max_loc
        center_x = match_x + tW // 2
        center_y = match_y + tH // 2

        # Convert to ratios within the full screenshot
        x_ratio = center_x / width
        y_ratio = center_y / height

        adb_tap_relative(x_ratio, y_ratio)
        return True
    else:
        print(f"❌ Button '{template_path}' not found. Best confidence: {max_val:.2f}")
        return False


def click_and_hold(template_path, hold_duration=1.0, threshold=0.85):
    template = cv2.imread(template_path, 0)
    if template is None:
        raise FileNotFoundError(f"Missing template image: {template_path}")

    w, h = template.shape[::-1]
    left, top, width, height = get_memu_bounds()

    screenshot = grab_screen_region()
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
