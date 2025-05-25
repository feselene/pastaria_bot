import ctypes
import time

# Calibrated game area
TOP_LEFT_X = 1920
TOP_LEFT_Y = 83
BOTTOM_RIGHT_X = 3797
BOTTOM_RIGHT_Y = 1141

RENDERED_WIDTH = BOTTOM_RIGHT_X - TOP_LEFT_X
RENDERED_HEIGHT = BOTTOM_RIGHT_Y - TOP_LEFT_Y


class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]


def get_mouse_position():
    pt = POINT()
    ctypes.windll.user32.GetCursorPos(ctypes.byref(pt))
    return pt.x, pt.y


def main():
    print("Tracking mouse ratios (always shown)... (Ctrl+C to stop)\n")
    try:
        while True:
            x, y = get_mouse_position()
            rel_x = (x - TOP_LEFT_X) / RENDERED_WIDTH
            rel_y = (y - TOP_LEFT_Y) / RENDERED_HEIGHT

            in_bounds = (0 <= rel_x <= 1) and (0 <= rel_y <= 1)

            status = "🟢 In bounds" if in_bounds else "🟡 Out of bounds"
            print(f"{status} | Mouse: ({x}, {y}) → Ratio: ({rel_x:.4f}, {rel_y:.4f})")

            time.sleep(0.1)
    except KeyboardInterrupt:
        print("👋 Exiting.")


if __name__ == "__main__":
    main()
