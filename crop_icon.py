import cv2
import numpy as np

# Load the image (replace 'input.png' with your filename)
img = cv2.imread(r'C:\Users\ceo\IdeaProjects\pastaria_bot\toppings\topping4.png', cv2.IMREAD_COLOR)
h, w = img.shape[:2]

# 1. Preprocess: blur the image to reduce noise speckles
blur = cv2.medianBlur(img, 3)  # or cv2.GaussianBlur(img, (3,3), 0)

# 2. Edge detection to find the border
gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 50, 150)  # Canny thresholds can be adjusted

# 3. Find the largest external contour (assumed to be the rounded border)
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
if len(contours) == 0:
    raise ValueError("No contours found – check the input image or adjust thresholds.")
# Select contour with max area
main_contour = max(contours, key=cv2.contourArea)
# (Optionally, you can verify contour area or shape here if needed)

# 4. Create mask of the interior of the border
mask = np.zeros((h, w), dtype=np.uint8)
cv2.drawContours(mask, [main_contour], contourIdx=-1, color=255, thickness=cv2.FILLED)

# 5. Remove the border outline by shrinking the mask slightly
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
mask = cv2.erode(mask, kernel, iterations=1)
# Now 'mask' has 255 for the area *inside* the border (border removed), 0 outside

# 6. Prepare output image with alpha channel
rgba = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
# Set alpha to 0 where mask is 0 (background), and 255 where mask is 255 (interior)
rgba[:, :, 3] = mask

# 7. (Optional) Remove interior white background
# Define white threshold (tolerating slightly off-white)
lower_white = np.array([240, 240, 240], dtype=np.uint8)
upper_white = np.array([255, 255, 255], dtype=np.uint8)
# Create a mask for near-white regions
white_mask = cv2.inRange(img, lower_white, upper_white)
# Mask it to only apply inside the border area (mask > 0)
white_mask = cv2.bitwise_and(white_mask, white_mask, mask=mask)
# Invert the white mask to get foreground content
content_mask = cv2.bitwise_not(white_mask)
# Update alpha: remove white background by applying content_mask
rgba[:, :, 3] = cv2.bitwise_and(rgba[:, :, 3], content_mask)

# 8. Crop the image tightly to the non-transparent content
# Find coordinates where alpha (mask) is non-zero
ys, xs = np.nonzero(rgba[:, :, 3])
if len(xs) == 0 or len(ys) == 0:
    raise ValueError("No foreground content found after background removal.")
x_min, x_max = xs.min(), xs.max()
y_min, y_max = ys.min(), ys.max()
cropped = rgba[y_min:y_max+1, x_min:x_max+1]

# Save the result as a PNG with transparency
cv2.imwrite('output.png', cropped)
