import os
import sys

CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "../../"))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from click_bread_button import click_bread_button
from utils.parse_ticket import get_filtered_bread_icon
from get_conveyor_bounds import get_conveyor_bounds

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

if __name__ == "__main__":
    run_bread_station()
