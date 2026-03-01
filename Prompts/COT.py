"""
Chain-of-Thought (CoT) Prompting
---------------------------------
Chain-of-Thought prompting is a technique where you instruct the AI model to
THINK STEP-BY-STEP before giving the final answer. Instead of jumping directly
to the output, the model breaks down the problem into logical steps, reasons
through each one, and then produces the final result.

Key characteristics:
  - The system prompt enforces a structured thinking process.
  - The model must follow a defined format: START → PLAN → OUTPUT.
  - Rules and constraints guide the model's reasoning behavior.
  - Best for tasks requiring logic, analysis, debugging, or multi-step reasoning.

Comparison:
  - Zero-shot:  "Solve this problem"                         → Direct answer, no reasoning shown
  - Few-shot:   "Here are examples... Now solve this"        → Learns pattern from examples
  - CoT:        "Think step-by-step and show your reasoning"  → Forces structured reasoning
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

# Load .env from the API_Integration folder
env_path = Path(__file__).resolve().parent.parent / "API_Integration" / ".env"
load_dotenv(dotenv_path=env_path)

# Chain-of-Thought system prompt — forces structured, step-by-step reasoning in JSON format
System_prompt = """
You are a helpful AI coding assistant named Codzii.
You must follow a strict Chain-of-Thought process for EVERY response.

Your response MUST be a valid JSON object with exactly these three keys:

{
    "start": "State what the user is asking. Identify the core topic or problem.",
    "plan": [
        "Step 1: ...",
        "Step 2: ...",
        "Step 3: ..."
    ],
    "output": "Provide the final, clear, and concise answer or solution here. Include code examples if the question is about coding."
}

Rules:
1. You MUST always respond in valid JSON with "start", "plan", and "output" keys. Never skip a key.
2. The "plan" value MUST be an array of strings, each representing one reasoning step.
3. Only answer questions related to coding and programming.
4. If the user asks a non-coding question, set "output" to:
   "I am Codzii, a coding assistant. I can only help with coding-related questions."
5. In "plan", break down your reasoning into small, logical steps.
6. In "output", give a clear and complete answer with examples when possible.
7. Keep explanations beginner-friendly but technically accurate.
8. If the question involves debugging, explain what went wrong step-by-step in "plan".
9. Do NOT include any text outside the JSON object. Output ONLY the JSON.
"""

# Use Gemini API through OpenAI SDK compatibility layer
client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Chain-of-Thought with few-shot examples in JSON format.
# We provide examples so the model sees the exact JSON structure we expect,
# combined with the CoT system prompt that enforces step-by-step reasoning.
response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {"role": "system", "content": System_prompt},

        # Example 1 — demonstrates the JSON CoT format for a simple concept
        {"role": "user", "content": "Explain list comprehension in Python"},
        {"role": "assistant", "content": '{"start": "The user wants to understand list comprehension in Python — a concise way to create lists.", "plan": ["Step 1: Define what list comprehension is.", "Step 2: Show the basic syntax: [expression for item in iterable].", "Step 3: Compare it with a traditional for-loop approach.", "Step 4: Provide a practical example."], "output": "List comprehension is a concise, Pythonic way to create lists in a single line.\\n\\nSyntax: `new_list = [expression for item in iterable if condition]`\\n\\nTraditional way:\\n```python\\nsquares = []\\nfor x in range(5):\\n    squares.append(x ** 2)\\n```\\n\\nWith list comprehension:\\n```python\\nsquares = [x ** 2 for x in range(5)]  # [0, 1, 4, 9, 16]\\n```\\n\\nYou can also add conditions:\\n```python\\neven_squares = [x ** 2 for x in range(10) if x % 2 == 0]  # [0, 4, 16, 36, 64]\\n```"}'},

        # Example 2 — demonstrates the JSON CoT format for a debugging question
        {"role": "user", "content": "Why am I getting IndexError in Python?"},
        {"role": "assistant", "content": '{"start": "The user is encountering an IndexError in Python and wants to understand why it happens and how to fix it.", "plan": ["Step 1: Explain what IndexError means.", "Step 2: Identify common causes — accessing an index that does not exist.", "Step 3: Show an example that triggers the error.", "Step 4: Provide solutions to prevent it."], "output": "IndexError occurs when you try to access an index that is out of range for a list or sequence.\\n\\nExample that causes the error:\\n```python\\nfruits = [\'apple\', \'banana\', \'cherry\']\\nprint(fruits[5])  # IndexError: list index out of range\\n```\\n\\nThe list has indices 0, 1, 2 — but index 5 does not exist.\\n\\nHow to prevent it:\\n```python\\n# Check length before accessing\\nif len(fruits) > 5:\\n    print(fruits[5])\\n\\n# Or use try-except\\ntry:\\n    print(fruits[5])\\nexcept IndexError:\\n    print(\'Index out of range!\')\\n```"}'},

        # Actual question — the model will now follow the same JSON CoT pattern
        {"role": "user", "content": "Explain how to reverse a linked list in Python"}
    ]
)

print(response.choices[0].message.content)
