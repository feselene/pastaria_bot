import cv2
import numpy as np
import os
import time
from skimage.metrics import structural_similarity as ssim
import mss

# Configuration
DEBUG_DIR = "debug"
os.makedirs(DEBUG_DIR, exist_ok=True)

TEMPLATE_PATH = r"C:\Users\ceo\IdeaProjects\pastaria_bot\toppings\topping3.png"

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

def compute_all_similarities(img1, img2):
    img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # 1. SSIM
    ssim_score = ssim(gray1, gray2)

    # 2. MSE
    mse_score = np.mean((gray1.astype("float") - gray2.astype("float")) ** 2)

    # 3. PSNR
    psnr_score = cv2.PSNR(gray1, gray2)

    # 4. TM_CCORR_NORMED
    tm_corr = cv2.matchTemplate(gray1, gray2, cv2.TM_CCORR_NORMED)[0][0]

    # 5. TM_CCOEFF_NORMED
    tm_coeff = cv2.matchTemplate(gray1, gray2, cv2.TM_CCOEFF_NORMED)[0][0]

    # 6. Histogram Correlation
    hist1 = cv2.calcHist([gray1], [0], None, [256], [0, 256])
    hist2 = cv2.calcHist([gray2], [0], None, [256], [0, 256])
    hist_score = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)

    # 7. ORB Feature Matching
    orb = cv2.ORB_create()
    kp1, des1 = orb.detectAndCompute(gray1, None)
    kp2, des2 = orb.detectAndCompute(gray2, None)

    if des1 is not None and des2 is not None:
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = bf.match(des1, des2)
        orb_score = len(matches)
    else:
        orb_score = 0

    return {
        "SSIM": ssim_score,
        "MSE": mse_score,
        "PSNR": psnr_score,
        "TM_CCORR_NORMED": tm_corr,
        "TM_CCOEFF_NORMED": tm_coeff,
        "Histogram Correlation": hist_score,
        "ORB Matches": orb_score,
    }

def monitor_similarity_to_cheese(interval=1.0):
    print("🔍 Monitoring topping selector for cheese...")
    template = cv2.imread(TEMPLATE_PATH)
    if template is None:
        raise FileNotFoundError(f"Could not load template image at {TEMPLATE_PATH}")

    try:
        while True:
            captured_img = capture_center_picker_square()
            scores = compute_all_similarities(captured_img, template)

            print("\n🔁 Similarity Metrics:")
            for k, v in scores.items():
                print(f"  {k:25}: {v:.4f}" if isinstance(v, float) else f"  {k:25}: {v}")
            time.sleep(interval)
    except KeyboardInterrupt:
        print("⏹️ Monitoring stopped.")

def main():
    monitor_similarity_to_cheese()

if __name__ == "__main__":
    main()
