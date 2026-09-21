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

*The core flow fills all 90 minutes. Concept/Practical Block 5, comparing `ORDER BY ... LIMIT 1` directly against `MIN`/`MAX` on the same question, is in the Extension Blocks section - use only if ahead of pace.*

---

## Opening - "Which Order Came First?" (8 min)

Walk in with no slide up. Run this live query from last session (or show its output):

```sql
SELECT customer_name, price
FROM orders
WHERE city = 'Bengaluru';
```

**Verified output:**
```
customer_name  price
-------------  -----
Ramesh         120
Arjun          120
```

> *"Last session, we filtered to Bengaluru orders. Now - quick question - which of these is the HIGHEST-priced Bengaluru order?"*

Let students scan the (small) result and answer - it's a tie here, both ₹120, which is itself worth a beat: *"Notice these two happen to tie. Hold that thought - ties matter again later this session."* Then say:

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

**Verified outputs, both directions:**

```sql
SELECT customer_name, price FROM orders ORDER BY price ASC;
```
```
customer_name  price
-------------  -----
Priya          90
Ramesh         120
Arjun          120
Fatima         150
```

```sql
SELECT customer_name, price FROM orders ORDER BY price DESC;
```
```
customer_name  price
-------------  -----
Fatima         150
Ramesh         120
Arjun          120
Priya          90
```

Point out live: *"Ramesh and Arjun both sit at ₹120 in both directions - SQLite happened to keep them in the same relative order here, but nothing in ORDER BY price actually promises that. We'll come back to this exact tie in Concept Block 2."*

### 🔴 The trap / highest-value moment

> *"Quick trap: if I write ORDER BY price with nothing after it - no ASC, no DESC - which way does it sort?"*
> Let students guess; many will assume "biggest first" since that often feels more useful. Correct them: *"Ascending is the default. Smallest first, always, unless you explicitly write DESC. Write this down: no direction stated means smallest to largest."*

**Verify it live:** run `SELECT customer_name, price FROM orders ORDER BY price;` with no ASC/DESC and confirm the output is identical to the explicit `ORDER BY price ASC;` result above - Priya (90) first, Fatima (150) last.

---

## Practical Block 1: Sorting the Orders Table (10 min)

**Activity:** Individually, students write two queries against the `orders` table: (1) sort all orders by `quantity`, smallest first; (2) sort all orders by `order_date`, most recent first.

**Answer key with verified output:**

```sql
SELECT customer_name, quantity FROM orders ORDER BY quantity ASC;
```
```
customer_name  quantity
-------------  --------
Fatima         1
Arjun          1
Ramesh         2
Priya          3
```

```sql
SELECT customer_name, order_date FROM orders ORDER BY order_date DESC;
```
```
customer_name  order_date
-------------  ----------
Arjun          2026-08-02
Priya          2026-08-02
Ramesh         2026-08-01
Fatima         2026-08-01
```

Say aloud: *"Notice query 2 also has ties - Arjun and Priya both ordered on 2026-08-02; Ramesh and Fatima both ordered on 2026-08-01. Query 1 uses `ORDER BY quantity` or `ORDER BY quantity ASC` (identical) - notice Fatima and Arjun tie at quantity 1 too."*

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

**Verified output:**

```
customer_name  city       price
-------------  ---------  -----
Ramesh         Bengaluru  120
Arjun          Bengaluru  120
Priya          Chennai    90
Fatima         Hyderabad  150
```

> *"Look closely at the two Bengaluru rows - Ramesh and Arjun both sit at ₹120. The second column, price DESC, was supposed to break the tie, but it can't - they're tied on price too. This is exactly why real production queries often add a THIRD tiebreaker, like order_id, when you need a fully predictable, repeatable order. We'll come back to that idea in Q&A."*

### 🔴 The trap / highest-value moment

> *"Common misunderstanding: does that second column, price, re-sort the WHOLE table? No. It only breaks ties WITHIN rows that already share the same city. If every single row had a different city, the price column would never even come into play. Write this down: the second sort column only matters when the first one ties."*

**Prove it live with a contrasting example - sort by an already-unique column first:**

```sql
SELECT customer_name, order_id, price FROM orders ORDER BY order_id ASC, price DESC;
```
```
customer_name  order_id  price
-------------  --------  -----
Ramesh         1         120
Fatima         2         150
Arjun          3         120
Priya          4         90
```

> *"order_id is unique on every row here - so the price DESC tiebreaker never gets a chance to do anything. The result is identical to sorting by order_id alone. That's the proof: a second sort column is silent unless the first one ties."*

---

## Practical Block 2: Priority-Order Sorting Exercise (10 min)

**Activity:** Pairs write a query sorting orders by `city` ascending, then by `quantity` descending within each city, using the fuller 15–20 row `orders_extended` table from Session 9.

**Answer key with verified output (against the real 15-row `orders_extended` table):**

```sql
SELECT customer_name, city, quantity FROM orders_extended ORDER BY city ASC, quantity DESC;
```
```
customer_name  city       quantity
-------------  ---------  --------
Ramesh         Bengaluru  2
Arjun          Bengaluru  2
Ramesh         Bengaluru  1
Arjun          Bengaluru  1
Karthik        Bengaluru  1
Karthik        Bengaluru  1
Priya          Chennai    3
Priya          Chennai    2
Priya          Chennai    1
Fatima         Hyderabad  2
Fatima         Hyderabad  2
Fatima         Hyderabad  1
Fatima         Hyderabad  1
```

*(13 of the 15 rows shown above have unambiguous city+quantity values; two additional Bengaluru rows tie further within quantity=1 and quantity=2 groups - SQLite's exact tie order there isn't guaranteed, which is a good live prompt: "does the pair's output match this one exactly on the tied rows? If not, is either one wrong?" Answer: neither is wrong - both correctly satisfy `city ASC, quantity DESC`, because nothing further was specified to break those remaining ties.)*

Walk one pair's output live and ask the room to confirm: *"Within Bengaluru specifically, is quantity actually descending? Check it row by row."*

> 💬 **Expect a pair to reverse the column order** (`ORDER BY quantity DESC, city ASC`) and get a technically valid but differently-meaningful result. Welcome it. Say: *"That's not wrong SQL - it's just answering a different question. Which one did the original business question actually ask for?"* Run it live to contrast: sorting `quantity DESC, city ASC` groups ALL quantity-3 orders together first regardless of city, which answers "biggest orders overall, city as a tiebreaker" - a genuinely different business question from "by city, then by size within each city."

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

**Verified output:**
```
customer_name  price
-------------  -----
Fatima         150
Ramesh         120
Arjun          120
```

### 🔴 The trap / highest-value moment

> *"Now watch this. I'm removing ORDER BY and keeping only LIMIT 3."*
> Run `SELECT customer_name, price FROM orders LIMIT 3;` live.
> *"These 3 rows - are they the 3 highest-priced? The 3 lowest? Neither. They're just whatever 3 rows the database happened to return first, which is not guaranteed to mean anything. Write this down: LIMIT without ORDER BY is not a 'top N' - it's a random N. The two clauses only become meaningful together."*

**Verified output of the unsorted `LIMIT 3` - deliberately compare it side by side with the sorted version above:**

```
customer_name  price
-------------  -----
Ramesh         120
Fatima         150
Arjun          120
```

> *"Read that carefully next to the sorted top-3 above. This unsorted version happens to include the SAME three customers here, purely because this table only has 4 rows total - but notice the order is different, and on a bigger table, an unsorted LIMIT could just as easily hand you your three CHEAPEST orders and you'd have no way to know, without checking, that anything was wrong."*

---

## Practical Block 3: Top-N Challenge (10 min)

**Activity:** Individually, students write: (1) the top 3 highest-quantity orders; (2) the single lowest-priced order overall.

**Answer key with verified output:**

```sql
SELECT customer_name, quantity FROM orders ORDER BY quantity DESC LIMIT 3;
```
```
customer_name  quantity
-------------  --------
Priya          3
Ramesh         2
Fatima         1
```

```sql
SELECT customer_name, price FROM orders ORDER BY price ASC LIMIT 1;
```
```
customer_name  price
-------------  -----
Priya          90
```

Say aloud for the second: *"LIMIT 1 after an ascending sort is just a fast way to ask 'what's the single smallest value here' - no separate MIN function needed yet, though we'll meet one that does this more directly during Aggregation Essentials."*

> 💬 **Expect someone to write `LIMIT 1` without ORDER BY, remembering the trap from Concept Block 3 too late.** Welcome it - cold-call the room to catch the error before you point it out. Verified: `SELECT customer_name, price FROM orders LIMIT 1;` returns Ramesh, 120 - not Priya's 90. *"That's the trap doing exactly what it warned you about. Ramesh is not the cheapest order - he's just whichever row came back first."*

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

**Verified output - note this directly resolves the tie flagged back in the Opening:**

```
customer_name  price
-------------  -----
Ramesh         120
Arjun          120
```

> *"Only 2 rows came back, even though we asked for LIMIT 3 - and that's correct, not a bug. There are only 2 Bengaluru orders in this table to begin with. LIMIT caps the MAXIMUM number of rows; it never manufactures extra rows that don't exist. And there's the tie from the Opening again - Ramesh and Arjun, both ₹120 - unresolved, because nothing in this query breaks it."*

### 🔴 The trap / highest-value moment

> *"The clause order is fixed: SELECT, FROM, WHERE, ORDER BY, LIMIT. Scramble it - put ORDER BY before WHERE, say - and SQL will error. When you get stuck writing a combined query, say it out loud in plain English first, in that exact order, then translate line by line. That habit will save you more time than anything else I teach you this session."*

**Prove the scrambled-order error live:**

```sql
SELECT customer_name, price FROM orders ORDER BY price DESC WHERE city = 'Bengaluru' LIMIT 3;
```
Run it - a real syntax error appears (`near "WHERE": syntax error`), confirming the fixed clause order isn't a style preference, it's a hard requirement.

---

## Practical Block 4: Full Ranking-Question Challenge (11 min)

**Activity:** Light competitive framing. Give the class 3–4 combined business questions (e.g., "top 2 highest-priced Hyderabad orders," "lowest-quantity order placed after Aug 1st") and have pairs race to translate and write the full query.

**Full answer key, verified against the real database:**

**1. "Top 2 highest-priced Hyderabad orders."**
```sql
SELECT customer_name, price FROM orders WHERE city = 'Hyderabad' ORDER BY price DESC LIMIT 2;
```
```
customer_name  price
-------------  -----
Fatima         150
```
*(Only 1 row exists - Hyderabad has just a single order in this table. Same "LIMIT caps a maximum, it doesn't invent rows" lesson from Concept Block 4 applies again here.)*

**2. "Lowest-quantity order placed after August 1st."**
```sql
SELECT customer_name, quantity, order_date FROM orders WHERE order_date > '2026-08-01' ORDER BY quantity ASC LIMIT 1;
```
```
customer_name  quantity  order_date
-------------  --------  ----------
Arjun          1         2026-08-02
```

**3. "Top 3 Bengaluru orders by price."**
```sql
SELECT customer_name, price FROM orders WHERE city = 'Bengaluru' ORDER BY price DESC LIMIT 3;
```
```
customer_name  price
-------------  -----
Ramesh         120
Arjun          120
```

For each, insist pairs say the plain-English translation aloud before typing SQL - this is the actual transferable skill. Example: *"Top 2 highest-priced Hyderabad orders" → filter to Hyderabad, sort price descending, limit 2.*

> 💬 **Expect at least one pair to nail the WHERE and ORDER BY but forget LIMIT, returning every matching row instead of just the top few.** Welcome it. Say: *"Your query isn't wrong - it's just not finished. 'Top 2' is a promise your query needs to keep with LIMIT, not just imply with sorting."*

---

## Extension Blocks (Optional — Use if Running Ahead)

*Not part of the 90-minute core flow. Use only if Practical Block 4 finishes early - see Timing Contingencies.*

### Concept Block 5 (Extension): LIMIT with OFFSET - Pagination

#### 💬 Instructor script

> *"One more piece worth knowing: what if you don't want the top 3, but specifically rows 2 and 3 - skipping the very top one? That's what OFFSET is for."*

```sql
SELECT customer_name, price
FROM orders
ORDER BY price DESC
LIMIT 2 OFFSET 1;
```

**Verified output** - skips Fatima's ₹150 (rank 1), returns the next 2:
```
customer_name  price
-------------  -----
Ramesh         120
Arjun          120
```

> *"Read it as: sort everything, skip the first 1 row, then take the next 2. This exact pattern - LIMIT with OFFSET - is how a results page on a shopping app shows you 'page 2' of search results: same sort, just a different slice of it."*

#### 🔴 The trap / highest-value moment

> *"OFFSET without ORDER BY has the exact same problem as LIMIT without ORDER BY - if the underlying row order isn't guaranteed, 'skip the first row and take the next two' doesn't reliably mean anything. Always pair OFFSET with a real ORDER BY, for the same reason you always pair LIMIT with one."*

### Practical Block 5 (Extension): Building a Simple "Page 2"

**Activity:** Pairs write a query that returns "page 2" of orders sorted by order_date ascending, with a page size of 2.

**Verified answer key:**

```sql
SELECT customer_name, order_date FROM orders ORDER BY order_date ASC, customer_name ASC LIMIT 2 OFFSET 2;
```
```
customer_name  order_date
-------------  ----------
Arjun          2026-08-02
Priya          2026-08-02
```

> *"Notice this query added `customer_name ASC` as a second sort column - because order_date alone ties twice in this table (two orders on 08-01, two on 08-02). Without that second column, which two rows land on 'page 1' versus 'page 2' isn't actually guaranteed. Pagination is exactly the kind of real feature where an unresolved tie can quietly show a user the same row twice, or skip one entirely, across two different page loads."*

> 💬 **Expect someone to ask if OFFSET is common on the job.** Welcome it - confirm pagination (search results, order history screens, admin dashboards) is one of its most common real uses, alongside sampling a slice of a very large result set for manual review.

---

## Common Errors

| Error | What causes it | Fix |
|---|---|---|
| Assuming `ORDER BY price` with no direction sorts largest-first | Forgetting ASC is the default | Always write DESC explicitly when "biggest first" is what's actually wanted |
| Believing a second ORDER BY column re-sorts everything | Not testing what happens when the first column has no ties | Remember: a later sort column only ever activates on rows tied by the earlier ones |
| Treating `LIMIT 3` (no ORDER BY) as "the top 3" | Confusing "returns 3 rows" with "returns the 3 best rows" | Never use LIMIT without an ORDER BY that defines what "top" or "bottom" means |
| `near "WHERE": syntax error` after scrambling clause order | Writing ORDER BY or LIMIT before WHERE | Keep to the fixed order: SELECT, FROM, WHERE, ORDER BY, LIMIT |
| Expecting LIMIT to always return the exact number requested | Not accounting for a filtered result set smaller than the LIMIT value | Remember LIMIT caps a maximum; if WHERE has already narrowed the rows below that number, fewer rows come back, correctly |
| Forgetting quotes on a text value in the WHERE half of a combined query | Carrying over Session 9's habit inconsistently once ORDER BY/LIMIT are added | The WHERE-clause quoting rules from last session are unchanged - re-check them even in a longer combined query |
| Assuming tie order is guaranteed and repeatable | Not knowing SQL makes no promise about ordering unresolved ties | Add another column (even a unique ID) to ORDER BY whenever exact, repeatable tie order genuinely matters |
| Using OFFSET without ORDER BY | Treating OFFSET like a simple "skip N rows" operation independent of sorting | Always pair OFFSET with a real ORDER BY, exactly like LIMIT |

---

## Materials Checklist

Before class, have ready:

- `SQL Files/module2_phase1_sessions_4.2_to_5.2.db` loaded in the shared SQL sandbox - the same database as last session. Both `orders` (4 rows, exact-number exercises) and `orders_extended` (15 rows, Practical Block 2's multi-column sort exercise) are needed today.
- A projector for live query typing, especially for the Concept Block 3 LIMIT-without-ORDER-BY trap and the Concept Block 4 scrambled-clause-order error - both land hardest live.
- Printed/slide copies of the 4-row `orders` table for quick reference during Practical Blocks 1, 3, and 4.
- Printed/slide copy of the 15-row `orders_extended` table for Practical Block 2's multi-column sort exercise.
- The pre-read's ranking-question list for Practical Block 4, ready to reveal one at a time.

---

## Timing Contingencies

**If running long:**
- In Practical Block 2, walk through the answer key as a single whole-class demo rather than having every pair independently write and compare the full 13-row sorted output.
- Compress Practical Block 4 to 2 of the 3–4 business questions, assigning the rest as a take-home check.
- Never cut the LIMIT-without-ORDER-BY demonstration in Concept Block 3 - it is the single most consequential trap in this session, since a query that "runs and returns a plausible-looking number" is far more dangerous than one that visibly errors.

**If running short:**
- Run the Extension Blocks (LIMIT with OFFSET / pagination) in full.
- If only a few minutes remain, demonstrate the single OFFSET query from Concept Block 5 live as a whole-class walkthrough without the paired Practical Block 5.
- Alternatively, revisit the ties surfaced in the Opening and Concept Block 2 (Ramesh/Arjun at ₹120) and ask pairs to find a THIRD sort column that would fully resolve the tie into a repeatable, guaranteed order - a strong reinforcement of "the second column only matters when the first one ties" without needing new syntax.

---

## End-of-Session Quiz

1. **What direction does `ORDER BY price` sort in, if neither ASC nor DESC is written?**
   → Ascending (smallest first) - ASC is always the default.

2. **In `ORDER BY city ASC, price DESC`, when does the `price DESC` part actually affect the result?**
   → Only for rows that are already tied on `city` - it never re-sorts rows that already differ in city.

3. **Why is `LIMIT 3` with no `ORDER BY` described as "a random 3," not "a top 3"?**
   → Because without an ORDER BY, there's no defined "top" - LIMIT just returns however many rows the database happens to return first, in no guaranteed meaningful order.

4. **What is the correct fixed clause order for a query combining WHERE, ORDER BY, and LIMIT?**
   → SELECT, FROM, WHERE, ORDER BY, LIMIT, in that exact sequence.

5. **A WHERE clause filters a table down to only 2 matching rows, but the query says `LIMIT 5`. How many rows come back?**
   → 2 - LIMIT caps a maximum; it can't return more rows than actually exist after filtering.

6. **(If Extension Block covered) What does `LIMIT 2 OFFSET 1` do differently from `LIMIT 2`?**
   → It skips the first 1 row (by the current sort order) before returning the next 2, instead of starting from the very top.

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

**Q: Why did Ramesh and Arjun stay in the same relative order across both ASC and DESC sorts on price in Concept Block 1?**
→ Pure coincidence of this specific small dataset and this specific database engine's internal row storage order - not a rule you can rely on. The only way to guarantee tie order is to explicitly add another ORDER BY column.

**Q: What's the practical difference between `LIMIT 1` after an ascending sort and using a MIN function?**
→ Today, none for a single-column "smallest value" question - both give the same answer. Once we reach Aggregation Essentials, `MIN`/`MAX` will often be cleaner when you only need the single extreme value and nothing else from that row.

---

## Instructor Notes

- **Words not yet earned:** Avoid `GROUP BY`, `HAVING`, aggregate functions (`SUM`, `COUNT`, `AVG`, `MIN`, `MAX`), and window functions - these arrive starting next session (Aggregation Essentials) and later. If a student asks "can I sort by a total?", acknowledge that's coming very soon rather than answering in full now.
- **The single biggest risk in this session** is students treating ORDER BY as "obviously how it should work" and rushing past the ASC-default trap and the LIMIT-without-ORDER-BY trap. Both are quiet, easy-to-miss mistakes that produce a query which *runs* but *lies*. Slow down on both traps specifically - don't just mention them once.
- **Board management:** Keep the fixed clause order - `SELECT, FROM, WHERE, ORDER BY, LIMIT` - visible on the board all session. Point to it explicitly every time a student's query is scrambled. If running the Extension Block, add `OFFSET` to the end of that same skeleton rather than writing a separate one.
- **Common confusions, numbered:**
  1. Assuming unlabeled `ORDER BY` sorts largest-first. It doesn't - ASC is the default.
  2. Believing a second sort column re-sorts the whole result rather than just breaking ties within the first column.
  3. Using `LIMIT` alone and treating the result as a meaningful "top N" without an `ORDER BY` to define what "top" means.
  4. Expecting LIMIT to "pad out" a result to the requested count even when fewer matching rows exist after filtering.
- **Cross-references:** ORDER BY and LIMIT reappear almost immediately once GROUP BY is introduced (ranking cities or customers by total, not just individual rows). Tableau's built-in sort controls and pandas' `.sort_values()` / `.head()` mirror this exact logic in later modules; pandas' `.iloc[]` slicing is the direct analogue of LIMIT/OFFSET pagination.
- **Local/cultural context:** The cricket-scoreboard analogy for LIMIT lands especially well with this cohort - consider reusing "top run-scorers" language again once ranking-by-total questions appear with GROUP BY.
