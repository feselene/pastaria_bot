import os
import sys

import cv2
import numpy as np

# Setup root imports from parse_ticket.py inside utils/
CURRENT_DIR = os.path.dirname(__file__)  # points to pastaria_bot/utils/
ROOT_DIR = os.path.abspath(
    os.path.join(CURRENT_DIR, "..")
)  # one level up to pastaria_bot/
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

DEBUG_DIR = os.path.join(ROOT_DIR, "debug")
os.makedirs(DEBUG_DIR, exist_ok=True)

from utils.detect_ticket_from_template import detect_ticket_from_template
from utils.parse_ticket import crop_ticket_regions
from utils.remove_background import crop, remove_background_and_crop


def is_bar_orange(threshold=0.2):
    print("🎟️ Detecting ticket...")
    ticket_img = detect_ticket_from_template()
    if ticket_img is None:
        print("❌ Ticket detection failed.")
        return

    debug_ticket_path = os.path.join(DEBUG_DIR, "ticket.png")
    cv2.imwrite(debug_ticket_path, ticket_img)

    print("✂️ Cropping ticket regions...")
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


def main():
    is_bar_orange()


if __name__ == "__main__":
    main()
