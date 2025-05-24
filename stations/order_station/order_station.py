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
    while not button_visible(TEMPLATE_DIR):
        time.sleep(1)
        if button_visible(os.path.join(ASSETS_DIR, "closed.png"), threshold=0.8):
            print("seen closed, returning. ")
            return
        if button_visible(os.path.join(ASSETS_DIR, "skip_button_left.png"), threshold=0.8):
            print("seen skip_button_left, returning.")
            return

    while button_visible(TEMPLATE_DIR):
        click_take_order()
        time.sleep(10)


if __name__ == "__main__":
    run_order_station()
