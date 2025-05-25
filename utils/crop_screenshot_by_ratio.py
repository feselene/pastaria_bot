import subprocess

from PIL import Image
import io
import numpy as np
import cv2


def adb_tap_relative(x_ratio: float, y_ratio: float):
    if not (0 <= x_ratio <= 1 and 0 <= y_ratio <= 1):
        raise ValueError("x_ratio and y_ratio must be between 0 and 1.")

    # Get screen resolution
    result = subprocess.run(["adb", "shell", "wm", "size"], capture_output=True, text=True)
    output = result.stdout.strip()

    if "Physical size" not in output:
        raise RuntimeError(f"Failed to get screen size: {output}")

    resolution = output.split("Physical size: ")[1]
    screen_width, screen_height = map(int, resolution.split("x"))

    # Calculate absolute coordinates
    x = int(screen_width * x_ratio)
    y = int(screen_height * y_ratio)

    # Perform the tap
    subprocess.run(["adb", "shell", "input", "tap", str(x), str(y)])
    print(f"Tapped at ({x}, {y}) on a screen of size {screen_width}x{screen_height}")

def crop_screenshot_by_ratio(xratio1, yratio1, xratio2, yratio2):
    if not all(0 <= r <= 1 for r in [xratio1, yratio1, xratio2, yratio2]):
        raise ValueError("All ratios must be between 0 and 1.")

    if xratio1 > xratio2 or yratio1 > yratio2:
        raise ValueError("Top-left ratios must be less than or equal to bottom-right ratios.")

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
    cropped_image = crop_screenshot_by_ratio(0.5653, 0.5284, 0.613, 0.6096)
    cropped_image.save("output.png")

if __name__ == "__main__":
    main()

