# Lecture Script: Generative AI — Text Embeddings & Semantic Search
> **Instructor Reference** — Module 3: GenAI & Agents | Academic Session 16.2 | Duration: 2 Hours

---

## Session Overview
**Goal:** By the end of this session, students can generate embeddings locally with sentence-transformers, compute cosine and dot product similarity (and explain when they're identical), compare semantic and keyword search on the same queries and say when each is right, use `HuggingFaceEmbeddings` in LangChain, and plot embeddings in 2D.

**Student profile at this point:** They built vectors, dot products and cosine by hand in 14.2, learned "walking downhill" in 16.1, and built LangChain workflows in 15.1–15.2. They've never generated a real embedding. Likely wrong assumptions: "each embedding number means something nameable," "0.6 similarity means 60% the same," and "semantic search is always better than keyword search." Boredom risk: low — the "where is my money" demo is a strong hook — but the model download (about 470 MB) can fail on slow Wi-Fi, so ask students to download it before class.

**Key outcome:** Students should leave asking, for any search problem: "Are people looking for meaning or for exact strings — and am I using the same embedding model for both sides?"

> 🎯 **The one sentence this session must land:** *An embedding turns meaning into direction — so "where is my money" and "kal ka paisa nahi aaya" can point the same way with zero shared words — but exact codes still need exact matching.*

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| Opening — "Where Is My Money?" | 8 min | 8 min |
| Concept Block 1: Embeddings & sentence-transformers | 14 min | 22 min |
| Practical Block 1: Predict the Neighbours | 8 min | 30 min |
| Concept Block 2: HuggingFaceEmbeddings in LangChain | 8 min | 38 min |
| Concept Block 3: Cosine vs Dot Product Similarity | 12 min | 50 min |
| **BREAK** | 10 min | 60 min |
| Concept Block 4: Semantic vs Keyword Search | 10 min | 70 min |
| Practical Block 2: Keyword vs Semantic Showdown | 8 min | 78 min |
| Practical Block 3: Live Coding Demo (TA Code) | 14 min | 92 min |
| Concept Block 5: Embedding Visualisation | 10 min | 102 min |
| Practical Block 4: When Does Keyword Win? | 10 min | 112 min |
| Summary & Bridge | 4 min | 116 min |
| Q&A & Doubt Solving | 4 min | 120 min |

---

## Opening — "Where Is My Money?" (8 min)

Open with this, verbatim-ish, with the helpdesk search box on screen showing the query "where is my money" and the keyword search's top result, "Where is the nearest hub?":

> "A partner at 11:40 pm — remember him from 13.1 — types 'where is my money'. Our search proudly returns directions to the hub, because it shares the words 'where' and 'is'."

Put three messages from the helpdesk history on screen — "Payout not credited since Friday", "kal ka paisa nahi aaya", "Weekly amount still showing pending". Pause. Ask the room:

> "These are what he needed. How many words do they share with 'where is my money'?"

(Zero.)

> "In 14.2 we drew arrows by hand on made-up axes. Today, a model trained by walking downhill — 16.1 — draws them for us, with 384 axes, and the cosine formula you already know does the searching."

**Pivot line:** "Today, search stops matching words and starts matching meaning."

**Context for sessions ahead:** "16.3 stores these vectors for a whole handbook, and 17.1 hands the best matches to an LLM to answer from. Today is the engine of RAG."

---

## Concept Block 1: Embeddings & sentence-transformers (14 min)

> "A map of Hyderabad gives every place two numbers, and close places get close numbers. An **embedding** is a map for meaning: close meanings, close directions. In 14.2 we invented two axes and scored messages by hand; a real embedding model has 384 axes and learned them itself."

```python
model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
vecs = model.encode(sentences, normalize_embeddings=True)   # shape (n, 384)
```

> "sentence-transformers is a kitchen in your own home: in 13.2 we paid a distant kitchen per order; here you download the recipe once and cook for free. We use the multilingual model because our partners write in Hindi and Hinglish; `all-MiniLM-L6-v2` is the popular, faster English-only choice."

### 🔴 The trap / highest-value moment
> "Someone always asks, 'Which number is the money one?' None of them alone — the model's axes aren't labelled like ours were. Write this down: *meaning lives in the direction of the whole vector, not in any single number.*"

---

## Practical Block 1: Predict the Neighbours (8 min)

Show the 12 helpdesk messages from the TA code and give pairs four minutes to predict the top two closest messages for three queries: "where is my money" (likely the payout messages, such as "Payout not credited..." and "kal ka paisa nahi aaya"), "bonus missing hai" (likely "mera peak hour bonus kahan hai" and "Rain bonus not added..."), and "I got hurt on duty" (likely "I had a small accident..." and "A customer threatened me..."). Have students write their predictions down — the TA demo will check them. Expect disagreement on the third ("threatened" isn't "hurt"); welcome it, and tell them to watch the actual scores, not just the ranking.

---

## Concept Block 2: HuggingFaceEmbeddings in LangChain (8 min)

> "Same home kitchen — but now with a standard plug that fits every LangChain appliance."

```python
emb = HuggingFaceEmbeddings(model_name="paraphrase-multilingual-MiniLM-L12-v2",
                            encode_kwargs={"normalize_embeddings": True})
emb.embed_documents([...])     # the texts you search through
emb.embed_query("...")         # one question
```

> "Two methods, because some models embed questions and documents slightly differently. You'll rarely call them yourself: in 16.3 you hand `emb` to a vector store once, and it calls them for you."

### 🔴 The trap / highest-value moment
> "A quiet bug: the handbook is embedded with `normalize_embeddings=True`, but a teammate creates a second embeddings object for queries without it — or with a different model. Each model draws its own meaning map, so the scores drift and nobody knows why. Write this down: *one embeddings object, same model and same settings, for documents and queries.*"

---

## Concept Block 3: Cosine vs Dot Product Similarity (12 min)

> "Back to 14.2's riders: we cared about the angle between their directions, not how far each one rode."

Write on the board:

> cosine(a, b) = (a · b) / (|a| × |b|) · dot(a, b) = a · b
> normalised (length 1) ⇒ cosine = dot product — and the dot product skips the division

> "What to expect, comparing 'Payout not credited since Friday': an English paraphrase scores high, the Hinglish 'kal ka paisa nahi aaya' medium to high, 'App keeps crashing' near 0. Romanised Hinglish is harder for these models than Devanagari Hindi — we'll see exactly how hard in the TA demo."

### 🔴 The trap / highest-value moment
> "Someone will write in a report, 'similarity 0.62 — they're 62% the same.' No — it's the cosine of an angle, not a percentage, and different models use different ranges. Write this down: *similarity scores are for ranking within one model — compare them to each other, not to 100%.*"

---

## BREAK (10 min)

---

## Concept Block 4: Semantic vs Keyword Search (10 min)

> "A new agent who only matches exact words misses 'paisa nahi aaya' when asked to find payout complaints. An experienced agent understands meaning."

Write on the board:

> KEYWORD: count shared words → "where is" matches "Where is the nearest hub?"
> SEMANTIC: cosine of embeddings → "where is my money" matches the payout messages

> "Semantic search wins whenever people say the same thing in different words or languages. Now — what if an agent searches 'P-20417'?" (Let them think.) "A partner ID has no meaning; its embedding lands somewhere arbitrary. Keyword search finds it exactly."

### 🔴 The trap / highest-value moment
> "After today, people want semantic search for everything. Write this down: *semantic for meaning, keyword for exact codes, IDs and names — the best systems use both.*"

---

## Practical Block 2: Keyword vs Semantic Showdown (8 min)

Rapid fire, students call out "keyword" or "semantic": "mera paisa kab aayega" (semantic); "Order #847201" (keyword); "app band ho jata hai" (semantic); "error E-104" (keyword); "how do I claim insurance after a fall" (semantic); "Rule 4.2(b)" (keyword). Point out the pattern: anything a person could rephrase is semantic; anything that must match character for character is keyword. If someone asks whether you can combine them, yes — it's called hybrid search, and it's common in production.

---

## Practical Block 3: Live Coding Demo (TA Code) (14 min)

**Handoff line (must match TA code file's opening comment):** "A partner types 'where is my money' — let's see which helpdesk messages keyword search finds, and which ones meaning-based search finds."

Hand off to `ta-code - Session 16.2 - Text Embeddings & Semantic Search.py`, narrating each `# --- EXPLAIN ---` block aloud:

1. Encode the 12 messages — show the (12, 384) shape and that each vector has length 1
2. Compare cosine by the 14.2 formula with the dot product — they're identical
3. Run keyword vs semantic search for "where is my money", "bonus missing hai" and "P-20417"
4. Check the predictions from Practical Block 1 — who got them right?
5. Get the same scores through `HuggingFaceEmbeddings`
6. *(Pause before the PCA plot — Concept Block 5 comes next)*

💬 Expect a comment: "For P-20417, semantic search returned something weird." Welcome it. Say: "Exactly the point — an ID has no meaning to embed, and keyword search nailed it."

💬 If "kal ka paisa nahi aaya" ranks lower than students predicted, welcome that too. Say: "Romanised Hinglish is genuinely hard for embedding models. It still beats keyword search, which found nothing. In 18.1, the agent will rephrase questions into clear English before searching — that's one real fix."

---

## Concept Block 5: Embedding Visualisation (10 min)

> "A globe is 3D; a printed map flattens it to 2D. Distances get a little distorted, but you can still see which cities are close. 384 dimensions can't be drawn, so **PCA** squashes them to two while keeping as much of the spread as possible."

*(Return to the TA code and run the PCA plot.)*

> "Look for the groups — payout messages near each other, app problems in another area, safety in another. (A Hinglish message may sit a little apart; that's the 2D squash plus the Hinglish difficulty.) Nobody told the model these categories — it's the same idea as clustering in Module 2."

### 🔴 The trap / highest-value moment
> "Flattening loses information: two points close on this plot might not be close in 384D. Write this down: *the 2D plot is for intuition — decisions use the real cosine scores.*"

---

## Practical Block 4: When Does Keyword Win? (10 min)

In pairs, students spend four minutes listing three helpdesk situations where keyword search should be used instead of semantic search, and one where you'd want both. Expected answers: keyword for partner IDs, order numbers, exact policy clause numbers, error codes and bank IFSC codes; both for "payout for order #847201 not received", where the order number needs an exact match and the complaint needs meaning. Point out that this last shape is a real query type that no single search method serves well.

---

## Summary & Bridge (4 min)

| Concept | The one thing to remember |
|---|---|
| Embeddings | Meaning as direction; no single number is nameable |
| sentence-transformers | Free and local; a multilingual model for Hindi and Hinglish |
| HuggingFaceEmbeddings | LangChain's standard plug — one object, same settings, both sides |
| Cosine vs dot product | Identical once vectors are normalised; dot product is faster |
| Semantic vs keyword | Meaning vs exact strings — use both where needed |
| Visualisation | PCA for intuition, cosine scores for decisions |

Close on the thesis line: "An embedding turns meaning into direction — so 'where is my money' and 'kal ka paisa nahi aaya' can point the same way with zero shared words — but exact codes still need exact matching."

**Bridge to next session:** "Today we searched 12 short messages. A real partner handbook runs to hundreds of pages — you can't embed a whole page as one vector and expect precise answers, or loop over thousands of vectors in Python. Session 16.3 — Chunking, Vector Stores & Retrieval — splits the handbook into chunks, stores them in ChromaDB and FAISS, and retrieves the best ones in milliseconds."

---

## Q&A & Doubt Solving (4 min)

**Q: Are paid API embeddings better than sentence-transformers?**
→ Paid embeddings are often stronger on benchmarks, but they cost money per call and send your text outside. For this course, local models are free and good enough — test on your own queries before deciding.

**Q: How long can the text be for one embedding?**
→ Each model has a maximum input length; beyond it, the text gets cut off. That's one of the two big reasons for chunking in 16.3.

**Q: Can I embed images?**
→ Yes, with image or multimodal embedding models — same idea, different model.

**Q: Why 384 numbers and not 10 or 10,000?**
→ It's a design choice when the model is built: more numbers can capture finer meaning but cost more storage and compute. 384 is a common small-and-fast size.

**Q: Does the model understand Telugu too?**
→ The multilingual model was trained on 50+ languages, including several Indian ones, but quality varies by language and script. Always test with real partner messages.

---

## Instructor Notes
- **Words not yet earned:** vector store, chunk, retriever and MMR (16.3), RAG (17.1), approximate nearest neighbour search.
- **Biggest risk in this session:** the model download failing in class. Ask students to run `SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")` the day before; the TA should have it cached.
- **Board management:** keep the "where is my money" query with both result lists visible all session, and box "normalised ⇒ cosine = dot product".
- **Common confusions, numbered:**
  1. Thinking individual embedding numbers have names
  2. Mixing embedding models or settings between queries and documents
  3. Reading similarity scores as percentages
  4. Assuming semantic search always beats keyword search
  5. Over-trusting the 2D PCA plot
- **Cross-references:** Session 14.2 supplied the cosine formula; Session 16.1 explained how embedding models are trained; Session 16.3 stores these vectors; Session 17.1 feeds retrieved chunks to the LLM; Session 18.1's agent rephrases Hinglish queries; Module 2's clustering connects to the PCA picture.
- **Local/cultural context notes:** the 11:40 pm partner and the "kal ka paisa nahi aaya" pair carry forward from 13.1 and 14.2 — remind students they first met the pair in the vectors master class. Rehearse the Hinglish queries before class so you know how your model ranks them.
