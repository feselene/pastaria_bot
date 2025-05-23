import pygetwindow as gw
import mss
import numpy as np

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