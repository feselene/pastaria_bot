import os
import sys
import time

import cv2
import mss
import numpy as np
import pyautogui
from PIL import Image
from rembg import remove

CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "../../"))
DEBUG_DIR = os.path.join(ROOT_DIR, "debug")
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from stations.build_station.parse_topping import center_contains_x, is_box_empty
from utils.get_memu_position import get_memu_bounds

topping1 = os.path.join(DEBUG_DIR, "debug_topping1_raw.png")
topping2 = os.path.join(DEBUG_DIR, "debug_topping2_raw.png")
topping3 = os.path.join(DEBUG_DIR, "debug_topping3_raw.png")
topping4 = os.path.join(DEBUG_DIR, "debug_topping4_raw.png")


def capture_center_picker_square():
    x_ratio = 0.422
    y_ratio = 0.32
    square_size = 200
    half = square_size / 2
    left, top, width, height = get_memu_bounds()
    center_x = int(left + width * x_ratio)
    center_y = int(top + height * y_ratio)

    region = {
        "left": center_x - half,
        "top": center_y - half,
        "width": square_size,
        "height": square_size,
    }

    with mss.mss() as sct:
        img = np.array(sct.grab(region))

    # Save the captured region
    output_path = os.path.join(DEBUG_DIR, f"topping_picker_center_{square_size}x{square_size}.png")
    cv2.imwrite(output_path, img)
    print(f"✅ Saved {square_size}x{square_size} picker center to {output_path}")
    return output_path


def swipe_topping_picker_left():
    x_ratio = 0.422
    y_ratio = 0.32
    swipe_offset_ratio = 0.1
    left, top, width, height = get_memu_bounds()
    center_x = int(left + width * x_ratio)
    center_y = int(top + height * y_ratio)
    swipe_x = int(center_x - width * swipe_offset_ratio)
    pyautogui.moveTo(center_x, center_y, duration=0.05)
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


def compute_orb_similarity(img1, img2, distance_threshold=50):
    """
    Computes the ORB match ratio between two images.
    """
    orb = cv2.ORB_create()
    kp1, des1 = orb.detectAndCompute(img1, None)
    kp2, des2 = orb.detectAndCompute(img2, None)

    if des1 is None or des2 is None or len(des1) == 0 or len(des2) == 0:
        return 0.0

    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(des1, des2)

    if not matches:
        return 0.0

    good_matches = [m for m in matches if m.distance < distance_threshold]
    match_ratio = len(good_matches) / len(matches)
    return match_ratio


def select_ingredient(cropped_path, threshold=0.2, max_attempts=1):
    """
    Scrolls through the topping picker until the cropped image is found using ORB feature matching.

    Parameters:
        cropped_path (str): Path to the template image.
        threshold (float): ORB match ratio threshold.
        max_attempts (int): Max swipes before giving up.

    Returns:
        bool: True if match found, False otherwise.
    """
    template = cv2.imread(cropped_path)
    if template is None:
        raise FileNotFoundError(f"Template not found: {cropped_path}")

    for attempt in range(max_attempts):
        output_path = capture_center_picker_square()
        search_img = cv2.imread(output_path)
        if search_img is None:
            continue

        match_ratio = compute_orb_similarity(template, search_img)
        print(f"🔍 Attempt {attempt + 1}: ORB Match Ratio = {match_ratio:.3f}")

        if match_ratio >= threshold:
            print("✅ Ingredient match found via ORB!")
            return True

        swipe_topping_picker_left()
        time.sleep(0.6)  # Give UI time to update

    print("❌ Failed to find ingredient after max attempts.")
    return False