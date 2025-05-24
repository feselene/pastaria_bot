import os
import sys
import time

CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "../../"))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from stations.cook_station.click_jar import click_jar
from stations.cook_station.click_leftmost_cook_button import click_leftmost_plus_button
from stations.cook_station.drag_pasta_to_plate import drag_pasta_to_plate
from stations.cook_station.stir import stir
from utils.click_button import click_and_hold_from_assets, click_from_assets
from utils.parse_ticket import get_filtered_pasta_icon, get_filtered_pasta_icon2, is_bar_orange


def cook():
    if is_bar_orange():
        cook_orange()
    else:
        cook_green()


def cook_orange():
    time.sleep(2)
    click_and_hold_from_assets("cook_boost.png", 19, threshold=0.8)
    stir()
    click_and_hold_from_assets("cook_boost.png", 2, threshold=0.8)


def cook_green():
    time.sleep(2)
    click_and_hold_from_assets("cook_boost.png", 9, threshold=0.8)
    stir()
    time.sleep(2)
    click_and_hold_from_assets("cook_boost.png", 9, threshold=0.8)


def run_cook_station():
    click_leftmost_plus_button()
    get_filtered_pasta_icon()
    get_filtered_pasta_icon2()
    time.sleep(1)
    click_jar()
    cook()
    click_from_assets("pot.png")
    time.sleep(13)
    drag_pasta_to_plate()
    time.sleep(1)


if __name__ == "__main__":
    run_cook_station()
