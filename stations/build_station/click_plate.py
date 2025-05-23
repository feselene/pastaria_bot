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

def swipe_blended_upward_away_from_oclock(n, distance_ratio=0.25, duration_ms=300, up_weight=1.0, oclock_weight=1.0):
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

    print(f"🧭 Raw swipe: {up_weight}×UP + {oclock_weight}×opp({n}) → ({center_x}, {center_y}) → ({end_x}, {end_y})")
    adb_swipe(center_x, center_y, end_x, end_y, duration_ms)



if __name__ == "__main__":
    swipe_blended_upward_away_from_oclock(0.01, up_weight=0.7, oclock_weight=0)
    for n in range(1, 12):  # 1 through 12 inclusive
        swipe_blended_upward_away_from_oclock(n, up_weight=0.7, oclock_weight=0.75)
        time.sleep(1)

    swipe_blended_upward_away_from_oclock(12, up_weight=0.7, oclock_weight=0)

