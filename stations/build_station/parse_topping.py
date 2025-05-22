import cv2
import numpy as np
import os

CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "../../"))
DEBUG_DIR = os.path.join(ROOT_DIR, "debug")
os.makedirs(DEBUG_DIR, exist_ok=True)

topping1 = os.path.join(DEBUG_DIR, "debug_topping1_raw.png")
topping2 = os.path.join(DEBUG_DIR, "debug_topping2_raw.png")
topping3 = os.path.join(DEBUG_DIR, "debug_topping3_raw.png")
topping4 = os.path.join(DEBUG_DIR, "debug_topping4_raw.png")

def is_box_empty(img, tolerance=10, match_ratio=0.6):
    """
    Determines if a UI ingredient box is empty based on uniform color coverage.

    Parameters:
        img (np.ndarray): Input image (BGR).
        tolerance (int): Max per-channel difference from center pixel.
        match_ratio (float): Required fraction of pixels matching center pixel.

    Returns:
        bool: True if at least `match_ratio` of pixels match center pixel within `tolerance`.
    """
    if img is None:
        return True

    h, w = img.shape[:2]
    center_pixel = img[h // 2, w // 2]

    # Compute absolute channel-wise difference from center pixel
    diff = np.abs(img.astype(np.int16) - center_pixel.astype(np.int16))
    mask = np.all(diff <= tolerance, axis=2)

    # Calculate match ratio
    ratio = np.sum(mask) / (h * w)
    return ratio >= match_ratio


def center_contains_x(box_img, debug=False):
    """
    Determines if the center of the box contains an 'X' pattern using edge and line detection.

    Parameters:
        box_img (np.ndarray): Input image (BGR).
        debug (bool): Whether to visualize detected lines.

    Returns:
        bool: True if an 'X' is likely present in the center, False otherwise.
    """
    if box_img is None:
        return False

    h, w = box_img.shape[:2]
    crop = box_img[h//4:h*3//4, w//4:w*3//4]  # center 50%

    gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)

    lines = cv2.HoughLines(edges, 1, np.pi / 180, threshold=20)
    if lines is None:
        return False

    angles = []
    for rho, theta in lines[:, 0]:
        angle = np.degrees(theta)
        angles.append(angle)

    # Look for one line near 45° and one near 135°
    found_45 = any(40 <= a <= 50 for a in angles)
    found_135 = any(130 <= a <= 140 for a in angles)

    if debug:
        debug_img = crop.copy()
        for rho, theta in lines[:, 0]:
            a, b = np.cos(theta), np.sin(theta)
            x0, y0 = a * rho, b * rho
            pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
            pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
            cv2.line(debug_img, pt1, pt2, (0, 255, 0), 2)
        cv2.imshow("Detected Lines", debug_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return found_45 and found_135

for i in range(1, 5):
    path = os.path.join(DEBUG_DIR, f"debug_topping{i}_raw.png")
    img = cv2.imread(path)

    if center_contains_x(img):
        print(f"❌ Topping {i}: Detected an X in center.")
    else:
        print(f"✅ Topping {i}: No X in center.")
