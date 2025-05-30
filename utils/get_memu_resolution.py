import re
import subprocess
import pygetwindow as gw
import os

from dotenv import load_dotenv

load_dotenv()
ADB_PATH = os.getenv("ADB_PATH")

def get_memu_bounds():
    windows = gw.getWindowsWithTitle("MEmu")

    for window in windows:
        if window.visible and window.width > 0 and window.height > 0:
            return window.left, window.top, window.width, window.height

    raise RuntimeError("❌ No visible MEmu window found.")

def get_memu_resolution():
    """
    Returns the screen resolution (width, height) of the MEmu emulator via ADB.

    :return: Tuple (width, height) in pixels
    :raises RuntimeError: if resolution cannot be determined
    """
    try:
        result = subprocess.check_output(
            [ADB_PATH, "shell", "wm", "size"], stderr=subprocess.DEVNULL
        )
        output = result.decode("utf-8").strip()
        match = re.search(r"Physical size:\s*(\d+)x(\d+)", output)

        if match:
            width = int(match.group(1))
            height = int(match.group(2))
            return width, height
        else:
            raise RuntimeError(
                f"❌ Could not parse resolution from ADB output: {output}"
            )
    except Exception as e:
        raise RuntimeError(f"❌ Failed to get MEmu resolution: {e}")

def main():
    try:
        resolution = get_memu_resolution()
        print(f"✅ MEmu resolution: {resolution[0]}x{resolution[1]}")
    except RuntimeError as e:
        print(str(e))

if __name__ == "__main__":
    main()
