import os
import subprocess
import sys
import time

from clean import clean_files
from utils.click_build_button import click_build_button

CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "./"))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from stations.bread_station import bread_station
from stations.bread_station.bread_station import drag_bread_to_oven, submit_bread_and_ticket
from stations.build_station import build_station
from stations.cook_station import cook_station

# Import station modules
from stations.order_station import order_station
from utils.click_build_button import click_build_button
from utils.click_button import click_from_assets
from utils.click_cook_button import click_cook_button

ADB_PATH = r"D:\Program Files\Microvirt\MEmu\adb.exe"
ADB_PORT = 21503  # Default for MEmu instance 1


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


def main():
    try_adb_connect()
    while True:
        click_from_assets("play.png")
        time.sleep(1)
        click_from_assets("select.png")
        time.sleep(1)
        click_from_assets("start_button_template.png")

        for i in range(6):
            clean_files()
            print("▶️ Running Order Station...")
            order_station.run_order_station()
            click_cook_button()

            print("🔥 Running Cook Station...")
            time.sleep(1)
            cook_station.run_cook_station()
            time.sleep(1)
            click_build_button()
            time.sleep(1)
            click_from_assets("bread_button_right.png")
            time.sleep(2)
            drag_bread_to_oven()
            time.sleep(2)
            click_from_assets("build_button_left.png")

            print("🍝 Running Build Station...")
            time.sleep(1)
            build_station.run_build_station()

            print("🍞 Running Bread Station...")
            time.sleep(1)
            submit_bread_and_ticket()
            time.sleep(12)

        time.sleep(10)
        click_from_assets("skip_button_right.png")
        time.sleep(5)
        click_from_assets("skip_button_left.png")
        time.sleep(1)


if __name__ == "__main__":
    main()
