import os
import sys
import time

# Setup root imports
CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "../.."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)
ASSETS_DIR = os.path.join(ROOT_DIR, "assets")
PASTA_PATH = os.path.join(ASSETS_DIR, "pasta_bowl.png")
PLATE_PATH = os.path.join(ASSETS_DIR, "plate.png")


from utils.click_button import click_button
from utils.drag import drag_between_templates

# Define path to assets
ASSETS_DIR = os.path.join(ROOT_DIR, "assets")


def drag_pasta_to_plate():
    drag_between_templates(PASTA_PATH, PLATE_PATH, threshold=0.85)


if __name__ == "__main__":
    drag_pasta_to_plate()
