import cv2
import mss
import numpy as np
import pyautogui
import time

from utils.get_memu_position import get_memu_bounds


def grab_screen_region(x, y, width, height):
    with mss.mss() as sct:
        monitor = {"top": y, "left": x, "width": width, "height": height}
        return np.array(sct.grab(monitor))


def click_button(template_path, threshold=0.85):
    # Load template
    template = cv2.imread(template_path, 0)
    if template is None:
        raise FileNotFoundError(f"Missing template image: {template_path}")

    w, h = template.shape[::-1]

    # Get emulator window position
    left, top, width, height = get_memu_bounds()

    # Capture emulator window
    screenshot = grab_screen_region(left, top, width, height)
    gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    # Template matching
    result = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    if max_val >= threshold:
        center_x = left + max_loc[0] + w // 2
        center_y = top + max_loc[1] + h // 2
        pyautogui.moveTo(center_x, center_y)
        pyautogui.click()
        print(
            f"✅ Clicked button '{template_path}' at ({center_x}, {center_y}) with confidence {max_val:.2f}"
        )
        return True
    else:
        print(f"❌ Button '{template_path}' not found. Confidence: {max_val:.2f}")
        return False

def click_and_hold(template_path, hold_duration=1.0, threshold=0.85):
    """
    Finds a button on screen using template matching, then clicks and holds it for `hold_duration` seconds.

    :param template_path: Path to the template image of the button
    :param hold_duration: Time (in seconds) to hold the click
    :param threshold: Minimum match confidence
    :return: True if click-and-hold was performed, False otherwise
    """
    # Load template
    template = cv2.imread(template_path, 0)
    if template is None:
        raise FileNotFoundError(f"Missing template image: {template_path}")

    w, h = template.shape[::-1]

    # Get emulator window position
    left, top, width, height = get_memu_bounds()

    # Capture emulator window
    screenshot = grab_screen_region(left, top, width, height)
    gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    # Template matching
    result = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    if max_val >= threshold:
        center_x = left + max_loc[0] + w // 2
        center_y = top + max_loc[1] + h // 2
        pyautogui.moveTo(center_x, center_y)
        pyautogui.mouseDown()
        time.sleep(hold_duration)
        pyautogui.mouseUp()
        print(
            f"✅ Clicked and held button '{template_path}' at ({center_x}, {center_y}) for {hold_duration:.2f}s (confidence {max_val:.2f})"
        )
        return True
    else:
        print(f"❌ Button '{template_path}' not found. Confidence: {max_val:.2f}")
        return False

