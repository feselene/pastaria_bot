# gemini_matcher.py
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

def encode_image(path):
    with open(path, "rb") as f:
        return f.read()

def is_matching(imgpath1, imgpath2) -> bool:
    image1 = encode_image(imgpath1)
    image2 = encode_image(imgpath2)

    response = model.generate_content(
        [
            "Is the ingredient in image2 selected in image1? Answer one word: yes or no. ",
            {"mime_type": "image/png", "data": image1},
            {"mime_type": "image/png", "data": image2},
        ],
        stream=False,
    )

    answer = response.text.strip().lower()
    return answer == "yes"

def is_matching2(imgpath1, imgpath2) -> bool:
    image1 = encode_image(imgpath1)
    image2 = encode_image(imgpath2)

    response = model.generate_content(
        [
            "Yes or No. Is image2 centered in image1?",
            {"mime_type": "image/png", "data": image1},
            {"mime_type": "image/png", "data": image2},
        ],
        stream=False,
    )

    answer = response.text.strip().lower()
    print(answer)


def main():
    print(os.getenv("GEMINI_API_KEY"))
    print(is_matching2(r"C:\Users\ceo\IdeaProjects\pastaria_bot\matches\match_00_current.png", r"C:\Users\ceo\IdeaProjects\pastaria_bot\matches\match_00_target.png"))

if __name__ == "__main__":
    main()
