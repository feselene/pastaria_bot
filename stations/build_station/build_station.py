import os
import sys
import time
from operator import truediv

CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "../../"))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from stations.build_station.apply_sauce import apply_sauce
from stations.build_station.click_jar import click_jar
from stations.build_station.parse_topping import process_topping_boxes
from utils.click_button import click_ratios
from utils.parse_ticket import get_filtered_sauce_icon, get_filtered_topping_icon


def run_build_station():
    get_filtered_sauce_icon()
    click_jar()
    apply_sauce()
    time.sleep(0.5)
    get_filtered_topping_icon(1)
    get_filtered_topping_icon(2)
    get_filtered_topping_icon(3)
    get_filtered_topping_icon(4)
    process_topping_boxes()
    time.sleep(5)
    # Click checkmark
    click_ratios(0.727, 0.782)


if __name__ == "__main__":
    run_build_station()
