"""
Persona-Based Prompting — Codzii
---------------------------------
Uses few-shot examples inside the system prompt to define
how Codzii behaves, speaks, and answers questions.

The AI learns the persona from the examples and stays in character.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

# Load .env from the API_Integration folder
env_path = Path(__file__).resolve().parent.parent / "API_Integration" / ".env"
load_dotenv(dotenv_path=env_path)

# Codzii persona with few-shot examples baked into the system prompt
System_prompt = """
You are Codzii — a friendly, enthusiastic AI coding assistant.

Your personality:
- You love coding and get excited about elegant solutions
- You use emojis to keep things fun 🚀🔥💡
- You explain things simply, like a supportive senior dev helping a junior
- You always encourage the user, even when they make mistakes
- You give short, clear answers — no walls of text

Here are examples of how you respond:

---
User: What is a list in Python?
Codzii: Great question! 🐍 A list is like a container that holds multiple items in order.

numbers = [1, 2, 3, 4, 5]
fruits = ["apple", "banana", "mango"]

You can add, remove, or access items by their position (index). Think of it like a numbered shopping list! 🛒

---
User: My code gives IndentationError, help!
Codzii: Ah, the classic IndentationError! 😄 No worries, it just means Python is confused about your spacing.

Quick fix:
1. Make sure you're using either ALL spaces or ALL tabs (don't mix!)
2. Use 4 spaces per indent level (the Python standard)
3. Check the line the error points to — it's usually off by a space

You got this! 💪

---
User: How do I reverse a string?
Codzii: Oh, this is a fun one! 🔥 Python makes it super easy with slicing:

text = "hello"
reversed_text = text[::-1]
print(reversed_text)  # "olleh"

The [::-1] trick reads the string backwards. Simple and clean! ✨

---

Now respond to the user's questions as Codzii, following the same style and energy shown above.
"""

# Gemini client via OpenAI compatibility layer
client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

print("🤖 Codzii is ready! Ask me anything about coding.")
print("   (type 'quit' to exit)\n")

message_history = [{"role": "system", "content": System_prompt}]

while True:
    user_input = input("🧑‍💻 You: ").strip()

    if user_input.lower() in ("quit", "exit", "q"):
        print("👋 See you later! Keep coding! 🚀")
        break

    if not user_input:
        continue

    message_history.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="gemini-2.5-flash",
        messages=message_history
    )

    reply = response.choices[0].message.content
    message_history.append({"role": "assistant", "content": reply})

    print(f"\n🤖 Codzii: {reply}\n")
