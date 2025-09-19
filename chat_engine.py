# chat_client.py
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

class ChatClient:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.messages = []
        self.system_message = ""

    def chat(self, user_input: str) -> str:
        self.messages.append({
            "role": "user",
            "content": user_input
        })

        completion = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=self.messages,
            temperature=1,
            max_tokens=2046,
            top_p=1,
            stream=True,
            stop=None
        )

        full_response = ""
        for chunk in completion:
            content = chunk.choices[0].delta.content
            if content:
                print(content, end="", flush=True)
                full_response += content

        self.messages.append({
            "system": self.system_message,
            "role": "assistant",
            "content": full_response
        })

        print()  # newline after response
        return full_response
