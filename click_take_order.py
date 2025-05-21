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

def wait_for_and_click_take_order(template_path="take_order_template.png", threshold=0.85, max_wait=20):
    print("⏳ Waiting for TAKE ORDER...")

    template = cv2.imread(template_path, 0)
    if template is None:
        raise FileNotFoundError(f"Missing {template_path}")

    tw, th = template.shape[::-1]
    left, top, width, height = get_memu_bounds()

    end_time = time.time() + max_wait
    while time.time() < end_time:
        screenshot = grab_screen_region(left, top, width, height)
        gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

        result = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)

        print(f"🔍 Confidence: {max_val:.2f}")
        if max_val >= threshold:
            click_x = left + max_loc[0] + tw // 2
            click_y = top + max_loc[1] + th // 2
            pyautogui.moveTo(click_x, click_y)
            pyautogui.click()
            print(f"✅ Clicked TAKE ORDER at ({click_x}, {click_y}) with confidence {max_val:.2f}")
            return True

        time.sleep(0.5)

    print("❌ TAKE ORDER button not found in time.")
    return False

# Execute it
wait_for_and_click_take_order()
