# gemini_matcher.py
import os
import google.generativeai as genai
from dotenv import load_dotenv

import time
import google.api_core.exceptions

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

def encode_image(path):
    with open(path, "rb") as f:
        return f.read()

def is_matching(imgpath1, imgpath2, max_retries=5) -> str:
    image1 = encode_image(imgpath1)
    image2 = encode_image(imgpath2)

    prompt = (
        "You are comparing two small food icons:\n"
        "Image A is from the topping picker.\n"
        "Image B is from the order ticket.\n\n"
        "Do they represent the same ingredient or topping? Answer only 'yes' or 'no'."
    )

    request_content = [
        prompt,
        {"mime_type": "image/png", "data": image1},
        {"mime_type": "image/png", "data": image2},
    ]

    for attempt in range(max_retries):
        try:
            response = model.generate_content(request_content, stream=False)
            answer = response.text.strip().lower()
            print(f"Gemini response: {answer}")
            return answer

        except google.api_core.exceptions.ResourceExhausted as e:
            retry_delay = getattr(e, 'retry_delay', None)
            wait_seconds = retry_delay.seconds if retry_delay else 15
            print(f"⏳ Gemini rate limit hit (429). Waiting {wait_seconds}s... (attempt {attempt+1}/{max_retries})")
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
    is_matching(r"C:\Users\ceo\IdeaProjects\pastaria_bot\matches\match_03_current.png", r"C:\Users\ceo\IdeaProjects\pastaria_bot\matches\match_03_target.png")

if __name__ == "__main__":
    main()
