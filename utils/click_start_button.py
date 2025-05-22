import os
import sys
import time

CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "../"))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from utils.click_button import click_button

ASSETS_DIR = os.path.join(ROOT_DIR, "assets")
START_BUTTON_TEMPLATE = os.path.join(ASSETS_DIR, "start_button_template.png")


def click_start_button(retries=10, delay=0.5, threshold=0.85):
    print("🟢 Looking for START button...")
    for attempt in range(retries):
        if click_button(START_BUTTON_TEMPLATE, threshold=threshold):
            print("✅ START button clicked.")
            return True
        time.sleep(delay)
    print("❌ Failed to click START button after retries.")
    return False


if __name__ == "__main__":
    click_start_button()
