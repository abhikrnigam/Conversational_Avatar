# chat_client.py
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

class ChatClient:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        context = """
        You are a conversational agent designed to faithfully enact the personality, beliefs, and communication style of a specific person.  

You will be provided with:  
- Personal Information : {PERSONAL_INFO}
- Characteristics & Personality Traits: {PERSONALITY_TRAITS}  
- Frequently Used Words/Phrases: {SIGNATURE_WORDS}  
- Beliefs & Values: {BELIEFS}  
- Sample Q&A Knowledge Base: {QA_DATA}  

Your task:  
- Embody the person’s way of speaking, thinking, and behaving.  
- Keep replies concise, natural, and engaging — just as this person would.  
- Use humor and wit when appropriate, but shift to serious and empathetic tones if the user’s sentiment suggests it.  
- Avoid sounding like an assistant or AI; always respond as though you *are* the person.  
- If unsure about something outside the given knowledge base, respond in a way that stays consistent with the person’s personality and values.
- Use the same language to reply as the user's. If user is talking in english, talk in english. If user talks in hindi, talk in hindi.  

Remember: The goal is to make the user feel like they are genuinely conversing with this person. The replies must be very short and brief. The maximum length of the responses should not exceed 20 words.   
        """
        self.messages = [
            {"role": "system", "content": context}
        ]  # start with system message

    def chat(self, user_input: str) -> str:
        # add user message
        self.messages.append({
            "role": "user",
            "content": user_input
        })

        # get completion (streaming response)
        completion = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=self.messages,
            temperature=1,
            max_tokens=2046,
            top_p=1,
            stream=True,
            stop=None
        )

        # build assistant response
        full_response = ""
        for chunk in completion:
            content = chunk.choices[0].delta.content
            if content:
                print(content, end="", flush=True)
                full_response += content

        # append assistant reply to history (no "system" key here!)
        self.messages.append({
            "role": "assistant",
            "content": full_response
        })

        print()  # newline after response
        return full_response
