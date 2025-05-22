import os
import sys
import time

import pyautogui

CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "../../"))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from utils.get_memu_position import get_memu_bounds


def apply_sauce():
    left, top, width, height = get_memu_bounds()

    # Step 2: Estimate plate center
    plate_center_x = left + width // 2
    plate_center_y = top + int(height * 0.65)  # approx. 65% down

    # Step 3: Define drag range (e.g., 150 pixels left/right)
    drag_distance = 150
    drag_left_x = plate_center_x - drag_distance
    drag_right_x = plate_center_x + drag_distance
    drag_left_x2 = plate_center_x - 1.5 * drag_distance
    drag_right_x2 = plate_center_x + 1.5 * drag_distance
    drag_left_x3 = plate_center_x - 2 * drag_distance
    drag_right_x3 = plate_center_x + 2 * drag_distance

    # Step 4: Perform drag
    pyautogui.moveTo(plate_center_x, plate_center_y, duration=0.1)
    pyautogui.mouseDown()
    time.sleep(0.05)
    pyautogui.moveTo(drag_right_x, plate_center_y, duration=0.2)
    pyautogui.moveTo(drag_left_x, plate_center_y, duration=0.2)
    pyautogui.moveTo(drag_right_x, plate_center_y, duration=0.2)
    pyautogui.moveTo(drag_left_x2, plate_center_y, duration=0.2)
    pyautogui.moveTo(drag_right_x2, plate_center_y, duration=0.2)
    pyautogui.moveTo(drag_left_x3, plate_center_y, duration=0.2)
    pyautogui.moveTo(drag_right_x3, plate_center_y, duration=0.2)
    pyautogui.moveTo(drag_left_x, plate_center_y, duration=0.2)
    pyautogui.moveTo(drag_right_x, plate_center_y, duration=0.2)
    pyautogui.moveTo(drag_left_x, plate_center_y, duration=0.2)
    pyautogui.moveTo(drag_right_x, plate_center_y, duration=0.2)
    pyautogui.moveTo(drag_left_x, plate_center_y, duration=0.2)
    pyautogui.mouseUp()

    print("✅ Stirred pasta side-to-side.")


if __name__ == "__main__":
    apply_sauce()
