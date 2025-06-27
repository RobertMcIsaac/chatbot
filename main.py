import os
from dotenv import load_dotenv
import openai
from openai import APIConnectionError, AuthenticationError

load_dotenv()

api_key=os.getenv("OPENAI_API_KEY")

if not api_key:
    raise Exception("API key is missing")

try:
    client = openai.OpenAI(api_key=api_key)
except AuthenticationError:
    raise Exception("API key is invalid")

system_message = "Repond in the tone of Samwise Gamgee from Lord of the Rings"
# system_message = input("Set the bot's behavior:")

history = [{"role": "system", "content": system_message}]

def ask_openai(prompt):
    history.append({"role": "user", "content": prompt})
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=history,
            temperature=1.0
        )
        reply = response.choices[0].message.content
        history.append({"role": "assistant", "content": reply})
        return reply
    except APIConnectionError:
        return "Could not connect to OpenAI servers"
    except AuthenticationError:
        return "Authentication failed"

# Simple loop
while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        break
    reply = ask_openai(user_input)
    print("Bot:", reply)
