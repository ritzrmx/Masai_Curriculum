# Coding Problem: Structured Outputs & Validation

> **Session 4** | ⏱ 12–15 mins | Module 3: GenAI & Agents

---

## Scenario

Extract structured product review data from free text and validate it with Pydantic before using it downstream.

---

## Setup

```python
import openai, json, os
from pydantic import BaseModel, ValidationError
from typing import List

client = openai.OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)
MODEL = "meta-llama/llama-3.3-70b-instruct:free"

review_text = "Great noise-cancelling headphones! Battery lasts 30 hours. Only downside: pricey at ₹8,999."
```

---

## Tasks

**Task 1 — Define Schema**

```python
class ProductReview(BaseModel):
    product_type:   str
    sentiment:      str          # positive / negative / mixed
    pros:           List[str]
    cons:           List[str]
    price_mentioned: bool
```

---

**Task 2 — Extract with JSON Mode**

```python
def extract_review(text: str) -> ProductReview:
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "Extract review fields as JSON matching the schema."},
            {"role": "user", "content": ___}          # fill: text
        ],
        response_format={"type": "___"},             # fill: json_object
        temperature=0
    )
    data = json.loads(response.choices[0].message.___)  # fill: content
    return ProductReview(**___)                          # fill: data
```

---

**Task 3 — Validate**

```python
try:
    review = extract_review(___)                    # fill: review_text
    print("Type:", review.___)
    print("Sentiment:", review.___)
    print("Pros:", review.___)
except ValidationError as e:
    print("Invalid output:", e)
```

---

**Task 4 — Schema as Prompt Guide**

```python
schema_hint = {
    "type": "object",
    "properties": {
        "product_type": {"type": "string"},
        "sentiment": {"type": "string", "enum": ["positive", "negative", "mixed"]},
        "pros": {"type": "array", "items": {"type": "string"}},
        "cons": {"type": "array", "items": {"type": "string"}},
        "price_mentioned": {"type": "boolean"}
    },
    "required": ["product_type", "sentiment", "pros", "cons", "price_mentioned"]
}

# Include schema_hint in your system message for clearer outputs
```

---

## Key Takeaways

- `response_format={"type": "json_object"}` forces valid JSON
- Pydantic validates types and required fields after parsing
- JSON schemas in prompts improve extraction accuracy
