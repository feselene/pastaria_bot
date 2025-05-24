import math
import os
import subprocess
import sys
import time

# Add root to sys.path so we can import project utilities
CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "../../"))
DEBUG_DIR = os.path.join(ROOT_DIR, "debug")
FLAG_PATH = os.path.join(DEBUG_DIR, "flag.txt")
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

import math
import subprocess

from utils.click_button import adb_tap
from utils.get_memu_resolution import get_memu_resolution

ADB_PATH = r"D:\Program Files\Microvirt\MEmu\adb.exe"  # Update path if needed


def adb_swipe(x1, y1, x2, y2, duration_ms):
    subprocess.run(
        [
            ADB_PATH,
            "shell",
            "input",
            "swipe",
            str(x1),
            str(y1),
            str(x2),
            str(y2),
            str(duration_ms),
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def adb_swipe(x1, y1, x2, y2, duration_ms=300):
    subprocess.run(
        [
            ADB_PATH,
            "shell",
            "input",
            "swipe",
            str(x1),
            str(y1),
            str(x2),
            str(y2),
            str(duration_ms),
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


ADB_PATH = r"D:\Program Files\Microvirt\MEmu\adb.exe"


def adb_swipe(x1, y1, x2, y2, duration_ms=300):
    subprocess.run(
        [
            ADB_PATH,
            "shell",
            "input",
            "swipe",
            str(x1),
            str(y1),
            str(x2),
            str(y2),
            str(duration_ms),
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def swipe_to_middle():
    swipe_blended_upward_away_from_oclock(6, oclock_weight=0)


def swipe_blended_upward_away_from_oclock(
    n, distance_ratio=0.25, duration_ms=300, up_weight=0.6, oclock_weight=0.6
):
    """
    Adds a raw upward vector and a raw reversed o'clock vector, scaled by respective weights.
    Final swipe vector magnitude is directly proportional to the combined vector length.
    """
    if not (0 <= n <= 12):
        raise ValueError("n must be in range 0–12 inclusive")

    memu_width, memu_height = get_memu_resolution()
    center_x = memu_width // 2
    center_y = int(memu_height * 0.65)

    if abs(n - 12) < 1e-2:
        print(f"🖱️ Tapping center of plate at ({center_x}, {center_y})")
        adb_tap(center_x, center_y)
        return

    # Weighted upward vector
    v1_x = 0
    v1_y = -up_weight

    # Weighted reversed o'clock vector
    angle_deg = (n * 30) - 90
    angle_rad = math.radians(angle_deg)
    v2_x = -math.cos(angle_rad) * oclock_weight
    v2_y = -math.sin(angle_rad) * oclock_weight

    # Raw combined vector
    vx = v1_x + v2_x
    vy = v1_y + v2_y

    # Final swipe endpoint (scaled by distance ratio and screen width)
    distance_scale = memu_width * distance_ratio
    end_x = int(center_x + vx * distance_scale)
    end_y = int(center_y + vy * distance_scale)
    adb_swipe(center_x, center_y, end_x, end_y, duration_ms)
    time.sleep(0.5)


def place_in_positions(positions):
    for pos in positions:
        swipe_blended_upward_away_from_oclock(pos)


def set_flag():
    """
    Creates a flag file (flag.txt) in DEBUG_DIR.
    """
    os.makedirs(DEBUG_DIR, exist_ok=True)
    with open(FLAG_PATH, "w") as f:
        f.write("1")
    print(f"🚩 Flag set at: {FLAG_PATH}")


def check_flag():
    """
    Checks if the flag file exists in DEBUG_DIR.

    Returns:
        bool: True if flag.txt exists, False otherwise.
    """
    exists = os.path.isfile(FLAG_PATH)
    print(f"✅ Flag exists: {exists}" if exists else "❌ Flag not found.")
    return exists


def place_topping(num):
    match num:
        case 1:
            swipe_to_middle()
        case 2:
            if not check_flag():
                place_in_positions([2, 8])
                set_flag()
            else:
                place_in_positions([4, 10])

        case 3:
            if not check_flag():
                place_in_positions([2, 6, 10])
                set_flag()
            else:
                place_in_positions([4, 8, 12])
        case 4:
            if not check_flag():
                place_in_positions([2, 4, 8, 10])
                set_flag()
            else:
                place_in_positions([3, 6, 9, 12])
        case 5:
            swipe_to_middle()
            place_in_positions([3, 6, 9, 12])
        case 6:
            if not check_flag():
                place_in_positions([2, 4, 6, 8, 10, 12])
                set_flag()
            else:
                place_in_positions([1, 3, 5, 7, 9, 11])
        case 7:
            swipe_to_middle()
            place_in_positions([2, 4, 6, 8, 10, 12])
        case 8:
            place_in_positions([1.5, 3, 4.5, 6, 7.5, 9, 10.5, 12])
        case 9:
            swipe_to_middle()
            place_in_positions([1.5, 3, 4.5, 6, 7.5, 9, 10.5, 12])
        case _:
            print(f"Unsupported topping count: {num}")


if __name__ == "__main__":
    place_topping(6)
