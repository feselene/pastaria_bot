import os
import re
import sys
import time
import shutil
import cv2
import mss
import numpy as np
from dotenv import load_dotenv
from PIL import Image
from rembg import remove
import subprocess

load_dotenv()

CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "../../"))
DEBUG_DIR = os.path.join(ROOT_DIR, "debug")
TOPPINGS_DIR = os.path.join(ROOT_DIR, "toppings")
MATCHES_DIR = os.path.join(ROOT_DIR, "matches")
os.makedirs(MATCHES_DIR, exist_ok=True)  # Ensure the directory exists

if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from utils.gemini_matcher import is_matching, recenter
from utils.get_memu_resolution import get_memu_bounds, get_memu_resolution

ADB_PATH = r"D:\Program Files\Microvirt\MEmu\adb.exe"  # Update if needed

def adb_swipe(x1, y1, x2, y2, duration_ms=300):
    subprocess.run([
        ADB_PATH, "shell", "input", "swipe",
        str(x1), str(y1), str(x2), str(y2), str(duration_ms)
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

import datetime

def capture_center_picker_square():
    x_ratio = 0.422
    y_ratio = 0.32
    width_px = 360
    height_px = 180
    half_w = width_px / 2
    half_h = height_px / 2

    left, top, width, height = get_memu_bounds()
    center_x = int(left + width * x_ratio)
    center_y = int(top + height * y_ratio)

    box_left = int(center_x - half_w)
    box_top = int(center_y - half_h)

    region = {
        "left": box_left,
        "top": box_top,
        "width": width_px,
        "height": height_px,
    }

    with mss.mss() as sct:
        full_screen = np.array(sct.grab({"left": left, "top": top, "width": width, "height": height}))
        cropped = np.array(sct.grab(region))

    # Draw blue rectangle on the full screen screenshot
    cv2.rectangle(
        full_screen,
        (box_left - left, box_top - top),
        (box_left - left + width_px, box_top - top + height_px),
        (255, 0, 0),
        2
    )

    # Save annotated debug screenshot
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    overlay_path = os.path.join(DEBUG_DIR, f"{timestamp}_picker_overlay.png")
    cv2.imwrite(overlay_path, full_screen)
    print(f"📸 Overlay with capture box saved to: {overlay_path}")

    # Save and return cropped region
    cropped_path = os.path.join(DEBUG_DIR, "topping_active.png")
    cv2.imwrite(cropped_path, cropped)
    return cropped_path




def swipe_topping_picker_left():
    x_ratio = 0.422
    y_ratio = 0.32
    swipe_offset_ratio = 0.1809
    left, top, width, height = get_memu_bounds()
    memu_width, memu_height = get_memu_resolution()

    center_x = int(memu_width * x_ratio)
    center_y = int(memu_height * y_ratio)
    swipe_x = int(center_x - memu_width * swipe_offset_ratio)

    adb_swipe(center_x, center_y, swipe_x, center_y, duration_ms=2000)

    print(f"⬅️ ADB swiped topping picker left from ({center_x}, {center_y}) to ({swipe_x}, {center_y})")

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

def select_ingredient(cropped_path, max_attempts=10, delay_between_swipes=2):
    for attempt in range(max_attempts):
        current_path = capture_center_picker_square()
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
