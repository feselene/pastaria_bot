import os
import subprocess
import sys
import time

from clean import clean_files

CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "./"))
ASSETS_DIR = os.path.join(ROOT_DIR, "assets")
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from stations.bread_station.bread_station import drag_bread_to_oven, submit_bread_and_ticket
from stations.build_station import build_station
from stations.cook_station import cook_station

# Import station modules
from stations.order_station import order_station
from utils.click_button import click_from_assets, click_ratios
from utils.button_visible import button_visible
from utils.click_cook_button import click_cook_button

ADB_PATH = r"D:\Program Files\Microvirt\MEmu\adb.exe"
ADB_PORT = 21503


def try_adb_connect(port=ADB_PORT):
    target = f"127.0.0.1:{port}"
    try:
        subprocess.run(
            [ADB_PATH, "connect", target],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except subprocess.CalledProcessError:
        print(f"❌ Failed to connect to MEmu via ADB on port {port}")
        raise SystemExit("Exiting due to ADB failure.")


def click_lower_right_button():
    # Click build station button in lower right.
    click_ratios(0.9, 0.9)

def click_lower_left_button():
    # Click build station button in lower right.
    click_ratios(0.07, 0.9)

def main():
    try_adb_connect()
    while True:
        # Click play button.
        click_ratios(0.5, 0.6)
        time.sleep(1)
        # Select save slot.
        click_ratios(0.5, 0.6)
        time.sleep(1)
        click_ratios(0.9, 0.9)
        time.sleep(1)

        for i in range(7):
            clean_files()
            print("▶️ Running Order Station...")
            order_station.run_order_station()
            if button_visible(os.path.join(ASSETS_DIR, "skip_button_left.png"), threshold=0.8):
                return
            click_cook_button()
            print("🔥 Running Cook Station...")
            time.sleep(1)
            cook_station.run_cook_station()
            time.sleep(1)
            # Click build station button in lower right.
            click_lower_right_button()
            time.sleep(1)
            # Click bread station button in lower right.
            click_lower_right_button()
            time.sleep(2)
            drag_bread_to_oven()
            time.sleep(2)
            click_lower_left_button()

            print("🍝 Running Build Station...")
            time.sleep(1)
            build_station.run_build_station()

            print("🍞 Running Bread Station...")
            time.sleep(3)
            submit_bread_and_ticket()
            time.sleep(12)

        time.sleep(10)
        click_from_assets("skip_button_right.png")
        time.sleep(5)
        click_from_assets("skip_button_left.png")
        time.sleep(1)


if __name__ == "__main__":
    main()
