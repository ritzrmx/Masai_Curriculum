# Coding Problem: Embeddings & Vector Search

> **Session 5** | ⏱ 12–15 mins | Module 3: GenAI & Agents

---

## Scenario

Build semantic search over a small FAQ using local embeddings — find the best answer by meaning, not keywords.

> OpenRouter does not provide embeddings. This problem uses `sentence-transformers` (free, local).

---

## Setup

```bash
pip install sentence-transformers numpy
```

```python
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

faq = [
    "You can return items within 30 days of purchase.",
    "Standard delivery takes 5–7 business days.",
    "We accept credit cards, UPI, and net banking.",
    "All products include a 1-year warranty.",
]
```

---

## Tasks

**Task 1 — Embed FAQ**

```python
embeddings = model.encode(___)           # fill: faq
print("Shape:", embeddings.___)         # fill: shape → (4, 384)
```

---

**Task 2 — Cosine Similarity**

```python
def cosine_sim(a, b):
    return np.dot(a, b) / (np.linalg.norm(___) * np.linalg.norm(___))

query_vec = model.encode("How do I get my money back?")
scores = [cosine_sim(query_vec, embeddings[i]) for i in range(len(faq))]
best_idx = np.argmax(___)                # fill: scores
print("Best match:", faq[___])          # fill: best_idx
```

---

**Task 3 — Top-K Search**

```python
def search(query: str, top_k: int = 2):
    q = model.encode(___)                # fill: query
    scores = [cosine_sim(q, embeddings[i]) for i in range(len(faq))]
    ranked = np.argsort(scores)[::-1][:top_k]
    for rank, idx in enumerate(ranked, 1):
        print(f"{rank}. [{scores[idx]:.3f}] {faq[___]}")  # fill: idx

search("payment options for my order")
```

---

**Task 4 — Similarity Threshold**

```python
THRESHOLD = 0.4

query = "What's the weather today?"   # unrelated to FAQ
q_vec = model.encode(query)
max_score = max(cosine_sim(q_vec, embeddings[i]) for i in range(len(faq)))

if max_score >= ___:                    # fill: THRESHOLD
    print("Found answer")
else:
    print("No relevant FAQ found — escalate to human")
```

---

## Key Takeaways

- Embeddings capture meaning — similar phrases get similar vectors
- Cosine similarity measures how aligned two vectors are
- Set a similarity threshold to avoid irrelevant retrievals
