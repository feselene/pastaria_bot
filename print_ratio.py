import os
import sys
import time

import pyautogui
import pygetwindow as gw

CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = CURRENT_DIR
DEBUG_DIR = os.path.join(ROOT_DIR, "debug")
TOPPINGS_DIR = os.path.join(ROOT_DIR, "toppings")
MATCHES_DIR = os.path.join(ROOT_DIR, "matches")
os.makedirs(MATCHES_DIR, exist_ok=True)

if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from dotenv import load_dotenv
load_dotenv()
ADB_PATH = os.getenv("ADB_PATH")


def print_pointer_ratio_in_memu():
    try:
        memu_window = None
        for window in gw.getWindowsWithTitle("MEmu"):
            if window.visible and window.width > 0 and window.height > 0:
                memu_window = window
                break

        if not memu_window:
            raise RuntimeError("❌ No visible MEmu window found.")

        left, top, width, height = (
            memu_window.left,
            memu_window.top,
            memu_window.width,
            memu_window.height,
        )

        print("🎯 Move your mouse over the MEmu window. Press Ctrl+C to stop.\n")
        while True:
            x, y = pyautogui.position()
            if left <= x < left + width and top <= y < top + height:
                rel_x = (x - left) / width
                rel_y = (y - top) / height
                print(f"📍 Mouse Ratio: x={rel_x:.3f}, y={rel_y:.3f}", end="\r")
            else:
                print(
                    "⛔ Mouse outside MEmu window.                         ", end="\r"
                )

            time.sleep(0.05)

    except KeyboardInterrupt:
        print("\n✅ Done.")


def main():
    print_pointer_ratio_in_memu()


if __name__ == "__main__":
    print_pointer_ratio_in_memu()
