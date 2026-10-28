# Lecture Script: Generative AI — Prompt Engineering & Reasoning
> **Instructor Reference** — Module 3: GenAI & Agents | Academic Session 14.1 | Duration: 2 Hours

---

## Session Overview
**Goal:** By the end of this session, students can write role, zero-shot, few-shot and chain-of-thought prompts for a real routing and calculation task, score prompt versions on a fixed test set, and improve a prompt one change at a time using failure analysis.

**Student profile at this point:** They can call an LLM from Python with `ask_llm()` (13.2), know tokens and temperature (13.1), and from Module 2 they know classification, accuracy and "never grade your own homework." Likely wrong assumptions: "prompt engineering is about magic words," "if it worked once it works," and "longer prompts are always better." Boredom risk: low, but students will want to tweak prompts by feel — keep dragging them back to the test set.

**Key outcome:** Students should leave asking, before shipping any prompt: "What's my test set, what's the score, and which failures am I fixing with this change?"

> 🎯 **The one sentence this session must land:** *Prompt engineering isn't finding magic words — it's giving the model the context, examples and thinking space it needs, then proving each change helped on a test set you never trained on.*

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| Opening — "The Message in the Wrong Queue" | 8 min | 8 min |
| Concept Block 1: Role Prompting | 10 min | 18 min |
| Concept Block 2: Zero-Shot vs Few-Shot | 12 min | 30 min |
| Practical Block 1: Pick the Few-Shot Examples | 8 min | 38 min |
| Concept Block 3: Chain-of-Thought | 12 min | 50 min |
| Practical Block 2: The ₹600 Question by Hand | 8 min | 58 min |
| **BREAK** | 10 min | 68 min |
| Concept Block 4: Prompt Evaluation with Test Sets | 10 min | 78 min |
| Practical Block 3: Live Coding Demo (TA Code) | 14 min | 92 min |
| Concept Block 5: Iterative Refinement & Failure Analysis | 10 min | 102 min |
| Practical Block 4: Group the Failures | 10 min | 112 min |
| Summary & Bridge | 4 min | 116 min |
| Q&A & Doubt Solving | 4 min | 120 min |

---

## Opening — "The Message in the Wrong Queue" (8 min)

Open with this, verbatim-ish:

> "Saturday night, 10:15 pm. A delivery partner in Gachibowli types into our helpdesk: 'customer bahut gussa, gate pe dhamki de raha hai' — the customer is very angry and threatening me at the gate. Our router reads it and files it under 'other'. Low priority. Someone reads it on Monday."

Pause. Ask the room:

> "Whose fault is that — the model's, or the person who wrote the prompt and never tested it on a Hinglish safety message?"

(Let a couple of students answer.)

> "In Module 2 you'd never ship a churn model without a test set. Prompts deserve the same respect."

**Pivot line:** "Every message our helpdesk receives must first be routed — payout, incentive, app issue, safety or other. That's a classification problem, Module 2's classification box, but this time the 'model' is a prompt. Today you learn to write it like an engineer."

**Context for sessions ahead:** "Every prompt inside LangChain (15.1), every RAG prompt (17.1) and every agent's instructions (17.2) will be built and tested with today's techniques."

---

## Concept Block 1: Role Prompting (10 min)

> "Ask a passer-by 'is this noise from my bike engine serious?' — you get a guess. Ask a two-wheeler mechanic — you get careful questions. Same question, different expert."

Write on the board:

> Weak: "You are a helpful assistant."
> Useful: "You are a senior support lead at Swiggy who routes delivery-partner messages. Partners often write short Hinglish messages. Safety issues must never be missed."

> "The useful role adds who the model is, who it's talking to, how they write and what matters most — all things it can't guess."

### 🔴 The trap / highest-value moment
> "The internet is full of roles like 'You are the world's greatest AI genius with 200 IQ.' That adds nothing — the model can't become smarter on command. Write this down: *a good role adds facts the model can't guess, not flattery.*"

---

## Concept Block 2: Zero-Shot vs Few-Shot (12 min)

> "Training a new delivery partner: 'deliver politely' and off they go — or they ride along on three deliveries first and see what polite looks like. That's zero-shot versus few-shot."

Write on the board:

```
Classify into: payout, incentive, app_issue, safety, other. Only the label.
Message: "Weekly amount still showing pending" -> payout
Message: "Peak hour bonus missing for Sunday" -> incentive
Message: "Fell off the scooter near Ameerpet, need help with insurance" -> safety
Message: "Can I change my registered bank account?" ->
```

> "Zero-shot often says 'other' for the bank account — it isn't obviously about money arriving. But we decided bank details belong in `payout`. Examples teach the model your boundaries. The cost: they're resent on every call (13.1)."

### 🔴 The trap / highest-value moment
> "Most people pick their three easiest examples — useless, the model already gets those right. Write this down: *few-shot examples should sit on the boundaries — the cases the model gets wrong without them.*"

---

## Practical Block 1: Pick the Few-Shot Examples (8 min)

Show eight candidate messages and give pairs three minutes to pick the best three as few-shot examples: "Payout not credited", "Thank you", "Insurance claim for yesterday's fall", "App crashed", "Weekly amount showing pending", "Mera app login nahi ho raha", "Peak bonus missing" and "Customer was rude". The strong picks are the insurance claim (safety, not payout), the Hinglish login message (Hinglish is normal) and the peak bonus (incentive, not payout), because each teaches a boundary. "Customer was rude" is the trap: if the room can't agree on its label, it's a policy question for the ops team, not a prompt question — decide the rule first, then add an example.

---

## Concept Block 3: Chain-of-Thought (12 min)

> "In a maths exam, students who write every step make fewer mistakes — and when they're wrong, you can see where. LLMs are the same: they write one token at a time (13.1), so writing the steps first gives them room to work."

Write on the board:

```
Rules (illustrative): ₹30/order · +₹15 per peak-hour order · ₹400 if ≥60 orders · −₹100 per cancellation
Last week: 62 orders, 40 peak, 0 cancellations
This week: 62 orders, 20 peak, 3 cancellations
```

> "Ask directly 'why is this week lower?' and a common reply is 'probably fewer orders' — wrong, same orders. Ask it to work step by step and it writes base, peak, bonus and penalty for each week, and lands on the real causes."

### 🔴 The trap / highest-value moment
> "After seeing chain-of-thought work, people add 'think step by step' to every prompt. For routing 'payout' vs 'safety', that's extra tokens, cost and waiting for zero gain. Write this down: *chain-of-thought is for multi-step problems — calculations, conditions, comparisons — not simple lookups.*"

---

## Practical Block 2: The ₹600 Question by Hand (8 min)

Students compute both weeks' payouts by hand in four minutes, then reveal: base ₹1,860 both weeks; peak bonus ₹600 last week and ₹300 this week; target bonus ₹400 both weeks; deductions ₹0 and ₹300 — totals ₹2,860 and ₹2,260, a ₹600 drop, half from peak orders and half from cancellations. Stress the key move: because *you* now know the right answer, you can check the model in the TA demo instead of trusting it. If someone asks why we'd use an LLM when Python can calculate this, agree — Python should do the maths; the LLM's value is explaining it in simple Hindi, and in 17.2 an agent hands the maths to a Python tool.

---

## BREAK (10 min)

---

## Concept Block 4: Prompt Evaluation with Test Sets (10 min)

> "A cricket selector doesn't pick a batter after one good shot in the nets — that was Module 2's lesson. One good answer from a prompt proves nothing either."

Write on the board:

> For each prompt version: run all 10 test messages → count correct → accuracy

> "Now 'is v2 better than v1?' stops being an opinion and becomes a number."

### 🔴 The trap / highest-value moment
> "Two traps, both from Module 2. One: putting test messages into your few-shot examples — grading your own homework. Two: trusting the overall score — safety is maybe 1 in 10 messages, so a prompt can score 90% while missing every safety message. Write this down: *test messages never become examples — and always read which ones failed, not just the score.*"

---

## Practical Block 3: Live Coding Demo (TA Code) (14 min)

**Handoff line (must match TA code file's opening comment):** "Same 10 partner messages, three prompt versions — let's prove which prompt routes them best, then crack the ₹600 payout question with chain-of-thought."

Hand off to `ta-code - Session 14.1 - Prompt Engineering & Reasoning.py`, narrating each `# --- EXPLAIN ---` block aloud:

1. Show the test set — point out that none of these messages appear in the few-shot examples
2. Run v1 (zero-shot, no role) — read out the score and each failure
3. Run v2 (role + definitions) — what got fixed? Say honestly: "v2 changed three things at once — the role, the label definitions and 'reply with ONLY the label' — to save class time. In your own work, change them one at a time."
4. Run v3 (+ few-shot) — what got fixed?
5. Compute the true ₹600 in Python, then compare the direct answer with the chain-of-thought answer

💬 Expect a comment: "My run gave different failures from the TA's." Welcome it. Say: "Different models, different failures — that's exactly why you test your model on your test set instead of copying a prompt from the internet."

---

## Concept Block 5: Iterative Refinement & Failure Analysis (10 min)

> "A good cook doesn't throw away a salty dish. She tastes it, finds what's off, changes one thing and tastes again."

Write on the board:

> v1 → run test set → group failures → change ONE thing → run again → keep it only if better
> Format ("Label: payout") → "Reply with ONLY the label"
> Language (Hinglish misread) → mention Hinglish in the role
> Boundary (bank details, insurance) → define labels; few-shot on the boundary

### 🔴 The trap / highest-value moment
> "When frustrated, people rewrite the whole prompt at once. If the score goes up, which change helped? If it goes down, which one hurt? Write this down: *change one thing, re-run the same test set, keep it only if it helps.*"

---

## Practical Block 4: Group the Failures (10 min)

Show six failures from a fictional v1 run and give pairs five minutes to group them and propose one fix per group: "kal ka paisa nahi aaya" → `other`; "Rain bonus missing" → `payout`; "Payout late" → "The label is payout."; "Accident, am I covered?" → `payout`; "mera bonus kahan hai" → `other`; "App crash" → `App_Issue`. The groups are language (#1, #5 — mention Hinglish in the role), boundary (#2, #4 — sharper definitions and boundary examples) and format (#3, #6 — "reply with only the lowercase label", plus lowercasing in code as a safety net). Point out that #5 is both language and boundary: real failures overlap, so fix the biggest group first and re-run.

---

## Summary & Bridge (4 min)

| Concept | The one thing to remember |
|---|---|
| Role prompting | A good role adds context the model can't guess |
| Zero-shot vs few-shot | Few-shot examples should sit on your category boundaries |
| Chain-of-thought | Gives the model room to work — for multi-step problems only |
| Test sets | Score every prompt on the same set; never reuse test items as examples |
| Refinement & failure analysis | Group failures, change one thing, re-run, keep only what helps |

Close on the thesis line: "Prompt engineering isn't finding magic words — it's giving the model the context, examples and thinking space it needs, then proving each change helped on a test set you never trained on."

**Bridge to next session:** "Today we compared short labels. Soon we'll compare meaning — is 'kal ka paisa nahi aaya' close to 'payout not credited'? To measure closeness, computers turn text into arrows of numbers. Session 14.2 — Master Class: Vectors & Linear Algebra — builds that maths from scratch."

---

## Q&A & Doubt Solving (4 min)

**Q: How many few-shot examples should I use?**
→ Usually 3–8 — enough to cover your tricky boundaries. Let your test set tell you when adding more stops helping.

**Q: Does "think step by step" work for every model?**
→ It helps most models on multi-step problems, but some newer models already reason internally. Test it; if the score doesn't improve, drop it and save the tokens.

**Q: Is 10 test messages enough?**
→ It's a quick sanity check. Anything going to real partners needs 50–100 or more, with plenty of rare-but-critical categories like safety. Session 18.1 formalises evaluation.

**Q: Why temperature 0 for routing?**
→ The same message should always go to the same queue. That makes it consistent, not correct — the test set checks correctness.

**Q: Can I ask the LLM to write the prompt for me?**
→ Yes, as a first draft. Then run it on your test set — an LLM-written prompt isn't automatically a good one.

---

## Instructor Notes
- **Words not yet earned:** Pydantic and structured output (14.3), embeddings and vectors (14.2, 16.2), RAG (17.1), agents and tools (17.2), RAGAS (18.1).
- **Biggest risk in this session:** students tweaking prompts by vibe. Every time someone says "this one seems better," ask "what's the score?"
- **Board management:** keep the five labels, the ₹600 rules and the refinement loop visible from Concept Block 3 through Practical Block 4.
- **Common confusions, numbered:**
  1. Thinking flattering roles improve quality
  2. Picking easy few-shot examples instead of boundary cases
  3. Using chain-of-thought for simple tasks
  4. Reusing test messages as few-shot examples
  5. Trusting overall accuracy while missing rare, critical categories
  6. Changing many prompt parts at once
- **Cross-references:** Session 14.3 removes format failures with validated JSON; Session 15.1 turns these prompts into reusable templates; Session 17.2 hands calculations to tools; Session 18.1 scales test sets into RAGAS metrics.
- **Local/cultural context notes:** Hinglish partner messages and the Gachibowli, Ameerpet and Secunderabad references keep it grounded. The ₹600 puzzle threads directly from 13.2 — keep the same numbers all module.
