# Lecture Script: SQL for Data Analysis - Grouping for KPIs
> **Instructor Reference** - Module 2: SQL for Data Analysis | Academic Session 12 | Duration: 1.5 Hours | Instructor: Industry Mentor

---

## Session Overview

**Goal:** Students can take a "by category" business question - "revenue by city," "top-selling item," "which branches passed a target" - and answer it in a single query using `GROUP BY`, `HAVING`, and every clause learned so far in the module.

**Student profile at this point:** They've completed Session 11 (COUNT, SUM, AVG, MIN, MAX) and specifically hit the wall where `WHERE SUM(price) > 1000` errored. That unresolved trap is the perfect setup for today - GROUP BY and HAVING exist specifically to fix it.

**Key outcome:** Students leave able to build, unprompted, the single most requested query shape in real analytics work: a KPI broken out by category, filtered, ranked, and trimmed to a headline answer.

> 🎯 **The one sentence this session must land:** *WHERE filters rows. GROUP BY creates the groups. HAVING filters groups. Confusing those three is the single most common SQL mistake - even experienced analysts make it.*

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| Opening - "Not one number. One number PER BRANCH." | 8 min | 8 min |
| Concept Block 1: GROUP BY | 10 min | 18 min |
| Practical Block 1: Grouping the orders table | 10 min | 28 min |
| Concept Block 2: Multiple aggregates per group | 8 min | 36 min |
| Practical Block 2: Building a mini KPI table | 10 min | 46 min |
| **BREAK** | 5 min | 51 min |
| Concept Block 3: HAVING | 10 min | 61 min |
| Practical Block 3: Fixing last session's broken query | 8 min | 69 min |
| Concept Block 4: The full clause order | 9 min | 78 min |
| Practical Block 4: Full KPI-query challenge | 12 min | 90 min |

*The core flow fills all 90 minutes. Concept/Practical Block 5, on grouping by more than one column at once, is in the Extension Blocks section - use only if ahead of pace.*

---

## Opening - "Not One Number. One Number PER BRANCH." (8 min)

Walk in and rerun last session's closing query live:

```sql
SELECT COUNT(*) AS total_orders, SUM(price) AS total_revenue
FROM orders;
```

**Verified output:**
```
total_orders  total_revenue
------------  -------------
4             480
```

> *"Last session, this told us total orders and total revenue for the WHOLE business. Now the chai stall owner from last week has grown - she runs 3 branches. She doesn't want ONE total anymore. She wants to know: how did EACH branch do? Bengaluru, Hyderabad, Chennai - separately, side by side, in one report."*

Ask the room: *"How would you get that with what you know right now?"* Someone may suggest running the query three times, once per WHERE filter. Let that land as painfully tedious - demonstrate it live to make the tedium concrete:

```sql
SELECT COUNT(*), SUM(price) FROM orders WHERE city = 'Bengaluru';
SELECT COUNT(*), SUM(price) FROM orders WHERE city = 'Hyderabad';
SELECT COUNT(*), SUM(price) FROM orders WHERE city = 'Chennai';
```

**Verified outputs, run separately:**
```
2, 240
1, 150
1, 90
```

> *"Three separate queries for three branches works today. What happens when there are 50 branches? Or 5,000 customers? Running the query 5,000 times isn't a plan."*

**Pivot line:**

> *"Today you learn ONE clause that does all of that in a single query: GROUP BY. By the end of ninety minutes, you'll build the exact table a manager actually wants - a KPI broken out by category - in one line of SQL, whether there are 3 categories or 3,000."*

**Context for the sessions ahead:** *"This is also, not coincidentally, exactly the shape of every pivot table you built back in Module 1, and exactly the shape behind every dashboard view you'll build in Tableau next module. Today you're learning the engine underneath both."*

---

## Concept Block 1: GROUP BY (10 min)

### 💬 Instructor script

> *"GROUP BY takes one column, splits your table into separate piles based on its distinct values, and then runs your aggregate function once per pile."*

```sql
SELECT city, COUNT(*) AS order_count
FROM orders
GROUP BY city;
```

Walk through it visually on the board: physically circle the Bengaluru rows, the Hyderabad row, the Chennai row as separate clusters before showing the collapsed result table.

**Verified output:**
```
city       order_count
---------  -----------
Bengaluru  2
Chennai    1
Hyderabad  1
```

> *"Three piles from four rows - exactly the three separate queries from the Opening, collapsed into one. Notice the totals match exactly what we ran three separate times a moment ago."*

### 🔴 The trap / highest-value moment

> *"Now watch this fail. I'm adding customer_name to the SELECT list without adding it to GROUP BY."*
> Write and run `SELECT city, customer_name, COUNT(*) FROM orders GROUP BY city;` - let the error or inconsistent result appear.

**Verified - this doesn't error in SQLite, which is itself worth flagging explicitly:**
```
city       customer_name  COUNT(*)
---------  -------------  --------
Bengaluru  Ramesh         2
Chennai    Priya          1
Hyderabad  Fatima         1
```

> *"No error - and that's more dangerous than an error would be. Within the Bengaluru group, there are 2 different customer names - Ramesh and Arjun. SQLite picked Ramesh here, silently, with no promise it'll pick the same one next time this exact query runs. Arjun placed one of Bengaluru's two orders and is completely invisible in this output, and nothing told you that. Write down this rule: every column in SELECT must either be in GROUP BY, or wrapped inside an aggregate function. No exceptions - even when SQLite lets you break the rule without complaint."*

---

## Practical Block 1: Grouping the Orders Table (10 min)

**Activity:** Individually, students write: (1) order count per city; (2) order count per item.

**Answer key with verified output:**

```sql
SELECT city, COUNT(*) AS order_count FROM orders GROUP BY city;
```
```
city       order_count
---------  -----------
Bengaluru  2
Chennai    1
Hyderabad  1
```

```sql
SELECT item, COUNT(*) AS order_count FROM orders GROUP BY item;
```
```
item           order_count
-------------  -----------
Mini Thali     1
Non-Veg Thali  1
Veg Thali      2
```

Say aloud for the second: *"Same clause, different column - GROUP BY works on any column with distinct categories, not just city. Notice Veg Thali groups Ramesh's and Arjun's orders together, even though they're different customers in different rows - GROUP BY only cares about the value in the grouped column."*

> 💬 **Expect someone to try grouping by `price` out of curiosity and get a group per unique price rather than a meaningful business category.** Welcome it. Verified: `SELECT price, COUNT(*) FROM orders GROUP BY price;` returns `90→1, 120→2, 150→1` - technically valid, but does "group by exact price" answer a real business question? Say: *"GROUP BY only becomes useful when the column represents a genuine category, like city or item, not an incidental number that happens to repeat."*

---

## Concept Block 2: Multiple Aggregates Per Group (8 min)

### 💬 Instructor script

> *"A manager reviewing branches doesn't want just order count - they want count, total revenue, AND average order value, together, per branch."*

```sql
SELECT city,
       COUNT(*) AS order_count,
       SUM(price) AS total_revenue,
       AVG(price) AS average_order_value
FROM orders
GROUP BY city;
```

Walk through the full 3-row output live.

**Verified output:**
```
city       order_count  total_revenue  average_order_value
---------  -----------  -------------  --------------------
Bengaluru  2            240            120.0
Chennai    1            90             90.0
Hyderabad  1            150            150.0
```

### 🔴 The trap / highest-value moment

> *"Quick check: is the AVG in the Hyderabad row the average across the WHOLE table, or just Hyderabad's orders?"*
> Let the room answer. Confirm: *"Just Hyderabad's - and since Hyderabad only has 1 order, that 'average' is really just that one order's price, 150. Write this down: every aggregate in a grouped query is scoped ONLY to its own group's rows, never the whole table."*

**Prove it isn't the whole-table average by comparing directly:**
```sql
SELECT AVG(price) AS whole_table_avg FROM orders;
```
```
whole_table_avg
-----------------
120.0
```

> *"Hyderabad's grouped average is 150. The whole table's average is 120. They're different numbers because they're answering different questions - and a manager skimming a report needs to know which one they're looking at."*

---

## Practical Block 2: Building a Mini KPI Table (10 min)

**Activity:** Pairs write a single query returning order count, total revenue, and average order value, grouped by item.

**Answer key with verified output:**

```sql
SELECT item,
       COUNT(*) AS order_count,
       SUM(price) AS total_revenue,
       AVG(price) AS average_order_value
FROM orders
GROUP BY item;
```
```
item           order_count  total_revenue  average_order_value
-------------  -----------  -------------  --------------------
Mini Thali     1            90             90.0
Non-Veg Thali  1            150            150.0
Veg Thali      2            240            120.0
```

Ask pairs to identify aloud, from their own output, which item has the highest total revenue - Veg Thali, at ₹240 - this previews Concept Block 4's ORDER BY/LIMIT combination.

> 💬 **Expect a pair to ask if they can add a fourth aggregate, like MIN or MAX price per item.** Welcome it enthusiastically. Verified: adding `MIN(price) AS min_price, MAX(price) AS max_price` to the query above returns, for Veg Thali, `min_price = 120, max_price = 120` (both Veg Thali orders happen to cost the same). Say: *"Try it - any number of aggregate functions can ride along in the same GROUP BY query, exactly like they could without GROUP BY last session."*

---

## BREAK (5 min)

---

## Concept Block 3: HAVING (10 min)

### 💬 Instructor script

> *"Remember last session's error? WHERE SUM(price) > 1000 - it failed, because WHERE only sees raw rows, before any total exists. Today, that exact business need has a real answer."*

```sql
SELECT city, SUM(price) AS total_revenue
FROM orders
GROUP BY city
HAVING SUM(price) > 100;
```

Walk through live: Bengaluru (240) and Hyderabad (150) survive; Chennai (90) is dropped.

**Verified output:**
```
city       total_revenue
---------  -------------
Bengaluru  240
Hyderabad  150
```

### 🔴 The trap / highest-value moment

> *"The test that saves you every time: does your condition mention a RAW column, like city or item? That's WHERE. Does it mention an AGGREGATE function, like SUM or COUNT? That's HAVING. Mixing them up - putting an aggregate condition in WHERE, or a raw condition in HAVING - is one of the most common SQL mistakes, and it doesn't stop being common once you have a job. Write this rule down, twice if you have to."*

---

## Practical Block 3: Fixing Last Session's Broken Query (8 min)

**Activity:** Project last session's error query again: `SELECT COUNT(*) FROM orders WHERE SUM(price) > 1000;`. In pairs, students rewrite it correctly using GROUP BY and HAVING to find cities (or items) with total revenue above a threshold.

**Answer key with verified output:**

```sql
SELECT city, SUM(price) AS total_revenue
FROM orders
GROUP BY city
HAVING SUM(price) > 100;
```
```
city       total_revenue
---------  -------------
Bengaluru  240
Hyderabad  150
```

Say aloud: *"Same business question that errored last week. The fix wasn't a small syntax tweak - it needed two new clauses working together."*

**A second worked version, grouped by item instead, to reinforce the pattern doesn't depend on the specific column:**
```sql
SELECT item, SUM(price) AS total_revenue FROM orders GROUP BY item HAVING SUM(price) > 100;
```
```
item           total_revenue
-------------  -------------
Non-Veg Thali  150
Veg Thali      240
```

> 💬 **Expect genuine satisfaction/relief in the room at finally resolving last session's unresolved error.** Let that land - it reinforces retention far better than introducing HAVING cold.

---

## Concept Block 4: The Full Clause Order (9 min)

### 💬 Instructor script

> *"Real manager requests are full sentences, not single clauses. 'Revenue by city, only cities over ₹100, sorted highest first, just the top 2.' Every clause you've learned this module answers one piece of that sentence, in a fixed order."*

Write the full skeleton on the board:
```
SELECT ... FROM ... WHERE ... GROUP BY ... HAVING ... ORDER BY ... LIMIT ...
```

```sql
SELECT city, SUM(price) AS total_revenue
FROM orders
WHERE quantity > 0
GROUP BY city
HAVING SUM(price) > 100
ORDER BY total_revenue DESC
LIMIT 2;
```

Read it aloud, clause by clause, mapping each back to a piece of the plain-English sentence.

**Verified output:**
```
city       total_revenue
---------  -------------
Bengaluru  240
Hyderabad  150
```

### 🔴 The trap / highest-value moment

> *"One more trap. After GROUP BY, can I still ORDER BY the original price column?"*
> Write `SELECT city, SUM(price) AS total_revenue FROM orders GROUP BY city ORDER BY price DESC;` and run it live.

**Verified - this does NOT error, and that makes it more dangerous, not less:**
```
city       total_revenue
---------  -------------
Hyderabad  150
Bengaluru  240
Chennai    90
```

> *"Look closely - is that sorted by total_revenue? No. Bengaluru's total (240) is actually the HIGHEST, but it's sitting in the MIDDLE of this output. SQLite let `price` slip through even though it's not in GROUP BY or wrapped in an aggregate - and it silently picked one arbitrary row's price to represent each group, then sorted by THAT. This is a technically-running query giving you a genuinely wrong ranking, with zero error message. After grouping, price doesn't reliably exist row-by-row anymore - only the aggregated column, total_revenue, exists in any well-defined sense. Sort and filter using the NEW column names your aggregates created, not the raw columns they were built from."*

---

## Practical Block 4: Full KPI-Query Challenge (12 min)

**Activity:** Light competitive framing. Give the class 2–3 full combined business questions (e.g., "top 2 cities by total revenue, but only cities with more than 1 order," "average order value per item, sorted lowest to highest, items with fewer than 2 orders excluded") and have pairs race to build the complete query.

**Full answer key, verified against the real database:**

**1. "Top 2 cities by total revenue, but only cities with more than 1 order."**
```sql
SELECT city, COUNT(*) AS order_count, SUM(price) AS total_revenue
FROM orders
GROUP BY city
HAVING COUNT(*) > 1
ORDER BY total_revenue DESC
LIMIT 2;
```
```
city       order_count  total_revenue
---------  -----------  -------------
Bengaluru  2            240
```
*(Only Bengaluru clears `COUNT(*) > 1` in this 4-row table - Hyderabad and Chennai each have exactly 1 order. This is a good moment to note: LIMIT 2 was requested, but only 1 row satisfies HAVING, so only 1 row comes back - the same "LIMIT caps a maximum, doesn't invent rows" lesson from Session 10.)*

**2. "Average order value per item, sorted lowest to highest, items with fewer than 2 orders excluded."**
```sql
SELECT item, AVG(price) AS avg_price, COUNT(*) AS order_count
FROM orders
GROUP BY item
HAVING COUNT(*) >= 2
ORDER BY avg_price ASC;
```
```
item       avg_price  order_count
---------  ---------  -----------
Veg Thali  120.0      2
```
*(Only Veg Thali has 2+ orders; Mini Thali and Non-Veg Thali each have exactly 1, so `HAVING COUNT(*) >= 2` correctly excludes them both.)*

Insist pairs say the plain-English translation aloud, mapping each clause before typing SQL. Reveal answers one at a time, discussing WHERE-vs-HAVING mix-ups as they surface.

> 💬 **Expect at least one pair to put a raw-row condition inside HAVING instead of WHERE** (e.g., `HAVING city = 'Bengaluru'` instead of filtering it in WHERE). Welcome it. Verified: `SELECT city, SUM(price) FROM orders GROUP BY city HAVING city = 'Bengaluru';` actually runs successfully and returns the correct Bengaluru row - it doesn't error. Say: *"That ran and gave the right answer here - so ask yourself: is 'city' an aggregate result, or a raw column? It happening to work doesn't make it the right clause. WHERE is the right home for this condition, and using HAVING for it will confuse the next person reading your query, even when SQLite tolerates it."*

---

## Extension Blocks (Optional — Use if Running Ahead)

*Not part of the 90-minute core flow. Use only if Practical Block 4 finishes early - see Timing Contingencies.*

### Concept Block 5 (Extension): Grouping by More Than One Column

#### 💬 Instructor script

> *"GROUP BY isn't limited to one column. You can group by a COMBINATION of columns, creating one pile per unique pairing."*

```sql
SELECT city, item, COUNT(*) AS order_count
FROM orders
GROUP BY city, item;
```

**Verified output:**
```
city       item           order_count
---------  -------------  -----------
Bengaluru  Veg Thali      2
Chennai    Mini Thali     1
Hyderabad  Non-Veg Thali  1
```

> *"Notice this table has the same 3 rows as grouping by city alone - purely because, in this small dataset, every city happens to have ordered only one distinct item. That's a coincidence of this table's size, not a rule. Add a second Chennai order for a different item, and grouping by city alone would merge them, while grouping by city AND item would correctly keep them as two separate rows."*

#### 🔴 The trap / highest-value moment

> *"Here's the test for whether you need one grouping column or two: does the business question have ONE category in it, or TWO stacked together? 'Revenue by city' is one category - GROUP BY city. 'Revenue by city, broken down by item' is two - GROUP BY city, item. Read the business question for how many categories it's actually asking to slice by."*

### Practical Block 5 (Extension): Two-Column Grouping Challenge

**Activity:** Pairs write a query showing total revenue for every city-and-item combination.

**Verified answer key:**

```sql
SELECT city, item, SUM(price) AS total_revenue
FROM orders
GROUP BY city, item;
```
```
city       item           total_revenue
---------  -------------  -------------
Bengaluru  Veg Thali      240
Chennai    Mini Thali     90
Hyderabad  Non-Veg Thali  150
```

> 💬 **Expect a pair to ask whether the column order in `GROUP BY city, item` versus `GROUP BY item, city` changes the result.** Welcome it - verified: reversing the order produces the identical set of grouped rows (just potentially displayed in a different row order, since no ORDER BY was specified). Say: *"The GROUPS themselves don't change based on column order in GROUP BY - but which order the resulting rows come back in isn't guaranteed either way. Add an ORDER BY if you need a specific, repeatable row order."*

---

## Common Errors

| Error | What causes it | Fix |
|---|---|---|
| Selecting a raw column not in GROUP BY or wrapped in an aggregate | Adding a column to SELECT without checking it belongs in GROUP BY | Every SELECT column must either appear in GROUP BY or be wrapped in an aggregate function - SQLite won't always stop you if you skip this |
| Assuming a grouped aggregate reflects the whole table | Not distinguishing a group's own scope from the full table's | Compare a suspicious grouped number against the ungrouped whole-table aggregate if it looks off |
| Putting an aggregate condition (e.g. `SUM(price) > 100`) inside WHERE | Habit from before HAVING was introduced | Use HAVING for any condition that references an aggregate function |
| Putting a raw-row condition (e.g. `city = 'Bengaluru'`) inside HAVING | Reaching for HAVING as a generic "second filter," regardless of what it filters | Use WHERE for raw-row conditions, even when HAVING happens to tolerate it without erroring |
| `ORDER BY price` after `GROUP BY city` producing a silently wrong ranking | SQLite allowing a raw column not in GROUP BY/aggregate to leak through and sort by an arbitrary representative row | Sort and filter using the new aggregate column names (e.g. `total_revenue`), never the raw columns the aggregate was built from |
| Expecting `LIMIT N` to always return N rows after HAVING has filtered the groups | Not accounting for fewer groups surviving HAVING than the LIMIT value | Remember LIMIT caps a maximum; if HAVING has already reduced the groups below N, fewer rows correctly come back |
| Grouping by an incidental numeric column (like exact price) instead of a real category | Treating any repeating column as fair game for GROUP BY | Confirm the grouped column represents a genuine business category before using it |
| Using only one grouping column when the business question describes two stacked categories | Not translating "by X, broken down by Y" into `GROUP BY X, Y` | Count how many categories the plain-English question actually names, and match that to the number of GROUP BY columns |

---

## Materials Checklist

Before class, have ready:

- `SQL Files/module2_phase1_sessions_4.2_to_5.2.db` loaded in the shared SQL sandbox - same database and same 4-row `orders` table as Sessions 9–11.
- A projector for live queries, especially: the Concept Block 1 `SELECT city, customer_name, COUNT(*) ... GROUP BY city` non-error trap, and the Concept Block 4 `ORDER BY price` after `GROUP BY city` silently-wrong-ranking trap - both need to be seen running live, not just described, since their entire teaching value is "this doesn't error, and that's the danger."
- Last session's error query (`SELECT COUNT(*) FROM orders WHERE SUM(price) > 1000;`) ready to re-project at the start of Practical Block 3.
- A printed or slide copy of the 4-row `orders` table for quick reference throughout.
- The pre-read's combined business-question list for Practical Block 4, ready to reveal one at a time.

---

## Timing Contingencies

**If running long:**
- In Practical Block 2, walk the class through the answer key as a single demo rather than having every pair independently confirm the MIN/MAX bonus extension.
- Compress Practical Block 4 to just the first business question, assigning the second as a take-home check.
- Never cut the Concept Block 4 `ORDER BY price` after `GROUP BY city` demonstration - it is the clearest possible proof that "runs without error" and "correct" are different things, a theme that recurs constantly for the rest of the module (joins, subqueries, GenAI-generated SQL).

**If running short:**
- Run the Extension Blocks (grouping by more than one column) in full.
- If only a few minutes remain, demonstrate the single two-column GROUP BY query from Concept Block 5 live as a quick capstone, without the paired Practical Block 5.
- Alternatively, revisit Practical Block 4's Question 1 and ask pairs to rewrite it without the `HAVING COUNT(*) > 1` condition, then discuss aloud how the result set changes - a strong reinforcement of HAVING's role without needing new syntax.

---

## End-of-Session Quiz

1. **What does GROUP BY actually do to a table before your aggregate functions run?**
   → It splits the table into separate groups (piles) based on the distinct values in the grouped column(s), and each aggregate function then runs once per group.

2. **Why does `SELECT city, customer_name, COUNT(*) FROM orders GROUP BY city;` produce a misleading result instead of an error in SQLite?**
   → `customer_name` isn't in GROUP BY and isn't wrapped in an aggregate, so SQLite picks one arbitrary row's value per group to display - silently hiding that a group might contain multiple different customer names.

3. **What's the test for choosing WHERE versus HAVING?**
   → Does the condition reference a raw row-level column (WHERE) or an aggregate function's result (HAVING)?

4. **In `SELECT city, SUM(price) AS total_revenue FROM orders GROUP BY city HAVING SUM(price) > 100;`, which city gets dropped, and why?**
   → Chennai - its total_revenue is 90, which doesn't clear the `> 100` threshold.

5. **What's wrong with `ORDER BY price` immediately after `GROUP BY city`?**
   → `price` no longer exists in a well-defined, row-by-row sense after grouping - sorting by it uses an arbitrary representative value per group, producing a ranking that doesn't actually match the aggregated totals.

6. **(If Extension Block covered) How do you translate "revenue by city, broken down by item" into a GROUP BY clause?**
   → `GROUP BY city, item` - one grouping column per category named in the business question.

---

## Q&A & Doubt Solving

**Q: Can I use HAVING without GROUP BY?**
→ Technically in some databases, but it's rarely meaningful - HAVING is built to filter *groups*, and without GROUP BY, the whole table is treated as one group. In this course, always pair HAVING with GROUP BY.

**Q: Can I GROUP BY more than one column at once?**
→ Yes - `GROUP BY city, item` creates a separate group for every unique city-and-item combination, not just every city. See the Extension Block above for a full worked example against this session's table.

**Q: Does the order of columns in GROUP BY matter?**
→ Less than in ORDER BY, but it's good practice to match your SELECT list's order for readability - the resulting groups are the same regardless of column order in GROUP BY itself; only the default row-return order can differ, and that's never guaranteed anyway.

**Q: Can I use an alias (like total_revenue) inside HAVING or ORDER BY?**
→ Most databases allow aliases in ORDER BY, but HAVING support for aliases varies - safest habit in this course is to repeat the full aggregate expression (`SUM(price)`) inside HAVING, and use the alias freely in ORDER BY.

**Q: What if a group has only 1 row - does AVG still work?**
→ Yes - AVG on a single-row group simply returns that one row's value, since sum ÷ count of 1 is just the value itself. It's mathematically valid, just worth remembering that a "1-order average" (like Hyderabad and Chennai in this table) isn't very statistically meaningful.

**Q: Why didn't `HAVING city = 'Bengaluru'` error, if HAVING is "supposed to" be for aggregates?**
→ SQLite (and most SQL databases) don't strictly enforce that HAVING conditions must reference an aggregate - they'll happily accept a raw-column condition there too, since by the time HAVING runs, the raw columns used in GROUP BY are still technically accessible. It running successfully doesn't make it the right clause to use; WHERE remains the correct, more efficient, and more readable home for raw-row conditions.

**Q: Is there a performance reason to prefer WHERE over HAVING when either would technically work?**
→ Yes, generally - WHERE filters rows before grouping happens, so the database does less work overall (fewer rows to group and aggregate). HAVING filters after grouping is already done. For small class datasets like today's it makes no visible difference, but it's a genuinely good habit for real-sized tables.

---

## Instructor Notes

- **Words not yet earned:** Avoid `JOIN`, subqueries, CTEs, and window functions - JOIN arrives explicitly next session. If a student asks "can I group by something from a different table?", acknowledge that's exactly next session's topic rather than answering in full now.
- **The single biggest risk in this session** is the WHERE/HAVING confusion becoming a permanently sticky habit if not corrected firmly and repeatedly today. Defeat it with the same one-line test every time it surfaces: *"Raw column or aggregate? WHERE or HAVING?"* - say it as a chant, not just an explanation.
- **Board management:** Keep the full clause skeleton - `SELECT, FROM, WHERE, GROUP BY, HAVING, ORDER BY, LIMIT` - visible all session, and physically point to each clause as you build up the Concept Block 4 example piece by piece. If running the Extension Block, note `GROUP BY col1, col2` as a variation on the same skeleton rather than a new one.
- **Common confusions, numbered:**
  1. Selecting a raw column that isn't in GROUP BY or wrapped in an aggregate - and not noticing, because SQLite often doesn't error.
  2. Assuming a grouped aggregate reflects the whole table rather than just its own group.
  3. Putting an aggregate condition in WHERE, or a raw-row condition in HAVING - the single most persistent SQL mistake and worth calling out by name every time it appears, even when SQLite happens to tolerate the misplaced one.
  4. Trying to ORDER BY a raw column (like price) after that column has been collapsed by GROUP BY - and trusting the result because it ran without an error.
- **Cross-references:** JOIN arrives next session, letting GROUP BY work across combined tables. Tableau's dimension/measure pill system (Module 3) and pandas' `.groupby()` (Module 4) are this exact same idea in different clothing - plant that connection explicitly in the bridge.
- **Local/cultural context:** The chai stall's growth from one stall to three branches is a deliberate callback thread - keep using "branch" language (not "store" or "location") consistently, since it'll resurface once JOIN introduces a linked `customers` table with `loyalty_tier` in the very next session.
