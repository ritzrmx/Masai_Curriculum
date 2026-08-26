# Lecture Script: Foundations of Data — Pandas: Loading, Inspection & Filtering
> **Instructor Reference** — Module 1: Foundations of Data | Academic Session 10 | Duration: 2 Hours | Instructor: [Industry Mentor / Name Placeholder]

---

## Session Overview
**Goal:** By the end, students can load a CSV into a DataFrame, inspect it thoroughly with head/info/describe/shape, filter rows using boolean indexing and loc/iloc, and identify data quality issues from inspection output.

**Student profile at this point:** Comfortable with NumPy arrays, Python data structures, and boolean logic. This is their first real exposure to Pandas — the tool most of the rest of the course centers on. Likely wrong assumption: that `df["col"] > 500 and df["col2"] == "X"` works the same as it did with plain Python variables. Boredom risk is low — this feels immediately powerful; frustration risk is moderate around the `&`/`and` distinction in boolean indexing.

**Key outcome:** Students should leave with a default habit: never analyze a new dataset before running head(), info(), describe(), and shape() first.

> 🎯 **The one sentence this session must land:** *Always inspect before you trust a dataset — head, info, describe, and shape catch problems that would otherwise silently corrupt every analysis built on top of them.*

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| Opening — "The Ledger You'd Never Trust Blindly" | 8 min | 8 min |
| Concept + Practical Block 1: Loading Data & DataFrame vs Series | 18 min | 26 min |
| Concept + Practical Block 2: Inspecting a DataFrame | 25 min | 51 min |
| ☕ BREAK | 5 min | 56 min |
| Concept + Practical Block 3: Boolean Indexing | 27 min | 83 min |
| Concept + Practical Block 4: loc vs iloc, Sorting & Column Selection | 22 min | 105 min |
| Summary & Bridge | 5 min | 110 min |
| Q&A & Doubt Solving | 10 min | 120 min |

---

## Opening — "The Ledger You'd Never Trust Blindly" (8 min)

> "Imagine someone hands you a shop's entire sales ledger — hundreds of pages — and asks you to calculate this month's total revenue right now. Would you just start adding numbers immediately, or would you first flip through it to check for torn pages, missing entries, or numbers that don't make sense?"

[Pause for the room's instinctive answer — most will say "check it first."]

> "That instinct is exactly what today's session formalizes. Pandas is how Python reads that entire ledger into memory as a table — and before we do ANY real analysis, we always inspect it first. Skipping that step is the single most common way beginners produce confidently wrong answers."

Pivot line: "Let's load our first real dataset and see this ledger analogy in action."

---

## Concept + Practical Block 1: Loading Data & DataFrame vs Series (18 min)

### "The digital version of the kirana shop ledger"
> "Every row in a shop's ledger is a transaction. Every column is a field — date, item, amount. A Pandas DataFrame is exactly this, loaded into Python."

**Hands-on, live-coded (use a sample sales CSV):**
```python
import pandas as pd

df = pd.read_csv("sales.csv")
print(type(df))
print(type(df["amount"]))
```

> "`df` is the whole ledger — a DataFrame. `df['amount']` is just ONE column pulled out — a Series. Same data, different shape."

**Answer key / reasoning to say aloud:** Demonstrate `df[["amount"]]` with double brackets right after, and compare `type()` — a DataFrame with one column, versus a Series. Point out visually that a Series prints without the extra column header formatting a DataFrame shows.

### 🔴 The trap / highest-value moment
Write on the board: **"Single brackets `df['col']` → Series. Double brackets `df[['col']]` → DataFrame with one column. They look almost identical but behave differently."**

💬 **Expect an argument about:** "Why would I ever want a one-column DataFrame instead of just a Series?" Welcome it. Say: *"Certain operations — especially merging and some plotting functions — expect a DataFrame, not a Series. Knowing both forms exist means you're never stuck when a function insists on one over the other."*

---

## Concept + Practical Block 2: Inspecting a DataFrame (25 min)

### "Flipping through the ledger before trusting it"
> "Before calculating anything, flip through the first few pages, check for missing entries, and skim a quick summary. That's exactly `head()`, `info()`, and `describe()`."

**Hands-on, live-coded, one function at a time:**
```python
print(df.head())
print(df.info())
print(df.describe())
print(df.shape)
```

Pause deliberately after `df.info()`:
> "Look at the non-null counts for each column. Is every column the same count? If one is lower, what does that tell you?"

**Answer key / reasoning to say aloud:** A lower non-null count in one column (e.g., "phone") than the total row count signals missing values in that column specifically — a real data quality issue worth flagging BEFORE building any calculation that depends on it.

### 🔴 The trap / highest-value moment
Write on the board: **"NEVER analyze a dataset before running head(), info(), describe(), and shape(). Every one of these can catch a problem that would otherwise silently corrupt your results."**

💬 **Expect an argument about:** "Isn't this a lot of extra steps before I even get to the 'real' analysis?" Welcome it. Say: *"It feels that way for the first few datasets — but the first time `describe()` reveals a price column secretly loaded as text instead of numbers, you'll understand why skipping this step is far more expensive than the two minutes it takes."*

---

## ☕ BREAK (5 min)

---

## Concept + Practical Block 3: Boolean Indexing (27 min)

### "Pulling only the big-ticket receipts"
> "A shop owner going through receipts, pulling out only the ones over ₹500 — that's boolean indexing. It's the exact same True/False logic from Session 2.1, now applied to an entire column of a DataFrame at once."

**Hands-on:**
```python
big_orders = df[df["amount"] > 500]
print(big_orders)
```

Then deliberately trigger the trap:
```python
df[df["amount"] > 500 and df["city"] == "Hyderabad"]   # this errors
```

> "Why does this fail, when `and` worked perfectly fine back in Session 2.1?"

**Answer key / reasoning to say aloud:** Python's plain `and`/`or` expect a single True/False value on each side — but `df["amount"] > 500` produces an entire COLUMN of True/False values, not one. Pandas needs `&`/`|` specifically because they're built to compare column-by-column, row-by-row — and each condition must be wrapped in parentheses to avoid operator-precedence surprises.

Fix it live:
```python
df[(df["amount"] > 500) & (df["city"] == "Hyderabad")]
```

### 🔴 The trap / highest-value moment
Write on the board: **"On a DataFrame, use `&` and `|`, NOT `and`/`or` — and always wrap each condition in parentheses."**

💬 **Expect an argument about:** "This feels like an arbitrary extra rule just for Pandas — why?" Welcome it. Say: *"It's not arbitrary — `and`/`or` are designed for single True/False values, and a DataFrame condition produces a whole column of them at once. `&`/`|` are Pandas' way of doing that comparison correctly, row by row, across the entire column."*

---

## Concept + Practical Block 4: loc vs iloc, Sorting & Column Selection (22 min)

### "Searching the ledger by date label vs. by page number"
> "Searching a ledger 'give me the row for 15th July' is searching by LABEL — that's `loc`. Searching 'give me the 5th row, whatever date it happens to be' is searching by POSITION — that's `iloc`."

**Hands-on:**
```python
top_orders = df.sort_values("amount", ascending=False)
print(top_orders[["item", "amount"]].head())

print(df.loc[3, "amount"])
print(df.iloc[3, 1])
```

Now demonstrate the trap that makes this block matter:
```python
filtered = df[df["amount"] > 500]
print(filtered.loc[0])    # may not exist if row 0 was filtered out
print(filtered.iloc[0])   # always works — first row of what's LEFT
```

> "After filtering, the original row labels stick around, but positions reset. `loc[0]` might not even exist anymore if row 0 got filtered out — but `iloc[0]` always gives you whatever the first remaining row is."

### 🔴 The trap / highest-value moment
Write on the board: **"loc and iloc only match by coincidence when row labels are simple 0,1,2,... After filtering or sorting, they usually diverge."**

💬 **Expect an argument about:** "So which one should I default to using?" Welcome it. Say: *"There's no universal answer — use `loc` when you're thinking in terms of meaningful labels (like a specific date or ID), and `iloc` when you're thinking in terms of raw position (like 'the top 5 rows'). The key is being deliberate about which one you actually mean."*

---

## Summary & Bridge (5 min)

| Concept | The one thing to remember |
|---|---|
| DataFrame vs Series | Double brackets keep it a DataFrame; single brackets give a Series |
| Inspection | Always run head/info/describe/shape before trusting new data |
| Boolean indexing | Use `&`/`|` with parentheses, never plain `and`/`or` |
| loc vs iloc | `loc` is by label, `iloc` is by position — they diverge after filtering/sorting |

Close on the thesis: *"Always inspect before you trust a dataset — head, info, describe, and shape catch problems that would otherwise silently corrupt every analysis built on top of them."*

Bridge: "Today you looked at one table at a time. Next session, you'll summarize this data by group and combine multiple tables together in **Pandas: Aggregation, Groupby & Merging**."

---

## Q&A & Doubt Solving (10 min)

**Q: What happens if my CSV has a column that's mostly numbers but a few text values mixed in?**
→ Pandas will likely load the entire column as text (`object` dtype) rather than numeric — `info()` and `describe()` together will reveal this, since the numeric summary stats won't appear for that column.

**Q: Can I filter using more than two conditions at once?**
→ Yes — chain as many `&`/`|` conditions as needed, each wrapped in its own parentheses, e.g., `df[(cond1) & (cond2) & (cond3)]`.

**Q: Does sort_values() change the original DataFrame?**
→ No, not by default — it returns a new sorted DataFrame; you'd need to reassign it (`df = df.sort_values(...)`) or use `inplace=True` to modify the original directly.

**Q: Is there a way to filter using string conditions, like "contains a certain word"?**
→ Yes — `df[df["item"].str.contains("Chai")]` filters rows where a text column contains a given substring, extending boolean indexing to text-based conditions.

**Q: What's the difference between df.shape and len(df)?**
→ `df.shape` returns a tuple of `(rows, columns)`; `len(df)` returns just the row count — both are useful, but `shape` gives you the full picture in one call.

---

## Instructor Notes
- **Words not yet earned — avoid using without defining:** "MultiIndex," "chained indexing warning," "categorical dtype." These are more advanced Pandas topics that would overload this foundational session.
- **Biggest risk this session:** the `and`/`or` vs `&`/`|` error in Block 3 is the single most common Pandas beginner mistake — let students hit the error themselves in the hands-on before revealing the fix, so the correction sticks.
- **Board management:** Keep the loc-vs-iloc "label vs position" distinction visible through the end of Block 4 — it's easy to forget once sorting and filtering are introduced and row labels stop matching positions.
- **Common confusions, numbered:**
  1. Confusing single vs. double bracket column selection (Series vs. DataFrame).
  2. Using plain `and`/`or` instead of `&`/`|` in boolean indexing.
  3. Assuming `loc` and `iloc` always return the same row after filtering or sorting.
- **Cross-references to later sessions:** Boolean indexing here is the direct Pandas equivalent of SQL's `WHERE` clause (Session 7.1); today's inspection habits (head/info/describe) become the starting checklist for the EDA session (6.3); loc/iloc precision matters again when merging tables in Session 5.2.
- **Local/cultural context notes:** The kirana shop ledger and big-ticket receipt analogies anchor this entire session — keep returning to "the ledger" as the running metaphor across all four blocks so students build one coherent mental model rather than four disconnected ones.
