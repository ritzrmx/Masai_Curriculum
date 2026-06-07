# Coding Problem: Embeddings and Semantic Retrieval Systems

> **Session 5** | ⏱ 12–15 mins | Module 3: GenAI & Agents

---

## Scenario

You are building a semantic search engine for a small product catalogue. A user types a natural language query, and your system finds the most relevant product using cosine similarity on embeddings — not keyword matching.

---

## Setup

```python
import openai, os
import numpy as np

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
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

Write a function to get the embedding vector for a text string using OpenAI's API.

```python
def get_embedding(text: str) -> list[float]:
    response = client.embeddings.create(
        input=___,                          # fill: the text
        model="text-embedding-3-small"
    )
    return response.data[0].___             # fill: attribute for the vector

# Test it
vec = get_embedding("wireless headphones")
print("Vector size:", len(vec))             # should be 1536
```

---

**Task 2 — Embed the Catalogue**

Embed all products and store them in a NumPy matrix (one row per product).

```python
catalogue_embeddings = np.array([
    get_embedding(p) for p in ___           # fill: iterate products
])

print("Matrix shape:", catalogue_embeddings.___)   # fill: shape attribute
# Expected: (6, 1536)
```

---

**Task 3 — Cosine Similarity Search**

Fill in the cosine similarity function and use it to find the best match for a query.

```python
def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    return np.dot(a, b) / (np.linalg.norm(___) * np.linalg.norm(___))   # fill a, b

def search(query: str, top_k: int = 3):
    query_vec = np.array(get_embedding(___))     # fill: query text

    scores = [
        cosine_similarity(query_vec, catalogue_embeddings[i])
        for i in range(len(products))
    ]

    ranked = np.argsort(scores)[::-1][:top_k]    # top_k highest scores

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

**Expected top result (approximate):**
```
Query: 'I need something to listen to music without wires'
  1. [0.87xx] Wireless noise-cancelling headphones with 30-hour battery
```

---

## Bonus

Add one more product: `"Over-ear gaming headset with surround sound"`. Re-embed the catalogue and re-run the first query. Does it now compete with the wireless headphones?

---

## Key Takeaways

- Embeddings capture **meaning**, not keywords — similar concepts get similar vectors
- Cosine similarity measures angle between vectors (not magnitude) → range [−1, 1]
- Chunking long documents before embedding keeps vectors meaningful
