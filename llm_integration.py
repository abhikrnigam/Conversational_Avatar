from groq import Groq
import os
from dotenv import load_dotenv
load_dotenv()


client = Groq(api_key=os.getenv("GROQ_API_KEY"))


messages = []
system_message = ""


while True:
    user_input = input(" You : ")

    
    if user_input.lower() == 'quit':
        print("Chat band ho gayi. Alvida!")
        break

    
    messages.append({
        "role": "user",
        "content": user_input
    })

    
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",  
        messages=messages, 
        temperature=1,
        max_completion_tokens=2046,
        top_p=1,
        stream=True,
        stop=None
    )

    
    print("Bot:", end=" ")
    full_response = ""
    for chunk in completion:
        content = chunk.choices[0].delta.content
        if content:
            print(content, end="", flush=True)
            full_response += content

    
    messages.append({
        "system":system_message,
        "role": "assistant",
        "content": full_response
    })

    print() 