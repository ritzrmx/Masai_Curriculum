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

*The core flow fills all 90 minutes. Concept/Practical Block 5, on rounding aggregate output for a report (`ROUND()`), is in the Extension Blocks section - use only if ahead of pace.*

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

**Materials note:** today's session continues against the same `orders` table from Sessions 9–10 (`SQL Files/module2_phase1_sessions_4.2_to_5.2.db`) - 4 rows, unchanged:

```
order_id  customer_name  city       item           quantity  price  order_date
--------  -------------  ---------  -------------  --------  -----  ----------
1         Ramesh         Bengaluru  Veg Thali      2         120    2026-08-01
2         Fatima         Hyderabad  Non-Veg Thali  1         150    2026-08-01
3         Arjun          Bengaluru  Veg Thali      1         120    2026-08-02
4         Priya          Chennai    Mini Thali     3          90    2026-08-02
```

---

## Concept Block 1: COUNT (8 min)

### 💬 Instructor script

> *"Simplest question first: how many rows do I have? COUNT answers that."*

```sql
SELECT COUNT(*) AS total_orders
FROM orders;
```

Walk through the output live, and introduce aliasing (`AS total_orders`) as good habit: *"Without the alias, your result column is just called count(*) - not exactly something you'd want on a report."*

**Verified output:**
```
total_orders
------------
4
```

### 🔴 The trap / highest-value moment

> *"Here's the trap. If Ramesh placed 2 separate orders today, and I run COUNT(*), what do I get for Ramesh - 1 or 2?"*
> Let students answer; several will say 1 ("1 customer"). Correct firmly:
> *"COUNT(*) counts ROWS, not customers, not people, not anything else - unless one row genuinely equals one of those things. You already answered this exact question back in Session 9: what does one row represent? Ask it again, every single time, before you trust a COUNT."*

**Ground this in the actual table - it's worth pointing out live that no customer here happens to appear twice**, so COUNT(*) (4) and "number of distinct customers" happen to coincide in this specific dataset:

```sql
SELECT COUNT(*) AS total_rows, COUNT(DISTINCT customer_name) AS distinct_customers FROM orders;
```
```
total_rows  distinct_customers
----------  ------------------
4           4
```

> *"They match here, purely because every customer in this small table only ordered once. That's a coincidence of THIS dataset, not a rule. The moment a customer places a second order, `COUNT(*)` and `COUNT(DISTINCT customer_name)` will diverge - and if you didn't already know to check, you wouldn't notice."*

---

## Practical Block 1: Counting Rows Correctly (10 min)

**Activity:** Individually, students write: (1) total number of orders in the table; (2) total number of Bengaluru orders (using WHERE, previewing Concept Block 4).

**Answer key with verified output:**

```sql
SELECT COUNT(*) FROM orders;
```
```
COUNT(*)
--------
4
```

```sql
SELECT COUNT(*) FROM orders WHERE city = 'Bengaluru';
```
```
COUNT(*)
--------
2
```

Say aloud: *"Notice WHERE still works exactly like Session 9 - it filters rows first. COUNT just runs on whatever's left."*

> 💬 **Expect a student to ask if COUNT(*) and COUNT(customer_name) give the same answer.** Welcome it - don't answer immediately, tell them to test it live. Verified: `SELECT COUNT(*) AS all_rows, COUNT(customer_name) AS named_rows FROM orders;` returns `4, 4` - they match here unless a name is blank (a useful preview that COUNT on a specific column skips blank/missing values, which matters again in Concept Block 2).

---

## Concept Block 2: SUM and AVG (10 min)

### 💬 Instructor script

> *"Two more questions a manager always asks: how much, total - and what's typical? SUM answers the first. AVG answers the second."*

```sql
SELECT SUM(price) AS total_revenue, AVG(price) AS average_order_value
FROM orders;
```

Compute live on the board using `120, 150, 120, 90`: SUM = 480, AVG = 120.

**Verified output:**
```
total_revenue  average_order_value
-------------  -------------------
480            120.0
```

> *"AVG here is the exact same mean you calculated by hand in Session 8 - the database is just doing the arithmetic for you now."*

### 🔴 The trap / highest-value moment

> *"What happens if I run SUM on the city column instead of price?"*

Run `SELECT SUM(city) FROM orders;` live.

**Verified output - and this is worth knowing precisely before you run it live:**
```
SUM(city)
---------
0.0
```

> *"No error at all. SQLite tried to treat every city name as a number, failed silently, and just used 0 for each one - so the SUM of four zeros is 0.0. This is a real, important trap: in a database like MySQL or PostgreSQL, this would either error outright or behave more strictly. SQLite is unusually forgiving about mixing types, and that forgiveness can hide a genuine mistake instead of catching it for you. The lesson isn't 'SUM(city) is safe' - it's the opposite: never trust that a wrong aggregate will announce itself with an error. Before you trust any SUM or AVG, check the column the way you learned to in Module 1: is it actually clean, and is it actually numeric?"*

**And the quieter trap on missing values:** *"Here's the second part of this trap. If a price is missing or blank in some rows, AVG silently skips those rows rather than treating them as zero - which quietly changes what 'average' means. A column with 3 real prices and 1 blank doesn't average across 4 rows; it averages across 3, and reports a number that looks completely normal."*

---

## Practical Block 2: Totals and Averages on Real Data (10 min)

**Activity:** Pairs write: (1) total revenue across all orders; (2) average quantity per order, across all orders.

**Answer key with verified output:**

```sql
SELECT SUM(price) AS total_revenue FROM orders;
```
```
total_revenue
-------------
480
```

```sql
SELECT AVG(quantity) AS avg_quantity FROM orders;
```
```
avg_quantity
------------
1.75
```

Say aloud for the second: *"An average quantity of 1.75 items per order doesn't mean any single real order had 1.75 items - it's a summary statistic, not a description of one row. That distinction matters when you're explaining a number to someone non-technical."*

> 💬 **Expect a pushback that a fractional average "doesn't make sense" for a countable thing like quantity.** Welcome it - it's a genuinely good instinct. Say: *"You're right that no single order has 1.75 items. The average describes the whole dataset's typical behaviour, not any one row in it - the same idea as Session 8's averages, just automated."*

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

**Verified output:**
```
cheapest_order  priciest_order
--------------  --------------
90              150
```

> *"Same answer as ORDER BY price ASC LIMIT 1, but one function, one line, no sorting required."*

### 🔴 The trap / highest-value moment

> *"MIN and MAX aren't just for numbers. What do you think MIN(order_date) returns?"*
> Let students guess. Confirm: the earliest date, not a "smallest-looking" number. *"MIN and MAX work on text alphabetically and dates chronologically too. Write this down: these two functions work on any orderable data type, not just numbers."*

**Verify it live:**
```sql
SELECT MIN(order_date) AS earliest, MAX(order_date) AS latest FROM orders;
```
```
earliest    latest
----------  ----------
2026-08-01  2026-08-02
```

**And show text alphabetical ordering with a column students haven't used this way before:**
```sql
SELECT MIN(customer_name) AS first_alphabetically, MAX(customer_name) AS last_alphabetically FROM orders;
```
```
first_alphabetically  last_alphabetically
---------------------  --------------------
Arjun                  Ramesh
```

> *"MIN(customer_name) didn't error or return nonsense - it correctly found 'Arjun' as alphabetically first among Ramesh, Fatima, Arjun, Priya. Same function, three completely different data types, three sensible answers."*

---

## Practical Block 3: Extremes Challenge (8 min)

**Activity:** Individually, students write: (1) the earliest order date in the table; (2) the highest quantity ordered in a single order.

**Answer key with verified output:**

```sql
SELECT MIN(order_date) FROM orders;
```
```
MIN(order_date)
----------------
2026-08-01
```

```sql
SELECT MAX(quantity) FROM orders;
```
```
MAX(quantity)
--------------
3
```

Confirm aloud that `MIN(order_date)` correctly returns the earliest calendar date, not the numerically smallest-looking value if dates were stored oddly.

> 💬 **Expect someone to try `ORDER BY order_date LIMIT 1` instead out of habit from last session.** Welcome it - both are valid! Verified: `SELECT order_date FROM orders ORDER BY order_date ASC LIMIT 1;` also returns `2026-08-01` - identical answer, different route. Say: *"Both give you the right answer here. MIN is usually cleaner when you only need the single extreme value and nothing else about that row - you'll develop a feel for which to reach for."*

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

**Verified output:**
```
bengaluru_orders  bengaluru_revenue
-----------------  ------------------
2                   240
```

**A second worked example, on a different city, to reinforce the pattern generalizes:**
```sql
SELECT COUNT(*) AS hyderabad_orders, SUM(price) AS hyderabad_revenue FROM orders WHERE city = 'Hyderabad';
```
```
hyderabad_orders  hyderabad_revenue
-----------------  ------------------
1                   150
```

### 🔴 The trap / highest-value moment

> *"Now the trap that catches almost everyone at least once. I'm going to try to filter on a TOTAL instead of a raw row value."*
> Write `SELECT COUNT(*) FROM orders WHERE SUM(price) > 1000;` and run it live - let the error appear.

**Verified - this genuinely does error, unlike the SUM(city) case above:**
```
Error: in prepare, misuse of aggregate: SUM()
  SELECT COUNT(*) FROM orders WHERE SUM(price) > 1000;
                      error here ---^
```

> *"This fails because WHERE filters individual ROWS, before any aggregation exists. At the moment WHERE runs, there IS no total yet - SUM(price) hasn't been calculated. Write this down: WHERE can never reference an aggregate function. If you need to filter on a total, you need a different tool - HAVING - which arrives next session alongside GROUP BY."*

---

## Practical Block 4: Full Business-Question Challenge (12 min)

**Activity:** Light competitive framing. Give the class 3–4 combined business questions (e.g., "total revenue and order count from Hyderabad," "cheapest and priciest order placed after August 1st") and have pairs race to translate and write the query.

**Full answer key, verified against the real database:**

**1. "Total revenue and order count from Hyderabad."**
```sql
SELECT COUNT(*) AS order_count, SUM(price) AS total_revenue FROM orders WHERE city = 'Hyderabad';
```
```
order_count  total_revenue
-----------  -------------
1            150
```

**2. "Cheapest and priciest order placed after August 1st."**
```sql
SELECT MIN(price) AS cheapest, MAX(price) AS priciest FROM orders WHERE order_date > '2026-08-01';
```
```
cheapest  priciest
--------  --------
90        120
```

**3. "Average order value in Bengaluru."**
```sql
SELECT AVG(price) AS avg_bengaluru_price FROM orders WHERE city = 'Bengaluru';
```
```
avg_bengaluru_price
--------------------
120.0
```

For each, insist pairs state aloud which function(s) the question maps to before writing SQL. Example: *"'Total revenue and order count from Hyderabad' → SUM(price) and COUNT(*), filtered first with WHERE city = 'Hyderabad'."*

> 💬 **Expect at least one pair to attempt an aggregate inside WHERE again, out of habit.** Welcome it - this is exactly the mistake worth surfacing publicly. Say: *"Good - you just found the same wall the whole class hit in Concept Block 4. What's the fix?"*

---

## Extension Blocks (Optional — Use if Running Ahead)

*Not part of the 90-minute core flow. Use only if Practical Block 4 finishes early - see Timing Contingencies.*

### Concept Block 5 (Extension): Rounding Aggregate Output with ROUND()

#### 💬 Instructor script

> *"AVG(quantity) gave us 1.75 - a clean number. But AVG(price) on a messier real dataset can easily produce something like 119.66666666666667. Nobody wants that on a report."*

```sql
SELECT AVG(price) AS raw_avg, ROUND(AVG(price), 2) AS rounded_avg
FROM orders;
```

**Verified output:**
```
raw_avg  rounded_avg
-------  ------------
120.0    120.0
```

> *"On THIS table, price divides evenly, so there's nothing messy to see - but the syntax is worth knowing before you hit a table where it matters. `ROUND(value, 2)` means 'round to 2 decimal places.' Try it now on quantity, where 1.75 already has 2 decimals, and then round it to just 1."*

```sql
SELECT AVG(quantity) AS raw_avg, ROUND(AVG(quantity), 1) AS rounded_to_1 FROM orders;
```
```
raw_avg  rounded_to_1
-------  -------------
1.75     1.8
```

#### 🔴 The trap / highest-value moment

> *"1.75 rounded to 1 decimal place became 1.8, not 1.7 - standard rounding rules, nothing SQL-specific. But here's the real trap: ROUND() changes what's DISPLAYED, not what's actually stored or calculated further downstream. If you round early and then do more math on the rounded number, small errors can quietly accumulate. Round for the FINAL report output, not for intermediate calculations you're going to keep using."*

### Practical Block 5 (Extension): Reporting Clean Numbers

**Activity:** Pairs write a query showing Bengaluru's average order value, rounded to the nearest whole rupee (0 decimal places).

**Verified answer key:**

```sql
SELECT ROUND(AVG(price), 0) AS avg_bengaluru_price FROM orders WHERE city = 'Bengaluru';
```
```
avg_bengaluru_price
--------------------
120.0
```

> 💬 **Expect a pair to try `ROUND(price, 0)` instead of `ROUND(AVG(price), 0)` and get one rounded value per row instead of one rounded average.** Welcome it - run it live to show the difference: without AVG, ROUND applies to each individual row's price, returning multiple rows instead of a single summary number. Say: *"ROUND wraps around whatever it's given - if you give it a raw column, you get a rounded value per row. If you give it an aggregate's result, you get one rounded summary. Which one does the business question actually want?"*

---

## Common Errors

| Error | What causes it | Fix |
|---|---|---|
| Treating `COUNT(*)` as counting unique customers/products | Assuming one row automatically equals one of some other business entity | Confirm what one row represents before trusting any COUNT - ask it every time |
| `SUM(city)` silently returning `0.0` instead of erroring | SQLite's lenient type handling treats non-numeric text as 0 in arithmetic | Always sanity-check that a column is genuinely numeric before SUM/AVG - don't rely on an error to catch this for you |
| `misuse of aggregate: SUM()` inside WHERE | Trying to filter on an aggregate result before it's been calculated | Use HAVING (next session) to filter on aggregate results, never WHERE |
| A fractional AVG result "looks wrong" and gets discarded | Not recognising AVG as a summary statistic, not a description of any single row | Explain the number as "typical across the dataset," not "true of any one row" |
| AVG silently changes when rows have blank/missing values | AVG (and COUNT(column)) skip NULLs rather than treating them as zero | Check for blanks/missing values in the column first, the same way you would in Module 1, before trusting an AVG |
| Reporting an unrounded aggregate like `119.66666666666667` on a summary report | Not applying ROUND() to the final displayed number | Wrap the aggregate in `ROUND(..., n)` for the final report output |
| Using `ROUND(column, n)` when `ROUND(AGGREGATE(column), n)` was intended | Misplacing which value ROUND should actually be wrapped around | Apply ROUND to the aggregate function's result, not to the raw column, when a single rounded summary is needed |
| Assuming MIN/MAX only work on numbers | Not testing MIN/MAX against a text or date column | Remember MIN/MAX work on any orderable type: numbers, alphabetical text, and chronological dates |

---

## Materials Checklist

Before class, have ready:

- `SQL Files/module2_phase1_sessions_4.2_to_5.2.db` loaded in the shared SQL sandbox - same database and same 4-row `orders` table as Sessions 9 and 10.
- A projector for live queries, especially the `SUM(city)` non-error demonstration in Concept Block 2 and the `WHERE SUM(price) > 1000` genuine error in Concept Block 4 - the contrast between these two ("one silently returns 0.0, one genuinely errors") is one of the most important moments in the session and lands best live.
- A printed or slide copy of the 4-row `orders` table for quick reference throughout.
- The pre-read's business-question list for Practical Block 4, ready to reveal one at a time.
- If running the Extension Block: confirm the SQLite build in use supports `ROUND()` (standard in SQLite's core function set, no extension needed).

---

## Timing Contingencies

**If running long:**
- In Practical Block 1, skip the optional `COUNT(DISTINCT customer_name)` side demonstration and move straight to the WHERE-filtered COUNT exercise.
- Compress Practical Block 4 to 2 of the 3 business questions, assigning the rest as a take-home check.
- Never cut the `SUM(city)` non-error demonstration in Concept Block 2 or the `WHERE SUM(price) > 1000` genuine error in Concept Block 4 - together they teach students that SQLite's leniency is inconsistent (silent on type mismatches, strict on aggregate misuse), which is exactly the instinct that prevents costly mistakes later in the module.

**If running short:**
- Run the Extension Blocks (ROUND() for report-ready numbers) in full.
- If only a few minutes remain, demonstrate the single `ROUND(AVG(price), 2)` query from Concept Block 5 live as a quick capstone, without the paired Practical Block 5.
- Alternatively, revisit Concept Block 1's `COUNT(*)` vs `COUNT(DISTINCT customer_name)` distinction and ask pairs to predict what would happen to each if a 5th order, also placed by Ramesh, were added to the table - a strong verbal reinforcement of the "one row ≠ one customer" trap without needing new syntax.

---

## End-of-Session Quiz

1. **What's the difference between `COUNT(*)` and `COUNT(column_name)`?**
   → `COUNT(*)` counts every row regardless of content. `COUNT(column_name)` counts only rows where that column isn't blank/missing.

2. **`SELECT SUM(price), AVG(price) FROM orders;` on this session's table returns what two numbers?**
   → 480 and 120.0.

3. **Why did `SUM(city)` return `0.0` instead of an error, while `WHERE SUM(price) > 1000` genuinely errored?**
   → SQLite is lenient about type mismatches in arithmetic (it silently treats non-numeric text as 0), but it strictly disallows using an aggregate function inside WHERE, because WHERE runs before any aggregation exists.

4. **What does `MIN(order_date)` return - and does MIN only work on numbers?**
   → The earliest calendar date, `2026-08-01`. No - MIN/MAX work on any orderable type: numbers, text (alphabetically), and dates (chronologically).

5. **Why can't you filter on an aggregate result using WHERE?**
   → WHERE filters individual rows before any aggregation happens - at that point in query execution, no total/average/count yet exists to compare against.

6. **(If Extension Block covered) What's the difference between `ROUND(price, 2)` and `ROUND(AVG(price), 2)`?**
   → The first rounds each individual row's price value (one rounded number per row); the second rounds the single aggregated average (one rounded summary number).

---

## Q&A & Doubt Solving

**Q: Can I use more than one aggregate function in the same query?**
→ Yes - as shown today, `SELECT COUNT(*), SUM(price), AVG(price) FROM orders;` runs all three in one query, each producing its own column in the result.

**Q: What does COUNT(column_name) do differently from COUNT(*)?**
→ `COUNT(*)` counts every row regardless of content. `COUNT(column_name)` counts only rows where that specific column isn't blank/missing - a subtle but important difference when data has gaps.

**Q: Can I combine an aggregate with ORDER BY or LIMIT from last session?**
→ Not quite yet in the way you might expect - ordering and limiting *grouped* aggregate results is exactly what next session's GROUP BY unlocks. For now, a single aggregate query returns one row, so ordering/limiting isn't meaningful yet.

**Q: Why did SUM(city) return 0.0 instead of just giving me something weird or refusing?**
→ SQLite checks types more loosely than most databases - it tried to convert each city name to a number for the addition, failed, and used 0 as the fallback for each failed conversion. Other databases (MySQL, PostgreSQL, SQL Server) are typically stricter and would raise a real error here instead.

**Q: Is AVG the same as the median from Session 8?**
→ No - AVG is always the mean (sum ÷ count), never the median. If you need the median in SQL, that requires a more advanced technique we haven't covered yet; know that "average" in SQL always defaults to mean unless stated otherwise.

**Q: Does ROUND() change the underlying data in the table?**
→ No - exactly like ORDER BY, ROUND() only changes what's displayed in that query's result. The stored data is completely unaffected.

**Q: If AVG silently skips blank values, is there a way to see how many rows were actually skipped?**
→ Yes - compare `COUNT(*)` (all rows) against `COUNT(column_name)` (non-blank rows only) in the same query. The difference between the two tells you exactly how many rows were excluded from the AVG calculation.

---

## Instructor Notes

- **Words not yet earned:** Avoid `GROUP BY`, `HAVING`, subqueries, and window functions - GROUP BY and HAVING arrive next session specifically to fix the WHERE-can't-filter-aggregates trap taught today. If a student asks "can I get total revenue PER city?", acknowledge that's exactly next session rather than answering in full now.
- **The single biggest risk in this session** is students treating COUNT/SUM/AVG as interchangeable "give me a number" buttons without checking what they actually measure. Defeat it by repeatedly asking, across every block: *"What does one row represent, and does that match what this function is telling you?"*
- **Board management:** Keep a simple four-row reference visible all session: COUNT = how many, SUM = how much total, AVG = what's typical, MIN/MAX = the extremes. Point to it before every new example.
- **Common confusions, numbered:**
  1. Treating `COUNT(*)` as counting unique entities (customers, products) rather than rows.
  2. Running SUM/AVG on unchecked columns with missing or non-numeric values, and trusting SQLite to error if something's wrong - it often won't.
  3. Trying to filter on an aggregate result inside WHERE - the single most common error this session, and worth explicitly normalising as "everyone hits this wall once."
  4. Applying ROUND() to a raw column when the intent was to round an aggregate's result, producing one rounded value per row instead of a single rounded summary.
- **Cross-references:** GROUP BY and HAVING arrive next session and directly resolve today's WHERE-can't-filter-aggregates trap. Tableau's aggregation pills (SUM, AVG, COUNT) in Module 3 and pandas' `.sum()/.mean()/.count()` in Module 4 are the same five ideas under different syntax; pandas' `.round()` mirrors today's Extension Block directly.
- **Local/cultural context:** The chai-stall "how many cups did we sell" hook and the cricket-statistician framing for MIN/MAX both continue this module's running cohort-friendly examples - keep reusing the same `orders` table and city set (Bengaluru, Hyderabad, Chennai) through GROUP BY next session for continuity.
