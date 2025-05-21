import cv2
import numpy as np
import mss
import os

# === CONFIG ===

TEMPLATE_PATH = "../assets/ticket_full.png"  # Full-size ticket screenshot as template
CONFIDENCE_THRESHOLD = 0.2
SCREENSHOT_SAVE = "../assets/matched_ticket.png"


# === FUNCTIONS ===

def capture_full_screen():
    """Capture a screenshot of the primary monitor using mss."""
    with mss.mss() as sct:
        screen = np.array(sct.grab(sct.monitors[1]))  # [1] is primary monitor
    return screen


def load_template(path):
    """Load grayscale template image from file."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"Template '{path}' not found.")
    template = cv2.imread(path, 0)
    return template


def find_ticket_on_screen(screen_bgr, template_gray):
    """Find the best match location for the template in the screen image."""
    screen_gray = cv2.cvtColor(screen_bgr, cv2.COLOR_BGR2GRAY)
    res = cv2.matchTemplate(screen_gray, template_gray, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, top_left = cv2.minMaxLoc(res)

    h, w = template_gray.shape
    bottom_right = (top_left[0] + w, top_left[1] + h)

    return top_left, bottom_right, max_val


def main():
    print("📸 Capturing screen...")
    screen = capture_full_screen()

    print(f"🧩 Loading template from '{TEMPLATE_PATH}'...")
    template = load_template(TEMPLATE_PATH)

    print("🔍 Matching template...")
    top_left, bottom_right, confidence = find_ticket_on_screen(screen, template)

    if confidence >= CONFIDENCE_THRESHOLD:
        print(f"✅ Ticket found at {top_left} with confidence {confidence:.2f}")
        matched = screen[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]
        cv2.imwrite(SCREENSHOT_SAVE, matched)
        print(f"💾 Cropped ticket saved to '{SCREENSHOT_SAVE}'")
    else:
        print(f"❌ Ticket not found. Confidence too low ({confidence:.2f})")


# === RUN ===

if __name__ == "__main__":
    main()
