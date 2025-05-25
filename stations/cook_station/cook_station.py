import os
import sys
import time

CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "../../"))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from stations.cook_station.click_leftmost_ticket import click_leftmost_ticket
from utils.click_button import (
    click_and_hold_ratios,
    click_button,
    click_ratios,
    drag_ratios,
)
from utils.parse_ticket import (
    get_filtered_pasta_icon,
    get_filtered_pasta_icon2,
    is_bar_orange,
)


def stir():
    drag_ratios(0.3, 0.8, 0.1, 0.5)


def drag_pasta_to_plate():
    drag_ratios(0.11, 0.28, 0.616, 0.86)


def cook_boost(n):
    boost_button_x = 0.11
    boost_button_y = 0.736
    click_and_hold_ratios(boost_button_x, boost_button_y, n)


def cook():
    if is_bar_orange():
        cook_orange()
    else:
        cook_green()


def cook_orange():
    time.sleep(2)
    cook_boost(19)
    stir()
    time.sleep(2)
    cook_boost(2)


def cook_green():
    time.sleep(2)
    cook_boost(9)
    stir()
    time.sleep(2)
    cook_boost(8)


def run_cook_station():
    click_leftmost_ticket()
    # Click right cooker
    click_ratios(0.1, 0.5)
    get_filtered_pasta_icon()
    get_filtered_pasta_icon2()
    time.sleep(1)
    click_button(os.path.join(ROOT_DIR, "debug", "pasta_logo.png"))
    cook()
    time.sleep(2)
    # Click pot
    click_ratios(0.1, 0.5)
    time.sleep(13)
    drag_pasta_to_plate()
    time.sleep(1)


if __name__ == "__main__":
    run_cook_station()
