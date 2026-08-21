# Lecture Script: Spreadsheets — Formulas for Analysis
> **Instructor Reference** — Module 1: Analytics Foundations + GenAI + Spreadsheets | Academic Session 6 | Duration: 1 Hour | Instructor: [Name/Placeholder]

---

## Session Overview
**Goal:** By the end, students can apply SUM/AVERAGE/COUNT correctly, drag formulas across rows/columns using relative and absolute references, build new calculated columns, and combine formulas into simple descriptive analysis with real comparisons.

**Student profile at this point:** Students have validated, trustworthy data from Session 5 — this is the payoff session where that work finally gets used. Assume basic familiarity with typing a formula, but not with the fill handle, `$` absolute references, or building calculated columns from scratch. Low boredom risk — this is hands-on and immediately rewarding — but watch for the `$` reference concept causing quiet confusion.

**Key outcome:** Every student should leave able to build a total, an average, and a new derived column on a fresh dataset without hesitation, and instinctively compare numbers rather than report them alone.

> 🎯 **The one sentence this session must land:** *A formula written once and dragged correctly is worth fifty formulas typed by hand — but only if you know when to lock a reference and when to let it move.*

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| Opening — "The Broken Drag" | 6 min | 6 min |
| Concept Block 1: SUM, AVERAGE, COUNT + Practical | 10 min | 16 min |
| Concept Block 2: Applying Formulas Across Rows/Columns + Practical | 12 min | 28 min |
| **BREAK** | 3 min | 31 min |
| Concept Block 3: Creating New Calculated Columns + Practical | 13 min | 44 min |
| Concept Block 4: Descriptive Analysis Using Formulas + Practical | 10 min | 54 min |
| Summary & Bridge | 3 min | 57 min |
| Q&A & Doubt Solving | 3 min | 60 min |

---

## Opening — "The Broken Drag" (6 min)

Project a small sheet: a `Sale Amount` column (D2:D8) and a fixed `Tax Rate` in cell B1 (e.g., 5%). Write on the board:

> **"=D2*$B$1 dragged down 50 rows → all correct. =D2*B1 dragged down 50 rows → row 1 correct, everything after is wrong."**

> "Same formula, one tiny difference — a couple of dollar signs. Someone guess what went wrong in the second version."

[Let students guess. Draw out: without the `$`, B1 shifted to B2, B3, B4... as it was dragged, so each row multiplied by an empty or wrong cell instead of the actual tax rate.]

> "This is a real, extremely common spreadsheet bug — and it fails silently. No error message, just quietly wrong numbers from row 2 onward."

**Pivot line:**
> "Today you get the three formulas every analyst uses constantly — SUM, AVERAGE, COUNT — and the two techniques that make them scale across a whole dataset without breaking. This is where all of Session 5's data validation finally pays off — you can now trust the numbers these formulas produce."

---

## Concept Block 1: SUM, AVERAGE, COUNT (10 min)

> "Three formulas, three questions. If I show you a stack of 7 days of Zappy Mart sales — what question does SUM answer? AVERAGE? COUNT?"

[Draw out: SUM = total, AVERAGE = typical value (same mean from Session 1), COUNT = how many entries.]

Write the syntax on the board:
```
=SUM(D2:D8)
=AVERAGE(D2:D8)
=COUNT(D2:D8)
```

> "Quick connection to Session 1 — what did we call this AVERAGE calculation back then?"

[Draw out: the mean — same math, now automated.]

### 🔴 The trap / highest-value moment
> "COUNT vs COUNTA — who can guess the difference?"

[Draw out: COUNT only counts numeric cells; COUNTA counts any non-blank cell, including text.]

**One-line rule to write down:**
> *"COUNT counts numbers only — if your column has text mixed in, COUNT will silently ignore it."*

## Practical Block 1: Which Formula? (part of the 10 min)

> "In pairs, 60 seconds — for Zappy Mart's `Sale Amount` column D2:D8, write the formula for (1) total weekly sales, (2) average daily sales, (3) confirming all 7 days have data logged."

**Answer key (with reasoning aloud):**
1. `=SUM(D2:D8)` — adds every value in the range.
2. `=AVERAGE(D2:D8)` — same mean logic from Session 1, now automatic.
3. `=COUNT(D2:D8)` — if it returns 7, all days have numeric data; if less, something's missing — this doubles as a Session 5-style validation check.

---

## Concept Block 2: Applying Formulas Across Rows and Columns (12 min)

> "You've got one formula working for Jaipur. Four more branches to go. Who's retyping four more nearly-identical formulas by hand?"

[Let the "no one, obviously" land.]

> "Right — you use the fill handle: write it once, drag, and cell references shift automatically for each row or column. Let's see this live."

Demonstrate dragging `=SUM(D2:D8)` across a row of 5 branch columns, referencing the correct branch each time.

> "Now the catch from the opening. What if one part of your formula should NOT shift when you drag it — like a shared tax rate in one fixed cell?"

Write:
```
=D2*B1     → relative, shifts when dragged (usually wrong here)
=D2*$B$1   → absolute, locked, stays on B1 no matter where you drag
```

### 🔴 The trap / highest-value moment
> "This is the opening's bug, exactly. What's the fix?"

[Draw out: add `$` before the column letter and row number of the reference you want locked.]

**One-line rule:**
> *"If a cell should stay fixed no matter where you drag, lock it with `$` — every time."*

## Practical Block 2: Fix the Broken Drag (part of the 12 min)

> "In pairs, 90 seconds — rewrite `=D2*B1` (tax rate in B1) so it can be safely dragged down 50 rows without breaking."

**Answer key (with reasoning aloud):**
> `=D2*$B$1` — locking both the column and row of B1 with `$` ensures every dragged row still multiplies by the correct, fixed tax rate in B1, while D2 correctly shifts to D3, D4, etc. as intended.

💬 Expect a question: "Do I always need to lock both the column and row?" Welcome it. Say: *"Not always — sometimes you only want to lock the row (`B$1`) or only the column (`$B1`), depending on whether you're dragging across or down. For a single fixed cell like a tax rate, locking both is the safest default."*

---

## ☕ BREAK (3 min)

---

## Concept Block 3: Creating New Calculated Columns (13 min)

> "Zappy Mart's raw data has `Units Sold` and `Sale Amount`. It doesn't have 'Average Price per Unit' — that column doesn't exist yet. How would you create it?"

[Draw out: a new column with a formula referencing the two existing columns.]

Write on the board:
```
New column: Avg Price per Unit
Formula: =Sale_Amount / Units_Sold
```

> "Drag this down for every row, and now you have a genuinely new piece of information that wasn't in the original export — this is a calculated column."

### 🔴 The trap / highest-value moment
> "What happens if a day has zero units sold, and this formula runs on that row?"

[Draw out: `#DIV/0!` error — dividing by zero.]

**One-line rule to write down:**
> *"Before dividing by a column, ask: could this ever be zero? If yes, plan for it — don't ignore the error."*

## Practical Block 3: Build the Column (part of the 13 min)

› "In pairs, 90 seconds — Zappy Mart's Udaipur branch has one day with 0 `Units Sold` but a non-zero `Sale Amount` (a data-entry issue, not a real zero-sales day, per Session 2's cleaning lessons). Your `Avg Price per Unit` formula shows `#DIV/0!` on that row. What's your plan?"

**Answer key (with reasoning aloud):**
> Don't just hide or delete the error — investigate the source row first, since a non-zero Sale Amount with 0 Units Sold suggests a data-entry mistake (per Session 2.1/2.2's cleaning and validation habits), not a legitimate zero-sales day. Fix the underlying data if possible; only after that, decide whether the calculated column should show blank, "N/A," or an actual recalculated value for that row.

---

## Concept Block 4: Descriptive Analysis Using Formulas (10 min)

> "A cricket commentator doesn't just read scores — they combine numbers into a story. Let's do that here. Question: 'Which branch had the highest total weekly sales, and how does its average daily sales compare to the company-wide average?'"

Walk through combining the pieces live:
1. `SUM` per branch (Concept Block 1)
2. Dragged across all 5 branches (Concept Block 2)
3. Company-wide `AVERAGE` across all branches combined
4. Compare the top branch's average to the company-wide average

> "Notice this isn't one formula — it's several simple formulas combined into a comparison. That comparison is what actually makes it useful to a manager."

### 🔴 The trap / highest-value moment
> "What's wrong with just reporting 'Jaipur's total sales: ₹1,42,000' and stopping there?"

[Draw out: a number alone has no context — is that good, bad, better or worse than another branch or a target? Descriptive analysis needs comparison to mean anything.]

**One-line rule:**
> *"A number without a comparison isn't an insight yet — it's just a number."*

## Practical Block 4: Build the Comparison (part of the 10 min)

> "In pairs, 90 seconds — using SUM and AVERAGE, describe exactly what you'd calculate to answer: 'Is Udaipur branch's average daily sales above or below the company-wide average?'"

**Answer key (with reasoning aloud):**
> Calculate `AVERAGE` of Udaipur's daily sales range, calculate a company-wide `AVERAGE` across all branches' combined daily sales, then directly compare the two numbers (e.g., Udaipur avg ₹28k vs company-wide avg ₹22k → Udaipur is above average). Reasoning: this directly answers the comparative business question, rather than reporting Udaipur's number in isolation.

---

## Summary & Bridge (3 min)

| Concept | The one thing to remember |
|---|---|
| SUM/AVERAGE/COUNT | Three different questions about the same range: total, typical, how many |
| Applying across rows/columns | Fill handle scales formulas; `$` locks references that shouldn't shift |
| Calculated columns | New formulas can create insight not present in the raw data — watch for `#DIV/0!` |
| Descriptive analysis | Combine formulas into comparisons — a lone number isn't yet an insight |

> "Remember the opening's broken drag — one missing `$` and every row after the first was silently wrong. That's now a bug you'll catch before it ever reaches a report."

**Bridge:** "Next session, **Pivot Tables and Quick Insights**, takes these exact same summaries — totals, averages, counts — and lets you compare them across categories like branch or product instantly, without writing a single repeated formula."

---

## Q&A & Doubt Solving (3 min)

**Q: Is there a limit to how many rows a formula can be dragged across?**
→ Practically no — spreadsheets handle thousands of rows fine. For very large datasets, though, Module 2 (SQL) and Module 4 (Python) become faster and more manageable.

**Q: What's the difference between `SUM` and just typing `=D2+D3+D4...`?**
→ Same result for a small range, but `SUM(range)` is faster to write, easier to drag/adjust, and far less error-prone for large ranges — always prefer it over manually adding cell by cell.

**Q: Can GenAI write these formulas for us?**
→ Yes, and it's a great use case — but per Session 3, always validate the formula it suggests actually references the right cells for your specific sheet before trusting it.

**Q: What if I want an average that ignores blank cells automatically?**
→ `AVERAGE()` already ignores blanks by default (unlike some other tools) — it only factors in cells that actually contain numbers, which is worth confirming with a quick `COUNT` check alongside it.

---

## Instructor Notes
- **Words not yet earned — avoid:** array formulas, VLOOKUP/XLOOKUP, nested functions, named ranges. These are useful but not needed yet — keep the toolkit to SUM/AVERAGE/COUNT/COUNTA and simple calculated columns.
- **Biggest risk this session:** the `$` absolute reference concept is small but easy to silently misunderstand — many students will nod along without truly getting it. Use the opening's broken-drag example at least twice more (Concept Block 2 and the summary) to reinforce it concretely.
- **Board management:** keep the `=D2*B1` vs `=D2*$B$1` comparison visible the entire session — it's the one line that makes the absolute-reference concept concrete rather than abstract.
- **Common confusions (numbered):**
  1. Forgetting `$` when a formula references a fixed cell that shouldn't shift while dragging.
  2. Using `COUNT` instead of `COUNTA` on a column with text entries.
  3. Dividing by a column that can contain zero without planning for `#DIV/0!`.
  4. Reporting a single formula result without comparing it to anything.
- **Cross-references forward:** Session 3.2 (Pivot Tables — the same SUM/AVERAGE/COUNT logic applied automatically across categories), Module 2 (SQL's `SUM()`, `AVG()`, `COUNT()` are the identical concepts in a new syntax), Module 4 (pandas' `.sum()`, `.mean()`, `.count()` — same logic again, at scale).
- **Local/cultural context notes:** The trip-budget and event-expense-splitting framing for SUM/AVERAGE landed well with this cohort's own group-expense experiences — continue using Zappy Mart's 5 branches as the row-vs-column drag example for continuity.
