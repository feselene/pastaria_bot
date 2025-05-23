import os
import sys
import time
import re
import cv2
import mss
import numpy as np
import pyautogui
from PIL import Image
from rembg import remove

from dotenv import load_dotenv
load_dotenv()

CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "../../"))
DEBUG_DIR = os.path.join(ROOT_DIR, "debug")
TOPPINGS_DIR = os.path.join(ROOT_DIR, "toppings")
MATCHES_DIR = os.path.join(ROOT_DIR, "matches")
os.makedirs(MATCHES_DIR, exist_ok=True)  # Ensure the directory exists

if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from utils.get_memu_position import get_memu_bounds
from utils.gemini_matcher import is_matching

topping1 = os.path.join(TOPPINGS_DIR, "topping1.png")
topping2 = os.path.join(TOPPINGS_DIR, "topping2.png")
topping3 = os.path.join(TOPPINGS_DIR, "topping3.png")
topping4 = os.path.join(TOPPINGS_DIR, "topping4.png")


def capture_center_picker_square():
    x_ratio = 0.422
    y_ratio = 0.32
    square_size = 150
    half = square_size / 2
    left, top, width, height = get_memu_bounds()
    center_x = int(left + width * x_ratio)
    center_y = int(top + height * y_ratio)

    region = {
        "left": int(center_x - half),
        "top": int(center_y - half),
        "width": square_size,
        "height": square_size,
    }

    with mss.mss() as sct:
        img = np.array(sct.grab(region))

    output_path = os.path.join(DEBUG_DIR, f"topping_active.png")
    cv2.imwrite(output_path, img)
    return output_path


def swipe_topping_picker_left():
    x_ratio = 0.422
    y_ratio = 0.32
    swipe_offset_ratio = 0.09
    left, top, width, height = get_memu_bounds()
    center_x = int(left + width * x_ratio)
    center_y = int(top + height * y_ratio)
    swipe_x = int(center_x - width * swipe_offset_ratio)

    pyautogui.moveTo(center_x, center_y, duration=0.01)
    pyautogui.mouseDown()
    pyautogui.moveTo(swipe_x, center_y, duration=1)
    pyautogui.mouseUp()

    print(
        f"⬅️ Swiped topping picker left from ({center_x}, {center_y}) to ({swipe_x}, {center_y})"
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


import os
import time
import shutil

MATCHES_DIR = os.path.join(ROOT_DIR, "matches")
os.makedirs(MATCHES_DIR, exist_ok=True)  # Ensure the matches directory exists

def sanitize_filename_component(text, max_length=50):
    """
    Cleans and truncates a string to make it safe for use in filenames.
    Keeps only letters, numbers, and underscores.
    """
    safe = re.sub(r'\W+', '_', text)
    return safe[:max_length]


def select_ingredient(cropped_path, max_attempts=30, delay_between_swipes=0.1):
    """
    Repeatedly swipes the topping picker left until the captured image matches the target ingredient.
    Saves both the matched image and the target image to MATCHES_DIR.

    :param cropped_path: Path to the target cropped ingredient image
    :param max_attempts: Max number of swipes to attempt
    :param delay_between_swipes: Time to wait between swipes (in seconds)
    """
    for attempt in range(max_attempts):
        current_path = capture_center_picker_square()
        match_response = is_matching(current_path, cropped_path)

        if 'yes' in match_response:
            print(f"✅ Match found on attempt {attempt}: {current_path}")

            safe_match_response = sanitize_filename_component(match_response)

            current_dest = os.path.join(MATCHES_DIR, f"{safe_match_response}_current.png")
            target_dest = os.path.join(MATCHES_DIR, f"{safe_match_response}_target.png")

            shutil.copy(current_path, current_dest)
            shutil.copy(cropped_path, target_dest)

            print(f"📁 Current match saved to: {current_dest}")
            print(f"📁 Target image saved to: {target_dest}")
            return True

        print(f"❌ No match on attempt {attempt}, swiping... (response: {match_response})")
        swipe_topping_picker_left()
        time.sleep(delay_between_swipes)



    print("⚠️ Maximum attempts reached without finding a match.")
    return False


def main():
    # Choose the target topping image to search for
    print(os.getenv("GEMINI_API_KEY"))
    target_topping = topping4
    success = select_ingredient(target_topping)

    if success:
        print("🎯 Ingredient successfully selected!")
    else:
        print("❌ Ingredient not found.")

if __name__ == "__main__":
    main()