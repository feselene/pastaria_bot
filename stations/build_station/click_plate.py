import pyautogui
import time
import os
import sys

# Add root to sys.path so we can import project utilities
CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "../../"))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from utils.get_memu_position import get_memu_bounds


def click_plate():
    left, top, width, height = get_memu_bounds()
    x = left + width // 2
    y = top + int(height * 2 / 3)

    print(f"🖱️ Clicking inside MEMU at ({x}, {y})...")
    pyautogui.moveTo(x, y, duration=0.2)
    pyautogui.click()


if __name__ == "__main__":
    time.sleep(1)  # Delay to allow user to switch to MEMU
    click_plate()
