"""
Few-Shot Prompting
------------------
Few-shot prompting is a technique where you provide the AI model with a FEW
EXAMPLES (2 or more) of the desired input-output pattern before asking it to
perform the actual task. This helps the model understand the format, tone,
and style you expect in the response.

Key characteristics:
  - Multiple examples are provided in the prompt (few "shots" / examples).
  - The model learns the pattern from the examples and applies it to the new query.
  - Best for tasks where you need consistent formatting, specific style, or
    when the model might misunderstand the task without examples.

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

# System prompt — sets the AI's role/behavior
System_prompt = "You are a coding assistant. Only answer questions related to coding. If user asks other questions just say I am Codzii (your name), I am just a coding assistant, can't answer other questions."

# Use Gemini API through OpenAI SDK compatibility layer
client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Few-shot: We provide multiple examples of the desired input-output pattern
# BEFORE asking the actual question. This teaches the model the format we expect.
response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {"role": "system", "content": System_prompt},

        # Example 1 — shows the model how we want the answer structured
        {"role": "user", "content": "Explain list in Python"},
        {"role": "assistant", "content": "List is a built-in data structure in Python that stores an ordered collection of items. Example: fruits = ['apple', 'banana', 'cherry']. Lists are mutable, meaning you can add, remove, or change items after creation."},

        # Example 2 — reinforces the pattern (short, clear, with an example)
        {"role": "user", "content": "Explain dictionary in Python"},
        {"role": "assistant", "content": "Dictionary is a built-in data structure in Python that stores data in key-value pairs. Example: student = {'name': 'John', 'age': 20}. Dictionaries are mutable and keys must be unique."},

        # Actual question — the model will now follow the same pattern from above
        {"role": "user", "content": "Explain tuple in Python"}  # The model should answer in the same style as the examples
    ]
)

print(response.choices[0].message.content)
