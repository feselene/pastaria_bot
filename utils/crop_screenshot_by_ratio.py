import io
import subprocess

import cv2
import numpy as np
from PIL import Image


def adb_tap_relative(x_ratio: float, y_ratio: float):
    """
    Performs a tap on the Android screen at the specified relative position using ADB.

    Args:
        x_ratio (float): Horizontal position (0.0 to 1.0).
        y_ratio (float): Vertical position (0.0 to 1.0).
    """
    if not (0 <= x_ratio <= 1 and 0 <= y_ratio <= 1):
        raise ValueError("x_ratio and y_ratio must be between 0 and 1.")

    # Get screen resolution via ADB
    result = subprocess.run(["adb", "shell", "wm", "size"], capture_output=True, text=True)
    output = result.stdout.strip()

    if "Physical size" not in output:
        raise RuntimeError(f"Failed to get screen size: {output}")

    resolution = output.split("Physical size: ")[1]
    screen_width, screen_height = map(int, resolution.split("x"))

    # Convert ratios to pixel coordinates
    x = int(screen_width * x_ratio)
    y = int(screen_height * y_ratio)

    # Perform the tap
    subprocess.run(["adb", "shell", "input", "tap", str(x), str(y)])
    print(f"👆 Tapped at ({x}, {y}) on a screen of size {screen_width}x{screen_height}")


def adb_tap_and_hold_relative(x_ratio: float, y_ratio: float, duration_seconds: float = 1.0):
    """
    Performs a tap-and-hold gesture at a relative position on the Android screen using ADB.

    Args:
        x_ratio (float): Horizontal position (0.0 to 1.0).
        y_ratio (float): Vertical position (0.0 to 1.0).
        duration_seconds (float): Duration of the hold in seconds (default: 1.0).
    """
    if not (0 <= x_ratio <= 1 and 0 <= y_ratio <= 1):
        raise ValueError("x_ratio and y_ratio must be between 0 and 1.")
    if duration_seconds < 0:
        raise ValueError("duration_seconds must be non-negative.")

    # Get screen resolution
    result = subprocess.run(["adb", "shell", "wm", "size"], capture_output=True, text=True)
    output = result.stdout.strip()

    if "Physical size" not in output:
        raise RuntimeError(f"Failed to get screen size: {output}")

    resolution = output.split("Physical size: ")[1]
    screen_width, screen_height = map(int, resolution.split("x"))

    # Convert ratios to pixel coordinates
    x = int(screen_width * x_ratio)
    y = int(screen_height * y_ratio)

    # Convert seconds to milliseconds
    duration_ms = int(duration_seconds * 1000)

    # Perform swipe with identical start and end coordinates for hold
    subprocess.run(["adb", "shell", "input", "swipe", str(x), str(y), str(x), str(y), str(duration_ms)])
    print(f"🕒 Tap-and-hold at ({x}, {y}) for {duration_seconds:.2f}s on screen {screen_width}x{screen_height}")


def adb_drag_relative(x1_ratio: float, y1_ratio: float, x2_ratio: float, y2_ratio: float, duration_ms: int = 500):
    """
    Drags (swipes) from one relative screen coordinate to another on an Android device via ADB.

    Args:
        x1_ratio, y1_ratio (float): Start position (0.0–1.0)
        x2_ratio, y2_ratio (float): End position (0.0–1.0)
        duration_ms (int): Duration of the swipe in milliseconds
    """
    for r in [x1_ratio, y1_ratio, x2_ratio, y2_ratio]:
        if not (0 <= r <= 1):
            raise ValueError("All ratios must be between 0 and 1.")

    # Get screen resolution
    result = subprocess.run(["adb", "shell", "wm", "size"], capture_output=True, text=True)
    output = result.stdout.strip()

    if "Physical size" not in output:
        raise RuntimeError(f"Failed to get screen size: {output}")

    resolution = output.split("Physical size: ")[1]
    screen_width, screen_height = map(int, resolution.split("x"))

    # Convert ratios to absolute coordinates
    x1 = int(screen_width * x1_ratio)
    y1 = int(screen_height * y1_ratio)
    x2 = int(screen_width * x2_ratio)
    y2 = int(screen_height * y2_ratio)

    # Perform the swipe
    subprocess.run(["adb", "shell", "input", "swipe", str(x1), str(y1), str(x2), str(y2), str(duration_ms)])
    print(f"Swiped from ({x1}, {y1}) to ({x2}, {y2}) over {duration_ms}ms on screen {screen_width}x{screen_height}")



def crop_screenshot_by_ratio(xratio1, yratio1, xratio2, yratio2):
    if not all(0 <= r <= 1 for r in [xratio1, yratio1, xratio2, yratio2]):
        raise ValueError("All ratios must be between 0 and 1.")

    if xratio1 > xratio2 or yratio1 > yratio2:
        raise ValueError(
            "Top-left ratios must be less than or equal to bottom-right ratios."
        )

    # Capture full screenshot via ADB
    result = subprocess.run(["adb", "exec-out", "screencap", "-p"], capture_output=True)
    if result.returncode != 0:
        raise RuntimeError("Failed to take screenshot.")

    image = Image.open(io.BytesIO(result.stdout))
    width, height = image.size

    # Compute absolute crop box
    x1 = int(width * xratio1)
    y1 = int(height * yratio1)
    x2 = int(width * xratio2)
    y2 = int(height * yratio2)

    cropped = image.crop((x1, y1, x2, y2))
    return cropped


def crop_screenshot_as_numpy(xratio1, yratio1, xratio2, yratio2):
    if not all(0 <= r <= 1 for r in [xratio1, yratio1, xratio2, yratio2]):
        raise ValueError("All ratios must be between 0 and 1.")

    if xratio1 > xratio2 or yratio1 > yratio2:
        raise ValueError("Top-left ratios must be <= bottom-right ratios.")

    # Capture screenshot using ADB
    result = subprocess.run(["adb", "exec-out", "screencap", "-p"], capture_output=True)
    if result.returncode != 0:
        raise RuntimeError("Failed to take screenshot.")

    # Open as RGB
    image = Image.open(io.BytesIO(result.stdout)).convert("RGB")
    width, height = image.size

    # Convert to numpy array and then to BGR (for OpenCV)
    img_rgb = np.array(image)
    img_bgr = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)

    # Crop region
    x1 = int(width * xratio1)
    y1 = int(height * yratio1)
    x2 = int(width * xratio2)
    y2 = int(height * yratio2)

    cropped_np = img_bgr[y1:y2, x1:x2, :]
    return cropped_np


def main():
    cropped_image = crop_screenshot_by_ratio(0, 0.896, 0.227, 1)
    cropped_image.save("output.png")


if __name__ == "__main__":
    main()
