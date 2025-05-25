import datetime
import os
import re
import shutil
import subprocess
import sys
import time

import cv2
import mss
import numpy as np
from dotenv import load_dotenv
from PIL import Image
from rembg import remove

load_dotenv()

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

ADB_PATH = r"D:\Program Files\Microvirt\MEmu\adb.exe"  # Update if needed


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


def contains_metal(image_path, threshold=0.3):
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


def capture_center_picker_square():
    x_ratio = 0.422
    y_ratio = 0.32
    width_px = 360
    height_px = 180
    square_size = 180
    small_square_size = 90
    half_w = width_px / 2
    half_h = height_px / 2
    half_sq = square_size / 2
    half_small_sq = small_square_size / 2

    left, top, width, height = get_memu_bounds()
    center_x = int(left + width * x_ratio)
    center_y = int(top + height * y_ratio)

    box_left = int(center_x - half_w)
    box_top = int(center_y - half_h)

    square_left = int(center_x - half_sq)
    square_top = int(center_y - half_sq)

    small_square_left = int(center_x - half_small_sq)
    small_square_top = int(center_y - half_small_sq) - 25  # Shift upward by 25 pixels

    region = {
        "left": box_left,
        "top": box_top,
        "width": width_px,
        "height": height_px,
    }

    square_region = {
        "left": square_left,
        "top": square_top,
        "width": square_size,
        "height": square_size,
    }

    small_square_region = {
        "left": small_square_left,
        "top": small_square_top,
        "width": small_square_size,
        "height": small_square_size,
    }

    with mss.mss() as sct:
        full_screen = np.array(
            sct.grab({"left": left, "top": top, "width": width, "height": height})
        )
        cropped = np.array(sct.grab(region))
        cropped_square = np.array(sct.grab(square_region))
        cropped_small_square = np.array(sct.grab(small_square_region))

    # Draw rectangles on full screen screenshot
    cv2.rectangle(
        full_screen,
        (box_left - left, box_top - top),
        (box_left - left + width_px, box_top - top + height_px),
        (255, 0, 0),
        2,
    )
    cv2.rectangle(
        full_screen,
        (square_left - left, square_top - top),
        (square_left - left + square_size, square_top - top + square_size),
        (0, 255, 0),
        2,
    )
    cv2.rectangle(
        full_screen,
        (small_square_left - left, small_square_top - top),
        (
            small_square_left - left + small_square_size,
            small_square_top - top + small_square_size,
        ),
        (0, 0, 255),
        2,
    )

    # Save screenshots
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    overlay_path = os.path.join(DEBUG_DIR, f"{timestamp}_picker_overlay.png")
    cropped_path = os.path.join(DEBUG_DIR, "topping_active.png")
    square_path = os.path.join(DEBUG_DIR, f"{timestamp}_cropped_square.png")
    small_square_path = os.path.join(DEBUG_DIR, f"{timestamp}_small_square.png")

    cv2.imwrite(overlay_path, full_screen)
    print(f"📸 Overlay with capture box saved to: {overlay_path}")

    cv2.imwrite(cropped_path, cropped)
    cv2.imwrite(square_path, cropped_square)
    cv2.imwrite(small_square_path, cropped_small_square)
    print(f"📸 Square crop saved to: {square_path}")
    print(f"📸 Small square crop saved to: {small_square_path}")

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

    print(
        f"⬅️ ADB swiped topping picker left from ({center_x}, {center_y}) to ({swipe_x}, {center_y})"
    )


def third_swipe_left():
    x_ratio = 0.422
    y_ratio = 0.32
    swipe_offset_ratio = 0.1809 / 3
    memu_width, memu_height = get_memu_resolution()

    center_x = int(memu_width * x_ratio)
    center_y = int(memu_height * y_ratio)
    swipe_x = int(center_x + memu_width * swipe_offset_ratio)  # Swiping right

    adb_swipe(center_x, center_y, swipe_x, center_y, duration_ms=2000)

    print(
        f"➡️ ADB swiped topping picker right from ({center_x}, {center_y}) to ({swipe_x}, {center_y})"
    )


def half_swipe_left():
    x_ratio = 0.422
    y_ratio = 0.32
    swipe_offset_ratio = 0.1809 / 2
    memu_width, memu_height = get_memu_resolution()

    center_x = int(memu_width * x_ratio)
    center_y = int(memu_height * y_ratio)
    swipe_x = int(center_x + memu_width * swipe_offset_ratio)  # Swiping right

    adb_swipe(center_x, center_y, swipe_x, center_y, duration_ms=2000)

    print(
        f"➡️ ADB swiped topping picker right from ({center_x}, {center_y}) to ({swipe_x}, {center_y})"
    )


def swipe_topping_picker_left():
    x_ratio = 0.422
    y_ratio = 0.32
    swipe_offset_ratio = 0.1809
    memu_width, memu_height = get_memu_resolution()

    center_x = int(memu_width * x_ratio)
    center_y = int(memu_height * y_ratio)
    swipe_x = int(center_x - memu_width * swipe_offset_ratio)

    adb_swipe(center_x, center_y, swipe_x, center_y, duration_ms=2000)

    print(
        f"⬅️ ADB swiped topping picker left from ({center_x}, {center_y}) to ({swipe_x}, {center_y})"
    )


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


def select_ingredient(cropped_path, max_attempts=10, delay_between_swipes=0):
    for attempt in range(max_attempts):
        current_path, small_square_path = capture_center_picker_square()

        if contains_metal(small_square_path):
            print("calling half_swipe_left because image is mostly_black or grey")
            half_swipe_left()
            current_path, small_square_path = capture_center_picker_square()

        if is_mostly_black(small_square_path):
            print("calling third_swipe_left because image is mostly_black")
            third_swipe_left()
            current_path, small_square_path = capture_center_picker_square()

        if contains_metal(small_square_path):
            print("calling half_swipe_left because image is mostly_black or grey")
            half_swipe_left()
            current_path, small_square_path = capture_center_picker_square()

        match_response = is_matching(current_path, cropped_path)

        if "yes" in match_response:
            print(f"✅ Match found on attempt {attempt}: {current_path}")

            safe_match_response = sanitize_filename_component(match_response)

            current_dest = os.path.join(
                MATCHES_DIR, f"{safe_match_response}_current.png"
            )
            target_dest = os.path.join(MATCHES_DIR, f"{safe_match_response}_target.png")

            shutil.copy(current_path, current_dest)
            shutil.copy(cropped_path, target_dest)

            print(f"📁 Current match saved to: {current_dest}")
            print(f"📁 Target image saved to: {target_dest}")
            return True
        else:
            print(
                f"❌ No match on attempt {attempt}, swiping... (response: {match_response})"
            )
            swipe_topping_picker_left()
        time.sleep(delay_between_swipes)

    print("⚠️ Maximum attempts reached without finding a match.")
    return False


def main():
    print(os.getenv("GEMINI_API_KEY"))
    target_topping = os.path.join(TOPPINGS_DIR, "topping4.png")
    success = select_ingredient(target_topping)

    if success:
        print("🎯 Ingredient successfully selected!")
    else:
        print("❌ Ingredient not found.")


if __name__ == "__main__":
    main()
