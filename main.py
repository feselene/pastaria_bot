import os
import sys
import time

from utils.click_build_button import click_build_button

CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "./"))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

# Import station modules
from stations.order_station import order_station
from stations.cook_station import cook_station
from stations.build_station import build_station
from stations.bread_station import bread_station
from utils.click_cook_button import click_cook_button
from utils.click_build_button import click_build_button
from utils.click_start_button import click_start_button

def main():
    click_start_button()
    time.sleep(20)

    for i in range(6):
        print("▶️ Running Order Station...")
        order_station.run_order_station()
        click_cook_button()

        print("🔥 Running Cook Station...")
        time.sleep(1)
        cook_station.run_cook_station()
        click_build_button()

        print("🍝 Running Build Station...")
        time.sleep(1)
        build_station.run_build_station()

        print("🍞 Running Bread Station...")
        time.sleep(1)
        bread_station.run_bread_station()
        time.sleep(12)

if __name__ == "__main__":
    main()
