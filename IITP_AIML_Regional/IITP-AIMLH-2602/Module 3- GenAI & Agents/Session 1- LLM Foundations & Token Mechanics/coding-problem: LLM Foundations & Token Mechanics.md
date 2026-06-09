# Coding Problem: LLM Foundations & Token Mechanics

> **Session 1** | ⏱ 10–12 mins | Module 3: GenAI & Agents

---

## Scenario

You are exploring how LLMs work — token counts, temperature effects, and context window limits — before building any GenAI application.

---

## Setup

```python
import openai
import os

client = openai.OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

MODEL = "meta-llama/llama-3.3-70b-instruct:free"
```

---

## Tasks

**Task 1 — Token Counting**

```python
import tiktoken

enc = tiktoken.encoding_for_model("gpt-4")
text = "Large language models break text into tokens, not whole words."

tokens = enc.encode(___)
print("Token count:", ___)
print("First 5 tokens:", tokens[:5])
```

---

**Task 2 — Temperature Comparison**

```python
prompt = "In one sentence, explain what an LLM is."

for temp in [0.0, 1.2]:
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=___,
        max_tokens=40
    )
    print(f"Temp={temp}: {response.choices[0].message.___}")
```

---

**Task 3 — Token Usage**

```python
response = client.chat.completions.create(
    model=MODEL,
    messages=[{"role": "user", "content": "What is a context window?"}],
    max_tokens=50
)

usage = response.___
print("Prompt tokens:", usage.___)
print("Completion tokens:", usage.___)
print("Total tokens:", usage.___)
```

---

**Task 4 — Context Window Check**

```python
CONTEXT_LIMIT = 131_072   # Llama 3.3 70B free tier

sizes = {"Short chat": 500, "Long doc": 8000, "Full book": 200000}

for name, tokens in sizes.items():
    fits = tokens ___ CONTEXT_LIMIT
    print(f"{name}: fits={fits}")
```

---

## Key Takeaways

- Tokens are subword units — count them before scaling prompts
- `temperature=0` gives more consistent outputs
- Every request consumes tokens from a finite context window
