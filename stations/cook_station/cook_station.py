import os
import sys
import time

CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "../../"))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from utils.click_button import click_button
from utils.parse_ticket import get_filtered_pasta_icon, is_bar_orange


from utils.crop_screenshot_by_ratio import adb_tap_relative, adb_tap_and_hold_relative, adb_drag_relative

def stir():
    spoon_start_x = 0.31
    spoon_start_y = 0.86
    pot_x = 0.11
    pot_y = 0.35
    adb_drag_relative(spoon_start_x, spoon_start_y, pot_x, pot_y)


def drag_pasta_to_plate():
    cooked_pasta_start_x = 0.11
    cooked_pasta_start_y = 0.25
    plate_x = 0.63
    plate_y = 0.9
    adb_drag_relative(cooked_pasta_start_x, cooked_pasta_start_y, plate_x, plate_y)


def cook_boost(n):
    boost_button_x = 0.11
    boost_button_y = 0.736
    adb_tap_and_hold_relative(boost_button_x, boost_button_y, n)


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
    cook_boost(15)


def cook_green():
    time.sleep(2)
    cook_boost(9)
    stir()
    time.sleep(2)
    cook_boost(8)


def run_cook_station():
    pot_x = 0.11
    pot_y = 0.48
    adb_tap_relative(pot_x, pot_y)
    get_filtered_pasta_icon()
    time.sleep(1)
    click_button(os.path.join(ROOT_DIR, "debug", "pasta_logo.png"), threshold=0.7)
    cook()
    time.sleep(2)
    adb_tap_relative(pot_x, pot_y)
    time.sleep(13)
    drag_pasta_to_plate()
    time.sleep(1)


if __name__ == "__main__":
    run_cook_station()
