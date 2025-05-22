import cv2
import numpy as np
import os
import sys

CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "../../"))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

DEBUG_DIR = os.path.join(ROOT_DIR, "debug")
os.makedirs(DEBUG_DIR, exist_ok=True)

import pyautogui
from utils.get_memu_position import get_memu_bounds

def click_center_topping_picker():
    # Relative ratios (from previous calculation)
    x_ratio = 0.422
    y_ratio = 0.32

    # Get MEmu window bounds
    left, top, width, height = get_memu_bounds()

    # Calculate absolute coordinates
    center_x = int(left + width * x_ratio)
    center_y = int(top + height * y_ratio)

    # Move and click
    pyautogui.moveTo(center_x, center_y, duration=0.2)
    pyautogui.click()

    print(f"✅ Clicked center of topping picker at ({center_x}, {center_y})")

def swipe_topping_picker_left():
    # Center picker ratios (based on earlier calculation)
    x_ratio = 0.422
    y_ratio = 0.32

    # Swipe range (in screen ratio terms)
    swipe_offset_ratio = 0.075  # 10% of window width to the left

    # Get emulator bounds
    left, top, width, height = get_memu_bounds()

    # Compute swipe coordinates
    center_x = int(left + width * x_ratio)
    center_y = int(top + height * y_ratio)
    swipe_x = int(center_x - width * swipe_offset_ratio)

    # Perform fast swipe (drag)
    pyautogui.moveTo(center_x, center_y, duration=0.05)
    pyautogui.mouseDown()
    pyautogui.moveTo(swipe_x, center_y, duration=0.6)
    pyautogui.mouseUp()

    print(f"⬅️ Swiped topping picker left from ({center_x}, {center_y}) to ({swipe_x}, {center_y})")

# Example usage
if __name__ == "__main__":
    swipe_topping_picker_left()

