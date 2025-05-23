import os
import sys
import cv2
import numpy as np

CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "../../"))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)
DEBUG_DIR = os.path.join(ROOT_DIR, "debug")
TOPPINGS_DIR = os.path.join(ROOT_DIR, "toppings")
os.makedirs(DEBUG_DIR, exist_ok=True)
os.makedirs(TOPPINGS_DIR, exist_ok=True)

from skimage.metrics import structural_similarity as ssim
from utils.parse_ticket import get_filtered_topping_icon

from utils.remove_background import remove_background_and_crop
from utils.detect_ticket_from_template import detect_ticket_from_template

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
    for i in range(1, 5):
        image_path = os.path.join(DEBUG_DIR, f"topping{i}.png")
        img = cv2.imread(image_path)

        if is_box_empty(img):
            print(image_path + "is empty")
            continue
        elif center_contains_x(img):
            print(image_path + "contains x")
            apply_ingredient(image_path)
        else:
            print(image_path + "is a sauce")
            apply_sauce(image_path)


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


def apply_sauce(image_path):
    img = cv2.imread(image_path)
    basename = os.path.basename(image_path)
    h, w = img.shape[:2]
    crop_width = int(w * 0.25)
    start_x = (w - crop_width) // 2
    end_x = start_x + crop_width
    cropped = img[:, start_x:end_x]
    save_path = os.path.join(TOPPINGS_DIR, basename)
    cv2.imwrite(save_path, cropped)


def main():
    print("🎟️ Detecting ticket...")
    ticket_img = detect_ticket_from_template()
    if ticket_img is None:
        print("❌ Ticket detection failed.")
        return

    debug_ticket_path = os.path.join(DEBUG_DIR, "debug_ticket.png")
    cv2.imwrite(debug_ticket_path, ticket_img)
    get_filtered_topping_icon(1)
    get_filtered_topping_icon(2)
    get_filtered_topping_icon(3)
    get_filtered_topping_icon(4)
    process_topping_boxes()


if __name__ == "__main__":
    main()