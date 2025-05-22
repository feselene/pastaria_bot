import os
import sys

CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "./"))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

# Import station modules
from stations.order_station import run_order_station
from stations.cook_station import cook_station
from stations.build_station import build_station
from stations.bread_station import bread_station

def main():
    print("▶️ Running Order Station...")
    order_station.run()

    print("🔥 Running Cook Station...")
    cook_station.run()

    print("🍝 Running Build Station...")
    build_station.run()

    print("🍞 Running Bread Station...")
    bread_station.run()

if __name__ == "__main__":
    main()