import pygetwindow as gw
import mss
import numpy as np
import subprocess
import re

ADB_PATH = r"D:\Program Files\Microvirt\MEmu\adb.exe"  # Update this path as needed

def get_memu_bounds():
    windows = gw.getWindowsWithTitle("MEmu")

    for window in windows:
        if window.visible and window.width > 0 and window.height > 0:
            return window.left, window.top, window.width, window.height

    raise RuntimeError("❌ No visible MEmu window found.")


def grab_screen_region(x, y, width, height):
    """
    Captures a region of the screen and returns it as a NumPy array (BGR format).

    :param x: Left offset (pixels)
    :param y: Top offset (pixels)
    :param width: Width of the region (pixels)
    :param height: Height of the region (pixels)
    :return: NumPy array image (H x W x 3) in BGR format
    """
    with mss.mss() as sct:
        monitor = {"left": x, "top": y, "width": width, "height": height}
        screenshot = sct.grab(monitor)
        img = np.array(screenshot)
        return img[:, :, :3]  # Drop alpha channel, keep BGR

def get_memu_resolution():
    """
    Returns the screen resolution (width, height) of the MEmu emulator via ADB.

    :return: Tuple (width, height) in pixels
    :raises RuntimeError: if resolution cannot be determined
    """
    try:
        result = subprocess.check_output([ADB_PATH, "shell", "wm", "size"], stderr=subprocess.DEVNULL)
        output = result.decode("utf-8").strip()
        match = re.search(r'Physical size:\s*(\d+)x(\d+)', output)

        if match:
            width = int(match.group(1))
            height = int(match.group(2))
            return width, height
        else:
            raise RuntimeError(f"❌ Could not parse resolution from ADB output: {output}")
    except Exception as e:
        raise RuntimeError(f"❌ Failed to get MEmu resolution: {e}")
