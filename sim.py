import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_digit(image_path):
    image = cv2.imread(image_path)

    # Resize for better OCR accuracy
    image = cv2.resize(image, None, fx=4, fy=4, interpolation=cv2.INTER_LINEAR)

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Increase contrast and threshold
    _, thresh = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY_INV)

    # Optional: save debug view
    cv2.imwrite("debug_thresh.png", thresh)

    # Tesseract config
    config = r'--psm 10 -c tessedit_char_whitelist=0123456789'
    raw_result = pytesseract.image_to_string(thresh, config=config)
    cleaned = ''.join(filter(str.isdigit, raw_result))

    # print(f"OCR Raw: {repr(raw_result)} | Cleaned: {cleaned}")
    return int(cleaned) if cleaned else None

# Example usage
if __name__ == "__main__":
    print(extract_digit(r"C:\Users\ceo\IdeaProjects\pastaria_bot\toppings\num_topping3.png"))
