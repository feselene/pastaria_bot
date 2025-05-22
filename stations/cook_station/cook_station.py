import os
import sys

CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "../../"))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from stations.cook_station.click_leftmost_cook_button import click_leftmost_plus_button
from utils.parse_ticket import get_filtered_pasta_icon

def run_cook_station():
    click_leftmost_plus_button()
    get_filtered_pasta_icon()

if __name__ == "__main__":
    run_cook_station()
