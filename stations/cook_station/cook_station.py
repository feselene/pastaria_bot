import os
import sys
import time

CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "../../"))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from stations.cook_station.click_leftmost_cook_button import click_leftmost_plus_button
from utils.parse_ticket import get_filtered_pasta_icon
from click_leftmost_jar import click_jar
from stir import stir

def run_cook_station():
    click_leftmost_plus_button()
    get_filtered_pasta_icon()

def run_random():
    click_leftmost_plus_button()
    click_jar()
    time.sleep(5)
    stir()

if __name__ == "__main__":
    run_random()
