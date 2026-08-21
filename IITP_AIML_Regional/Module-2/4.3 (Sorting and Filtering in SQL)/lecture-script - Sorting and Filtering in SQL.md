# Lecture Script: SQL for Data Analysis - Sorting and Filtering in SQL
> **Instructor Reference** - Module 2: SQL for Data Analysis | Academic Session 10 | Duration: 1.5 Hours | Instructor: Industry Mentor

---

## Session Overview

**Goal:** Students can take a ranking question - "who's our top...", "what's our slowest..." - and answer it in a single query using `ORDER BY` and `LIMIT`, correctly combined with `WHERE`.

**Student profile at this point:** They've completed Session 9 (SELECT, WHERE, AND/OR) and are comfortable filtering rows. They have **not** yet sorted or ranked anything in SQL - every result so far has come back in whatever order the database happened to return it.

**Key outcome:** Students leave able to answer, unprompted, the two-part question every "top N" business request hides: *"Sorted by what, and how many do you actually want?"*

> 🎯 **The one sentence this session must land:** *Filtering tells the database which rows matter. Sorting and LIMIT tell it which of those rows matter MOST - and those are two different questions.*

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| Opening - "Which order came first?" (the unsorted-results problem) | 8 min | 8 min |
| Concept Block 1: ORDER BY | 8 min | 16 min |
| Practical Block 1: Sorting the orders table | 10 min | 26 min |
| Concept Block 2: Sorting by multiple columns | 10 min | 36 min |
| Practical Block 2: Priority-order sorting exercise | 10 min | 46 min |
| **BREAK** | 5 min | 51 min |
| Concept Block 3: LIMIT | 8 min | 59 min |
| Practical Block 3: Top-N challenge | 10 min | 69 min |
| Concept Block 4: WHERE + ORDER BY + LIMIT together | 10 min | 79 min |
| Practical Block 4: Full ranking-question challenge | 11 min | 90 min |

---

## Opening - "Which Order Came First?" (8 min)

Walk in with no slide up. Run this live query from last session (or show its output):

```sql
SELECT customer_name, price
FROM orders
WHERE city = 'Bengaluru';
```

> *"Last session, we filtered to Bengaluru orders. Now - quick question - which of these is the HIGHEST-priced Bengaluru order?"*

Let students scan the (small) result and answer - easy on 2 rows. Then say:

> *"That took you two seconds because I gave you 2 rows. Now imagine this table has 40,000 Bengaluru orders. Same question: which is the highest-priced? Raise your hand if you'd want to scroll through 40,000 rows to find out."*

Nobody will. Land the point:

> *"WHERE tells the database WHICH rows matter. It says nothing about which of those rows matter MOST. That's a completely different question, and it's what today is about."*

**Pivot line:**

> *"By the end of ninety minutes, you'll answer 'who's our top customer' or 'what's our slowest-moving item' in a single query - no scrolling, no guessing, regardless of whether the table has 4 rows or 4 million."*

**Context for the sessions ahead:** *"Sorting and 'top N' questions come back again and again - once GROUP BY arrives next week, you'll be ranking not just individual orders, but entire cities or customers by their totals. Today's ORDER BY and LIMIT are the exact same tools you'll reuse there."*

---

## Concept Block 1: ORDER BY (8 min)

### 💬 Instructor script

> *"Sorting in SQL uses one clause: ORDER BY. Tell it which column, and which direction."*

Write on the board:
```sql
SELECT customer_name, price
FROM orders
ORDER BY price ASC;
```

Walk through the output live - lowest price first. Then flip it:
```sql
ORDER BY price DESC;
```

### 🔴 The trap / highest-value moment

> *"Quick trap: if I write ORDER BY price with nothing after it - no ASC, no DESC - which way does it sort?"*
> Let students guess; many will assume "biggest first" since that often feels more useful. Correct them: *"Ascending is the default. Smallest first, always, unless you explicitly write DESC. Write this down: no direction stated means smallest to largest."*

---

## Practical Block 1: Sorting the Orders Table (10 min)

**Activity:** Individually, students write two queries against the `orders` table: (1) sort all orders by `quantity`, smallest first; (2) sort all orders by `order_date`, most recent first.

**Answer key with reasoning:** Query 1 uses `ORDER BY quantity` or `ORDER BY quantity ASC` (identical). Query 2 needs `ORDER BY order_date DESC` - say aloud: *"Most recent means the latest date, which is the largest date value chronologically - so DESC, not ASC."*

> 💬 **Expect confusion between "most recent" and "ascending."** Welcome it. Say: *"Dates work like numbers - later dates are 'bigger.' If 'most recent first' feels intuitively like it should be ASC, that's the trap. Translate 'most recent' into 'largest value' before picking ASC or DESC."*

---

## Concept Block 2: Sorting by Multiple Columns (10 min)

### 💬 Instructor script

> *"What if two rows tie on the column you're sorting by? SQL lets you add a second column as a tiebreaker."*

```sql
SELECT customer_name, city, price
FROM orders
ORDER BY city ASC, price DESC;
```

Walk through the output live: Bengaluru orders grouped together (alphabetical city first), and *within* Bengaluru, sorted by price, highest first.

### 🔴 The trap / highest-value moment

> *"Common misunderstanding: does that second column, price, re-sort the WHOLE table? No. It only breaks ties WITHIN rows that already share the same city. If every single row had a different city, the price column would never even come into play. Write this down: the second sort column only matters when the first one ties."*

---

## Practical Block 2: Priority-Order Sorting Exercise (10 min)

**Activity:** Pairs write a query sorting orders by `city` ascending, then by `quantity` descending within each city, using the fuller 15–20 row `orders` table from Session 9.

**Answer key with reasoning:** `ORDER BY city ASC, quantity DESC`. Walk one pair's output live and ask the room to confirm: *"Within Bengaluru specifically, is quantity actually descending? Check it row by row."*

> 💬 **Expect a pair to reverse the column order** (`ORDER BY quantity DESC, city ASC`) and get a technically valid but differently-meaningful result. Welcome it. Say: *"That's not wrong SQL - it's just answering a different question. Which one did the original business question actually ask for?"*

---

## BREAK (5 min)

---

## Concept Block 3: LIMIT (8 min)

### 💬 Instructor script

> *"A cricket scoreboard doesn't list every player who's ever batted - it shows the top run-scorers. LIMIT does exactly that for a query."*

```sql
SELECT customer_name, price
FROM orders
ORDER BY price DESC
LIMIT 3;
```

Walk through: only the 3 highest-priced orders come back.

### 🔴 The trap / highest-value moment

> *"Now watch this. I'm removing ORDER BY and keeping only LIMIT 3."*
> Run `SELECT customer_name, price FROM orders LIMIT 3;` live.
> *"These 3 rows - are they the 3 highest-priced? The 3 lowest? Neither. They're just whatever 3 rows the database happened to return first, which is not guaranteed to mean anything. Write this down: LIMIT without ORDER BY is not a 'top N' - it's a random N. The two clauses only become meaningful together."*

---

## Practical Block 3: Top-N Challenge (10 min)

**Activity:** Individually, students write: (1) the top 3 highest-quantity orders; (2) the single lowest-priced order overall.

**Answer key with reasoning:** `ORDER BY quantity DESC LIMIT 3;` and `ORDER BY price ASC LIMIT 1;`. Say aloud for the second: *"LIMIT 1 after an ascending sort is just a fast way to ask 'what's the single smallest value here' - no separate MIN function needed yet, though we'll meet one that does this more directly during Aggregation Essentials."*

> 💬 **Expect someone to write `LIMIT 1` without ORDER BY, remembering the trap from Concept Block 3 too late.** Welcome it - cold-call the room to catch the error before you point it out.

---

## Concept Block 4: WHERE + ORDER BY + LIMIT Together (10 min)

### 💬 Instructor script

> *"Real manager requests are almost never 'sort everything.' They're 'sort SOMETHING SPECIFIC.' That's WHERE narrowing the field first, then ORDER BY ranking what's left, then LIMIT trimming to the headline number."*

```sql
SELECT customer_name, price
FROM orders
WHERE city = 'Bengaluru'
ORDER BY price DESC
LIMIT 3;
```

Read it aloud in plain English, left to right: *"Start with orders. Keep only Bengaluru. Sort what's left, highest price first. Show me the top 3."*

### 🔴 The trap / highest-value moment

> *"The clause order is fixed: SELECT, FROM, WHERE, ORDER BY, LIMIT. Scramble it - put ORDER BY before WHERE, say - and SQL will error. When you get stuck writing a combined query, say it out loud in plain English first, in that exact order, then translate line by line. That habit will save you more time than anything else I teach you this session."*

---

## Practical Block 4: Full Ranking-Question Challenge (11 min)

**Activity:** Light competitive framing. Give the class 3–4 combined business questions (e.g., "top 2 highest-priced Hyderabad orders," "lowest-quantity order placed after Aug 1st") and have pairs race to translate and write the full query.

**Answer key with reasoning:** For each, insist pairs say the plain-English translation aloud before typing SQL - this is the actual transferable skill. Example: *"Top 2 highest-priced Hyderabad orders" → filter to Hyderabad, sort price descending, limit 2.*

> 💬 **Expect at least one pair to nail the WHERE and ORDER BY but forget LIMIT, returning every matching row instead of just the top few.** Welcome it. Say: *"Your query isn't wrong - it's just not finished. 'Top 2' is a promise your query needs to keep with LIMIT, not just imply with sorting."*

---

## Summary & Bridge

**Recap table:**

| Concept | The one thing to remember |
|---|---|
| ORDER BY | ASC is the default - smallest first, unless you write DESC |
| Multi-column sort | The second column only breaks ties within the first |
| LIMIT | Meaningless as a "top N" without ORDER BY first |
| WHERE + ORDER BY + LIMIT | Fixed clause order: filter, then rank, then trim |

**Close on the thesis line:**

> *"At the start of today, filtering to Bengaluru orders left you still scanning by eye to find the highest price. Now: `SELECT customer_name, price FROM orders WHERE city = 'Bengaluru' ORDER BY price DESC LIMIT 3;` - one query, filtered, ranked, and trimmed to exactly the headline number your manager actually wanted. Filtering tells the database which rows matter. Sorting and LIMIT tell it which of those rows matter MOST - and now you can answer both in the same breath."*

**Bridge to next session:**

> *"Next session - Aggregation Essentials - you stop ranking individual rows and start turning many rows into one number: total revenue, order count, average price. And notice: once we reach 'top 5 customers by total spend' in a couple of sessions, it'll be the exact same ORDER BY and LIMIT you used today, just applied to totals instead of single orders."*

---

## Q&A & Doubt Solving

**Q: Can I sort by a column I'm not selecting?**
→ Yes - just like WHERE, ORDER BY can reference any column in the table, even ones not included in your SELECT list.

**Q: What happens if two rows are completely identical across every sort column?**
→ Their relative order becomes unpredictable - the database doesn't guarantee a specific tiebreak beyond what you've told it to sort by. If exact, repeatable order matters, add another column (even a unique ID) to the ORDER BY list.

**Q: Is LIMIT the same in every database?**
→ The concept is universal, but the exact keyword varies - `LIMIT` in MySQL/PostgreSQL/SQLite, `TOP` in SQL Server (written differently, before SELECT's column list). We'll use `LIMIT` consistently in this course; know that the idea transfers even if the keyword changes on the job.

**Q: Can I use ORDER BY without WHERE?**
→ Yes - WHERE is optional. `SELECT ... FROM ... ORDER BY ...` sorts the entire table with no filtering at all, which is fine when you genuinely want every row ranked.

**Q: Does ORDER BY change the actual data in the table?**
→ No - it only changes the order of the *results returned to you*. The underlying table is completely unaffected, every time.

---

## Instructor Notes

- **Words not yet earned:** Avoid `GROUP BY`, `HAVING`, aggregate functions (`SUM`, `COUNT`, `AVG`, `MIN`, `MAX`), and window functions - these arrive starting next session (Aggregation Essentials) and later. If a student asks "can I sort by a total?", acknowledge that's coming very soon rather than answering in full now.
- **The single biggest risk in this session** is students treating ORDER BY as "obviously how it should work" and rushing past the ASC-default trap and the LIMIT-without-ORDER-BY trap. Both are quiet, easy-to-miss mistakes that produce a query which *runs* but *lies*. Slow down on both traps specifically - don't just mention them once.
- **Board management:** Keep the fixed clause order - `SELECT, FROM, WHERE, ORDER BY, LIMIT` - visible on the board all session. Point to it explicitly every time a student's query is scrambled.
- **Common confusions, numbered:**
  1. Assuming unlabeled `ORDER BY` sorts largest-first. It doesn't - ASC is the default.
  2. Believing a second sort column re-sorts the whole result rather than just breaking ties within the first column.
  3. Using `LIMIT` alone and treating the result as a meaningful "top N" without an `ORDER BY` to define what "top" means.
- **Cross-references:** ORDER BY and LIMIT reappear almost immediately once GROUP BY is introduced (ranking cities or customers by total, not just individual rows). Tableau's built-in sort controls and pandas' `.sort_values()` / `.head()` mirror this exact logic in later modules.
- **Local/cultural context:** The cricket-scoreboard analogy for LIMIT lands especially well with this cohort - consider reusing "top run-scorers" language again once ranking-by-total questions appear with GROUP BY.
