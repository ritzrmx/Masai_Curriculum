# Lecture Script: SQL for Data Analysis - Aggregation Essentials
> **Instructor Reference** - Module 2: SQL for Data Analysis | Academic Session 11 | Duration: 1.5 Hours | Instructor: Industry Mentor

---

## Session Overview

**Goal:** Students can take a business question that asks for "how many," "how much," "on average," or "at the extreme," and answer it in a single query using `COUNT`, `SUM`, `AVG`, `MIN`, and `MAX` - combined correctly with `WHERE`.

**Student profile at this point:** They've completed Sessions 9–10 (SELECT, WHERE, ORDER BY, LIMIT) and can filter and rank individual rows confidently. They have **not** yet collapsed multiple rows into one summary number in SQL - everything so far has returned a list, never a single total.

**Key outcome:** Students leave able to answer, unprompted, the question every dashboard number secretly hides: *"Is this a COUNT, a SUM, or an AVG - and did I filter before or after?"*

> 🎯 **The one sentence this session must land:** *Every KPI you'll ever build a dashboard around - total revenue, order count, average order value - is just one of five functions, applied correctly.*

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| Opening - "How many cups did we actually sell today?" | 8 min | 8 min |
| Concept Block 1: COUNT | 8 min | 16 min |
| Practical Block 1: Counting rows correctly | 10 min | 26 min |
| Concept Block 2: SUM and AVG | 10 min | 36 min |
| Practical Block 2: Totals and averages on real data | 10 min | 46 min |
| **BREAK** | 5 min | 51 min |
| Concept Block 3: MIN and MAX | 8 min | 59 min |
| Practical Block 3: Extremes challenge | 8 min | 67 min |
| Concept Block 4: Aggregates + WHERE | 11 min | 78 min |
| Practical Block 4: Full business-question challenge | 12 min | 90 min |

---

## Opening - "How Many Cups Did We Actually Sell Today?" (8 min)

Walk in with no slide up. Say:

> *"You're helping a chai stall owner at closing time. She asks: 'How many cups did we sell today?' You have the full sales log - every single transaction, one row each. What do you do - read her the whole list?"*

Let the room laugh a little, then push:

> *"Obviously not. She doesn't want a list. She wants ONE number. That's the entire idea of today's session - turning a table full of rows into the one number that actually answers the question being asked."*

Write on the board, informally, without SQL yet: *"How many? How much, total? What's typical? What's the biggest/smallest?"*

> *"Every one of those four questions has its own SQL function, and by the end of today you'll reach for the right one instantly."*

**Pivot line:**

> *"By the end of ninety minutes, you'll answer 'what was our total revenue,' 'how many orders did we get,' and 'what's our average order size' - each in a single line of SQL, on a table of any size."*

**Context for the sessions ahead:** *"Every single number on a real analytics dashboard - the kind you'll build in Module 3 - comes from exactly the five functions we cover today. Learn them well now, and dashboards later will feel like plumbing you already understand, not new magic."*

---

## Concept Block 1: COUNT (8 min)

### 💬 Instructor script

> *"Simplest question first: how many rows do I have? COUNT answers that."*

```sql
SELECT COUNT(*) AS total_orders
FROM orders;
```

Walk through the output live, and introduce aliasing (`AS total_orders`) as good habit: *"Without the alias, your result column is just called count(*) - not exactly something you'd want on a report."*

### 🔴 The trap / highest-value moment

> *"Here's the trap. If Ramesh placed 2 separate orders today, and I run COUNT(*), what do I get for Ramesh - 1 or 2?"*
> Let students answer; several will say 1 ("1 customer"). Correct firmly:
> *"COUNT(*) counts ROWS, not customers, not people, not anything else - unless one row genuinely equals one of those things. You already answered this exact question back in Session 9: what does one row represent? Ask it again, every single time, before you trust a COUNT."*

---

## Practical Block 1: Counting Rows Correctly (10 min)

**Activity:** Individually, students write: (1) total number of orders in the table; (2) total number of Bengaluru orders (using WHERE, previewing Concept Block 4).

**Answer key with reasoning:** `SELECT COUNT(*) FROM orders;` and `SELECT COUNT(*) FROM orders WHERE city = 'Bengaluru';`. Say aloud: *"Notice WHERE still works exactly like Session 9 - it filters rows first. COUNT just runs on whatever's left."*

> 💬 **Expect a student to ask if COUNT(*) and COUNT(customer_name) give the same answer.** Welcome it - don't answer immediately, tell them to test it live. (They'll match here unless a name is blank - a useful preview that COUNT on a specific column skips blank/missing values, which matters again in Concept Block 2.)

---

## Concept Block 2: SUM and AVG (10 min)

### 💬 Instructor script

> *"Two more questions a manager always asks: how much, total - and what's typical? SUM answers the first. AVG answers the second."*

```sql
SELECT SUM(price) AS total_revenue, AVG(price) AS average_order_value
FROM orders;
```

Compute live on the board using `120, 150, 120, 90`: SUM = 480, AVG = 120.

> *"AVG here is the exact same mean you calculated by hand in Session 1 - the database is just doing the arithmetic for you now."*

### 🔴 The trap / highest-value moment

> *"What happens if I run SUM on the city column instead of price?"*
> Run `SELECT SUM(city) FROM orders;` live and let the error appear.
> *"SUM and AVG only work on numbers. And here's the quieter trap: if a price is missing or blank in some rows, AVG silently skips those rows rather than treating them as zero - which quietly changes what 'average' means. Before you trust any SUM or AVG, check the column the way you learned to in Module 1: is it actually clean, and is it actually numeric?"*

---

## Practical Block 2: Totals and Averages on Real Data (10 min)

**Activity:** Pairs write: (1) total revenue across all orders; (2) average quantity per order, across all orders.

**Answer key with reasoning:** `SUM(price)` and `AVG(quantity)`. Say aloud for the second: *"An average quantity of, say, 1.75 items per order doesn't mean any single real order had 1.75 items - it's a summary statistic, not a description of one row. That distinction matters when you're explaining a number to someone non-technical."*

> 💬 **Expect a pushback that a fractional average "doesn't make sense" for a countable thing like quantity.** Welcome it - it's a genuinely good instinct. Say: *"You're right that no single order has 1.75 items. The average describes the whole dataset's typical behaviour, not any one row in it - the same idea as Session 1's averages, just automated."*

---

## BREAK (5 min)

---

## Concept Block 3: MIN and MAX (8 min)

### 💬 Instructor script

> *"Last question type: what's the biggest, or the smallest? You could technically answer this with ORDER BY and LIMIT 1 from last session - but there's a more direct tool."*

```sql
SELECT MIN(price) AS cheapest_order, MAX(price) AS priciest_order
FROM orders;
```

Compute live: MIN = 90, MAX = 150.

> *"Same answer as ORDER BY price ASC LIMIT 1, but one function, one line, no sorting required."*

### 🔴 The trap / highest-value moment

> *"MIN and MAX aren't just for numbers. What do you think MIN(order_date) returns?"*
> Let students guess. Confirm: the earliest date, not a "smallest-looking" number. *"MIN and MAX work on text alphabetically and dates chronologically too. Write this down: these two functions work on any orderable data type, not just numbers."*

---

## Practical Block 3: Extremes Challenge (8 min)

**Activity:** Individually, students write: (1) the earliest order date in the table; (2) the highest quantity ordered in a single order.

**Answer key with reasoning:** `MIN(order_date)` and `MAX(quantity)`. Confirm aloud that `MIN(order_date)` correctly returns the earliest calendar date, not the numerically smallest-looking value if dates were stored oddly.

> 💬 **Expect someone to try `ORDER BY order_date LIMIT 1` instead out of habit from last session.** Welcome it - both are valid! Say: *"Both give you the right answer here. MIN is usually cleaner when you only need the single extreme value and nothing else about that row - you'll develop a feel for which to reach for."*

---

## Concept Block 4: Aggregates + WHERE (11 min)

### 💬 Instructor script

> *"Managers almost never want 'total revenue, ever.' They want 'total revenue from Bengaluru' or 'average order value last week.' That's WHERE, narrowing the rows BEFORE the aggregate ever runs."*

```sql
SELECT COUNT(*) AS bengaluru_orders, SUM(price) AS bengaluru_revenue
FROM orders
WHERE city = 'Bengaluru';
```

Walk through live: filtering happens first, then COUNT and SUM run only on what survived.

### 🔴 The trap / highest-value moment

> *"Now the trap that catches almost everyone at least once. I'm going to try to filter on a TOTAL instead of a raw row value."*
> Write `SELECT COUNT(*) FROM orders WHERE SUM(price) > 1000;` and run it live - let the error appear.
> *"This fails because WHERE filters individual ROWS, before any aggregation exists. At the moment WHERE runs, there IS no total yet - SUM(price) hasn't been calculated. Write this down: WHERE can never reference an aggregate function. If you need to filter on a total, you need a different tool - HAVING - which arrives next session alongside GROUP BY."*

---

## Practical Block 4: Full Business-Question Challenge (12 min)

**Activity:** Light competitive framing. Give the class 3–4 combined business questions (e.g., "total revenue and order count from Hyderabad," "cheapest and priciest order placed after August 1st") and have pairs race to translate and write the query.

**Answer key with reasoning:** For each, insist pairs state aloud which function(s) the question maps to before writing SQL. Example: *"'Total revenue and order count from Hyderabad' → SUM(price) and COUNT(*), filtered first with WHERE city = 'Hyderabad'."*

> 💬 **Expect at least one pair to attempt an aggregate inside WHERE again, out of habit.** Welcome it - this is exactly the mistake worth surfacing publicly. Say: *"Good - you just found the same wall the whole class hit in Concept Block 4. What's the fix?"*

---

## Summary & Bridge

**Recap table:**

| Concept | The one thing to remember |
|---|---|
| COUNT | Counts rows - confirm what one row represents before trusting the number |
| SUM / AVG | Only work on numeric columns; missing values get silently skipped by AVG |
| MIN / MAX | Work on numbers, text (alphabetical), and dates (chronological) |
| Aggregates + WHERE | WHERE filters rows first; it can never reference an aggregate result |

**Close on the thesis line:**

> *"At the start of today, you had a full sales log and no way to answer 'how many did we sell?' in one step. Now: COUNT, SUM, AVG, MIN, MAX - five functions, and every KPI you'll ever put on a dashboard is built from one of them, applied correctly, to the right filtered slice of rows."*

**Bridge to next session:**

> *"Today you aggregated the WHOLE table, or one filtered slice of it, at a time. Next session - Grouping for KPIs - you learn GROUP BY, which runs these same five functions separately for EVERY city, or EVERY item, or EVERY customer, all in a single query. Same functions you learned today. One new clause."*

---

## Q&A & Doubt Solving

**Q: Can I use more than one aggregate function in the same query?**
→ Yes - as shown today, `SELECT COUNT(*), SUM(price), AVG(price) FROM orders;` runs all three in one query, each producing its own column in the result.

**Q: What does COUNT(column_name) do differently from COUNT(*)?**
→ `COUNT(*)` counts every row regardless of content. `COUNT(column_name)` counts only rows where that specific column isn't blank/missing - a subtle but important difference when data has gaps.

**Q: Can I combine an aggregate with ORDER BY or LIMIT from last session?**
→ Not quite yet in the way you might expect - ordering and limiting *grouped* aggregate results is exactly what next session's GROUP BY unlocks. For now, a single aggregate query returns one row, so ordering/limiting isn't meaningful yet.

**Q: Why did SUM(city) error instead of just giving me something weird?**
→ SQL checks that a function's input makes sense for its data type before running - adding text values together is undefined, so it refuses rather than guessing.

**Q: Is AVG the same as the median from Session 1.1?**
→ No - AVG is always the mean (sum ÷ count), never the median. If you need the median in SQL, that requires a more advanced technique we haven't covered yet; know that "average" in SQL always defaults to mean unless stated otherwise.

---

## Instructor Notes

- **Words not yet earned:** Avoid `GROUP BY`, `HAVING`, subqueries, and window functions - GROUP BY and HAVING arrive next session specifically to fix the WHERE-can't-filter-aggregates trap taught today. If a student asks "can I get total revenue PER city?", acknowledge that's exactly next session rather than answering in full now.
- **The single biggest risk in this session** is students treating COUNT/SUM/AVG as interchangeable "give me a number" buttons without checking what they actually measure. Defeat it by repeatedly asking, across every block: *"What does one row represent, and does that match what this function is telling you?"*
- **Board management:** Keep a simple four-row reference visible all session: COUNT = how many, SUM = how much total, AVG = what's typical, MIN/MAX = the extremes. Point to it before every new example.
- **Common confusions, numbered:**
  1. Treating `COUNT(*)` as counting unique entities (customers, products) rather than rows.
  2. Running SUM/AVG on unchecked columns with missing or non-numeric values.
  3. Trying to filter on an aggregate result inside WHERE - the single most common error this session, and worth explicitly normalising as "everyone hits this wall once."
- **Cross-references:** GROUP BY and HAVING arrive next session and directly resolve today's WHERE-can't-filter-aggregates trap. Tableau's aggregation pills (SUM, AVG, COUNT) in Module 3 and pandas' `.sum()/.mean()/.count()` in Module 4 are the same five ideas under different syntax.
- **Local/cultural context:** The chai-stall "how many cups did we sell" hook and the cricket-statistician framing for MIN/MAX both continue this module's running cohort-friendly examples - keep reusing the same `orders` table and city set (Bengaluru, Hyderabad, Chennai) through GROUP BY next session for continuity.
