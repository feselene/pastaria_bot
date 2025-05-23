import os
import sys
import time

CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "../../"))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from stations.bread_station.click_bread import click_bread
from stations.bread_station.click_bread_button import click_bread_button
from stations.bread_station.drag_bread_to_oven import drag_bread_to_oven
from stations.bread_station.drag_cooked_bread_to_plate import drag_bread_to_plate
from stations.bread_station.drag_ticket_to_green import drag_ticket_to_green
from stations.bread_station.get_conveyor_bounds import get_conveyor_bounds
from stations.bread_station.click_boost import click_boost
from utils.parse_ticket import get_filtered_bread_icon


def run_bread_station():
    click_bread_button()
    get_filtered_bread_icon()
    time.sleep(1)
    click_bread()
    click_boost()
    drag_bread_to_plate()
    time.sleep(0.5)
    drag_ticket_to_green()


def run_random():
    click_bread_button()
    time.sleep(1)
    drag_bread_to_oven()
    time.sleep(25)
    drag_bread_to_plate()
    time.sleep(0.5)
    drag_ticket_to_green()


if __name__ == "__main__":
    run_bread_station()
