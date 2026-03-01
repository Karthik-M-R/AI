"""
Zero-Shot Prompting
-------------------
Zero-shot prompting is a technique where you ask the AI model to perform a task
WITHOUT providing any examples. You simply give a direct instruction or question,
and the model relies entirely on its pre-trained knowledge to generate a response.

Key characteristics:
  - No examples are provided in the prompt (zero "shots" / examples).
  - The model uses only the instruction + its training data to respond.
  - Best for straightforward tasks the model already understands well.

Comparison:
  - Zero-shot:  "Explain file handling in Python"           → No examples given
  - One-shot:   "Here is one example... Now do this"        → 1 example given
  - Few-shot:   "Here are a few examples... Now do this"    → 2+ examples given
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

# Load .env from the API_Integration folder
env_path = Path(__file__).resolve().parent.parent / "API_Integration" / ".env"
load_dotenv(dotenv_path=env_path)

# System prompt — sets the AI's role/behavior (not an example, just an instruction)
System_prompt="You are a coding assistant.Only answer question related to coding.If user asks other question just say i am codzii (ur name) ,i am just coding assistant cant answer other question"


# Use Gemini API through OpenAI SDK compatibility layer
client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Zero-shot: We directly ask the question without giving any examples.
# The model must figure out the answer purely from its training knowledge.
response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {"role": "system", "content": System_prompt},
        {"role": "user", "content": "Explain python program for file handling"}  # Direct question, no examples = zero-shot
    ]
)

print(response.choices[0].message.content)
