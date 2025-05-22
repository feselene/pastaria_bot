import cv2
import numpy as np
import pyautogui
import mss
from utils.get_memu_position import get_memu_bounds

def grab_screen_region(x, y, width, height):
    with mss.mss() as sct:
        monitor = {
            "top": y,
            "left": x,
            "width": width,
            "height": height
        }
        return np.array(sct.grab(monitor))

def drag_between_templates(start_template_path, end_template_path, threshold=0.85):
    # Load templates
    start_template = cv2.imread(start_template_path, 0)
    end_template = cv2.imread(end_template_path, 0)
    if start_template is None:
        raise FileNotFoundError(f"Missing start template: {start_template_path}")
    if end_template is None:
        raise FileNotFoundError(f"Missing end template: {end_template_path}")

    start_w, start_h = start_template.shape[::-1]
    end_w, end_h = end_template.shape[::-1]

    # Get MEmu window position
    left, top, width, height = get_memu_bounds()
    screenshot = grab_screen_region(left, top, width, height)
    gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    # Match start
    result_start = cv2.matchTemplate(gray, start_template, cv2.TM_CCOEFF_NORMED)
    _, max_val_start, _, max_loc_start = cv2.minMaxLoc(result_start)

    # Match end
    result_end = cv2.matchTemplate(gray, end_template, cv2.TM_CCOEFF_NORMED)
    _, max_val_end, _, max_loc_end = cv2.minMaxLoc(result_end)

    if max_val_start >= threshold and max_val_end >= threshold:
        start_x = left + max_loc_start[0] + start_w // 2
        start_y = top + max_loc_start[1] + start_h // 2
        end_x = left + max_loc_end[0] + end_w // 2
        end_y = top + max_loc_end[1] + end_h // 2

        pyautogui.moveTo(start_x, start_y)
        pyautogui.mouseDown()
        pyautogui.moveTo(end_x, end_y, duration=0.2)
        pyautogui.mouseUp()

        print(f"✅ Dragged from ({start_x}, {start_y}) to ({end_x}, {end_y})")
        return True
    else:
        print(f"❌ Drag failed. Start confidence: {max_val_start:.2f}, End confidence: {max_val_end:.2f}")
        return False