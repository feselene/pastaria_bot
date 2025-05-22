import os
import sys
import time

CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "../../"))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from stations.bread_station.click_bread_button import click_bread_button
from stations.bread_station.get_conveyor_bounds import get_conveyor_bounds
from stations.bread_station.drag_bread_to_oven import drag_bread_to_oven
from stations.bread_station.drag_cooked_bread_to_plate import drag_bread_to_plate
from stations.bread_station.drag_ticket_to_green import drag_ticket_to_green
from utils.parse_ticket import get_filtered_bread_icon

def run_bread_station():
    click_bread_button()

    # Stores bread icon in debug folder
    bread_img = get_filtered_bread_icon()

    # Detect the brown conveyor belt region on screen
    conveyor_x, conveyor_y, conveyor_w, conveyor_h = get_conveyor_bounds()
    print(f"📦 Conveyor bounds: x={conveyor_x}, y={conveyor_y}, w={conveyor_w}, h={conveyor_h}")

    # TODO:
    # 1. Crop conveyor region from screenshot using bounds
    # 2. Match bread_img within conveyor crop
    # 3. Move mouse to matched bread center
    # 4. Drag to left-side conveyor slot

def run_random():
    click_bread_button()
    time.sleep(1)
    drag_bread_to_oven()
    time.sleep(25)
    drag_bread_to_plate()
    time.sleep(0.5)
    drag_ticket_to_green()

if __name__ == "__main__":
    run_random()
    # run_bread_station()
