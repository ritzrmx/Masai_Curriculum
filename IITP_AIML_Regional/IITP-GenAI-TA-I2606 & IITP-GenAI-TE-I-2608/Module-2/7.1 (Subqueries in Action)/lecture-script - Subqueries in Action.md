# Lecture Script: SQL for Data Analysis - Subqueries in Action
> **Instructor Reference** - Module 2: SQL for Data Analysis | Academic Session 15 | Duration: 1.5 Hours | Instructor: Industry Mentor

---

## Session Overview

**Goal:** Students can write a query that needs another query's answer as an input - comparing rows to a calculated average, checking membership in a list, and aggregating safely in a subquery before joining or filtering further.

**Student profile at this point:** They completed Session 14 (join fan-out, fair comparisons, insight writing) and are now rightly a little suspicious of joins followed immediately by aggregation. That suspicion is the perfect setup for today - subqueries are the clean, structural fix for exactly the danger they just learned to fear.

**Key outcome:** Students leave able to recognise, unprompted, when a business question is secretly TWO questions stacked together - and to answer the inner one first, safely, before the outer one ever runs.

> 🎯 **The one sentence this session must land:** *Some questions can't be answered in one step - a subquery is how you answer the smaller question first, so the bigger question has something real to compare against.*

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| Opening - "Above average... than what?" | 8 min | 8 min |
| Concept Block 1: What is a subquery | 8 min | 16 min |
| Practical Block 1: Writing a first scalar subquery | 8 min | 24 min |
| Concept Block 2: Subqueries in WHERE | 10 min | 34 min |
| Practical Block 2: Comparing rows to a calculated value | 10 min | 44 min |
| **BREAK** | 5 min | 49 min |
| Concept Block 3: IN / NOT IN and the NULL trap | 12 min | 61 min |
| Practical Block 3: Finding customers who never ordered, two ways | 10 min | 71 min |
| Concept Block 4: Subqueries in FROM - the fan-out fix | 9 min | 80 min |
| Practical Block 4: Full subquery-in-FROM challenge | 10 min | 90 min |

---

## Opening - "Above Average... Than What?" (8 min)

Walk in and write on the board, nothing else: **"Find every order priced above average."**

> *"Simple enough sentence. Write me the WHERE clause for it - right now, using everything you already know."*

Let students try. Someone will likely write `WHERE price > average` or similar and get stuck.

> *"What number goes after that greater-than sign? You don't know yet - because 'average' isn't a number you were given. It's a number you'd have to CALCULATE first, from the very same table you're filtering."*

Let that land as a genuine puzzle for a moment.

> *"This is not a rare situation. 'Above average,' 'more than the typical customer,' 'never ordered' - a huge number of real business questions are secretly TWO questions folded into one sentence. Today, you learn how to answer the hidden first question before the second one ever runs."*

**Pivot line:**

> *"By the end of ninety minutes, you'll write queries that calculate their own comparison value on the fly - and, as a bonus, you'll have the cleanest possible fix for last session's join fan-out trap."*

**Context for the sessions ahead:** *"Everything you write today with a subquery, you'll be able to write again next session in a cleaner, more readable form called a CTE. Today builds the concept; next session gives it better handwriting."*

---

## Concept Block 1: What Is a Subquery (8 min)

### 💬 Instructor script

> *"A subquery is just a complete SELECT statement, living inside another query's parentheses. The inner one runs first, produces one answer, and the outer query uses that answer."*

```sql
SELECT order_id, price
FROM orders
WHERE price > (SELECT AVG(price) FROM orders);
```

Run the inner query alone first, live: `SELECT AVG(price) FROM orders;` → 120. Then show it embedded in the full query, and the single row (order 2, ₹150) that comes back.

### 🔴 The trap / highest-value moment

> *"Watch what happens if I drop the parentheses."*
> Write `WHERE price > SELECT AVG(price) FROM orders` without parentheses and run it - let the error appear.
> *"SQL needs the inner query clearly boxed off from the outer one. No parentheses, no subquery - just a syntax error. Write this down: every subquery lives inside parentheses, no exceptions."*

---

## Practical Block 1: Writing a First Scalar Subquery (8 min)

**Activity:** Individually, students write a query for orders priced *below* the overall average.

**Answer key with reasoning:** `WHERE price < (SELECT AVG(price) FROM orders);` → 1 row (₹90, Priya's order) - because `<` is strictly less than, the two ₹120 orders sit exactly AT the average and don't qualify. Say aloud: *"This is worth checking carefully: below average, above average, and exactly-at-average should together account for every single row. Two orders sit exactly at ₹120 - neither the below-average nor the above-average query picks them up. Always verify your row counts add up to the total."*

> 💬 **Expect someone to try nesting the inner query with its own WHERE clause and get confused by two WHEREs in one query.** Welcome it. Say: *"Totally valid - the inner query can have its own WHERE, GROUP BY, anything a normal query can have. It's a full, independent query; it just happens to be living inside another one."*

---

## Concept Block 2: Subqueries in WHERE (10 min)

### 💬 Instructor script

> *"Real business question: which CUSTOMERS placed an order above average - not just which orders?"*

```sql
SELECT DISTINCT customers.customer_name
FROM customers
INNER JOIN orders ON customers.customer_id = orders.customer_id
WHERE orders.price > (SELECT AVG(price) FROM orders);
```

Run it live: Fatima, and only Fatima.

> *"Notice the JOIN and the subquery are doing two completely different jobs here - JOIN connects customers to their orders; the subquery calculates the comparison value. Neither replaces the other."*

### 🔴 The trap / highest-value moment

> *"Now the big one. What if my subquery could return MORE than one row, and I'm still using a single-value operator like equals or greater-than?"*
> Write `WHERE orders.price = (SELECT price FROM orders WHERE item = 'Veg Thali')` and run it live - there are 2 Veg Thali orders, both priced ₹120, so the inner query returns 2 rows.
> *"In most databases - MySQL, PostgreSQL, SQL Server - this would error immediately with 'subquery returned more than 1 row.' Watch what SQLite does instead."*
> Run it and show the result - it runs without error, silently using one of the two ₹120 values.
> *"No error. No warning. Just a query that happened to work today because both Veg Thali orders are coincidentally the same price - try this on data where they're NOT the same price, and you'd get a technically-successful query with an arbitrarily wrong answer. SQL has no reliable way to compare one number to a LIST of values using equals, and SQLite won't always stop you from trying. Before you ever use =, >, or < with a subquery, ask yourself: could this inner query possibly return more than one row? Never rely on your specific database catching the mistake for you."*

---

## Practical Block 2: Comparing Rows to a Calculated Value (10 min)

**Activity:** Pairs write a query for customers whose order quantity is above the average quantity across all orders.

**Answer key with reasoning:** `WHERE orders.quantity > (SELECT AVG(quantity) FROM orders);` → average quantity is 1.75, so Ramesh (quantity 2) and Priya (quantity 3) both qualify - walk through live, confirming the subquery genuinely returns a single number before the outer query runs.

> 💬 **Expect a pair to accidentally write a subquery that could return multiple rows for this exercise too, hitting the same error live.** Welcome it - it's exactly the reinforcement this exercise is designed to produce. Ask: *"What does that error message actually mean, in your own words?"* before helping fix it.

---

## BREAK (5 min)

---

## Concept Block 3: IN / NOT IN and the NULL Trap (12 min)

### 💬 Instructor script

> *"'Which customers have NEVER ordered' is a different shape of question entirely - it's not comparing to ONE value, it's checking membership against an entire LIST. That's what IN and NOT IN are for."*

```sql
SELECT customer_name
FROM customers
WHERE customer_id NOT IN (SELECT customer_id FROM orders);
```

Run it live: Karthik. Confirm it matches Session 13's LEFT JOIN answer for the exact same business question, just written differently.

### 🔴 The trap / highest-value moment

> *"Here's the single most dangerous trap in this entire session - and it doesn't error. It just quietly gives you the wrong answer."*
> Demonstrate live: temporarily insert a NULL customer_id into a copy of orders (or describe it clearly if live demo isn't feasible), then rerun the NOT IN query - show it now returns **zero rows**, not Karthik.
> *"NOT IN, combined with even ONE NULL anywhere in that inner list, breaks the entire comparison silently - no error, just an empty result that LOOKS like 'nobody matched' when that's not actually true. This has genuinely cost real companies real money in production systems. The safe habit: before trusting NOT IN, check that column can't contain NULLs - or just use LEFT JOIN with an IS NULL check instead, which never has this problem."*

---

## Practical Block 3: Finding Customers Who Never Ordered, Two Ways (10 min)

**Activity:** Pairs write the "customers who never ordered" question BOTH as a `NOT IN` subquery AND as a `LEFT JOIN ... WHERE ... IS NULL`, and confirm both return Karthik.

**Answer key with reasoning:**
```sql
-- NOT IN version
SELECT customer_name FROM customers
WHERE customer_id NOT IN (SELECT customer_id FROM orders);

-- LEFT JOIN version
SELECT customers.customer_name FROM customers
LEFT JOIN orders ON customers.customer_id = orders.customer_id
WHERE orders.order_id IS NULL;
```
Both return Karthik here since there's no NULL customer_id in this dataset - the point is the *habit*, not a different answer today.

> 💬 **Expect a pair to ask "so which one should I just always use?"** Welcome it. Say: *"Given today's trap, LEFT JOIN with IS NULL is the safer default in professional work - NOT IN isn't wrong, it's just one accidental NULL away from a silent bug. Prefer the version that fails loudly, or doesn't fail at all, over the version that fails silently."*

---

## Concept Block 4: Subqueries in FROM - The Fan-Out Fix (9 min)

### 💬 Instructor script

> *"Last session, joining orders to customer_addresses duplicated Ramesh's order and inflated his revenue from 120 to 240. What if we aggregate FIRST, before any join that could duplicate rows happens?"*

```sql
SELECT city_totals.city, city_totals.total_revenue
FROM (
    SELECT customers.city, SUM(orders.price) AS total_revenue
    FROM customers
    INNER JOIN orders ON customers.customer_id = orders.customer_id
    GROUP BY customers.city
) AS city_totals
WHERE city_totals.total_revenue > 100;
```

Run it live: Bengaluru 240, Hyderabad 150 - Chennai's 90 correctly dropped.

> *"The inner subquery does the join-and-group-by ONCE, cleanly. By the time the outer query's WHERE runs, the numbers are already correct - there's no later join left that could still duplicate anything."*

### 🔴 The trap / highest-value moment

> *"One easy-to-miss requirement: try removing the alias - the 'AS city_totals' part - and run it."*
> Remove `AS city_totals` and run it live - let the error appear.
> *"SQL requires a name for anything that acts like a table, even a temporary one built on the fly inside FROM. No alias, no valid query. Always name your subquery in FROM."*

---

## Practical Block 4: Full Subquery-in-FROM Challenge (10 min)

**Activity:** Pairs write a subquery-in-FROM query calculating total revenue per loyalty tier, then filtering the outer query to tiers above ₹200.

**Answer key with reasoning:**
```sql
SELECT tier_totals.loyalty_tier, tier_totals.total_revenue
FROM (
    SELECT customers.loyalty_tier, SUM(orders.price) AS total_revenue
    FROM customers
    INNER JOIN orders ON customers.customer_id = orders.customer_id
    GROUP BY customers.loyalty_tier
) AS tier_totals
WHERE tier_totals.total_revenue > 200;
```
Result: Silver (270) only - Gold's 210 also clears it actually, so expect both Silver and Gold depending on the exact threshold; walk through the real output live and adjust the threshold discussion accordingly.

> 💬 **Expect a pair to try filtering with HAVING instead inside the subquery, then WHERE again outside.** Welcome it - ask: *"Could you have just used HAVING inside the subquery and skipped the outer WHERE entirely? What's the difference in the end result?"* (There often isn't one for this specific case - a good moment to discuss that SQL frequently offers more than one valid path to the same answer.)

---

## Summary & Bridge

**Recap table:**

| Concept | The one thing to remember |
|---|---|
| What is a subquery | A complete query nested in parentheses, answering a smaller question first |
| Subqueries in WHERE | Only safe with =/>/< if the inner query returns exactly one row |
| IN / NOT IN | For checking membership in a list - but NOT IN silently breaks on a NULL in that list |
| Subqueries in FROM | Aggregate once, safely, inside the subquery - before any risky join happens |

**Close on the thesis line:**

> *"At the start of today, 'above average' was a question you couldn't even write the WHERE clause for. Now: a subquery answers the hidden first question, so the bigger question has something real to compare against. And as a bonus, you now have the cleanest fix for last session's fan-out trap - aggregate first, in a subquery, then filter or join on numbers you already know are correct."*

**Bridge to next session:**

> *"Everything you wrote today works - but nested subqueries inside subqueries can get genuinely hard to read fast. Next session - CTEs and GenAI for SQL - you learn a cleaner way to write exactly what you did today, using a WITH clause that reads top to bottom like a recipe instead of nested parentheses. And we'll cover something else important: how to use GenAI to draft SQL like this safely, without blindly trusting what it hands you."*

---

## Q&A & Doubt Solving

**Q: Can a subquery go anywhere else besides WHERE and FROM?**
→ Yes - subqueries can also appear in SELECT (to compute a per-row calculated column) and in HAVING. We've covered the two most common and highest-value uses today; you'll encounter the others naturally as your queries get more advanced.

**Q: Is a subquery always slower than a JOIN?**
→ Not necessarily - it depends on the database and the specific query. For now, focus on correctness and readability; performance tuning is a more advanced skill for later in your career.

**Q: Can I nest a subquery inside another subquery?**
→ Technically yes, but readability suffers fast, which is exactly why CTEs (next session) exist - they let you name each step instead of nesting parentheses inside parentheses inside parentheses.

**Q: Does the subquery in FROM run once, or once per outer row?**
→ Once - it's calculated as its own complete result first, then the outer query treats that result as a normal (if temporary) table. This is part of why it's safe from the fan-out problem: the aggregation happens exactly once, before anything else touches it.

**Q: If NOT IN is risky, why does it still exist / get used?**
→ It's perfectly safe and often more readable when you're certain the inner column has no NULLs - many real datasets genuinely don't. The trap only bites when that assumption turns out to be wrong, which is exactly why checking first (or defaulting to LEFT JOIN + IS NULL) is the safer habit.

---

## Instructor Notes

- **Database-specific behaviour to know before class:** This module's database is SQLite, which does **not** raise an error for a multi-row scalar subquery the way MySQL/PostgreSQL/SQL Server do - it silently uses one arbitrary row instead. The Concept Block 2 demo is written around this actual SQLite behavior (no error appears; the class needs to be told explicitly that other databases WOULD error here). Don't promise students they'll see an error message during the live demo - they won't, and that's the point.
- **Words not yet earned:** Avoid `WITH`/CTEs (arriving explicitly next session), window functions, and correlated subqueries (where the inner query references the outer row) - today stays with non-correlated subqueries only, which is the appropriate depth for this stage.
- **The single biggest risk in this session** is students treating subqueries as "just another way to write a JOIN" without grasping WHY each shape exists - the "more than 1 row" error and the NOT IN/NULL trap are the two moments that make the distinction real. Don't rush either.
- **Board management:** Keep the four subquery shapes - scalar (WHERE with =/>/<), list (WHERE with IN/NOT IN), FROM (aliased temp table) - visible all session as a running reference, updated after each Concept Block.
- **Common confusions, numbered:**
  1. Forgetting parentheses around a subquery.
  2. Using =/>/< with a subquery that could return more than one row.
  3. Trusting NOT IN without checking whether the inner column could contain NULLs.
  4. Forgetting to alias a subquery used in FROM.
- **Cross-references:** CTEs next session rewrite every subquery from today in cleaner syntax - explicitly promise this in the bridge so students don't feel today's syntax is "the only way" going forward. The NOT IN/NULL trap reappears conceptually in Module 4 (pandas' handling of missing values) - worth a one-line callback when you reach it there.
- **Local/cultural context:** Keep using Ramesh (fan-out), Karthik (never ordered), and Fatima (above-average order) as the running named examples - students have built familiarity with this exact cast since Session 13, and reusing them keeps cognitive load on the new SQL concept, not on re-learning a new story.
