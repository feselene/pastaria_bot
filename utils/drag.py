import os
import subprocess

from dotenv import load_dotenv

load_dotenv()
ADB_PATH = os.getenv("ADB_PATH")

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
