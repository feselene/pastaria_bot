import os
import sys
import time

import cv2
import numpy as np
import pytesseract

CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "../../"))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)
DEBUG_DIR = os.path.join(ROOT_DIR, "debug")
TOPPINGS_DIR = os.path.join(ROOT_DIR, "toppings")
os.makedirs(DEBUG_DIR, exist_ok=True)
os.makedirs(TOPPINGS_DIR, exist_ok=True)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

from skimage.metrics import structural_similarity as ssim

from stations.build_station.apply import select_ingredient
from stations.build_station.apply_sauce import apply_shaker
from stations.build_station.click_plate import place_topping
from utils.detect_ticket_from_template import detect_ticket_from_template
from utils.parse_ticket import get_filtered_topping_icon
from utils.remove_background import remove_background_and_crop


def is_box_empty(img, tolerance=10, match_ratio=0.6):
    """
    Determines if a UI ingredient box is empty based on uniform color coverage.

    Parameters:
        img (np.ndarray): Input image (BGR).
        tolerance (int): Max per-channel difference from center pixel.
        match_ratio (float): Required fraction of pixels matching center pixel.

    Returns:
        bool: True if at least `match_ratio` of pixels match center pixel within `tolerance`.
    """
    if img is None:
        return True

    h, w = img.shape[:2]
    center_pixel = img[h // 2, w // 2]

    # Compute absolute channel-wise difference from center pixel
    diff = np.abs(img.astype(np.int16) - center_pixel.astype(np.int16))
    mask = np.all(diff <= tolerance, axis=2)

    # Calculate match ratio
    ratio = np.sum(mask) / (h * w)
    return ratio >= match_ratio


def crop_x_region(img):
    h, w = img.shape[:2]

    # Heuristic region: center 1/3rd
    start_x = int(w * 0.39)
    end_x = int(w * 0.6)
    start_y = int(h * 0.08)
    end_y = int(h * 0.88)

    cropped = img[start_y:end_y, start_x:end_x]
    return cropped


def center_contains_x(img):
    # Crop the X region from the input
    img = crop_x_region(img)

    # Load reference image
    reference_path = r"C:\Users\ceo\IdeaProjects\pastaria_bot\assets\x.png"
    reference = cv2.imread(reference_path)

    if reference is None:
        raise FileNotFoundError(f"Reference image not found at {reference_path}")

    # Resize input to match reference if needed
    if img.shape[:2] != reference.shape[:2]:
        img = cv2.resize(img, (reference.shape[1], reference.shape[0]))

    # Convert to grayscale
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ref_gray = cv2.cvtColor(reference, cv2.COLOR_BGR2GRAY)

    # Compute SSIM
    score, _ = ssim(img_gray, ref_gray, full=True)

    return score > 0.5


def process_topping_boxes():
    for i in range(4, 0, -1):
        image_path = os.path.join(DEBUG_DIR, f"topping{i}.png")
        img = cv2.imread(image_path)

        if is_box_empty(img):
            print(image_path + " is an empty box.")
            continue
        elif center_contains_x(img):
            print(image_path + " is an ingredient.")
            time.sleep(2)
            apply_ingredient(image_path)
        else:
            print(image_path + " is a sauce.")
            time.sleep(2)
            apply_shaker(image_path)


import cv2


def extract_digit(image_path):
    image = cv2.imread(image_path)

    # Resize for better OCR accuracy
    image = cv2.resize(image, None, fx=4, fy=4, interpolation=cv2.INTER_LINEAR)

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Increase contrast and threshold
    _, thresh = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY_INV)

    # Tesseract config
    config = r"--psm 10 -c tessedit_char_whitelist=0123456789"
    raw_result = pytesseract.image_to_string(thresh, config=config)
    cleaned = "".join(filter(str.isdigit, raw_result))

    # print(f"OCR Raw: {repr(raw_result)} | Cleaned: {cleaned}")
    return int(cleaned) if cleaned else None


def apply_ingredient(image_path):
    img = cv2.imread(image_path)
    basename = os.path.basename(image_path)
    numname = "num_" + basename
    h, w = img.shape[:2]
    cropped = img[:, : int(w * 0.45)]
    cropped_num = img[:, int(w * 0.65) : int(w * 0.875)]
    save_path = os.path.join(TOPPINGS_DIR, basename)
    save_path_num = os.path.join(TOPPINGS_DIR, numname)
    cv2.imwrite(save_path, cropped)
    remove_background_and_crop(save_path, save_path)
    cv2.imwrite(save_path_num, cropped_num)
    select_ingredient(save_path)
    num = extract_digit(save_path_num)
    place_topping(num)


def apply_shaker(image_path):
    img = cv2.imread(image_path)
    basename = os.path.basename(image_path)
    h, w = img.shape[:2]
    cropped = img[int(h * 0.05) : int(h * 0.92), int(w * 0.38) : int(w * 0.61)]
    save_path = os.path.join(TOPPINGS_DIR, basename)
    cv2.imwrite(save_path, cropped)
    select_ingredient(save_path)
    time.sleep(0.5)
    apply_shaker()


def main():
    print("🎟️ Detecting ticket...")
    ticket_img = detect_ticket_from_template()
    if ticket_img is None:
        print("❌ Ticket detection failed.")
        return

    debug_ticket_path = os.path.join(DEBUG_DIR, "ticket.png")
    cv2.imwrite(debug_ticket_path, ticket_img)
    get_filtered_topping_icon(1)
    get_filtered_topping_icon(2)
    get_filtered_topping_icon(3)
    get_filtered_topping_icon(4)
    process_topping_boxes()


if __name__ == "__main__":
    main()
