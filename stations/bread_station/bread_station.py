import os
import sys
import time

CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "../../"))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from stations.bread_station.click_bread import click_bread
from utils.parse_ticket import get_filtered_bread_icon
from utils.click_button import click_from_assets, click_and_hold_from_assets, drag_ratios

def run_bread_station():
    click_from_assets(filename="bread_menu.png")
    get_filtered_bread_icon()
    time.sleep(1)
    click_bread()
    click_and_hold_from_assets(filename="bread_boost.png", hold_duration=12, threshold=0.80)
    drag_ratios()
    time.sleep(0.5)
    drag_ratios(0.9, 0.5, 0.2, 0.7)

if __name__ == "__main__":
    run_bread_station()
