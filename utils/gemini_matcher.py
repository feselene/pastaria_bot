# gemini_matcher.py
import os
import sys
import time

import google.generativeai as genai
import google.api_core.exceptions
from dotenv import load_dotenv

CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "../"))
DEBUG_DIR = os.path.join(ROOT_DIR, "debug")

if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

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
        "Icons may include ingredients like mushroom, orange shrimp, light brown chicken strip, circle meatball, dark brown sausage, tomato slice, dead fish, starburst C icon, yellow M icon, cheese wheel icon, sliced bread icon.\n"
        "Are these the same icon? Ignore the background setting.\n"
        "Answer yes or no with explanation."
    )

    request_content = [
        prompt,
        {"mime_type": "image/png", "data": image1},
        {"mime_type": "image/png", "data": image2},
    ]

    for attempt in range(max_retries):
        try:
            response = model.generate_content(request_content, stream=False)
            answer = response.text.strip()
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


if __name__ == "__main__":
    main()
