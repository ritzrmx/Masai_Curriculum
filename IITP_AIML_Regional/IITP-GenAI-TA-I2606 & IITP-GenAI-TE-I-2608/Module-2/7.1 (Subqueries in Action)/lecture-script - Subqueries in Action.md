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

*The core flow fills all 90 minutes. Concept/Practical Block 5, on correlated subqueries in SELECT (a per-row calculated column), is in the Extension Blocks section - use only if ahead of pace, and flag it explicitly as a preview beyond this session's core scope.*

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

**Materials note:** this session continues against the same `customers` / `orders` / `customer_addresses` schema from Sessions 13–14 (`SQL Files/module2_phase2_sessions_6.1_to_6.2.db`):

```
customers: customer_id, customer_name, city, loyalty_tier   (5 rows - Karthik has no orders)
orders: order_id, customer_id, item, quantity, price, order_date   (4 rows)
customer_addresses: customer_id, address_label   (5 rows - Ramesh has 2)
```

---

## Concept Block 1: What Is a Subquery (8 min)

### 💬 Instructor script

> *"A subquery is just a complete SELECT statement, living inside another query's parentheses. The inner one runs first, produces one answer, and the outer query uses that answer."*

```sql
SELECT order_id, price
FROM orders
WHERE price > (SELECT AVG(price) FROM orders);
```

Run the inner query alone first, live: `SELECT AVG(price) FROM orders;` → **120.0** (verified). Then show it embedded in the full query.

**Verified output of the full query:**
```
order_id  price
--------  -----
2         150
```

Only order 2 (Fatima's, ₹150) is above the ₹120 average.

### 🔴 The trap / highest-value moment

> *"Watch what happens if I drop the parentheses."*
> Write `WHERE price > SELECT AVG(price) FROM orders` without parentheses and run it - let the error appear.

**Verified error:**
```
Error: in prepare, near "SELECT": syntax error
  SELECT order_id, price FROM orders WHERE price > SELECT AVG(price) FROM orders;
                                                    error here ---^
```

> *"SQL needs the inner query clearly boxed off from the outer one. No parentheses, no subquery - just a syntax error. Write this down: every subquery lives inside parentheses, no exceptions."*

---

## Practical Block 1: Writing a First Scalar Subquery (8 min)

**Activity:** Individually, students write a query for orders priced *below* the overall average.

**Answer key with verified output:**

```sql
SELECT order_id, price
FROM orders
WHERE price < (SELECT AVG(price) FROM orders);
```
```
order_id  price
--------  -----
4         90
```

1 row (₹90, Priya's order) - because `<` is strictly less than, the two ₹120 orders sit exactly AT the average and don't qualify. Say aloud: *"This is worth checking carefully: below average, above average, and exactly-at-average should together account for every single row. Two orders sit exactly at ₹120 - neither the below-average nor the above-average query picks them up. Always verify your row counts add up to the total."*

**Verify that add-up live, as the script itself insists on:**
```sql
SELECT
  (SELECT COUNT(*) FROM orders WHERE price < (SELECT AVG(price) FROM orders)) AS below,
  (SELECT COUNT(*) FROM orders WHERE price = (SELECT AVG(price) FROM orders)) AS at_avg,
  (SELECT COUNT(*) FROM orders WHERE price > (SELECT AVG(price) FROM orders)) AS above;
```
```
below  at_avg  above
-----  ------  -----
1      2       1
```

> *"1 + 2 + 1 = 4, exactly the full table. That's the check passing. If those three numbers didn't sum to your total row count, you'd know immediately something was off - a NULL price, a typo in one of the three conditions, something worth chasing down before trusting any of the three results."*

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

**Verified output:**
```
customer_name
-------------
Fatima
```

> *"Notice the JOIN and the subquery are doing two completely different jobs here - JOIN connects customers to their orders; the subquery calculates the comparison value. Neither replaces the other."*

### 🔴 The trap / highest-value moment

> *"Now the big one. What if my subquery could return MORE than one row, and I'm still using a single-value operator like equals or greater-than?"*
> Write `WHERE orders.price = (SELECT price FROM orders WHERE item = 'Veg Thali')` and run it live - there are 2 Veg Thali orders, both priced ₹120, so the inner query returns 2 rows.

**Verified: the inner query alone returns 2 rows:**
```sql
SELECT price FROM orders WHERE item = 'Veg Thali';
```
```
price
-----
120
120
```

> *"In most databases - MySQL, PostgreSQL, SQL Server - this would error immediately with 'subquery returned more than 1 row.' Watch what SQLite does instead."*
> Run it and show the result - it runs without error, silently using one of the two ₹120 values.

**Verified full query - no error, a clean-looking result:**
```sql
SELECT order_id, price FROM orders WHERE price = (SELECT price FROM orders WHERE item = 'Veg Thali');
```
```
order_id  price
--------  -----
1         120
3         120
```

> *"No error. No warning. Just a query that happened to work today because both Veg Thali orders are coincidentally the same price - try this on data where they're NOT the same price, and you'd get a technically-successful query with an arbitrarily wrong answer. SQL has no reliable way to compare one number to a LIST of values using equals, and SQLite won't always stop you from trying. Before you ever use =, >, or < with a subquery, ask yourself: could this inner query possibly return more than one row? Never rely on your specific database catching the mistake for you."*

---

## Practical Block 2: Comparing Rows to a Calculated Value (10 min)

**Activity:** Pairs write a query for customers whose order quantity is above the average quantity across all orders.

**Answer key with verified output:**

```sql
SELECT customers.customer_name, orders.quantity
FROM customers
INNER JOIN orders ON customers.customer_id = orders.customer_id
WHERE orders.quantity > (SELECT AVG(quantity) FROM orders);
```
```
customer_name  quantity
-------------  --------
Ramesh         2
Priya          3
```

Average quantity is 1.75, so Ramesh (quantity 2) and Priya (quantity 3) both qualify - walk through live, confirming the subquery genuinely returns a single number before the outer query runs.

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

**Verified output:**
```
customer_name
-------------
Karthik
```

### 🔴 The trap / highest-value moment

> *"Here's the single most dangerous trap in this entire session - and it doesn't error. It just quietly gives you the wrong answer."*
> Demonstrate live: temporarily insert a NULL customer_id into a copy of orders (or describe it clearly if live demo isn't feasible), then rerun the NOT IN query - show it now returns **zero rows**, not Karthik.

**Verified - this exact demonstration, run safely without modifying the real table, by unioning a NULL directly into the subquery's result:**
```sql
SELECT customer_name
FROM customers
WHERE customer_id NOT IN (SELECT customer_id FROM orders UNION SELECT NULL);
```
```
(0 rows returned)
```

> *"NOT IN, combined with even ONE NULL anywhere in that inner list, breaks the entire comparison silently - no error, just an empty result that LOOKS like 'nobody matched' when that's not actually true. This has genuinely cost real companies real money in production systems. The safe habit: before trusting NOT IN, check that column can't contain NULLs - or just use LEFT JOIN with an IS NULL check instead, which never has this problem."*

**Prove the LEFT JOIN version doesn't have this blind spot, using the same NULL-injected list:**
```sql
SELECT customers.customer_name
FROM customers
LEFT JOIN (SELECT customer_id FROM orders UNION SELECT NULL) AS orders_with_null
  ON customers.customer_id = orders_with_null.customer_id
WHERE orders_with_null.customer_id IS NULL;
```
```
customer_name
-------------
Karthik
```

> *"Same poisoned list, same NULL sitting in it - and LEFT JOIN with IS NULL still correctly finds Karthik. That's the concrete proof of why this is the safer default, not just a theoretical preference."*

---

## Practical Block 3: Finding Customers Who Never Ordered, Two Ways (10 min)

**Activity:** Pairs write the "customers who never ordered" question BOTH as a `NOT IN` subquery AND as a `LEFT JOIN ... WHERE ... IS NULL`, and confirm both return Karthik.

**Answer key with verified output:**
```sql
-- NOT IN version
SELECT customer_name FROM customers
WHERE customer_id NOT IN (SELECT customer_id FROM orders);
```
```
customer_name
-------------
Karthik
```

```sql
-- LEFT JOIN version
SELECT customers.customer_name FROM customers
LEFT JOIN orders ON customers.customer_id = orders.customer_id
WHERE orders.order_id IS NULL;
```
```
customer_name
-------------
Karthik
```

Both return Karthik here since there's no NULL customer_id in the real `orders` table - the point is the *habit*, not a different answer today.

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

**Verified output:**
```
city       total_revenue
---------  -------------
Bengaluru  240
Hyderabad  150
```

> *"The inner subquery does the join-and-group-by ONCE, cleanly. By the time the outer query's WHERE runs, the numbers are already correct - there's no later join left that could still duplicate anything."*

### 🔴 The trap / highest-value moment

> *"One easy-to-miss requirement: try removing the alias - the 'AS city_totals' part - and run it."*
> Remove `AS city_totals` and run it live - let the error appear.

**Verified error:**
```
Error: in prepare, no such column: city_totals.city
  SELECT city_totals.city, city_totals.total_revenue FROM (SELECT customers.city
         ^--- error here
```

> *"SQL requires a name for anything that acts like a table, even a temporary one built on the fly inside FROM. No alias, no valid query. Always name your subquery in FROM."*

---

## Practical Block 4: Full Subquery-in-FROM Challenge (10 min)

**Activity:** Pairs write a subquery-in-FROM query calculating total revenue per loyalty tier, then filtering the outer query to tiers above ₹200.

**Answer key with verified output:**
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
```
loyalty_tier  total_revenue
------------  -------------
Gold          210
Silver        270
```

**Result: BOTH Gold (210) and Silver (270) clear the ₹200 threshold** - walk through the real output live and make this explicit, rather than assuming only one tier would qualify. Say aloud: *"Both tiers pass here - Gold's 210 clears 200 by a comfortable margin, same as Silver's 270. If your exercise was specifically designed to show only ONE tier surviving a filter, this particular threshold doesn't demonstrate that - which is itself worth discussing: always actually run a filter and read its real output, rather than assuming what it 'should' show before checking."*

> 💬 **Expect a pair to try filtering with HAVING instead inside the subquery, then WHERE again outside.** Welcome it - ask: *"Could you have just used HAVING inside the subquery and skipped the outer WHERE entirely? What's the difference in the end result?"*

**Verify this live - it genuinely does produce the identical result:**
```sql
SELECT customers.loyalty_tier, SUM(orders.price) AS total_revenue
FROM customers
INNER JOIN orders ON customers.customer_id = orders.customer_id
GROUP BY customers.loyalty_tier
HAVING SUM(orders.price) > 200;
```
```
loyalty_tier  total_revenue
------------  -------------
Gold          210
Silver        270
```

> *"Identical result, and simpler - no subquery needed at all for this specific case, since HAVING can filter the aggregate directly. So when would you actually need the FROM-subquery version instead? When you need to filter or join on the aggregated result using something HAVING can't reach cleanly - like joining tier_totals to a THIRD table, or filtering with a condition that itself needs another subquery. A good moment to discuss that SQL frequently offers more than one valid path to the same answer, and picking the simplest one that works is a real skill."*

---

## Extension Blocks (Optional — Use if Running Ahead)

*Not part of the 90-minute core flow. Use only if Practical Block 4 finishes early - see Timing Contingencies. This block previews correlated subqueries, which are meaningfully more advanced than anything else in today's core session - flag that explicitly if you run it.*

### Concept Block 5 (Extension): A Subquery in SELECT - a Per-Row Calculated Column

#### 💬 Instructor script

> *"Everything today has used a subquery in WHERE or FROM. One more place a subquery can live: right inside SELECT, calculating a value for every single row."*

```sql
SELECT order_id, price,
       (SELECT AVG(price) FROM orders) AS overall_avg,
       price - (SELECT AVG(price) FROM orders) AS diff_from_avg
FROM orders;
```

**Verified output:**
```
order_id  price  overall_avg  diff_from_avg
--------  -----  -----------  --------------
1         120    120.0        0.0
2         150    120.0        30.0
3         120    120.0        0.0
4         90     120.0        -30.0
```

> *"Every single row now carries its own comparison to the overall average, right alongside its own price. Notice `overall_avg` is identical on all 4 rows - that subquery genuinely runs once, calculates 120.0, and the same single number gets attached to every row. This is called a scalar subquery in SELECT, and it's a clean way to show 'how does this row compare to the whole' without a separate query."*

#### 🔴 The trap / highest-value moment

> *"This works cleanly here because the subquery doesn't depend on which row it's currently attached to - it's the SAME subquery, run once, reused four times. There's a more advanced version called a correlated subquery, where the inner query DOES reference the outer row (e.g., 'how does this order compare to the average for just ITS city') - and that version genuinely re-runs once per row, which can get slow on a large table. That's beyond today's scope; know the term exists, and that not all subqueries in SELECT behave identically underneath."*

### Practical Block 5 (Extension): Building a Per-Row Comparison Column

**Activity:** Pairs write a query showing every order's price alongside the overall average and quantity alongside the overall average quantity.

**Verified answer key:**
```sql
SELECT order_id, price, (SELECT AVG(price) FROM orders) AS avg_price,
       quantity, (SELECT AVG(quantity) FROM orders) AS avg_quantity
FROM orders;
```
```
order_id  price  avg_price  quantity  avg_quantity
--------  -----  ---------  --------  ------------
1         120    120.0      2         1.75
2         150    120.0      1         1.75
3         120    120.0      1         1.75
4         90     120.0      3         1.75
```

> 💬 **Expect a pair to ask why this doesn't need an alias like the FROM-subquery did.** Welcome it - say: *"A subquery in SELECT is producing a single VALUE for a column, not standing in for a whole table the way a FROM subquery does - so there's no table-like structure that needs a name. Give the resulting COLUMN an alias (like `avg_price`) for readability, but the subquery itself doesn't require one the way a FROM subquery's alias is actually required."*

---

## Common Errors

| Error | What causes it | Fix |
|---|---|---|
| `near "SELECT": syntax error` | Forgetting to wrap a subquery in parentheses | Every subquery, in WHERE, FROM, or SELECT, must be enclosed in parentheses |
| A `=`/`>`/`<` subquery silently using an arbitrary row instead of erroring | Using a single-value comparison operator against a subquery that can return more than one row (SQLite-specific leniency) | Before using `=`, `>`, or `<` with a subquery, confirm it can only ever return exactly one row - use IN or a further aggregate if it could return more |
| `NOT IN` returning zero rows unexpectedly | A NULL present anywhere in the subquery's result list | Check the inner column for NULLs before trusting NOT IN, or default to `LEFT JOIN ... WHERE ... IS NULL` instead |
| `no such column: <alias>.<column>` after a FROM subquery | Forgetting to alias (`AS ...`) a subquery used in FROM | Always give a subquery in FROM a table alias - it's required, not optional |
| Row counts from a "below/at/above average" split not summing to the table total | An arithmetic or condition-writing slip in one of the three queries, or an unaccounted-for NULL | Explicitly sum the three counts and confirm they equal the full row count before trusting any of them |
| Assuming a correlated subquery behaves identically to a non-correlated one | Not yet distinguishing "runs once, reused" from "re-runs per outer row" | Treat correlated subqueries (Extension Block) as a distinct, more advanced case outside this session's core scope |
| Nesting subqueries several levels deep and losing track of what each level does | Reaching for more nesting instead of a cleaner structure | Consider whether a CTE (next session) would make the same logic easier to read, once nesting exceeds one level |
| Using HAVING inside a FROM-subquery's inner query but also repeating the same filter as an outer WHERE | Not recognising the two are often redundant for a simple case | Check whether HAVING alone (no FROM-subquery needed) already answers the question before reaching for the more complex form |

---

## Materials Checklist

Before class, have ready:

- `SQL Files/module2_phase2_sessions_6.1_to_6.2.db` loaded in the shared SQL sandbox - same database and schema as Sessions 13–14 (`customers`, `orders`, `customer_addresses`).
- A projector for live queries - the multi-row scalar subquery non-error in Concept Block 2, and the NOT IN / NULL trap demonstration in Concept Block 3, are this session's two highest-value moments and both need to run live.
- Confirm in advance how you'll demonstrate the NULL trap safely: this script uses a `UNION SELECT NULL` inside the subquery itself, which doesn't require modifying the real `orders` table - test this exact query before class so it's ready to run smoothly.
- A printed or slide reference of the `customers`, `orders`, and `customer_addresses` tables for quick lookup throughout.
- Session 13's LEFT JOIN "never ordered" answer (Karthik) ready to reference for continuity in Concept Block 3.

---

## Timing Contingencies

**If running long:**
- In Practical Block 1, skip the live "do the three counts sum to the total" verification and state the result verbally instead.
- Compress Practical Block 4 to the subquery-in-FROM version only, presenting the HAVING-only alternative as a quick verbal aside rather than a second full live run.
- Never cut the NOT IN / NULL trap in Concept Block 3 - it is described by the script itself as "the single most dangerous trap in this entire session," and it is the one failure mode in the whole session that produces a plausible-looking WRONG answer with zero error at all.

**If running short:**
- Run the Extension Blocks (subqueries in SELECT) in full, clearly flagging the correlated-subquery distinction as beyond today's core scope.
- If only a few minutes remain, demonstrate the single scalar-subquery-in-SELECT query from Concept Block 5 live as a quick capstone, without the paired Practical Block 5.
- Alternatively, revisit Practical Block 4 and ask pairs to rewrite the tier_totals FROM-subquery as a HAVING-only query (already shown as the answer key's bonus comparison) and discuss when each form would actually be necessary - reinforcing "more than one valid path" without new syntax.

---

## End-of-Session Quiz

1. **What are the two required ingredients of any subquery, regardless of where it's used?**
   → It must be a complete SELECT statement, and it must be wrapped in parentheses.

2. **Why is it risky to use `=` or `>` with a subquery that could return more than one row?**
   → Some databases will error outright; SQLite specifically will silently use just one of the returned rows without warning, which can produce a technically-successful but arbitrarily wrong result.

3. **Why does `NOT IN (SELECT customer_id FROM orders)` fail silently if that subquery's result contains a NULL?**
   → NULL represents "unknown" in SQL comparisons - comparing anything to an unknown value via NOT IN makes the entire condition's truth unknown too, causing the whole query to return zero rows instead of the correct answer.

4. **What is the safer alternative to NOT IN for a "never matched" question, and why?**
   → `LEFT JOIN ... WHERE ... IS NULL` - it doesn't have the NULL-in-the-list blind spot that NOT IN does.

5. **Why does a subquery used in FROM require an alias (`AS ...`), while a subquery in WHERE doesn't?**
   → A FROM subquery is standing in for a table, and every table-like structure referenced in a query needs a name; a WHERE subquery is just producing a comparison value, not a queryable structure.

6. **(If Extension Block covered) What's the difference between a plain scalar subquery in SELECT and a correlated subquery?**
   → A plain scalar subquery calculates its value once and reuses it for every row; a correlated subquery references something from the outer row and re-runs once per row.

---

## Q&A & Doubt Solving

**Q: Can a subquery go anywhere else besides WHERE and FROM?**
→ Yes - subqueries can also appear in SELECT (to compute a per-row calculated column, see the Extension Block above) and in HAVING. We've covered the three most common and highest-value uses today; you'll encounter more advanced placements naturally as your queries get more advanced.

**Q: Is a subquery always slower than a JOIN?**
→ Not necessarily - it depends on the database and the specific query. For now, focus on correctness and readability; performance tuning is a more advanced skill for later in your career.

**Q: Can I nest a subquery inside another subquery?**
→ Technically yes, but readability suffers fast, which is exactly why CTEs (next session) exist - they let you name each step instead of nesting parentheses inside parentheses inside parentheses.

**Q: Does the subquery in FROM run once, or once per outer row?**
→ Once - it's calculated as its own complete result first, then the outer query treats that result as a normal (if temporary) table. This is part of why it's safe from the fan-out problem: the aggregation happens exactly once, before anything else touches it.

**Q: If NOT IN is risky, why does it still exist / get used?**
→ It's perfectly safe and often more readable when you're certain the inner column has no NULLs - many real datasets genuinely don't. The trap only bites when that assumption turns out to be wrong, which is exactly why checking first (or defaulting to LEFT JOIN + IS NULL) is the safer habit.

**Q: In Practical Block 4, both Gold and Silver cleared the ₹200 threshold - was the exercise "supposed to" filter one of them out?**
→ Not necessarily - the value of the exercise is in correctly building and running the query, not in a specific dramatic result. Always trust what the real, verified output actually shows over an assumption about what an exercise "should" produce.

**Q: Is there a limit to how many subqueries I can use in a single query?**
→ No hard limit in SQL itself, but readability and (eventually) performance both suffer as nesting grows - which is precisely the motivation for CTEs, arriving next session.

---

## Instructor Notes

- **Database-specific behaviour to know before class:** This module's database is SQLite, which does **not** raise an error for a multi-row scalar subquery the way MySQL/PostgreSQL/SQL Server do - it silently uses one arbitrary row instead. The Concept Block 2 demo is written around this actual SQLite behavior (no error appears; the class needs to be told explicitly that other databases WOULD error here). Don't promise students they'll see an error message during the live demo - they won't, and that's the point.
- **Words not yet earned:** Avoid `WITH`/CTEs (arriving explicitly next session), window functions, and correlated subqueries where the inner query references the outer row for a filtering (not just a SELECT-column) purpose - today's core scope stays with non-correlated subqueries; the Extension Block's SELECT-column example is a controlled, explicitly-flagged preview, not a full treatment.
- **The single biggest risk in this session** is students treating subqueries as "just another way to write a JOIN" without grasping WHY each shape exists - the "more than 1 row" error and the NOT IN/NULL trap are the two moments that make the distinction real. Don't rush either.
- **Board management:** Keep the four subquery shapes - scalar (WHERE with =/>/<), list (WHERE with IN/NOT IN), FROM (aliased temp table), and (if Extension Block run) SELECT - visible all session as a running reference, updated after each Concept Block.
- **Common confusions, numbered:**
  1. Forgetting parentheses around a subquery.
  2. Using =/>/< with a subquery that could return more than one row.
  3. Trusting NOT IN without checking whether the inner column could contain NULLs.
  4. Forgetting to alias a subquery used in FROM.
- **Cross-references:** CTEs next session rewrite every subquery from today in cleaner syntax - explicitly promise this in the bridge so students don't feel today's syntax is "the only way" going forward. The NOT IN/NULL trap reappears conceptually in Module 4 (pandas' handling of missing values) - worth a one-line callback when you reach it there.
- **Local/cultural context:** Keep using Ramesh (fan-out), Karthik (never ordered), and Fatima (above-average order) as the running named examples - students have built familiarity with this exact cast since Session 13, and reusing them keeps cognitive load on the new SQL concept, not on re-learning a new story.
