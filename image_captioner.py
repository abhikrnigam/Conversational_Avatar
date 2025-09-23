# image_captioner.py
import os
import base64
import mimetypes
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# Prefer OPENAI_API_KEY, but keep your existing OPEN_AI_API for compatibility
_API_KEY = os.getenv("OPENAI_API_KEY") or os.getenv("OPEN_AI_API")
client = OpenAI(api_key=_API_KEY)

DEFAULT_PROMPT = (
    "You will receive an image as input. Generate a detailed caption for the image. "
    "If the image contains text, include the text in the caption. Be concise but descriptive. Make sure to mention the colour of the subjects."
    "The description should not exceed 50 words."
)

class ImageCaptioner:
    def __init__(self, prompt: str = DEFAULT_PROMPT):
        self.prompt = prompt

    def caption_image(self, image_path: str) -> str:
        # Encode image as data URL
        mime, _ = mimetypes.guess_type(image_path)
        if not mime:
            mime = "image/jpeg"
        with open(image_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("utf-8")
        data_url = f"data:{mime};base64,{b64}"

        # Call OpenAI Responses API (vision)
        resp = client.responses.create(
            model="gpt-4.1-mini",
            input=[{
                "role": "user",
                "content": [
                    {"type": "input_text", "text": self.prompt},
                    {"type": "input_image", "image_url": data_url},
                ],
            }],
        )

        return resp.output_text.strip() if getattr(resp, "output_text", "").strip() else "No caption generated."
