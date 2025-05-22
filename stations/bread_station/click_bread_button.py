import os
import sys

# Setup root imports
CURRENT_DIR = os.path.dirname(__file__)  # .../stations/bread_station
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "../.."))  # .../pastaria_bot
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from utils.click_button import click_button

# Define path to assets
ASSETS_DIR = os.path.join(ROOT_DIR, "assets")
BREAD_BUTTON_TEMPLATE = os.path.join(ASSETS_DIR, "bread_button_template.png")

def click_bread_button():
    click_button(BREAD_BUTTON_TEMPLATE, threshold=0.80)

if __name__ == "__main__":
    click_bread_button()
