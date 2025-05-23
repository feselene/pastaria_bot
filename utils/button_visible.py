import cv2
import numpy as np
from utils.get_memu_position import get_memu_bounds, grab_screen_region

def button_visible(template_path, threshold=0.85):
    template = cv2.imread(template_path, 0)
    if template is None:
        raise FileNotFoundError(f"Missing template image: {template_path}")

    w, h = template.shape[::-1]
    left, top, width, height = get_memu_bounds()
    screenshot = grab_screen_region(left, top, width, height)
    gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    result = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, _ = cv2.minMaxLoc(result)

    return max_val >= threshold
