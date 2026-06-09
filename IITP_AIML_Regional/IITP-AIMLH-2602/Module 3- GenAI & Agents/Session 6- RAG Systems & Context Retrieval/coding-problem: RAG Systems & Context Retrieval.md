# Coding Problem: RAG Systems & Context Retrieval

> **Session 6** | ⏱ 15 mins | Module 3: GenAI & Agents

---

## Scenario

Build a mini RAG pipeline: retrieve relevant HR policy chunks, inject them into the prompt, and generate a grounded answer.

---

## Setup

```bash
pip install openai sentence-transformers numpy
```

```python
import openai, os, numpy as np
from sentence_transformers import SentenceTransformer

embed_model = SentenceTransformer("all-MiniLM-L6-v2")
client = openai.OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)
MODEL = "meta-llama/llama-3.3-70b-instruct:free"

docs = [
    "Employees get 18 days paid leave per year. Apply 3 days in advance.",
    "Remote work allowed 3 days/week. Core hours: 10 AM–4 PM.",
    "Performance reviews in June and December. Ratings 1–5.",
]
```

---

## Tasks

**Task 1 — Embed Documents**

```python
doc_embeddings = embed_model.encode(___)    # fill: docs
```

---

**Task 2 — Retriever**

```python
def retrieve(query: str, top_k: int = 2):
    q_vec = embed_model.encode(___)
    scores = doc_embeddings @ q_vec
    top_idx = np.argsort(scores)[::-1][:___]   # fill: top_k
    return [docs[i] for i in ___]               # fill: top_idx
```

---

**Task 3 — RAG Answer**

```python
def rag_answer(question: str) -> str:
    context = "\n".join(retrieve(___))          # fill: question
    messages = [
        {"role": "system", "content": (
            "Answer using ONLY this context. If unknown, say 'I don't know'.\n\n"
            f"Context:\n{___}"                  # fill: context
        )},
        {"role": "user", "content": ___}        # fill: question
    ]
    r = client.chat.completions.create(model=MODEL, messages=messages, temperature=0)
    return r.choices[0].message.content
```

---

**Task 4 — Test**

```python
for q in ["How many leave days do I get?", "What is the stock option policy?"]:
    print(f"\nQ: {q}")
    print(f"A: {rag_answer(q)}")
```

---

## Key Takeaways

- RAG = Retrieve → Augment prompt → Generate
- Grounding prevents hallucination on unknown topics
- Retrieval quality directly limits answer quality
