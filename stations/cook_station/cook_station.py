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
from utils.parse_ticket import get_filtered_pasta_icon
from utils.click_button import click_from_assets, click_and_hold_from_assets

def run_cook_station():
    click_leftmost_plus_button()
    get_filtered_pasta_icon()
    time.sleep(1)
    click_jar()
    time.sleep(2)
    click_and_hold_from_assets("cook_boost.png", 19, threshold=0.8)
    stir()
    time.sleep(2)
    click_and_hold_from_assets("cook_boost.png", 19, threshold=0.8)
    click_from_assets("pot.png")
    time.sleep(13)
    drag_pasta_to_plate()


if __name__ == "__main__":
    run_cook_station()
