# Coding Problem: Retrieval-Augmented Generation (RAG) Basics

> **Session 6** | ⏱ 15 mins | Module 3: GenAI & Agents

---

## Scenario

You are building a document Q&A bot for a company's internal HR policy. The LLM has no knowledge of these policies — you must retrieve the relevant chunk first and inject it into the context window before generating an answer.

---

## Setup

```bash
pip install openai sentence-transformers numpy
```

```python
import openai, os
import numpy as np
from sentence_transformers import SentenceTransformer

# Local embeddings — no API key needed
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

# OpenRouter — free LLM for generation
client = openai.OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

MODEL = "meta-llama/llama-3.3-70b-instruct:free"
```

---

## Knowledge Base (HR Policy Chunks)

```python
documents = [
    "Employees are entitled to 18 days of paid annual leave per year. Leave must be applied for at least 3 days in advance.",
    "Remote work is allowed up to 3 days per week. Employees must be available during core hours: 10 AM to 4 PM.",
    "The performance review cycle runs twice a year — in June and December. Ratings are on a scale of 1 to 5.",
    "Medical reimbursement is capped at ₹50,000 per year. Submit claims within 30 days of incurring the expense.",
    "Travel allowance is provided for client visits. Flights must be booked at least 5 days in advance through the travel portal.",
]
```

---

## Tasks

**Task 1 — Embed the Knowledge Base**

Embed all document chunks and store in a NumPy matrix.

```python
doc_embeddings = embed_model.encode(___)    # fill: documents list
print("Shape:", doc_embeddings.___)         # fill: shape → (5, 384)
```

---

**Task 2 — Retriever**

Write a function that returns the top-k most relevant document chunks for a query.

```python
def retrieve(query: str, top_k: int = 2) -> list[str]:
    q_vec  = embed_model.encode(___)                 # fill: query string
    scores = doc_embeddings @ q_vec                  # dot product similarity

    top_indices = np.argsort(scores)[::-1][:___]     # fill: top_k
    return [documents[i] for i in ___]               # fill: top_indices
```

---

**Task 3 — RAG: Augment + Generate**

Combine retrieval with generation. Fill in the prompt so the LLM uses **only the retrieved context**.

```python
def rag_answer(question: str) -> str:
    context_chunks = retrieve(___)                   # fill: question
    context        = "\n\n".join(context_chunks)

    messages = [
        {
            "role":    "system",
            "content": (
                "You are an HR assistant. Answer using ONLY the context below. "
                "If the answer is not in the context, say 'I don't have that information'.\n\n"
                f"Context:\n{___}"                   # fill: context variable
            )
        },
        {
            "role":    "user",
            "content": ___                           # fill: question
        }
    ]

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0
    )
    return response.choices[0].message.content
```

---

**Task 4 — Test the RAG Bot**

Run these queries. The third one should trigger the fallback response.

```python
questions = [
    "How many days of annual leave do I get?",
    "When are performance reviews held?",
    "What is the company's stock option policy?"   # not in the knowledge base
]

for q in questions:
    print(f"\nQ: {q}")
    print(f"A: {rag_answer(q)}")
    print("-" * 50)
```

---

## Key Takeaways

- RAG = **Retrieve** relevant chunks → **Augment** the prompt → **Generate** a grounded answer
- Embeddings (local) handle retrieval; the LLM (OpenRouter) handles generation — two separate steps
- Grounding the model prevents hallucination — it can only answer from what you provide
