import os
import sys
import time

# Setup root imports
CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "../.."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)
ASSETS_DIR = os.path.join(ROOT_DIR, "assets")
TICKET_PATH = os.path.join(ASSETS_DIR, "ticket_full.png")
GREEN_PATH = os.path.join(ASSETS_DIR, "green.png")


from utils.click_button import click_button
from utils.drag import drag_between_templates

# Define path to assets
ASSETS_DIR = os.path.join(ROOT_DIR, "assets")

def drag_ticket_to_green():
    drag_between_templates(TICKET_PATH, GREEN_PATH, threshold=0.5)

if __name__ == "__main__":
    drag_ticket_to_green()
