import os
import sys
import time
from operator import truediv

from click_tomato_jar import click_tomato_jar

CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "../../"))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

def run_build_station():
    return True

def run_random():
    click_tomato_jar()

if __name__ == "__main__":
    run_random()
