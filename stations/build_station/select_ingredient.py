import os
import sys

import cv2
import numpy as np

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


# Example usage
if __name__ == "__main__":
    click_center_topping_picker()
