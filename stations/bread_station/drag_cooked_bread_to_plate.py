import os
import sys
import time
import pyautogui


# Setup root imports
CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "../.."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from utils.get_memu_position import get_memu_bounds


def drag_bread_to_plate(start_x_ratio=0.72, start_y_ratio=0.46,
                       end_x_ratio=0.44, end_y_ratio=0.61, duration=0.1):
    """
    Clicks and drags from a start position to an end position based on ratio
    coordinates relative to the MEmu window.

    :param start_x_ratio: Horizontal ratio of the start point (0.0 to 1.0)
    :param start_y_ratio: Vertical ratio of the start point (0.0 to 1.0)
    :param end_x_ratio: Horizontal ratio of the end point (0.0 to 1.0)
    :param end_y_ratio: Vertical ratio of the end point (0.0 to 1.0)
    :param duration: Time in seconds for the drag
    """
    left, top, width, height = get_memu_bounds()

    start_x = int(left + width * start_x_ratio)
    start_y = int(top + height * start_y_ratio)
    end_x = int(left + width * end_x_ratio)
    end_y = int(top + height * end_y_ratio)

    pyautogui.moveTo(start_x, start_y, duration=0.05)
    pyautogui.mouseDown()
    pyautogui.moveTo(end_x, end_y, duration=duration)
    pyautogui.mouseUp()

    print(f"🖱️ Dragged from ({start_x}, {start_y}) to ({end_x}, {end_y})")


if __name__ == "__main__":
    drag_bread_to_plate()
