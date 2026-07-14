# Lecture Script: Clean Up the Data
> **Instructor Reference** — Module 1: Analytics Foundations + GenAI + Spreadsheets | Academic Session 4 | Duration: 1.5 Hours | Instructor: Industry Mentor

---

## Session Overview

**Goal:** Students can load a messy CSV without corrupting it, run a systematic 5-point audit to find every problem, remove duplicates using the correct unique key, and justify every row they deleted.

**Student profile at this point:** They have three sessions of *concepts* and **zero hands-on tool time.** They are itching to touch something. Some are quietly worried the course is all theory. **This session is the payoff — make it feel like one.**

**Key outcome:** Students leave having personally found a duplicate that was inflating revenue, and having personally destroyed a pin code by importing it wrong — so that both lessons are earned, not told.

> 🎯 **The one sentence this session must land:** *Cleaning is not the boring part before the real work — it IS the work, and every number you will ever report depends on it.*

---

## Setup Required — Read Before Class

> ⚙️ **You must prepare a deliberately dirty dataset before this session.** Everything below depends on it.

**Create `messy_orders.csv` (~40 rows) containing, on purpose:**

| Planted issue | How to plant it |
|---|---|
| **Exact duplicates** | Copy 3 complete rows verbatim (same `order_id`) |
| **Repeat customers** | One customer (`Ravi Kumar`) with **6 different orders** — *not* duplicates. **This is the trap.** |
| **Inconsistent city spelling** | `Chennai`, `chennai`, `CHENNAI`, `Chennai ` (trailing space) |
| **Missing values** | 5 blank `order_value`, 4 blank `rating`, 8 blank `delivery_date` (some legitimately cancelled) |
| **Currency as text** | A few values as `₹2,400` and `2,400` instead of `2400` |
| **Mixed date formats** | `2025-03-01`, `01/03/2025`, `March 1, 2025` |
| **Impossible values** | One `order_value = -500`, one `= 9999999`, one `rating = 0` (vs blank) |
| **Leading-zero column** | A `store_code` column with values like `007`, `012` |

**Columns:** `order_id, customer_name, city, store_code, order_value, order_date, delivery_date, rating, status`

**Tool:** Google Sheets (recommended — nothing to install, easy to share) or Excel. Have the file shareable via link.

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| Opening & Hook — The ₹4 Lakh Mistake | 6 min | 0:06 |
| **Concept 1:** Loading Data Without Corrupting It | 10 min | 0:16 |
| **Practical 1:** Load the file — and break it on purpose | 10 min | 0:26 |
| **Concept 2:** The 5-Point Audit | 8 min | 0:34 |
| **Practical 2:** Sort & Filter — hunt the problems | 14 min | 0:48 |
| **BREAK** | 5 min | 0:53 |
| **Concept 3:** Missing Values — Not All Absences Are Equal | 10 min | 1:03 |
| **Concept 4:** Duplicates — The Silent Revenue Inflator | 10 min | 1:13 |
| **Practical 3:** De-duplicate (and fall into the trap) | 12 min | 1:25 |
| Summary & Bridge to Session 5 | 5 min | 1:30 |

---

## Opening — The ₹4 Lakh Mistake (6 min)

**Put this on the board before you say anything:**

```
An analyst reports:   Q3 Revenue = ₹48,20,000   ✅ Up 9% !!

The real number is:   Q3 Revenue = ₹44,10,000   ❌ Down 0.2%

The difference:       ₹4,10,000  —  from 47 duplicated rows.
```

> *"This analyst did nothing wrong with their maths. Their formula was perfect. Their chart was beautiful. They presented growth to a board that then approved a hiring plan based on it."*
>
> *"Six weeks later, finance reconciled the numbers and found the duplicates. **Every decision made on that number had to be unwound.**"*

**Now the question that sets up the session:**

> *"Here's what I want you to notice. **Duplicates made the number look GOOD.** Revenue up! Orders up! **Who questions good news?**"*
>
> *"A missing value makes a number look obviously wrong — you notice, you fix it. A duplicate makes it look great. That's why duplicates get caught late, in front of important people, or never at all."*

**Frame the session:**

> *"For three sessions you've had no tools and you've been very patient. **Today you open a spreadsheet.** And within ten minutes you'll find out that real data is nothing like the tidy examples in a textbook — it's filthy, and it's filthy in the same five ways every single time. By the end of today you'll have a checklist that catches all five."*

> 💬 **Expect the question:** *"Isn't cleaning the boring bit before the real work?"* Answer it head-on and early:
>
> *"Analysts spend the majority of their working lives cleaning data. If you think that's the boring part, you've misunderstood the job. **Cleaning IS the job.** Everything else — the dashboard, the model, the insight — is what happens in the last hour, on top of the foundation you spent all week building. And if the foundation is rotten, the beautiful thing on top of it is worse than useless: it's confidently wrong."*

---

## Concept Block 1: Loading Data Without Corrupting It (10 min)

### What a CSV actually is (3 min)

> *"Before we open anything — what IS a CSV? It's the most common data file in the world and most people have never looked inside one."*

Show it as raw text:

```
order_id,customer_name,city,order_value
1001,Ravi Kumar,Chennai,2400
1002,Priya S,Madurai,1800
```

> *"That's it. Plain text. Commas separate the columns, new lines separate the rows. **No formatting, no formulas, no colours.** When you open this in Excel and it appears in neat columns, Excel is *interpreting* it for you — and that interpretation is exactly where things go wrong."*

### The three traps (5 min) — this is the block

| Trap | What happens | Prevention |
|---|---|---|
| **Leading zeros vanish** | `007` → `7` | Import that column **as TEXT** |
| **Dates get rewritten** | `03-04-2025` → April 3rd… **or March 4th.** The spreadsheet *guesses*. | Set the date format explicitly |
| **Long numbers → scientific notation** | `9876543210` → `9.88E+09` | Import **as TEXT** |

**Stop on the date one. This is the most costly and least understood:**

> *"`03-04-2025`. Is that the 3rd of April, or the 4th of March? **You cannot tell.** And here's the thing — **neither can Excel.** So it guesses, based on your computer's regional settings."*
>
> *"Which means: **the same file, opened on two different laptops, can produce two different datasets.** I have watched two analysts on the same team present conflicting numbers from the identical file for exactly this reason."*

> 🔴 **The line to land:** *"These are not display quirks. **The underlying value is genuinely changed and it is not recoverable.** Once `007` becomes `7`, the zeros are gone. You cannot get them back by re-formatting the cell. You have to go get the file again."*

### The habit (2 min)

> ### 👀 **After loading, LOOK at the first 20 rows with your own eyes. Before anything else.**
>
> *"Ten seconds. That's the whole habit. It will save you hours, and it will save you at least one meeting you'd rather not have."*

---

## Practical Block 1: Load the File — And Break It On Purpose (10 min)

**Everyone opens `messy_orders.csv` in Google Sheets.**

### Step 1 — The naive import (3 min)

> *"Just open it. Don't do anything clever. File → Import → Replace spreadsheet."*

**Then, immediately:**

> *"Everyone look at the `store_code` column. Read me what you see."*

They'll see `7`, `12`, `3` — where the file contained `007`, `012`, `003`.

> *"**You have just destroyed data, and it took you four seconds and zero effort.** Those are store codes. Store `007` and store `7` are not the same store — and now nobody can tell which is which. If you joined this to another table on store code, you'd match nothing."*

### Step 2 — Do it properly (4 min)

**Walk them through it live:**

```
Google Sheets:  File → Import → Upload
                → "Convert text to numbers, dates, and formulas" → NO
                → Then set specific columns to Number/Date deliberately

Excel:          Data → From Text/CSV → Transform Data
                → set store_code = Text, order_date = Date (specify the format!)
```

> *"Notice what you just did: **you stopped the spreadsheet from being clever.** That's the entire skill. The default behaviour of every spreadsheet is to guess, and its guesses are optimised for convenience, not correctness."*

### Step 3 — Eyes on the data (3 min)

> *"Now, before we do ANYTHING — everybody read the first 20 rows. Out loud, to yourself. What do you notice?"*

**Let them find things. They will call out:**
- *"The cities are spelled differently!"*
- *"Some order values have a rupee sign"*
- *"There are blank cells"*
- *"There's a negative order value"*

> *"Perfect. **You just did an audit — but you did it by accident, by noticing.** Noticing doesn't scale to 50,000 rows. So let's turn what you just did into a system."*

---

## Concept Block 2: The 5-Point Audit (8 min)

### The doctor analogy

> *"A doctor doesn't examine you randomly — pulse, blood pressure, temperature, every time, in order. **Because if you only look for what you happen to notice, you only find what's obvious.** And the problems that hurt you are the ones that aren't."*

### The five — write these on the board, leave them up

| # | Issue | Looks like | Why it breaks your analysis |
|---|---|---|---|
| **1** | **Missing values** | Empty cells, `NA`, `-` | Averages wrong; rows vanish from counts |
| **2** | **Duplicates** | The same order twice | 🔴 **Revenue overstated. You report money that doesn't exist.** |
| **3** | **Formatting issues** | `₹2,400` vs `2400` | It's **text**, not a number — *you cannot sum it* |
| **4** | **Inconsistent entries** | `Chennai` / `chennai` / `CHENNAI` | One city becomes four; every group-by is wrong |
| **5** | **Impossible values** | `age = 999`, `order_value = -500` | Mean destroyed — **remember Session 1** |

**Callback to Session 1 on #5:**

> *"Remember the café, and the billionaire? One value of −500, or one of 99,99,999, and your mean is describing a business that doesn't exist. **The outlier lesson wasn't theory — this is where it bites.**"*

**Demonstrate #3 live — it's the one they underestimate:**

> *"Watch. I'll type `=SUM()` over the order_value column."*

The `₹2,400` cells are silently ignored — text isn't summed.

> *"No error. No warning. **The total is just quietly wrong.** That's Excel's most dangerous behaviour: it doesn't tell you it skipped something. It just gives you a smaller number, with total confidence. Sound familiar? **It's exactly what GenAI did to you last session.**"*

---

## Practical Block 2: Sort & Filter — Hunt the Problems (14 min)

**Format:** Everyone hands-on. You call the moves; they execute and report what they find.

### The key idea — say it first (2 min)

> ### 🔑 **Sorting a column makes the broken values sit next to each other.**
>
> *"Problems that are invisible when scattered across 5,000 rows become obvious when they're neighbours. This is the highest-value trick in the whole session."*

### The hunt (10 min) — run these one at a time, together

| # | The move | What the class will find |
|---|---|---|
| **1** | Sort `order_value` **ascending** | The `-500`. All the blanks. **They all cluster at the top.** |
| **2** | Sort `order_value` **descending** | The `9999999`. *"Is that real, or a typo for 999?"* |
| **3** | Sort `city` **A → Z** | `CHENNAI`, `Chennai`, `Chennai `, `chennai` — **all adjacent.** |
| **4** | Filter `order_value` **is empty** | Count them. *"5 rows. Now: WHY are they empty?"* |
| **5** | Sort `order_date` ascending | The mixed formats sort nonsensically — **text dates don't sort as dates** |
| **6** | Filter `city` = "Chennai" | **The count is too low!** *"Where did the rest go?"* → the other spellings |

**Stop on #3 and let it land:**

> *"Look at your screen. `CHENNAI`, `Chennai`, `Chennai-with-a-space`, `chennai`. To you, one city. To the spreadsheet, **four completely different cities.** If you ran a group-by right now — and in Session 7 you will — you'd get four rows for Chennai, each with a fraction of the revenue, and your Chennai number would be wrong by 75%."*
>
> *"And the trailing space one? **`Chennai ` looks identical to `Chennai` on screen.** You cannot see it. Sorting is how you catch what you cannot see."*

**Stop on #6 — the punchline:**

> *"Your filter says Chennai has 12 orders. But you know from the sort that there are four spellings. **The filter is lying to you — and it's lying by telling you the exact truth about a broken column.**"*

### Sort/filter are safe (2 min)

> *"One reassurance: **sorting and filtering never change your data.** They change what you can see. So explore fearlessly. It's *deleting* that requires a reason — and that's next."*

---

## BREAK (5 min)

> *"A question for the break. In our data, `Ravi Kumar` appears in **six rows**. Is that six duplicates that need deleting? Think carefully. We'll settle it in five minutes — and getting this wrong is how people delete their best customers."*

---

## Concept Block 3: Missing Values — Not All Absences Are Equal (10 min)

### The form analogy (2 min)

> *"A blank on a form can mean three different things: **'I have no phone'**, **'I'd rather not say'**, or **'I didn't see the question.'** Treating all three identically throws away real information."*

### The three causes (3 min)

| Why it's missing | Example in our data | What to do |
|---|---|---|
| **Genuinely doesn't exist** | `delivery_date` blank for a **cancelled** order | ✅ **Leave it.** It's correct — there was no delivery. |
| **Never recorded** | `rating` — the customer just didn't rate | ⚠️ Leave blank. It is *not* zero. |
| **Lost or broken** | `order_value` blank on a completed order | 🔴 **Investigate.** This is a real problem. |

> *"Look at our dataset. Some `delivery_date` blanks are on cancelled orders — **those blanks are correct and you must not touch them.** Others are on delivered orders — **those are broken.** Same blank cell. Completely different meaning. **The only way to tell is to look at the `status` column.** That's what 'understand why it's missing' actually means in practice."*

### 🚨 The `0` trap (4 min) — this is the block's whole point

Write on the board:

```
rating = [blank]   →  the customer did not rate
rating = 0         →  the customer rated us ZERO
```

> *"These are completely different facts about the world."*

**Now the disaster, live:**

> *"Watch what happens if I 'clean' this column by filling blanks with zero."*

Do it. Show the average rating collapse (e.g. 4.3 → 3.1).

> *"I have just told the business that customers hate us. **I invented that.** Not one customer gave us a zero. I converted 'no opinion' into 'worst possible score' — and I did it while believing I was tidying up."*

> 🔴 **And the same trap in reverse:** *"If you fill a blank `order_value` with 0, you've recorded a real sale as ₹0. **You just deleted revenue while cleaning.**"*

### The rule (1 min)

> ### 🔑 **Understand WHY it's missing before you decide what to do about it.**
> ### **Never delete a row you haven't looked at.**

---

## Concept Block 4: Duplicates — The Silent Revenue Inflator (10 min)

### Settle the break question first (3 min)

> *"So: `Ravi Kumar` appears six times. Duplicates?"*

Take a show of hands. **Some will say yes.** That's the moment.

> *"Let's look."*

Put the rows up:

```
1001, Ravi Kumar, Chennai, 2400, 2025-03-01
1005, Ravi Kumar, Chennai, 1800, 2025-03-09
1012, Ravi Kumar, Chennai, 3200, 2025-03-15
...
```

> *"**Different order IDs. Different dates. Different amounts.** These are six separate orders from one customer. He's not a duplicate — **he's your best customer.** He's exactly the person you want more of."*
>
> *"If you had de-duplicated on `customer_name`, you would have deleted five real orders, wiped out ₹9,000 of genuine revenue, and — worse — **erased the single most valuable pattern in your dataset: loyalty.** Repeat customers appear many times. **That's what loyalty looks like in a table.**"*

### Exact vs partial (3 min)

```
DUPLICATE — every column identical:
  1001, Ravi Kumar, Chennai, 2400, 2025-03-01
  1001, Ravi Kumar, Chennai, 2400, 2025-03-01     ← same order_id. Delete one.

NOT A DUPLICATE:
  1001, Ravi Kumar, Chennai, 2400, 2025-03-01
  1005, Ravi Kumar, Chennai, 1800, 2025-03-09     ← different order. KEEP BOTH.
```

### The unique key (4 min) — the concept that actually protects them

> ### ❓ **Ask one question before you de-duplicate anything:**
> ### *"Which column SHOULD be unique in this table?"*

| Table | Unique key | So a duplicate is… |
|---|---|---|
| **Orders** | `order_id` | The same `order_id` on two rows |
| **Customers** | `customer_id` | The same `customer_id` twice — *the same NAME is fine!* |
| **Products** | `sku` | The same `sku` twice |

> *"There are thousands of Ravi Kumars in Chennai. **A name is not an identity.** An ID is. Find your unique key first, then de-duplicate on it. Never on a name, never on a city, never on a date."*

> 💡 **The discipline:** *"Count your rows. Delete. Count again. **You must be able to say exactly how many rows you removed, and why.** 'I clicked Remove Duplicates and it said 47' is not an answer. Why were there 47? Was it a double-import? A system retry? **The duplicates are themselves a clue about a broken process upstream** — and telling someone about that is worth more than the cleaning."*

---

## Practical Block 3: De-duplicate — And Fall Into the Trap (12 min)

**Format:** Hands-on. **Let them make the mistake first.** This is deliberate.

### Step 1 — Set the trap (3 min)

> *"Right. Clean the duplicates out of this file. Go."*

**Say nothing else.** Some students *will* de-duplicate on `customer_name` — the tool makes it easy, and the button is right there.

**Circulate. Find someone who did it. Then, to the room:**

> *"Stop. Count your rows. Who's down to 28 rows? Who's at 37?"*

The `customer_name` de-duplicators lost far more rows.

> *"You just deleted Ravi Kumar's five other orders. **You deleted your best customer's business.** And notice — the spreadsheet let you. It didn't warn you. It said 'Removed 11 duplicate rows' and looked very pleased with itself."*

### Step 2 — Do it right (6 min)

**Together, on screen:**

```
1.  COUNT the rows first.  Write the number on your sheet.  (=COUNTA(A:A)-1)

2.  Identify the unique key:  order_id

3.  Find the real duplicates BEFORE deleting — inspect, don't just nuke:
       =COUNTIF(A:A, A2)      →  drag down. Any value > 1 is a repeated order_id.
       Sort by that column descending — the duplicates rise to the top.
       LOOK at them. Are they truly identical?

4.  Only now:  Data → Data cleanup → Remove duplicates → select ONLY order_id

5.  COUNT again.  Removed = 3.

6.  Write it down:  "Removed 3 exact duplicate rows (order_ids 1003, 1017, 1029).
                     Cause: likely a double-submit in the ordering system —
                     worth flagging to engineering."
```

> 🎯 **Point at step 6:** *"That last line is what separates an analyst from a button-clicker. **You didn't just clean the data — you diagnosed the process that dirtied it.** Any intern can click 'Remove Duplicates'. Telling the engineering team their checkout has a double-submit bug? That's the job."*

### Step 3 — Recompute (3 min)

> *"Now sum `order_value` before and after. How much revenue did the duplicates invent?"*

Let them compute the fake revenue themselves.

> *"That's your ₹4 lakh mistake from the opening. **Except you just caught it.**"*

---

## Summary & Bridge (5 min)

**The checklist — this is the takeaway artefact. Have them copy it:**

```
□  1.  Load carefully — text columns as TEXT, dates explicitly
□  2.  LOOK at the first 20 rows with your own eyes
□  3.  COUNT the rows. Write it down.
□  4.  Sort each key column ASC and DESC — extremes reveal themselves
□  5.  Sort text columns A–Z — spelling inconsistencies become neighbours
□  6.  Filter for blanks — count them, and ask WHY each one is blank
□  7.  Find the UNIQUE KEY. De-duplicate on that. Never on a name.
□  8.  COUNT again. Explain every row you removed.
```

**What we covered:**

| Concept | The one thing to remember |
|---|---|
| **Loading** | The spreadsheet *guesses*, and its guesses destroy data. Stop it from being clever. |
| **The 5 issues** | Missing · Duplicates · Formatting · Inconsistency · Impossible values |
| **Missing values** | **A blank is not a zero.** Understand *why* before you touch it. |
| **Duplicates** | 🔴 They make numbers look **good**, which is why they survive. **De-duplicate on the unique key, never on a name.** |
| **Sort & filter** | Free, safe, and they make invisible problems sit next to each other |

**Close:**

> *"Today you found a duplicate that was inflating revenue, and you destroyed a pin code by opening a file carelessly. **Both of those will happen to you again in your career — but now they'll happen where they belong: in a practice file, not in a board meeting.**"*

**Bridge to Session 5:**

> *"Right now your data is **not broken**. That is not the same as **usable**. You still have `₹2,400` sitting as text, four spellings of Chennai, and three different date formats — we *found* those today, we didn't *fix* them. **Next session: Make Data Ready for Analysis.** We standardise every column, fix every entry, and — critically — write a validation check that **proves** the data is clean, rather than just hoping it is."*

---

## Instructor Notes

- **The dirty dataset is the entire session.** If you skip preparing it, you have no class. Build it deliberately with every planted issue in the setup table — especially the **repeat-customer trap** (`Ravi Kumar` × 6), which is the emotional high point.
- **Let them make the mistakes.** Do not warn them before Practical 1 (leading zeros) or Practical 3 (de-duping on name). **A mistake they made themselves is worth ten warnings you gave them.** Both mistakes are free here and catastrophic at work.
- **This is their first tool session. Watch the energy.** After three conceptual sessions, students are hungry to *do* something. Front-load the hands-on: get them into the file within 15 minutes and keep them there.
- **Callback discipline:** Session 1 (outliers destroying the mean) at the `-500` and `9999999` values. Session 3 (GenAI failing silently) at the `=SUM()` that silently ignores text. These threads are what make the course feel like a course.
- **Common confusion #1:** *"Just delete rows with missing values."* → Ask: *"What if that's 30% of your data? Is that cleaning, or is that data loss?"*
- **Common confusion #2:** Blank = 0. The live demo of the collapsing average rating is the fix. Do it in front of them; do not describe it.
- **Common confusion #3:** They'll want to fix the `Chennai`/`chennai` problem today. **Hold them back** — that's Session 5, and the anticipation is useful. Today is *finding*; next session is *fixing*.
- **No coding question for this session** — it is spreadsheet-based, per course design. The hands-on practicals and the 8-point checklist are the assessment. *If you want a homework artefact: have them submit the cleaned file plus a written log of every row they removed and why.*
- **Local context:** Indian pin codes, ₹ values, Chennai/Madurai/Coimbatore cities, and store codes with leading zeros are all realistic for this cohort and land better than generic examples.
