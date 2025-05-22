import os
import sys
import time

# Setup root imports
CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "../.."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)
ASSETS_DIR = os.path.join(ROOT_DIR, "assets")
SPOON_PATH = os.path.join(ASSETS_DIR, "spoon.png")
JAR_PATH = os.path.join(ASSETS_DIR, "pot.png")


from utils.click_button import click_button
from utils.drag import drag_between_templates

# Define path to assets
ASSETS_DIR = os.path.join(ROOT_DIR, "assets")
SPOON_TEMPLATE = os.path.join(ASSETS_DIR, "spoon.png")

def stir():
    drag_between_templates(SPOON_PATH, JAR_PATH, threshold=0.85)

if __name__ == "__main__":
    stir()
