# Embeddings and Semantic Retrieval Systems
---

## Mental Map

```mermaid
%%{init: {'flowchart': {'nodeSpacing': 55, 'rankSpacing': 65, 'diagramPadding': 24}}}%%
flowchart TB
linkStyle default stroke-width:3px

subgraph foundation[" Foundation "]
direction TB
    P0["<b>Previous Module</b><br/>Foundations of Data<br/><i>[Python · Data Stack]</i><br/><i>Learnt:</i> Python, NumPy, Pandas, SQL, viz, APIs"]
    P1["<b>Previous Module</b><br/>Classical ML<br/><i>[scikit-learn · Statistics]</i><br/><i>Learnt:</i> Regression, classification, ensembles, clustering"]
    CURMOD["<b>Current Module Until<br/>Previous Session</b><br/><i>GenAI & Agents</i><br/>Tokens · prompting<br/>Agents · tools · structured outputs<br/>JSON schemas · Pydantic"]
    CURSES["<b>Current Session</b><br/><b>Embeddings & Semantic Retrieval</b><br/><i>Shift:</i> Search meaning, not just keywords<br/>Embeddings · chunking<br/>Retrievers · vector stores"]
end

subgraph value[" Value "]
direction LR
    CVAL["<b>Course Value</b><br/>Foundation for grounded<br/>RAG applications"]
    RVAL["<b>Real-Life Value</b><br/>Q&A over your own documents<br/>and knowledge bases"]
end

P0 -.->|&nbsp;Builds&nbsp;| P1
P1 ==>|&nbsp;Foundation&nbsp;| CURMOD
CURMOD ==>|&nbsp;Progress&nbsp;| CURSES
CURSES ==>|&nbsp;Course Path&nbsp;| CVAL
CURSES ==>|&nbsp;Real-Life&nbsp;| RVAL

classDef prevBox fill:#E8F4FC,stroke:#2B6CB0,stroke-width:2px,color:#1A202C
classDef curModBox fill:#FFF8E6,stroke:#B7791F,stroke-width:2px,color:#1A202C
classDef curSessBox fill:#E6FFFA,stroke:#0D9488,stroke-width:3px,color:#1A202C
classDef valueBox fill:#F3E8FF,stroke:#7C3AED,stroke-width:2px,color:#1A202C
class P0,P1 prevBox
class CURMOD curModBox
class CURSES curSessBox
class CVAL,RVAL valueBox
```

## What You'll Learn

In this pre-read, you'll discover:

- What a **text embedding** is — and why it lets computers compare meaning
- How **document chunking** prepares large texts for embedding
- What **retrievers** are and how they find the most relevant chunks for a query
- What a **vector store** does and how it enables fast semantic search
- How semantic search differs from keyword search — and when each is better

---

## A. Text Embeddings — Meaning as Numbers

> 💡 **Analogy:** A map uses (latitude, longitude) coordinates to place every location. Nearby coordinates mean nearby locations. A **text embedding** is a coordinate system for meaning: texts that mean similar things get similar coordinates in a high-dimensional space.

**One-line definition:** A **text embedding** is a list of numbers (a vector) produced by a model trained to place semantically similar texts close together in a high-dimensional space.

```mermaid
flowchart LR
    T1["'How do I reset my password?'"] --> E["Embedding model"]
    T2["'I forgot my login credentials'"] --> E
    T3["'What is the weather in Mumbai?'"] --> E
    E --> V1["[0.12, −0.45, 0.88, ...]\n(1536 numbers)"]
    E --> V2["[0.13, −0.43, 0.85, ...]\n← very close to V1"]
    E --> V3["[−0.71, 0.22, −0.55, ...]\n← far from V1 and V2"]
```

**Cosine similarity** measures how close two embedding vectors are:

| Score | Meaning |
|---|---|
| 0.95–1.00 | Near-duplicate or paraphrase |
| 0.80–0.94 | Closely related — same topic |
| Below 0.60 | Likely unrelated |

Embeddings capture **synonyms, paraphrases, and related concepts** automatically — "Car", "automobile", and "vehicle" will embed near each other even though they share no words.

---

## B. Document Chunking — Preparing Text for Embedding

> 💡 **Analogy:** You cannot meaningfully summarise a 300-page book in one sentence. But you can summarise each chapter in one paragraph. **Chunking** is that chapter-by-chapter breakdown — splitting large documents into pieces that can each be embedded meaningfully.

**One-line definition:** **Document chunking** is the process of splitting source documents into smaller segments before embedding — balancing the need for focused, specific embeddings against the need for sufficient context in each retrieved piece.

```mermaid
flowchart LR
    D["Full document\n10,000 tokens"] --> C["Chunker"]
    C --> CH1["Chunk 1\n~300 tokens"]
    C --> CH2["Chunk 2\n~300 tokens"]
    C --> CHN["Chunk N\n~300 tokens"]
    CH1 --> E1["Embed → vector 1"]
    CH2 --> E2["Embed → vector 2"]
    CHN --> EN["Embed → vector N"]
    E1 & E2 & EN --> VS["Vector store"]
```

**Common chunking strategies:**

| Strategy | How | Best for |
|---|---|---|
| Fixed-size with overlap | Every N tokens, overlap of M tokens | General prose |
| By paragraph | Split on double newlines | When each paragraph = one idea |
| By section / heading | Split on `#` headers | Structured documents (policies, manuals) |

**Overlap matters:** A 50-token overlap between adjacent chunks means a concept spanning a boundary appears in both — neither chunk loses it. Typical overlap is 10–20% of chunk size.

**Chunk size guidelines:**

| Too small (< 100 tokens) | Just right (200–500 tokens) | Too large (> 1,000 tokens) |
|---|---|---|
| Loses context | Focused + useful context | Averages out meaning; imprecise retrieval |
| Embedding less meaningful | Good retrieval precision | Wastes context window when injected |

---

## C. Retrievers — Finding the Right Chunks

> 💡 **Analogy:** A librarian who has read every book can fetch the three most relevant pages for any question, even if the exact words never appear in the question. A **retriever** is that librarian — it matches the query's meaning to the stored chunks, not just the words.

**One-line definition:** A **retriever** is a component that takes a query, embeds it, and searches the vector store for the K most semantically similar chunks — returning them as context for the LLM.

```mermaid
flowchart LR
    Q["User query\n'What is the refund process?'"] --> QE["Embed query → query vector"]
    QE --> SEARCH["Find top-K similar vectors\nin vector store"]
    SEARCH --> RESULTS["Top 3 chunks:\n0.94: 'Refunds processed within 7 days...'\n0.88: 'To start a refund, email support@...'\n0.71: 'Non-refundable items include...'"]
```

**Retriever types:**

| Type | How it works | Best for |
|---|---|---|
| Dense (vector) | Cosine similarity on embeddings | Semantic / paraphrase queries |
| Sparse (BM25) | Keyword frequency matching | Exact term matches, codes, IDs |
| Hybrid | Combine dense + sparse scores | Production systems needing both |

**Choosing K (number of chunks to retrieve):**

- K too small (1–2): May miss the answer if it spans multiple chunks
- K too large (10+): Fills the context window with irrelevant content
- K = 3–5 is a good starting point for most tasks

---

## D. Vector Stores — Storing and Searching Embeddings

> 💡 **Analogy:** A traditional library catalogue searches by title or author keywords. A vector store is a library where every book has been "meaning-fingerprinted" and finding similar books is instant, regardless of whether the titles match.

**One-line definition:** A **vector store** is a database that stores embedding vectors alongside their source texts and provides fast nearest-neighbour search — returning the most semantically similar items to a query vector, even across millions of documents.

**How a vector store is built and used:**

```mermaid
flowchart TD
    subgraph indexing["Indexing (offline — run once)"]
        I1["Load and chunk documents"] --> I2["Embed each chunk"]
        I2 --> I3["Store vector + text + metadata in vector store"]
    end
    subgraph retrieval["Retrieval (online — every query)"]
        R1["Embed user query"] --> R2["Search vector store for top K"]
        R2 --> R3["Return chunks for context injection"]
    end
```

**Vector store options:**

| Tool | Type | Best for |
|---|---|---|
| FAISS | In-memory library | Prototypes, learning |
| Chroma | Local database | Learning + small projects |
| Pinecone | Managed cloud | Production at scale |
| pgvector | PostgreSQL extension | If already using Postgres |

**For this course:** Chroma is recommended — it runs locally, requires no account, and has a clean Python API.

---

## E. Semantic Search vs Keyword Search

> 💡 **Analogy:** Keyword search finds documents containing the exact words you typed. Semantic search finds documents that *mean* what you asked — even when every word is different. "Vehicle registration procedure" and "how to get a car licence" are zero keyword overlap but very high semantic similarity.

**One-line definition:** **Semantic search** retrieves documents by meaning similarity to the query, finding conceptually related content even when no exact words match; **keyword search** requires word-level overlap — each excels in different scenarios.

| Dimension | Keyword search | Semantic search |
|---|---|---|
| Matching basis | Exact word frequency | Meaning similarity |
| Handles synonyms | No | Yes |
| Handles paraphrases | No | Yes |
| Handles product codes / IDs | Yes (exact match) | Less reliable |
| Speed at large scale | Very fast | Fast with ANN index |
| Failure mode | Misses conceptual matches | May retrieve off-topic if poorly trained |

```mermaid
flowchart LR
    Q["Query: 'automobile insurance claim form'"] --> KW["Keyword search\nFinds: docs with 'automobile', 'insurance', 'claim', 'form'\nMisses: 'car insurance documentation'"]
    Q --> SEM["Semantic search\nFinds: 'car insurance documentation'\n'vehicle damage report template'\n'motor policy claim process'"]
```

**Hybrid search** combines both approaches — keyword search for exact IDs and product codes, semantic search for conceptual intent. Most production RAG systems use hybrid retrieval.

---

## Practice Exercises

**1. Pattern Recognition**  
Three sentences: "The server response time exceeded 2 seconds", "API latency went above 2000ms", "The network cable was unplugged." (a) Which two would you expect to have the highest embedding similarity? (b) Would a keyword search on "latency" find all three? (c) Would a semantic search on "slow server performance" find all three?

**2. Concept Detective**  
A developer embeds an entire 150-page policy manual as a single vector and searches it with user queries. The system retrieves the "entire manual" as the single matching document and injects all 150 pages into the context window, which immediately overflows. Using sections B and D, explain the two mistakes made and describe the corrected pipeline.

**3. Real-Life Application**  
Design the embedding and retrieval pipeline for three scenarios: (a) a university student asking questions about admission procedures, (b) a technician querying a database of 500 machine error codes and their solutions, (c) a sales rep searching for relevant case studies from a library of 200 customer success stories. For each: chunk strategy, K value, and whether to use pure semantic or hybrid search.

**4. Spot the Error**  
A developer chunks a 300-page HR manual into 3,000-token chunks (no overlap). A user asks "Is carry-forward of leaves allowed?" The answer spans two sentences: the last sentence of chunk 8 and the first sentence of chunk 9. The retriever returns chunk 7, 9, 11 — missing chunk 8 entirely. Using sections B and C, explain why the answer is incomplete and what two changes to the chunking strategy would fix it.

**5. Planning Ahead**  
You are building a semantic search system over 5,000 internal Confluence pages (company wiki). Each page is 500–3,000 words. Describe the full pipeline: (a) chunking strategy and size choice, (b) embedding model to use and why, (c) vector store selection and why, (d) K value for retrieval and reasoning, (e) whether to use keyword, semantic, or hybrid search for a mixed use case (topic questions AND searching by document title).

---

> ✅ **You're done!** You now understand embeddings (meaning as vectors), document chunking (preparing text for precise retrieval), retrievers (finding the right chunks), and vector stores (the infrastructure for semantic search). These are the building blocks for RAG. Next: **Retrieval-Augmented Generation (RAG) Basics**, where you will assemble these pieces into a complete question-answering system grounded in your own documents.
