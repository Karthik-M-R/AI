"""
Running LLMs via Hugging Face
------------------------------
How it works:
  1. You pick a chat model from https://huggingface.co/models
  2. pipeline() downloads the model + tokenizer (cached after first run)
  3. You send messages with roles (system/user/assistant) just like ChatGPT/OpenAI API
  4. The model generates a response

We use "SmolLM2-360M-Instruct" — a tiny chat model (~700 MB, runs on CPU).
"""

from transformers import pipeline

# Create a text-generation pipeline with a small CHAT model
generator = pipeline("text-generation", model="HuggingFaceTB/SmolLM2-360M-Instruct")

# Use the messages format (same style as OpenAI API)
messages = [
    {"role": "system", "content": "You are a helpful assistant. Keep answers short."},
    {"role": "user", "content": "What is hugging face used for in 4 lines ?"},
]

result = generator(messages, max_new_tokens=100)

# Print only the assistant's reply
print("="* 60)
print(result[0]["generated_text"][-1]["content"])
print("="*60)
