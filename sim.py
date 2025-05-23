import pyautogui
import time
from utils.get_memu_resolution import get_memu_bounds  # Make sure this import is valid

def swipe_topping_picker_left():
    x_ratio = 0.422
    y_ratio = 0.32
    swipe_offset_ratio = 0.09
    left, top, width, height = get_memu_bounds()
    center_x = int(left + width * x_ratio)
    center_y = int(top + height * y_ratio)
    swipe_x = int(center_x - width * swipe_offset_ratio)

    pyautogui.moveTo(center_x, center_y, duration=0.01)
    pyautogui.mouseDown()
    pyautogui.moveTo(swipe_x, center_y, duration=1)
    pyautogui.mouseUp()

    print(
        f"⬅️ Swiped topping picker left from ({center_x}, {center_y}) to ({swipe_x}, {center_y})"
    )

def print_mouse_ratios():
    """
    Prints the x_ratio and y_ratio of the current mouse position
    relative to the MEmu emulator window.
    """
    left, top, width, height = get_memu_bounds()
    print("🖱 Move your mouse to the target location. Tracking in 3 seconds...")
    time.sleep(3)

    x, y = pyautogui.position()
    x_ratio = (x - left) / width
    y_ratio = (y - top) / height

    print(f"🧮 Mouse position: ({x}, {y})")
    print(f"📐 x_ratio: {x_ratio:.5f}, y_ratio: {y_ratio:.5f}")


def main():
    while True:
        print_mouse_ratios()
    '''
    for i in range(9):
        print(f"🔁 Swipe {i+1}/3")
        swipe_topping_picker_left()
        time.sleep(0.5)  # Optional delay between swipes
    '''

if __name__ == "__main__":
    main()
