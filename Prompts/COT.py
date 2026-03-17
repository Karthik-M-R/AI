"""
Chain-of-Thought (CoT) Agent
-----------------------------
This script implements an AI agent that follows a strict Chain-of-Thought
process. The agent reasons step-by-step using PLAN steps and produces
a final OUTPUT.

Flow:
  START  — User gives an input
  PLAN   — AI breaks the problem into steps (can be multiple)
  OUTPUT — AI gives the final answer
"""

import os
import json
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

# Load .env from the API_Integration folder
env_path = Path(__file__).resolve().parent.parent / "API_Integration" / ".env"
load_dotenv(dotenv_path=env_path)

System_prompt = """
You are a helpful AI assistant. You work by running a start, plan, and output loop.
For the given user query, analyse the query and break it down into sub-tasks.
- Strictly follow the given JSON output format.
- Only run one step at a time.
- The sequence of steps is START (where user gives an input), PLAN (that can be multiple times),
  and finally OUTPUT (to give the final answer).

Output JSON Format:
{ "step": "START" | "PLAN" | "OUTPUT", "content": "string" }

Example:
START: Hey, Can you solve 2 + 3 * 5 / 10
PLAN: { "step": "PLAN", "content": "Seems like user is interested in math problem" }
PLAN: { "step": "PLAN", "content": "Looking at the problem, we should solve this using BODMAS method" }
PLAN: { "step": "PLAN", "content": "Yes, The BODMAS is correct thing to be done here" }
PLAN: { "step": "PLAN", "content": "first we must multiply 3 * 5 which is 15" }
PLAN: { "step": "PLAN", "content": "Now the new equation is 2 + 15 / 10" }
PLAN: { "step": "PLAN", "content": "We must perform divide that is 15 / 10 = 1.5" }
PLAN: { "step": "PLAN", "content": "Now the new equation is 2 + 1.5" }
PLAN: { "step": "PLAN", "content": "Now finally lets perform the add 3.5" }
PLAN: { "step": "PLAN", "content": "Great, we have solved and finally left with 3.5 as ans" }
OUTPUT: { "step": "OUTPUT", "content": "3.5" }
"""

# Use Gemini API through OpenAI SDK compatibility layer
client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

message_history = [
    {"role": "system", "content": System_prompt}
]

user_query = input("🧑‍💻 INPUT:->  ")
message_history.append({"role": "user", "content": user_query})

while True:
    response = client.chat.completions.create(
        model="gemini-1.5-flash",
        response_format={"type": "json_object"},
        messages=message_history
    )

    raw_result = response.choices[0].message.content
    message_history.append({"role": "assistant", "content": raw_result})

    try:
        parsed_result = json.loads(raw_result)
    except json.JSONDecodeError:
        print("⚠️ Failed to parse response:", raw_result)
        break

    if parsed_result.get("step") == "START":
        print("🚀 START:", parsed_result.get("content"))
        continue

    if parsed_result.get("step") == "PLAN":
        print("🧠 PLAN:", parsed_result.get("content"))
        continue

    if parsed_result.get("step") == "OUTPUT":
        print("📦 OUTPUT:", parsed_result.get("content"))
        break
