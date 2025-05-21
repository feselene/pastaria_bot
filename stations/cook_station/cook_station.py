import os
import sys
import cv2
import numpy as np
import pyautogui
from time import sleep

# Setup root imports
CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "../../"))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from stations.cook_station.click_leftmost_cook_button import click_leftmost_plus_button
from utils.detect_ticket_from_template import detect_ticket_from_template
from utils.get_memu_position import get_memu_bounds
import mss


def crop_ticket_regions(ticket_img):
    h, w = ticket_img.shape[:2]
    return {
        "order":     ticket_img[int(0.0000*h):int(0.1094*h), :],  # 0–62
        "bread":     ticket_img[int(0.1094*h):int(0.2575*h), :],  # 62–146
        "topping1":  ticket_img[int(0.2575*h):int(0.3687*h), :],  # 146–209
        "topping2":  ticket_img[int(0.3687*h):int(0.4746*h), :],  # 209–269
        "topping3":  ticket_img[int(0.4746*h):int(0.5804*h), :],  # 269–329
        "topping4":  ticket_img[int(0.5804*h):int(0.6862*h), :],  # 329–389
        "sauce":     ticket_img[int(0.6862*h):int(0.7921*h), :],  # 389–449
        "pasta":     ticket_img[int(0.7921*h):int(0.9273*h), :],  # 449–526
        "doneness":  ticket_img[int(0.9273*h):int(1.0000*h), :]   # 526–567
    }


def capture_full_screen():
    with mss.mss() as sct:
        monitor = sct.monitors[1]  # Adjust if needed
        screenshot = np.array(sct.grab(monitor))
        return screenshot, monitor["left"], monitor["top"]


def match_and_click_icon(ticket_icon, screen, offset_x=0, offset_y=0, threshold=0.85):
    ticket_gray = cv2.cvtColor(ticket_icon, cv2.COLOR_BGR2GRAY)
    screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

    result = cv2.matchTemplate(screen_gray, ticket_gray, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    if max_val >= threshold:
        h, w = ticket_gray.shape
        center_x = offset_x + max_loc[0] + w // 2
        center_y = offset_y + max_loc[1] + h // 2
        pyautogui.moveTo(center_x, center_y)
        pyautogui.click()
        print(f"✅ Clicked matching jar icon at ({center_x}, {center_y}) with confidence {max_val:.2f}")
        return True
    else:
        print(f"❌ No match found for jar icon. Confidence was {max_val:.2f}")
        return False


def run_cook_station():
    print("🍳 Opening pot...")
    click_leftmost_plus_button()
    sleep(0.3)

    print("🎟️ Detecting ticket...")
    ticket_img = detect_ticket_from_template()
    if ticket_img is None:
        print("❌ Ticket detection failed.")
        return

    # 💾 Save full ticket for debug
    cv2.imwrite("debug_ticket.png", ticket_img)

    print("✂️ Cropping ticket regions...")
    regions = crop_ticket_regions(ticket_img)

    # 🖨️ Print and save each region
    for name, region_img in regions.items():
        print(f"📦 Region: {name}, shape: {region_img.shape}")
        cv2.imwrite(f"debug_{name}.png", region_img)

    pasta_icon = regions["pasta"]

    print("🖥️ Capturing screen for jar match...")
    screen, offset_x, offset_y = capture_full_screen()

    print("🎯 Matching and clicking correct jar...")
    match_and_click_icon(pasta_icon, screen, offset_x, offset_y)


if __name__ == "__main__":
    run_cook_station()
