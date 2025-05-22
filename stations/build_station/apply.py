import cv2
import numpy as np
import os

CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "../../"))
DEBUG_DIR = os.path.join(ROOT_DIR, "debug")
os.makedirs(DEBUG_DIR, exist_ok=True)

from stations.build_station.select_ingredient import swipe_topping_picker_left
from stations.build_station.parse_topping import is_box_empty, center_contains_x
from stations.build_station.apply_sauce import apply_sauce

topping1 = os.path.join(DEBUG_DIR, "debug_topping1_raw.png")
topping2 = os.path.join(DEBUG_DIR, "debug_topping2_raw.png")
topping3 = os.path.join(DEBUG_DIR, "debug_topping3_raw.png")
topping4 = os.path.join(DEBUG_DIR, "debug_topping4_raw.png")

def process_topping_boxes():
    for i in range(1, 5):
        image_path = os.path.join(DEBUG_DIR, f"debug_topping{i}_raw.png")
        img = cv2.imread(image_path)

        if is_box_empty(img):
            continue
        elif center_contains_x(img):
            apply_ingredient(image_path)
        else:
            apply_topping(image_path)

def apply_ingredient(image_path):
    select_ingredient(image_path)
    return True

def apply_topping(image_path):
    select_ingredient(image_path)
    apply_sauce()

def select_ingredient(image_path):
    return True