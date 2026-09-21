# Lecture Script: GenAI — GenAI for Analytics: Prompt, Check, Improve
> **Instructor Reference** — Module 1: Analytics Foundations + GenAI + Spreadsheets | Academic Session 3 | Duration: 1 Hour | Instructor: [Name/Placeholder]

---

## Session Overview
**Goal:** By the end, students can explain where GenAI fits into the analytics workflow, write a clear prompt using instruction + context + output format, generate structured outputs (tables/lists), and validate a GenAI output before trusting it.

**Student profile at this point:** Students now know the four-step analytics workflow and metrics vs KPIs from Session 2, and mean/median/outliers from Session 1. Most have used ChatGPT casually but never systematically — assume enthusiasm but sloppy prompting habits and an instinct to trust confident-sounding answers. Boredom risk is low (GenAI is inherently engaging to this cohort) — the real risk is overconfidence in GenAI's outputs, which this session must directly correct.

**Key outcome:** Every student should leave with the reflex: never forward a GenAI output without checking it against real numbers or logic first — exactly the same discipline as Session 1's "is that the mean, and is there an outlier?"

> 🎯 **The one sentence this session must land:** *GenAI is a fast intern, not a fact-checker — the prompt gets you a draft, and it's your job to verify it before it's a deliverable.*

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| Opening — "The Confident Wrong Answer" | 6 min | 6 min |
| Concept Block 1: What Is GenAI in Analytics? + Practical | 11 min | 17 min |
| Concept Block 2: Writing Basic Prompts + Practical | 11 min | 28 min |
| **BREAK** | 3 min | 31 min |
| Concept Block 3: Generating Structured Outputs + Practical | 12 min | 43 min |
| Concept Block 4: Checking and Validating Outputs + Practical | 11 min | 54 min |
| Summary & Bridge | 3 min | 57 min |
| Q&A & Doubt Solving | 3 min | 60 min |

---

## Opening — "The Confident Wrong Answer" (6 min)

Write this on the board, nothing else:

> **"GenAI summary: 'Average daily sales were ₹25,000, showing consistent strong performance.'"**

> "This is a real GenAI response to a real dataset — the Kanpur branch numbers from Session 1: 15, 15, 16, 17, 18, 19, 30, in thousands of rupees. Quick math check — someone tell me the actual mean."

[Let a student compute: ≈ ₹18,600 — clearly lower, and "consistent strong performance" doesn't match six days barely above 15-19.]

> "So GenAI got the number wrong, and it got the story wrong — and it said it with total confidence, in a clean, professional-sounding sentence. If you copy-pasted this straight into a report to your manager, what happens?"

[Pause for the room to feel the risk — credibility damage, bad decisions made on a wrong number.]

**Pivot line:**
> "This isn't a reason to avoid GenAI — it's incredibly useful, and you'll use it constantly for the rest of this course. Today is about using it *well*: writing prompts that get you better answers, and — just as important as Session 1's outlier check — knowing exactly how to catch it when it's confidently wrong."

---

## Concept Block 1: What Is GenAI in Analytics? (11 min)

> "Think of GenAI as a new intern on day one — incredibly fast, drafts things in seconds, but sometimes wrong with total confidence. What's your job when you manage an intern like that?"

[Draw out: supervise, check the work, don't just forward it blindly.]

Write the workflow-mapping table on the board (from Session 2's four steps):

| Workflow step | How GenAI helps |
|---|---|
| Problem | Draft/sharpen a fuzzy problem statement |
| Data | Suggest relevant fields (can't fetch real data itself) |
| Analysis | Draft formulas, organize findings into tables |
| Insight | Draft a first-version report — for you to check |

> "Notice the word 'draft' repeats in every row. That's deliberate."

### 🔴 The trap / highest-value moment
> "Someone tell me — in the opening example, why did GenAI get the average so wrong?"

[Draw out: it likely wasn't given the real numbers at all, or was asked something vague, so it produced a plausible-sounding guess.]

**One-line rule to write down:**
> *"GenAI only knows what you tell it — anything else is a guess dressed up as a fact."*

## Practical Block 1: Map It to the Workflow (part of the 11 min)

> "In pairs, 60 seconds — for each of these three tasks, say which workflow step GenAI is helping with: (1) 'Suggest three sub-questions for why revenue is flat,' (2) 'Organize this list of complaint types into a table,' (3) 'Draft a one-paragraph summary of this month's KPI performance.'"

**Answer key (with reasoning aloud):**
1. Problem — helping sharpen/break down the initial question.
2. Analysis — organizing raw information into a usable structure.
3. Insight — drafting the final communicated conclusion (still needs checking).

---

## Concept Block 2: Writing Basic Prompts (11 min)

> "Let's fix how we talk to GenAI. Compare these two requests at the Zappy Mart food counter: 'make me something' versus 'one plate veg fried rice, medium spice, no onions.' Which gets you what you actually wanted?"

[Let students say the second, obviously.]

Write the three-part prompting pattern on the board:

**Instruction + Context + Output Format**

> "Let's build a real prompt live. Instruction — what do we want? 'Summarize this week's sales data.' Context — what does GenAI actually need to know? 'For Udaipur branch, 7 days of daily sales.' Output format — how should it look? 'As 3 bullet points, under 50 words, highlighting the highest and lowest day.'"

Write the weak-vs-strong comparison table on the board (from the pre-read) and read both aloud.

### 🔴 The trap / highest-value moment
> "What's the single most commonly forgotten part of these three?"

[Draw out: output format — people specify what they want but not how they want it shaped.]

**One-line rule:**
> *"If you don't say how you want the answer shaped, don't be surprised when it isn't."*

## Practical Block 2: Rewrite the Weak Prompt (part of the 11 min)

> "In pairs, 90 seconds — rewrite this weak prompt using instruction + context + output format: 'Tell me about our customer complaints.'"

**Answer key (sample, with reasoning aloud):**
> "Summarize the following month's customer complaint log for Zappy Mart's Lucknow branch. Group by complaint category, and present as a table with columns: Category, Count, % of Total. Keep it to the top 5 categories only." — reasoning: instruction (summarize + categorize), context (Lucknow branch, one month), output format (table, specific columns, top 5 only).

💬 Expect pushback: "Isn't this a lot of effort just to ask a question?" Welcome it. Say: *"A 20-second better prompt saves you 5 minutes of re-prompting and cleaning up a messy answer — it's a net time saver, not extra work."*

---

## ☕ BREAK (3 min)

---

## Concept Block 3: Generating Structured Outputs (12 min)

> "Quick recall from Session 1 — why did we like pivot tables over scrolling through raw rows of data?"

[Draw out: easier to scan, compare, and act on.]

> "Same logic applies to GenAI. If you don't ask for structure, you get a paragraph. If you do, you get something instantly usable."

Write the worked example prompt and its numbered-list output on the board (from the pre-read: "List 3 possible reasons Udaipur sales dropped").

> "Notice how much faster you could hand this numbered list to a teammate compared to the same content buried in a paragraph."

### 🔴 The trap / highest-value moment
> "Here's the dangerous part. Does a neatly formatted table being *neat* tell you anything about whether it's *correct*?"

[Let the "no" land clearly — this connects directly back to the opening hook.]

**One-line rule:**
> *"Structure makes an output easier to check — it does not make it automatically correct."*

## Practical Block 3: Request the Structure (part of the 12 min)

> "In pairs, 60 seconds — rewrite this prompt to force a structured output: 'What are some ways to improve Zappy Mart's loyalty program?'"

**Answer key (sample, with reasoning aloud):**
> "List 5 specific ways to improve Zappy Mart's loyalty program, as a numbered list, one line each, ordered from easiest to hardest to implement." — reasoning: added a specific count (5), format (numbered list), and even a sort order, turning a vague open question into an actionable, scannable output.

---

## Concept Block 4: Checking and Validating Outputs (11 min)

> "Back to our opening example — GenAI claimed ₹25,000 average, 'consistent strong performance,' on data that actually averaged ₹18,600 with one clear outlier. How would you have caught this before trusting it?"

Write the four-part validation checklist on the board:

**Numbers · Logic · Completeness · Source**

> "Numbers — does any quoted figure match your real data? Logic — does the reasoning actually hold up, or does it just sound fluent? Completeness — did it skip something you specifically asked for? Source — is it stating something as fact it couldn't actually know?"

Walk through the opening example against all four:
> "Numbers — fails, ₹25,000 doesn't match. Logic — fails, 'consistent strong performance' contradicts six days of much lower sales. That's two red flags in one sentence."

### 🔴 The trap / highest-value moment
> "Someone tell me why this matters even more than Session 1's outlier check."

[Draw out: at least with your own calculation, you know your own math. A GenAI output can be wrong and still sound completely authoritative — the confidence of the language is not a signal of correctness.]

**One-line rule:**
> *"Treat every GenAI output like a first draft from an unsupervised intern — confident-sounding is not the same as correct."*

## Practical Block 4: Validate and Improve (part of the 11 min)

> "In pairs, 90 seconds — using the four-part checklist, write one sentence flagging what's wrong with this GenAI output, and one improved re-prompt to fix it: 'Revenue increased 22% this quarter, driven primarily by the Lucknow branch' — when you know Lucknow data was never given to it."

**Answer key (with reasoning aloud):**
> Flag: fails the **Source** check — it's stating a specific branch driver as fact when that data was never provided, meaning it's likely invented. Improved re-prompt: "Here is our actual quarterly revenue by branch: [insert real data]. Summarize which branch(es) drove the increase, based only on the numbers provided — do not assume or infer branches not listed."

💬 Expect a question: "So should we just not trust GenAI at all?" Welcome it. Say: *"No — trust it as a fast drafting tool, and verify it like you would any other draft before it goes out under your name. That's the whole 'prompt, check, improve' loop."*

---

## Summary & Bridge (3 min)

| Concept | The one thing to remember |
|---|---|
| GenAI in analytics | Useful for drafting each workflow step — never a substitute for your judgment |
| Writing prompts | Instruction + Context + Output Format — vague prompts get vague results |
| Structured outputs | Ask explicitly for tables/lists — but structure ≠ correctness |
| Validating outputs | Check numbers, logic, completeness, and source before trusting or sharing |

> "Remember the opening's confidently wrong ₹25,000 average. That single mistake — trusted without checking — is exactly the kind of error this session trains you to catch every time."

**Bridge:** "Next session moves from GenAI back to hands-on spreadsheet work — **Clean Up the Data** — where you'll load a real, messy dataset into Excel/Sheets. And notice the connection: even a perfectly validated GenAI summary is only as good as the data underneath it, which is exactly why cleaning data comes next."

---

## Q&A & Doubt Solving (3 min)

**Q: Is it okay to just paste our raw data into GenAI and ask it to analyze everything?**
→ It can work for small datasets, but always still validate the output against a quick manual spot-check (like a mean or count you calculate yourself) — never skip the check step just because you gave it real data.

**Q: What if GenAI gives two different answers when I ask the same question twice?**
→ This is expected and normal — GenAI outputs can vary between attempts. Treat any single response as one draft, not a guaranteed answer, which is exactly why validation matters every time, not just once.

**Q: How specific should context be — do we need to paste the entire dataset every time?**
→ For small analytics tasks, yes, include the actual numbers where possible. For larger datasets, you'll learn in Module 4 (Python + APIs) how to feed data programmatically — for now, focus on being specific with whatever you can reasonably include.

**Q: Can GenAI itself tell us if its answer is wrong?**
→ Not reliably on its own — it can sound equally confident whether right or wrong. The validation checklist is something you apply from the outside, using your own domain knowledge and real data.

---

## Instructor Notes
- **Words not yet earned — avoid:** hallucination (as a technical term — describe the behavior instead, e.g. "confidently making something up"), temperature, tokens, model parameters, fine-tuning. These arrive naturally later, if at all, and add confusion here.
- **Biggest risk this session:** overconfidence — students already like using ChatGPT casually and may resist the idea that it needs checking. Counter directly and repeatedly with the opening's concrete wrong-number example; return to it at least twice more (Concept Blocks 3 and 4).
- **Board management:** keep the opening's wrong GenAI quote ("₹25,000... consistent strong performance") visible the entire session — it's the through-line example tying every concept block back to a single, memorable failure case.
- **Common confusions (numbered):**
  1. Assuming GenAI "knows" real business data unless it's explicitly given.
  2. Treating a neatly formatted table as automatically accurate.
  3. Giving an instruction without specifying the desired output format.
  4. Believing a single GenAI response is a fixed, guaranteed-correct answer.
- **Cross-references forward:** Session 7.2 (CTEs and GenAI for SQL — same validation discipline applied to generated queries), Session 11.2 (Insight Writing with GenAI), Session 12.2 (Summarise, Compare and Report with GenAI), Session 13.1 (Multi-Step GenAI Workflows), Session 15.1 (Python + OpenAI API integration).
- **Local/cultural context notes:** The food-counter ordering analogy and the Kanpur branch dataset (already familiar from Session 1) both landed well — reusing the same dataset across sessions also reinforces that GenAI's wrong answer was checkable specifically because students already knew the real numbers.
