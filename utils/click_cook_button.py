import os
import sys
import time

CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "../"))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from utils.button_visible import button_visible
from utils.click_button import click_from_assets

ASSETS_DIR = os.path.join(ROOT_DIR, "assets")
COOK_BUTTON_TEMPLATE = os.path.join(ASSETS_DIR, "cook_button_right.png")


def click_cook_button():
    while not button_visible(COOK_BUTTON_TEMPLATE):
        time.sleep(1)

    click_from_assets("cook_button_right.png")


def main():
    click_cook_button()


if __name__ == "__main__":
    main()
