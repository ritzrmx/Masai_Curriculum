# Coding Problem: Evaluation and Deployment

> **Session 10** | ⏱ 12–15 mins | Module 3: GenAI & Agents

---

## Scenario

Evaluate a prompt on a small test set before deployment — measure accuracy and track failures for iteration.

---

## Setup

```python
import openai, os

client = openai.OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)
MODEL = "meta-llama/llama-3.3-70b-instruct:free"

# Test set: sentiment classification
test_cases = [
    {"text": "I love this product!", "expected": "positive"},
    {"text": "Terrible experience, never again.", "expected": "negative"},
    {"text": "It works fine, nothing special.", "expected": "neutral"},
    {"text": "Best purchase I've made this year!", "expected": "positive"},
    {"text": "Completely broken on arrival.", "expected": "negative"},
]

def classify(text: str) -> str:
    r = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "Classify sentiment as: positive, negative, or neutral. One word only."},
            {"role": "user", "content": text}
        ],
        temperature=0,
        max_tokens=10
    )
    return r.choices[0].message.content.strip().lower()
```

---

## Tasks

**Task 1 — Run Evaluation**

```python
correct = 0
failures = []

for case in test_cases:
    predicted = classify(case["___"])              # fill: text
    if predicted == case["___"]:                   # fill: expected
        correct += 1
    else:
        failures.append({
            "text": case["text"],
            "expected": case["expected"],
            "got": predicted
        })

accuracy = correct / len(___)                    # fill: test_cases
print(f"Accuracy: {accuracy:.0%} ({correct}/{len(test_cases)})")
```

---

**Task 2 — Failure Report**

```python
for f in failures:
    print(f"Text: {f['text']}")
    print(f"  Expected: {f['expected']}, Got: {f['___']}")  # fill: got
    print()
```

---

**Task 3 — Deployment Checklist**

```python
checklist = {
    "API key in env (not code)":     os.getenv("OPENROUTER_API_KEY") is not None,
    "Temperature set to 0 for eval": True,
    "Test accuracy >= 60%":          accuracy >= ___ ,   # fill: 0.6
    "Error handling in place":       True,
}

for item, passed in checklist.items():
    status = "✓" if passed else "✗"
    print(f"{status} {item}")
```

---

**Task 4 — Version Tag**

```python
DEPLOYMENT_CONFIG = {
    "model": MODEL,
    "prompt_version": "v1.0",
    "eval_accuracy": round(accuracy, 2),
    "test_set_size": len(___),                     # fill: test_cases
}

print("Deploy config:", DEPLOYMENT_CONFIG)
```

---

## Key Takeaways

- Always evaluate on a held-out test set before deploying
- Track failures — they guide prompt improvements
- Version your prompts and log eval scores with each deployment
