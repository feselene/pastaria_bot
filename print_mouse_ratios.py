import time
import pyautogui
from utils.get_memu_resolution import get_memu_bounds

def print_mouse_ratios():
    left, top, width, height = get_memu_bounds()

    print("🖱️ Move your mouse over the MEmu window... Press Ctrl+C to stop.\n")
    try:
        while True:
            x, y = pyautogui.position()
            if left <= x <= left + width and top <= y <= top + height:
                rel_x = (x - left) / width
                rel_y = (y - top) / height
                print(f"Mouse at ({rel_x:.3f}, {rel_y:.3f}) in MEmu")
            else:
                print("🟡 Mouse is outside MEmu bounds")
            time.sleep(0.2)
    except KeyboardInterrupt:
        print("👋 Exiting.")

if __name__ == "__main__":
    print_mouse_ratios()
