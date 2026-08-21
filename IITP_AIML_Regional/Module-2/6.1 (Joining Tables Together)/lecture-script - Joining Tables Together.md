# Lecture Script: SQL for Data Analysis - Joining Tables Together
> **Instructor Reference** - Module 2: SQL for Data Analysis | Academic Session 13 | Duration: 1.5 Hours | Instructor: Industry Mentor

---

## Session Overview

**Goal:** Students can explain why data lives in multiple related tables, write an `INNER JOIN` to combine matching rows, write a `LEFT JOIN` to preserve unmatched rows, and combine either with `WHERE`/`GROUP BY` to answer a richer business question.

**Student profile at this point:** They've completed Sessions 9–12 (SELECT, WHERE, ORDER BY, LIMIT, aggregation, GROUP BY, HAVING) - all on a single `orders` table. Today is their **first time working with two tables at once.**

**Key outcome:** Students leave able to answer, unprompted, the two-part question every JOIN silently requires: *"Do these two tables share a key I can match on - and do I want only matches, or everything from one side regardless?"*

> 🎯 **The one sentence this session must land:** *Almost no real business question lives inside a single table - JOIN is how you make two tables answer a question that neither one could answer alone.*

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| Opening - "Where did the customer's city go?" | 8 min | 8 min |
| Concept Block 1: Why two tables - meet customers | 10 min | 18 min |
| Practical Block 1: Reading the two tables before joining | 8 min | 26 min |
| Concept Block 2: INNER JOIN | 10 min | 36 min |
| Practical Block 2: Writing INNER JOIN queries | 10 min | 46 min |
| **BREAK** | 5 min | 51 min |
| Concept Block 3: LEFT JOIN | 10 min | 61 min |
| Practical Block 3: Finding the missing customer | 10 min | 71 min |
| Concept Block 4: JOIN + WHERE/GROUP BY | 8 min | 79 min |
| Practical Block 4: Full joined-KPI challenge | 11 min | 90 min |

---

## Opening - "Where Did the Customer's City Go?" (8 min)

Walk in and project last session's `orders` table - but this time with `customer_name` and `city` columns already removed, replaced by just a `customer_id`.

> *"Quick question. Where did customer_name and city go? Last week's orders table had them right there."*

Let confusion land for a beat, then reveal the `customers` table alongside it.

> *"They didn't disappear. They moved - into a second table. From today, this business runs on TWO tables instead of one. Why would anyone deliberately split their data apart like that?"*

Take a guess or two, then land the real-world reason:

> *"Imagine Ramesh moves from Bengaluru to Chennai. In last week's design, you'd have to find and update EVERY order row he's ever placed. In today's design, you update his city ONCE, in the customers table, and it's correct everywhere instantly. This is called normalization, and it's how almost every real company database is actually built."*

**Pivot line:**

> *"By the end of ninety minutes, you'll combine these two tables back together whenever you need to - pulling in customer details alongside their orders - using one new clause: JOIN."*

**Context for the sessions ahead:** *"This is, without exaggeration, the single most-used skill in professional SQL. Almost no real business question - 'revenue by loyalty tier,' 'customers who never ordered' - lives inside just one table. Today's skill is the one you'll use constantly, for the rest of your career, not just this course."*

---

## Concept Block 1: Why Two Tables - Meet customers (10 min)

### 💬 Instructor script

Project both tables side by side. Point out the shared column: `customer_id` in both.

> *"This shared column is called a key - it's the thread connecting a row in one table to a row in the other. customer_id 1 in customers is the same real person as customer_id 1 in orders. Everything today depends on that shared thread."*

### 🔴 The trap / highest-value moment

> *"Point at Karthik, customer_id 5, in the customers table. Does he have any rows in orders?"*
> Let the room check - no, he doesn't. *"Hold onto that. Karthik signed up but never ordered. He's about to matter a lot in about forty minutes - write his name down."*

---

## Practical Block 1: Reading the Two Tables Before Joining (8 min)

**Activity:** In pairs, before writing any SQL, students answer verbally: Which column exists in both tables? For customer_id 3, what's their name, city, and loyalty tier? Which customer(s) have zero matching orders?

**Answer key with reasoning:** Shared column = `customer_id`. Customer 3 = Arjun, Bengaluru, Silver. Zero-order customer = Karthik (id 5).

> 💬 **Expect a pair to try matching on `customer_name` instead of `customer_id`.** Welcome it. Say: *"Names can have typos, duplicates, or spelling variations across two systems - IDs generally can't. This is exactly why databases use ID-based keys instead of names to link tables, even though it's less human-readable at a glance."*

---

## Concept Block 2: INNER JOIN (10 min)

### 💬 Instructor script

> *"Time to reconnect the two tables. INNER JOIN says: 'match rows using the shared key, and only keep rows where a match was actually found on both sides.'"*

```sql
SELECT orders.order_id, customers.customer_name, orders.item, orders.price
FROM orders
INNER JOIN customers
  ON orders.customer_id = customers.customer_id;
```

Walk through the output live, row by row, physically tracing which `orders` row matched which `customers` row via the shared ID.

### 🔴 The trap / highest-value moment

> *"Where's Karthik in this result?"*
> Let the room scan - he's nowhere. *"Exactly. INNER JOIN only keeps rows that matched on BOTH sides. Karthik has no order, so he has no match, so INNER JOIN silently drops him. That word 'silently' should worry you a little - if you're trying to find customers who've never ordered, INNER JOIN will actively hide the exact answer you're looking for."*

---

## Practical Block 2: Writing INNER JOIN Queries (10 min)

**Activity:** Pairs write an INNER JOIN query showing `item` and `city` for every order.

**Answer key with reasoning:** `SELECT orders.item, customers.city FROM orders INNER JOIN customers ON orders.customer_id = customers.customer_id;` - 4 rows, one per order, since Karthik contributes no order rows to match against.

> 💬 **Expect a pair to accidentally write `ON orders.order_id = customers.customer_id`** (matching two unrelated ID columns). Welcome it - run it live and let the nonsensical or empty result appear. Say: *"This is technically valid SQL that runs without error - and returns garbage, because order_id and customer_id were never meant to be compared to each other. A JOIN can run cleanly and still be completely wrong. Always sanity-check what your ON condition is actually claiming."*

---

## BREAK (5 min)

---

## Concept Block 3: LEFT JOIN (10 min)

### 💬 Instructor script

> *"Remember Karthik. What if the actual business question is 'show me every customer, INCLUDING ones who've never ordered'? INNER JOIN can't do that - it needs a match. LEFT JOIN can."*

```sql
SELECT customers.customer_name, orders.item, orders.price
FROM customers
LEFT JOIN orders
  ON customers.customer_id = orders.customer_id;
```

Walk through live - Karthik now appears, with blank/NULL `item` and `price`.

### 🔴 The trap / highest-value moment

> *"Notice which table came FIRST in the FROM clause this time - customers, not orders. LEFT JOIN keeps every row from whichever table is on the LEFT - the one named right after FROM. Swap the table order, and you'd get a completely different result. Write this down: 'left' means the table named in FROM, not just a general direction."*

---

## Practical Block 3: Finding the Missing Customer (10 min)

**Activity:** Pairs write a `LEFT JOIN` query starting from `customers`, then identify - by reading the output - exactly which customer has NULL order data.

**Answer key with reasoning:** Karthik, customer_id 5 - confirmed as the only row with blank `item`/`price`. Bonus discussion: to isolate ONLY the customers with no orders (not the whole joined table), you'd add `WHERE orders.order_id IS NULL` - worth demonstrating live if time allows, as a genuine "find the gap" business technique.

> 💬 **Expect someone to ask "why is it called LEFT if it's really about the FROM table?"** Welcome it - it's a fair naming question. Say: *"SQL was designed to read left to right: FROM table on the left, JOIN table on the right of it in the query text. The name reflects the query's layout, not a real-world direction."*

---

## Concept Block 4: JOIN + WHERE/GROUP BY (8 min)

### 💬 Instructor script

> *"Once two tables are joined, every clause you already know still works - exactly as if it had always been one table."*

```sql
SELECT customers.loyalty_tier, SUM(orders.price) AS total_revenue
FROM customers
INNER JOIN orders
  ON customers.customer_id = orders.customer_id
GROUP BY customers.loyalty_tier
ORDER BY total_revenue DESC;
```

Walk through live: Gold and Silver tiers, each with a total revenue figure - a question neither table alone could answer, since `orders` has no loyalty_tier column and `customers` has no price column.

### 🔴 The trap / highest-value moment

> *"Notice every column reference here has a table name in front of it - customers.loyalty_tier, orders.price. Once two tables are joined, if both happen to share a column name, or if it's ambiguous which table a column belongs to, SQL will refuse to guess and throw an error. Get in the habit of prefixing column names with their table now, even when it feels unnecessary - it will save you a confusing error later."*

---

## Practical Block 4: Full Joined-KPI Challenge (11 min)

**Activity:** Light competitive framing. Give the class 2–3 combined business questions (e.g., "total revenue by city, using the joined tables," "which customers have never placed an order") and have pairs race to build the full query.

**Answer key with reasoning:** For the "never ordered" question specifically, insist pairs justify their choice of `LEFT JOIN` over `INNER JOIN` out loud before writing SQL - this is the actual transferable judgment call, not just syntax.

> 💬 **Expect a pair to default to INNER JOIN out of habit** for the "never ordered" question, since it was taught first. Welcome it - run their query live, show that Karthik is (predictably) missing from the result, and ask: *"Does this actually answer the question that was asked?"*

---

## Summary & Bridge

**Recap table:**

| Concept | The one thing to remember |
|---|---|
| Why two tables | Normalization avoids repeating (and risking inconsistent copies of) the same data everywhere |
| INNER JOIN | Keeps only rows matched on both sides - silently drops anything unmatched |
| LEFT JOIN | Keeps every row from the FROM table, matched or not - unmatched rows get NULLs |
| JOIN + WHERE/GROUP BY | Every clause you already know works on the combined result, exactly as before |

**Close on the thesis line:**

> *"At the start of today, customer_name and city had vanished from orders, and it looked like a step backward. Now you know why - and you know how to bring them right back whenever you need them, using INNER JOIN or LEFT JOIN depending on whether unmatched rows like Karthik's should be dropped or kept. Almost no real business question lives inside a single table. JOIN is how you make two tables answer a question that neither one could answer alone."*

**Bridge to next session:**

> *"Today you learned to COMBINE two tables into one richer result. Next session - Insights from Combined Data - you learn what to actually DO with that result: how to read a joined, grouped table and write the one or two sentences a manager actually needs, not just the numbers themselves."*

---

## Q&A & Doubt Solving

**Q: Can I join more than two tables in one query?**
→ Yes - you can chain multiple JOIN clauses, each with its own ON condition, to bring in a third, fourth, or more related tables. We'll practice this more as the module continues.

**Q: What's the difference between JOIN and INNER JOIN?**
→ None - `JOIN` alone defaults to `INNER JOIN` in virtually every SQL database. Writing `INNER JOIN` explicitly is just clearer to read, especially while learning.

**Q: Is there a RIGHT JOIN too?**
→ Yes - it's the mirror image of LEFT JOIN, keeping every row from the second (right) table instead. In practice, most analysts just rewrite the table order and use LEFT JOIN instead of reaching for RIGHT JOIN, since it reads more naturally left to right.

**Q: What if two rows in orders both point to the same customer_id - does JOIN handle that fine?**
→ Yes - that's exactly the normal case (a customer with multiple orders). Each matching order row gets its own row in the joined result, each carrying the same customer details alongside it.

**Q: Can I use an aggregate function and a JOIN in the same query as GROUP BY?**
→ Yes - that's exactly what today's Concept Block 4 example does. JOIN happens first to combine the tables, then GROUP BY and the aggregate function work on the combined result exactly as they did on a single table.

---

## Instructor Notes

- **Words not yet earned:** Avoid subqueries, CTEs, and multi-table joins beyond two tables - subqueries and CTEs arrive in the next two sessions. If a student asks about joining three or more tables, acknowledge it's a natural extension they'll get more practice with soon, without a full demonstration today.
- **The single biggest risk in this session** is students treating INNER JOIN as the "default correct choice" simply because it's taught first, and reaching for it automatically even when a question specifically needs LEFT JOIN. Defeat it by returning to Karthik by name at every opportunity - he's the concrete anchor for "when does INNER JOIN silently hide the answer?"
- **Board management:** Keep both tables - `customers` and `orders` - visible side by side on the board all session, with the shared `customer_id` column visually highlighted or circled in both.
- **Common confusions, numbered:**
  1. Believing the two tables are "the same data, just reorganized" rather than genuinely separate, related tables.
  2. Joining on the wrong pair of columns (e.g., two unrelated ID columns) and getting a technically-valid but meaningless result.
  3. Defaulting to INNER JOIN when the business question specifically requires preserving unmatched rows.
  4. Forgetting to prefix column names with their table name once two tables are joined, especially when column names could be ambiguous.
- **Cross-references:** Subqueries (next-but-one session) and CTEs (the session after that) both build directly on today's JOIN skill, often used to prepare data before joining it. Tableau's "relationships" and "blending" features and pandas' `.merge()` in Module 4 are this exact same idea under different names.
- **Local/cultural context:** Keep Karthik's storyline (signed up, never ordered) alive as a running example - it resurfaces naturally in Session 14 (Insights from Combined Data) as a genuine "customers at risk of churn" business insight.
