import os
import sys

import cv2

from utils.detect_ticket_from_template import detect_ticket_from_template
from utils.remove_background import crop, remove_background_and_crop

# Setup root imports from parse_ticket.py inside utils/
CURRENT_DIR = os.path.dirname(__file__)  # points to pastaria_bot/utils/
ROOT_DIR = os.path.abspath(
    os.path.join(CURRENT_DIR, "..")
)  # one level up to pastaria_bot/
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

DEBUG_DIR = os.path.join(ROOT_DIR, "debug")
os.makedirs(DEBUG_DIR, exist_ok=True)


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
    print("🎟️ Detecting ticket...")
    ticket_img = detect_ticket_from_template()
    if ticket_img is None:
        print("❌ Ticket detection failed.")
        return

    debug_ticket_path = os.path.join(DEBUG_DIR, "ticket.png")
    cv2.imwrite(debug_ticket_path, ticket_img)

    print("✂️ Cropping ticket regions...")
    regions = crop_ticket_regions(ticket_img)

    bread_img_bgr = regions["bread"]
    bread_img_path = os.path.join(ROOT_DIR, "debug", "debug_bread_raw.png")
    bread_out_path = os.path.join(ROOT_DIR, "debug", "debug_bread_cropped.png")

    os.makedirs(os.path.dirname(bread_img_path), exist_ok=True)
    cv2.imwrite(bread_img_path, bread_img_bgr)

    # ✅ Remove background and crop
    print("🔍 Removing background from bread icon...")
    remove_background_and_crop(bread_img_path, bread_out_path)
    print(f"✅ Bread icon saved to: {bread_out_path}")
    return bread_out_path


def get_filtered_pasta_icon():
    print("🎟️ Detecting ticket...")
    ticket_img = detect_ticket_from_template()
    if ticket_img is None:
        print("❌ Ticket detection failed.")
        return

    debug_ticket_path = os.path.join(DEBUG_DIR, "ticket.png")
    cv2.imwrite(debug_ticket_path, ticket_img)

    print("✂️ Cropping ticket regions...")
    regions = crop_ticket_regions(ticket_img)

    pasta_img_bgr = regions["pasta"]
    pasta_img_path = os.path.join(ROOT_DIR, "debug", "debug_pasta_raw.png")
    pasta_out_path = os.path.join(ROOT_DIR, "debug", "debug_pasta_cropped.png")

    os.makedirs(os.path.dirname(pasta_img_path), exist_ok=True)
    cv2.imwrite(pasta_img_path, pasta_img_bgr)

    # ✅ Remove background and crop
    print("🔍 Removing background from pasta icon...")
    remove_background_and_crop(pasta_img_path, pasta_out_path)
    print(f"✅ Pasta icon saved to: {pasta_out_path}")


def get_filtered_sauce_icon():
    print("🎟️ Detecting ticket...")
    ticket_img = detect_ticket_from_template()
    if ticket_img is None:
        print("❌ Ticket detection failed.")
        return

    debug_ticket_path = os.path.join(DEBUG_DIR, "ticket.png")
    cv2.imwrite(debug_ticket_path, ticket_img)

    print("✂️ Cropping ticket regions...")
    regions = crop_ticket_regions(ticket_img)

    sauce_img_bgr = regions["sauce"]
    sauce_img_path = os.path.join(ROOT_DIR, "debug", "sauce.png")
    sauce_out_path = os.path.join(ROOT_DIR, "debug", "sauce_icon.png")

    os.makedirs(os.path.dirname(sauce_img_path), exist_ok=True)
    cv2.imwrite(sauce_img_path, sauce_img_bgr)

    # ✅ Remove background and crop
    print("🔍 Removing background from sauce icon...")
    crop(sauce_img_path, sauce_out_path)
    print(f"✅ Sauce icon saved to: {sauce_out_path}")


def get_filtered_topping_icon(topping_number: int):
    region_key = f"topping{topping_number}"
    raw_filename = f"topping{topping_number}.png"

    print("🎟️ Detecting ticket...")
    ticket_img = detect_ticket_from_template()
    if ticket_img is None:
        print("❌ Ticket detection failed.")
        return

    debug_ticket_path = os.path.join(DEBUG_DIR, "ticket.png")
    cv2.imwrite(debug_ticket_path, ticket_img)

    print("✂️ Cropping ticket regions...")
    regions = crop_ticket_regions(ticket_img)

    if region_key not in regions:
        print(f"❌ Invalid topping number: {topping_number}")
        return

    topping_img_bgr = regions[region_key]
    raw_path = os.path.join(ROOT_DIR, "debug", raw_filename)

    os.makedirs(os.path.dirname(raw_path), exist_ok=True)
    cv2.imwrite(raw_path, topping_img_bgr)

    return raw_path
