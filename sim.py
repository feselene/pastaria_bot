import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim
from PIL import Image
import imagehash

def load_image(path, grayscale=False):
    if grayscale:
        return cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    else:
        return cv2.imread(path)

def compute_ssim(img1, img2):
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    score, _ = ssim(gray1, gray2, full=True)
    return score

def compute_mse(img1, img2):
    err = np.mean((img1.astype("float") - img2.astype("float")) ** 2)
    return err

def compare_histograms(img1, img2):
    hsv_img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2HSV)
    hsv_img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2HSV)
    hist_img1 = cv2.calcHist([hsv_img1], [0, 1], None, [50, 60], [0, 180, 0, 256])
    hist_img2 = cv2.calcHist([hsv_img2], [0, 1], None, [50, 60], [0, 180, 0, 256])
    cv2.normalize(hist_img1, hist_img1, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
    cv2.normalize(hist_img2, hist_img2, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
    score = cv2.compareHist(hist_img1, hist_img2, cv2.HISTCMP_CORREL)
    return score

def feature_matching(img1, img2, method='SIFT'):
    if method == 'SIFT':
        try:
            sift = cv2.SIFT_create()
        except:
            sift = cv2.xfeatures2d.SIFT_create()
        kp1, des1 = sift.detectAndCompute(img1, None)
        kp2, des2 = sift.detectAndCompute(img2, None)
        bf = cv2.BFMatcher()
    elif method == 'ORB':
        orb = cv2.ORB_create()
        kp1, des1 = orb.detectAndCompute(img1, None)
        kp2, des2 = orb.detectAndCompute(img2, None)
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    else:
        raise ValueError("Method must be 'SIFT' or 'ORB'.")

    if des1 is None or des2 is None:
        return 0

    matches = bf.match(des1, des2)
    matches = sorted(matches, key=lambda x: x.distance)
    good_matches = [m for m in matches if m.distance < 50]
    match_ratio = len(good_matches) / len(matches) if matches else 0
    return match_ratio

def compute_phash_similarity(img1_path, img2_path):
    img1 = Image.open(img1_path)
    img2 = Image.open(img2_path)
    hash1 = imagehash.phash(img1)
    hash2 = imagehash.phash(img2)
    return 1 - (hash1 - hash2) / len(hash1.hash) ** 2

def compute_all_similarities(img1_path, img2_path):
    img1 = load_image(img1_path)
    img2 = load_image(img2_path)
    results = {}
    results['SSIM'] = compute_ssim(img1, img2)
    results['MSE'] = compute_mse(img1, img2)
    results['Histogram Correlation'] = compare_histograms(img1, img2)
    results['SIFT Match Ratio'] = feature_matching(img1, img2, method='SIFT')
    results['ORB Match Ratio'] = feature_matching(img1, img2, method='ORB')
    results['pHash Similarity'] = compute_phash_similarity(img1_path, img2_path)
    return results

# Example usage:
if __name__ == "__main__":
    img1_path = r'C:\Users\ceo\IdeaProjects\pastaria_bot\debug\moz_s.png'
    img2_path = r'C:\Users\ceo\IdeaProjects\pastaria_bot\debug\moz_t.png'

    # Load images
    img1 = cv2.imread(img1_path)
    img2 = cv2.imread(img2_path)

    # Check if images are loaded properly
    if img1 is None:
        raise FileNotFoundError(f"Image at path {img1_path} not found.")
    if img2 is None:
        raise FileNotFoundError(f"Image at path {img2_path} not found.")

    # Determine target size (e.g., size of img1)
    target_size = (img1.shape[1], img1.shape[0])  # (width, height)

    # Resize img2 to match img1's size
    img2_resized = cv2.resize(img2, target_size, interpolation=cv2.INTER_AREA)

    # Save or process the resized images as needed
    a = r'C:\Users\ceo\IdeaProjects\pastaria_bot\debug\img1_resized.png'
    b = r'C:\Users\ceo\IdeaProjects\pastaria_bot\debug\img2_resized.png'
    cv2.imwrite(a, img1)
    cv2.imwrite(b, img2_resized)

    similarities = compute_all_similarities(a, b)
    for method, score in similarities.items():
        print(f"{method}: {score}")
