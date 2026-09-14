# Lecture Script: Spreadsheets — Clean Up the Data
> **Instructor Reference** — Module 1: Analytics Foundations + GenAI + Spreadsheets | Academic Session 4 | Duration: 1 Hour | Instructor: [Name/Placeholder]

---

## Session Overview
**Goal:** By the end, students can load a raw dataset into Excel/Sheets, identify missing values, duplicates, and formatting issues by eye, clean them using Remove Duplicates and standardization tools, and use sort/filter to inspect data quickly.

**Student profile at this point:** Students know the analytics workflow, metrics vs KPIs, and how to validate GenAI outputs — but this is their first fully hands-on tool session. Assume comfort with spreadsheets for basic typing/viewing, but no experience treating a spreadsheet as an analysis instrument. Boredom risk: cleaning data can feel tedious/unglamorous compared to GenAI — counter by tying it directly back to Session 3's lesson (garbage data in → wrong GenAI summary out).

**Key outcome:** Every student should leave with the instinct: never trust a total, count, or average from a dataset you haven't first inspected for missing values, duplicates, and formatting issues.

> 🎯 **The one sentence this session must land:** *A spreadsheet full of numbers isn't data you can trust — it's data you haven't inspected yet.*

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| Opening — "The Double-Counted Sale" | 6 min | 6 min |
| Concept Block 1: Loading Data into a Spreadsheet + Practical | 10 min | 16 min |
| Concept Block 2: Spotting Common Data Issues + Practical | 12 min | 28 min |
| **BREAK** | 3 min | 31 min |
| Concept Block 3: Cleaning — Duplicates & Formats + Practical | 13 min | 44 min |
| Concept Block 4: Sort and Filter to Inspect + Practical | 10 min | 54 min |
| Summary & Bridge | 3 min | 57 min |
| Q&A & Doubt Solving | 3 min | 60 min |

---

## Opening — "The Double-Counted Sale" (6 min)

Project or write a tiny 6-row extract of Zappy Mart transaction data on the board, with rows 3 and 5 identical (same date, store, amount), and one blank `Sale Amount` cell in row 4.

> "Someone just ran =SUM() on the Sale Amount column here and reported the total to head office. Before I tell you what happened — does anyone spot anything odd in these six rows?"

[Give it 20-30 seconds; let students notice the duplicate and/or the blank cell.]

> "Right — one sale got counted twice, and one sale got silently ignored because the cell was blank. The SUM formula doesn't know any of this — it just adds whatever's there. It's confidently wrong, exactly like GenAI was in Session 3."

**Pivot line:**
> "Today we fix the layer underneath every formula, pivot table, dashboard, and even every GenAI prompt you'll use for the rest of this course — the data itself. If the data going in is messy, everything built on top of it is quietly wrong, no matter how correct your formula is."

---

## Concept Block 1: Loading Data into a Spreadsheet (10 min)

> "Before touching a single formula, what's the very first thing you should do with a new file?"

[Draw out: open it and just look, don't calculate yet.]

Write the loading checklist on the board:
1. Open/import the file
2. Confirm row/column count looks roughly right
3. Freeze the header row
4. Take a full, unhurried first look

> "Why freeze the header row specifically?"

[Draw out: keeps column names visible while scrolling through thousands of rows — otherwise you lose track of what column you're even looking at.]

### 🔴 The trap / highest-value moment
> "What's the single most common mistake right after opening a new file?"

[Draw out: jumping straight into formulas/calculations before looking at the data properly.]

**One-line rule to write down:**
> *"Look before you calculate — issues are cheap to catch now and expensive to catch later."*

## Practical Block 1: First-Look Checklist (part of the 10 min)

> "In pairs, 60 seconds — looking at this six-row Zappy Mart extract on the board, list two things you'd check in your 'first look' before doing any analysis."

**Answer key (with reasoning aloud):**
> Sample answers: check whether all expected columns actually loaded separately (not jammed together), and whether the row count roughly matches what was expected (e.g., "we expect ~7 days of data, do we see ~7 unique dates?"). Reasoning: both catch structural problems before you've built anything on top of them.

---

## Concept Block 2: Spotting Common Data Issues (12 min)

> "Let's name what's actually wrong with data, in general. Three categories — someone define 'missing value' for me. Now 'duplicate.' Now 'formatting issue.'"

Write the three-issue table on the board:

| Issue | Example |
|---|---|
| Missing values | Blank `Sale Amount` cell |
| Duplicates | Same transaction entered twice |
| Formatting issues | "Jaipur" vs "jaipur " vs "JAIPUR" |

> "Why does 'Jaipur' vs 'jaipur' actually matter? Isn't it obviously the same city to a human reading it?"

[Draw out: to a human, yes — but a spreadsheet function like COUNTIF treats them as different text strings unless you standardize them.]

### 🔴 The trap / highest-value moment
> "Here's the dangerous one — someone tell me why a dataset can 'look fine' and still be wrong."

[Draw out: issues like duplicates or trailing spaces are often invisible unless you specifically sort, filter, or check for them — a quick visual scan won't catch most of these.]

**One-line rule:**
> *"'Looks fine at a glance' is not the same as 'clean' — always sort or filter to actually check."*

## Practical Block 2: Diagnose the Dataset (part of the 12 min)

> "In pairs, 90 seconds — Zappy Mart's `Store City` column shows: Jaipur, JAIPUR, jaipur, Udaipur, Udaipur, udaipur . List every issue you can spot, and name its category."

**Answer key (with reasoning aloud):**
> Formatting/capitalization inconsistency across "Jaipur" variants and "Udaipur" variants (three different case styles, plus a likely trailing space on "udaipur "). Reasoning: a COUNTIF("Jaipur") right now would undercount, since it wouldn't match "JAIPUR" or "jaipur" — this is purely a formatting issue category, not missing data or duplication.

💬 Expect a question: "Why not just manually retype every mismatched value?" Welcome it. Say: *"Fine for six rows, but real datasets have thousands — that's exactly why we use tools like PROPER(), TRIM(), and Find & Replace, which we're building next."*

---

## ☕ BREAK (3 min)

---

## Concept Block 3: Cleaning — Duplicates & Formats (13 min)

> "Time to actually fix what we found. First — duplicates. If I run Remove Duplicates using only the `Store City` column on a 1,000-row dataset, what happens?"

[Let students guess — draw out: nearly everything gets deleted, since many genuinely different transactions share the same city.]

> "Exactly — that's a real mistake people make. The fix: choose the *combination* of columns that actually defines a true duplicate — here, probably Date + Store City + Sale Amount together."

Write the cleaning toolkit on the board:

| Fix | Tool |
|---|---|
| Duplicates | Data → Remove duplicates (select the right column combination) |
| Text casing/spacing | PROPER(), TRIM(), or Find & Replace |
| Dates | Format → Number → Date, applied consistently |

### 🔴 The trap / highest-value moment
> "Say the one-line rule about choosing duplicate columns with me."

**One-line rule to write down:**
> *"A duplicate isn't 'same in one column' — it's 'same across every column that defines a unique record.'"*

## Practical Block 3: Fix the Six Rows (part of the 13 min)

> "Back to our opening six-row extract, with the double-counted sale in rows 3 and 5. In pairs, 90 seconds — which columns together would you use to define 'duplicate' here, and what's your plan for the blank `Sale Amount` cell in row 4?"

**Answer key (with reasoning aloud):**
> Duplicate definition: Date + Store City + Sale Amount together (not just one column) — this correctly flags rows 3 and 5 as true duplicates without wrongly deleting other real rows. For the blank cell: don't guess a number — first investigate why it's blank (was it never recorded, or is it a genuine zero-sales day?) before deciding whether to leave it, flag it, or follow up with the source.

💬 Expect pushback: "Can't we just fill the blank with 0 or the average?" Welcome it. Say: *"Tempting, but dangerous — a blank might mean 'no data recorded,' not 'zero sales.' Filling it with a guess can quietly distort your median and mean, exactly like Session 1's outlier lesson. Investigate before you fill."*

---

## Concept Block 4: Sort and Filter to Inspect (10 min)

> "Once cleaning tools are in place, how do you actually *find* the rows that need fixing, in a dataset of thousands of rows, without scrolling forever?"

[Draw out: sort and filter.]

> "Filter the `Sale Amount` column to show only blanks — every problem row appears instantly. Sort by `Date` then `Store City` — identical transactions land right next to each other, easy to eyeball."

### 🔴 The trap / highest-value moment
> "Here's a mistake almost everyone makes at least once — someone guess it."

[Draw out: forgetting a filter only *hides* rows, it doesn't delete or fix them — fixing only what's visible and forgetting the rest of the dataset is still there, filtered out of view.]

**One-line rule:**
> *"A filter hides rows, it doesn't fix them — always clear the filter and double-check before calling the job done."*

## Practical Block 4: Find the Duplicates (part of the 10 min)

> "In pairs, 60 seconds — describe, step by step, how you'd use sort (not remove duplicates) to visually confirm which rows in a 200-row dataset are true duplicates before deleting anything."

**Answer key (with reasoning aloud):**
> Sort by Date, then Store City, then Sale Amount (in that priority order) — this groups any truly identical rows so they sit directly next to each other, making them easy to visually confirm as real duplicates (rather than blindly trusting an automated tool) before removing anything.

---

## Summary & Bridge (3 min)

| Concept | The one thing to remember |
|---|---|
| Loading data | Look before you calculate — check structure before formulas |
| Spotting issues | Missing values, duplicates, formatting issues — often invisible at a glance |
| Cleaning | Use the right column combination for duplicates; standardize formats, don't guess-fill blanks |
| Sort & filter | Fast, non-destructive ways to inspect — but filters hide, they don't fix |

> "Remember the opening's double-counted sale and silently ignored blank cell — a =SUM() formula can't tell the difference between clean and messy data. That's now your job, not the formula's."

**Bridge:** "Next session, **Make Data Ready for Analysis**, goes one level deeper — structuring your now-cleaned data into consistent formats and data types, and validating that your cleaning actually worked, before you start building formulas on top of it."

---

## Q&A & Doubt Solving (3 min)

**Q: Should we always run Remove Duplicates immediately after loading data?**
→ No — first inspect and decide which columns actually define a true duplicate for that specific dataset. Running it blindly can delete real, distinct records.

**Q: What if I'm not sure whether a blank cell means "zero" or "not recorded"?**
→ Don't guess — flag it, and if possible check with whoever owns the data source. Filling it wrong can distort your mean/median exactly like an unnoticed outlier.

**Q: Can GenAI help clean data for us?**
→ Yes, it can suggest what to standardize or draft a cleaning plan — but per Session 3, you must still validate its suggestions against your actual data rather than applying them blindly.

**Q: How do I know when data is "clean enough" to move on?**
→ There's no single universal rule, but a good check is: can you confidently run a SUM, COUNT, or AVERAGE on it and trust the number? If you're still unsure, more inspection is needed — Session 2.2 builds a fuller validation checklist for exactly this.

---

## Instructor Notes
- **Words not yet earned — avoid:** data type casting, regex, normalization (as a technical term), null vs NaN distinctions. Keep language to "missing," "duplicate," and "inconsistent format" only.
- **Biggest risk this session:** feels tedious/unglamorous compared to Session 3's GenAI session. Counter by repeatedly tying cleaning back to consequences students already care about — wrong totals, wrong GenAI summaries, wrong business decisions.
- **Board management:** keep the six-row opening extract visible the entire session, and return to it explicitly in Concept Block 3's practical — this makes the abstract cleaning tools feel like they're solving the exact problem from the hook.
- **Common confusions (numbered):**
  1. Believing a dataset that "looks fine" at a glance is clean.
  2. Running Remove Duplicates on a single column instead of the right combination.
  3. Guess-filling blank cells with 0 or an average instead of investigating first.
  4. Forgetting that filters hide rows rather than deleting or fixing them.
- **Cross-references forward:** Session 2.2 (Make Data Ready for Analysis — data types, validation checklist), Session 3.1 (Formulas — which only work correctly on data cleaned this session), Module 2 (SQL `WHERE`/`DISTINCT` do similar jobs at scale), Module 4 (pandas `.duplicated()`, `.isnull()` automate exactly what was done manually today).
- **Local/cultural context notes:** The attendance-register analogy for missing/duplicate/inconsistent entries landed well with this cohort's shared classroom experience — keep reusing it alongside Zappy Mart's Jaipur/Udaipur/Kanpur/Lucknow branches for continuity.
