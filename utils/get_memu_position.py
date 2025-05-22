import pygetwindow as gw


def get_memu_bounds():
    windows = gw.getWindowsWithTitle("MEmu")

    for window in windows:
        if window.visible and window.width > 0 and window.height > 0:
            # Print title and position for debugging
            print(
                f"✅ Found window: '{window.title}' at ({window.left}, {window.top}) size ({window.width}x{window.height})"
            )
            return window.left, window.top, window.width, window.height

    raise RuntimeError("❌ No visible MEmu window found.")
