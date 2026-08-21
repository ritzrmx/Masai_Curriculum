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

---

## Opening - "Not One Number. One Number PER BRANCH." (8 min)

Walk in and rerun last session's closing query live:

```sql
SELECT COUNT(*) AS total_orders, SUM(price) AS total_revenue
FROM orders;
```

> *"Last session, this told us total orders and total revenue for the WHOLE business. Now the chai stall owner from last week has grown - she runs 3 branches. She doesn't want ONE total anymore. She wants to know: how did EACH branch do? Bengaluru, Hyderabad, Chennai - separately, side by side, in one report."*

Ask the room: *"How would you get that with what you know right now?"* Someone may suggest running the query three times, once per WHERE filter. Let that land as painfully tedious:

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

### 🔴 The trap / highest-value moment

> *"Now watch this fail. I'm adding customer_name to the SELECT list without adding it to GROUP BY."*
> Write and run `SELECT city, customer_name, COUNT(*) FROM orders GROUP BY city;` - let the error or inconsistent result appear.
> *"Within the Bengaluru group, there are 2 different customer names - Ramesh and Arjun. SQL has no idea which one you want shown, so it either errors or picks unpredictably. Write down this rule: every column in SELECT must either be in GROUP BY, or wrapped inside an aggregate function. No exceptions."*

---

## Practical Block 1: Grouping the Orders Table (10 min)

**Activity:** Individually, students write: (1) order count per city; (2) order count per item.

**Answer key with reasoning:** `GROUP BY city` and `GROUP BY item`, each with `COUNT(*)`. Say aloud for the second: *"Same clause, different column - GROUP BY works on any column with distinct categories, not just city."*

> 💬 **Expect someone to try grouping by `price` out of curiosity and get a group per unique price rather than a meaningful business category.** Welcome it. Say: *"Technically valid SQL - but does 'group by exact price' answer a real business question? GROUP BY only becomes useful when the column represents a genuine category, like city or item, not an incidental number."*

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

### 🔴 The trap / highest-value moment

> *"Quick check: is the AVG in the Hyderabad row the average across the WHOLE table, or just Hyderabad's orders?"*
> Let the room answer. Confirm: *"Just Hyderabad's - and if Hyderabad only has 1 order, that 'average' is really just that one order's price. Write this down: every aggregate in a grouped query is scoped ONLY to its own group's rows, never the whole table."*

---

## Practical Block 2: Building a Mini KPI Table (10 min)

**Activity:** Pairs write a single query returning order count, total revenue, and average order value, grouped by item.

**Answer key with reasoning:** Same three-function pattern as Concept Block 2, `GROUP BY item`. Ask pairs to identify aloud, from their own output, which item has the highest total revenue - this previews Concept Block 4's ORDER BY/LIMIT combination.

> 💬 **Expect a pair to ask if they can add a fourth aggregate, like MIN or MAX price per item.** Welcome it enthusiastically. Say: *"Try it - any number of aggregate functions can ride along in the same GROUP BY query, exactly like they could without GROUP BY last session."*

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

### 🔴 The trap / highest-value moment

> *"The test that saves you every time: does your condition mention a RAW column, like city or item? That's WHERE. Does it mention an AGGREGATE function, like SUM or COUNT? That's HAVING. Mixing them up - putting an aggregate condition in WHERE, or a raw condition in HAVING - is one of the most common SQL mistakes, and it doesn't stop being common once you have a job. Write this rule down, twice if you have to."*

---

## Practical Block 3: Fixing Last Session's Broken Query (8 min)

**Activity:** Project last session's error query again: `SELECT COUNT(*) FROM orders WHERE SUM(price) > 1000;`. In pairs, students rewrite it correctly using GROUP BY and HAVING to find cities (or items) with total revenue above a threshold.

**Answer key with reasoning:** `SELECT city, SUM(price) AS total_revenue FROM orders GROUP BY city HAVING SUM(price) > 100;` - say aloud: *"Same business question that errored last week. The fix wasn't a small syntax tweak - it needed two new clauses working together."*

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

### 🔴 The trap / highest-value moment

> *"One more trap. After GROUP BY, can I still ORDER BY the original price column?"*
> Write `ORDER BY price DESC` after a grouped query and show the error or nonsense result.
> *"After grouping, price doesn't exist row-by-row anymore - only the aggregated column, total_revenue, exists in the output. Sort and filter using the NEW column names your aggregates created, not the raw columns they were built from."*

---

## Practical Block 4: Full KPI-Query Challenge (12 min)

**Activity:** Light competitive framing. Give the class 2–3 full combined business questions (e.g., "top 2 cities by total revenue, but only cities with more than 1 order," "average order value per item, sorted lowest to highest, items with fewer than 2 orders excluded") and have pairs race to build the complete query.

**Answer key with reasoning:** Insist pairs say the plain-English translation aloud, mapping each clause before typing SQL. Reveal answers one at a time, discussing WHERE-vs-HAVING mix-ups as they surface.

> 💬 **Expect at least one pair to put a raw-row condition inside HAVING instead of WHERE** (e.g., `HAVING city = 'Bengaluru'` instead of filtering it in WHERE). Welcome it. Say: *"That might even run without erroring - but ask yourself: is 'city' an aggregate result, or a raw column? Where does it actually belong?"*

---

## Summary & Bridge

**Recap table:**

| Concept | The one thing to remember |
|---|---|
| GROUP BY | Splits the table into groups; every SELECT column must be grouped or aggregated |
| Multiple aggregates | Any number can ride along in one grouped query, each scoped to its own group |
| HAVING | Filters groups AFTER aggregation - the fix for what WHERE can't do |
| Full clause order | SELECT → FROM → WHERE → GROUP BY → HAVING → ORDER BY → LIMIT, always in that sequence |

**Close on the thesis line:**

> *"At the start of today, the chai stall owner with 3 branches would have needed 3 separate queries. Now: one query, GROUP BY city, and you have every branch's numbers side by side - filtered, ranked, and trimmed to exactly what she asked for. WHERE filters rows. GROUP BY creates the groups. HAVING filters groups. Keep those three straight, and you can answer almost any 'by category' business question that comes your way."*

**Bridge to next session:**

> *"Everything today has come from ONE table - orders. Next session - Joining Tables Together - you learn to pull in a SECOND table, like a customers table with loyalty tier or signup date, so you can answer even richer questions: not just 'revenue by city,' but 'revenue by city, broken down by loyalty tier.' Same GROUP BY skill, richer data to group."*

---

## Q&A & Doubt Solving

**Q: Can I use HAVING without GROUP BY?**
→ Technically in some databases, but it's rarely meaningful - HAVING is built to filter *groups*, and without GROUP BY, the whole table is treated as one group. In this course, always pair HAVING with GROUP BY.

**Q: Can I GROUP BY more than one column at once?**
→ Yes - `GROUP BY city, item` creates a separate group for every unique city-and-item combination, not just every city. We'll use this more once we reach richer joined data next session.

**Q: Does the order of columns in GROUP BY matter?**
→ Less than in ORDER BY, but it's good practice to match your SELECT list's order for readability - the resulting groups are the same regardless of column order in GROUP BY itself.

**Q: Can I use an alias (like total_revenue) inside HAVING or ORDER BY?**
→ Most databases allow aliases in ORDER BY, but HAVING support for aliases varies - safest habit in this course is to repeat the full aggregate expression (`SUM(price)`) inside HAVING, and use the alias freely in ORDER BY.

**Q: What if a group has only 1 row - does AVG still work?**
→ Yes - AVG on a single-row group simply returns that one row's value, since sum ÷ count of 1 is just the value itself. It's mathematically valid, just worth remembering that a "1-order average" isn't very statistically meaningful.

---

## Instructor Notes

- **Words not yet earned:** Avoid `JOIN`, subqueries, CTEs, and window functions - JOIN arrives explicitly next session. If a student asks "can I group by something from a different table?", acknowledge that's exactly next session's topic rather than answering in full now.
- **The single biggest risk in this session** is the WHERE/HAVING confusion becoming a permanently sticky habit if not corrected firmly and repeatedly today. Defeat it with the same one-line test every time it surfaces: *"Raw column or aggregate? WHERE or HAVING?"* - say it as a chant, not just an explanation.
- **Board management:** Keep the full clause skeleton - `SELECT, FROM, WHERE, GROUP BY, HAVING, ORDER BY, LIMIT` - visible all session, and physically point to each clause as you build up the Concept Block 4 example piece by piece.
- **Common confusions, numbered:**
  1. Selecting a raw column that isn't in GROUP BY or wrapped in an aggregate.
  2. Assuming a grouped aggregate reflects the whole table rather than just its own group.
  3. Putting an aggregate condition in WHERE, or a raw-row condition in HAVING - the single most persistent SQL mistake and worth calling out by name every time it appears.
  4. Trying to ORDER BY a raw column (like price) after that column has been collapsed by GROUP BY.
- **Cross-references:** JOIN arrives next session, letting GROUP BY work across combined tables. Tableau's dimension/measure pill system (Module 3) and pandas' `.groupby()` (Module 4) are this exact same idea in different clothing - plant that connection explicitly in the bridge.
- **Local/cultural context:** The chai stall's growth from one stall to three branches is a deliberate callback thread - keep using "branch" language (not "store" or "location") consistently, since it'll resurface once JOIN introduces a linked `branches` or `riders` table.
