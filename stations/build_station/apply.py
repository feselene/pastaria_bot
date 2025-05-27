import datetime
import io
import os
import re
import subprocess
import sys
import time

import cv2
import numpy as np
from PIL import Image
from rembg import remove
from dotenv import load_dotenv

CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "../../"))
DEBUG_DIR = os.path.join(ROOT_DIR, "debug")
TOPPINGS_DIR = os.path.join(ROOT_DIR, "toppings")
MATCHES_DIR = os.path.join(ROOT_DIR, "matches")
os.makedirs(MATCHES_DIR, exist_ok=True)  # Ensure the directory exists

if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from utils.gemini_matcher import is_matching
from utils.get_memu_resolution import get_memu_bounds, get_memu_resolution

load_dotenv()
ADB_PATH = os.getenv("ADB_PATH")


def adb_swipe(x1, y1, x2, y2, duration_ms=300):
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


def is_mostly_black(image_path, threshold=0.65, tolerance=10):
    """
    Checks if more than `threshold` of the image is visually black,
    defined as within `tolerance` of #0e0e0e.

    Args:
        image_path (str): Path to the image file.
        threshold (float): Fraction of near-black pixels required to return True.
        tolerance (int): Max per-channel distance from [14, 14, 14] to count as black.

    Returns:
        bool: True if black pixel ratio exceeds threshold.
        float: Actual black pixel ratio.
    """
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Could not load image from: {image_path}")

    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    pixels = image_rgb.reshape(-1, 3)

    target_black = np.array([14, 14, 14])
    diff = np.abs(pixels - target_black)
    matches = np.all(diff <= tolerance, axis=1)

    match_ratio = np.sum(matches) / len(pixels)
    return match_ratio > threshold


def contains_metal(image_path, threshold=0.2):
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Could not load image from: {image_path}")

    # Convert to RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Flatten the image and compare
    pixels = image_rgb.reshape(-1, 3)
    target_color = np.array([152, 152, 152])

    matches = np.all(pixels == target_color, axis=1)
    match_ratio = np.sum(matches) / pixels.shape[0]

    return match_ratio > threshold

def grab_screen_region():
    """
    Captures a screenshot from the Android emulator/device using ADB
    and returns it as a NumPy RGB image array.
    """
    try:
        result = subprocess.check_output(["adb", "exec-out", "screencap", "-p"])
        image = Image.open(io.BytesIO(result)).convert("RGB")
        img_np = np.array(image)
        return img_np
    except Exception as e:
        print(f"❌ Failed to capture or convert ADB screenshot: {e}")
        return None

def crop_region(image, region):
    left = region["left"]
    top = region["top"]
    right = left + region["width"]
    bottom = top + region["height"]
    return image[top:bottom, left:right]

def capture_center_picker_square():
    x_ratio = 0.422
    y_ratio = 0.26

    screen = grab_screen_region()
    if screen is None:
        return None, None

    screen_height, screen_width, _ = screen.shape

    small_square_size = int(screen_height / 12.5)
    square_size = 2 * small_square_size
    height_px = 2 * small_square_size
    width_px = 4 * small_square_size
    half_w = width_px / 2
    half_h = height_px / 2
    half_sq = square_size / 2
    half_small_sq = small_square_size / 2

    center_x = int(screen_width * x_ratio)
    center_y = int(screen_height * y_ratio)

    box_left = int(center_x - half_w)
    box_top = int(center_y - half_h)

    square_left = int(center_x - half_sq)
    square_top = int(center_y - half_sq)

    small_square_left = int(center_x - half_small_sq)
    small_square_top = int(center_y - half_small_sq) - int(screen_height / 40)  # Shift upward

    region = {"left": box_left, "top": box_top, "width": width_px, "height": height_px}
    square_region = {"left": square_left, "top": square_top, "width": square_size, "height": square_size}
    small_square_region = {"left": small_square_left, "top": small_square_top, "width": small_square_size, "height": small_square_size}

    cropped = crop_region(screen, region)
    cropped_square = crop_region(screen, square_region)
    cropped_small_square = crop_region(screen, small_square_region)

    # Draw rectangles
    overlay = screen.copy()
    cv2.rectangle(overlay, (box_left, box_top), (box_left + width_px, box_top + height_px), (255, 0, 0), 2)
    cv2.rectangle(overlay, (square_left, square_top), (square_left + square_size, square_top + square_size), (0, 255, 0), 2)
    cv2.rectangle(overlay, (small_square_left, small_square_top), (small_square_left + small_square_size, small_square_top + small_square_size), (0, 0, 255), 2)

    # Save images
    os.makedirs(DEBUG_DIR, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    overlay_path = os.path.join(DEBUG_DIR, f"{timestamp}_picker_overlay.png")
    cropped_path = os.path.join(DEBUG_DIR, "topping_active.png")
    small_square_path = os.path.join(DEBUG_DIR, f"{timestamp}_small_square.png")

    cv2.imwrite(overlay_path, cv2.cvtColor(overlay, cv2.COLOR_RGB2BGR))
    cv2.imwrite(cropped_path, cv2.cvtColor(cropped, cv2.COLOR_RGB2BGR))
    cv2.imwrite(small_square_path, cv2.cvtColor(cropped_small_square, cv2.COLOR_RGB2BGR))

    return cropped_path, small_square_path


def half_swipe():
    x_ratio = 0.422
    y_ratio = 0.32
    swipe_offset_ratio = 0.1809 / 2
    memu_width, memu_height = get_memu_resolution()

    center_x = int(memu_width * x_ratio)
    center_y = int(memu_height * y_ratio)
    swipe_x = int(center_x - memu_width * swipe_offset_ratio)

    adb_swipe(center_x, center_y, swipe_x, center_y, duration_ms=2000)


def third_swipe_left():
    x_ratio = 0.422
    y_ratio = 0.32
    swipe_offset_ratio = 0.1809 / 3
    memu_width, memu_height = get_memu_resolution()

    center_x = int(memu_width * x_ratio)
    center_y = int(memu_height * y_ratio)
    swipe_x = int(center_x + memu_width * swipe_offset_ratio)  # Swiping right

    adb_swipe(center_x, center_y, swipe_x, center_y, duration_ms=2000)


def half_swipe_left():
    x_ratio = 0.422
    y_ratio = 0.32
    swipe_offset_ratio = 0.1809 / 2
    memu_width, memu_height = get_memu_resolution()

    center_x = int(memu_width * x_ratio)
    center_y = int(memu_height * y_ratio)
    swipe_x = int(center_x + memu_width * swipe_offset_ratio)  # Swiping right

    adb_swipe(center_x, center_y, swipe_x, center_y, duration_ms=2000)


def swipe_topping_picker_left():
    x_ratio = 0.422
    y_ratio = 0.32
    swipe_offset_ratio = 0.1809
    memu_width, memu_height = get_memu_resolution()

    center_x = int(memu_width * x_ratio)
    center_y = int(memu_height * y_ratio)
    swipe_x = int(center_x - memu_width * swipe_offset_ratio)

    adb_swipe(center_x, center_y, swipe_x, center_y, duration_ms=2000)

def jump_backwards():
    # Quickly jump from tomato to chicken.
    x_ratio = 0.422
    y_ratio = 0.32
    swipe_offset_ratio = -0.4
    memu_width, memu_height = get_memu_resolution()

    center_x = int(memu_width * x_ratio)
    center_y = int(memu_height * y_ratio)
    swipe_x = int(center_x - memu_width * swipe_offset_ratio)
    for i in range(2):
        adb_swipe(center_x, center_y, swipe_x, center_y, duration_ms=500)


def remove_background_and_crop_image(cv_image: np.ndarray) -> np.ndarray:
    if cv_image.shape[2] == 3:
        cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGBA)
    elif cv_image.shape[2] == 4:
        cv_image = cv_image
    else:
        raise ValueError("Input image must have 3 or 4 channels")

    pil_image = Image.fromarray(cv2.cvtColor(cv_image, cv2.COLOR_BGRA2RGBA))

    removed = remove(pil_image)
    if removed.mode != "RGBA":
        removed = removed.convert("RGBA")
    bbox = removed.getbbox()
    cropped = removed.crop(bbox) if bbox else removed
    result = cv2.cvtColor(np.array(cropped), cv2.COLOR_RGBA2BGRA)
    return result


def sanitize_filename_component(text, max_length=50):
    safe = re.sub(r"\W+", "_", text)
    return safe[:max_length]


def select_ingredient(cropped_path, max_attempts=20, delay_between_swipes=0, jump = False):
    if jump:
        jump_backwards()

    for attempt in range(max_attempts):
        current_path, small_square_path = capture_center_picker_square()

        if contains_metal(small_square_path):
            print("Calling half_swipe_left because ingredient picture looking at metal.")
            half_swipe_left()
            current_path, small_square_path = capture_center_picker_square()

        if is_mostly_black(small_square_path):
            print("calling third_swipe_left because image is mostly_black")
            third_swipe_left()
            current_path, small_square_path = capture_center_picker_square()

        if contains_metal(small_square_path):
            print("Calling half_swipe_left because ingredient picture looking at metal.")
            half_swipe_left()
            current_path, small_square_path = capture_center_picker_square()

        match_response = is_matching(current_path, cropped_path)

        if "yes" in match_response:
            return True
        else:
            swipe_topping_picker_left()
        time.sleep(delay_between_swipes)

    print("⚠️ Maximum attempts reached without finding a match.")
    return False


def main():
    jump_backwards()


if __name__ == "__main__":
    main()
