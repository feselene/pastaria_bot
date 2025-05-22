import os
import sys

CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "../../"))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from click_bread_button import click_bread_button
from utils.parse_ticket import get_filtered_bread_icon

def run_bread_station():
    click_bread_button()
    get_filtered_bread_icon()

if __name__ == "__main__":
    run_bread_station()
