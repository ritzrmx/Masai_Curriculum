# Lecture Script: Generative AI — Chunking, Vector Stores & Retrieval
> **Instructor Reference** — Module 3: GenAI & Agents | Academic Session 16.3 | Duration: 2 Hours

---

## Session Overview
**Goal:** By the end of this session, students can chunk a long document with `RecursiveCharacterTextSplitter` and justify the chunk size and overlap, index chunks with metadata into both ChromaDB and FAISS, retrieve with similarity search and MMR, read distance scores correctly, wrap a store as a `VectorStoreRetriever`, and choose between Chroma and FAISS for a given situation.

**Student profile at this point:** They can generate embeddings and compare them with cosine (16.2), and they know context windows and token cost (13.1). They've never worked with a document longer than a few sentences in an AI pipeline. Likely wrong assumptions: "just embed the whole document," "bigger chunks keep more context so they're better," "a higher score is a better match" (true for cosine, false for distances), and "one of FAISS or Chroma must be the best." Boredom risk: low, but install friction with `chromadb` and `faiss-cpu` is real — check setups before class.

**Key outcome:** Students should leave asking, for any document collection: "How should I cut this, what metadata do I keep, which store fits, and how many chunks should come back?"

> 🎯 **The one sentence this session must land:** *Retrieval is only as good as your chunks — cut documents into focused, labelled pieces, store them in a vector store, and bring back a few relevant, non-repetitive ones.*

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| Opening — "The 300-Page Haystack" | 8 min | 8 min |
| Concept Block 1: Chunking with RecursiveCharacterTextSplitter | 10 min | 18 min |
| Concept Block 2: Chunk Size & Overlap Strategies | 10 min | 28 min |
| Practical Block 1: Cut the Handbook | 8 min | 36 min |
| Concept Block 3: ChromaDB & FAISS Setup and Indexing | 12 min | 48 min |
| **BREAK** | 10 min | 58 min |
| Concept Block 4: Similarity Search & MMR | 12 min | 70 min |
| Practical Block 2: Live Coding Demo (TA Code) | 14 min | 84 min |
| Concept Block 5: VectorStoreRetriever | 8 min | 92 min |
| Concept Block 6: ChromaDB vs FAISS | 6 min | 98 min |
| Practical Block 3: Pick the Store | 7 min | 105 min |
| Practical Block 4: Read the Scores | 7 min | 112 min |
| Summary & Bridge | 4 min | 116 min |
| Q&A & Doubt Solving | 4 min | 120 min |

---

## Opening — "The 300-Page Haystack" (8 min)

Open with this, verbatim-ish, holding up a thick printed document or scrolling a long PDF on screen:

> "Swiggy ops has finally given us the partner handbook: payouts, incentives, bank details, safety, insurance, app issues, ratings. A partner asks, 'bonus nahi mila barish wale din.' The answer is one paragraph — somewhere in here."

Pause. Ask the room:

> "Two ideas from earlier sessions: embed the whole handbook as one vector and compare, or paste the whole handbook into the LLM. What's wrong with each?"

(Steer to: one vector blurs everything together; pasting costs too much and may not fit — 13.1.)

> "Today we cut the handbook into focused pieces, catalogue them in a proper vector store, and pull back just the right two or three paragraphs in milliseconds. In class we use a short extract — seven sections, in `partner_handbook.txt`. It's written for this course, not Swiggy's real policy, and the code works unchanged on 300 pages."

**Pivot line:** "16.2 was search over 12 sentences. Today is search over a real document — the way every production RAG system starts."

**Context for sessions ahead:** "The retriever you build today becomes the 'R' in RAG in 17.1, and an agent's tool in 18.1."

---

## Concept Block 1: Chunking with RecursiveCharacterTextSplitter (10 min)

> "If someone asks where the rain bonus rule is, you don't hand them the handbook and say 'it's in there.' You open it to the paragraph. And when you cut an article to fit a notice board, you cut between paragraphs first, then sentences — mid-sentence only as a last resort. That's exactly what `RecursiveCharacterTextSplitter` does."

Write on the board:

> One big chunk → embedding points at the "average" of payouts + deductions + disputes → weak match for any question
> Many small chunks → each points at one topic → strong match for the right one
> Metadata on every chunk: {"section": "4. Safety and Insurance"}

> "We split the handbook into its seven sections first and store each section's title as **metadata**, so every chunk remembers where it came from — for showing sources later, and for searching one section only."

### 🔴 The trap / highest-value moment
> "Cut carelessly — every 25 characters — and you get 'Rs 100 is deducted for ea' and 'ch cancellation'. Half a fact answers nothing. Write this down: *chunk at natural breaks — a chunk should be able to stand on its own.*"

---

## Concept Block 2: Chunk Size & Overlap Strategies (10 min)

> "When you photocopy a long document, you leave a little margin from the previous page at the top of each copy, so a sentence across the page break appears whole somewhere. That's overlap."

```python
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=80)
```

Write on the board:

> ~200 chars → precise facts, but may lose context
> ~500 chars → most policy Q&A — our starting point
> ~1,500 chars → whole procedures, but blurred meaning and more tokens later
> Overlap ≈ 10–20% of the chunk size; sizes are in characters, not words or tokens

### 🔴 The trap / highest-value moment
> "Remember Module 2's split ratio — 'a judgement call, not a formula'? Same here. Write this down: *there's no correct chunk size — try a few on real questions and keep the one that retrieves the right paragraphs.*"

---

## Practical Block 1: Cut the Handbook (8 min)

Show handbook section 4 (Safety and Insurance) on screen and give pairs five minutes to mark where they would cut it into chunks of roughly 500 characters, writing the metadata they'd attach to each. The natural cuts fall at the numbered paragraphs — 4.1 SOS, 4.2 insurance amounts, 4.3 the claim procedure, 4.4 threats — with `{"section": "4. Safety and Insurance"}` at minimum; praise pairs that add `{"subsection": "4.3"}`, since finer metadata means finer filtering. If a pair asks whether 4.2 and 4.3 should be one chunk because both are about insurance, say it depends on how partners ask — if they usually ask "how much am I covered and how do I claim" together, one chunk may be better. That's why you test with real questions.

---

## Concept Block 3: ChromaDB & FAISS Setup and Indexing (12 min)

> "A library doesn't pile books on the floor — it shelves them with a catalogue. A **vector store** is the catalogue for embeddings: text, vector and metadata together, searchable fast."

```python
chroma_db = Chroma.from_documents(chunks, emb, collection_name="partner_handbook",
                                  persist_directory="chroma_partner_handbook")
faiss_db = FAISS.from_documents(chunks, emb)
faiss_db.save_local("faiss_partner_handbook")
```

> "One line embeds every chunk with our 16.2 model, stores everything and builds the index. **ChromaDB** saves to its folder automatically — close Python, come back tomorrow, and it's still there. **FAISS** is a lightning-fast index-card box held in memory; you save it yourself."

### 🔴 The trap / highest-value moment
> "Run `Chroma.from_documents` three times on the same folder while debugging, and every paragraph is stored three times — your search returns triplicates. Write this down: *from_documents adds — delete the folder first, or load the existing store instead of rebuilding.*"

---

## BREAK (10 min)

---

## Concept Block 4: Similarity Search & MMR (12 min)

> "Ask three friends for a restaurant and all three say 'Paradise Biryani.' Relevant — but you learned only one thing. Better: Paradise, a dosa place and a café. Still relevant, and each adds something new."

```python
chroma_db.similarity_search_with_score("bonus nahi mila barish wale din", k=3)
chroma_db.max_marginal_relevance_search(
    "how is my weekly payout calculated", k=3, fetch_k=10, lambda_mult=0.5)
```

> "Similarity search returns the k closest chunks. The handbook is English and the question is Hinglish; the multilingual embeddings from 16.2 should bridge them, so the top result should be the rain-bonus paragraph from section 2 — let's check soon. **MMR** shortlists `fetch_k` similar chunks, then picks k that are relevant and different from each other; `lambda_mult` slides from pure relevance (1.0) to pure variety (0.0). For 'how is my weekly payout calculated', plain search may return three overlapping slices of one paragraph, while MMR returns the components, the deductions and the peak-hour rules."

### 🔴 The trap / highest-value moment
> "In 16.2, cosine similarity: higher means closer. Here, `similarity_search_with_score` returns a **distance**: lower means closer. Write this down: *before reading a score, ask — is this a similarity or a distance?* And use MMR for broad questions; for a precise single fact, plain similarity wins."

---

## Practical Block 2: Live Coding Demo (TA Code) (14 min)

**Handoff line (must match TA code file's opening comment):** "From 12 short messages to the whole Partner Handbook — let's chunk it, store it in ChromaDB and FAISS, and pull back the right section for a partner's question in milliseconds."

Hand off to `ta-code - Session 16.3 - Chunking, Vector Stores & Retrieval.py` (with `partner_handbook.txt` alongside), narrating each `# --- EXPLAIN ---` block aloud:

1. Split the handbook by section with metadata, and print the section names
2. Compare chunk counts at sizes 200, 500 and 1,500; show one sample chunk with its metadata
3. Build Chroma (point out the folder deletion — the duplicate trap) and FAISS
4. Run the Hinglish rain-bonus query on both stores — read the distances and timings
5. Compare plain similarity with MMR for "how is my weekly payout calculated" — point at the variety
6. *(Pause before the retriever section — Concept Block 5 comes next, then return for it and the reload-from-disk check)*

💬 If the rain-bonus chunk isn't first for the Hinglish query, welcome it. Say: "Romanised Hinglish is hard for embeddings — we saw this in 16.2. Look at where it did land, and remember the fix we'll build in 18.1: let an agent rephrase the question into clear English before searching."

💬 Expect a question: "FAISS was faster, but both took milliseconds — why does speed matter?" Welcome it. Say: "With 50 chunks it doesn't. With 50 million product descriptions, FAISS's design really shows. Choose for your scale."

---

## Concept Block 5: VectorStoreRetriever (8 min)

> "Instead of walking into the library yourself, you have a librarian on call. Ask a question; she brings back pages. You don't care how the shelves work."

```python
retriever = chroma_db.as_retriever(search_type="mmr", search_kwargs={"k": 3, "fetch_k": 10})
retriever.invoke("I fell off my bike during a delivery, what do I do?")
```

> "One standard object: `.invoke(question)` returns a list of documents. A RAG chain in 17.1 just needs *a* retriever — swap Chroma for FAISS and the chain doesn't change. Add `filter={"section": ...}` in `search_kwargs` to search one section only."

*(Return to the TA code: run the retriever, the safety-filtered retriever and the reload-from-disk check.)*

### 🔴 The trap / highest-value moment
> "Setting k = 20 'to be safe.' Every retrieved chunk is pasted into the LLM's prompt next session — more tokens, more cost, more noise. Write this down: *start with k = 3 or 4 — more isn't safer, it's noisier.*"

---

## Concept Block 6: ChromaDB vs FAISS (6 min)

> "A library built to grow, stay put and be organised, versus an index-card box built for raw speed."

Write on the board:

> ChromaDB: database · saves automatically · metadata filters · easy updates → apps that grow
> FAISS: in-memory library · you save it · built for speed at huge scale → large, mostly static collections

### 🔴 The trap / highest-value moment
> "Asking which one is 'better' is the wrong question. Write this down: *choose on persistence, updates, filtering and scale — not on which name you've heard more.*"

---

## Practical Block 3: Pick the Store (7 min)

Give pairs four minutes to choose Chroma or FAISS, with one reason, for four scenarios: the partner helpdesk, whose handbook is updated monthly and needs "search only Safety" (Chroma — persistence, easy updates, filters); a one-time research notebook searching 20 million product titles (FAISS — raw speed at scale, static data); a classroom experiment with 50 chunks (either — pick the one you know); a review-search feature where new reviews arrive every minute (Chroma, or another database-style store — frequent additions). Point out that nobody chose on "which is better"; they chose on persistence, updates, filters and scale.

---

## Practical Block 4: Read the Scores (7 min)

Show this output on screen and ask rapid questions: `dist=0.42 [2. Incentives] 2.2 Rain bonus...`, `dist=0.45 [2. Incentives] 2.1 Peak hours...`, `dist=0.91 [5. App Issues] 5.1 GPS problems...`. The best match is 0.42, the rain bonus — lower distance is closer. Peak hours sits close because it's in the same section and also about bonuses. The 0.91 chunk is there only because we asked for k = 3, so the third-best came back even though it isn't relevant. To stop irrelevant chunks coming back, use the `similarity_score_threshold` search type or a smaller k — and tune that cut-off on test questions, just like chunk size.

---

## Summary & Bridge (4 min)

| Concept | The one thing to remember |
|---|---|
| Chunking | Focused chunks cut at natural breaks, with metadata for sources and filters |
| Size & overlap | ~500 / 80 is a starting point — then test on real questions |
| ChromaDB & FAISS | Database with persistence and filters vs a blazing in-memory index |
| Similarity & MMR | Top k by closeness (check distance vs similarity); MMR for broad questions |
| Retriever | One standard `.invoke()` interface; keep k small |

Close on the thesis line: "Retrieval is only as good as your chunks — cut documents into focused, labelled pieces, store them in a vector store, and bring back a few relevant, non-repetitive ones."

**Bridge to next session:** "Today the partner asked about the rain bonus and got back three paragraphs of handbook. He doesn't want to read policy text at 11:40 pm. Session 17.1 — Building a RAG Pipeline — hands these chunks to an LLM, so he gets 'Your rain bonus is ₹10 per order; raise a dispute within 7 days' — answered from the handbook, not guessed."

---

## Q&A & Doubt Solving (4 min)

**Q: Should chunk size be measured in tokens instead of characters?**
→ You can — LangChain has token-based splitters. Characters are simpler to start with; roughly four English characters make one token, so 500 characters is about 125 tokens.

**Q: What about PDFs and Word files?**
→ LangChain has document loaders for PDFs, Word files, web pages and more. They produce the same `Document` objects, so everything from today applies.

**Q: What happens when the handbook is updated?**
→ With Chroma you can delete a section's old chunks (using metadata or IDs) and add the new ones. For a small handbook, re-indexing everything also works.

**Q: Does FAISS use cosine or distance?**
→ By default it uses straight-line (L2) distance. With normalised embeddings, ranking by L2 distance and by cosine gives the same order.

**Q: Isn't overlap wasting storage?**
→ A little — but it's cheap insurance against facts being cut in half. Typical overlap is 10–20% of the chunk size.

---

## Instructor Notes
- **Words not yet earned:** RAG chain, context injection and grounding (17.1), agents and tools (17.2), RAGAS (18.1), re-ranking.
- **Rehearse the Hinglish query:** run "bonus nahi mila barish wale din" before class so you know where the rain-bonus chunk lands with your model.
- **Biggest risk in this session:** install problems with `chromadb` and `faiss-cpu`, and the embedding model download. Ask students to install and load the model before class; the TA should have a working environment ready to share.
- **Board management:** keep the chunk-size trade-offs, the Chroma vs FAISS comparison and "distance: lower = closer" visible all session.
- **Common confusions, numbered:**
  1. Embedding whole documents as one vector
  2. Cutting chunks mid-fact
  3. Thinking chunk size is measured in words or tokens
  4. Re-running `from_documents` and creating duplicates
  5. Reading distances as similarities
  6. Using MMR for precise single-fact questions
  7. Setting k too high
- **Cross-references:** Session 16.2 supplied the embeddings; Session 13.1's context-window and cost lessons explain why k stays small; Session 17.1 consumes the retriever; Session 18.1 wraps it as an agent tool and measures context recall with RAGAS.
- **Local/cultural context notes:** "bonus nahi mila barish wale din" is a strong anchor query (Hinglish question, English handbook), and the Paradise Biryani MMR analogy always lands in Hyderabad.
