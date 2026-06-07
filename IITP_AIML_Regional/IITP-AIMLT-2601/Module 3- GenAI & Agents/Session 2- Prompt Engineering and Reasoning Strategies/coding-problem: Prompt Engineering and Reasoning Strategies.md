# Coding Problem: Prompt Engineering and Reasoning Strategies

> **Session 2** | ⏱ 12–15 mins | Module 3: GenAI & Agents

---

## Scenario

You are building a prompt testing harness to compare different prompting strategies — zero-shot, few-shot, and chain-of-thought — for a customer support classification task.

---

## Setup

```python
import openai, os

client = openai.OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

MODEL = "meta-llama/llama-3.3-70b-instruct:free"

def ask(messages, temperature=0):
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=temperature,
        max_tokens=150
    )
    return response.choices[0].message.content.strip()
```

---

## Tasks

**Task 1 — Zero-Shot Prompt**

Classify the customer message below with no examples — just a clear instruction.

```python
customer_msg = "My order hasn't arrived in 10 days. I'm very frustrated!"

zero_shot = [
    {"role": "system", "content": ___},   # fill: instruction to classify as Complaint / Inquiry / Compliment
    {"role": "user", "content": customer_msg}
]

print("Zero-shot:", ask(zero_shot))
```

---

**Task 2 — Few-Shot Prompt**

Add 3 examples to guide the model before the real query.

```python
few_shot = [
    {"role": "system", "content": "Classify customer messages as: Complaint, Inquiry, or Compliment."},
    {"role": "user",      "content": "I love your fast delivery!"},
    {"role": "assistant", "content": "Compliment"},
    {"role": "user",      "content": "Where is my refund?"},
    {"role": "assistant", "content": "___"},          # fill: Inquiry
    {"role": "user",      "content": "The product broke after one day."},
    {"role": "assistant", "content": "___"},          # fill: Complaint
    {"role": "user",      "content": customer_msg}
]

print("Few-shot:", ask(few_shot))
```

---

**Task 3 — Chain-of-Thought Prompt**

Ask the model to reason step-by-step before giving the final answer.

```python
cot_system = """Classify the customer message.
Think step by step:
1. Identify the emotion
2. Identify what they want
3. Then give the category: Complaint, Inquiry, or Compliment"""

cot = [
    {"role": "system", "content": ___},   # fill: use cot_system
    {"role": "user",   "content": customer_msg}
]

print("Chain-of-Thought:\n", ask(cot))
```

---

**Task 4 — Role Prompting**

Rewrite the system message so the model acts as a **senior customer support analyst** with 10 years of experience. Re-run classification and compare tone.

```python
role_prompt = [
    {"role": "system", "content": "You are ___. Classify: Complaint, Inquiry, or Compliment."},
    {"role": "user",   "content": customer_msg}
]

print("Role prompt:", ask(role_prompt))
```

> Compare all 4 outputs. Which strategy gives the most useful/accurate response?

---

## Key Takeaways

- Zero-shot is fast but can be vague; few-shot anchors the model with examples
- Chain-of-thought improves accuracy on reasoning tasks by externalising thinking
- Role prompting shapes tone and depth — useful for domain-specific tasks
