# Lecture Script: Foundations of Data — Pandas: Aggregation, Groupby & Merging
> **Instructor Reference** — Module 1: Foundations of Data | Academic Session 11 | Duration: 2 Hours | Instructor: [Industry Mentor / Name Placeholder]

---

## Session Overview
**Goal:** By the end, students can group and aggregate data to answer business questions using groupby and agg, handle missing values by deliberately dropping or filling them, and merge and concatenate multiple DataFrames correctly.

**Student profile at this point:** Comfortable loading, inspecting, and filtering a single DataFrame from Session 5.1. Likely wrong assumption: that `dropna()` and `merge()`'s default settings are always "safe" choices that don't need scrutiny. Boredom risk is low — groupby answers feel immediately like "real business insight"; frustration risk is moderate around merge types, since an inner merge silently dropping rows doesn't throw an error.

**Key outcome:** Students should leave asking, before calling `dropna()` or `merge()`: "what exactly am I about to lose or keep, and is that actually what I want?"

> 🎯 **The one sentence this session must land:** *groupby answers "how does this break down by category," and merge/concat answer "how do I bring two tables together" — but both have defaults that silently discard data if you're not deliberate about your choices.*

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| Opening — "Total Sales, By City, In One Line" | 8 min | 8 min |
| Concept + Practical Block 1: groupby() & agg() | 25 min | 33 min |
| Concept + Practical Block 2: value_counts() & Missing Values | 22 min | 55 min |
| ☕ BREAK | 5 min | 60 min |
| Concept + Practical Block 3: merge() & join() | 28 min | 88 min |
| Concept + Practical Block 4: concat() & drop_duplicates() | 17 min | 105 min |
| Summary & Bridge | 5 min | 110 min |
| Q&A & Doubt Solving | 10 min | 120 min |

---

## Opening — "Total Sales, By City, In One Line" (8 min)

> "Last session, you learned to filter — pull out ONE city's rows and manually sum them. Now imagine your manager asks: 'give me the total sales for EVERY city, broken down.' Are you going to filter and sum separately for each of 20 cities?"

Type live:
```python
city_sales = df.groupby("city")["amount"].sum()
print(city_sales)
```

> "One line. Every city, summed, automatically. This is the entire power of `groupby` — answer 'break this down by category' questions instantly, instead of manually filtering category by category."

Pivot line: "Let's understand exactly what's happening under that one line."

---

## Concept + Practical Block 1: groupby() & agg() (25 min)

### "Sorting receipts into piles"
> "A shop owner sorting receipts into piles by product category, then totaling each pile — that's groupby, done by hand. Pandas does it instantly, at any scale."

**Hands-on:**
```python
city_sales = df.groupby("city")["amount"].sum()
print(city_sales)

city_stats = df.groupby("city")["amount"].agg(["sum", "mean", "count"])
print(city_stats)
```

Ask the room: "What does the `count` column actually tell us here — total ₹ amount, or something else?" Let them reason through it — count is the number of orders per city, not a rupee figure, distinguishing it clearly from sum and mean.

### 🔴 The trap / highest-value moment
Write on the board: **"`df.groupby('city').sum()` without specifying a column sums EVERY numeric column — including ones that make no sense to total, like an ID column."**

Demonstrate live: run `df.groupby("city").sum()` without column specification and point out any nonsensical summed columns in the output.

💬 **Expect an argument about:** "Why not just always specify every column I want, every time, to avoid confusion?" Welcome it. Say: *"That's exactly the right habit — being explicit about which column(s) you're aggregating is safer and clearer, both for you and for anyone reading your code later."*

---

## Concept + Practical Block 2: value_counts() & Missing Values (22 min)

### "The form with a blank phone number field"
> "A customer forgot to fill in their phone number on a form. Do you write 'not provided' in that blank, or throw the whole form away? Both are valid choices — but they're very different choices, and you must make it deliberately."

**Hands-on:**
```python
print(df["city"].value_counts())
print(df.isnull().sum())
df["phone"] = df["phone"].fillna("Not provided")
```

Then demonstrate the trap:
```python
print(df.shape)          # e.g. (1000, 6)
print(df.dropna().shape) # e.g. (200, 6) — a shock
```

> "We went from 1000 rows to 200 with one line. What happened?"

**Answer key / reasoning to say aloud:** `dropna()` with default settings drops an ENTIRE row if even ONE column has a missing value — if 800 rows were missing something in just one relatively unimportant column (like an optional phone number), you just lost 800 rows of otherwise perfectly good data.

### 🔴 The trap / highest-value moment
Write on the board: **"`dropna()` removes the WHOLE row for even one missing value, in any column, by default. Always check the row-count impact before trusting it."**

💬 **Expect an argument about:** "So should I just never use dropna() then?" Welcome it. Say: *"Not at all — sometimes dropping incomplete rows is exactly right, especially for critical columns. The point isn't 'avoid dropna,' it's 'know exactly what you're about to lose before you run it' — check `.isnull().sum()` first, every time."*

---

## ☕ BREAK (5 min)

---

## Concept + Practical Block 3: merge() & join() (28 min)

### "Matching the hostel room list to the student ID list"
> "A hostel room allocation list and a student ID list, matched by student ID — that's a merge. Two related tables, combined using a shared key."

**Hands-on, building all three merge types live:**
```python
customers = pd.DataFrame({"customer_id": [1,2,3], "name": ["Priya","Rohan","Meera"]})
orders = pd.DataFrame({"customer_id": [1,1,2], "item": ["Chai","Samosa","Cola"]})

inner_merge = pd.merge(customers, orders, on="customer_id", how="inner")
left_merge = pd.merge(customers, orders, on="customer_id", how="left")

print(inner_merge)
print(left_merge)
```

Ask before running: "What happens to Meera — customer_id 3 — in each version?"

**Answer key / reasoning to say aloud:** In the inner merge, Meera disappears entirely, since she has no matching order rows. In the left merge, she stays, with her `item` column showing as missing (`NaN`) — this is exactly why choosing the merge type deliberately matters.

### 🔴 The trap / highest-value moment
Write on the board: **"Inner merge (the default) SILENTLY drops unmatched rows — no error, no warning. Always ask: do I need to see the unmatched rows too?"**

💬 **Expect an argument about:** "If inner is the default, isn't it usually the 'safe' choice?" Welcome it. Say: *"It's the most common choice, not necessarily the safest — 'safe' depends entirely on your question. If your manager asks 'which customers have never ordered,' an inner merge would have silently hidden the exact answer you needed."*

---

## Concept + Practical Block 4: concat() & drop_duplicates() (17 min)

### "Stacking two months' ledgers into one"
> "January's ledger and February's ledger, stacked one after another into a single continuous record — that's `concat()`. If a transaction accidentally appears in both months, `drop_duplicates()` removes the repeat."

**Hands-on:**
```python
all_sales = pd.concat([january_sales, february_sales])
print(all_sales.shape)

all_sales = all_sales.drop_duplicates(subset=["order_id"])
print(all_sales.shape)
```

**Answer key / reasoning to say aloud:** Point out the row count dropping slightly after `drop_duplicates()` — that difference IS the number of accidentally double-recorded transactions, made visible directly through the shape change.

### 🔴 The trap / highest-value moment
Write on the board: **"`concat()` stacks similar tables (more ROWS). `merge()` combines related tables using a key (more COLUMNS). Using the wrong one produces nonsense."**

💬 **Expect an argument about:** "How do I quickly tell which one I need in a real situation?" Welcome it. Say: *"Ask: are these two tables describing the SAME kind of thing (like two months of the same sales data) — that's concat. Or are they describing DIFFERENT but related things (like customers and their orders) — that's merge."*

---

## Summary & Bridge (5 min)

| Concept | The one thing to remember |
|---|---|
| groupby & agg | Splits data by category, then summarizes each group — be explicit about which column |
| value_counts & missing values | `dropna()` removes whole rows on any missing value — check impact first |
| merge & join | Choose the merge type deliberately — inner silently drops unmatched rows |
| concat & drop_duplicates | concat stacks similar tables; merge combines related tables by key |

Close on the thesis: *"groupby answers 'how does this break down by category,' and merge/concat answer 'how do I bring two tables together' — but both have defaults that silently discard data if you're not deliberate about your choices."*

Bridge: "Every groupby and merge you did today secretly relied on geometry and statistics you haven't formally named yet. Next session is a Master class where we step back and look at the coordinate plane, slope, and descriptive statistics underneath all of it."

---

## Q&A & Doubt Solving (10 min)

**Q: Can I group by more than one column at once?**
→ Yes — `df.groupby(["city", "item"])["amount"].sum()` groups by every unique combination of city AND item, giving a more granular breakdown.

**Q: What's the difference between fillna() and dropna() in terms of when to use each?**
→ Use `fillna()` when a sensible placeholder exists and you want to preserve the rest of the row's data; use `dropna()` when the missing value makes the entire row unusable for your specific analysis.

**Q: Does merge() require the key column to have the exact same name in both DataFrames?**
→ Not necessarily — if the column names differ, you can use `left_on` and `right_on` to specify which column from each DataFrame to match on.

**Q: What happens if I concat() two DataFrames with different columns?**
→ Pandas will include all columns from both, filling in missing values (`NaN`) wherever a row's original table didn't have that column — usually a sign the two tables weren't truly meant to be stacked.

**Q: Is there an "outer" merge type too?**
→ Yes — `how="outer"` keeps ALL rows from both DataFrames, matching where possible and filling with missing values where there's no match on either side.

---

## Instructor Notes
- **Words not yet earned — avoid using without defining:** "pivot_table," "multi-level index," "transform() vs apply()." These are more advanced Pandas patterns worth flagging as "coming later" but not taught today.
- **Biggest risk this session:** the inner-merge silent-drop behavior in Block 3 is the highest-stakes trap in the entire module so far, because it produces no error — spend extra time letting students predict Meera's fate in each merge type before revealing the answer.
- **Board management:** Keep the three merge-type table (inner/left/right) from the pre-read visible throughout Block 3, updating it live with the outer merge type once introduced in Q&A.
- **Common confusions, numbered:**
  1. Calling `groupby().sum()` without specifying a column, summing irrelevant numeric columns.
  2. Using `dropna()` without checking how many rows it actually removes first.
  3. Confusing `concat()` (stacking similar tables) with `merge()` (combining related tables by key).
- **Cross-references to later sessions:** groupby is the direct Pandas equivalent of SQL's `GROUP BY`/`HAVING` (Session 7.1); merge is the direct equivalent of SQL JOINs (also Session 7.1) — flag this connection explicitly, since seeing the same concept in two tools cements it; missing-value handling resurfaces as a core EDA checklist item (Session 6.3).
- **Local/cultural context notes:** The kirana shop receipt-sorting, hostel room allocation list, and monthly sales ledger analogies continue the running thread — the customer/order merge example deliberately echoes the nested customer-orders JSON structure from Session 4.1 for continuity.
