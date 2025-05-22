import os

import cv2
import mss
import numpy as np
import pygetwindow as gw


def get_memu_bounds():
    windows = gw.getWindowsWithTitle("MEmu")
    for window in windows:
        if window.visible and window.width > 0 and window.height > 0:
            return window.left, window.top, window.width, window.height
    raise RuntimeError("❌ No visible MEmu window found.")


def get_conveyor_bounds(debug_dir="debug"):
    os.makedirs(debug_dir, exist_ok=True)

    # Capture MEmu screen
    left, top, width, height = get_memu_bounds()
    with mss.mss() as sct:
        monitor = {"left": left, "top": top, "width": width, "height": height}
        screenshot = np.array(sct.grab(monitor))

    # Detect brown belt using HSV filtering
    hsv = cv2.cvtColor(screenshot, cv2.COLOR_BGR2HSV)
    lower_brown = np.array([10, 100, 50])
    upper_brown = np.array([30, 255, 200])
    mask = cv2.inRange(hsv, lower_brown, upper_brown)
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    # Find largest brown contour
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        raise RuntimeError("❌ No brown conveyor found.")

    largest = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(largest)

    # Debug output
    debug_img = screenshot.copy()
    cv2.rectangle(debug_img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.imwrite(os.path.join(debug_dir, "conveyor_detected.png"), debug_img)

    # Return coordinates in full-screen space
    return x + left, y + top, w, h
