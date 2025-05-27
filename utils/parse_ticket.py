import os
import sys

import cv2
import numpy as np
from PIL import Image

from utils.crop_screenshot_by_ratio import crop_screenshot_as_numpy
from utils.remove_background import crop, remove_background_and_crop

CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
DEBUG_DIR = os.path.join(ROOT_DIR, "debug")

if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

os.makedirs(DEBUG_DIR, exist_ok=True)

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

def detect_ticket_from_template():
    if is_box_empty(crop_screenshot_as_numpy(0.851, 0.6975, 0.9931, 0.7647)):
        return load_special_asset_as_numpy()
    return crop_screenshot_as_numpy(0.845, 0.132, 1, 0.8185)

def detect_bread_from_template():
    return crop_screenshot_as_numpy(0.845, 0.132, 1, 0.8185)

def load_special_asset_as_numpy():
    path = os.path.join("assets", "special.png")

    # Load with PIL and convert to RGB
    image = Image.open(path).convert("RGB")

    # Convert to NumPy array and then to BGR for OpenCV
    img_rgb = np.array(image)
    img_bgr = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)

    return img_bgr

def is_bar_orange(threshold=0.1):
    ticket_img = detect_ticket_from_template()
    debug_ticket_path = os.path.join(DEBUG_DIR, "ticket.png")
    cv2.imwrite(debug_ticket_path, ticket_img)

    regions = crop_ticket_regions(ticket_img)
    img = regions["doneness"]

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Define orange hue range
    lower_orange = np.array([10, 100, 100])
    upper_orange = np.array([25, 255, 255])

    # Mask and ratio
    mask = cv2.inRange(hsv, lower_orange, upper_orange)
    orange_ratio = np.sum(mask > 0) / (img.shape[0] * img.shape[1])

    print(f"🍊 Orange pixel ratio: {orange_ratio:.2f}")
    return orange_ratio >= threshold


def crop_ticket_regions(ticket_img):
    h, w = ticket_img.shape[:2]
    return {
        "order": ticket_img[int(0.0000 * h) : int(0.1094 * h), :],
        "bread": ticket_img[int(0.1094 * h) : int(0.2575 * h), :],
        "topping1": ticket_img[int(0.2575 * h) : int(0.3687 * h), :],
        "topping2": ticket_img[int(0.3687 * h) : int(0.4746 * h), :],
        "topping3": ticket_img[int(0.4746 * h) : int(0.5804 * h), :],
        "topping4": ticket_img[int(0.5804 * h) : int(0.6862 * h), :],
        "sauce": ticket_img[int(0.6862 * h) : int(0.7921 * h), :],
        "pasta": ticket_img[int(0.7921 * h) : int(0.9273 * h), :],
        "doneness": ticket_img[int(0.9273 * h) : int(1.0000 * h), :],
    }


def get_filtered_bread_icon():
    ticket_img = detect_bread_from_template()
    debug_ticket_path = os.path.join(DEBUG_DIR, "ticket.png")
    cv2.imwrite(debug_ticket_path, ticket_img)
    regions = crop_ticket_regions(ticket_img)

    bread_img_bgr = regions["bread"]
    bread_img_path = os.path.join(ROOT_DIR, "debug", "bread.png")
    bread_out_path = os.path.join(ROOT_DIR, "debug", "bread_icon.png")

    os.makedirs(os.path.dirname(bread_img_path), exist_ok=True)
    cv2.imwrite(bread_img_path, bread_img_bgr)
    remove_background_and_crop(bread_img_path, bread_out_path)

    return bread_out_path

def read_pasta_on_ticket():
    ticket_img = detect_ticket_from_template()
    debug_ticket_path = os.path.join(DEBUG_DIR, "ticket.png")
    cv2.imwrite(debug_ticket_path, ticket_img)
    regions = crop_ticket_regions(ticket_img)

    pasta_img_bgr = regions["pasta"]
    pasta_img_path = os.path.join(ROOT_DIR, "debug", "debug_pasta_raw.png")
    pasta_out_path = os.path.join(ROOT_DIR, "debug", "pasta.png")

    os.makedirs(os.path.dirname(pasta_img_path), exist_ok=True)
    cv2.imwrite(pasta_img_path, pasta_img_bgr)

    remove_background_and_crop(pasta_img_path, pasta_out_path)

def get_filtered_pasta_icon():
    read_pasta_on_ticket()
    pasta_out_path = os.path.join(ROOT_DIR, "debug", "pasta.png")
    circle_path = os.path.join(ROOT_DIR, "assets", "circle.png")
    output_path = os.path.join(ROOT_DIR, "debug", "pasta_logo.png")

    # Open images
    pasta_img = Image.open(pasta_out_path).convert("RGBA")
    circle_img = Image.open(circle_path).convert("RGBA")

    # Resize pasta image by 0.75
    new_size = (int(pasta_img.width * 0.75), int(pasta_img.height * 0.75))
    pasta_img_resized = pasta_img.resize(new_size, Image.Resampling.LANCZOS)

    # Calculate position to center the pasta on the circle
    x_offset = (circle_img.width - pasta_img_resized.width) // 2
    y_offset = (circle_img.height - pasta_img_resized.height) // 2

    # Paste resized pasta onto the circle
    result_img = circle_img.copy()
    result_img.paste(pasta_img_resized, (x_offset, y_offset), pasta_img_resized)

    # Save result
    result_img.save(output_path)


def get_filtered_sauce_icon():
    ticket_img = detect_ticket_from_template()
    debug_ticket_path = os.path.join(DEBUG_DIR, "ticket.png")
    cv2.imwrite(debug_ticket_path, ticket_img)
    regions = crop_ticket_regions(ticket_img)

    sauce_img_bgr = regions["sauce"]
    sauce_img_path = os.path.join(ROOT_DIR, "debug", "sauce.png")
    sauce_out_path = os.path.join(ROOT_DIR, "debug", "sauce_icon.png")

    os.makedirs(os.path.dirname(sauce_img_path), exist_ok=True)
    cv2.imwrite(sauce_img_path, sauce_img_bgr)

    crop(sauce_img_path, sauce_out_path)


def get_filtered_topping_icon(topping_number: int):
    region_key = f"topping{topping_number}"
    raw_filename = f"topping{topping_number}.png"

    ticket_img = detect_ticket_from_template()
    debug_ticket_path = os.path.join(DEBUG_DIR, "ticket.png")
    cv2.imwrite(debug_ticket_path, ticket_img)
    regions = crop_ticket_regions(ticket_img)

    if region_key not in regions:
        print(f"❌ Invalid topping number: {topping_number}")
        return

    topping_img_bgr = regions[region_key]
    raw_path = os.path.join(ROOT_DIR, "debug", raw_filename)

    os.makedirs(os.path.dirname(raw_path), exist_ok=True)
    cv2.imwrite(raw_path, topping_img_bgr)

    return raw_path


def main():
    get_filtered_sauce_icon()


if __name__ == "__main__":
    main()
