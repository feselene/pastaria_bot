import os
import sys
import time

CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "../"))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from utils.click_button import click_button

ASSETS_DIR = os.path.join(ROOT_DIR, "assets")
START_BUTTON_TEMPLATE = os.path.join(ASSETS_DIR, "cook_button_right.png")

def click_cook_button(retries=15, delay=0.5, threshold=0.85):
    print("🟢 Looking for COOK button...")

    for attempt in range(retries):
        if click_button(START_BUTTON_TEMPLATE, threshold=threshold):
            print("✅ COOK button clicked.")
            return True
        print(f"⏳ Attempt {attempt+1}/{retries} failed. Retrying...")
        time.sleep(delay)

    print("❌ Failed to click COOK button after retries.")
    return False
