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

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
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

Using the `tiktoken` library, count how many tokens are in `sample_text`.

```python
import tiktoken

enc = tiktoken.encoding_for_model("gpt-4o")

# Count tokens in sample_text
tokens = enc.encode(___)
print("Token count:", ___)
print("Tokens:", tokens[:10], "...")  # first 10 tokens
```

**Expected output:**
```
Token count: 13
Tokens: [8989, 16895, 11, ...] ...
```

---

**Task 2 — Temperature: Deterministic vs Creative**

Call the API twice for the same prompt — once with `temperature=0` and once with `temperature=1.2`. Observe the difference.

```python
prompt = "Complete this sentence in one line: The best way to learn AI is to..."

for temp in [0.0, 1.2]:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=___,
        max_tokens=30
    )
    print(f"Temp={temp}: {response.choices[0].message.___}")
```

> What do you notice between the two outputs? Which one is more consistent if you run it multiple times?

---

**Task 3 — Cost Estimation**

Given the following token usage stats, calculate the approximate cost.

```python
# GPT-4o-mini pricing (as of 2024)
INPUT_PRICE_PER_1K  = 0.000150   # $ per 1K input tokens
OUTPUT_PRICE_PER_1K = 0.000600   # $ per 1K output tokens

input_tokens  = 520
output_tokens = 180

# Calculate cost
input_cost  = (input_tokens / 1000) * ___
output_cost = (___ / 1000) * OUTPUT_PRICE_PER_1K
total_cost  = ___ + ___

print(f"Input cost:  ${input_cost:.6f}")
print(f"Output cost: ${output_cost:.6f}")
print(f"Total cost:  ${total_cost:.6f}")
```

**Expected output:**
```
Input cost:  $0.000078
Output cost: $0.000108
Total cost:  $0.000186
```

---

## Bonus

Modify Task 2 to also print `response.usage.total_tokens`. How many tokens did each call use?

---

## Key Takeaways

- Tokens ≠ words — punctuation and subwords count separately
- `temperature=0` → deterministic; higher values → more creative/random
- Every token has a cost — efficient prompts save money at scale
