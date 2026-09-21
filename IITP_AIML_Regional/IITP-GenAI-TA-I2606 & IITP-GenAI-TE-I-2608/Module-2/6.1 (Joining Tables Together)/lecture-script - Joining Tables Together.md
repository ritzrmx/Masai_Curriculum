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

*The core flow fills all 90 minutes. Concept/Practical Block 5, joining three tables at once by chaining a second JOIN onto `customer_addresses`, is in the Extension Blocks section - use only if ahead of pace, and it deliberately previews next session's fan-out trap without fully teaching it yet.*

---

## Opening - "Where Did the Customer's City Go?" (8 min)

Walk in and project last session's `orders` table - but this time with `customer_name` and `city` columns already removed, replaced by just a `customer_id`.

> *"Quick question. Where did customer_name and city go? Last week's orders table had them right there."*

**Project the actual new `orders` table students will use all session** (from `SQL Files/module2_phase2_sessions_6.1_to_6.2.db` - a different database from Sessions 9–12's):

```
order_id  customer_id  item           quantity  price  order_date
--------  -----------  -------------  --------  -----  ----------
1         1            Veg Thali      2         120    2026-08-01
2         2            Non-Veg Thali  1         150    2026-08-01
3         3            Veg Thali      1         120    2026-08-02
4         4            Mini Thali     3          90    2026-08-02
```

Let confusion land for a beat, then reveal the `customers` table alongside it:

```
customer_id  customer_name  city       loyalty_tier
-----------  -------------  ---------  ------------
1            Ramesh         Bengaluru  Gold
2            Fatima         Hyderabad  Silver
3            Arjun          Bengaluru  Silver
4            Priya          Chennai    Gold
5            Karthik        Bengaluru  Bronze
```

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

**Push one level further, verbally, before any SQL:** *"customer_id and order_id both run 1 through 4 in this specific dataset. Is that a coincidence, or does it always have to be true?"* Let the room reason it through - it's a coincidence of this particular 4-row table (each of the first four customers happens to have placed exactly one order, in the same numeric sequence). *"Hold onto that thought too - it'll matter when we write our first JOIN in a few minutes."*

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

**Verified output:**
```
order_id  customer_name  item           price
--------  -------------  -------------  -----
1         Ramesh         Veg Thali      120
2         Fatima         Non-Veg Thali  150
3         Arjun          Veg Thali      120
4         Priya          Mini Thali     90
```

### 🔴 The trap / highest-value moment

> *"Where's Karthik in this result?"*
> Let the room scan - he's nowhere. *"Exactly. INNER JOIN only keeps rows that matched on BOTH sides. Karthik has no order, so he has no match, so INNER JOIN silently drops him. That word 'silently' should worry you a little - if you're trying to find customers who've never ordered, INNER JOIN will actively hide the exact answer you're looking for."*

---

## Practical Block 2: Writing INNER JOIN Queries (10 min)

**Activity:** Pairs write an INNER JOIN query showing `item` and `city` for every order.

**Answer key with verified output:**

```sql
SELECT orders.item, customers.city
FROM orders
INNER JOIN customers ON orders.customer_id = customers.customer_id;
```
```
item           city
-------------  ---------
Veg Thali      Bengaluru
Non-Veg Thali  Hyderabad
Veg Thali      Bengaluru
Mini Thali     Chennai
```

4 rows, one per order, since Karthik contributes no order rows to match against.

> 💬 **Expect a pair to accidentally write `ON orders.order_id = customers.customer_id`** (matching two unrelated ID columns). Welcome it - run it live and let the result appear.

**Verified - and this is a genuinely important correction to make here:**

```sql
SELECT orders.order_id, customers.customer_name
FROM orders
INNER JOIN customers ON orders.order_id = customers.customer_id;
```
```
order_id  customer_name
--------  -------------
1         Ramesh
2         Fatima
3         Arjun
4         Priya
```

> *"Look at that - it ran, and every name actually looks correct! This is exactly the coincidence I flagged back in Practical Block 1: order_id and customer_id both happen to run 1, 2, 3, 4 in perfect lockstep in this small dataset, purely because each of these four customers placed exactly one order, in matching order. This query is WRONG - it's matching an order's ID number to a customer's ID number, two things that were never meant to be compared - and today's tiny dataset is hiding that mistake completely."*

**Prove the mistake with a condition that breaks the coincidence:**

```sql
SELECT orders.order_id, orders.quantity, customers.customer_id, customers.customer_name
FROM orders
INNER JOIN customers ON orders.quantity = customers.customer_id;
```
```
order_id  quantity  customer_id  customer_name
--------  --------  -----------  --------------
1         2         2            Fatima
2         1         1            Ramesh
3         1         1            Ramesh
4         3         3            Arjun
```

> *"Now the nonsense is obvious - order 1 is Ramesh's real order, but this query pairs it with Fatima because Ramesh happened to order 2 items and Fatima's ID is 2. That's what a meaningless join condition actually looks like once the coincidence isn't there to hide it. A JOIN can run cleanly and still be completely wrong. Always sanity-check what your ON condition is actually claiming - ask yourself in plain English what the two columns you're comparing are each SUPPOSED to represent."*

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

**Verified output:**
```
customer_name  item           price
-------------  -------------  -----
Ramesh         Veg Thali      120
Fatima         Non-Veg Thali  150
Arjun          Veg Thali      120
Priya          Mini Thali     90
Karthik
```

> *"5 rows now, not 4 - every customer is present, and Karthik's item and price are genuinely blank (NULL), not zero, not a made-up placeholder. NULL means 'no matching row existed,' which is a completely different thing from '0' or an empty string."*

### 🔴 The trap / highest-value moment

> *"Notice which table came FIRST in the FROM clause this time - customers, not orders. LEFT JOIN keeps every row from whichever table is on the LEFT - the one named right after FROM. Swap the table order, and you'd get a completely different result. Write this down: 'left' means the table named in FROM, not just a general direction."*

**Prove it by swapping the order live:**
```sql
SELECT customers.customer_name, orders.item, orders.price
FROM orders
LEFT JOIN customers ON orders.customer_id = customers.customer_id;
```
This time `orders` is on the left - and since every order already has a matching customer, the result is the same 4 rows as the INNER JOIN, with Karthik nowhere to be found. *"Same two tables, same ON condition, same keyword LEFT JOIN - completely different result, purely because of which table was named first."*

---

## Practical Block 3: Finding the Missing Customer (10 min)

**Activity:** Pairs write a `LEFT JOIN` query starting from `customers`, then identify - by reading the output - exactly which customer has NULL order data.

**Answer key with reasoning:** Karthik, customer_id 5 - confirmed as the only row with blank `item`/`price`.

**Bonus discussion, worth demonstrating live:** to isolate ONLY the customers with no orders (not the whole joined table), add `WHERE orders.order_id IS NULL`:

```sql
SELECT customers.customer_name
FROM customers
LEFT JOIN orders ON customers.customer_id = orders.customer_id
WHERE orders.order_id IS NULL;
```
```
customer_name
-------------
Karthik
```

> *"This is a genuine 'find the gap' business technique you'll use constantly - customers who signed up but never bought, products that exist in a catalog but never sold, employees on a roster with no logged hours. LEFT JOIN plus `IS NULL` on the second table's key column is the standard pattern for all of them."*

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

**Verified output:**
```
loyalty_tier  total_revenue
------------  -------------
Silver        270
Gold          210
```

> *"Silver-tier customers are currently generating more revenue than Gold - our supposedly 'premium' tier. Hold onto that number; it's exactly what next session's whole discussion is built around."*

### 🔴 The trap / highest-value moment

> *"Notice every column reference here has a table name in front of it - customers.loyalty_tier, orders.price. Once two tables are joined, if both happen to share a column name, or if it's ambiguous which table a column belongs to, SQL will refuse to guess and throw an error. Get in the habit of prefixing column names with their table now, even when it feels unnecessary - it will save you a confusing error later."*

**Prove the ambiguity error live - both tables have a `customer_id` column:**

```sql
SELECT customer_id, customer_name FROM customers INNER JOIN orders ON customers.customer_id = orders.customer_id;
```
This genuinely errors with `ambiguous column name: customer_id`, since SQLite can't tell whether you mean `customers.customer_id` or `orders.customer_id` - even though, once joined, they always hold the same value for a matched row. *"The values would be identical either way here - and SQLite still refuses to guess. That's a good, strict default to have."*

---

## Practical Block 4: Full Joined-KPI Challenge (11 min)

**Activity:** Light competitive framing. Give the class 2–3 combined business questions (e.g., "total revenue by city, using the joined tables," "which customers have never placed an order") and have pairs race to build the full query.

**Full answer key, verified against the real database:**

**1. "Total revenue by city, using the joined tables."**
```sql
SELECT customers.city, SUM(orders.price) AS total_revenue
FROM customers
INNER JOIN orders ON customers.customer_id = orders.customer_id
GROUP BY customers.city
ORDER BY total_revenue DESC;
```
```
city       total_revenue
---------  -------------
Bengaluru  240
Hyderabad  150
Chennai    90
```

**2. "Which customers have never placed an order?"**
```sql
SELECT customers.customer_name
FROM customers
LEFT JOIN orders ON customers.customer_id = orders.customer_id
WHERE orders.order_id IS NULL;
```
```
customer_name
-------------
Karthik
```

For the "never ordered" question specifically, insist pairs justify their choice of `LEFT JOIN` over `INNER JOIN` out loud before writing SQL - this is the actual transferable judgment call, not just syntax.

> 💬 **Expect a pair to default to INNER JOIN out of habit** for the "never ordered" question, since it was taught first. Welcome it - run their query live:

```sql
SELECT customers.customer_name
FROM customers
INNER JOIN orders ON customers.customer_id = orders.customer_id
WHERE orders.order_id IS NULL;
```
Verified: this returns **zero rows** - not an error, just an empty, wrong-looking-right result, since INNER JOIN already dropped Karthik before the `IS NULL` condition ever had a row to check. Ask: *"Does this actually answer the question that was asked? What happened to Karthik before WHERE even ran?"*

---

## Extension Blocks (Optional — Use if Running Ahead)

*Not part of the 90-minute core flow. Use only if Practical Block 4 finishes early - see Timing Contingencies. This block deliberately previews next session's fan-out trap without fully resolving it - flag that explicitly to students if you run it.*

### Concept Block 5 (Extension): Joining a Third Table

#### 💬 Instructor script

> *"Nothing stops you from chaining a second JOIN to bring in a third table. Here's `customer_addresses` - each customer's saved delivery addresses - joined onto what we already have."*

```sql
SELECT customers.customer_name, orders.item, customer_addresses.address_label
FROM customers
INNER JOIN orders ON customers.customer_id = orders.customer_id
INNER JOIN customer_addresses ON customers.customer_id = customer_addresses.customer_id;
```

**Verified output:**
```
customer_name  item           address_label
-------------  -------------  -------------
Ramesh         Veg Thali      Home
Ramesh         Veg Thali      Office
Fatima         Non-Veg Thali  Home
Arjun          Veg Thali      Home
Priya          Mini Thali     Home
```

> *"Look closely - Ramesh's single Veg Thali order now shows up TWICE, once for each of his two saved addresses. His order didn't duplicate in the real `orders` table - it's just appearing twice in THIS joined result, because he matched two rows in customer_addresses instead of one."*

#### 🔴 The trap / highest-value moment

> *"If you were tempted to SUM the price column on this exact result right now, stop. Ramesh's ₹120 order would get counted twice - once per address - inflating his total to ₹240 when he actually spent ₹120. I'm deliberately not solving this today - it's called a JOIN fan-out, and it's the entire subject of next session. For now, just notice it happened, and remember: a join to a table where one side can have MULTIPLE matches will duplicate rows on the other side, every time, with zero error or warning."*

### Practical Block 5 (Extension): Spotting the Duplication

**Activity:** Pairs run the query above and count: how many rows does Ramesh appear in, versus how many real orders does he actually have?

**Verified answer key:** Ramesh appears in 2 rows of the joined result, but has exactly 1 real order in the `orders` table (`SELECT * FROM orders WHERE customer_id = 1;` confirms a single row, ₹120). Every other customer here (Fatima, Arjun, Priya) has exactly 1 saved address, so they each appear exactly once - only Ramesh duplicates.

> 💬 **Expect a pair to ask "so is this JOIN wrong?"** Welcome it - say: *"No, it's not wrong. It's answering exactly what it was asked: 'show me every order alongside every one of that customer's saved addresses' - and Ramesh genuinely does have two addresses, so two rows is the correct answer to THAT question. The mistake only happens if you then aggregate (SUM, COUNT) on top of this result without accounting for the duplication. We'll build the full fix for that next session."*

---

## Common Errors

| Error | What causes it | Fix |
|---|---|---|
| Believing `customers` and `orders` are "the same data, reorganized" | Not internalizing that normalization genuinely splits data across separate, related tables | Point back to the Opening's "Ramesh moves cities" example - one update, in one table, fixes it everywhere |
| Joining on two unrelated ID columns (e.g. `order_id = customer_id`) | Assuming any two similarly-named ID columns are safe to compare | Ask in plain English what each column is SUPPOSED to represent before writing the ON condition - don't rely on the query running without error |
| `ambiguous column name` error after a JOIN | Referencing a column name (like `customer_id`) that exists identically in both joined tables, without a table prefix | Always prefix column names with their table once two or more tables are joined |
| Defaulting to INNER JOIN for a "who's missing" question | INNER JOIN was taught first and feels like the "default" JOIN | Ask explicitly: does this question need only matches, or does it need unmatched rows preserved too? |
| `LEFT JOIN ... INNER JOIN ... WHERE ... IS NULL` returning zero rows unexpectedly | Using INNER JOIN somewhere in the chain, which drops the very unmatched rows the `IS NULL` check was trying to find | Make sure every JOIN between the anchor table and the "IS NULL" check is a LEFT JOIN, not an INNER JOIN |
| Treating NULL in a LEFT JOIN result as "zero" or "blank text" | Not distinguishing "no matching row" from an actual stored value of 0 or "" | Remember NULL specifically means no match was found - never treat it as equivalent to zero in later calculations without deliberately deciding to |
| Swapping table order in LEFT JOIN and expecting the same result | Assuming LEFT JOIN's behavior is symmetric like INNER JOIN's | Remember: "left" means the table named first, right after FROM - swapping it changes which unmatched rows get preserved |
| SUMing or COUNTing directly on a multi-table joined result without checking for duplication | Not yet knowing about join fan-out (formally covered next session) | If a query joins to a table where the "one" side could have multiple matches, verify row counts before trusting any aggregate on top |

---

## Materials Checklist

Before class, have ready:

- `SQL Files/module2_phase2_sessions_6.1_to_6.2.db` loaded in the shared SQL sandbox - a **different database** from Sessions 9–12. Do not reuse the Phase 1 database today; this one has the normalized `customers`/`orders`/`customer_addresses` schema the whole session depends on.
- A projector for live queries - the ambiguous-column-name error in Concept Block 4, the table-order-swap demonstration in Concept Block 3, and the coincidental-ID-match correction in Practical Block 2 all need to be run live, not just described.
- Printed or slide copies of both the `customers` table (5 rows) and the new `orders` table (4 rows, FK schema) side by side, with `customer_id` visually highlighted in both, for Concept Block 1.
- If running the Extension Block: the `customer_addresses` table (5 rows, Ramesh has 2) from the same database.

---

## Timing Contingencies

**If running long:**
- Skip the "swap the table order" live demonstration in Concept Block 3 and instead state the result verbally, pointing back to the LEFT JOIN definition.
- Compress Practical Block 4 to just the "never ordered" question, since it's the more consequential judgment call (LEFT JOIN vs. INNER JOIN) and folds in a review of Practical Block 3.
- Never cut the coincidental order_id/customer_id correction in Practical Block 2 - it is this session's single clearest demonstration that a join can run cleanly and still be meaningless, a theme this module returns to constantly.

**If running short:**
- Run the Extension Blocks (joining a third table, spotting the Ramesh duplication) in full - they set up next session extremely well.
- If only a few minutes remain, run just the three-table JOIN query from Concept Block 5 live as a teaser, explicitly naming it as "next session's whole topic," without the paired Practical Block 5.
- Alternatively, revisit Practical Block 4's "never ordered" question and ask pairs to also write it as an INNER JOIN with a HAVING-based count check (a customer whose joined order count is 0) - though note this specific alternative doesn't actually work cleanly with INNER JOIN, which is itself an instructive dead end worth letting a pair discover.

---

## End-of-Session Quiz

1. **What column links the `customers` and `orders` tables, and why is an ID used instead of the customer's name?**
   → `customer_id` - IDs avoid ambiguity from typos, duplicate names, or spelling variations that a name-based match could produce.

2. **Does INNER JOIN include Karthik (customer_id 5) in its results? Why or why not?**
   → No - Karthik has zero matching rows in `orders`, and INNER JOIN only keeps rows matched on both sides.

3. **What appears in the `item` and `price` columns for Karthik under a LEFT JOIN starting from `customers`?**
   → NULL (blank) - not zero, not an empty string - because no matching order row exists for him.

4. **Why does swapping the table order in a LEFT JOIN change the result?**
   → "Left" refers specifically to whichever table is named first, right after FROM - LEFT JOIN preserves every row from THAT table, so swapping which table comes first changes which unmatched rows are preserved.

5. **Why does `ambiguous column name: customer_id` occur after joining `customers` and `orders`?**
   → Both tables have a column named `customer_id`, and without a table prefix, SQL can't determine which one you mean - even though their values match for a joined row.

6. **(If Extension Block covered) Why does Ramesh appear twice in a three-way join to `customer_addresses`, while Fatima, Arjun, and Priya each appear once?**
   → Ramesh has two saved addresses (Home and Office) in `customer_addresses`, so his one order matches two address rows; everyone else has exactly one saved address.

---

## Q&A & Doubt Solving

**Q: Can I join more than two tables in one query?**
→ Yes - you can chain multiple JOIN clauses, each with its own ON condition, to bring in a third, fourth, or more related tables. See the Extension Block above for a worked three-table example.

**Q: What's the difference between JOIN and INNER JOIN?**
→ None - `JOIN` alone defaults to `INNER JOIN` in virtually every SQL database. Writing `INNER JOIN` explicitly is just clearer to read, especially while learning.

**Q: Is there a RIGHT JOIN too?**
→ Yes - it's the mirror image of LEFT JOIN, keeping every row from the second (right) table instead. In practice, most analysts just rewrite the table order and use LEFT JOIN instead of reaching for RIGHT JOIN, since it reads more naturally left to right.

**Q: What if two rows in orders both point to the same customer_id - does JOIN handle that fine?**
→ Yes - that's exactly the normal case (a customer with multiple orders). Each matching order row gets its own row in the joined result, each carrying the same customer details alongside it.

**Q: Can I use an aggregate function and a JOIN in the same query as GROUP BY?**
→ Yes - that's exactly what today's Concept Block 4 example does. JOIN happens first to combine the tables, then GROUP BY and the aggregate function work on the combined result exactly as they did on a single table.

**Q: If I write `ON orders.customer_id = customers.customer_id`, does the ORDER of the two sides of the equals sign matter?**
→ No - `a = b` and `b = a` mean the same thing in an ON condition. What matters is which columns you're comparing, not which side of the `=` they're written on.

**Q: Why didn't `orders.order_id = customers.customer_id` produce an error, if it's a meaningless comparison?**
→ Both columns are integers, so SQL has no way to know the comparison is conceptually meaningless - it will happily compare any two columns of compatible types. This is exactly why "does it run" and "is it correct" are two different questions - SQL checks the first, you have to check the second.

---

## Instructor Notes

- **Words not yet earned:** Avoid subqueries, CTEs, and full multi-table fan-out analysis - subqueries and CTEs arrive in the next-but-two and next-but-three sessions. If a student asks about joining three or more tables, the Extension Block gives you a real, controlled way to show it without teaching the full fan-out fix yet.
- **The single biggest risk in this session** is students treating INNER JOIN as the "default correct choice" simply because it's taught first, and reaching for it automatically even when a question specifically needs LEFT JOIN. Defeat it by returning to Karthik by name at every opportunity - he's the concrete anchor for "when does INNER JOIN silently hide the answer?"
- **Board management:** Keep both tables - `customers` and `orders` - visible side by side on the board all session, with the shared `customer_id` column visually highlighted or circled in both.
- **Common confusions, numbered:**
  1. Believing the two tables are "the same data, just reorganized" rather than genuinely separate, related tables.
  2. Joining on the wrong pair of columns (e.g., two unrelated ID columns) and getting a technically-valid but meaningless result - especially dangerous here because this dataset's small size makes some wrong joins coincidentally look right.
  3. Defaulting to INNER JOIN when the business question specifically requires preserving unmatched rows.
  4. Forgetting to prefix column names with their table name once two tables are joined, especially when column names could be ambiguous.
- **Cross-references:** Subqueries (next-but-one session) and CTEs (the session after that) both build directly on today's JOIN skill, often used to prepare data before joining it. Tableau's "relationships" and "blending" features and pandas' `.merge()` in Module 4 are this exact same idea under different names.
- **Local/cultural context:** Keep Karthik's storyline (signed up, never ordered) alive as a running example - it resurfaces naturally in Session 14 (Insights from Combined Data) as a genuine "customers at risk of churn" business insight.
