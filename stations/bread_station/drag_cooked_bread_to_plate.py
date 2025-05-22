import os
import sys
import time

# Setup root imports
CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "../.."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)
ASSETS_DIR = os.path.join(ROOT_DIR, "assets")
BREAD_PATH = os.path.join(ASSETS_DIR, "bread_cooked.png")
PLATE_PATH = os.path.join(ASSETS_DIR, "cooked_plate.png")

from utils.click_button import click_button
from utils.drag import drag_between_templates

# Define path to assets
ASSETS_DIR = os.path.join(ROOT_DIR, "assets")

def drag_bread_to_plate():
    drag_between_templates(BREAD_PATH, PLATE_PATH, threshold=0.85)

if __name__ == "__main__":
    drag_bread_to_plate()
