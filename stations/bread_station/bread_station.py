import os
import sys
import time

CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "../../"))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from stations.bread_station.click_bread import click_bread
from utils.click_button import (
    click_and_hold_ratios,
    click_ratios,
    drag_ratios
)
from utils.parse_ticket import get_filtered_bread_icon

def drag_bread_to_oven():
    click_ratios(0.434, 0.258)
    get_filtered_bread_icon()
    time.sleep(1.5)
    click_bread()


def submit_bread_and_ticket():
    drag_ratios()
    time.sleep(0.5)
    drag_ratios(0.9, 0.5, 0.2, 0.7)


def bread_boost(n):
    click_and_hold_ratios(0.035, 0.465, n)


if __name__ == "__main__":
    drag_bread_to_oven()
