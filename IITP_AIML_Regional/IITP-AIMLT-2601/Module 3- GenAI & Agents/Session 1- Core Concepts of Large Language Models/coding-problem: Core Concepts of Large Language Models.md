# Coding Problem: Core Concepts of Large Language Models

> **Session 1** | ⏱ 10–12 mins | Module 3: GenAI & Agents

---

## Scenario

You are exploring how LLMs work under the hood — how text is broken into tokens, how temperature affects randomness, and how context windows limit what the model can "see" at once.

---

## Setup

```python
import openai
import os

# OpenRouter — free LLM API (OpenAI-compatible)
client = openai.OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

MODEL = "meta-llama/llama-3.3-70b-instruct:free"
```

---

## Dataset / Context

```python
sample_text = "Artificial intelligence is transforming the world of data science and engineering."

messages_short = [
    {"role": "user", "content": "What is 2 + 2?"}
]

messages_long = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Explain what a token is in the context of LLMs in one sentence."}
]
```

---

## Tasks

**Task 1 — Token Counting (no API needed)**

Using the `tiktoken` library, count how many tokens `sample_text` uses (GPT-4 tokeniser is a close approximation for most modern LLMs).

```python
import tiktoken

enc = tiktoken.encoding_for_model("gpt-4")

# Count tokens in sample_text
tokens = enc.encode(___)
print("Token count:", ___)
print("Tokens (first 10):", tokens[:10], "...")
```

**Expected output (approximate):**
```
Token count: 13
Tokens (first 10): [8989, 16895, 11, ...] ...
```

---

**Task 2 — Temperature: Deterministic vs Creative**

Call the API twice for the same prompt — once with `temperature=0` and once with `temperature=1.2`. Observe the difference.

```python
prompt = "Complete this sentence in one line: The best way to learn AI is to..."

for temp in [0.0, 1.2]:
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=___,      # fill: the loop variable
        max_tokens=30
    )
    print(f"Temp={temp}: {response.choices[0].message.___}")   # fill: content attribute
```

> Run each temperature value 3 times. Which one gives the same answer every time?

---

**Task 3 — Token Usage Inspection**

Call the API for `messages_long` and inspect how many tokens the request consumed.

```python
response = client.chat.completions.create(
    model=MODEL,
    messages=___,    # fill: messages_long
    max_tokens=60
)

usage = response.___       # fill: usage attribute
print("Prompt tokens: ",   usage.___)     # fill
print("Response tokens:",  usage.___)     # fill
print("Total tokens:",     usage.___)     # fill
print("Reply:", response.choices[0].message.content)
```

**Expected shape:**
```
Prompt tokens:  28
Response tokens: 38
Total tokens:   66
Reply: A token is a unit of text...
```

---

**Task 4 — Context Window Awareness**

The model `meta-llama/llama-3.3-70b-instruct:free` has a **131,072 token** context window.

Given the token counts below, will each request fit in context? Fill in `True` or `False`.

```python
context_limit = 131_072

requests = {
    "Short chat (50 tokens)":        50,
    "10-page report (8,000 tokens)": 8_000,
    "Full novel (200,000 tokens)":   200_000,
    "1-hour transcript (90K tokens)":90_000,
}

for desc, tokens in requests.items():
    fits = tokens ___ context_limit    # fill: comparison operator
    print(f"{desc}: fits={fits}")
```

---

## Key Takeaways

- Tokens ≠ words — punctuation, spaces, and subwords all count
- `temperature=0` → deterministic output; higher values introduce randomness
- Every request consumes tokens from a finite context window — design prompts efficiently
