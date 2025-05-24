import os
import sys
import time

CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "../../"))
ASSETS_DIR = os.path.join(ROOT_DIR, "assets")
TEMPLATE_DIR = os.path.join(ASSETS_DIR, "take_order_template.png")
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from stations.order_station.click_take_order import click_take_order
from utils.button_visible import button_visible

def run_order_station():
    print("⏳ Waiting for button to become visible...")
    while not button_visible(TEMPLATE_DIR):
        time.sleep(1)

    print("✅ Button is visible. Starting order loop.")

    # While button remains visible, keep clicking and waiting
    while button_visible(TEMPLATE_DIR):
        click_take_order()
        print("🖱️ Clicked 'Take Order'. Waiting 15s...")
        time.sleep(10)

    print("🛑 Button no longer visible. Stopping.")


if __name__ == "__main__":
    run_order_station()
