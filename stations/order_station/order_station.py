import os
import sys

CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "../../"))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from click_take_order import click_take_order

def run_order_station():
    click_take_order()

if __name__ == "__main__":
    run_order_station()
