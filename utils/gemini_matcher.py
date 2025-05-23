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

def is_matching(imgpath1, imgpath2) -> str:
    image1 = encode_image(imgpath1)
    image2 = encode_image(imgpath2)

    response = model.generate_content(
        [
            "Compare image A (current topping picker selection) and image B (ingredient from the order ticket).",
            "Are they the same ingredient?",
            "Respond in this exact format: 'yes' or 'no', followed by a numeric confidence score from 0 to 1.",
            "Example: yes, 0.92",
            {"mime_type": "image/png", "data": image1},
            {"mime_type": "image/png", "data": image2},
        ],
        stream=False,
    )

    answer = response.text.strip().lower()
    print(f"Gemini response: {answer}")
    return answer

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
