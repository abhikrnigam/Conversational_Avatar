from groq import Groq
import os
from dotenv import load_dotenv
load_dotenv()

# API key ko environment variable se read karna
# Sabse best tarika hai GROQ_API_KEY environment variable set karna
# for Linux/Mac: export GROQ_API_KEY="tumhari_api_key_yahan"
# for Windows: set GROQ_API_KEY="tumhari_api_key_yahan"

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Chat history ko store karne ke liye ek list banate hain
# Isse model ko previous conversation yaad rahegi
messages = []

# Ek loop jo user se input lega jab tak user 'quit' nahi type karta
while True:
    user_input = input(" You : ")

    # Agar user 'quit' type kare, toh loop band kar do
    if user_input.lower() == 'quit':
        print("Chat band ho gayi. Alvida!")
        break

    # User ka naya message chat history mein add karein
    messages.append({
        "role": "user",
        "content": user_input
    })

    # Groq API ko call karein
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",  # Aap model ka naam badal sakte hain
        messages=messages, # Yahan hum puri chat history bhej rahe hain
        temperature=1,
        max_completion_tokens=2046,
        top_p=1,
        stream=True,
        stop=None
    )

    # Response ko stream karein aur print karein
    print("Bot:", end=" ")
    full_response = ""
    for chunk in completion:
        content = chunk.choices[0].delta.content
        if content:
            print(content, end="", flush=True)
            full_response += content

    # Bot ka response bhi chat history mein add karein
    messages.append({
        "role": "assistant",
        "content": full_response
    })

    print() # Nayi line ke liye