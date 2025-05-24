import os
import sys
import time

CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "../../"))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from utils.click_button import click_button

ASSETS_DIR = os.path.join(ROOT_DIR, "assets")
TAKE_ORDER_TEMPLATE = os.path.join(ASSETS_DIR, "take_order_template.png")


def click_take_order(retries=10, delay=0.5, threshold=0.7):
    for attempt in range(retries):
        clicked = click_button(TAKE_ORDER_TEMPLATE, threshold=threshold)
        if clicked:
            return True
        time.sleep(delay)
    print("❌ Failed to click TAKE ORDER after retries.")
    return False


if __name__ == "__main__":
    click_take_order()
