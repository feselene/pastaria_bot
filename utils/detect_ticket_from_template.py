import os

import cv2
import mss
import numpy as np

# Use the ticket template located in assets/
TEMPLATE_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../assets/ticket_full.png")
)
CONFIDENCE_THRESHOLD = 0.5  # Adjustable depending on screenshot fidelity


def detect_ticket_from_template():
    """Detect and return the cropped ticket from the full screen using template matching."""
    with mss.mss() as sct:
        screen = np.array(sct.grab(sct.monitors[1]))  # Primary monitor

    screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(TEMPLATE_PATH, 0)
    if template is None:
        raise FileNotFoundError(f"❌ Template image not found at {TEMPLATE_PATH}")

    result = cv2.matchTemplate(screen_gray, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, top_left = cv2.minMaxLoc(result)

    h, w = template.shape
    bottom_right = (top_left[0] + w, top_left[1] + h)

    if max_val >= CONFIDENCE_THRESHOLD:
        cropped = screen[top_left[1] : bottom_right[1], top_left[0] : bottom_right[0]]
        print(f"✅ Ticket detected at {top_left} with confidence {max_val:.2f}")
        return cropped
    else:
        print(f"❌ Ticket not found (confidence: {max_val:.2f})")
        return None
