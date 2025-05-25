import os

import cv2
import mss
import numpy as np

from utils.crop_screenshot_by_ratio import crop_screenshot_as_numpy

# Use the ticket template located in assets/
TEMPLATE_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../assets/ticket_full.png")
)
CONFIDENCE_THRESHOLD = 0.5  # Adjustable depending on screenshot fidelity


def detect_ticket_from_template():
    return crop_screenshot_as_numpy(0.845, 0.132, 1, 0.8185)
