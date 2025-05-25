import os
import sys

import cv2

from utils.click_button import drag_ratios, grab_screen_region

CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "../../"))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from utils.get_memu_resolution import get_memu_bounds


def get_best_template_match_center(template_path, threshold=0.75):
    # Load template
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
    if template is None:
        raise FileNotFoundError(f"Missing template image: {template_path}")
    tH, tW = template.shape[:2]

    # Capture screen and prepare search space
    screenshot = grab_screen_region()
    gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    height, width = gray.shape[:2]

    # Emulator window offset
    left, top, _, _ = get_memu_bounds()

    # Define ratio-based crop region
    xratio1, yratio1 = 0.3, 0.0
    xratio2, yratio2 = 0.6, 1.0

    x1 = int(width * xratio1)
    y1 = int(height * yratio1)
    x2 = int(width * xratio2)
    y2 = int(height * yratio2)

    cropped = gray[y1:y2, x1:x2]

    # Debug image output
    debug_output_path = os.path.join(ROOT_DIR, "debug", "search_region.png")
    cv2.imwrite(debug_output_path, cropped)

    # Matching loop
    best_val = -1
    best_loc = None
    best_scale = None
    best_template = None

    for scale in [1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0]:
        resized_template = cv2.resize(template, (int(tW * scale), int(tH * scale)))
        rH, rW = resized_template.shape[:2]

        if cropped.shape[0] < rH or cropped.shape[1] < rW:
            continue

        result = cv2.matchTemplate(cropped, resized_template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)

        if max_val > best_val:
            best_val = max_val
            best_loc = max_loc
            best_scale = scale
            best_template = resized_template

    if best_val >= threshold:
        match_x, match_y = best_loc
        match_h, match_w = best_template.shape[:2]

        # Final center coordinates in full screenshot
        center_x = x1 + match_x + match_w // 2
        center_y = y1 + match_y + match_h // 2

        # Offset by emulator window position to get absolute screen coords
        screen_x = center_x + left
        screen_y = center_y + top

        print(
            f"✅ Found match at ({screen_x}, {screen_y}) with scale {best_scale} and confidence {best_val:.3f}"
        )
        return screen_x, screen_y
    else:
        print(f"❌ No match found. Highest confidence: {best_val:.3f}")
        return None, None


def get_bread_ratios():
    """
    Matches the bread image and returns its (x, y) position as ratios
    relative to the emulator window.

    :return: (x_ratio, y_ratio) if match is found, otherwise (None, None)
    """
    template_path = (
        r"C:\Users\ceo\IdeaProjects\pastaria_bot\debug\debug_bread_cropped.png"
    )
    match_x, match_y = get_best_template_match_center(template_path)

    if match_x is None or match_y is None:
        print("❌ Could not find bread image.")
        return None, None

    memu_left, memu_top, memu_width, memu_height = get_memu_bounds()
    x_ratio = (match_x - memu_left) / memu_width
    y_ratio = (match_y - memu_top) / memu_height

    return x_ratio, y_ratio


def click_bread():
    template_path = (
        r"C:\Users\ceo\IdeaProjects\pastaria_bot\debug\debug_bread_cropped.png"
    )
    x, y = get_bread_ratios()

    drag_ratios(x, y, 0.15, 0.46)


def main():
    print(True)


if __name__ == "__main__":
    main()
