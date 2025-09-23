from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPEN_AI_API"))

import base64
with open("captured.jpg", "rb") as f:
    b64 = base64.b64encode(f.read()).decode("utf-8")
data_url = f"data:image/jpeg;base64,{b64}"
prompt = "You will receive an image as input. Generate a detailed caption for the image. If the image contains text, include the text in the caption. Be concise but descriptive."

response = client.responses.create(
    model="gpt-4.1-mini",
    input=[{
        "role": "user",
        "content": [
            {"type": "input_text", "text": prompt},
            {"type": "input_image", "image_url": data_url},
        ],
    }],
)

print(response.output_text)
