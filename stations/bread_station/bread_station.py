import os
import sys
import time

CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "../../"))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from stations.bread_station.click_bread import click_bread
from utils.parse_ticket import get_filtered_bread_icon

from utils.crop_screenshot_by_ratio import adb_tap_relative, adb_tap_and_hold_relative, adb_drag_relative

def drag_bread_to_oven():
    bread_menu_x = 0.445
    bread_menu_y = 0.21
    adb_tap_relative(bread_menu_x, bread_menu_y)
    get_filtered_bread_icon()
    time.sleep(1.5)
    click_bread()


def submit_bread_and_ticket():
    oven_x = 0.74
    oven_y = 0.44
    plate_x = 0.45
    plate_y = 0.6
    adb_drag_relative(oven_x, oven_y, plate_x, plate_y)
    time.sleep(0.5)
    ticket_x = 0.924
    ticket_y = 0.48
    drag_ticket_here_x = 0.21
    drag_ticket_here_y = 0.73
    adb_drag_relative(ticket_x, ticket_y, drag_ticket_here_x, drag_ticket_here_y)


def bread_boost(n):
    boost_button_x = 0.036
    boost_button_y = 0.45
    adb_tap_and_hold_relative(boost_button_x, boost_button_y, n)


if __name__ == "__main__":
    drag_bread_to_oven()
