import math
import os
import sys
import subprocess
import time

# Add root to sys.path so we can import project utilities
CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "../../"))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from utils.click_button import adb_tap
import math
import subprocess
from utils.get_memu_resolution import get_memu_resolution

ADB_PATH = r"D:\Program Files\Microvirt\MEmu\adb.exe"  # Update path if needed


def adb_swipe(x1, y1, x2, y2, duration_ms):
    subprocess.run([ADB_PATH, "shell", "input", "swipe", str(x1), str(y1), str(x2), str(y2), str(duration_ms)],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def click_plate():
    # Use emulator resolution (not window bounds)
    memu_width, memu_height = get_memu_resolution()
    start_x = memu_width // 2
    start_y = int(memu_height * 2 / 3)
    end_y = start_y - int(memu_height * 0.3)

    print(f"📱 ADB swipe from ({start_x}, {start_y}) to ({start_x}, {end_y})")
    adb_swipe(start_x, start_y, start_x, end_y, 300)


def adb_swipe(x1, y1, x2, y2, duration_ms=300):
    subprocess.run([ADB_PATH, "shell", "input", "swipe", str(x1), str(y1), str(x2), str(y2), str(duration_ms)],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


ADB_PATH = r"D:\Program Files\Microvirt\MEmu\adb.exe"

def adb_swipe(x1, y1, x2, y2, duration_ms=300):
    subprocess.run([ADB_PATH, "shell", "input", "swipe", str(x1), str(y1), str(x2), str(y2), str(duration_ms)],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def swipe_blended_upward_away_from_oclock(n, distance_ratio=0.25, duration_ms=300):
    """
    Adds the upward vector and the reversed o'clock vector (dragging away from the given o'clock angle),
    then performs a swipe in that blended direction.
    """
    if not (0 <= n <= 12):
        raise ValueError("n must be in range 0–12")

    memu_width, memu_height = get_memu_resolution()
    center_x = memu_width // 2
    center_y = int(memu_height * 0.65)

    if n == 12:
        print(f"🖱️ Tapping center of plate at ({center_x}, {center_y})")
        adb_tap(center_x, center_y)
        return

    # Upward unit vector
    v1_x = 0
    v1_y = -1

    # O'clock angle in degrees (12 o'clock = -90°)
    angle_deg = (n * 30) - 90
    angle_rad = math.radians(angle_deg)

    # Reversed o'clock vector
    v2_x = -math.cos(angle_rad)
    v2_y = -math.sin(angle_rad)

    # Add vectors
    vx = v1_x + v2_x
    vy = v1_y + v2_y
    mag = math.sqrt(vx ** 2 + vy ** 2)

    if mag < 1e-5:
        print(f"⚠️ Blended vector canceled out: UP + opposite {n} o’clock → zero movement.")
        return

    # Normalize and scale
    dir_x = vx / mag
    dir_y = vy / mag
    distance = int(memu_width * distance_ratio)
    end_x = int(center_x + dir_x * distance)
    end_y = int(center_y + dir_y * distance)

    print(f"🔀 Swipe: UP + opposite {n} o’clock → from ({center_x}, {center_y}) to ({end_x}, {end_y})")
    adb_swipe(center_x, center_y, end_x, end_y, duration_ms)

if __name__ == "__main__":
    for n in range(1, 13):  # 1 through 12 inclusive
        swipe_blended_upward_away_from_oclock(n)
        time.sleep(1)

