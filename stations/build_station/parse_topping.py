import cv2
import numpy as np
import os

CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "../../"))
DEBUG_DIR = os.path.join(ROOT_DIR, "debug")
os.makedirs(DEBUG_DIR, exist_ok=True)

topping1 = os.path.join(DEBUG_DIR, "debug_topping1_raw.png")
topping2 = os.path.join(DEBUG_DIR, "debug_topping2_raw.png")
topping3 = os.path.join(DEBUG_DIR, "debug_topping3_raw.png")
topping4 = os.path.join(DEBUG_DIR, "debug_topping4_raw.png")

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

def check_blank_toppings():
    results = {}
    for i in range(1, 5):
        path = os.path.join(DEBUG_DIR, f"debug_topping{i}_raw.png")
        img = cv2.imread(path)
        is_blank = is_box_empty(img)
        results[f"topping{i}"] = is_blank
    return results

blank_status = check_blank_toppings()
print(blank_status)
# Output: {'topping1': False, 'topping2': True, ...}

