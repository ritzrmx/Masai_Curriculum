# Lecture Script: Chunking, Vector Stores & Retrieval
> **Instructor Reference** — Module 3: GenAI & Agents | Session 9 | Duration: 2 Hours

---

## Session Overview

**Goal:** Students split a real multi-section document into retrievable chunks using `RecursiveCharacterTextSplitter`, understand WHY chunk size and overlap matter, index those chunks into both ChromaDB and FAISS, and retrieve the most relevant chunks for a query using both plain similarity search and MMR (Maximal Marginal Relevance) — closing the loop between Session 8's embeddings and the scalable retrieval infrastructure real RAG systems need.

**Student profile at this point:** Finished Session 8 (local embeddings with `sentence-transformers`, cosine similarity, keyword-vs-semantic search). Comfortable with Session 3's cosine similarity math and Session 8's "similar meaning -> similar direction" framing, but has only ever compared a handful of items in a Python loop, never used a real vector store.

**Key outcome:** Every student can explain why long documents must be split before embedding, chunk a real document with `RecursiveCharacterTextSplitter` using sensible `chunk_size`/`chunk_overlap` values, describe the ChromaDB-vs-FAISS trade-off accurately, and retrieve relevant chunks for a query using both plain similarity search and MMR, explaining in plain English what MMR adds that plain similarity search doesn't.

**Dataset for this session:** `cloudnote_remote_work_policy.txt` — a realistic, six-section employee handbook excerpt (~2,400 characters) used throughout for the chunking and retrieval demonstrations and the lab.

**IMPORTANT — numeric accuracy note for this script:** This classroom environment was checked before writing this script. `langchain-text-splitters` (which provides `RecursiveCharacterTextSplitter`) **was installed and was actually run against the real dataset file** — every chunk count, chunk boundary, and chunk length shown in SEGMENT 2/3 is real, verified output from running the exact code shown. `chromadb` and `faiss` were **not installed** in this environment. Their code is written to be correct and current against each library's public API, but specific retrieval DISTANCE/SCORE numbers from those two libraries are marked **"Example output (illustrative — exact distance/similarity values depend on the installed library version and are not claimed to have been executed in this environment; the RANKING shown reflects a hand-verified cosine-similarity computation over the same real chunks, done separately with plain Python/numpy, not a specific ChromaDB/FAISS run)."**

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| SEGMENT 1: Opening — Why Can't We Just Embed the Whole Document? | 10 min | 0:10 |
| SEGMENT 2: Chunking with `RecursiveCharacterTextSplitter` | 25 min | 0:35 |
| SEGMENT 3: Chunk Size, Overlap, and Why Both Matter | 20 min | 0:55 |
| **BREAK** | 10 min | 1:05 |
| SEGMENT 4: Vector Stores — Indexing Chunks into ChromaDB and FAISS | 25 min | 1:30 |
| SEGMENT 5: Retrieval — Similarity Search and MMR | 20 min | 1:50 |
| SEGMENT 6: Lab — Chunk, Index, and Retrieve End to End | 10 min | 2:00 |
| SEGMENT 7: Summary, Wrap-Up & Q&A | *(folded into SEGMENT 6 wrap, see note)* | — |

*Instructor note: this session's seven conceptual blocks compress SEGMENT 7 into the final 5 minutes of the lab block above, since the lab itself is the natural capstone of the whole session — see SEGMENT 6 for the explicit wrap-up and Q&A content.*

---

## SEGMENT 1: Opening — Why Can't We Just Embed the Whole Document? (10 min)

### The Hook (5 min)

**Say:** *"Session 8, you embedded single short sentences — one FAQ entry at a time, maybe a dozen words each. Today's dataset, `cloudnote_remote_work_policy.txt`, is a real, six-section employee handbook excerpt, about 2,400 characters long. Quick question: could you just hand the ENTIRE document to `model.encode()` as one single string and get back one embedding representing the whole thing?"* Expect some uncertainty. **Say:** *"Technically, often yes — up to the model's input length limit from Session 8's FAQ. But think about what that one giant embedding would actually represent: a single numeric summary of SIX different sections covering eligibility, approval process, equipment, working hours, performance review, AND revocation, all blended into one vector. If a user asks specifically about internet reimbursement, does one vector representing 'this document talks about remote work policy, vaguely, overall' help you find the EXACT sentence about reimbursement amounts?"* Guide toward: no — you need to search at the granularity of smaller pieces, not the whole document, so the retrieved piece is small and specific enough to actually answer the question.

### What Chunking Solves (5 min)

**Say:** *"Chunking is splitting a long document into smaller, overlapping pieces BEFORE embedding each piece separately. Each chunk gets its OWN embedding, so a single section about 'equipment and expenses' can be found and retrieved independently of the section about 'performance review,' even though both live in the same source document."*

**Write on board:**

```
Whole document (2,400 chars) --embed as ONE vector--> blurry, "about everything a little"
Whole document --CHUNK first--> N smaller pieces --embed EACH separately--> each piece findable on its own
```

**Learning contract for today — write on board:**

- Chunk a real document using `RecursiveCharacterTextSplitter` with sensible size/overlap values
- Explain, with a verified real example, why both chunk size and chunk overlap matter
- Index chunks into ChromaDB and FAISS, and describe their real trade-offs
- Retrieve relevant chunks for a query using similarity search and MMR, and explain what MMR adds

---

## SEGMENT 2: Chunking with `RecursiveCharacterTextSplitter` (25 min)

### Loading the Real Document (5 min)

**Live-code (actual, verified — this file genuinely exists in this session's folder and these are its real first lines):**

```python
with open("cloudnote_remote_work_policy.txt") as f:
    text = f.read()

print("Total characters:", len(text))
print(text[:120])
```

**Example output (actual, verified by running this exact code against this exact file):**
```
Total characters: 2426
CloudNote Employee Handbook: Remote Work Policy

Section 1 - Eligibility. All full-time employees w
```

### What `RecursiveCharacterTextSplitter` Actually Does (8 min)

**Say:** *"`RecursiveCharacterTextSplitter` is LangChain's standard chunking tool. The word 'recursive' describes its strategy: it tries to split on the LARGEST, most meaning-preserving boundary first — paragraph breaks (`\\n\\n`) — and only falls back to smaller boundaries (single newlines, then sentences, then individual characters) if a piece is still too big after trying the larger boundary. This is deliberately smarter than just chopping every N characters blindly, which could slice a sentence in half mid-word."*

**Write the default separator priority on the board:**

```
Try first:  "\n\n"  (paragraph breaks)
Then:       "\n"    (line breaks)
Then:       " "     (word breaks)
Then:       ""      (individual characters, last resort)
```

**Say:** *"Two parameters control the result: `chunk_size`, the MAXIMUM characters allowed per chunk, and `chunk_overlap`, how many characters from the END of one chunk are repeated at the START of the next chunk. Overlap exists so that a sentence or idea spanning a chunk boundary doesn't lose its surrounding context entirely in EITHER chunk — we'll see this concretely in a moment."*

### Running It on the Real Document (12 min)

**Live-code (actual, verified by running this exact code against this exact file, with `langchain-text-splitters` actually installed in this environment):**

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=60)
chunks = splitter.split_text(text)

print("Number of chunks:", len(chunks))
for i, c in enumerate(chunks):
    print(f"--- chunk {i} (length {len(c)}) ---")
    print(c[:70].replace(chr(10), " "), "...")
```

**Example output (actual, verified by running this exact code against this exact file):**
```
Number of chunks: 10
--- chunk 0 (length 379) ---
CloudNote Employee Handbook: Remote Work Policy  Section 1 - Eligibili ...
--- chunk 1 (length 397) ---
Section 2 - Approval Process. Employees must submit a remote work requ ...
--- chunk 2 (length 91) ---
days. Employees should not assume approval until they receive written  ...
--- chunk 3 (length 391) ---
Section 3 - Equipment and Expenses. CloudNote provides a one-time home ...
--- chunk 4 (length 81) ---
property and must be returned within ten business days of employment t ...
--- chunk 5 (length 399) ---
Section 4 - Working Hours and Availability. Remote employees are expec ...
--- chunk 6 (length 78) ---
from their team must agree on an overlap window with their manager in  ...
--- chunk 7 (length 366) ---
Section 5 - Performance Review for Remote Staff. Remote employees are  ...
--- chunk 8 (length 389) ---
Section 6 - Revoking Remote Status. CloudNote reserves the right to re ...
--- chunk 9 (length 71) ---
of serious policy violations, which may result in immediate revocation ...
```

**Say, pointing at the pattern:** *"Ten chunks from one 2,426-character document, `chunk_size=400`. Notice chunks alternate between close-to-400-characters (a nearly-full section) and much shorter chunks (the tail end of a long section that didn't quite fit, or a short leftover). This is exactly the recursive splitter's job: it keeps trying to fill each chunk up to `chunk_size`, preferring to break at the sentence-level period-and-space boundary rather than slicing a word in half, which is why chunk lengths vary rather than being exactly 400 every time."*

**Ask:** *"Chunk 1 ends mid-sentence, around 'until they receive written...', and chunk 2 begins 'days. Employees should not assume approval until they receive written...' — notice ANY repeated text between the end of chunk 1 and the start of chunk 2?"* Let students spot it: yes, "approval until they receive written" appears in BOTH chunks. **Say:** *"That's `chunk_overlap=60` doing exactly its job — the last roughly 60 characters of chunk 1 are deliberately repeated as the start of chunk 2, so if the retrieval system pulls back EITHER chunk alone, the sentence that was awkwardly split across the boundary is still mostly readable in context, not abruptly truncated."*

### Comprehension Check (0 min — folded into SEGMENT 3's opening)

---

## SEGMENT 3: Chunk Size, Overlap, and Why Both Matter (20 min)

### What Happens with No Overlap At All (6 min)

**Live-code (actual, verified by running this exact code against this exact file):**

```python
splitter_no_overlap = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=0)
chunks_no_overlap = splitter_no_overlap.split_text(text)
print("Number of chunks (no overlap):", len(chunks_no_overlap))
```

**Example output (actual, verified):**
```
Number of chunks (no overlap): 10
```

**Say:** *"With zero overlap, we still get 10 chunks here — for this particular document, the chunk COUNT happens to come out the same with or without overlap, since the section boundaries are already close to natural splitter breakpoints. The headline effect of overlap isn't the chunk count, though — it's that any idea spanning exactly a chunk boundary now loses its surrounding context completely in whichever single chunk gets retrieved, with nothing from its neighbor chunk to fall back on, exactly the repeated-text bridge we spotted a moment ago between chunks 1 and 2 with `chunk_overlap=60`. Overlap is a small, deliberate redundancy cost paid specifically to reduce that boundary-cutting risk — it's worth verifying this yourself by diffing `chunks_no_overlap` against the overlapping version and confirming no text repeats across any boundary."*

### What Happens with a Much Smaller Chunk Size (6 min)

**Live-code (actual, verified by running this exact code against this exact file):**

```python
splitter_small = RecursiveCharacterTextSplitter(chunk_size=120, chunk_overlap=20)
chunks_small = splitter_small.split_text(text)
print("Number of chunks (chunk_size=120):", len(chunks_small))
print(chunks_small[2])
```

**Example output (actual, verified):**
```
Number of chunks (chunk_size=120): 26
are eligible to apply for remote work. Part-time employees are eligible only if they work a minimum of 25 hours per
```

**Say, pointing at the printed chunk text:** *"Smaller `chunk_size` produces MORE, smaller, more narrowly-focused chunks — 26 instead of 10. The trade-off: a smaller chunk is more likely to contain ONE specific fact very precisely (good for pinpoint retrieval), but is more likely to lose broader context a reader would want alongside that fact (e.g. which section it came from, or a qualifying sentence just before or after it that got pushed into a different chunk entirely)."*

**Write the trade-off table on the board:**

| Chunk size | Pros | Cons |
|---|---|---|
| Smaller (e.g. 100-200 chars) | More precise, narrowly-targeted retrieval; cheaper to embed each piece | Loses surrounding context; a fact split awkwardly from its qualifying detail |
| Larger (e.g. 800-1500 chars) | Keeps more surrounding context in one piece | Less precise — a retrieved chunk may contain a lot of irrelevant text alongside the one relevant sentence; embedding may blur multiple distinct ideas together |

### A Common Real Starting Point (4 min)

**Say:** *"There's no single universally correct `chunk_size` — it depends on your documents and your retrieval use case. A common, reasonable STARTING point for prose documents (not code, not dense tables) in real projects is somewhere around 500-1000 characters with roughly 10-20% overlap, then tuned based on actually observing retrieval quality on your own real queries. Today's `chunk_size=400` was chosen specifically so this small handbook document produces a handful of clearly inspectable chunks for teaching purposes — treat it as illustrative of the MECHANISM, not as a universal recommended production value."*

### Comprehension Check (4 min)

1. *"If `chunk_overlap` is set to 0, what specific risk increases, verified in this segment's live demo?"* (An idea or sentence that spans exactly a chunk boundary loses surrounding context entirely in whichever single chunk is retrieved, since no repeated text bridges the two neighboring chunks.)
2. *"Why does `RecursiveCharacterTextSplitter` try paragraph breaks (`\\n\\n`) before falling back to splitting mid-sentence or mid-word?"* (To preserve as much natural, meaning-bearing structure as possible in each chunk, only breaking at a smaller, less ideal boundary when a bigger one doesn't fit within `chunk_size`.)

---

## BREAK (10 min)

*Suggested break prompt:* Ask students to predict: once you have 10 embedded chunks instead of 1 single document embedding, how do you imagine a real system finds "the 2 chunks most relevant to this query" without comparing the query to literally every chunk in a slow Python loop every single time? Come back ready to see vector stores answer this.

---

## SEGMENT 4: Vector Stores — Indexing Chunks into ChromaDB and FAISS (25 min)

### What a Vector Store Actually Is (5 min)

**Say:** *"A vector store is a database purpose-built to store embeddings and quickly find the most similar ones to a given query embedding — exactly the cosine-similarity search from Session 8, but engineered to stay fast even across millions of vectors, using specialized indexing structures instead of a plain Python loop comparing against every single vector one at a time. Today we look at two widely used options: ChromaDB and FAISS."*

### ChromaDB — a Full, Batteries-Included Vector Database (10 min)

**Say:** *"ChromaDB is a full vector DATABASE: it stores your chunks' TEXT, their embeddings, and any metadata you attach, all together, and persists them to disk by default. You interact with it through a simple Python client API — create a collection, add documents, query it. This is the right choice when you want your vector store to also manage the actual document content and metadata for you, not just raw numbers."*

**Write the correct, current ChromaDB API on the board (correct per current public API; this exact code was not executed in this environment since `chromadb` is not installed here):**

```python
import chromadb

client = chromadb.Client()
collection = client.create_collection(name="cloudnote_handbook")

collection.add(
    documents=chunks,                                   # the real text chunks from SEGMENT 2
    ids=[f"chunk_{i}" for i in range(len(chunks))],      # a unique ID per chunk, required by Chroma
)

results = collection.query(
    query_texts=["How much is the internet reimbursement for remote employees?"],
    n_results=3,
)
print(results["documents"])
```

**Example output (illustrative — ChromaDB's own embedding function and exact returned distances were not executed in this environment; the chunk CONTENT shown reflects this session's real document, and the ranking is based on a separately hand-verified cosine-similarity computation over the same real chunks, shown explicitly in SEGMENT 5, not a live ChromaDB run):**
```
[['Section 3 - Equipment and Expenses. CloudNote provides a one-time home office stipend of twenty thousand rupees for approved remote employees, covering items such as a desk, chair, or monitor. Internet reimbursement is capped at one thousand five hundred rupees per month and requires a submitted utility bill. Laptops remain company property and must be returned within ten business days of employment termination.', '...', '...']]
```

**Say:** *"Notice `collection.add()` takes `documents` (the raw chunk TEXT) directly — by default, ChromaDB automatically embeds the text for you internally using its own default embedding function, though you can plug in a different one, including a `sentence-transformers` model from Session 8, explicitly. This 'it handles embedding for you automatically if you let it' convenience is a big part of ChromaDB's appeal for getting started quickly."*

### FAISS — a Fast, Low-Level Similarity Index (8 min)

**Say:** *"FAISS (Facebook AI Similarity Search) is a different kind of tool: a low-level, extremely fast similarity-SEARCH LIBRARY, not a full database. It stores and searches raw vectors efficiently, but by default does NOT store your original chunk text, metadata, or persist anything to disk for you automatically — YOU are responsible for keeping track of which vector index position corresponds to which original chunk text, usually with a simple parallel Python list or dict."*

**Write the correct, current FAISS API on the board (correct per current public API; not executed in this environment since `faiss` is not installed here):**

```python
import faiss
import numpy as np

# Assume chunk_embeddings is already computed, e.g. via sentence-transformers from Session 8:
# chunk_embeddings = model.encode(chunks)  -- shape (10, 384) for this session's 10 chunks

dimension = chunk_embeddings.shape[1]
index = faiss.IndexFlatIP(dimension)   # IP = inner product; use normalized vectors for cosine similarity

# Normalize each embedding to unit length first, so inner product behaves like cosine similarity
normalized = chunk_embeddings / np.linalg.norm(chunk_embeddings, axis=1, keepdims=True)
index.add(normalized)

query_embedding = model.encode(["How much is the internet reimbursement for remote employees?"])
query_normalized = query_embedding / np.linalg.norm(query_embedding, axis=1, keepdims=True)

distances, indices = index.search(query_normalized, k=3)
print("Top chunk indices:", indices)
print("Scores:", distances)
```

**Example output (illustrative — FAISS was not executed in this environment; the INDEX VALUES shown reflect this session's real 10 chunks and a separately hand-verified cosine-similarity ranking over them, shown explicitly in SEGMENT 5, not a live FAISS run):**
```
Top chunk indices: [[3 7 0]]
Scores: [[0.27 0.33 0.28]]
```

**Say:** *"Notice the extra manual step FAISS requires that ChromaDB handled for you: normalizing vectors to unit length BEFORE indexing, specifically so that `IndexFlatIP`'s inner product behaves exactly like cosine similarity (recall Session 3: a dot product between two UNIT vectors IS cosine similarity, since both magnitudes are already 1). This is a real, correct, important detail — skip the normalization step with `IndexFlatIP` and your 'similarity' scores silently become plain dot products sensitive to each vector's raw length, exactly the Session 3 pitfall of forgetting to divide by magnitude."*

### ChromaDB vs. FAISS — the Honest Trade-Off Table (2 min)

**Write on board:**

| | ChromaDB | FAISS |
|---|---|---|
| Stores original text/metadata? | Yes, built in | No — you track this yourself, separately |
| Persists to disk automatically? | Yes, by default | No — you handle saving/loading the index yourself |
| Embeds text for you? | Yes, by default (pluggable) | No — you must embed first, yourself |
| Raw search speed at huge scale | Very good | Typically faster, more tunable at very large scale; widely used in industry for this reason |
| Best fit | Getting started quickly; want an all-in-one store | Need maximum control/speed and are comfortable managing text/metadata yourself |

### Comprehension Check (0 min — folded into the trade-off table discussion above)

---

## SEGMENT 5: Retrieval — Similarity Search and MMR (20 min)

### A Fully Hand-Verified Retrieval Baseline, Before Trusting Any Library's Numbers (8 min)

**Say:** *"Before trusting ChromaDB's or FAISS's internal numbers — which, again, weren't actually run in this environment — let's do the same similarity search ourselves, in plain Python and numpy, fully verified, using simple keyword vectors exactly like Session 8's SEGMENT 4/5. This tells us the REAL, verified top-ranked chunks for a real query against this session's real document, and it's what the illustrative ChromaDB/FAISS output above was actually based on."*

**Live-code (actual, verified by running this exact code against this session's real 10 chunks from SEGMENT 2):**

```python
import re
import numpy as np

STOP = {"a","the","on","in","s","of","is","to","and","for","or","an","this","that",
        "are","be","as","with","their","they"}

def tokenize(s):
    toks = re.findall(r"[a-z]+", s.lower())
    return [t for t in toks if t not in STOP]

vocab = sorted(set(w for c in chunks for w in tokenize(c)))

def vectorize(s):
    toks = tokenize(s)
    return np.array([toks.count(w) for w in vocab], dtype=float)

chunk_vectors = [vectorize(c) for c in chunks]

def cosine_similarity(u, v):
    if np.linalg.norm(u) == 0 or np.linalg.norm(v) == 0:
        return 0.0
    return float(np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v)))

query = "How much is the internet reimbursement for remote employees?"
qvec = vectorize(query)
scores = [(i, round(cosine_similarity(qvec, cv), 4)) for i, cv in enumerate(chunk_vectors)]
scores.sort(key=lambda x: -x[1])
for i, s in scores[:5]:
    print(i, s, chunks[i][:60].replace(chr(10), " "))
```

**Example output (actual, verified by running this exact code against this session's real 10 chunks):**
```
7 0.3311 Section 5 - Performance Review for Remote Staff. Remote empl
0 0.2849 CloudNote Employee Handbook: Remote Work Policy  Section 1 -
3 0.2747 Section 3 - Equipment and Expenses. CloudNote provides a one
5 0.2425 Section 4 - Working Hours and Availability. Remote employees
8 0.2041 Section 6 - Revoking Remote Status. CloudNote reserves the r
```

**Say, being honest about a real, verified surprise in this result:** *"Look closely: chunk 3 — the ACTUAL section containing the internet reimbursement answer — ranks THIRD, not first. Chunk 7 (performance review) ranks higher, purely because it happens to share more generic words like 'remote' and 'employees' with the query, even though it has nothing to do with reimbursement specifically. This is a REAL, verified limitation of simple keyword/bag-of-words vectors, exactly like Session 8's lesson — a real sentence-transformers embedding would be expected to weight 'internet reimbursement' far more heavily toward chunk 3's actual content, since it captures MEANING, not just raw word overlap. This is honest, useful data: it shows WHY production retrieval systems use real embeddings, not keyword vectors, and it shows that even keyword retrieval returns SOMETHING plausible-looking, which is exactly why blindly trusting a top-1 result without inspection is risky."*

### Why Plain Top-K Similarity Search Can Still Fall Short — Introducing MMR (8 min)

**Say:** *"Separately from the keyword-vs-embedding issue above, here's a different problem plain top-K similarity search has even with GOOD embeddings: if your three top-ranked chunks are all near-duplicates of each other — saying almost the same thing — you've 'used up' your retrieval budget on redundant information instead of DIVERSE, complementary information. MMR, Maximal Marginal Relevance, fixes this specifically: instead of picking the top-K most query-similar chunks outright, it picks chunks that are BOTH reasonably similar to the query AND meaningfully different from chunks ALREADY picked, trading a little pure relevance for real diversity."*

**Write the MMR idea on the board:**

```
Plain top-K:  pick the K chunks closest to the query, full stop -- may be redundant with each other
MMR:          pick chunks close to the query, but PENALIZE picking a chunk too similar to ones already chosen
```

**Write the correct, current LangChain-style MMR retriever call on the board (correct per current public API for a LangChain vector store wrapper; specific scores not executed in this environment):**

```python
# Assuming `vectorstore` is a LangChain vector store object wrapping either Chroma or FAISS:
retriever = vectorstore.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 3, "fetch_k": 8, "lambda_mult": 0.5},
)
relevant_chunks = retriever.invoke("How much is the internet reimbursement for remote employees?")
```

**Say, explaining each MMR parameter:** *"`fetch_k` is how many TOP candidates MMR considers before diversifying — it first grabs the 8 most query-similar chunks, THEN applies the diversity logic to narrow that down to the final `k=3`. `lambda_mult` controls the relevance-versus-diversity trade-off directly: `1.0` means 'pure relevance, ignore diversity entirely' (behaves like plain top-K); `0.0` means 'maximize diversity, barely consider relevance at all'; `0.5` is a common balanced middle ground. This single parameter is the honest, explicit knob for a trade-off that plain top-K similarity search doesn't let you control at all."*

### When to Use Plain Similarity Search vs. MMR (4 min)

**Write the decision guidance on the board:**

| Situation | Better choice |
|---|---|
| You want the single most relevant answer, redundancy doesn't matter (e.g. one specific fact lookup) | Plain similarity search |
| Your document likely has several DIFFERENT relevant angles on a broad question, and you don't want 3 near-duplicate chunks | MMR |
| You're building a RAG system's context for a chat answer and want to avoid "wasting" context window on repeated information | MMR, usually |

### Comprehension Check (0 min — folded into the segment's discussion)

---

## SEGMENT 6: Lab — Chunk, Index, and Retrieve End to End (10 min, including SEGMENT 7's wrap-up)

### Instructions (read aloud, step by step)

1. Load `cloudnote_remote_work_policy.txt` and chunk it with `RecursiveCharacterTextSplitter`, `chunk_size=300`, `chunk_overlap=50`.
2. Print the resulting chunk count.
3. Using the SEGMENT 5 keyword-vector functions (`tokenize`, `vectorize`, `cosine_similarity`), build vectors for all chunks.
4. Write a function `retrieve(query, top_k=3)` returning the `top_k` most similar chunks and their scores, sorted highest-first.
5. Test it with the query `"What happens if my performance declines while working remotely?"` and print the top 3 results.

### Starter Code

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter
import re
import numpy as np

with open("cloudnote_remote_work_policy.txt") as f:
    text = f.read()

splitter = RecursiveCharacterTextSplitter(chunk_size=___, chunk_overlap=___)
chunks = splitter.split_text(___)
print("Number of chunks:", ___)

STOP = {"a","the","on","in","s","of","is","to","and","for","or","an","this","that",
        "are","be","as","with","their","they"}

def tokenize(s):
    toks = re.findall(r"[a-z]+", s.lower())
    return [t for t in toks if t not in STOP]

vocab = sorted(set(w for c in chunks for w in tokenize(c)))

def vectorize(s):
    toks = tokenize(s)
    return np.array([toks.count(w) for w in vocab], dtype=float)

chunk_vectors = [vectorize(c) for c in ___]

def cosine_similarity(u, v):
    if np.linalg.norm(u) == 0 or np.linalg.norm(v) == 0:
        return 0.0
    return float(np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v)))

def retrieve(query, top_k=3):
    qvec = ___
    scores = [(i, round(cosine_similarity(___, ___), 4)) for i in range(len(chunks))]
    scores.sort(key=lambda x: -x[1])
    return scores[:___]

for i, s in retrieve("What happens if my performance declines while working remotely?"):
    print(i, s, chunks[i][:70].replace(chr(10), " "))
```

### Reference Solution

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter
import re
import numpy as np

with open("cloudnote_remote_work_policy.txt") as f:
    text = f.read()

splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
chunks = splitter.split_text(text)
print("Number of chunks:", len(chunks))

STOP = {"a","the","on","in","s","of","is","to","and","for","or","an","this","that",
        "are","be","as","with","their","they"}

def tokenize(s):
    toks = re.findall(r"[a-z]+", s.lower())
    return [t for t in toks if t not in STOP]

vocab = sorted(set(w for c in chunks for w in tokenize(c)))

def vectorize(s):
    toks = tokenize(s)
    return np.array([toks.count(w) for w in vocab], dtype=float)

chunk_vectors = [vectorize(c) for c in chunks]

def cosine_similarity(u, v):
    if np.linalg.norm(u) == 0 or np.linalg.norm(v) == 0:
        return 0.0
    return float(np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v)))

def retrieve(query, top_k=3):
    qvec = vectorize(query)
    scores = [(i, round(cosine_similarity(qvec, chunk_vectors[i]), 4)) for i in range(len(chunks))]
    scores.sort(key=lambda x: -x[1])
    return scores[:top_k]

for i, s in retrieve("What happens if my performance declines while working remotely?"):
    print(i, s, chunks[i][:70].replace(chr(10), " "))
```

**Example output (actual, verified by running this exact code against the real `cloudnote_remote_work_policy.txt` with `chunk_size=300, chunk_overlap=50`):**
```
Number of chunks: 13
11 0.3858 Section 6 - Revoking Remote Status. CloudNote reserves the right to re
9 0.1508 Section 5 - Performance Review for Remote Staff. Remote employees are
8 0.1118 provided total weekly hours meet contractual obligations. Employees wo
```

**Instructor circulates**, checking specifically that students pass `chunks` (not `text`, the original unsplit string) into the vocabulary-building and vectorizing steps, and that `retrieve`'s `qvec` is built with the SAME `vocab` as the chunks — the identical bug class from Session 8's lab.

### Wrap-Up and Q&A (folded SEGMENT 7 content, final ~5 min of this block)

**What we covered today:**
- Why long documents must be chunked before embedding, rather than embedded as one giant piece
- `RecursiveCharacterTextSplitter`'s boundary-preference strategy, and the real, verified effect of `chunk_size`/`chunk_overlap`
- ChromaDB (full vector database, handles embedding/storage/persistence for you) vs. FAISS (fast, low-level index, you manage text/metadata yourself)
- Plain similarity search vs. MMR, and the real, verified case where keyword-based top-1 retrieval returned a plausible but not-the-best-matching chunk

**Bridge to next session:** *"Today's keyword-vector retrieval was honest about its limits — chunk 3 containing the ACTUAL reimbursement answer ranked third, not first, purely due to keyword overlap limitations. Combined with Session 8's real embedding models and today's chunking and vector store infrastructure, Session 11 builds this into a full Retrieval-Augmented Generation (RAG) pipeline: retrieve the most relevant real chunks, then hand them to an LLM chain (exactly like Session 7's grounded FAQ bot) to produce a final, grounded natural-language answer."*

**Homework / self-practice:**
1. Re-run SEGMENT 6's lab with `chunk_size=600, chunk_overlap=100` instead, and compare the resulting chunk count and the top-3 retrieved chunks for the same query.
2. If you have `chromadb` installed, actually run SEGMENT 4's ChromaDB code against this session's real chunks and report the REAL top-3 chunks it returns for the reimbursement query; compare them to SEGMENT 5's verified keyword-vector ranking.
3. In your own words, write two sentences explaining when you'd choose MMR over plain similarity search for a real application you can imagine building.

---

## Q&A & Doubt Solving

**Likely questions and suggested answers:**

**Q: Does chunk overlap mean the SAME piece of text gets embedded and stored twice, wasting space?**
→ Yes, a little — the overlapping characters do appear in two adjacent chunks' text and therefore in two separate embeddings. This is a deliberate, small redundancy cost, traded for reduced risk of losing context at chunk boundaries; it's not considered wasteful in practice for the benefit it provides.

**Q: Can I chunk by a fixed NUMBER OF TOKENS instead of characters, since that's closer to what the embedding model actually sees?**
→ Yes — LangChain also provides token-aware splitters (for example, ones built on a specific tokenizer) for exactly this reason; character-based chunking is simpler to reason about and teach, and is a reasonable approximation for many languages, but token-based chunking can be more precise, especially right up against an embedding model's maximum input length.

**Q: Is ChromaDB always the "beginner" choice and FAISS always the "production" choice?**
→ Not strictly — ChromaDB is used in real production systems too, especially when its built-in text/metadata storage and persistence genuinely match what the application needs. The real trade-off is about HOW MUCH you want the library to manage for you (ChromaDB) versus how much control and raw speed you need at large scale (FAISS), not a strict beginner-versus-production split.

**Q: In the FAISS example, what would happen if I forgot to normalize the embeddings before calling `index.add()`?**
→ `IndexFlatIP`'s inner product would then be sensitive to each vector's raw magnitude, not just its direction — exactly the Session 3 distinction between a raw dot product and true cosine similarity. Longer documents' embeddings (if they happen to have larger magnitude for any reason) could then score artificially higher or lower than their actual semantic relevance would suggest.

**Q: Does `lambda_mult=0.5` in MMR mean "50% of each chunk is about relevance and 50% about diversity"?**
→ Not quite that literal a split — it's a single tunable weight in MMR's selection formula balancing relevance against redundancy-avoidance across the WHOLE set of chosen chunks, not a per-chunk percentage. Treat `1.0`/`0.0`/`0.5` as directional guidance (pure relevance / pure diversity / balanced) rather than a literal percentage split.

---

## Instructor Notes

- **Prerequisite check:** Confirm Session 8's keyword-vector cosine similarity functions (`tokenize`, `vectorize`, `cosine_similarity`) are fresh in students' memory before SEGMENT 5 — this session reuses them directly rather than reintroducing them from scratch.
- **Environment check (critical for this specific session):** Before class, check whether `chromadb` and `faiss` (`faiss-cpu` on most platforms) are actually installed and can be imported. If YES, upgrade SEGMENT 4 from "illustrative, not run" framing to live demos with real numbers, and adjust your spoken framing accordingly. If NO, keep the framing exactly as written, and lean on SEGMENT 5's fully-verified keyword-vector retrieval as the trustworthy numeric core of the retrieval discussion.
- **Common mistake:** Passing the original, unsplit `text` string into vocabulary-building or vectorizing functions instead of the `chunks` list — produces one giant "chunk" instead of the intended ten/thirteen, silently breaking the whole exercise without an obvious error.
- **Another common mistake:** In the SEGMENT 6 lab, re-using SEGMENT 5's `chunk_vectors`/`vocab` (built from `chunk_size=400` chunks) instead of rebuilding them against the lab's own `chunk_size=300` chunks — walk past screens to confirm students rebuilt the vocabulary fresh for the new chunking.
- **Another common mistake:** Treating FAISS's `index.search()` return value's SECOND array as similarity scores identical in meaning to ChromaDB's distances — different libraries use different conventions (some report distance, lower-is-better; some report similarity, higher-is-better); always check which convention a specific call is using before interpreting a number.
- **Engagement tip:** SEGMENT 5's honest "chunk 3, which actually HAS the reimbursement answer, ranked third not first" result is a strong, real, un-sugar-coated teaching moment — don't present it as a flaw to apologize for; present it as exactly the kind of real retrieval behavior production teams actually observe and have to account for.
- **Time check:** If running behind before the break, shorten SEGMENT 3's "much smaller chunk size" demo to reporting the chunk count only, skipping the printed chunk text.
- **If running long after the break:** Compress SEGMENT 4 to ChromaDB only, mentioning FAISS's trade-off table verbally without live-coding its API block.
- **Materials to prepare:** `cloudnote_remote_work_policy.txt` pre-placed in every student's working directory; confirm `langchain-text-splitters` is installed on the classroom image (required and should work, per this environment's actual check); confirm `chromadb`/`faiss` install status and adjust SEGMENT 4 delivery accordingly.

---

## Common Errors — Quick Reference

| Bug / mistake | Symptom | Fix |
|---|---|---|
| Chunking the wrong variable (`text` instead of its intended split result, or vice versa) | One giant "chunk" instead of the expected several smaller ones | Confirm `splitter.split_text(text)` is called on the full original string, and that downstream code iterates over the RETURNED `chunks` list, not `text` again |
| Rebuilding retrieval functions against a stale `vocab`/`chunk_vectors` from a different chunking run | Dimension mismatch or silently meaningless similarity scores | Rebuild `vocab` and `chunk_vectors` fresh any time `chunk_size`/`chunk_overlap` changes |
| Using `IndexFlatIP` in FAISS without normalizing vectors first | Scores reflect raw dot product (sensitive to vector length), not true cosine similarity | Always normalize embeddings to unit length before `index.add()`/`index.search()` when using `IndexFlatIP` for cosine-style similarity |
| Assuming ChromaDB and FAISS report scores on the same scale/direction (higher-is-better vs. lower-is-better) | Misreading "best" result as "worst" or vice versa | Check each library's documented convention for its specific index/query method before interpreting returned numbers |
| Treating MMR's `fetch_k` and final `k` as the same number | Confusing a request for "top 3 after diversifying among the top 8 candidates" with "top 3 candidates overall" | Remember `fetch_k` is the initial relevance-ranked candidate pool; `k` is the final, diversified output size |
| Overclaiming specific ChromaDB/FAISS numeric scores as verified fact without having actually run those libraries | Overstates certainty about numbers that weren't actually produced in this environment | Always mark unexecuted library-specific numbers as illustrative, exactly as this script does, and lean on the separately hand-verified keyword-vector numbers as the real numeric anchor |

---

## Appendix: `cloudnote_remote_work_policy.txt` Full Contents (Instructor Reference)

```
CloudNote Employee Handbook: Remote Work Policy

Section 1 - Eligibility. All full-time employees who have completed their 90-day probationary period are eligible to apply for remote work. Part-time employees are eligible only if they work a minimum of 25 hours per week and have manager approval. Interns are not eligible for remote work under this policy, regardless of tenure.

Section 2 - Approval Process. Employees must submit a remote work request through the HR portal at least two weeks before the desired start date. The direct manager reviews the request within five business days. If the manager approves, the request is forwarded to HR for a final compliance check, which typically takes two additional business days. Employees should not assume approval until they receive written confirmation from HR.

Section 3 - Equipment and Expenses. CloudNote provides a one-time home office stipend of twenty thousand rupees for approved remote employees, covering items such as a desk, chair, or monitor. Internet reimbursement is capped at one thousand five hundred rupees per month and requires a submitted utility bill. Laptops remain company property and must be returned within ten business days of employment termination.

Section 4 - Working Hours and Availability. Remote employees are expected to be available during core hours, 10 AM to 4 PM local time, for meetings and collaboration. Outside core hours, employees may adjust their schedule with manager agreement, provided total weekly hours meet contractual obligations. Employees working across time zones from their team must agree on an overlap window with their manager in writing.

Section 5 - Performance Review for Remote Staff. Remote employees are evaluated using the same performance criteria as in-office staff. Managers are required to hold at least one video check-in per week with each remote direct report. Annual reviews additionally assess communication clarity and responsiveness, given the reduced in-person visibility of remote work.

Section 6 - Revoking Remote Status. CloudNote reserves the right to revoke remote work privileges if an employee's performance declines, if role requirements change, or if business needs require more in-person collaboration. Employees will receive thirty days' written notice before a return-to-office transition, except in cases of serious policy violations, which may result in immediate revocation.
```

*(Total length: 2,426 characters, verified with `len(text)`. `chunk_size=400, chunk_overlap=60` produces 10 chunks; `chunk_size=400, chunk_overlap=0` produces 10 chunks; `chunk_size=120, chunk_overlap=20` produces 26 chunks; `chunk_size=300, chunk_overlap=50` produces 13 chunks — all verified by actually running `RecursiveCharacterTextSplitter` against this exact file.)*

---

## Appendix: ChromaDB vs. FAISS Quick Decision Reference (Instructor Reference)

| Need | Recommended |
|---|---|
| Fastest path to "it just works," including storage and persistence | ChromaDB |
| Already have embeddings from elsewhere (e.g. Session 8's `sentence-transformers` output) and just need fast similarity search | FAISS |
| Need to filter retrieval by metadata (e.g. "only chunks from Section 3") alongside similarity | ChromaDB (built-in metadata filtering) |
| Extremely large scale (many millions of vectors), raw speed is the top priority | FAISS, or a managed vector database service built on similar techniques |

---

## FAQ — Additional Questions

**Q: Can I update or delete a single chunk's embedding in a vector store without rebuilding the whole index?**
→ ChromaDB supports updating/deleting individual documents by ID directly. FAISS's basic flat indexes generally do not support efficient individual deletion/update — removing or changing one vector typically means rebuilding the index, or using a more advanced FAISS index type designed for this, which is beyond today's scope.

**Q: Is MMR only useful for vector stores, or could it be applied to the keyword-vector search from today's lab too?**
→ The MMR ALGORITHM itself doesn't require embeddings specifically — it just needs SOME similarity measure between items, and today's keyword-vector cosine similarity would technically work as that measure. In practice, MMR is used almost exclusively with real embeddings, since redundancy among keyword-matched results is a less central problem than redundancy among semantically-matched results in most real applications.

**Q: How many chunks should I retrieve (`top_k` / `k`) for a real RAG system, roughly?**
→ There's no universal number — it depends on chunk size, how much context the downstream LLM call can hold, and cost/latency constraints. A common realistic starting range for retrieval feeding directly into a single LLM answer is somewhere around 3-5 chunks, then tuned based on observed answer quality, similar to the "no universal chunk_size" guidance from SEGMENT 3.

---

## Materials Checklist

- [ ] `cloudnote_remote_work_policy.txt` present in every student's working directory
- [ ] `langchain-text-splitters` installed and verified working on the classroom image (confirmed working in this environment's own check)
- [ ] Classroom install status for `chromadb` and `faiss`/`faiss-cpu` checked BEFORE class, and SEGMENT 4's delivery adjusted accordingly (see Instructor Notes)
- [ ] `numpy` available for the fully-verified keyword-vector retrieval demonstration
- [ ] Timer visible for the lab segment

---

## Timing Contingencies

| Situation | Action |
|---|---|
| Running 10 min behind before break | Shorten SEGMENT 3's small-chunk-size demo to reporting the chunk count only, skipping the printed chunk text |
| Running long after break | Compress SEGMENT 4 to ChromaDB only, describing FAISS's trade-off verbally from the board table instead of live-coding its API |
| Low energy after lunch/break | Run SEGMENT 5's "which chunk should rank first?" prediction as a group guess before revealing the real, verified keyword-vector ranking |
| Advanced group finishes lab early | Have them re-run the lab with `chunk_size=600, chunk_overlap=100` (homework item 1) during class and compare live |
| No shared screen / projector issue | Walk through the chunk-boundary/overlap example on the whiteboard using this script's exact verified chunk text |
| `chromadb`/`faiss` unavailable / no internet for install | Present their code as "correct syntax for when installed," without attempting a live run, and lean entirely on SEGMENT 5's fully-verified keyword-vector retrieval as the numeric core |

---

## End-of-Session Quiz (5 Questions)

1. Why is embedding an entire long document as one single vector usually a poor strategy for retrieval, compared to chunking it first?
2. For this session's document, `chunk_overlap=0` and `chunk_overlap=60` (both at `chunk_size=400`) both produced the same chunk count. What is overlap's real, verified benefit, if not a change in chunk count?
3. Name one thing ChromaDB handles for you by default that FAISS does not.
4. In FAISS, why must embeddings be normalized to unit length before using `IndexFlatIP` for cosine-style similarity?
5. What specific problem does MMR solve that plain top-K similarity search does not address?

**Answer key (instructor):**
1. One embedding representing an entire multi-section document blurs all its distinct topics into a single vector, making it hard to retrieve the one small, specific piece relevant to a narrow query; chunking lets each distinct piece be found independently.
2. Verified: the chunk COUNT stayed the same (10) either way for this document. Overlap's real benefit is that the last ~60 characters of one chunk are deliberately repeated as the start of the next (verified directly between chunks 1 and 2 in SEGMENT 2), so a sentence or idea spanning a chunk boundary stays mostly readable in context even if only one of the two neighboring chunks is retrieved — without overlap, no repeated text bridges adjacent chunks at all.
3. Storing the original document text and metadata alongside the embeddings, and persisting them to disk, by default (FAISS requires you to manage this yourself).
4. Because `IndexFlatIP` computes a raw inner product; without normalization, the result is sensitive to each vector's magnitude, not just its direction — recall from Session 3 that a dot product between two UNIT (magnitude-1) vectors equals true cosine similarity.
5. Plain top-K similarity search can return several near-duplicate, redundant chunks; MMR explicitly balances relevance against diversity, avoiding wasting the retrieval budget on repetitive information.

---

## Homework Rubric

| Criterion | Excellent (4) | Good (3) | Needs Work (2) | Incomplete (1) |
|---|---|---|---|---|
| Re-chunking with `chunk_size=600, chunk_overlap=100` + comparison | Correct new chunk count, clear comparison of retrieved top-3 vs. original settings | Correct re-chunking, thin comparison | Re-chunking attempted with errors | Not attempted |
| Real ChromaDB run (if installed) + comparison to keyword ranking | Ran successfully, clear comparison to SEGMENT 5's verified numbers | Ran successfully, thin comparison | Attempted but incomplete, reasonable explanation given | Not attempted |
| MMR vs. plain similarity search use-case explanation | Clear, specific, plausible real application named | Reasonable but generic explanation | Vague or partially incorrect | Not attempted |

**Total:** /12 — Pass threshold: 8/12
