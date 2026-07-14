# Lecture Script: Formulas for Analysis
> **Instructor Reference** — Module 1: Analytics Foundations + GenAI + Spreadsheets | Academic Session 6 | Duration: 1.5 Hours | Instructor: Industry Mentor

---

## Session Overview

**Goal:** Students can compute descriptive statistics with formulas, use `COUNTIF`/`SUMIF` to answer conditional business questions, build calculated columns, and avoid the `$`-reference bug.

**Student profile at this point:** They have a **clean, validated dataset** they built themselves over two sessions. They are more than ready to finally *compute* something. Many have used `=SUM()` before, but almost none have used `SUMIF`, and almost none understand `$`.

**Key outcome:** Students leave understanding that `SUMIF` is **`GROUP BY` in disguise** — planting the seed that Module 2's SQL and Module 4's pandas are the same thought in different clothes.

> 🎯 **The one sentence this session must land:** *"Group the rows by something, then compute per group" is the most common operation in all of data work — you just met it for the first time, and you'll meet it in every tool for the rest of your career.*

---

## Setup Required

> ⚙️ **Use the CLEANED dataset the students produced in Session 5** — with the validation row still at the top. The continuity is the reward for two sessions of cleaning; do not hand them a fresh file.

**If some students' files are broken,** keep a "known-good" cleaned version ready to distribute so nobody is locked out of the practicals.

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| Opening & Hook — Now the Number Is True | 5 min | 0:05 |
| **Concept 1:** What a Formula Actually Is | 8 min | 0:13 |
| **Concept 2:** The Five Workhorses + the Mean/Median Habit | 12 min | 0:25 |
| **Practical 1:** Descriptive stats — and find the skew | 10 min | 0:35 |
| **Concept 3:** COUNTIF & SUMIF — the condition changes everything | 14 min | 0:49 |
| **BREAK** | 5 min | 0:54 |
| **Practical 2:** Build a city KPI table with SUMIF | 12 min | 1:06 |
| **Concept 4:** Calculated Columns + the `$` Bug | 12 min | 1:18 |
| **Practical 3:** Delivery days, late flag, % of total | 8 min | 1:26 |
| Summary & Bridge to Session 7 | 4 min | 1:30 |

---

## Opening — Now the Number Is True (5 min)

**Open the cleaned file. Point at the validation row.**

> *"Two sessions ago this file was a disaster. Last session you fixed it, and you put that validation row at the top to prove it. **Look at it. Everything says TRUE, everything says zero.**"*

Now type, live:

```
=SUM(E2:E40)      →   ₹83,200
```

> *"Session 5, this same formula told us ₹71,400. **It was lying — it was silently skipping five orders.** Today it says ₹83,200."*
>
> *"Nothing about the formula changed. **What changed is that you can now trust it.** That's what those two sessions bought you. And it's why I made you suffer through them."*

**Frame the session:**

> *"Today you finally get to compute. And I want to warn you: the functions themselves are easy. `SUM`. `AVERAGE`. **You will not struggle with the syntax.**"*
>
> *"What you'll struggle with — and what actually matters — is two things: **choosing which number is honest** *(and Session 1 is about to come roaring back)*, and one idea called `SUMIF` that is quietly the most important thing in this entire module. **You'll see it again as SQL. You'll see it again as Python. Learn it properly today and you get it three times for free.**"*

---

## Concept Block 1: What a Formula Actually Is (8 min)

### The standing instruction (3 min)

> *"A calculator gives you an answer and forgets you existed. **A formula is a standing instruction:** 'however this data changes, keep computing this, forever.' It's the difference between doing a sum once, and **hiring someone to do it for the rest of time.**"*

**Anatomy — on the board:**

```
=SUM(E2:E40)
│  │    │
│  │    └── the RANGE — which cells
│  └─────── the FUNCTION — what to do with them
└────────── the EQUALS SIGN — "this is an instruction, not text"
```

> *"Forget the `=` and the spreadsheet stores it as **text**. You'll literally see the letters `SUM(E2:E40)` sitting in the cell, doing nothing at all. **Everyone does this once.** Do it today, in here, where it's free."*

### The live-link — demo it (3 min)

```
=SUM(E2:E4)   →  9,400

Now change E2 from 2400 to 3400.

=SUM(E2:E4)   →  10,400     ← it updated ITSELF
```

> *"You didn't touch the formula. It re-fired on its own."*

### Why this makes cleaning matter (2 min)

> 🔑 *"Now think about what that means. Your formulas are **live**. They sit on top of your data and re-compute forever."*
>
> ### **Clean data + live formulas = a report that stays true.**
> ### **Dirty data + live formulas = a report that stays WRONG — automatically, at scale, forever.**
>
> *"That's the whole argument for Sessions 4 and 5, in one line. **A live formula on dirty data doesn't make one mistake. It makes the same mistake every single day, cheerfully, until someone notices.**"*

---

## Concept Block 2: The Five Workhorses + the Mean/Median Habit (12 min)

### The functions (4 min) — move fast, this is the easy part

| Function | Does | Example |
|---|---|---|
| `=SUM` | Adds up | `=SUM(E2:E40)` → total revenue |
| `=AVERAGE` | The **mean** | `=AVERAGE(E2:E40)` → average order value |
| `=COUNT` | Counts **numbers only** | Your data-quality check from Session 5! |
| `=COUNTA` | Counts **all non-empty** | Ditto |
| `=MIN` / `=MAX` | Smallest / largest | `=MAX(E2:E40)` → biggest order |
| `=MEDIAN` | The middle value | 👀 **Session 1** |

> *"`COUNT` and `COUNTA` — you've already met these as a **data-quality check**. Same functions. **Now you're using them to actually analyse.** Notice how the toolkit compounds."*

### 🎯 The Session 1 callback — this is the heart of the session (8 min)

**Type both, side by side, live:**

```
=AVERAGE(E2:E40)   →   ₹4,850
=MEDIAN(E2:E40)    →   ₹2,100
```

**Stop. Let them look at it.**

> *"₹4,850 and ₹2,100. These are the same column. **Which one is the honest number?**"*

Take answers. Then:

> *"The mean says a typical order is ₹4,850. But look at your data — **most of your orders are between ₹800 and ₹3,000.** Almost nothing is near ₹4,850. So what's dragging it up?"*

Sort by `order_value` descending. Show the ₹9,99,999-type order.

> *"**One order.** One wholesale customer, one data-entry error, one Diwali bulk purchase. **And it has hijacked the mean of the entire dataset.**"*
>
> *"That's the café. That's the billionaire walking in. **Session 1 wasn't a warm-up — it was this.**"*

**Now the habit — make them write it down:**

> # 🔑 **Compute the MEAN and the MEDIAN side by side. Every single time.**
>
> ### **Close together?** → Data is well-behaved. The mean is safe.
> ### **Far apart?** → You have skew or outliers. **Go and look.**

> *"Two formulas. Five seconds. **It is the cheapest, fastest diagnostic in all of analytics — and I promise you, almost nobody in the industry actually does it.** Be the person who does. It will make you look like you can see through walls."*

---

## Practical Block 1: Descriptive Stats — And Find the Skew (10 min)

**Hands-on. Everyone builds a summary block on their cleaned sheet.**

```
Build this, in empty cells to the right:

    Total revenue        =SUM(E2:E40)
    Order count          =COUNT(E2:E40)
    Average order        =AVERAGE(E2:E40)
    Median order         =MEDIAN(E2:E40)     ← the truth-teller
    Largest order        =MAX(E2:E40)
    Smallest order       =MIN(E2:E40)
```

**Then, together:**

1. *"Is your mean far from your median? By how much?"*
2. *"Sort descending by order_value. **Which specific rows are causing the gap?**"*
3. *"Now the analyst's question: **is that big order real, or is it an error?**"*

> 💬 **Push them on #3.** *"If it's a genuine wholesale order — **keep it**, report the median as typical, and report that order **separately**, because it might be the most interesting row in the file. If it's a typo — fix it. **What you must never do is delete it because it's inconvenient. Remember Session 4: that's not analysis.**"*

**Sanity check to close the block:**

```
=COUNT(E2:E40)  should equal  =COUNTA(E2:E40)
```

> *"Still equal? Good — your data's still clean. **Your validation habit is doing its job.**"*

---

## Concept Block 3: COUNTIF & SUMIF — The Condition Changes Everything (14 min)

### The basket (2 min)

> *"`SUM` says: **add up everything in the basket.**"*
> *"`SUMIF` says: **add up only the vegetables.**"*
>
> *"That one word — **only** — is what turns arithmetic into analysis. Everything before this moment was counting. Everything after it is asking questions."*

### The syntax (4 min) — go slowly, this confuses everyone

```
=COUNTIF( range_to_check , condition )

=SUMIF( range_to_check , condition , range_to_add )
```

**Read `SUMIF` in plain English on the board:**

```
=SUMIF( C2:C40 , "Chennai" , E2:E40 )
          │          │           │
          │          │           └── ...then ADD UP the matching rows from HERE
          │          └────────────── ...that equal "Chennai"...
          └───────────────────────── LOOK in this column for rows...
```

> *"Three arguments: **where to look, what to look for, what to add up.** Say it that way in your head every time and you'll never get the order wrong."*

### The examples (3 min) — build these live, ask the room for each

| Business question | Formula |
|---|---|
| How many orders from Chennai? | `=COUNTIF(C2:C40, "Chennai")` |
| **Chennai's total revenue?** | `=SUMIF(C2:C40, "Chennai", E2:E40)` |
| Orders over ₹5,000? | `=COUNTIF(E2:E40, ">5000")` |
| Revenue from **completed** orders only? | `=SUMIF(I2:I40, "completed", E2:E40)` |

> 💡 **Point out the quotes on `">5000"`:** *"The condition is a **text string**, even when it's about numbers. Yes, that's weird. Yes, everybody forgets the quotes. **It's just how it is.**"*

### 🔑 The big reveal (5 min) — the most important five minutes of Module 1

**Stop everything. Write this on the board:**

```
=SUMIF(C2:C40, "Chennai",    E2:E40)   →  ₹41,200
=SUMIF(C2:C40, "Madurai",    E2:E40)   →  ₹22,000
=SUMIF(C2:C40, "Coimbatore", E2:E40)   →  ₹20,000
```

> *"Look at what you just built. **Revenue, per city.** You took forty scattered rows and you produced one number per group."*

Pause.

> *"Now let me show you something. This is a SQL query. You have never written SQL. You will not write SQL until Session 9. **Just look at it.**"*

Write underneath, deliberately:

```sql
SELECT city, SUM(order_value)
FROM orders
GROUP BY city
```

> *"**That is the identical operation.** 'Look in the city column, group the rows, sum the order values per group.' **You just did it with SUMIF. That's GROUP BY — the single most important operation in SQL — and you already understand it.**"*
>
> *"And in Module 4 you'll write `df.groupby('city')['order_value'].sum()` in Python. **Same thought. Third costume.**"*

> ### 🎯 **The line to land:**
> ### ***"Group the rows by something, then compute per group."***
> ### **That is the most common operation in all of data work.**
>
> *"When you get to Session 12 and someone says 'now we'll learn GROUP BY,' I want you to feel **bored**. I want you to think: *oh, that's just SUMIF with better syntax.* **That feeling is the entire point of this module.**"*

### Multi-condition, quickly (1 min)

```
=SUMIFS(E2:E40, C2:C40, "Chennai", I2:I40, "completed")
```

> ⚠️ *"One landmine: **`SUMIF` puts the sum-range LAST. `SUMIFS` puts it FIRST.** There is no logic to this. It is an accident of history. Just know it, because it will bite you."*

---

## BREAK (5 min)

> *"Before you go — you just computed revenue for three cities with three SUMIF formulas. **Now imagine you have 50 cities. And you want revenue, order count, AND average — for each one.**"*
>
> *"**That's 150 formulas.** How do you feel about that? Hold that feeling. It's the reason next session exists."*

---

## Practical Block 2: Build a City KPI Table with SUMIF (12 min)

**Hands-on. This is the block where it all comes together.**

```
Build this table with formulas:

    City          Orders                              Revenue                                    Avg Order
    ─────────────────────────────────────────────────────────────────────────────────────────────────────
    Chennai       =COUNTIF($C$2:$C$40, H2)            =SUMIF($C$2:$C$40, H2, $E$2:$E$40)         =I2/... 
    Madurai       (drag down)                         (drag down)                                (drag down)
    Coimbatore
```

> ⚠️ **Do NOT explain the `$` yet.** Let them try it without, hit the bug, and *then* teach it. **A bug they created themselves teaches ten times better than a warning you gave them.**

**What will happen:** students who write `=COUNTIF(C2:C40, H2)` and drag down will see the range slide to `C3:C41`, `C4:C42`… and their numbers will be subtly, quietly wrong.

**When someone notices — and someone will:**

> *"Excellent. **You've found the single most common bug in spreadsheets.** Hold that thought — it's the next concept, and it's about to make total sense."*

**Then bring it to the KPI callback:**

> *"Now look at what you've built. **This is a KPI table.** Session 2 — remember? Metric plus formula plus timeframe plus target."*
>
> *"You have the metric and the formula right there. **Add one more column: a target.** What's a reasonable target for average order value? Now you have a real KPI table — and it updates itself the moment new data arrives."*

---

## Concept Block 4: Calculated Columns + the `$` Bug (12 min)

### Calculated columns — new information from old (5 min)

> *"You have height. You have weight. Neither tells you much. **Divide one by the other and you get BMI** — a genuinely new fact that was hiding inside data you already had. **That's a calculated column.**"*

| New column | Formula | What it gives you |
|---|---|---|
| **Delivery days** | `=D2 - C2` | Two dates become a **performance metric** |
| **Value band** | `=IF(E2>5000, "High", "Low")` | A number becomes a **category** |
| **Is late?** | `=IF(F2>3, "LATE", "On time")` | A number becomes a **KPI breach flag** |
| **% of total** | `=E2/SUM($E$2:$E$40)` | Each order's **share of revenue** |

> 🔑 **Point at the `IF` rows:** *"Look at what `IF` does — it converts a **numerical** column into a **categorical** one. Session 1! And why do you want categories? **Because categories are what you group by.** Which means you can now SUMIF on a band you invented. **You are creating the very thing you'll analyse.**"*

### 💥 The `$` bug (7 min) — call back to the block they just lived through

> *"Right. Let's fix what half of you just hit."*

**The failure, on the board:**

```
You want each order's % of total revenue.

F2:  =E2 / SUM(E2:E40)        ← looks completely reasonable!

Drag it down... and watch it rot:

F3:  =E3 / SUM(E3:E40)        ← the total SHRANK
F4:  =E4 / SUM(E4:E40)        ← shrank again
F40: =E40 / SUM(E40:E40)      ← dividing by itself → 100% !
```

> *"Every percentage is wrong. And they get **more** wrong as you go down. **The last row confidently reports 100%.** And notice — no error message. **It just quietly hands you nonsense.** Where have we seen that before? Everywhere. Every session. **This is the theme of your career.**"*

**The address analogy:**

> *"'The house three doors down' is a **relative** address — it means something different depending on where you're standing. '14 Anna Salai' is an **absolute** address — it means the same thing from anywhere in the world."*
>
> *"Spreadsheets have both. **`E2` is 'three doors down.' `$E$2` is '14 Anna Salai.'**"*

**The fix:**

```
F2:  =E2 / SUM($E$2:$E$40)      ← the $ pins the range

F3:  =E3 / SUM($E$2:$E$40)      ← total stays put ✅
F4:  =E4 / SUM($E$2:$E$40)      ← ✅
```

> ### 🔑 **The rule:** *Pointing at a **fixed thing** (a total, a rate, a target)? **Lock it with `$`.** Pointing at **"this row's value"**? Leave it relative.*

> 💡 *"Shortcut: click the reference in the formula bar and hit **F4** (Windows) or **⌘+T** (Mac). It cycles through the lock modes."*

---

## Practical Block 3: Delivery Days, Late Flag, % of Total (8 min)

**Hands-on. Three columns. This pulls everything together.**

```
1.  delivery_days   =D2 - C2
                    → If this errors, your dates are TEXT. (Session 5!)

2.  is_late         =IF(F2 > 3, "LATE", "On time")

3.  pct_of_total    =E2 / SUM($E$2:$E$40)      ← LOCK IT
                    Format as %.
```

**Then the payoff — compute the KPI:**

```
    % of orders late    =COUNTIF(G2:G40, "LATE") / COUNTA(G2:G40)
```

> 🎯 *"**Look at what you just did.** You had two raw date columns. Nobody could have answered 'what percentage of our orders are late?' from those. **Now you can — and it recomputes itself forever, the moment new orders arrive.**"*
>
> *"And it's a real KPI: metric, formula, timeframe, and — if you add a target cell — a threshold. **Session 2, alive on your screen.**"*

**Sanity check to close:**

```
=SUM(H2:H40)   →  should be 100%   (your % of total column)
```

> *"If it isn't 100%, **you forgot a `$`.** Go find it."*

---

## Summary & Bridge (4 min)

**What we covered:**

| Concept | The one thing to remember |
|---|---|
| **Formula** | A **live** standing instruction. Clean data + live formulas = a report that stays true. |
| **The workhorses** | SUM · AVERAGE · COUNT · MIN · MAX · MEDIAN |
| **The habit** | 🔑 **Mean and median, side by side, every time.** Far apart = skew. Go look. |
| **COUNTIF / SUMIF** | 🔴 **This is `GROUP BY` in disguise.** *"Group the rows, compute per group."* |
| **Calculated columns** | Create new information. `IF` turns numbers into **categories you can group by**. |
| **`$` absolute refs** | Pointing at a **fixed thing** → lock it. **The bug everyone hits exactly once.** |

**Close on the big idea:**

> *"One thing from today outlives all the others. Not `SUM`. Not `$`."*
>
> ### ***"Group the rows by something, then compute per group."***
>
> *"That's `SUMIF` today. It's `GROUP BY` in Session 12. It's `.groupby()` in Session 35. **Three tools, three syntaxes, one idea — and you learned the idea today, in a spreadsheet, with no code.** When SQL arrives and it feels easy, you'll know why."*

**Bridge to Session 7:**

> *"Before the break I asked how you'd feel about writing 150 formulas for 50 cities. **Badly. You'd feel badly.**"*
>
> *"**Next session: Pivot Tables.** Everything you did with SUMIF today — every city, every metric, all at once — **with zero formulas and about four mouse clicks.** It is the single highest-leverage tool in a spreadsheet, and it closes out Module 1."*
>
> *"And then, Module 2: **SQL.** Where 'group the rows and compute per group' becomes the thing you do all day."*

---

## Instructor Notes

- **The SUMIF → GROUP BY reveal is the most important five minutes of Module 1.** Do not rush it, and do not skip writing the SQL on the board. Students will not understand the SQL syntax — **that's fine and intended.** The goal is recognition later, not comprehension now. When SQL arrives in Session 12, you want them to feel *"oh — I know this."*
- **Let them hit the `$` bug in Practical 2 before you explain it.** This is deliberate. Teaching `$` cold is abstract and forgettable; teaching it 30 seconds after their own numbers came out wrong is permanent.
- **The mean/median side-by-side habit is the single most transferable thing in this session.** Sell it hard. It costs five seconds and it makes a student look like they can see through walls.
- **Callback density is high and intentional** — S1 (mean vs median, numerical vs categorical), S2 (KPI table with a target), S4 (don't delete inconvenient outliers), S5 (COUNT vs COUNTA, dates as text). **This session is where students first feel the course as one thing rather than seven.** Voice every callback out loud.
- **Common confusion #1:** `SUMIF` argument order. Drill the plain-English reading: *"look here, for this, add that."*
- **Common confusion #2:** `SUMIF` vs `SUMIFS` range order flip. There is no logic. Tell them so — students waste time hunting for a rule that doesn't exist.
- **Common confusion #3:** Forgetting quotes around numeric conditions (`">5000"`). Point it out once, expect it anyway.
- **Common confusion #4:** `=D2-C2` on dates throwing an error → their dates are still text. Great moment to reinforce Session 5's date test.
- **No coding question for this session** — spreadsheet-based, per course design. The practicals are the assessment. *A good homework artefact: the city KPI table with a target column, plus a written one-line answer to "is the mean or the median the honest number for this dataset, and why?"*
