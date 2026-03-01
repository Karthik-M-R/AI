"""
Automated Chain-of-Thought (Auto-CoT) Prompting
-------------------------------------------------
Auto-CoT makes Chain-of-Thought prompting INTERACTIVE. Instead of hardcoding
the user's question, the script gathers input from the terminal and displays
the AI's step-by-step reasoning one by one.

Flow:
  🧑‍💻 User types a coding question
  � START  — AI restates what was asked
  🧠 PLAN   — AI breaks the problem into steps
  📦 OUTPUT — AI gives the final answer
"""

import os
import json
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

# Load .env from the API_Integration folder
env_path = Path(__file__).resolve().parent.parent / "API_Integration" / ".env"
load_dotenv(dotenv_path=env_path)

# System prompt — AI responds ONE step at a time
System_prompt = """
You are a helpful AI coding assistant named Codzii.
You must follow a strict Chain-of-Thought process.

IMPORTANT: You must respond ONE STEP at a time. Each response is a JSON object with "step" and "content".

Step 1 — When the user asks a question, respond with:
{"step": "START", "content": "Restate what the user is asking."}

Step 2 — After your START response appears in the conversation, respond with:
{"step": "PLAN", "content": "Step 1: ...\\nStep 2: ...\\nStep 3: ..."}

Step 3 — After your PLAN response appears in the conversation, respond with:
{"step": "OUTPUT", "content": "The final answer with code examples."}

Rules:
1. Respond with ONLY ONE step per message. Never combine steps.
2. The "step" value must be exactly "START", "PLAN", or "OUTPUT".
3. Only answer coding-related questions.
4. If non-coding question, set content to: "I am Codzii, a coding assistant. I can only help with coding-related questions."
5. Do NOT include any text outside the JSON. Output ONLY the JSON.
"""

# Use Gemini API through OpenAI SDK compatibility layer
client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

message_history = [{"role": "system", "content": System_prompt}]

user_query = input("🧑‍💻 INPUT:->> ")
message_history.append({"role": "user", "content": user_query})

while True:
    response = client.chat.completions.create(
        model="gemini-1.5-flash",
        response_format={"type": "json_object"},
        messages=message_history
    )

    raw_result = response.choices[0].message.content
    message_history.append({"role": "assistant", "content": raw_result})

    parsed_result = json.loads(raw_result)

    if parsed_result.get("step") == "START":
        print("�", parsed_result.get("content"))
        continue

    if parsed_result.get("step") == "PLAN":
        print("🧠", parsed_result.get("content"))
        continue

    if parsed_result.get("step") == "OUTPUT":
        print("📦", parsed_result.get("content"))
        break
