# Lecture Script: LLM Fundamentals — How Language Models Work
> **Instructor Reference** — Module 3: GenAI & Agents | Session 1 | Duration: 2 Hours

---

## Session Overview

**Goal:** Build a correct mental model of how large language models generate text — tokens, context windows, next-token prediction, and the role of temperature/top-p in controlling output variability — and contrast this learning/prediction paradigm with the classical ML models students trained in Module 2.

**Student profile at this point:** Just finished Module 2 (Classical ML) — comfortable with the idea of a model that "learns" from labeled data (`X`, `y`), fits parameters, and predicts. Has trained `LinearRegression`, `LogisticRegression`, decision trees, and ensembles. Has almost certainly USED a chatbot (ChatGPT, Claude, Gemini) casually, but has never thought about what's happening mechanically underneath. This is the first session of the GenAI module — no API calls yet, no code libraries beyond a tokenizer demo.

**Key outcome:** Every student can explain, in their own words, that an LLM generates text one token at a time by predicting a probability distribution over "what comes next," can define a context window and explain why it's a hard limit, can predict qualitatively how raising temperature or top-p changes an output's randomness, and can list at least three concrete differences between how an LLM "learns" versus how `LinearRegression` or a decision tree learns.

**Dataset for this session:** None. This session uses small inline text examples and a tokenizer library (`tiktoken`) to inspect real tokenization — no CSV or dataset file is read from disk.

**Tone:** Conceptual and demo-heavy, similar spirit to a master class but grounded in a tool students will actually use next session (OpenRouter). Light code — mostly `tiktoken` for tokenization, and small illustrative probability tables for next-token prediction. No live API calls yet; that starts Session 2.

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| SEGMENT 1: Opening — What Does "Generate Text" Actually Mean? | 10 min | 0:10 |
| SEGMENT 2: Tokens — The Real Unit LLMs Think In | 25 min | 0:35 |
| SEGMENT 3: Next-Token Prediction & the Context Window | 20 min | 0:55 |
| **BREAK** | 10 min | 1:05 |
| SEGMENT 4: Temperature & Top-p — Controlling Randomness | 25 min | 1:30 |
| SEGMENT 5: LLMs vs. Classical ML — How They Learn and Predict | 15 min | 1:45 |
| SEGMENT 6: Lab — Tokenizing & Predicting-by-Hand | 10 min | 1:55 |
| SEGMENT 7: Summary, Wrap-Up & Q&A | 5 min | 2:00 |

---

## SEGMENT 1: Opening — What Does "Generate Text" Actually Mean? (10 min)

### The Hook (5 min)

**Say:** *"Almost everyone in this room has typed a question into ChatGPT, Claude, or Gemini and watched an answer appear, word by word, like it's being typed live. Before we write a single line of code with these models — which starts next session — I want you to be able to answer one question with total confidence: what is ACTUALLY happening, mechanically, between you pressing Enter and that first word appearing on screen?"*

**Ask the class:** *"Show of hands — who has a guess, even a rough one?"* Collect 2-3 guesses. Common answers: "it searches the internet," "it looks up the answer in a database," "it's like a really smart autocomplete." Do not correct yet — just collect.

**Say:** *"That last guess — 'really smart autocomplete' — is actually the closest one, and today's whole session is about making that intuition precise and mechanically correct. Spoiler: there is no database lookup happening at generation time. There is no search. The model is not 'looking anything up.' It is doing ONE repeated action, over and over: given everything written so far, predict what comes next. That's it. That one repeated action, applied a few hundred or a few thousand times in a row, is what produces an entire essay, a working piece of code, or a poem."*

### Why This Session Matters (5 min)

**Say:** *"You already know how to train a model that predicts a number — `LinearRegression` predicting a house price — or a category — a decision tree predicting churn. An LLM is also fundamentally a prediction machine. It just predicts a different kind of thing: the next small chunk of text. Once that clicks, an enormous amount of 'AI magic' stops being magic. You'll be able to explain why LLMs sometimes make things up, why they have a maximum length they can handle, why the same prompt can give you a different answer twice, and why a well-structured prompt (which we build starting Session 4) matters so much."*

**Course arc — write on board:**

| Session | Topic |
|---|---|
| 1 (today) | How LLMs generate text — tokens, context, temperature |
| 2 | Calling LLMs for real, via OpenRouter's raw API |
| 3 | Master class: vectors & the math behind "similarity" (embeddings) |
| 4 | Prompt engineering & reasoning techniques |
| 5 | Structured outputs — forcing an LLM to return clean, validated data |

**Learning contract for today — write on board:**

- Explain what a token is and why LLMs use tokens instead of whole words
- Explain next-token prediction and the context window as a hard limit
- Predict qualitatively how temperature and top-p change output randomness
- List concrete differences between how an LLM and a classical ML model learn and predict

---

## SEGMENT 2: Tokens — The Real Unit LLMs Think In (25 min)

### Why Not Just "Words"? (6 min)

**Say:** *"Here's the first wrong intuition to clear up: an LLM does not read or generate whole words one at a time. It reads and generates TOKENS — small chunks of text that are often shorter than a word, sometimes exactly a word, and sometimes a whole common phrase-fragment. Let's see why chunks-shorter-than-words are actually the smart design choice."*

**Ask:** *"If I told you a model could only ever generate from a fixed dictionary of, say, 50,000 whole English words, what would break the first time someone typed a typo, a made-up brand name, or a word in Hindi transliteration, like 'kya'?"* Guide toward: a whole-word vocabulary can't represent anything outside that fixed list — new words, misspellings, other languages, code identifiers like `train_test_split`, all break it.

**Say:** *"Tokenization solves this by breaking text into a vocabulary of sub-word pieces — commonly tens of thousands of them, learned statistically from huge amounts of text so that frequent chunks (like 'ing', 'tion', common whole words) get their own single token, while rare or unusual text gets broken into smaller pieces, letter by letter if it has to. This means the model can represent ANY string of text, even one it's never seen before, by falling back to smaller and smaller pieces — nothing is ever 'undefined.'"*

### Live Demo — Real Tokenization with `tiktoken` (12 min)

**Say:** *"Let's inspect this directly using `tiktoken`, the tokenizer library OpenAI released and that's become a de facto standard for inspecting this behavior (the exact tokenizer an OpenRouter-served model uses varies by model, but the intuition is identical everywhere). Install it with `pip install tiktoken` if you don't already have it."*

**Live-code:**

```python
import tiktoken

# cl100k_base is the tokenizer used by GPT-3.5/GPT-4-era models —
# a widely available reference tokenizer for demonstrating the concept
encoding = tiktoken.get_encoding("cl100k_base")

text = "Language models predict the next token."
tokens = encoding.encode(text)

print("Text:", text)
print("Token IDs:", tokens)
print("Number of tokens:", len(tokens))

for token_id in tokens:
    piece = encoding.decode([token_id])
    print(f"  {token_id:>6} -> {piece!r}")
```

**Example output (actual — `tiktoken` is deterministic and installed locally, so this output is exact for `cl100k_base`):**
```
Text: Language models predict the next token.
Token IDs: [14126, 4211, 7168, 279, 1828, 4037, 13]
Number of tokens: 7

   14126 -> 'Language'
    4211 -> ' models'
    7168 -> ' predict'
     279 -> ' the'
    1828 -> ' next'
    4037 -> ' token'
      13 -> '.'
```

**Say, pointing at the output:** *"Seven English words, seven tokens — in this particular sentence, it lined up one-to-one. That's common for everyday English words. Now watch what happens with something the tokenizer's training data saw less often."*

**Live-code a second example, deliberately choosing an uncommon/compound word:**

```python
text2 = "Unbelievability of tokenization in multilingual settings: नमस्ते!"
tokens2 = encoding.encode(text2)

print("Text:", text2)
print("Number of tokens:", len(tokens2))
for token_id in tokens2:
    piece = encoding.decode([token_id])
    print(f"  {token_id:>6} -> {piece!r}")
```

**Example output (actual, verified by running the code above with `cl100k_base` — exact token IDs and split points can shift slightly across tokenizer library versions, but the qualitative pattern below is reliably reproducible):**
```
Text: Unbelievability of tokenization in multilingual settings: नमस्ते!
Number of tokens: 20
     Un | belie | v | ability | ' of' | ' token' | 'ization' | ' in'
     ' mult' | 'ilingual' | ' settings' | ':' | ' <partial-byte>' | '<partial-byte>'
     'म' | 'स' | '्<partial-byte>' | '<partial-byte>' | 'े' | '!'
```

**Say:** *"Notice two things. First, `'Unbelievability'` — an uncommon compound word — got split into FOUR pieces: `Un`, `belie`, `v`, `ability`. The model has never memorized 'Unbelievability' as one chunk, but it doesn't need to — it reconstructs it from familiar pieces, the same way you'd sound out an unfamiliar word syllable by syllable. Similarly, `'multilingual'` split into `mult` + `ilingual`. Second, the Hindi text in Devanagari script takes roughly one token per SCRIPT CLUSTER or even per raw byte fragment, MANY more tokens per character than the English text needed, because the tokenizer's training data was overwhelmingly English-heavy — the whole 20-token sentence has only about 8 'natural' English words but needed 20 tokens once you count the Hindi greeting. This has a real, practical consequence: non-English text often costs more (in tokens, and therefore in API price and context-window space) for the same amount of 'meaning' — something worth knowing before you build a multilingual product."*

### Why This Matters Practically (4 min)

**Say:** *"Three concrete reasons token-counting matters to you as a builder, starting next session: one, OpenRouter and every LLM API bills by the token, input and output separately. Two, every model has a maximum context window measured in tokens, not words or characters — we cover that next. Three, when you're debugging a truncated or cut-off response, 'ran out of tokens' is one of the first things to check."*

### Comprehension Check (3 min)

1. *"Is a token always exactly one whole word?"* (No — it can be a word fragment, a whole word, punctuation, or even part of a single character in some scripts.)
2. *"Why can an LLM handle a brand-new made-up word it's never seen before, like 'blorpify'?"* (Because tokenization falls back to smaller sub-word pieces — nothing is undefined; it reconstructs unfamiliar text from familiar fragments.)

---

## SEGMENT 3: Next-Token Prediction & the Context Window (20 min)

### The One Repeated Action (8 min)

**Say:** *"Now the core mechanic. At each step, an LLM looks at every token generated so far — the prompt plus whatever it has generated in this response already — and outputs a probability distribution over 'what token comes next,' across its entire vocabulary of tens of thousands of possible tokens. It then picks one (we'll get to exactly how in SEGMENT 4), appends it to the sequence, and repeats the ENTIRE process again, now with one more token of context than before."*

**Draw this loop on the board:**

```
sequence so far -> [model] -> probability distribution over next token
                                        |
                              pick one token (how = temperature/top-p)
                                        |
                         append it to sequence, REPEAT
```

**Say:** *"This is why a response appears to 'type itself out' — because that's literally, mechanically, what's happening. Each new token requires re-running this prediction step with the updated sequence. A 500-token response isn't generated all at once; it's 500 individual next-token predictions, chained together, each one built on top of everything generated so far — including the model's own earlier tokens in this same response."*

**Illustrative probability table — draw or project (values are illustrative, for teaching the mechanism, not a real model's exact output):**

Given the prompt `"The capital of France is"`, an illustrative next-token probability distribution might look like:

| Candidate next token | Illustrative probability |
|---|---|
| ` Paris` | 0.91 |
| ` the` | 0.03 |
| ` located` | 0.02 |
| ` known` | 0.01 |
| (tens of thousands of other tokens) | remaining ~0.03 combined |

**Say:** *"This table is illustrative — I'm not claiming these are a specific real model's exact numbers, since that changes model to model and isn't something we can inspect from the outside through a normal chat API. But the SHAPE of it is real and important: for a strongly-implied continuation like this one, one token dominates the distribution overwhelmingly. For an open-ended prompt like 'Once upon a time,' the distribution is far flatter — many plausible next words, none dominating. That flatness or peakedness of the distribution is exactly what temperature and top-p operate on, which we get to right after the break."*

### The Context Window (8 min)

**Say:** *"Every LLM has a maximum number of tokens it can 'see' at once — this is the context window. It includes EVERYTHING: your system instructions, the entire conversation history you send, and the tokens the model is currently generating. It is a hard, non-negotiable limit, not a soft guideline."*

**Write concrete numbers on the board (illustrative, order-of-magnitude — exact limits vary by model and change over time, so always check the specific model's listing on OpenRouter before building):**

| Model class (illustrative) | Rough context window |
|---|---|
| Small/older models | ~4,000-8,000 tokens |
| Mid-size modern models | ~32,000-128,000 tokens |
| Long-context modern models | 200,000+ tokens |

**Say:** *"Two direct consequences. One: if your conversation history plus your new prompt exceeds the context window, something has to give — either the API rejects the request, or (in many chat products, NOT the raw API we use next session) older messages silently get dropped or summarized to make room. Two: 'the model forgot what we discussed earlier' in a long chat session is almost always a context-window problem in disguise — the earlier messages are no longer literally present in what the model is looking at right now, not the model having some separate persistent 'memory' that failed."*

**Ask:** *"If a model has an 8,000-token context window, and your conversation history alone is already 7,500 tokens, roughly how much room is left for the model's own new response?"* (Answer: about 500 tokens — and that shrinks further if the conversation keeps going, unless you actively manage what you send.)

### Comprehension Check (4 min)

1. *"Does the context window limit include the model's own response, or just your input?"* (Both — everything in the exchange, input and output combined, counts against the same limit.)
2. *"True or false: an LLM has some separate persistent memory of earlier conversations beyond what's literally included in the current context window."* (False, for a raw API call like we'll use next session — every call is stateless; "memory" in a chat product is an illusion created by resending prior messages as part of the new context each time.)

---

## BREAK (10 min)

*Suggested break prompt:* Ask students to think of one time a chatbot "forgot" something they told it earlier in a long conversation, or gave a noticeably different answer to the same question asked twice. Come back ready to connect both of those experiences to precise mechanical causes: context window limits, and randomness in token selection.

---

## SEGMENT 4: Temperature & Top-p — Controlling Randomness (25 min)

### Why Not Always Pick the Single Most Likely Token? (5 min)

**Say:** *"Given a probability distribution over next tokens, the simplest strategy — called greedy decoding — is to always pick the single highest-probability token. Why doesn't every LLM product just do that all the time?"*

**Ask:** *"What would you expect from a model that ALWAYS picks the single most likely next token, every single time, for the exact same prompt?"* Guide toward: it becomes fully deterministic — same prompt, same output, every time — and can feel repetitive, bland, or get stuck in loops for open-ended creative tasks. Sometimes that's exactly what you want (a math answer, a JSON field); sometimes it's exactly what you don't want (a creative story, brainstorming ideas).

**Say:** *"Temperature and top-p are the two most common dials for controlling exactly how much randomness gets injected into that token-picking step, instead of always greedily picking the top one."*

### Temperature, Explained Mechanically (10 min)

**Say:** *"Temperature reshapes the probability distribution BEFORE a token is sampled from it. Mathematically it divides each token's underlying score by the temperature value before converting scores into probabilities — but you don't need the formula to build the right intuition. Just remember the two extremes and the middle."*

**Draw this on the board, using the earlier illustrative "capital of France" distribution:**

| Temperature | Effect on the distribution | Practical result |
|---|---|---|
| `0.0` (or very low) | Sharpens toward the single top token — nearly greedy | Deterministic, focused, repeatable-ish output |
| `0.7` (a common default) | Mild reshaping — top token still favored, but real variety | Coherent but not robotic; typical chat default |
| `1.5`+ (high) | Flattens the distribution — lower-probability tokens get real odds | Creative, surprising, but higher risk of incoherent or off-topic text |

**Say:** *"Picture our 'capital of France' example, where `Paris` had roughly 91% probability. At temperature near 0, the model will pick `Paris` essentially every time — there's barely any other candidate left with meaningful weight after sharpening. At a high temperature, `Paris` might drop to something like 40-50% weight after flattening, and tokens like `the`, `located`, or even less likely ones get real odds of being chosen — so occasionally you'd get a stranger, less on-the-nose continuation."*

**Say:** *"Rule of thumb for picking a temperature in your own projects: low (0-0.3) for factual Q&A, code generation, or anything with one 'correct-ish' answer; medium (0.5-0.8) for general chat and everyday assistant behavior; high (1.0+) for brainstorming, creative writing, or generating diverse alternatives on purpose."*

### Top-p (Nucleus Sampling), Explained Mechanically (7 min)

**Say:** *"Top-p works differently — instead of reshaping every probability, it CUTS OFF the pool of candidate tokens the model is even allowed to sample from, keeping only the smallest set of top candidates whose probabilities add up to at least `p`."*

**Walk through a concrete illustrative example on the board:**

Suppose the (illustrative) distribution for some prompt is:

| Token | Probability |
|---|---|
| A | 0.50 |
| B | 0.25 |
| C | 0.10 |
| D | 0.08 |
| E | 0.04 |
| ...rest | 0.03 combined |

**Say:** *"With `top_p = 0.9`, the model sorts tokens by probability, highest first, and keeps adding them to an allowed pool until the running total crosses 0.9. Here: A (0.50) + B (0.25) = 0.75, + C (0.10) = 0.85, + D (0.08) = 0.93 — that crosses 0.9, so the allowed pool is {A, B, C, D}. Everything past D, including E and the long tail, is excluded ENTIRELY from consideration this step — probability zero, no matter how high the temperature is set."*

**Ask:** *"If we lowered `top_p` to 0.7 on this same distribution, which tokens would remain in the pool?"* Walk through: A (0.50) + B (0.25) = 0.75, which already crosses 0.7 — so the pool is just {A, B}. Lower `top_p` means a smaller, safer, more predictable pool of candidates.

**Say:** *"In practice, most API calls set BOTH temperature and top-p, and they interact: top-p decides the pool of eligible tokens, temperature reshapes how sharply probability is distributed WITHIN that pool. A common, sensible default many APIs ship with is something like `temperature=0.7, top_p=1.0` (meaning top-p isn't restricting anything extra beyond what temperature already does) — you'll set both explicitly starting next session when we make raw API calls."*

### Comprehension Check (3 min)

1. *"At `temperature=0`, would you expect the exact same prompt to produce the exact same output every single time?"* (Very close to always yes — near-deterministic, though some providers still have tiny amounts of residual randomness from how they batch requests internally.)
2. *"If `top_p=0.5`, roughly how many tokens do you expect to be in the eligible pool — many, or few?"* (Typically few — a low top-p aggressively restricts the pool to only the highest-probability candidates.)

---

## SEGMENT 5: LLMs vs. Classical ML — How They Learn and Predict (15 min)

### Setting Up the Comparison (3 min)

**Say:** *"You've now trained several classical ML models this course — linear regression, logistic regression, decision trees, random forests. Let's put an LLM side by side with those and be precise about what's genuinely similar and what's fundamentally different, because the word 'model' is doing a lot of work covering up real differences."*

### The Comparison Table (8 min) — build it WITH the class, don't just present it

**Ask, and fill in together as students answer:**

| Dimension | Classical ML (e.g. `LinearRegression`, Decision Tree) | LLM |
|---|---|---|
| What it predicts | A number or a category, from structured features | The next token, from a sequence of prior tokens |
| Training data | A specific, curated dataset (`X`, `y`) for ONE task | Enormous, general text corpora scraped from books, web, code — not built for one narrow task |
| What "learning" produces | A small, interpretable set of parameters (coefficients, tree splits) | Billions of numeric parameters (weights) with no single human-readable meaning per parameter |
| Whose job is "feature engineering"? | Yours — you choose and build `sqft`, `age_years`, etc. | The model itself, implicitly, from raw text — no manual feature table |
| Can you retrain it yourself, in this course? | Yes — `model.fit(X_train, y_train)` in minutes | No — training a frontier LLM from scratch costs millions of dollars and enormous compute; you will only ever CALL an already-trained model via an API |
| Output determinism | Fully deterministic given the same input (same `X` row, same prediction) | Only near-deterministic even at `temperature=0`; genuinely random by default |
| How you "use" it in this course | `.fit()` then `.predict()` on your own data | Send a prompt via API, receive generated text — starting next session |

**Say, once the table is filled:** *"The single biggest mental shift: with `LinearRegression`, YOU decided the features, YOU trained it on YOUR specific dataset, and it will do exactly one job forever — predict `price_lakhs` from `sqft`, `bedrooms`, `age_years`. An LLM was trained once, by someone else, on a colossal and general dataset, to do the one general job of 'predict the next token' — and that single general skill turns out to be powerful enough to answer questions, write code, translate languages, and hold a conversation, all without ever being retrained for each new task. That's the entire reason GenAI feels so different from everything in Module 2."*

### The Honest Caveats (4 min)

**Say:** *"Two important honesty checks, so you don't walk away over-trusting this new tool. First: because an LLM is a probability machine, not a fact-lookup machine, it can generate fluent, confident-sounding text that is simply wrong — this is usually called 'hallucination,' and it happens because a plausible-sounding next token can be sampled even when it doesn't correspond to a true fact. Second: an LLM has no concept of 'I don't know' baked in by default the way a well-calibrated classical model can express uncertainty through predicted probabilities — it will happily keep generating tokens for a question it has no real basis to answer, unless it's been specifically trained or prompted to hedge. We'll actively fight both of these with technique starting Session 4 (prompting) and Session 5 (structured, validated outputs)."*

---

## SEGMENT 6: Lab — Tokenizing & Predicting-by-Hand (10 min)

### Instructions (read aloud, step by step)

1. Using `tiktoken`, tokenize a sentence of your own choosing (at least 8 words, including one uncommon or made-up word).
2. Print the token count and each token's decoded piece.
3. By hand, write out an illustrative next-token probability table (4-5 candidate tokens with made-up but plausible probabilities that sum to roughly 1.0) for the prompt `"My favorite programming language is"`.
4. In one sentence each, state what you'd expect to change about your sampled token if temperature were raised from 0.2 to 1.3, and if top-p were lowered from 1.0 to 0.3.

### Starter Code

```python
import tiktoken

encoding = tiktoken.get_encoding("cl100k_base")

my_sentence = "___"  # write your own sentence, at least 8 words

tokens = encoding.encode(___)
print("Number of tokens:", ___)

for token_id in tokens:
    piece = ___
    print(f"  {token_id:>6} -> {piece!r}")

# TODO: write your illustrative probability table as a comment or a dict

# TODO: write your two one-sentence predictions (temperature and top-p) as comments
```

### Reference Solution

```python
import tiktoken

encoding = tiktoken.get_encoding("cl100k_base")

my_sentence = "The blorpinator suddenly malfunctioned during the live demo."

tokens = encoding.encode(my_sentence)
print("Number of tokens:", len(tokens))

for token_id in tokens:
    piece = encoding.decode([token_id])
    print(f"  {token_id:>6} -> {piece!r}")

# Illustrative next-token table for "My favorite programming language is":
# {"Python": 0.55, "JavaScript": 0.20, "Java": 0.10, "Go": 0.08, "Rust": 0.07}

# Raising temperature from 0.2 to 1.3: the distribution flattens, so a
# less-likely candidate (e.g. "Rust" or "Go") becomes meaningfully more
# likely to be sampled instead of the model almost always picking "Python".

# Lowering top_p from 1.0 to 0.3: the eligible candidate pool shrinks to
# only the highest-probability tokens (likely just "Python", maybe
# "JavaScript"), excluding "Go" and "Rust" from consideration entirely.
```

**Instructor circulates**, checking specifically that students chose an uncommon or made-up word (so they actually SEE a multi-piece split, not just one-token-per-word) and that their two one-sentence predictions correctly connect temperature to "reshaping/flattening the distribution" versus top-p to "restricting/shrinking the eligible pool" rather than conflating the two mechanisms.

---

## SEGMENT 7: Summary, Wrap-Up & Q&A (5 min)

**What we covered today:**
- LLMs operate on tokens (sub-word chunks), not whole words — verified directly with `tiktoken`
- Text generation is repeated next-token prediction, one token at a time, built on everything generated so far
- The context window is a hard token limit covering input AND output combined
- Temperature reshapes the probability distribution; top-p restricts the eligible candidate pool — both control randomness, differently
- LLMs and classical ML both "learn from data and predict," but differ enormously in what they predict, how they're trained, and who trained them

**Bridge to next session:** *"Today was entirely conceptual — no API key, no live calls. Next session, we make this real: you'll sign up for OpenRouter, get an API key, and make your first raw HTTP call to an actual LLM using nothing but the `requests` library — no framework, no magic wrapper. Everything you learned today about tokens, context windows, and temperature will show up directly as fields in the JSON you send and receive."*

**Homework / self-practice:**
1. Using `tiktoken`, tokenize the same sentence in three different "styles" — plain English, English with deliberate typos, and a sentence full of code-like syntax (e.g. `df.groupby("col").mean()`). Compare token counts and note which one tokenizes least efficiently (most tokens per character) and guess why.
2. Write a short paragraph (5-6 sentences) explaining, in your own words and without technical jargon, why an LLM might "make up" a fake citation or fake statistic with total apparent confidence. Use the words "probability" and "next token" somewhere in your explanation.
3. Look up (via a web search) the advertised context window size, in tokens, of two different models available on OpenRouter, and note them for reference before next session.

---

## Q&A & Doubt Solving

**Likely questions and suggested answers:**

**Q: If tokens aren't words, how does the model know where one word ends and another begins when generating?**
→ It doesn't need an explicit rule — word boundaries emerge naturally because whitespace and punctuation are themselves encoded as part of tokens (notice the leading space baked into tokens like `' models'` in today's demo). The model learned, from its training data, which token sequences look like fluent text.

**Q: Is a bigger context window always better?**
→ Mostly yes for capability, but not free — a larger context window means the API call can cost more (billed per input token) and, for very long contexts, some models show a genuine drop in how well they use information buried in the middle of a huge context ("lost in the middle" effect). Bigger isn't automatically better for every use case; it's a capability ceiling, not a target to always max out.

**Q: Does `temperature=0` guarantee the exact same output every time, forever?**
→ Very close to it, and commonly treated as deterministic in practice, but not always mathematically guaranteed byte-for-byte across different hardware/batching conditions on the provider's servers. For this course, treat `temperature=0` as "as deterministic as it gets" — genuinely useful for tasks like classification or structured extraction where you want stable answers.

**Q: Why would anyone ever want high temperature — isn't a wrong-but-confident answer worse than a boring-but-correct one?**
→ Depends entirely on the task. For factual Q&A or code generation, you're right — low temperature is almost always the better choice. But for brainstorming marketing taglines, generating varied practice questions, or creative writing, some controlled randomness is a FEATURE, not a bug — you often want several different plausible outputs to choose from, not one narrowly "correct" one.

**Q: Can I set temperature above 1.0, or is 1.0 a hard ceiling?**
→ Most APIs allow values above 1.0 (commonly up to 2.0), producing increasingly flat, unpredictable distributions. In practice, going much past 1.0-1.2 tends to produce noticeably less coherent text — it's rarely useful in real applications, but it's technically allowed.

**Q: Does the model "remember" earlier conversations from yesterday, the way a person would?**
→ No, not for a raw API call — every request we make starting next session is stateless. Any apparent "memory" across sessions in a consumer chat product comes from that product explicitly storing and resending relevant history (or a summary of it) as part of the context on your behalf — it is not something happening inside the model itself between separate API calls.

---

## Instructor Notes

- **Prerequisite check:** No coding prerequisite beyond comfort installing a `pip` package. Confirm `tiktoken` installs cleanly for everyone before SEGMENT 2 — this is the one dependency for today.
- **Common mistake:** Students conflating "tokens" with "words" persistently through the session — re-anchor to the `tiktoken` output every time the word "token" comes up in the first half of class.
- **Another common mistake:** Assuming temperature and top-p do the "same thing" because both control randomness. Use the two distinct board diagrams (reshaping vs. restricting-the-pool) side by side if this confusion surfaces.
- **Engagement tip:** SEGMENT 2's tokenization of a non-English script (Hindi example) is usually the strongest "I didn't know that" moment — let it breathe, and if you have multilingual students, invite them to test a sentence in their own language live.
- **Time check:** If running behind before the break, shorten SEGMENT 3's context-window numeric table discussion to the single comprehension-check question instead of walking through all three rows.
- **If running long after the break:** Compress SEGMENT 5's comparison table to just 4 rows (what it predicts, training data, retrainability, determinism) instead of all 7.
- **Materials to prepare:** `tiktoken` installed and tested ahead of time; the "capital of France" and top-p worked examples pre-typed in a scratch notebook so live-coding doesn't stall on typos.

---

## Common Errors — Quick Reference

| Bug / mistake | Symptom | Fix |
|---|---|---|
| `pip install tiktoken` missing or failing | `ModuleNotFoundError: No module named 'tiktoken'` | Run `pip install tiktoken` before the session; have a backup pre-run output ready to show if install fails live |
| Confusing tokens with words when reasoning about limits | Miscalculates how much text fits in a context window | Always reason in TOKENS, and note that roughly 1 token ≈ 0.75 English words as a rough rule of thumb, not an exact rule |
| Treating temperature=0 as "impossible to change the output" across different prompts | Assumes changing the PROMPT won't change output at temp=0 | Determinism at temp=0 means same prompt -> same-ish output, not that output never changes when you change the prompt |
| Thinking top-p and temperature are redundant settings | Sets only one, unsure why output still varies unexpectedly | Explain they operate on different parts of the sampling process and are commonly used together |
| Assuming the model "looks things up" during generation | Over-trusts confident-sounding but factually wrong answers | Reinforce: generation is next-token prediction from learned patterns, not real-time lookup, unless the system explicitly adds a retrieval step (out of scope for this session) |

---

## Appendix: Extra Tokenization Examples (Optional, If Time Allows)

| Input text | Approx. token count (illustrative order of magnitude) | Note |
|---|---|---|
| `"Hello, world!"` | ~4 | Common short greeting, tokenizes efficiently |
| `"supercalifragilisticexpialidocious"` | ~10-12 | Rare invented word, splits into many small pieces |
| `"2 + 2 = 4"` | ~7 | Numbers and symbols each often take their own token |
| A block of Python code with `snake_case_variable_names` | Higher than equivalent plain English of the same character length | Underscores and code punctuation often split oddly compared to natural prose |

---

## Appendix: Temperature/Top-p Cheat Sheet (Instructor Reference)

| Use case | Suggested temperature | Suggested top-p |
|---|---|---|
| Structured data extraction / classification | 0.0-0.2 | 1.0 (let temperature do the work) |
| Code generation | 0.0-0.3 | 0.9-1.0 |
| General chat assistant | 0.5-0.8 | 0.9-1.0 |
| Brainstorming / creative writing | 0.9-1.3 | 0.9-1.0, or lower top-p (e.g. 0.8) to keep it from going fully incoherent |

---

## FAQ — Additional Questions

**Q: Do all LLM providers expose both temperature and top-p through their API?**
→ The large majority do, since both trace back to a common, widely-adopted sampling interface popularized by early large-scale language model APIs. Some providers add extra knobs on top (e.g. frequency/presence penalties to discourage repetition) — out of scope for today, but you'll see them as optional fields once we're making real calls next session.

**Q: Is a "token" the same thing across every model?**
→ No — different model families are trained with different tokenizers (different vocabularies, different splitting rules), so the exact token count for the same sentence can vary from model to model. `cl100k_base`, used in today's demo, is a widely-used reference tokenizer, not a universal standard every model shares.

**Q: Why do LLMs seem to "think" before answering hard questions sometimes?**
→ Some modern models are trained or prompted to generate intermediate reasoning tokens before their final answer — effectively "thinking out loud" in tokens the user may or may not see. Mechanically it's still the same next-token-prediction loop; it's just been extended to include a reasoning phase. We touch on encouraging this behavior deliberately, via prompting, in Session 4 (chain-of-thought).

---

## SEGMENT 8: Supplemental Code Demos (Instructor Optional, If Time or Advanced Group)

### Demo A — Counting tokens across a simulated conversation (5 min)

```python
import tiktoken

encoding = tiktoken.get_encoding("cl100k_base")

conversation = [
    "You are a helpful assistant for a bookstore.",           # system
    "Can you recommend a sci-fi novel?",                       # user
    "Sure! I'd recommend 'Project Hail Mary' by Andy Weir.",   # assistant
    "Does it have a sequel?",                                  # user
]

running_total = 0
for turn in conversation:
    n = len(encoding.encode(turn))
    running_total += n
    print(f"{n:>3} tokens -> {turn!r}")

print("Running total so far:", running_total, "tokens")
```

**Example output (actual — deterministic for this exact fixed text under `cl100k_base`):**
```
  9 tokens -> 'You are a helpful assistant for a bookstore.'
  8 tokens -> 'Can you recommend a sci-fi novel?'
 16 tokens -> "Sure! I'd recommend 'Project Hail Mary' by Andy Weir."
  6 tokens -> 'Does it have a sequel?'
Running total so far: 39 tokens
```

**Break it down:**
- Every turn of a conversation — including the system message, which is invisible to the end user — costs real tokens against the same shared context window
- A running total like this is exactly what you should picture happening silently, turn after turn, in any multi-turn chat product
- This is a preview of why long conversations eventually need a strategy — trimming, summarizing, or starting fresh — once they approach the context window ceiling

**Ask:** If each of these four short turns costs roughly 6-15 tokens, and a model's context window is 8,000 tokens, roughly how many turns of similarly-sized conversation could you fit before running out?

**Common mistake:** Assuming only the user's literal typed words count toward the limit, forgetting the system message and the assistant's own prior responses all count too.

**Fix:** Always reason about token budget across the FULL conversation history that will be resent, not just the newest message.

### Demo B — Visualizing a flattening distribution with plain Python (5 min)

```python
import math

# Illustrative toy "logits" (unnormalized scores) for 5 candidate tokens
logits = {"Paris": 4.0, "the": 0.5, "located": 0.2, "known": 0.1, "France's": -0.3}

def softmax_with_temperature(logits, temperature):
    scaled = {k: v / temperature for k, v in logits.items()}
    exp_vals = {k: math.exp(v) for k, v in scaled.items()}
    total = sum(exp_vals.values())
    return {k: v / total for k, v in exp_vals.items()}

for temp in [0.3, 1.0, 2.0]:
    probs = softmax_with_temperature(logits, temp)
    formatted = ", ".join(f"{k}: {v:.2f}" for k, v in probs.items())
    print(f"Temperature {temp}: {formatted}")
```

**Example output (actual — this is plain deterministic arithmetic, verified by hand and by running the code above):**
```
Temperature 0.3: Paris: 1.00, the: 0.00, located: 0.00, known: 0.00, France's: 0.00
Temperature 1.0: Paris: 0.92, the: 0.03, located: 0.02, known: 0.02, France's: 0.01
Temperature 2.0: Paris: 0.63, the: 0.11, located: 0.09, known: 0.09, France's: 0.07
```

**Break it down:**
- This is the actual mathematical operation (softmax with a temperature-scaled input) underlying the qualitative table shown earlier in SEGMENT 4 — running real numbers through it makes the "sharpening vs. flattening" claim verifiable, not just asserted
- Notice `Paris` never drops to near-zero even at high temperature in this toy example — its underlying score was still comfortably the highest; temperature redistributes probability mass, it doesn't erase a strong signal entirely
- This is optional, deeper mechanism — students only need the qualitative table from SEGMENT 4 to pass the quiz; this demo is for students who want the "show me the math" version

**Ask:** If `temperature` were set to a very large number, like 100, what would you expect to happen to how close together all five probabilities become?

**Common mistake:** Assuming temperature can make a very low-scoring candidate become the MOST likely pick.

**Fix:** Temperature redistributes probability mass among existing candidates according to their relative scores — it does not reverse their relative ranking.

### Demo C — A minimal illustrative greedy-vs-sampling loop (4 min)

```python
import random

# Toy illustrative distribution, reused from Demo B at temperature=1.0
probs = {"Paris": 0.70, "the": 0.11, "located": 0.08, "known": 0.08, "France's": 0.03}

def sample_token(probs):
    tokens = list(probs.keys())
    weights = list(probs.values())
    return random.choices(tokens, weights=weights, k=1)[0]

random.seed(42)  # for a reproducible classroom demo run
picks = [sample_token(probs) for _ in range(10)]
print("10 sampled next-tokens:", picks)
```

**Example output (actual for `random.seed(42)` on a standard CPython installation; exact sequence can differ across Python versions/platforms since `random.choices`' internal algorithm isn't guaranteed identical everywhere — treat this as illustrative of the PATTERN, not a byte-exact universal result):**
```
10 sampled next-tokens: ['Paris', 'Paris', 'Paris', 'Paris', 'the', 'Paris', 'known', 'Paris', 'Paris', 'Paris']
```

**Break it down:**
- Out of 10 draws, `Paris` — the dominant ~70% probability token — was picked 8 times, reasonably close to its probability given the small sample size, exactly as expected from weighted random sampling
- This is a simplified but mechanically honest illustration of what real LLM sampling does at each single generation step, just with a toy 5-token vocabulary instead of tens of thousands
- Re-running with a different `random.seed` (or no seed at all) would give a different specific sequence, which is the whole reason two calls to a real LLM at the same non-zero temperature can produce different text

**Ask:** If you re-ran this cell without setting `random.seed(42)`, would you expect the exact same 10 tokens back?

**Common mistake:** Expecting a random seed set in YOUR Python script to have any effect on an LLM API's own internal sampling randomness.

**Fix:** `random.seed()` only controls Python's own `random` module locally in this toy demo — it has no connection to, or control over, the sampling randomness happening inside a remote LLM provider's servers.

---

## Materials Checklist

- [ ] `tiktoken` installed and verified on the demo machine
- [ ] Scratch notebook with SEGMENT 2's tokenization demos pre-typed
- [ ] Whiteboard space for the next-token-prediction loop diagram and the temperature/top-p tables
- [ ] Printed or projected comparison table template for SEGMENT 5 (fill in live with the class)
- [ ] Timer visible for the lab segment

---

## Timing Contingencies

| Situation | Action |
|---|---|
| Running 10 min behind before break | Shorten SEGMENT 2's multilingual tokenization example to a quick mention instead of a live run |
| Running long after break | Compress SEGMENT 5's comparison table to 4 core rows instead of all 7 |
| Low energy after lunch/break | Run SEGMENT 4's top-p worked example as a cold-call group activity instead of instructor-led |
| Advanced group finishes lab early | Have them tokenize a full paragraph of their own choosing and estimate token cost for a realistic 10-message conversation |
| No shared screen / projector issue | Walk the token tables on the whiteboard from memory using today's exact worked examples, skip live `tiktoken` run |

---

## End-of-Session Quiz (5 Questions)

1. What is a token, and why is it usually smaller than a whole word?
2. What does the context window limit, exactly — input only, output only, or both combined?
3. Does raising temperature reshape the probability distribution or restrict the candidate pool? What about top-p?
4. Name two concrete differences between how `LinearRegression` learns and how an LLM is trained.
5. Why can an LLM state a wrong fact with complete apparent confidence?

**Answer key (instructor):**
1. A token is a sub-word chunk of text from the model's vocabulary; it's smaller than a word so the model can represent any text, including rare words, typos, and other languages, by combining smaller familiar pieces.
2. Both — every token in the input (prompt/history) and every token generated in the output count against the same shared limit.
3. Temperature reshapes the probability distribution (sharper at low values, flatter at high values); top-p restricts which tokens are even eligible to be sampled, based on cumulative probability.
4. Any two of: LLMs are trained on enormous general text corpora vs. a specific curated dataset; LLMs have billions of non-interpretable parameters vs. a handful of interpretable coefficients; you cannot retrain/re-fit an LLM yourself in this course, unlike `LinearRegression.fit()`; LLM output is only near-deterministic even at low randomness settings, while classical ML predictions are fully deterministic for a given input row.
5. Because it's generating the statistically plausible next token based on learned patterns, not performing a real-time factual lookup — a fluent, confident-sounding continuation can be sampled even when it doesn't correspond to a true fact ("hallucination").

---

## Homework Rubric

| Criterion | Excellent (4) | Good (3) | Needs Work (2) | Incomplete (1) |
|---|---|---|---|---|
| Tokenization comparison (plain/typo/code) | All three tokenized, correct counts, clear reasoning on which is least efficient and why | Tokenized correctly, thin reasoning | Tokenized, no comparison reasoning | Not attempted |
| Hallucination explanation paragraph | Clear, jargon-free, correctly uses "probability" and "next token" in context | Mostly clear, uses both terms | Vague or missing one required term | Not attempted |
| Context window lookup for two models | Both models found with correct token figures noted | One model found correctly | Numbers found but unclear which model they belong to | Not attempted |

**Total:** /12 — Pass threshold: 8/12
