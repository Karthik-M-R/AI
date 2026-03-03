# Prompt Styles for LLMs

Three common formats used to structure prompts when working with open-source LLMs.

---

## 1. Alpaca Format

Used by: **Stanford Alpaca**, fine-tuned LLaMA models

The Alpaca format has 3 fields — **Instruction**, **Input** (optional), and **Response**.

### Structure
```
### Instruction:
{Tell the model what to do}

### Input:
{Optional extra context}

### Response:
{Model answers here}
```

### Example — With Input
```
### Instruction:
Translate the following English sentence to French.

### Input:
Hello, how are you?

### Response:
Bonjour, comment allez-vous ?
```

### Example — Without Input
```
### Instruction:
Write a Python function that adds two numbers.

### Response:
def add(a, b):
    return a + b
```

> **When to use:** Fine-tuning or prompting Alpaca-style models for task-based instructions.

---

## 2. ChatML Format

Used by: **OpenAI (GPT)**, **Mistral**, **many modern chat models**

ChatML uses role-based tags — `system`, `user`, and `assistant`.

### Structure
```
<|im_start|>system
{System instructions}
<|im_end|>

<|im_start|>user
{User's message}
<|im_end|>

<|im_start|>assistant
{Model answers here}
<|im_end|>
```

### Example
```
<|im_start|>system
You are a helpful coding assistant.
<|im_end|>

<|im_start|>user
What is a dictionary in Python?
<|im_end|>

<|im_start|>assistant
A dictionary stores key-value pairs, like a real dictionary stores words and definitions.

my_dict = {"name": "Karthik", "age": 21}
print(my_dict["name"])  # Karthik
<|im_end|>
```

> **When to use:** ChatGPT-style conversations, multi-turn chat with system instructions.

---

## 3. INST Format (Llama 2)

Used by: **Meta's Llama 2** chat models

Uses `[INST]` and `[/INST]` tags to wrap user messages. System prompt goes inside `<<SYS>>` tags.

### Structure
```
<s>[INST] <<SYS>>
{System prompt}
<</SYS>>

{User's message} [/INST]

{Model answers here} </s>
```

### Example — Single Turn
```
<s>[INST] <<SYS>>
You are a helpful coding assistant. Keep answers short.
<</SYS>>

How do I read a file in Python? [/INST]

with open("data.txt", "r") as f:
    content = f.read()
    print(content) </s>
```

### Example — Multi Turn
```
<s>[INST] <<SYS>>
You are a helpful assistant.
<</SYS>>

What is a loop? [/INST]

A loop repeats a block of code multiple times. </s>

<s>[INST] Give me an example. [/INST]

for i in range(5):
    print(i)  # prints 0 to 4 </s>
```

> **When to use:** Running or fine-tuning Llama 2 chat models locally.

---

## Quick Comparison

| Feature         | Alpaca              | ChatML                | INST (Llama 2)         |
|-----------------|---------------------|-----------------------|------------------------|
| **Tags**        | `### Instruction:`  | `<\|im_start\|>role`  | `[INST]` `[/INST]`    |
| **System role** | Not separate        | `system` role         | `<<SYS>>` block       |
| **Multi-turn**  | ❌ Single task       | ✅ Yes                | ✅ Yes                 |
| **Used by**     | Alpaca, early LLaMA | GPT, Mistral          | Llama 2 Chat           |
| **Best for**    | Task instructions   | Chat applications     | Llama 2 local models   |
