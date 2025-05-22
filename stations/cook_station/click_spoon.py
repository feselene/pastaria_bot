import os
import sys
import time

# Setup root imports
CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "../.."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from utils.click_button import click_button

# Define path to assets
ASSETS_DIR = os.path.join(ROOT_DIR, "assets")
SPOON_TEMPLATE = os.path.join(ASSETS_DIR, "spoon.png")

def click_spoon():
    click_button(SPOON_TEMPLATE, threshold=0.80)

if __name__ == "__main__":
    click_spoon()
