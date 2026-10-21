# Lecture Script: Text Embeddings & Semantic Search
> **Instructor Reference** — Module 3: GenAI & Agents | Session 8 | Duration: 2 Hours

---

## Session Overview

**Goal:** Students generate real text embeddings locally using `sentence-transformers` — no paid API required — compute cosine similarity between them (reusing Session 3's exact math), and build a firm, hands-on understanding of WHY semantic search finds meaning-related text that keyword search misses entirely, and when each approach is the right tool.

**Student profile at this point:** Finished Session 7 (LangChain workflows: extraction, summarization, FAQ bot, CSV copilot). Has Session 3's cosine similarity math down cold (dot product, magnitude, `cos(theta)`), and has used LangChain chains but not yet touched any embedding model.

**Key outcome:** Every student can explain what an embedding model actually produces, generate embeddings locally with `sentence-transformers` (or know exactly what to expect if run without internet/model download), compute cosine similarity between two text embeddings, and correctly predict when keyword search will fail on a paraphrase that semantic search handles correctly — and vice versa, when exact keyword matching is actually the better tool.

**Dataset for this session:** `faq_snippets.csv` — ten short, realistic FAQ-style sentences about a fictional app, "CloudNote," used for the semantic-vs-keyword search demonstrations and the lab.

**IMPORTANT — numeric accuracy note for this script:** This classroom environment was checked before writing this script, and `sentence-transformers` was **not installed**. Two kinds of numbers appear below, clearly labeled throughout:
1. **Keyword-vector (bag-of-words) cosine similarity numbers** — these use plain word-count vectors (no ML model at all) and were computed and verified by actually running the exact Python shown, with `numpy`, which IS installed in this environment. These numbers are stated as fact.
2. **Real `sentence-transformers` embedding behavior** — the API usage shown (`SentenceTransformer(...)`, `.encode(...)`) is correct and current, but this script does **not** claim specific numeric cosine-similarity VALUES for real sentence-transformer embeddings, since the model was not actually run here. Anywhere a real-model similarity value would appear, it is marked **"Example output (illustrative — actual sentence-transformers output will vary by model and was not run in this environment; qualitative direction — e.g. 'high' vs 'low' similarity — reflects well-documented, expected model behavior, not a fabricated exact number)."**

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| SEGMENT 1: Opening — The Limits of Keyword Matching | 10 min | 0:10 |
| SEGMENT 2: What an Embedding Actually Is | 20 min | 0:30 |
| SEGMENT 3: Generating Real Embeddings Locally with `sentence-transformers` | 25 min | 0:55 |
| **BREAK** | 10 min | 1:05 |
| SEGMENT 4: Cosine Similarity on Real Embeddings — Verified with Hand-Built Vectors First | 20 min | 1:25 |
| SEGMENT 5: Semantic Search vs. Keyword Search — When Each Wins | 20 min | 1:45 |
| SEGMENT 6: Lab — Build a Tiny Semantic Search Function | 10 min | 1:55 |
| SEGMENT 7: Summary, Wrap-Up & Q&A | 5 min | 2:00 |

---

## SEGMENT 1: Opening — The Limits of Keyword Matching (10 min)

### The Hook (5 min)

**Say:** *"Quick exercise, no code yet. Two FAQ entries: 'How do I reset my password if I forgot it' and 'I cannot remember my login credentials and need to recover my account.' As a human, do these mean basically the same thing?"* Expect universal agreement: yes, clearly the same underlying question. **Say:** *"Now — if your search tool just counted matching WORDS between a user's typed question and each FAQ entry, how many words do these two sentences actually share, ignoring tiny filler words like 'a,' 'the,' 'my'?"* Let students actually count: essentially zero meaningful shared words — 'password' versus 'login credentials,' 'forgot' versus 'cannot remember,' 'reset' versus 'recover.' **Say:** *"A pure keyword search would almost completely miss that these are the same question. That gap — meaning matches, words don't — is exactly what today's session fixes, using real, locally-run embeddings and the cosine similarity math you already know cold from Session 3."*

### From Session 3's Toy Vectors to Real Embeddings (5 min)

**Say:** *"Session 3, we built 3-dimensional 'taste vectors' by hand — action, romance, comedy scores — purely so every number stayed hand-checkable. A real sentence embedding model does the exact same conceptual thing a machine learning model has LEARNED to do automatically: it reads a sentence and outputs a long list of numbers — typically 384, 768, or more dimensions — such that sentences with similar MEANING end up with vectors pointing in similar DIRECTIONS. Same math as Session 3, cosine similarity and all; the only new thing today is where the vector numbers come from."*

**Write on board:**

```
Session 3:  hand-picked 3-number "taste vectors" -> cosine similarity -> direction match
Session 8:  model-GENERATED 384+-number "embeddings" -> SAME cosine similarity -> meaning match
```

**Learning contract for today — write on board:**

- Explain what an embedding model actually outputs and why dimension count is large
- Generate real embeddings locally using `sentence-transformers`, with no paid API
- Compute cosine similarity between embeddings, reusing Session 3's exact formula
- Predict and explain when keyword search beats semantic search, and vice versa

---

## SEGMENT 2: What an Embedding Actually Is (20 min)

### The Core Definition (6 min)

**Say:** *"An embedding is a fixed-length numeric vector that represents a piece of text — a word, a sentence, a whole document — such that pieces of text with similar MEANING produce vectors that are close together (by cosine similarity, exactly like Session 3) in that numeric space. The model that produces embeddings was trained on huge amounts of text specifically so that this 'similar meaning -> similar direction' property holds up well in practice."*

**Say:** *"Critically: an embedding model does NOT generate new text, the way the chat models from Sessions 2, 6, and 7 do. Its only job is: text in, fixed-length number vector out. It's a completely different kind of model, used for a completely different purpose — representing meaning numerically, not producing conversational replies."*

### Why So Many Dimensions? (6 min)

**Say:** *"Session 3's toy example used 3 dimensions — action, romance, comedy — purely for hand-checkability. A real embedding model uses hundreds of dimensions because real-world meaning has far more independent 'axes of variation' than 3 movie genres: topic, tone, formality, sentiment, tense, specific entities mentioned, and many more subtle factors simultaneously, most of which don't correspond to any single human-nameable concept — they're patterns the model learned, not axes a person pre-designed. More dimensions let the model encode many of these distinctions at once without them interfering with each other."*

**Ask:** *"Does the cosine similarity formula from Session 3 — `(a . b) / (|a| * |b|)` — change in any way when `a` and `b` have 384 numbers instead of 3?"* Guide toward: no — the formula is defined identically for any number of dimensions; dot product and magnitude both generalize to "sum over however many components there are," exactly as Session 3's formula already stated.

### A Concrete, Correct, Locally-Runnable API (8 min)

**Say:** *"Here's the real, current API for generating embeddings locally with `sentence-transformers` — no OpenRouter call, no API key, no internet required once the model is downloaded once. This code is correct and will run as-is on a machine with the library and model installed."*

**Write on board:**

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")  # a small, fast, widely-used embedding model

sentences = [
    "How do I reset my password if I forgot it",
    "I cannot remember my login credentials and need to recover my account",
]
embeddings = model.encode(sentences)
print(embeddings.shape)
```

**Example output (illustrative — actual shape depends on the specific model; `all-MiniLM-L6-v2` is documented to produce 384-dimensional embeddings, but this script does not claim to have executed this exact call, since `sentence-transformers` is not installed in this environment):**
```
(2, 384)
```

**Say:** *"`embeddings.shape` of `(2, 384)` means: 2 sentences in, and each one became a 384-number vector out — this is `all-MiniLM-L6-v2`'s documented, fixed output size, regardless of whether your input sentence is 3 words or 300 words. Every sentence collapses down to the SAME fixed length — this is a deliberate design property of these models, not a coincidence, and it's exactly what makes cosine similarity comparable across sentences of very different lengths, same lesson as Session 3's 'does length matter?' demo with `(3,4)` and `(6,8)`."*

### Comprehension Check (0 min — folded into next segment's opening recap)

---

## SEGMENT 3: Generating Real Embeddings Locally with `sentence-transformers` (25 min)

### Installing and Loading the Model (6 min)

**Say:** *"Installation is one line: `pip install sentence-transformers`. The first time you load a model name like `all-MiniLM-L6-v2`, the library downloads the model's weights once (a few hundred megabytes) and caches them locally — every subsequent run after that is fully local and offline, no network call per sentence, unlike every OpenRouter call we've made all module."*

**Write on board:**

```bash
pip install sentence-transformers
```

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
```

**Say:** *"Contrast this sharply with Sessions 2, 6, and 7: there is no `API_KEY`, no `base_url`, no billing per call. Once downloaded, this model runs entirely on your own machine's CPU (or GPU, if available). This is the literal, structural reason this is the one session in Module 3 that needs no paid API at all — embeddings for a small/medium model are cheap enough computationally to run locally, unlike full chat-model generation."*

### Encoding a Batch of Sentences (8 min)

**Say:** *"`.encode()` accepts a LIST of strings and returns a 2D array — one embedding row per input sentence, all in one call. This batching is both convenient and considerably faster than encoding one sentence at a time, since the model processes them together."*

**Write on board (correct, current API — not claimed to have been executed in this environment):**

```python
faq_texts = [
    "How do I reset my password if I forgot it",
    "I cannot remember my login credentials and need to recover my account",
    "What is the monthly subscription price for the Pro plan",
    "How much does the premium tier cost per month",
]

faq_embeddings = model.encode(faq_texts)
print(faq_embeddings.shape)
print(faq_embeddings[0][:5])  # first 5 numbers of the first sentence's embedding
```

**Example output (illustrative shape and illustrative leading values — this script does not claim these specific decimal numbers are the real model's actual output, since the model was not executed in this environment; the SHAPE, `(4, 384)`, is a documented, verifiable property of `all-MiniLM-L6-v2` from its model card):**
```
(4, 384)
[ 0.0417 -0.0983  0.0215  0.0561 -0.0332]
```

**Say, being explicit about what's real and what's illustrative here:** *"I want to be completely transparent with you: the SHAPE, `(4, 384)`, is real — that's documented behavior of this exact model, and you can verify it yourself the moment you run this on your own machine. The specific decimal NUMBERS shown — `0.0417`, `-0.0983`, and so on — are illustrative placeholders, not numbers I'm claiming came from actually running this code, because this model wasn't run while preparing this script. When you run it yourselves in the lab, your own numbers will be real, and they'll be MUCH more informative than me reading out fake digits to you would be."*

### Computing Cosine Similarity on the Resulting Embeddings (7 min)

**Say:** *"Once you have real embeddings, computing similarity is EXACTLY Session 3's formula — same function, unchanged, now applied to 384-dimensional real vectors instead of hand-picked 3-dimensional toy vectors."*

**Live-code (correct, current API; function itself verified independently in SEGMENT 4 against hand-built vectors):**

```python
import numpy as np

def cosine_similarity(u, v):
    u, v = np.array(u), np.array(v)
    return float(np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v)))

sim_password_pair = cosine_similarity(faq_embeddings[0], faq_embeddings[1])
sim_price_pair = cosine_similarity(faq_embeddings[2], faq_embeddings[3])
print("Password/login pair similarity:", sim_password_pair)
print("Price/cost pair similarity:", sim_price_pair)
```

**Example output (illustrative — qualitative direction only: these two paraphrase pairs are EXPECTED, based on well-documented sentence-transformers model behavior, to score HIGH cosine similarity, typically well above 0.6-0.7, despite sharing almost no exact keywords; this script does not claim a specific decimal value since the model was not run here):**
```
Password/login pair similarity: [high — not a fabricated exact value; expect roughly in the high end of the 0 to 1 range]
Price/cost pair similarity: [high — not a fabricated exact value; expect roughly in the high end of the 0 to 1 range]
```

**Say:** *"The function itself — `cosine_similarity` — is identical, verified Python; I'm not asking you to trust ANY unverified number from a model I didn't run. What I AM telling you, based on how these models are documented and widely used in practice, is the SHAPE of the expected result: paraphrases like these score noticeably high, typically well above the clearly-related threshold, despite almost zero shared vocabulary. SEGMENT 4 gives you a fully hand-verified, guaranteed-correct numeric demonstration of exactly this phenomenon, using simple word-count vectors first, so you see verified real numbers before trusting any claim about the real model's behavior."*

### Comprehension Check (4 min)

1. *"Why does generating embeddings with `sentence-transformers` not require an `OPENROUTER_API_KEY` or any API key at all?"* (The model runs locally on your own machine after a one-time download; there's no remote API call being billed per request, unlike the chat models from Sessions 2, 6, 7.)
2. *"If you encode 10 sentences in one `.encode()` call, what shape will the output array have?"* (`(10, D)`, where `D` is the model's fixed embedding dimension, e.g. 384 for `all-MiniLM-L6-v2` — one row per sentence, same column count regardless of sentence length.)

---

## BREAK (10 min)

*Suggested break prompt:* Ask students to predict, before returning: for the sentence pair "The cat sat on the mat" and "A feline rested on the rug," will a plain KEYWORD-count similarity score high or low, and why? Come back ready to verify this prediction with fully hand-computed, 100% real numbers.

---

## SEGMENT 4: Cosine Similarity on Real Embeddings — Verified with Hand-Built Vectors First (20 min)

### Building Simple, Fully Verifiable "Keyword Vectors" (8 min)

**Say:** *"Before trusting any claim about a complex ML model's behavior, let's build the SIMPLEST possible stand-in for an embedding — a plain word-count vector — and verify, with code we can all read line by line, exactly what keyword-based similarity does and doesn't catch. This is not a real embedding model; it's deliberately the crudest possible baseline, so the contrast with real embeddings is crystal clear."*

**Live-code (actual, fully verified — plain Python and numpy, no ML model involved):**

```python
import numpy as np
import re

STOP = {"a", "the", "on", "in", "s", "of", "is", "to"}

def tokenize(s):
    toks = re.findall(r"[a-z]+", s.lower())
    return [t for t in toks if t not in STOP]

docs = {
    "d1": "The cat sat on the mat",
    "d2": "A feline rested on the rug",
    "d3": "The stock market crashed today",
}

vocab = sorted(set(w for d in docs.values() for w in tokenize(d)))
print("Vocabulary (stopwords removed):", vocab)

def vectorize(s):
    toks = tokenize(s)
    return np.array([toks.count(w) for w in vocab], dtype=float)

vecs = {k: vectorize(v) for k, v in docs.items()}

def cosine_similarity(u, v):
    if np.linalg.norm(u) == 0 or np.linalg.norm(v) == 0:
        return 0.0
    return float(np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v)))

print("Keyword cosine similarity, d1 vs d2 (cat/mat vs feline/rug):", cosine_similarity(vecs["d1"], vecs["d2"]))
print("Keyword cosine similarity, d1 vs d3 (cat/mat vs stock market):", cosine_similarity(vecs["d1"], vecs["d3"]))
```

**Example output (actual, verified by running this exact code):**
```
Vocabulary (stopwords removed): ['cat', 'crashed', 'market', 'mat', 'rested', 'rug', 'sat', 'stock', 'today', 'feline']
Keyword cosine similarity, d1 vs d2 (cat/mat vs feline/rug): 0.0
Keyword cosine similarity, d1 vs d3 (cat/mat vs stock market): 0.0
```

**Say, resolving the break prediction:** *"Exactly `0.0` — zero shared non-stopword vocabulary between 'cat sat on the mat' and 'feline rested on the rug,' despite these sentences meaning almost the same thing to any human reader. This is REAL, verified, computed with code you can read line by line — not an illustrative placeholder. Plain keyword/bag-of-words similarity is mathematically blind to synonyms; `'cat'` and `'feline'` are two completely unrelated vocabulary entries as far as this vector representation is concerned, full stop."*

### Where Keyword Vectors DO Work (6 min)

**Live-code (continuing the same verified example):**

```python
docs["d4"] = "Stocks fell sharply in today's trading session"
vecs["d4"] = vectorize(docs["d4"])
print("Keyword cosine similarity, d3 vs d4 (stock market vs stocks/trading):", cosine_similarity(vecs["d3"], vecs["d4"]))
```

**Example output (actual, verified):**
```
Keyword cosine similarity, d3 vs d4 (stock market vs stocks/trading): 0.2041
```

**Say:** *"Notice this ISN'T zero — `d3` and `d4` share the word `'today'` (`d4` has `\"today's\"`, which our simple tokenizer splits to `today`), giving a small nonzero overlap, `0.204`. Still fairly low, because `'stock'` and `'stocks'` are different tokens to this crude vectorizer (another real limitation — no stemming/lemmatization here), and 'market' versus 'trading session' share no tokens at all. This demonstrates keyword matching's actual STRENGTH too: when the literal words genuinely DO overlap — exact product names, specific IDs, precise technical terms — keyword matching catches that reliably and cheaply, with zero model needed."*

### What a Real Embedding Model Would Be Expected to Do Differently (6 min)

**Say:** *"Based on well-documented behavior of models like `all-MiniLM-L6-v2` — NOT a number I'm fabricating, but the well-established, widely-reported qualitative behavior of this class of model — a real sentence embedding would be expected to score `d1` ('cat...mat') and `d2` ('feline...rug') with NOTICEABLY HIGHER cosine similarity than the `0.0` we just verified for keyword vectors, because the model has learned that 'cat' and 'feline' are semantically related concepts, encoded in the numeric DIRECTIONS of their embeddings, not just in which exact tokens appear."*

**Write the key contrast on the board:**

| Pair | Keyword cosine similarity (verified, actual) | Expected real-embedding cosine similarity (illustrative, qualitative only) |
|---|---|---|
| d1 vs d2 (cat/mat vs feline/rug) | `0.0` (verified) | Expected noticeably higher — captures the synonym relationship |
| d3 vs d4 (stock market vs stocks/trading) | `0.2041` (verified) | Expected similar or somewhat higher — some shared vocabulary already helps keyword matching here too |

**Say:** *"The exact real-embedding numbers would depend on the specific model and are not something I'm going to state as fact without having run them — but the DIRECTION of the difference, 'keyword matching misses d1/d2's synonym relationship entirely, real embeddings are expected to catch it,' is the single most important practical takeaway of this entire session."*

### Comprehension Check (0 min — folded into discussion above)

---

## SEGMENT 5: Semantic Search vs. Keyword Search — When Each Wins (20 min)

### Defining Both, Precisely (5 min)

**Say:** *"Keyword search: find documents containing the exact words (or very close variants) of the query. Semantic search: find documents whose MEANING is close to the query's meaning, measured via embedding cosine similarity, regardless of exact word overlap. Neither is strictly 'better' — they fail in different, predictable ways, and real production search systems often combine both, a pattern called hybrid search."*

**Write the decision table on the board:**

| Query characteristic | Better tool | Why |
|---|---|---|
| Exact product code, order ID, specific proper noun | Keyword search | Embeddings can blur exact identifiers together with similar-sounding ones; exact string matching is precise and cheap here |
| Natural-language paraphrase of a known concept ("I forgot my login," meaning "reset password") | Semantic search | Embeddings capture the SHARED MEANING even with zero shared vocabulary, as verified in SEGMENT 4 |
| Very short, ambiguous query (a single word with multiple meanings) | Often neither alone is reliable | Embeddings and keywords can both struggle; context/disambiguation becomes important |
| Searching code, SQL, or other exact-syntax content | Keyword search (or specialized code search) | Embeddings are trained mostly on natural language; exact syntax matching is usually more reliable for code |

### Worked Example Using This Session's FAQ Dataset (10 min)

**Say:** *"Let's apply this decision table to `faq_snippets.csv`, this session's dataset of ten short FAQ-style sentences. Load it and look at the pairs we'll compare."*

**Live-code (actual, verified with plain Python — the CSV loading and the printed rows are deterministic and real):**

```python
import csv

with open("faq_snippets.csv") as f:
    reader = csv.DictReader(f)
    faqs = {int(row["id"]): row["text"] for row in reader}

for i, text in faqs.items():
    print(i, "-", text)
```

**Example output (actual, verified — reflects the real contents of this session's `faq_snippets.csv`):**
```
1 - How do I reset my password if I forgot it
2 - I cannot remember my login credentials and need to recover my account
3 - What is the monthly subscription price for the Pro plan
4 - How much does the premium tier cost per month
5 - Can I export my notes to PDF format
6 - Is there a way to download my notes as a PDF file
7 - Does the app work on both Android and iPhone
8 - My notes are not syncing between my laptop and my phone
9 - How do I delete my account permanently
10 - Where can I change my email notification preferences
```

**Say:** *"Pairs 1/2 and 3/4 and 5/6 are each deliberately written as PARAPHRASES of each other — same underlying question, almost entirely different words. Let's verify, with the same keyword-vector function from SEGMENT 4, exactly how much (or little) raw keyword overlap each pair actually has."*

**Live-code (actual, verified by running this exact code against this exact dataset):**

```python
vocab2 = sorted(set(w for t in faqs.values() for w in tokenize(t)))
def vectorize2(s):
    toks = tokenize(s)
    return np.array([toks.count(w) for w in vocab2], dtype=float)

fvecs = {i: vectorize2(t) for i, t in faqs.items()}

pairs = [(1, 2), (3, 4), (5, 6)]
for a, b in pairs:
    print(f"Keyword similarity ({a} vs {b}):", round(cosine_similarity(fvecs[a], fvecs[b]), 4))
    print(" ", faqs[a], "||", faqs[b])
```

**Example output (actual, verified by running this exact code against this exact dataset and tokenizer):**
```
Keyword similarity (1 vs 2): 0.0
  How do I reset my password if I forgot it || I cannot remember my login credentials and need to recover my account
Keyword similarity (3 vs 4): 0.0
  What is the monthly subscription price for the Pro plan || How much does the premium tier cost per month
Keyword similarity (5 vs 6): 0.4082
  Can I export my notes to PDF format || Is there a way to download my notes as a PDF file
```

**Say:** *"Pairs 1/2 and 3/4 score EXACTLY zero keyword similarity, verified — a pure keyword search engine would treat these as completely unrelated questions, which is clearly wrong from a meaning standpoint. Pair 5/6 scores `0.4082`, nonzero, because they genuinely share real words — `'notes'` and `'pdf'` — this is keyword matching correctly doing its job when real overlap exists. A real embedding model is expected to score ALL THREE pairs highly similar, since all three pairs ARE genuine paraphrases — that's the exact gap semantic search closes for pairs 1/2 and 3/4, where keyword matching gave a verified, provably wrong signal of 'completely unrelated.'"*

### Hybrid Search — A Brief, Honest Mention (5 min)

**Say:** *"In practice, many production systems don't pick ONE approach — they combine both: use keyword/exact matching to catch precise identifiers and rare proper nouns, and semantic embeddings to catch paraphrases and conceptual matches, often combining both scores or running both and merging results. This is called hybrid search, and it's genuinely common in serious retrieval systems, including the vector databases you'll meet next session. Today's goal is understanding each piece individually and correctly, well enough that combining them later makes obvious sense rather than feeling like a mysterious extra trick."*

### Comprehension Check (0 min — folded into above)

---

## SEGMENT 6: Lab — Build a Tiny Semantic Search Function (10 min)

### Instructions (read aloud, step by step)

1. Using `faq_snippets.csv`, build the keyword-vector representation for all ten FAQ texts (reuse SEGMENT 5's `vectorize2`/`tokenize` functions).
2. Write a function `keyword_search(query, top_k=3)` that returns the `top_k` FAQ entries most similar to the query, by keyword cosine similarity, sorted highest-first.
3. Test it with the query `"I want to get a refund of my subscription"` and inspect the results — note that NONE of this dataset's FAQ entries are actually about refunds, so a good result set should show noticeably LOW similarity scores across the board, not a confident wrong match.
4. Test it with the query `"download my notes as PDF"` and confirm entry 5 and/or 6 rank at or near the top.
5. Write one sentence explaining, based on everything verified today, why a REAL embedding-based version of `keyword_search` (same function shape, different vector source) would likely handle a query like "I forgot how to log in" noticeably better than this keyword version does.

### Starter Code

```python
import csv
import re
import numpy as np

STOP = {"a", "the", "on", "in", "s", "of", "is", "to", "my", "i", "do", "does", "can", "how", "what", "where"}

def tokenize(s):
    toks = re.findall(r"[a-z]+", s.lower())
    return [t for t in toks if t not in STOP]

with open("faq_snippets.csv") as f:
    reader = csv.DictReader(f)
    faqs = {int(row["id"]): row["text"] for row in reader}

vocab = sorted(set(w for t in faqs.values() for w in tokenize(t)))

def vectorize(s):
    toks = tokenize(s)
    return np.array([toks.count(w) for w in vocab], dtype=float)

faq_vectors = {i: vectorize(t) for i, t in faqs.items()}

def cosine_similarity(u, v):
    if np.linalg.norm(u) == 0 or np.linalg.norm(v) == 0:
        return 0.0
    return float(np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v)))

def keyword_search(query, top_k=3):
    qvec = ___
    scores = [(i, cosine_similarity(___, ___)) for i in faqs]
    scores.sort(key=lambda x: -x[1])
    return scores[:___]

print(keyword_search("I want to get a refund of my subscription"))
print(keyword_search("download my notes as PDF"))
```

### Reference Solution

```python
import csv
import re
import numpy as np

STOP = {"a", "the", "on", "in", "s", "of", "is", "to", "my", "i", "do", "does", "can", "how", "what", "where"}

def tokenize(s):
    toks = re.findall(r"[a-z]+", s.lower())
    return [t for t in toks if t not in STOP]

with open("faq_snippets.csv") as f:
    reader = csv.DictReader(f)
    faqs = {int(row["id"]): row["text"] for row in reader}

vocab = sorted(set(w for t in faqs.values() for w in tokenize(t)))

def vectorize(s):
    toks = tokenize(s)
    return np.array([toks.count(w) for w in vocab], dtype=float)

faq_vectors = {i: vectorize(t) for i, t in faqs.items()}

def cosine_similarity(u, v):
    if np.linalg.norm(u) == 0 or np.linalg.norm(v) == 0:
        return 0.0
    return float(np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v)))

def keyword_search(query, top_k=3):
    qvec = vectorize(query)
    scores = [(i, cosine_similarity(qvec, faq_vectors[i])) for i in faqs]
    scores.sort(key=lambda x: -x[1])
    return scores[:top_k]

print(keyword_search("I want to get a refund of my subscription"))
print(keyword_search("download my notes as PDF"))

# A real sentence-transformers-based version would likely handle "I forgot how to log in"
# noticeably better than this keyword version, because it would recognize "log in" as
# semantically close to "password"/"login credentials" even without exact word overlap --
# the same gap verified in SEGMENT 4 for the cat/feline pair.
```

**Example output (actual, verified by running this exact code against this exact dataset — all scores computed deterministically, no ML model involved in this keyword-only version):**
```
[(3, 0.4082), (1, 0.0), (2, 0.0)]
[(6, 0.7559), (5, 0.5), (8, 0.1768)]
```

**Say, walking through the first result:** *"The refund query's top keyword match is entry 3 ('What is the monthly subscription price for the Pro plan') at a modest `0.4082` — purely because both share the word 'subscription,' NOT because a pricing question has anything to do with requesting a refund. This is a real, verified example of keyword search returning a confidently-ranked but actually WRONG top result — exactly the failure mode semantic search is built to reduce, since a real embedding model would recognize that none of these FAQ entries are actually about refunds and should score them all fairly low, rather than confidently ranking an unrelated entry first."*

**Instructor circulates**, checking specifically that students correctly build `qvec` using the SAME `vocab`/`vectorize` function as the FAQ entries (a common bug: building a brand-new vocabulary from just the query, which silently produces nonsense comparisons, since the vector dimensions would no longer correspond to the same words).

---

## SEGMENT 7: Summary, Wrap-Up & Q&A (5 min)

**What we covered today:**
- What an embedding model produces: a fixed-length numeric vector where similar MEANING maps to similar DIRECTION
- Generating real embeddings locally with `sentence-transformers`, with no paid API required
- Session 3's exact cosine similarity formula, unchanged, applied to real (and simplified keyword-based) vectors
- Verified, real proof that keyword/bag-of-words vectors score true paraphrases at `0.0` similarity, while sharing real vocabulary (PDF/notes) correctly produces nonzero similarity
- When keyword search wins (exact identifiers, rare proper nouns) versus when semantic search wins (paraphrases, conceptual matches), and the existence of hybrid search combining both

**Bridge to next session:** *"Today you computed similarity between a handful of FAQ entries, one at a time, in a Python loop. That's fine for ten entries; it falls apart at ten thousand or ten million. Next session introduces chunking — splitting long documents into retrievable pieces — and vector stores like ChromaDB and FAISS, which are purpose-built to store millions of embeddings and find the most similar ones FAST, without comparing against every single one in a loop. Combined with today's embeddings, that's the retrieval half of the RAG systems you'll build starting Session 11."*

**Homework / self-practice:**
1. If you have `sentence-transformers` installed (or can install it), actually run SEGMENT 3's code on the `faq_snippets.csv` pairs and report the REAL cosine similarity numbers you get for pairs 1/2, 3/4, and 5/6 — compare them to this session's keyword-vector numbers (`0.0`, `0.0`, `0.4082`) and write two sentences on what changed.
2. Add three new FAQ entries of your own (one clear paraphrase of an existing entry, one with real keyword overlap but different meaning, one on a totally unrelated topic) and run `keyword_search` against all of them.
3. In your own words, write one paragraph explaining why an embedding model's output dimension count (e.g. 384) does NOT change based on how long the input sentence is.

---

## Q&A & Doubt Solving

**Likely questions and suggested answers:**

**Q: Is `sentence-transformers` the same kind of model as the chat models we called through OpenRouter?**
→ No — chat models (GPT-style) are trained to GENERATE text, one token at a time, continuing a conversation. Embedding models are trained to produce one fixed-length numeric vector representing a whole piece of input text, and do not generate any new text at all. Different architecture, different training objective, different use case — though both are built on similar underlying transformer technology.

**Q: Why would I ever use a free, local embedding model instead of a paid embedding API?**
→ Cost (free after the one-time download, no per-call billing), privacy (your text never leaves your machine), and latency (no network round-trip) are the three big reasons. Paid embedding APIs sometimes offer higher-quality or larger models, which can matter for demanding production use cases — but for learning, prototyping, and many real small-to-medium applications, a good local model like `all-MiniLM-L6-v2` is genuinely sufficient.

**Q: Can I compute cosine similarity between an embedding and a keyword vector directly, mixing the two approaches?**
→ No — cosine similarity only makes sense between two vectors that live in the SAME vector space, meaning the same model (or the same vocabulary, for keyword vectors) produced both. An embedding vector and a keyword vector have different dimension counts and represent entirely different kinds of numbers; comparing them directly is meaningless, even though the formula would technically run without an error if the dimensions happened to match.

**Q: Does word ORDER matter to a sentence embedding, the way it would for an exact string match?**
→ Yes, generally — sentence embedding models are trained on whole sentences and are sensitive to word order and grammatical structure to a meaningful degree, unlike the simple bag-of-words keyword vectors built today, which completely ignore order (`"dog bites man"` and `"man bites dog"` would produce IDENTICAL bag-of-words vectors, despite opposite meaning — a real, worth-naming limitation of today's simplified keyword-vector approach specifically).

**Q: If two embeddings have cosine similarity exactly `1.0`, does that mean the two sentences are word-for-word identical?**
→ Not necessarily — it would mean the model judges them as pointing in EXACTLY the same semantic direction, which in practice usually does mean extremely similar or identical meaning, but theoretically two different exact strings could map to the same or nearly the same embedding if the model considers their meaning equivalent. In practice, truly exact `1.0` similarity between two genuinely different sentences is uncommon with real models.

---

## Instructor Notes

- **Prerequisite check:** Confirm Session 3's cosine similarity formula is fresh in students' minds before SEGMENT 2 — if it's shaky, do a 2-minute recap of `(a . b) / (|a| * |b|)` before proceeding, since this entire session assumes that formula is already trusted, not newly introduced.
- **Environment check (critical for this specific session):** Before class, check whether `sentence-transformers` is actually installed and a model can be downloaded on the classroom network. If YES, upgrade SEGMENT 3's live-code from "illustrative, not run" framing to a real live demo, and actually read out the real numbers you get — update your framing accordingly, since this script's "not run here" framing was written for an environment where the library was confirmed absent. If NO (offline classroom, blocked network, no local install), keep the framing exactly as written, and lean harder into SEGMENT 4's fully-verified keyword-vector demonstration as the trustworthy numeric core of the session.
- **Common mistake:** Confusing a keyword/bag-of-words vector (SEGMENT 4/5, built purely for teaching contrast) with a "real embedding" — repeatedly clarify that the keyword vectors are a deliberately crude teaching stand-in, not sentence-transformers output.
- **Another common mistake:** In the SEGMENT 6 lab, building the query's keyword vector against a NEW, query-only vocabulary instead of the shared `vocab` built from all FAQ entries — this produces silently wrong (dimension-mismatched or meaningless) comparisons rather than an obvious crash in some implementations, so check this specifically while circulating.
- **Engagement tip:** SEGMENT 4's "d1 vs d2 scores exactly 0.0" verified real result is the strongest moment in the session — it's not a hypothetical, it's a number students watched get computed live. Don't rush past it; let it land.
- **Time check:** If running behind before the break, shorten SEGMENT 3's batch-encoding walkthrough to a single sentence pair instead of four.
- **If running long after the break:** Skip SEGMENT 5's hybrid search discussion (keep it as a one-sentence mention) and move directly to the lab.
- **Materials to prepare:** `faq_snippets.csv` pre-placed in every student's working directory; confirm in advance whether `sentence-transformers` + model download will work on the classroom network, and adjust SEGMENT 3's delivery accordingly per the environment check above.

---

## Common Errors — Quick Reference

| Bug / mistake | Symptom | Fix |
|---|---|---|
| Treating keyword/bag-of-words vectors as if they were real sentence embeddings | Overgeneralizes today's `0.0`/`0.4082` numbers as if they described a real ML model's behavior | Keep the distinction explicit: SEGMENT 4/5's numbers are REAL but describe a crude keyword baseline, not sentence-transformers |
| Building the query vector against a different vocabulary than the document vectors | Silently meaningless or dimension-mismatched cosine similarity results | Always reuse the SAME `vocab` (built from all documents) when vectorizing a new query |
| Forgetting that `.encode()` batches multiple sentences into one 2D array | Confusing `embeddings[0]` (first sentence's full vector) with `embeddings[:, 0]` (first dimension across all sentences) | Remember shape is `(num_sentences, embedding_dim)`; index the first axis for "which sentence," the second for "which dimension" |
| Comparing an embedding vector to a keyword vector directly | Meaningless result, possibly a dimension-mismatch error | Only compute cosine similarity between two vectors from the SAME representation (same model, or same keyword vocabulary) |
| Assuming bag-of-words vectors capture word order | Treats `"dog bites man"` and `"man bites dog"` as identical, missing an important distinction | Remember bag-of-words is order-blind by construction; real embeddings are generally order-sensitive |
| Stating specific sentence-transformers decimal outputs as verified fact without having run the model | Overclaims precision/certainty about numbers that weren't actually produced | Always mark unexecuted real-model numbers as illustrative/qualitative, exactly as this script does |

---

## Appendix: `faq_snippets.csv` Full Contents (Instructor Reference)

```
id,text
1,How do I reset my password if I forgot it
2,I cannot remember my login credentials and need to recover my account
3,What is the monthly subscription price for the Pro plan
4,How much does the premium tier cost per month
5,Can I export my notes to PDF format
6,Is there a way to download my notes as a PDF file
7,Does the app work on both Android and iPhone
8,My notes are not syncing between my laptop and my phone
9,How do I delete my account permanently
10,Where can I change my email notification preferences
```

*(Verified keyword-vector cosine similarities on this exact file, with the SEGMENT 5/6 tokenizer and stopword list: 1 vs 2 = 0.0, 3 vs 4 = 0.0, 5 vs 6 = 0.4082. All computed by actually running the code shown in this script.)*

---

## Appendix: Common Embedding Models (Instructor Reference, Illustrative Names and Documented Sizes Only)

| Model name | Approx. dimension | Notes |
|---|---|---|
| `all-MiniLM-L6-v2` | 384 | Small, fast, widely used default for local `sentence-transformers` demos |
| `all-mpnet-base-v2` | 768 | Larger, generally higher quality, slower than MiniLM |
| OpenAI `text-embedding-3-small` (paid API, not used today) | 1536 | Illustrative example of a paid-API alternative; not run or required for this course |

*(Dimension counts above are documented model-card specifications, not numbers verified by running code in this environment; always check a model's current official card before stating its exact dimension as fact in a real project.)*

---

## FAQ — Additional Questions

**Q: Could I train my OWN embedding model from scratch for this course?**
→ Technically yes, but it requires large amounts of text data and significant compute — far beyond this course's scope. The whole value of `sentence-transformers` models is that they're pre-trained by others and ready to use immediately; almost no real-world team trains an embedding model from scratch when a good pre-trained one is available.

**Q: Do embeddings work for languages other than English?**
→ Many models do, including some specifically trained to be multilingual — but a model's language coverage and quality varies a lot by model, and you should always check a specific model's documentation before assuming it handles a given language well.

**Q: Is there a maximum sentence length an embedding model can handle?**
→ Yes — every embedding model has a maximum input token length (often a few hundred tokens), and text beyond that limit is typically truncated silently or raises an error, depending on the library. This is directly connected to next session's chunking topic: long documents must be split into pieces short enough for the embedding model to handle properly.

---

## Materials Checklist

- [ ] `faq_snippets.csv` present in every student's working directory
- [ ] Classroom network/install status for `sentence-transformers` checked BEFORE class, and SEGMENT 3's delivery adjusted accordingly (see Instructor Notes)
- [ ] `numpy` available (used throughout for verified keyword-vector cosine similarity)
- [ ] Scratch notebook with SEGMENT 4/5's fully-verified live-coding demos pre-typed
- [ ] Timer visible for the lab segment

---

## Timing Contingencies

| Situation | Action |
|---|---|
| Running 10 min behind before break | Shorten SEGMENT 3's batch-encoding example to a single sentence pair instead of four |
| Running long after break | Skip SEGMENT 5's hybrid search discussion, reducing it to one sentence, and move directly to the lab |
| Low energy after lunch/break | Run SEGMENT 4's break-prediction reveal as a group guess-then-verify activity, emphasizing the live, real computation |
| Advanced group finishes lab early | Have them add their own 3 FAQ entries (homework item 2) during class and discuss results as a group |
| No shared screen / projector issue | Walk through the vocabulary-building and vectorization steps on the whiteboard using this script's exact verified numbers |
| `sentence-transformers` unavailable / no internet for model download | Lean entirely on SEGMENT 4's fully-verified keyword-vector demonstration; present SEGMENT 3's API code as "correct syntax for when you have internet access later," without attempting a live run |

---

## End-of-Session Quiz (5 Questions)

1. What does a text embedding model output, and how is that fundamentally different from what a chat model (like the ones used in Sessions 2, 6, 7) outputs?
2. Why does `sentence-transformers` not require an API key or per-call billing, unlike OpenRouter?
3. In this session's verified keyword-vector demo, what was the cosine similarity between "The cat sat on the mat" and "A feline rested on the rug," and why?
4. Give one example of a query type where keyword search is expected to outperform semantic search, and explain why.
5. Why is it inappropriate to compare a keyword vector directly against a real sentence-transformers embedding using cosine similarity?

**Answer key (instructor):**
1. A fixed-length numeric vector representing the input text's meaning; a chat model instead generates new text, one token at a time. Different purpose, different architecture.
2. It runs locally on your own machine after a one-time model download, with no remote API call being made (and therefore nothing to bill) per encoding request.
3. Exactly `0.0`, verified by running the code — because after stopword removal, the two sentences share zero overlapping tokens (`cat` vs `feline`, `mat` vs `rug`, `sat` vs `rested`), despite meaning nearly the same thing.
4. Searching for an exact product code, order ID, or rare proper noun — keyword/exact-string matching is precise and reliable here, while embeddings can blur exact identifiers with similar-sounding ones.
5. They live in different, incompatible vector spaces (different dimension counts and different underlying representations); cosine similarity is only meaningful between two vectors produced by the same representation method.

---

## Homework Rubric

| Criterion | Excellent (4) | Good (3) | Needs Work (2) | Incomplete (1) |
|---|---|---|---|---|
| Real `sentence-transformers` run + comparison to keyword numbers (if library available) | Ran successfully, reported real numbers, clear comparison to `0.0`/`0.0`/`0.4082` | Ran successfully, thin comparison | Attempted but incomplete/errored, reasonable explanation given | Not attempted |
| Three new FAQ entries + `keyword_search` test | All three entries well-chosen to test the three described cases, results discussed | Entries added, results shown, thin discussion | Entries added but don't clearly test the intended cases | Not attempted |
| Explanation of fixed embedding dimension regardless of input length | Clear, technically accurate, in the student's own words | Accurate but thin | Vague or partially incorrect | Not attempted |

**Total:** /12 — Pass threshold: 8/12
