import cv2

from utils.click_button import grab_screen_region


def button_visible(template_path, threshold=0.6):
    template = cv2.imread(template_path, 0)
    if template is None:
        raise FileNotFoundError(f"Missing template image: {template_path}")

    screenshot = grab_screen_region()
    gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    result = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, _ = cv2.minMaxLoc(result)

    return max_val >= threshold
