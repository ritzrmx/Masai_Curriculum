# Lecture Script: Generative AI — LLM Fundamentals: How Language Models Work
> **Instructor Reference** — Module 3: GenAI & Agents | Academic Session 13.1 | Duration: 2 Hours

---

## Session Overview
**Goal:** By the end of this session, students can explain how an LLM generates text one token at a time, estimate token counts and costs for a real feature, predict how temperature and top-p change an output, and decide when an LLM is the wrong tool compared with their Module 2 models.

**Student profile at this point:** Just finished Module 2 — they can frame a problem, split data, train and evaluate classical models, and they know the Swiggy churn story well. Most have used ChatGPT casually but have no mental model of what happens inside. Likely wrong assumptions: "the AI looks things up," "temperature 0 means correct," and "LLMs make classical ML obsolete." Boredom risk: moderate — there's no real API call yet, so the human next-token game and the TA demo must carry the energy.

**Key outcome:** Students should leave asking, before any AI feature: "How many tokens is this, does it fit in the window, what temperature does it need, and would a Module 2 model do it better?"

> 🎯 **The one sentence this session must land:** *An LLM doesn't know or look up answers — it predicts the next token, over and over, and every setting you'll touch just shapes that one repeated guess.*

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| Opening — "The Midnight Payout Question" | 8 min | 8 min |
| Concept Block 1: What an LLM Really Does | 12 min | 20 min |
| Practical Block 1: Be the LLM | 8 min | 28 min |
| Concept Block 2: Tokens | 10 min | 38 min |
| Concept Block 3: Context Windows | 10 min | 48 min |
| **BREAK** | 10 min | 58 min |
| Concept Block 4: Temperature & Top-p | 12 min | 70 min |
| Practical Block 2: Live Coding Demo (TA Code) | 12 min | 82 min |
| Concept Block 5: Cost & Latency | 10 min | 92 min |
| Concept Block 6: LLM vs Traditional ML | 10 min | 102 min |
| Practical Block 3: Right Tool for the Job | 10 min | 112 min |
| Summary & Bridge | 4 min | 116 min |
| Q&A & Doubt Solving | 4 min | 120 min |

---

## Opening — "The Midnight Payout Question" (8 min)

Open with this, verbatim-ish:

> "Remember our Swiggy churn problem from Module 2? We figured out *who* might leave. Here's *why* many of them leave. It's 11:40 pm. A delivery partner finishes his last order in Kukatpally, opens the app, and sees his weekly payout is ₹600 less than last week. There's no one to ask until Monday. By Monday, he's signed up with a competitor. For the next fourteen sessions, we're building the AI helpdesk that answers him at 11:40 pm."

Pause. Ask the room:

> "Raise your hand if you think ChatGPT looks up the answer somewhere when you ask it a question."

(Many hands will go up — that's the point.)

> "It doesn't. It's guessing — extremely well-informed guessing, one small piece at a time. Once you get that, everything else today falls into place."

**Pivot line:** "In Module 2, you trained a model on your table to predict one label. Today we meet a model someone else trained on almost the whole internet, which predicts something much smaller — just the next piece of text — again and again."

**Context for sessions ahead:** "Every single thing we build in Module 3 — API calls, prompts, LangChain, RAG, agents — is a way of steering that one repeated guess."

---

## Concept Block 1: What an LLM Really Does (12 min)

> "Let's play a quick one. I say: 'And that's gone all the way for...' — the whole room?" (They'll shout "SIX!") "Did anyone look that up? No. You've heard so much commentary that you knew what usually comes next. That is exactly what an LLM does — for every kind of text, at enormous scale."

Write on the board:

> "Your payout will be" → score every possible next piece → pick "credited" → append → repeat

> "Inside, each piece becomes numbers, and many layers work out how every piece relates to every other one. That design is called a **transformer** — the 'T' in GPT. That's all the architecture you need today: score, pick, append, repeat."

### 🔴 The trap / highest-value moment
> "Because it generates instead of looking up, an LLM can produce a sentence that sounds perfect and is completely false — **hallucination**. If our helpdesk says 'payouts arrive every Tuesday' when the rule is Friday, that's not a bug in our code; it's the model producing likely-sounding text. Write this down: *an LLM predicts plausible text, not true text.* Sessions 17.1 and 18.1 are about closing that gap. And tell the room once, clearly: the helpdesk's policies and numbers in this module are invented for teaching, not Swiggy's real rules."

---

## Practical Block 1: Be the LLM (8 min)

Put "Dear partner, your weekly payout..." on screen and go around the room, each student adding exactly one word — whatever feels most likely. Run it a second time, telling students to pick the second- or third-most-likely word instead. Round 1 usually lands on something safe like "...has been credited to your bank account"; Round 2 drifts somewhere creative. Name the difference — "that's low versus high temperature; we'll put numbers on it after the break" — and point out that nobody looked up a single fact, yet Round 1 sounded authoritative.

---

## Concept Block 2: Tokens (10 min)

> "Does the model read letters? Words? Neither. Think of a Swiggy bill — you're charged per item: one biryani, one raita, one Coke. LLMs read, write and charge per **token**."

Write on the board:

> 1 token ≈ ¾ of an English word → 100 words ≈ 130 tokens
> "Why is my weekly payout less than last week?" = 9 words ≈ 12 tokens
> "Hyderabad" → "Hy" + "der" + "abad" (splits differ by model)

### 🔴 The trap / highest-value moment
> "Here's what catches people building for India: the same sentence in Hindi or Telugu can take two to three times more tokens than English, because the model saw far less of that text while learning. Our partners write in many languages. Write this down: *tokens, not words, decide cost — and Indian languages usually cost more tokens.*"

---

## Concept Block 3: Context Windows (10 min)

> "Picture a support agent at a small desk. She can only keep so many papers on it. When the desk is full, the oldest ones slide off and she can't see them any more. That desk is the **context window** — the maximum tokens a model handles in one go, input plus reply."

Write on the board:

> Small ≈ 8,000 tokens (a few pages) · Medium ≈ 128,000 (a short book) · Large ≈ 1,000,000 (several books)

> "Imagine the full partner handbook is about 300 pages — roughly 150,000 tokens. Can we paste it into every question?" (Let them answer.) "On a 128k model it doesn't fit. On a bigger one it fits, but we'd pay for 150,000 tokens on every 'where is my payout' message. Session 17.1 fixes this properly."

### 🔴 The trap / highest-value moment
> "Many people think the context window is the model's memory. It isn't. When the chat ends, the model forgets everything; when an app 'remembers' earlier messages, it's quietly re-sending them. Write this down: *the context window is a desk, not a memory.*"

---

## BREAK (10 min)

---

## Concept Block 4: Temperature & Top-p (12 min)

> "Two Hyderabad auto drivers going to the airport: the cautious one always takes the main road; the adventurous one sometimes tries a shortcut. Same city knowledge, different appetite for risk."

Write on the board — next token after "Your payout will be credited by ___":

| Next token | Temp 0.2 | Temp 1.0 | Temp 1.5 |
|---|---|---|---|
| Friday | 98% | 55% | 44% |
| tomorrow | 2% | 25% | 26% |
| Monday | ~0% | 12% | 16% |
| tonight | ~0% | 6% | 10% |
| never | ~0% | 2% | 5% |

> "**Temperature** reshapes these chances: low squeezes everything onto the top choice, high flattens them. **Top-p** cuts the list: with top-p 0.9 at temperature 1.0, Friday + tomorrow + Monday = 92%, so only those three stay. Policy answers: temperature 0–0.3. Five Diwali push-notification lines: 0.8–1.0."

### 🔴 The trap / highest-value moment
> "Temperature 0 does not make the model correct. It makes it (almost always) consistent. If its top guess for the payout day is 'Tuesday', temperature 0 says 'Tuesday' every time, with total confidence. Write this down: *temperature controls randomness, not truth.*"

---

## Practical Block 2: Live Coding Demo (TA Code) (12 min)

**Handoff line (must match TA code file's opening comment):** "Let's look inside the engine of our Swiggy partner helpdesk — tokens, temperature, top-p and the bill, in code."

Hand off to `ta-code - Session 13.1 - LLM Fundamentals - How Language Models Work.py`, narrating each `# --- EXPLAIN ---` block aloud:

1. Count tokens for the partner's question with `tiktoken` — compare the word count with the token count
2. Compare English, Hindi, Telugu and an amount string — point out the Indian-language token jump
3. Apply temperatures 0.2, 1.0 and 1.5 to the same five next-token options — read out the probabilities and the 10 sampled answers each time
4. Apply top-p 0.9 — show "tonight" and "never" dropping to 0%
5. Compute the cost of a lean prompt vs pasting the whole handbook, then the context-window check — let the "over ₹1 lakh a day" number land in silence

💬 Expect a question: "Is this how the real model does it?" Welcome it. Say: "The temperature and top-p maths is exactly what providers do. What we faked is the scoring — a real LLM produces those starting chances with billions of numbers. Calling a real one is next session."

---

## Concept Block 5: Cost & Latency (10 min)

> "An auto ride costs per kilometre and takes time per kilometre. An LLM call costs per token and takes time per token."

Write on the board:

> cost per call = (input tokens × input price) + (output tokens × output price)
> Illustrative: ₹15 per million in, ₹60 per million out
> 500 in + 200 out ≈ 2 paise → ~₹975/day at 50,000 questions
> Pasting the handbook every time → ~₹1.1 lakh/day

> "Output tokens usually cost three to five times more, because writing is the slow part — the model produces output one token at a time. That's also why **latency** grows mostly with how much it writes."

### 🔴 The trap / highest-value moment
> "People see '2 paise' and relax. Always multiply by volume. And the cheapest lever is often shorter answers — 'reply in under 60 words' cuts both cost and waiting time. Write this down: *estimate cost per call × calls per day — before you build.*"

---

## Concept Block 6: LLM vs Traditional ML (10 min)

> "A Module 2 churn model is a specialist doctor trained on your clinic's patients, for one question. An LLM is a well-read general physician — it's read a huge library and can discuss almost anything, but it's never seen your clinic's files."

Write on the board:

> Classical ML: you train it on your table → one label or number → same input, same output → train/test split
> LLM: a provider trained it → you write instructions → free text → can vary → prompt test sets (14.1), RAGAS (18.1)

### 🔴 The trap / highest-value moment
> "'LLMs are smarter, so use them for everything.' For 'will this partner churn?' on a clean table, your Module 2 classifier is cheaper, instant, consistent and easy to evaluate. Write this down: *frame the problem first — the box still comes before the code.*"

---

## Practical Block 3: Right Tool for the Job (10 min)

In pairs, students decide "classical ML", "LLM" or "both" for five tasks, with one reason each: predict next month's churners from activity data (classical ML); explain incentive rules in simple Hindi (LLM); tag 10,000 complaints as payout, app, safety or other (debatable — an LLM if there are no labels, a classifier if thousands of labelled examples already exist); forecast order volume per zone for IPL final week (classical ML, regression); flag likely churners and write each a retention message (both). Cold-call pairs, and let the complaint-tagging argument run — it depends on the data you have, exactly like supervised vs unsupervised in Module 2.

---

## Summary & Bridge (4 min)

| Concept | The one thing to remember |
|---|---|
| What an LLM does | Predicts the next token, appends, repeats — it generates, it doesn't look up |
| Tokens | Cost and limits are counted in tokens; Indian languages usually use more |
| Context window | Input + output must fit; it's a desk, not a memory |
| Temperature & top-p | Randomness dials — neither controls truth |
| Cost & latency | (in × price) + (out × price), times daily volume |
| LLM vs classical ML | Different tools — frame the problem first |

Close on the thesis line: "An LLM doesn't know or look up answers — it predicts the next token, over and over, and every setting you'll touch just shapes that one repeated guess."

**Bridge to next session:** "Today we simulated the engine with NumPy. Session 13.2 — Calling LLMs with APIs — is where you get an API key, keep it safe, and send our partner's payout question to a real LLM from your own Python code."

---

## Q&A & Doubt Solving (4 min)

**Q: If it only predicts the next word, how can it write code or solve maths?**
→ Predicting the next token well across huge amounts of text forces the model to pick up patterns of reasoning, code and maths. It's still prediction underneath — which is why it can also make confident arithmetic mistakes.

**Q: Does the model learn from my chats?**
→ Not during the conversation — its learned numbers are fixed. Whether a provider uses your data for future training depends on its policy and your settings; we cover privacy in Session 18.1.

**Q: What temperature should our helpdesk use?**
→ Low, around 0–0.3, because policy answers should be consistent. Low temperature removes randomness, not mistakes.

**Q: Why are output tokens more expensive than input tokens?**
→ The model reads your input in one fast pass but must generate output one token at a time. Writing is the slow, compute-heavy part.

**Q: Is a bigger context window always better?**
→ No. It costs more, runs slower, and models can miss a detail buried in a huge input. Sending only the relevant pages (RAG, Session 17.1) usually wins.

---

## Instructor Notes
- **Words not yet earned:** API key (13.2), few-shot and chain-of-thought (14.1), embeddings (16.2), RAG (name it only as "coming in 17.1"), agents (17.2).
- **Biggest risk in this session:** impatience — there's no real API call today. Counter it with the "SIX!" opener, the Be-the-LLM game and the 11:40 pm partner story.
- **Board management:** keep the "score → pick → append → repeat" loop and the temperature table visible from Concept Block 4 through the TA demo.
- **Common confusions, numbered:**
  1. Thinking the LLM looks up answers instead of generating them
  2. Believing temperature 0 means correct
  3. Treating the context window as long-term memory
  4. Counting words instead of tokens when estimating cost
  5. Assuming LLMs replace classical ML for every task
- **Cross-references:** Session 13.2 sets temperature in a real API call; Session 14.1 brings back test sets; Session 16.2 explains the "text becomes numbers" step; Session 17.1 solves the handbook-doesn't-fit problem; Session 18.1 tackles hallucination head-on.
- **Local/cultural context notes:** the Swiggy delivery-partner helpdesk is the running scenario for all of Module 3, continuing Module 2's churn story. Say once, clearly, that its policies and numbers are invented for teaching. The cricket "SIX!" opener and the Hyderabad auto-driver analogy land well, and Indian-language token counts make the cost discussion feel real.
