import os
import sys
import time
from operator import truediv

CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "../../"))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from stations.build_station.apply_sauce import apply_sauce
from stations.build_station.click_checkmark import click_checkmark
from stations.build_station.click_jar import click_jar
from stations.build_station.click_tomato_jar import click_tomato_jar
from utils.parse_ticket import get_filtered_sauce_icon, get_filtered_topping_icon


def get_filtered_toppings():
    get_filtered_topping_icon(1)
    get_filtered_topping_icon(2)
    get_filtered_topping_icon(3)
    get_filtered_topping_icon(4)


def run_random():
    click_tomato_jar()
    apply_sauce()
    time.sleep(0.5)
    click_checkmark()


if __name__ == "__main__":
    get_filtered_toppings()
