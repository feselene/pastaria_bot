import cv2
import numpy as np
import os
import time
from skimage.metrics import structural_similarity as ssim
import mss

# Configuration
DEBUG_DIR = "debug"
os.makedirs(DEBUG_DIR, exist_ok=True)

TEMPLATE_PATH = r"C:\Users\ceo\IdeaProjects\pastaria_bot\toppings\topping4.png"

def get_memu_bounds():
    import pygetwindow as gw
    win = gw.getWindowsWithTitle("MEmu")[0]
    return win.left, win.top, win.width, win.height

def capture_center_picker_square():
    x_ratio = 0.422
    y_ratio = 0.32
    square_size = 150
    half = square_size / 2
    left, top, width, height = get_memu_bounds()
    center_x = int(left + width * x_ratio)
    center_y = int(top + height * y_ratio)

    region = {
        "left": int(center_x - half),
        "top": int(center_y - half),
        "width": square_size,
        "height": square_size,
    }

    with mss.mss() as sct:
        img = np.array(sct.grab(region))

    output_path = os.path.join(DEBUG_DIR, f"topping_active.png")
    cv2.imwrite(output_path, img)
    return img

def compute_similarity(img1, img2):
    img2_resized = cv2.resize(img2, (img1.shape[1], img1.shape[0]))
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2_resized, cv2.COLOR_BGR2GRAY)
    score, _ = ssim(gray1, gray2, full=True)
    return score

def monitor_similarity_to_cheese(interval=1.0):
    print("🔍 Monitoring topping selector for cheese...")
    template = cv2.imread(TEMPLATE_PATH)
    if template is None:
        raise FileNotFoundError(f"Could not load template image at {TEMPLATE_PATH}")

    try:
        while True:
            captured_img = capture_center_picker_square()
            score = compute_similarity(captured_img, template)
            print(f"🔁 Similarity score to cheese: {score:.3f}")
            time.sleep(interval)
    except KeyboardInterrupt:
        print("⏹️ Monitoring stopped.")

def main():
    monitor_similarity_to_cheese()

if __name__ == "__main__":
    main()
