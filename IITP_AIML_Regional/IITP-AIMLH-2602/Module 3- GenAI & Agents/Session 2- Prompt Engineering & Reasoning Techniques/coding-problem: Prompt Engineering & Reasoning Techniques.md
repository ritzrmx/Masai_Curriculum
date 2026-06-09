# Coding Problem: Prompt Engineering & Reasoning Techniques

> **Session 2** | ⏱ 12–15 mins | Module 3: GenAI & Agents

---

## Scenario

Compare zero-shot, few-shot, and chain-of-thought prompting on a support ticket classification task.

---

## Setup

```python
import openai, os

client = openai.OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)
MODEL = "meta-llama/llama-3.3-70b-instruct:free"

def ask(messages):
    r = client.chat.completions.create(model=MODEL, messages=messages, temperature=0, max_tokens=120)
    return r.choices[0].message.content.strip()

ticket = "I've been waiting 12 days for my refund. This is unacceptable!"
```

---

## Tasks

**Task 1 — Zero-Shot**

```python
zero_shot = [
    {"role": "system", "content": ___},   # classify as Complaint / Inquiry / Compliment
    {"role": "user", "content": ticket}
]
print("Zero-shot:", ask(zero_shot))
```

---

**Task 2 — Few-Shot**

```python
few_shot = [
    {"role": "system", "content": "Classify as: Complaint, Inquiry, or Compliment."},
    {"role": "user", "content": "Love your fast delivery!"},
    {"role": "assistant", "content": "Compliment"},
    {"role": "user", "content": "Where is my order?"},
    {"role": "assistant", "content": "___"},          # Inquiry
    {"role": "user", "content": ticket}
]
print("Few-shot:", ask(few_shot))
```

---

**Task 3 — Chain-of-Thought**

```python
cot = [
    {"role": "system", "content": "Classify the ticket. Think step by step, then give the category."},
    {"role": "user", "content": ___}                  # ticket
]
print("CoT:\n", ask(cot))
```

---

**Task 4 — Prompt Template**

```python
def classify_ticket(text: str) -> str:
    template = """You are a support analyst.
Ticket: {ticket}
Category (one word): Complaint, Inquiry, or Compliment"""

    messages = [{"role": "user", "content": template.format(___=text)}]  # fill: ticket
    return ask(messages)

print(classify_ticket(ticket))
```

---

## Key Takeaways

- Few-shot anchors the model with examples
- Chain-of-thought improves reasoning tasks
- Templates make prompts reusable and consistent
