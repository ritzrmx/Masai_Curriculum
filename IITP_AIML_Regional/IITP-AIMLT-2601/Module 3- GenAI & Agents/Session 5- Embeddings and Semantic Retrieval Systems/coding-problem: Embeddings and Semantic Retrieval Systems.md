# Coding Problem: Embeddings and Semantic Retrieval Systems

> **Session 5** | ⏱ 12–15 mins | Module 3: GenAI & Agents

---

## Scenario

You are building a semantic search engine for a small product catalogue. A user types a natural language query, and your system finds the most relevant product using cosine similarity on embeddings — not keyword matching.

> **Note:** OpenRouter does not provide an embeddings endpoint. This problem uses `sentence-transformers`, a free local library that generates high-quality embeddings with no API key required.

---

## Setup

```bash
pip install sentence-transformers numpy
```

```python
import numpy as np
from sentence_transformers import SentenceTransformer

# Loads a small, fast model (~90 MB, runs on CPU)
model = SentenceTransformer("all-MiniLM-L6-v2")
```

---

## Product Catalogue

```python
products = [
    "Wireless noise-cancelling headphones with 30-hour battery",
    "Portable Bluetooth speaker with waterproof design",
    "USB-C laptop charger 65W fast charging",
    "Mechanical keyboard with RGB backlight",
    "Smart fitness tracker with heart rate monitor",
    "4K webcam for video conferencing",
]
```

---

## Tasks

**Task 1 — Generate Embeddings**

Embed all products at once and check the shape of the output matrix.

```python
# Embed all products in one call
catalogue_embeddings = model.encode(___)    # fill: pass the products list

print("Type:", type(catalogue_embeddings))
print("Shape:", catalogue_embeddings.___)   # fill: shape attribute
# Expected: (6, 384)  — 6 products, 384-dim vectors
```

---

**Task 2 — Cosine Similarity**

Fill in the cosine similarity function — it measures how similar two vectors are regardless of their magnitude.

```python
def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    return np.dot(___, ___) / (np.linalg.norm(___) * np.linalg.norm(___))
    # fill all four blanks with: a, b, a, b
```

Test it manually:

```python
v1 = model.encode("wireless headphones")
v2 = model.encode("bluetooth earbuds")
v3 = model.encode("laptop charger")

print("headphones vs earbuds:", round(cosine_similarity(v1, v2), 4))  # high similarity
print("headphones vs charger:", round(cosine_similarity(v1, v3), 4))  # low similarity
```

---

**Task 3 — Semantic Search**

Fill in the search function to find the top-k most relevant products for any query.

```python
def search(query: str, top_k: int = 3):
    query_vec = model.encode(___)            # fill: query string

    scores = [
        cosine_similarity(query_vec, catalogue_embeddings[i])
        for i in range(len(products))
    ]

    ranked = np.argsort(scores)[::-1][:top_k]

    print(f"\nQuery: '{query}'")
    for rank, idx in enumerate(ranked, 1):
        print(f"  {rank}. [{scores[idx]:.4f}] {products[___]}")   # fill: idx
```

---

**Task 4 — Run Queries**

Test the search with these queries. Do the results make intuitive sense?

```python
search("I need something to listen to music without wires")
search("track my steps and health")
search("charge my MacBook quickly")
```

**Expected top result for query 1 (approximate):**
```
Query: 'I need something to listen to music without wires'
  1. [0.68xx] Wireless noise-cancelling headphones with 30-hour battery
```

---

## Bonus

Add one more product: `"Over-ear gaming headset with surround sound"`. Re-encode and re-run the first query. Does it now compete with the wireless headphones?

---

## Key Takeaways

- Embeddings capture **meaning**, not keywords — similar concepts get similar vectors
- `sentence-transformers` runs entirely locally — no API key, no cost, no rate limits
- Cosine similarity measures the angle between vectors (not magnitude) → range [−1, 1]
