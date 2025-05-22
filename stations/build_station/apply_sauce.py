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
TOMATO_JAR_TEMPLATE = os.path.join(ASSETS_DIR, "tomato_jar.png")

def apply_sauce():
    return True

if __name__ == "__main__":
    apply_sauce()
