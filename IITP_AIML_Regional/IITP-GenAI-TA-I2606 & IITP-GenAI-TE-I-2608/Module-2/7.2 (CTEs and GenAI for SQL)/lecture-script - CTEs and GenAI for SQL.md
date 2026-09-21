# Lecture Script: SQL for Data Analysis - CTEs and GenAI for SQL
> **Instructor Reference** - Module 2: SQL for Data Analysis | Academic Session 16 | Duration: 1.5 Hours | Instructor: Industry Mentor

---

## Session Overview

**Goal:** Students can rewrite a nested subquery as a clean, named CTE, chain multiple CTEs into a readable step-by-step query, and use GenAI to draft SQL safely - always verifying the output against the real schema and real data before trusting it.

**Student profile at this point:** They completed Session 15 (subqueries in WHERE, IN/NOT IN, subqueries in FROM) and can technically write correct nested queries - but nested parentheses get genuinely hard to read as steps multiply. They also completed Session 3 (GenAI for Analytics: Prompt, Check, Improve) early in the course, but have never applied that workflow specifically to SQL.

**Key outcome:** Students leave with two closely related reflexes: naming each step of a multi-part query clearly with a CTE, and treating any AI-generated SQL with the exact same scrutiny they'd give their own - schema check, run it, check for fan-out, never trust fluency alone.

> 🎯 **The one sentence this session must land:** *A CTE doesn't calculate anything a subquery couldn't - it just gives each step a name, so a human can follow it; and GenAI-generated SQL deserves that exact same "prove it to me" scrutiny as anything you'd write yourself.*

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| Opening - "Read this query out loud." | 8 min | 8 min |
| Concept Block 1: The WITH clause | 8 min | 16 min |
| Practical Block 1: Rewriting a subquery as a CTE | 10 min | 26 min |
| Concept Block 2: Chaining multiple CTEs | 10 min | 36 min |
| Practical Block 2: Building a two-step CTE query | 10 min | 46 min |
| **BREAK** | 5 min | 51 min |
| Concept Block 3: Prompt, Check, Improve for SQL | 10 min | 61 min |
| Practical Block 3: Writing a strong schema-aware prompt | 8 min | 69 min |
| Concept Block 4: Catching hallucinated SQL and repeated traps | 11 min | 80 min |
| Practical Block 4: Full verification challenge + Module 2 wrap | 10 min | 90 min |

*The core flow fills all 90 minutes. Concept/Practical Block 5, on asking GenAI to explain and improve a query you already wrote (rather than draft one from scratch), is in the Extension Blocks section - use only if ahead of pace.*

---

## Opening - "Read This Query Out Loud." (8 min)

Walk in and project, without comment, a deliberately dense nested query - Session 15's subquery-in-FROM example wrapped inside one more layer for effect:

```sql
SELECT * FROM (
    SELECT city_totals.city, city_totals.total_revenue
    FROM (
        SELECT customers.city, SUM(orders.price) AS total_revenue
        FROM customers
        INNER JOIN orders ON customers.customer_id = orders.customer_id
        GROUP BY customers.city
    ) AS city_totals
    WHERE city_totals.total_revenue > 100
) AS final_result
ORDER BY total_revenue DESC;
```

**Verified output (against `SQL Files/module2_phase2_sessions_6.1_to_6.2.db`, the same database as Sessions 13–15):**
```
city       total_revenue
---------  -------------
Bengaluru  240
Hyderabad  150
```

> *"Read this out loud to the person next to you. Not silently - out loud, start to finish."*

Let the room struggle a little with the nested parentheses.

> *"That struggle is the entire problem with today's session. Every piece of logic in there is something you already know how to write - subqueries, joins, GROUP BY. The struggle isn't the LOGIC. It's that nothing in this query has a NAME. You have to hold the whole nested structure in your head at once just to follow it."*

**Pivot line:**

> *"By the end of ninety minutes, you'll rewrite queries exactly like this one so they read top to bottom like a recipe - Step 1, Step 2, Step 3, each one named. And in the second half, we tackle something you'll actually do constantly on the job: using GenAI to draft SQL, and knowing exactly how to catch it when it's confidently wrong."*

**Context for the sessions ahead:** *"This is the last new SQL syntax in Module 2 - everything from here is about writing what you already know more clearly, and using AI tools responsibly to help you write it faster. Both of those habits carry directly into every module ahead."*

---

## Concept Block 1: The WITH Clause (8 min)

### 💬 Instructor script

> *"Here's the exact same logic from the Opening, rewritten."*

```sql
WITH city_totals AS (
    SELECT customers.city, SUM(orders.price) AS total_revenue
    FROM customers
    INNER JOIN orders ON customers.customer_id = orders.customer_id
    GROUP BY customers.city
)
SELECT city, total_revenue
FROM city_totals
WHERE total_revenue > 100;
```

Run it live: Bengaluru 240, Hyderabad 150 - identical result to Session 15's subquery-in-FROM version.

**Verified output - confirmed identical to the Opening's nested version:**
```
city       total_revenue
---------  -------------
Bengaluru  240
Hyderabad  150
```

> *"Same numbers. Same logic. The ONLY thing that changed is that city_totals now has a name, sitting clearly at the top, before the main query even starts. Read it out loud now - much easier, right?"*

### 🔴 The trap / highest-value moment

> *"One thing that trips people up: can I use city_totals again in a completely separate query later in my script?"*
> Let students guess, then confirm: no. *"A CTE only exists for the ONE statement it's attached to. The moment that query finishes, city_totals is gone - it's not a saved view, not a permanent table. Every single time you want to reuse it, you have to write the WITH clause again."*

**Prove it live - try to reference `city_totals` in a brand new, separate statement:**
```sql
SELECT * FROM city_totals;
```
```
Error: in prepare, no such table: city_totals
  SELECT * FROM city_totals;
         ^--- error here
```

> *"There it is - 'no such table.' city_totals was real for exactly one query, and it's already gone. If you genuinely need a reusable named result across multiple separate queries, that's a different, more permanent database object (a VIEW) - outside this course's scope, but good to know the term exists."*

---

## Practical Block 1: Rewriting a Subquery as a CTE (10 min)

**Activity:** Individually, students take Session 15's Practical Block 4 answer (tier_totals subquery-in-FROM, filtered above ₹200) and rewrite it as a CTE.

**Answer key with verified output:**
```sql
WITH tier_totals AS (
    SELECT customers.loyalty_tier, SUM(orders.price) AS total_revenue
    FROM customers
    INNER JOIN orders ON customers.customer_id = orders.customer_id
    GROUP BY customers.loyalty_tier
)
SELECT loyalty_tier, total_revenue
FROM tier_totals
WHERE total_revenue > 200;
```
```
loyalty_tier  total_revenue
------------  -------------
Gold          210
Silver        270
```

Result: Gold 210, Silver 270 - both tiers clear ₹200, identical to last session's subquery version. Say aloud: *"Confirm for yourselves - same numbers as last week. This is purely a readability upgrade, not a new calculation."*

> 💬 **Expect someone to ask if CTEs are just "the modern way" and subqueries are outdated.** Welcome it. Say: *"Not outdated - just better suited to different situations. A single, simple subquery is often fine as-is. The moment you're nesting more than one level, or want to reuse a calculation across multiple later steps, that's when CTEs start paying for themselves."*

---

## Concept Block 2: Chaining Multiple CTEs (10 min)

### 💬 Instructor script

> *"CTEs get genuinely powerful once you chain more than one - each step building on the last, like a recipe."*

```sql
WITH city_totals AS (
    SELECT customers.city, SUM(orders.price) AS total_revenue
    FROM customers
    INNER JOIN orders ON customers.customer_id = orders.customer_id
    GROUP BY customers.city
),
top_cities AS (
    SELECT city, total_revenue
    FROM city_totals
    WHERE total_revenue > 100
)
SELECT *
FROM top_cities
ORDER BY total_revenue DESC
LIMIT 1;
```

Run it live: Bengaluru, 240 - the single top city.

**Verified output:**
```
city       total_revenue
---------  -------------
Bengaluru  240
```

> *"Read it out loud, step by step: first calculate city_totals. Then, from THAT, keep only top_cities above 100. Finally, from top_cities, give me the single highest one. Three clearly named steps - nothing here is nested inside anything else."*

### 🔴 The trap / highest-value moment

> *"Quick question: could city_totals, defined FIRST, reference top_cities, defined SECOND?"*
> Let the room reason it out. *"In standard SQL - and in most databases you'll meet on the job, including PostgreSQL and SQL Server - the answer is no: CTEs can only look backward, at steps already defined above them, never forward. Write this down as the rule to rely on: top-to-bottom only, unless you have a specific reason to know your database is more permissive."*

**Test it live by deliberately breaking the order - and here's a genuinely useful surprise worth showing honestly:**
```sql
WITH city_totals AS (
    SELECT city, total_revenue FROM top_cities WHERE total_revenue > 200
),
top_cities AS (
    SELECT customers.city, SUM(orders.price) AS total_revenue
    FROM customers INNER JOIN orders ON customers.customer_id = orders.customer_id
    GROUP BY customers.city
)
SELECT * FROM city_totals;
```

**Verified: on this course's SQLite version, this does NOT error - it correctly resolves the forward reference and returns `Bengaluru, 240`.**

> *"That probably isn't what you expected, and it's an important, honest lesson in its own right: this specific version of SQLite is smart enough to figure out the dependency between these two CTEs regardless of the order they're written in - it's more permissive than the standard rule I just gave you. This is exactly the same pattern you've now seen several times this module: SQLite is often more forgiving than stricter databases like PostgreSQL or SQL Server, where this exact query WOULD fail with something like 'relation top_cities does not exist.' The lesson isn't 'forward references are always fine' - it's 'never assume your local database's leniency is a universal SQL guarantee.' Write your CTEs top-to-bottom in dependency order as a portable habit, even on a database that happens to tolerate skipping it."*

---

## Practical Block 2: Building a Two-Step CTE Query (10 min)

**Activity:** Pairs write a chained two-CTE query: first, average order price per loyalty tier; second, keep only tiers whose average clears ₹100.

**Answer key with verified output:**
```sql
WITH tier_avg AS (
    SELECT customers.loyalty_tier, AVG(orders.price) AS avg_price
    FROM customers
    INNER JOIN orders ON customers.customer_id = orders.customer_id
    GROUP BY customers.loyalty_tier
),
strong_tiers AS (
    SELECT loyalty_tier, avg_price
    FROM tier_avg
    WHERE avg_price > 100
)
SELECT * FROM strong_tiers;
```
```
loyalty_tier  avg_price
------------  ---------
Gold          105.0
Silver        135.0
```

Walk through one pair's live output and confirm both tiers (Gold avg 105.0, Silver avg 135.0) clear ₹100 here.

> 💬 **Expect a pair to try doing both steps in ONE CTE instead of two.** Welcome it - ask them to try, and discuss live whether it's actually possible here.

**Verify this live - filtering on an alias inside the SAME CTE that defines it genuinely fails:**
```sql
WITH tier_avg AS (
    SELECT customers.loyalty_tier, AVG(orders.price) AS avg_price
    FROM customers INNER JOIN orders ON customers.customer_id = orders.customer_id
    GROUP BY customers.loyalty_tier
    HAVING avg_price > 100
)
SELECT * FROM tier_avg;
```
```
loyalty_tier  avg_price
------------  ---------
Gold          105.0
Silver        135.0
```

> *"Interesting - SQLite actually allows referencing the `avg_price` alias inside HAVING here and gets the right answer, which isn't guaranteed behavior in every database. The more universally portable version repeats the full expression: `HAVING AVG(orders.price) > 100`, verified to give the identical result. Either way, this specific example COULD collapse into one step using HAVING - so when do you genuinely need two CTEs instead of one? When the second step needs something HAVING can't express as a simple aggregate condition - like joining the first result to a third table, or applying a second, unrelated aggregation on top."* This is a great moment to reinforce WHY chaining exists, not just how.

---

## BREAK (5 min)

---

## Concept Block 3: Prompt, Check, Improve for SQL (10 min)

### 💬 Instructor script

> *"Callback to Session 3, right at the start of this course - Prompt, Check, Improve. Today we apply that exact same cycle to SQL specifically."*

Write two prompts on the board side by side:

> **Weak:** *"Write a SQL query showing total revenue by city."*
> **Strong:** *"I have two tables. customers has columns: customer_id, customer_name, city, loyalty_tier. orders has columns: order_id, customer_id, item, quantity, price, order_date. Write a SQL query joining them to show total revenue (SUM of price) by city."*

> *"What's actually different between these two prompts?"*

Let the room identify: the strong one gives real column and table names.

### 🔴 The trap / highest-value moment

> *"Here's the uncomfortable truth about the weak prompt: the AI won't refuse to answer it. It won't say 'I don't know your schema.' It will confidently GUESS a schema that sounds reasonable - and you're about to see exactly what that guess looks like, and why it's dangerous, in the next block."*

---

## Practical Block 3: Writing a Strong Schema-Aware Prompt (8 min)

**Activity:** Individually, students write a strong, schema-aware prompt (in plain text, not run through an actual AI tool live unless your setup allows it) asking for "which customers have placed more than one order."

**Model strong prompt to reveal after the activity:**

> *"I have two tables. customers has columns: customer_id, customer_name, city, loyalty_tier. orders has columns: order_id, customer_id, item, quantity, price, order_date, with customer_id as a foreign key referencing customers. Write a SQL query that returns the customer_name of every customer who has placed more than one order in the orders table."*

**If your setup allows a live AI check, here is the verified correct answer this prompt should produce, checked against the real data:**
```sql
SELECT customers.customer_name
FROM customers
INNER JOIN orders ON customers.customer_id = orders.customer_id
GROUP BY customers.customer_id, customers.customer_name
HAVING COUNT(orders.order_id) > 1;
```
```
(0 rows returned)
```

> *"Zero rows - and that's the CORRECT answer, not a bug. In our actual table, every one of the four customers with orders placed exactly one order each; nobody has two. This is a good moment to underline: a correct query returning an empty, boring result is still a completely successful query. Don't second-guess a correct query just because its answer isn't dramatic."*

**Answer key with reasoning:** A strong version explicitly lists `customers` and `orders` columns, states the join key (`customer_id`), and states the exact business question. Cold-call 2–3 students to read theirs aloud; check as a class whether each includes enough schema detail that an AI genuinely couldn't guess wrong.

> 💬 **Expect a student to write a technically detailed but overly long prompt and ask if that's necessary.** Welcome it. Say: *"More schema detail is rarely wasted - the risk is almost always UNDER-specifying, not over-specifying. When in doubt, include more of your real structure, not less."*

---

## Concept Block 4: Catching Hallucinated SQL and Repeated Traps (11 min)

### 💬 Instructor script

> *"Remember Session 13 - city USED to live directly on orders, then we deliberately moved it into customers. Watch what happens when I ask an AI for 'total revenue by city' without giving it our current schema."*

Show the plausible AI output:
```sql
SELECT city, SUM(price) AS total_revenue
FROM orders
GROUP BY city;
```

Run it live - let the "no such column: city" error appear.

**Verified error - genuinely reproducible against the real database:**
```
Error: in prepare, no such column: city
  SELECT city, SUM(price) AS total_revenue FROM orders GROUP BY city;
         ^--- error here
```

> *"This is FLUENT, well-formatted, completely plausible SQL - for a schema that doesn't exist anymore in our database. The AI wasn't 'wrong' about SQL syntax at all. It was wrong about OUR specific tables, because we never told it what they actually look like."*

Now show the corrected version, using the strong prompt's schema info:
```sql
SELECT customers.city, SUM(orders.price) AS total_revenue
FROM customers
INNER JOIN orders ON customers.customer_id = orders.customer_id
GROUP BY customers.city;
```

Run it live - **verified output:**
```
city       total_revenue
---------  -------------
Bengaluru  240
Hyderabad  150
Chennai    90
```

### 🔴 The trap / highest-value moment

> *"One more layer, and this is the one that should genuinely worry you. Even a SCHEMA-CORRECT, error-free AI query can still walk straight into Session 14's fan-out trap. If I ask an AI for 'total revenue by customer, including their saved delivery addresses,' it might confidently join orders to customer_addresses - and just like two sessions ago, silently double Ramesh's revenue to 240."*

Run the AI-plausible fan-out query live:
```sql
SELECT orders.customer_id, SUM(orders.price) AS naive_total
FROM orders
INNER JOIN customer_addresses ON orders.customer_id = customer_addresses.customer_id
WHERE orders.customer_id = 1
GROUP BY orders.customer_id;
```

**Verified output - the exact same inflated figure from Session 14's Opening:**
```
customer_id  naive_total
-----------  -----------
1            240
```

> *"No error. No warning. A perfectly fluent, schema-correct query, with a silently wrong number. GenAI does not automatically know which of your tables have one-to-many relationships - it has to be told, or it has to be caught by YOU, the reviewer. Every single check from Sessions 14 and 15 - fan-out, fair comparison, schema accuracy - applies in full to AI-generated SQL. Fluency is not correctness. Ever."*

**Show the AI-drafted fix too, using what students already know from Session 15 - aggregate first, in a CTE, before joining:**
```sql
WITH real_totals AS (
    SELECT customer_id, SUM(price) AS real_total FROM orders GROUP BY customer_id
)
SELECT real_totals.customer_id, real_totals.real_total, customer_addresses.address_label
FROM real_totals
INNER JOIN customer_addresses ON real_totals.customer_id = customer_addresses.customer_id
WHERE real_totals.customer_id = 1;
```
```
customer_id  real_total  address_label
-----------  ----------  -------------
1            120         Home
1            120         Office
```

> *"Ramesh's row still appears twice - once per address, which is genuinely correct if you want both addresses listed - but his `real_total` now correctly reads 120 on both rows, not 240. This is the CTE version of last session's fix: name the safe aggregation step, then join to it."*

---

## Practical Block 4: Full Verification Challenge + Module 2 Wrap (10 min)

**Activity:** Pairs are handed 2 "AI-generated" queries (one genuinely correct, one containing either a hallucinated column or an unchecked fan-out) and must determine, by actually running each against the real database, which is trustworthy and why.

**The two queries to hand out, with verified outcomes for your answer key:**

**Query A (hallucinated schema):**
```sql
SELECT customer_name, city, SUM(price) AS total_revenue
FROM orders
GROUP BY city;
```
Running this against the real database produces: `Error: in prepare, no such column: customer_name` - `customer_name` and `city` both live on `customers`, not `orders`. **Verdict: broken, hallucinated schema.**

**Query B (correct, schema-aware, fan-out-safe):**
```sql
WITH customer_totals AS (
    SELECT customer_id, SUM(price) AS total_revenue FROM orders GROUP BY customer_id
)
SELECT customers.customer_name, customer_totals.total_revenue
FROM customers
INNER JOIN customer_totals ON customers.customer_id = customer_totals.customer_id
ORDER BY customer_totals.total_revenue DESC;
```
**Verified output:**
```
customer_name  total_revenue
-------------  -------------
Fatima         150
Ramesh         120
Arjun          120
Priya          90
```
**Verdict: correct** - joins on the real schema, aggregates before joining (fan-out-safe), Karthik correctly absent since INNER JOIN was deliberately chosen here (he has no order total to show).

**Answer key with reasoning:** Walk through both live as a class at the end. For the flawed one, have the pair state explicitly which of today's or last two sessions' checks caught it.

> 💬 **Expect at least one pair to trust the fluent-sounding query without running it first.** Welcome it - this is the exact behaviour the whole session exists to interrupt. Say: *"That's the instinct to unlearn, starting today. Fluent isn't proof. Running it against real data is proof."*

**Module 2 wrap (fold into this block's final 2 minutes):** Briefly walk the room through the full arc - SELECT/WHERE (Session 9) → sorting (10) → aggregation (11) → grouping (12) → joins (13) → verifying joined insights (14) → subqueries (15) → CTEs and safe AI use (16). Name it as a complete, real analyst toolkit, not a checklist of disconnected topics.

---

## Extension Blocks (Optional — Use if Running Ahead)

*Not part of the 90-minute core flow. Use only if Practical Block 4 finishes early - see Timing Contingencies.*

### Concept Block 5 (Extension): Asking GenAI to Explain and Improve, Not Just Draft

#### 💬 Instructor script

> *"So far today, GenAI has drafted queries FOR us. There's a second, equally valuable use: handing GenAI a query YOU already wrote, and asking it to explain or improve it."*

Write the Opening's original nested query back on the board:
```sql
SELECT * FROM (
    SELECT city_totals.city, city_totals.total_revenue
    FROM (
        SELECT customers.city, SUM(orders.price) AS total_revenue
        FROM customers
        INNER JOIN orders ON customers.customer_id = orders.customer_id
        GROUP BY customers.city
    ) AS city_totals
    WHERE city_totals.total_revenue > 100
) AS final_result
ORDER BY total_revenue DESC;
```

> *"A strong prompt here isn't 'fix my query' - it's specific: 'Here is a SQL query using nested subqueries. Rewrite it using a WITH clause (CTE) instead, keeping the exact same logic and result. Explain each step.' That's a request an AI is genuinely good at, and one where the risk of hallucination is much lower - it's transforming logic you already verified, not inventing new logic against a schema it's guessing at."*

#### 🔴 The trap / highest-value moment

> *"Here's the check that still applies, even for this lower-risk use case: does the 'improved' query still return the SAME result as your original? Run BOTH, side by side, and compare. An AI 'simplification' that quietly changes the actual output isn't an improvement - it's a new bug wearing a cleaner outfit. Verify before and after, every time, even for a rewrite."*

**Demonstrate the check live - both queries, run side by side, must match:**

Original nested version → `Bengaluru 240, Hyderabad 150` (verified in the Opening).
CTE rewrite → `Bengaluru 240, Hyderabad 150` (verified in Concept Block 1).

> *"They match, exactly. That's what a trustworthy AI-assisted rewrite looks like - not just 'it looks cleaner,' but 'I checked, and it produces the identical answer.'"*

### Practical Block 5 (Extension): Verifying an AI "Improvement"

**Activity:** Pairs are given an "AI-suggested improvement" to Practical Block 2's two-CTE query that collapses it into one CTE using HAVING (shown in Concept Block 2's trap discussion), and must verify it produces the identical result before accepting it.

**Verified answer key:**

Two-CTE original:
```sql
WITH tier_avg AS (
    SELECT customers.loyalty_tier, AVG(orders.price) AS avg_price
    FROM customers INNER JOIN orders ON customers.customer_id = orders.customer_id
    GROUP BY customers.loyalty_tier
),
strong_tiers AS (
    SELECT loyalty_tier, avg_price FROM tier_avg WHERE avg_price > 100
)
SELECT * FROM strong_tiers;
```
→ `Gold 105.0, Silver 135.0`

"AI-suggested" one-CTE version:
```sql
WITH tier_avg AS (
    SELECT customers.loyalty_tier, AVG(orders.price) AS avg_price
    FROM customers INNER JOIN orders ON customers.customer_id = orders.customer_id
    GROUP BY customers.loyalty_tier
    HAVING AVG(orders.price) > 100
)
SELECT * FROM tier_avg;
```
→ `Gold 105.0, Silver 135.0`

> *"Identical results, confirmed by actually running both - so this particular 'simplification' is safe to accept. That confirmation step is the whole point of the exercise, not the simplification itself."*

> 💬 **Expect a pair to accept the "improvement" without running the comparison, since both queries "look" equivalent.** Welcome it - press them: *"Looking equivalent and being verified-identical are two different confidence levels. Which one would you put your name on in a report?"*

---

## Common Errors

| Error | What causes it | Fix |
|---|---|---|
| `no such table: <cte_name>` in a separate later query | Trying to reuse a CTE beyond the single statement it was defined in | Rewrite the WITH clause again for every new query that needs it - a CTE is not a permanent, reusable object |
| `no such table: <cte_name>` from referencing a CTE defined below it | Writing CTEs out of dependency order | Order CTEs so each one only references CTEs already defined above it |
| Believing a fluent, well-formatted AI-drafted query is automatically correct | Trusting fluency as a proxy for correctness | Run every AI-drafted query against the real schema and real data before trusting its output |
| `no such column: city` from AI-drafted SQL | Not giving the AI your actual current schema, letting it guess a plausible but wrong one | Always supply real table and column names in the prompt - schema detail is rarely "too much" |
| AI-drafted SQL walking into a fan-out (e.g. joining to `customer_addresses` for a revenue total) | GenAI has no built-in awareness of your specific one-to-many relationships | Apply the same fan-out check from Session 14 to AI-generated SQL - aggregate before joining, or verify row counts |
| Accepting an "AI-improved" query without checking it returns the same result | Assuming a cleaner-looking rewrite is automatically equivalent | Run the original and the "improved" version side by side and confirm identical output before accepting the rewrite |
| Treating an empty (zero-row) AI-verification result as a sign something went wrong | Assuming a correct query must return a dramatic or non-empty result | Confirm zero rows is a legitimate, correct answer to some real business questions - check the LOGIC, not the row count, for correctness |
| Writing an under-specified prompt ("write a query showing revenue by city") | Assuming the AI will ask for missing schema details rather than guessing | Always include real column and table names, and the exact business question, in the prompt itself |

---

## Materials Checklist

Before class, have ready:

- `SQL Files/module2_phase2_sessions_6.1_to_6.2.db` loaded in the shared SQL sandbox - same database and schema as Sessions 13–15.
- A projector for live queries - the `no such table: city_totals` reuse-across-statements error, the CTE-ordering error, the hallucinated-schema error, and the fan-out demonstration are this session's four highest-value live moments.
- If your setup allows a live GenAI tool during Practical Block 3 or the Extension Block, have it ready and pre-tested with the exact prompts in this script; if not, run those blocks as text-only exercises using the model answers provided.
- The two "AI-generated" queries for Practical Block 4's verification challenge, printed or on slides, ready to hand out.
- A recap slide or board layout for the Module 2 wrap (Sessions 9 through 16 in sequence) for the final two minutes.

---

## Timing Contingencies

**If running long:**
- Skip the live "reorder the CTEs to break it" demonstration in Concept Block 2 and state the resulting error verbally instead.
- Compress Practical Block 3 to a single cold-called strong prompt read aloud, rather than checking multiple students' prompts individually.
- Never cut the Concept Block 4 fan-out-in-AI-generated-SQL demonstration - it is the single most important idea in the whole session, since it's the moment students realize GenAI doesn't inherit any of the verification habits built across Sessions 14 and 15 automatically.

**If running short:**
- Run the Extension Blocks (asking GenAI to explain/improve an existing query) in full.
- If only a few minutes remain, demonstrate the single before/after CTE-rewrite comparison from Concept Block 5 live as a quick capstone, without the paired Practical Block 5.
- Alternatively, use any remaining time to extend the Module 2 wrap into a genuinely reflective 5-minute discussion: ask students to name, unprompted, the single riskiest silent-failure moment from the entire module (SUM(city) returning 0.0, ORDER BY after GROUP BY, NOT IN with NULL, or AI-generated fan-out are all strong candidates) and explain why it worried them most.

---

## End-of-Session Quiz

1. **What does a CTE actually calculate differently from an equivalent subquery?**
   → Nothing - a CTE produces the identical result as an equivalent nested subquery; the only difference is that it's named and appears before the main query, making it easier to read.

2. **Can a CTE be reused in a separate query written later in the same script?**
   → No - a CTE only exists for the single statement it's attached to; referencing it afterward produces a "no such table" error.

3. **In a chain of multiple CTEs, can an earlier-defined CTE reference a later one?**
   → No - CTEs can only reference CTEs already defined above them, never ones defined below.

4. **Why did `SELECT city, SUM(price) FROM orders GROUP BY city;` fail against this session's database, even though it's syntactically valid SQL?**
   → `city` doesn't exist on the `orders` table in this schema - it lives on `customers` - so the query fails with "no such column," even though nothing is syntactically wrong with it.

5. **Why is a schema-correct, error-free AI-generated query not automatically trustworthy?**
   → It can still walk into a join fan-out or other logical trap (like the ones covered in Sessions 14 and 15) that produces a plausible but wrong number, with no error or warning at all.

6. **(If Extension Block covered) What's the correct way to verify an AI-suggested "simplification" of a query you already wrote?**
   → Run both the original and the suggested version and confirm they return the identical result before accepting the change - a cleaner-looking query isn't automatically an equivalent one.

---

## Q&A & Doubt Solving

**Q: Is a CTE ever actually faster than a subquery, not just more readable?**
→ In some databases, yes - certain engines can optimize CTEs differently, sometimes calculating them once and reusing the result if referenced multiple times. This varies by database; for this course, treat the readability benefit as the primary reason to use one.

**Q: Can a CTE reference itself (a "recursive" CTE)?**
→ Yes, in some databases - used for things like organizational hierarchies or running totals. That's an advanced technique beyond this course's current scope; know the term exists for when you encounter it later in your career.

**Q: Should I always give GenAI my entire database schema, every single time?**
→ For any query involving more than one table, yes - it costs you a few extra seconds of typing and removes almost all the risk of a hallucinated column or table name. For single-table, simple requests, it's a smaller risk but still good habit.

**Q: If I always have to check GenAI's SQL output anyway, does it actually save time?**
→ Usually yes - drafting the first version and checking it is typically faster than writing every query from scratch, especially for complex joins or multi-step logic. The time saved comes from drafting speed, not from skipping verification - never skip verification to "save" more time.

**Q: What's the single most important habit from this whole session?**
→ Run it before you trust it - whether you wrote the query yourself or an AI did. That one habit catches almost everything else this session covered.

**Q: In Practical Block 4, why did Karthik not appear in the "correct" Query B, even though it's supposed to be trustworthy?**
→ Query B deliberately used INNER JOIN, which only keeps matched rows - Karthik has no order total to show, so his correct and intentional absence there is different from the earlier, wrongly-schema'd Query A simply erroring out. A trustworthy query can still legitimately exclude a row; the test is whether that exclusion was the actual intent.

**Q: Does asking GenAI to "explain" a query I already wrote carry the same hallucination risk as asking it to draft one from scratch?**
→ Generally lower risk, since it's working from logic you already supplied rather than inventing a schema from nothing - but the verification habit (run before/after and compare) still applies in full, as shown in the Extension Block.

---

## Instructor Notes

- **Words not yet earned:** Avoid recursive CTEs, window functions, and query performance optimization - these are meaningfully more advanced and outside this course's scope. If asked, acknowledge they exist as a "later in your career" topic rather than demonstrating.
- **The single biggest risk in this session** is students treating the GenAI-verification content as less important than the CTE syntax, since it's not "new SQL" in the same way. Counter this directly: on the job, most of these students WILL use GenAI to draft SQL constantly - the verification habit is arguably the more career-relevant half of today.
- **Board management:** Keep the "before/after" nested-query vs. CTE comparison from the Opening and Concept Block 1 visible all session as the throughline - refer back to it explicitly when introducing chained CTEs in Concept Block 2.
- **Common confusions, numbered:**
  1. Believing a CTE persists beyond the single query it's attached to.
  2. Trying to reference a later-defined CTE from an earlier one.
  3. Trusting a GenAI-generated query because it's fluent or well-formatted, without running it.
  4. Assuming GenAI automatically knows a database's one-to-many relationships and won't cause a fan-out.
- **Cross-references:** This session deliberately closes the loop on Sessions 13, 14, and 15's traps by applying them to AI-generated SQL - make all three callbacks explicit rather than assuming students will make the connection themselves. Session 3's Prompt-Check-Improve framework is the direct ancestor of today's Concept Block 3; naming that connection aloud reinforces that GenAI workflows are consistent across the whole course, not session-specific.
- **Local/cultural context:** This is the final session of Module 2 - consider a genuinely brief moment (30–60 seconds, folded into Practical Block 4) acknowledging the full arc from Session 9's first SELECT to today's verified, AI-assisted, multi-table queries. Cohorts respond well to an explicit "look how far you've come" moment at a natural module boundary like this one.
