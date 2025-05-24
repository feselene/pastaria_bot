# gemini_matcher.py
import os
import sys

import google.generativeai as genai
from dotenv import load_dotenv
import shutil

CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "../"))
DEBUG_DIR = os.path.join(ROOT_DIR, "debug")

if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

import time

import google.api_core.exceptions

from utils.capture import capture_center_picker_square
from utils.drag import half_swipe

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")


def encode_image(path):
    with open(path, "rb") as f:
        return f.read()


import datetime

def is_matching(imgpath1, imgpath2, max_retries=5) -> str:
    image1 = encode_image(imgpath1)
    image2 = encode_image(imgpath2)

    prompt = (
        "You are comparing two food ingredient icons from a cooking game.\n"
        "Icons may include ingredients like mushroom, light brown chicken strip, circle meatball, dark brown sausage, pink ham, red C icon, yellow M icon, cheese wheel icon, leafy sliced lemon icon.\n"
        "Are these the same icon?\n"
        "Answer yes or no with explanation."
    )

    request_content = [
        prompt,
        {"mime_type": "image/png", "data": image1},
        {"mime_type": "image/png", "data": image2},
    ]

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    for attempt in range(max_retries):
        try:
            response = model.generate_content(request_content, stream=False)
            answer = response.text.strip()

            # Save debug outputs with timestamp at the front
            img_a_debug = os.path.join(DEBUG_DIR, f"{timestamp}_compared_a.png")
            img_b_debug = os.path.join(DEBUG_DIR, f"{timestamp}_compared_b.png")
            explanation_debug = os.path.join(DEBUG_DIR, f"{timestamp}_comparison.txt")

            shutil.copy(imgpath1, img_a_debug)
            shutil.copy(imgpath2, img_b_debug)
            with open(explanation_debug, "w", encoding="utf-8") as f:
                f.write(answer)

            print(f"Gemini response: {answer}")
            return answer.lower()

        except google.api_core.exceptions.ResourceExhausted as e:
            retry_delay = getattr(e, "retry_delay", None)
            wait_seconds = retry_delay.seconds if retry_delay else 15
            print(
                f"⏳ Gemini rate limit hit (429). Waiting {wait_seconds}s... (attempt {attempt+1}/{max_retries})"
            )
            time.sleep(wait_seconds)

        except Exception as e:
            print(f"❌ Unexpected Gemini error: {e}")
            break

    print("❌ Failed to get a valid response after retries.")
    return "no"



def recenter(image_path, max_retries=3):
    """
    Asks Gemini if the topping in image_path is centered in the picker UI.
    If not, performs a half swipe to try to center it.
    """
    prompt = (
        "This image is from a horizontal ingredient picker in a cooking game.\n"
        "The currently selected topping should appear centered and slightly lower than the others.\n"
        "Is the topping in the center of this image correctly centered in the picker?\n"
        "Answer only 'yes' or 'no'."
    )

    image = encode_image(image_path)

    for attempt in range(max_retries):
        try:
            response = model.generate_content([
                prompt,
                {"mime_type": "image/png", "data": image}
            ], stream=False)

            answer = response.text.strip().lower()
            print(f"📍 Gemini recenter check: {answer}")

            if answer == "yes":
                return True
            else:
                print("↔️ Not centered — nudging with half swipe...")
                half_swipe()
                time.sleep(0.4)
        except Exception as e:
            print(f"❌ Recenter Gemini error: {e}")
            break

    return False



def is_matching2(imgpath1, imgpath2) -> bool:
    image1 = encode_image(imgpath1)
    image2 = encode_image(imgpath2)

    response = model.generate_content(
        [
            "Visually compare image A and image B. Are they the same ingredient? Respond only with yes or no. ",
            {"mime_type": "image/png", "data": image1},
            {"mime_type": "image/png", "data": image2},
        ],
        stream=False,
    )

    answer = response.text.strip().lower()
    print(answer)


def main():
    print(os.getenv("GEMINI_API_KEY"))
    image_path = capture_center_picker_square()


if __name__ == "__main__":
    main()
