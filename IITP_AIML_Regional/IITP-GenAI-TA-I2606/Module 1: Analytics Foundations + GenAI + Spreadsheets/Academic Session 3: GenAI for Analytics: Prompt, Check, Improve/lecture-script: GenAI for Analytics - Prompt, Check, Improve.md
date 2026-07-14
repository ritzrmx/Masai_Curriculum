# Lecture Script: GenAI for Analytics — Prompt, Check, Improve
> **Instructor Reference** — Module 1: Analytics Foundations + GenAI + Spreadsheets | Academic Session 3 | Duration: 1.5 Hours | Instructor: Industry Mentor

---

## Session Overview

**Goal:** Students can write a four-ingredient prompt that returns a structured, usable output, place GenAI correctly inside the analytics workflow, and run three validation checks that catch a hallucination before it reaches a report.

**Student profile at this point:** They know the workflow and KPIs (S2) and how to summarise honestly (S1). Most have used ChatGPT casually. **Almost none have ever been burned by it.** That is the gap this session closes.

**Key outcome:** Students leave with a healthy, *specific* distrust — not "AI is bad" and not "AI is magic", but a precise sense of **which tasks it is safe for and which it is not.**

> 🎯 **The one sentence this session must land:** *GenAI is optimised to sound right, not to be right — so use it for language, and use your tools for numbers.*

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| Opening & Hook — The Confident Lie (live demo) | 8 min | 0:08 |
| **Concept 1:** What GenAI Actually Is | 10 min | 0:18 |
| **Concept 2:** Where GenAI Fits in the Workflow | 10 min | 0:28 |
| **Practical 1:** Safe / Careful / Never — sort the tasks | 8 min | 0:36 |
| **Concept 3:** The Four Ingredients of a Prompt | 12 min | 0:48 |
| **BREAK** | 5 min | 0:53 |
| **Practical 2:** Weak prompt → strong prompt (live, hands-on) | 14 min | 1:07 |
| **Concept 4:** Structured Outputs + The Three Checks | 12 min | 1:19 |
| **Practical 3:** Hallucination hunt | 8 min | 1:27 |
| Summary & Bridge to Session 4 | 3 min | 1:30 |

---

## Opening — The Confident Lie (8 min)

> ⚙️ **Setup:** Have ChatGPT (or any chat LLM) open and projected. This hook must be **live**. A screenshot does not produce the same effect — students need to watch it happen in real time.

**Do this in front of them.** Paste a small dataset into the chat:

```
Here is my sales data:

order_id, city, order_value
1, Chennai, 2400
2, Madurai, 1800
3, Chennai, 3200
4, Coimbatore, 950
5, Chennai, 1100

What is the average order value, and what percentage of revenue comes from Chennai?
```

**Before you press Enter, ask the room:**

> *"Hands up — who thinks it will get this right?"*

Most hands go up. Now run it.

**Then — and this is the important part — compute the truth on the board, by hand, with them:**

```
Total revenue  = 2400 + 1800 + 3200 + 950 + 1100 = 9,450
Average        = 9,450 / 5 = 1,890

Chennai        = 2400 + 3200 + 1100 = 6,700
Chennai share  = 6,700 / 9,450 = 70.9%
```

> ⚠️ **Instructor note — read this carefully.** With only 5 rows, the model will *often* get this right. **Do not panic if it does.** That outcome is *more* useful to you, and here is the line to say:

> *"It got it right. Good. Now tell me — **how do you know?** You know because I just did the arithmetic on the board and checked. You did not know it was right when the answer appeared. You **found out** it was right. **Those are completely different things, and the gap between them is this entire session.**"*
>
> *"And here's what should genuinely worry you: it looked exactly this confident either way. It would have produced that same fluent, well-formatted, comma-separated answer if it had been wrong. There was no warning light. **There is never a warning light.**"*

**Then escalate — the demo that reliably lands:**

> *"Now watch this."*

Paste this:

```
Based on this data, what was our customer satisfaction score,
and how many repeat customers did we have?
```

The dataset contains **no** satisfaction column and **no** customer ID. Watch what it does. It will usually either invent something plausible, or caveat heavily and then *still* offer an estimate.

> *"There is no satisfaction column. There is no customer ID. It cannot possibly know this. And yet look how willing it was to help."*

**The frame for the session:**

> *"GenAI will be the most useful assistant of your career and the most confident liar you will ever work with. **Those are the same sentence.** Today you learn to get everything from the first half while being immune to the second."*

---

## Concept Block 1: What GenAI Actually Is (10 min)

### The autocomplete analogy (3 min)

> *"You type 'I'm running a bit…' into WhatsApp and your phone suggests 'late'. Does your phone know you're late? Does it care? No. It has seen that word follow those words a few million times. **GenAI is that exact idea, scaled up enormously.**"*

### The one fact — write it on the board and leave it there all session

> # 🔑 **GenAI is optimised to produce text that LOOKS right.**
> # **It is NOT optimised to produce text that IS right.**

> *"Sit with that. Most of the time those two things overlap — which is exactly what makes it dangerous. If it were wrong all the time, you'd never trust it and you'd be safe. It's right often enough to earn your trust, and wrong often enough to destroy your credibility."*

### Every failure explained by that one fact (4 min)

| What it does | Why |
|---|---|
| Invents a statistic that sounds plausible | A number *fits* there, so it produces one |
| Cites a source that doesn't exist | Citations *look like that*, so it generates one |
| Gets an average wrong | **It is pattern-matching text, not doing arithmetic** |
| Almost never says "I don't know" | Uncertainty is rare in the text it learned from |

**Stop on row 3.** This is the one that saves them:

> *"When you ask it for an average, it is not opening a calculator. It is producing the text that most plausibly follows your question. Sometimes plausible text and the correct number are the same. Sometimes they are not. **And it cannot tell the difference — because from the inside, it's doing the identical thing either way.**"*

### Name the thing (3 min)

> **HALLUCINATION:** output that is fluent, confident, well-formatted — and false.

> 🔴 **The line to land:** *"A hallucination does not look like an error. **That is the entire problem.** When your calculator breaks, it shows an error. When Excel breaks, you get #REF!. When GenAI breaks, you get a beautiful, well-formatted table of wrong numbers, delivered with total confidence. **It fails silently, and it fails beautifully.**"*

---

## Concept Block 2: Where GenAI Fits in the Workflow (10 min)

**Callback to Session 2.** Put the four steps back on the board:

```
1. PROBLEM  →  2. DATA  →  3. ANALYSIS  →  4. INSIGHT
```

> *"GenAI is not equally good at all four. It is superb at two of them and dangerous at the other two. Knowing which is which is the difference between a productive analyst and an unemployed one."*

| Step | GenAI is… | Use it for | **Never** use it for |
|---|---|---|---|
| **1. Problem** | ✅ **Excellent** | Brainstorming sub-questions, suggesting KPIs, challenging your framing | Deciding what the business should care about |
| **2. Data** | ⚠️ **Careful** | Suggesting what to check, explaining an error message | **Generating data. Ever.** |
| **3. Analysis** | ⚠️ **Careful** | Writing a formula or query *for you to run* | **Computing the answer itself** |
| **4. Insight** | ✅ **Excellent** | Rewriting a verified finding clearly, drafting the summary | Deciding what the finding *is* |

### Why 1 and 4 are safe — the pattern (3 min)

> *"Look at what steps 1 and 4 have in common. Both are about **language**. Framing questions. Wording a finding. And in both, **you are the judge** — a bad sub-question is obvious to you, and you'd never send out a summary you hadn't read."*
>
> *"Now look at 2 and 3. Both are about **facts and numbers**. And in both, if it's wrong, **you might not notice.** That's the whole difference. Not 'creative vs boring' — **checkable-by-you vs not.**"*

### The rule — make them write it down (3 min)

> # ✅ **Use GenAI for LANGUAGE.**
> # **Use your TOOLS for NUMBERS.**

Make it concrete:

```
❌  "What's the average order value in this data?"
       → You just asked autocomplete to do arithmetic.

✅  "Write me the SQL to compute average order value by city."
       → You get the query. YOU run it. The DATABASE gives the number.
       → GenAI did language. The tool did the maths. Both did their job.
```

> *"This is not a limitation you're working around. This is you using each tool for what it's actually good at. **You'd never use a hammer to measure a wall.**"*

---

## Practical Block 1: Safe / Careful / Never (8 min)

**Format:** Rapid-fire, whole class. Put each task up. Students call out **SAFE ✅ / CAREFUL ⚠️ / NEVER 🛑**. Move fast.

| # | Task | Answer | The reasoning to voice |
|---|---|---|---|
| 1 | Draft 5 sub-questions about a drop in app installs | ✅ SAFE | Language. Step 1. You judge quality instantly. |
| 2 | Compute the average of these 500 rows | 🛑 NEVER | Arithmetic. Use a tool. |
| 3 | Write a SQL query to compute the average | ✅ SAFE | Language → you run it → the database does the maths |
| 4 | Rewrite my verified finding for the CEO | ✅ SAFE | Pure language. Step 4. And you'll read it. |
| 5 | Generate 100 rows of sample customer data | ⚠️ **CAREFUL** | Fine for *practice*. 🛑 **NEVER** as real data in a real analysis. |
| 6 | Explain what this error message means | ✅ SAFE | Language, and you can verify by trying the fix |
| 7 | Estimate our probable churn rate | 🛑 NEVER | It has no idea. It will produce a plausible-looking number anyway. |
| 8 | Suggest which columns might have data quality issues | ⚠️ CAREFUL | Useful *checklist* — but you must go verify each one |

> 💬 **#5 is the one that starts an argument. Let it.** Land it with: *"Synthetic data for practice? Excellent — we do it in this course. Synthetic data that quietly ends up in an analysis someone acts on? **That's fabrication, and the fact that a machine typed it doesn't change what it is.**"*

---

## Concept Block 3: The Four Ingredients of a Prompt (12 min)

### The intern analogy (2 min)

> *"Picture a new intern. Brilliant, fast, has read the entire internet — and has **never seen your company**. You would not walk up and say 'look into sales.' You'd tell them who to be, what you want, what they need to know, and what the answer should look like. **A prompt is an intern brief. Nothing more.**"*

### The four ingredients (4 min) — on the board, all session

```
1. ROLE      Who should it act as?      "You are a retail data analyst."
2. TASK      What exactly do you want?  "List 5 sub-questions to investigate a sales drop."
3. CONTEXT   What does it need to know? "Columns: city, product, order_value, date. Q3 2025."
4. FORMAT    What shape is the answer?  "A markdown table: Question | Data needed."
```

**Plus the fifth, which is really a superpower:**

```
5. CONSTRAINT   What must it NOT do?    "Use only the columns I listed. Do not invent data."
```

### Why FORMAT and CONSTRAINT matter most (4 min)

> **On FORMAT:** *"This is the ingredient beginners always drop, and it's the one that saves the most time. If you don't say what shape you want, you get **prose**. Prose has to be read, re-typed, and reformatted before it's any use. Ask for a table — you get a table. You'll get an hour of your life back every week from this one line."*

> **On CONSTRAINT:** *"This is the fence. 'Use only the columns I listed.' Without a fence, it will invent a `customer_age` column you don't have and build a beautiful analysis on top of it. **Remember the demo — it made up a satisfaction score out of thin air.** One sentence would have stopped it."*

### Show the difference (2 min)

```
❌  "Help me analyse sales."
    → Returns a generic essay about sales analysis. Useless.

✅  "You are a retail data analyst. Our Q3 revenue fell 12% vs Q2.
     Columns available: order_id, city, product_category, order_value, order_date.
     Task: list the 5 sub-questions I should investigate first.
     Format: markdown table — Sub-question | Why it matters | Columns needed.
     Constraint: use ONLY the columns listed above."
    → Returns a table you can start working from in 30 seconds.
```

> *"Same model. Same five seconds of compute. **Completely different value.** The difference wasn't the AI — it was you."*

---

## BREAK (5 min)

> *"Think about this while you're out: I said GenAI is dangerous for computing numbers. **But you're all going to use it to write SQL in Module 2 — and SQL computes numbers.** Is that a contradiction? Five minutes."*

*(Answer on return: **no** — GenAI writes the query, the database computes. GenAI never touches the number. The tool does. That's precisely why it's safe.)*

---

## Practical Block 2: Weak Prompt → Strong Prompt (14 min)

**Format:** Hands-on. Students on laptops/phones with any chat LLM. Pairs.

### Round 1 — feel the pain (4 min)

**Everyone types this exact weak prompt:**

```
Analyse my customer data and tell me what's wrong with it.
```

**Then ask the room:** *"How many of you got something you could actually use?"*

Nobody. Collect what they got — generic checklists, questions back, vague advice.

> *"Notice it didn't fail. It gave you a fluent, reasonable, **completely useless** answer. That's what a vague prompt buys you."*

### Round 2 — rebuild it together (5 min)

**Build the strong version live, on the board, asking the room for each ingredient:**

```
ROLE:        You are a data quality analyst.
TASK:        Review this customer dataset and identify data quality issues.
CONTEXT:     Columns: customer_id, name, email, city, signup_date, total_spend.
             ~5,000 rows, exported from our CRM. Indian customers.
FORMAT:      A markdown table: Column | Issue | Severity (High/Med/Low) | How to fix
CONSTRAINT:  Only reference the columns listed. If you're unsure about a column,
             say so explicitly rather than guessing.
```

**Everyone runs it. Compare in the room.**

> *"Same tool. Same question, in essence. Now look at what came back — it's a work plan. You could hand that to someone."*

### Round 3 — the pairs challenge (5 min)

**Each pair writes a full five-ingredient prompt for their own scenario:**

| Scenario |
|---|
| A student dropout problem at a university |
| A restaurant with falling weekend footfall |
| An app with rising uninstalls |

**Two pairs present. The class scores them against the five ingredients — is each one actually present?**

> 💬 **The most common miss you'll see:** they write ROLE, TASK and CONTEXT beautifully, and **forget FORMAT**. Call it out every time — it's the habit that sticks.

---

## Concept Block 4: Structured Outputs + The Three Checks (12 min)

### Structured outputs (4 min)

> **A structured output is a response in a fixed shape** — a table, a numbered list, a set of fields — that you can use *directly*, without rewriting it.

| Ask for this | Get this |
|---|---|
| *"Markdown table with columns: Metric, Formula, Target"* | A clean 3-column table |
| *"Exactly 5 bullets, max 15 words each"* | 5 tight bullets |
| *"Answer in one sentence. No preamble."* | One sentence — no *"Certainly! Here's…"* |

**The upgrade — hand it a template to fill in:**

```
Fill in this table. One row per issue. Add no commentary.

| Column name | Issue found | Severity | Suggested fix |
|-------------|-------------|----------|---------------|
|             |             |          |               |
```

> 🔑 **The non-obvious payoff — say this explicitly:** *"Structure isn't just tidy. **A table is checkable. An essay is not.** An essay hides its assumptions inside flowing sentences. But if the table has a 'Columns needed' field and it lists `customer_age` — a column you don't have — **you see the lie instantly.** Structure is a hallucination detector."*

### The three checks (5 min) — make them write these down

| # | Check | The question you ask | What it catches |
|---|---|---|---|
| **1** | **Source** | *"Is every number traceable to my actual data?"* | Invented figures |
| **2** | **Sanity** | *"Does this make sense in the real world?"* | A 340% conversion rate |
| **3** | **Recompute** | *"If I calculate it myself, do I get the same answer?"* | Arithmetic errors |

**The red flags — teach them to *feel* these:**

```
🚩  Suspiciously round numbers    ("exactly 25% of customers")
🚩  A column you don't have       (it filled a gap)
🚩  Zero hedging on a genuinely uncertain question
🚩  A citation you can't find
🚩  Numbers that don't add up to the stated total
```

> *"Real data is messy. **Real data is almost never exactly 25%.** When you see a suspiciously clean number, your neck should prickle."*

### The two habits (3 min)

> ### 🔍 **Habit 1: Ask it — "Which parts of this are you least sure about?"**
> *"It will often flag its own weakest claims. Free, five seconds, and it will save you at least one public embarrassment in your career."*

> ### 🛑 **Habit 2: You own every number you ship.**
> *"'The AI said so' has never been an acceptable answer in a meeting, and it never will be. GenAI is a tool, like a calculator. **A calculator that gives you a wrong answer is your problem, not the calculator's.** Your name is on the report. Not the model's."*

---

## Practical Block 3: Hallucination Hunt (8 min)

**Format:** Individual, 3 minutes. Then whole-class dissection.

**Put this on screen:**

```
YOUR DATASET has exactly these columns:
    order_id,  city,  order_value,  order_date

GENAI'S SUMMARY:
"Revenue grew 23% in Q3, driven primarily by the Bangalore region,
 which contributed exactly 40% of total sales. Customer satisfaction
 remained strong at 4.5/5, and repeat customers accounted for
 roughly two-thirds of orders. Source: internal Q3 analytics report."
```

> *"Find every red flag. There are at least five."*

**The answer key — walk through each:**

| 🚩 The claim | Why it's a red flag |
|---|---|
| *"Customer satisfaction 4.5/5"* | 🛑 **Pure invention.** There is no satisfaction column. |
| *"Repeat customers… two-thirds"* | 🛑 **Impossible.** There's no customer ID — you *cannot* identify a repeat customer. |
| *"exactly 40% of total sales"* | 🚩 Suspiciously round, and "exactly" is doing a lot of work |
| *"Source: internal Q3 analytics report"* | 🚩 **Hallucinated citation.** That document does not exist. |
| *"Bangalore region"* | 🚩 Is Bangalore even in your city column? **Verify it.** |
| *"Revenue grew 23%"* | ⚠️ **Possible** — but it's a computed number, so **recompute it yourself.** |

> 🎯 **The closing line for the block:** *"Notice how good it sounds. Read it out loud — it's better written than most human analyst summaries. **That fluency is exactly why it's dangerous.** If it had been badly written, you'd have questioned it. **It got past you because it was well-written, not despite it.**"*

---

## Summary & Bridge (3 min)

**What we covered:**

| Concept | The one thing to remember |
|---|---|
| **What GenAI is** | Optimised to *look* right, not to *be* right. It's autocomplete at scale. |
| **Hallucination** | Fluent, confident, well-formatted — and false. **It fails silently and beautifully.** |
| **Where it fits** | ✅ Problem & Insight (language). ⚠️ Data & Analysis (facts). |
| **The rule** | **Use GenAI for LANGUAGE. Use your tools for NUMBERS.** |
| **The prompt** | Role · Task · Context · Format · Constraint |
| **The checks** | Source · Sanity · Recompute — every time |
| **The law** | **You own every number you ship.** |

**Close on the hook:**

> *"At the start, I asked it for an average and most of you expected it to be right. Now you know the question was never 'will it be right?' — the question is **'how would I know?'** You now have the answer to that. That's the whole session."*

**Bridge to Session 4:**

> *"Three sessions, no tools. That ends now. **Next session you open a spreadsheet** — and you'll meet the reality of this job: duplicate rows, missing values, dates stored as text, 'Chennai' spelled four different ways. It is unglamorous, and analysts spend **most of their working lives here.** And here's the thread: everything you just learned about GenAI checking? You'll use it on real, filthy data — where the mistakes actually cost something."*

---

## Instructor Notes

- **The opening demo MUST be live.** A screenshot cannot produce the moment where a student watches a machine confidently invent a satisfaction score. **Test your prompts before class** so you know what the model does today.
- **Have a fallback if the model behaves too well.** If it refuses to hallucinate and caveats everything, use the script's line: *"It got it right — but how did you KNOW?"* That version of the lesson is arguably stronger. Do not fight the model; use whatever it gives you.
- **Tone is everything in this session.** You are not teaching "AI is bad" (they'll tune out) and not "AI is magic" (they'll get burned). You are teaching **calibrated, specific trust.** The tell that you've succeeded: students start asking *"is this a language task or a number task?"* unprompted.
- **The 'Use GenAI for language, tools for numbers' line is the load-bearing beam** of every remaining GenAI session in this course (S16 CTEs+GenAI, S25 Insight Writing, S27–S29 workflows). Make sure it lands.
- **Common confusion #1:** *"But it got the answer right when I tried it!"* → *"Yes. And how did you know?"* Always the same response.
- **Common confusion #2:** Students think a longer prompt is a better prompt. It isn't — a *complete* prompt is. Five ingredients, tightly written, beats three paragraphs of rambling.
- **Common confusion #3:** They will use GenAI to generate practice data and then forget it's fake. Draw the line hard in Practical 1 (#5).
- **No coding question for this session** — conceptual/GenAI-literacy session, per course design. The pre-read exercises plus the prompt-rebuild in Practical 2 are the assessment.
- **Tooling note:** Any chat LLM works. Free-tier ChatGPT, Claude, or Gemini are all fine. Make sure students can access *something* before class starts — a student watching over a neighbour's shoulder gets very little out of Practical 2.
