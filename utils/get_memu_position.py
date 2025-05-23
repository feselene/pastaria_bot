import pygetwindow as gw


def get_memu_bounds():
    windows = gw.getWindowsWithTitle("MEmu")

    for window in windows:
        if window.visible and window.width > 0 and window.height > 0:
            return window.left, window.top, window.width, window.height

    raise RuntimeError("❌ No visible MEmu window found.")
