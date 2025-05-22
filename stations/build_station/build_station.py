import os
import sys
import time
from operator import truediv

from stations.build_station.click_tomato_jar import click_tomato_jar
from stations.build_station.apply_sauce import apply_sauce
from stations.build_station.click_checkmark import click_checkmark

CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "../../"))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

def run_build_station():
    return True

def run_random():
    click_tomato_jar()
    apply_sauce()
    time.sleep(0.5)
    click_checkmark()

if __name__ == "__main__":
    run_random()
