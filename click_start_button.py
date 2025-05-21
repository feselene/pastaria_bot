import cv2
import numpy as np
import pyautogui
import time
import mss
from get_memu_position import get_memu_bounds

# Grab a region from screen using mss (multi-monitor safe)
def grab_screen_region(x, y, width, height):
    with mss.mss() as sct:
        monitor = {
            "top": y,
            "left": x,
            "width": width,
            "height": height
        }
        return np.array(sct.grab(monitor))

# Load the cropped START button template
template = cv2.imread("start_button_template.png", 0)
if template is None:
    raise FileNotFoundError("Missing 'start_button_template.png'. Make sure it’s in the same folder.")

w, h = template.shape[::-1]

# Get emulator window position
left, top, width, height = get_memu_bounds()

# Capture emulator window region
screenshot = grab_screen_region(left, top, width, height)
gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

# Template matching
result = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
_, max_val, _, max_loc = cv2.minMaxLoc(result)

# Confidence threshold
THRESHOLD = 0.85

if max_val >= THRESHOLD:
    center_x = left + max_loc[0] + w // 2
    center_y = top + max_loc[1] + h // 2
    pyautogui.moveTo(center_x, center_y)
    pyautogui.mouseDown(button='left')
    pyautogui.mouseUp(button='left')
    print(f"✅ Clicked START at ({center_x}, {center_y}) with confidence {max_val:.2f}")
else:
    print(f"❌ START button not found. Confidence: {max_val:.2f}")
