import os
import subprocess
import sys


CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "../../"))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from stations.build_station.click_jar import click_jar
from utils.get_memu_resolution import get_memu_resolution

ADB_PATH = r"D:\Program Files\Microvirt\MEmu\adb.exe"


def apply_sauce():
    memu_width, memu_height = get_memu_resolution()
    center_x = memu_width // 2
    center_y = int(memu_height * 0.65)

    # Offset ratios relative to screen width
    offset_ratios = [0.02, 0.04, 0.08, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.1]

    for i, ratio in enumerate(offset_ratios):
        print(f"swiping {i} with ratio {ratio}")
        print(ratio)
        offset = int(memu_width * ratio)
        start_x = center_x - offset
        end_x = center_x + offset
        duration_ms = 250

        if i % 2 == 0:
            adb_swipe(start_x, center_y, end_x, center_y, duration_ms)
        else:
            adb_swipe(end_x, center_y, start_x, center_y, duration_ms)

    print("✅ Stirred pasta side-to-side.")

def apply_sauce2():
    memu_width, memu_height = get_memu_resolution()
    center_x = memu_width // 2
    center_y = int(memu_height * 0.65)

    # Offset ratios relative to screen width
    offset_ratios = [0.02, 0.04, 0.08, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.1]

    for i, ratio in enumerate(offset_ratios):
        print(f"swiping {i} with ratio {ratio}")
        print(ratio)
        offset = int(memu_width * ratio)
        start_x = center_x - offset
        end_x = center_x + offset
        duration_ms = 250

        if i % 2 == 0:
            adb_swipe(start_x, center_y, end_x, center_y, duration_ms)
        else:
            adb_swipe(end_x, center_y, start_x, center_y, duration_ms)

    print("✅ Stirred pasta side-to-side.")


def adb_swipe(x1, y1, x2, y2, duration_ms=200):
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


if __name__ == "__main__":
    click_jar()
    apply_sauce()
