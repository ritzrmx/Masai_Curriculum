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

> *"Same numbers. Same logic. The ONLY thing that changed is that city_totals now has a name, sitting clearly at the top, before the main query even starts. Read it out loud now - much easier, right?"*

### 🔴 The trap / highest-value moment

> *"One thing that trips people up: can I use city_totals again in a completely separate query later in my script?"*
> Let students guess, then confirm: no. *"A CTE only exists for the ONE statement it's attached to. The moment that query finishes, city_totals is gone - it's not a saved view, not a permanent table. Every single time you want to reuse it, you have to write the WITH clause again."*

---

## Practical Block 1: Rewriting a Subquery as a CTE (10 min)

**Activity:** Individually, students take Session 15's Practical Block 4 answer (tier_totals subquery-in-FROM, filtered above ₹200) and rewrite it as a CTE.

**Answer key with reasoning:**
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
Result: Silver 270, Gold 210 - identical to last session's subquery version. Say aloud: *"Confirm for yourselves - same numbers as last week. This is purely a readability upgrade, not a new calculation."*

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

> *"Read it out loud, step by step: first calculate city_totals. Then, from THAT, keep only top_cities above 100. Finally, from top_cities, give me the single highest one. Three clearly named steps - nothing here is nested inside anything else."*

### 🔴 The trap / highest-value moment

> *"Quick question: could city_totals, defined FIRST, reference top_cities, defined SECOND?"*
> Let the room reason it out - no. *"CTEs can only look backward, at steps already defined above them. Never forward. This is exactly like a recipe - Step 3 can reference Step 1's dough, but Step 1 can't reference an ingredient you haven't prepared yet in Step 3. Write this down: top-to-bottom only."*

---

## Practical Block 2: Building a Two-Step CTE Query (10 min)

**Activity:** Pairs write a chained two-CTE query: first, average order price per loyalty tier; second, keep only tiers whose average clears ₹100.

**Answer key with reasoning:**
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
Walk through one pair's live output and confirm both tiers (Gold avg 105, Silver avg 135) clear ₹100 here.

> 💬 **Expect a pair to try doing both steps in ONE CTE instead of two.** Welcome it - ask them to try, and discuss live whether it's actually possible here (filtering on an alias like `avg_price` inside the SAME CTE that defines it usually isn't allowed) versus genuinely needing the second step. This is a great moment to reinforce WHY chaining exists, not just how.

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

> *"This is FLUENT, well-formatted, completely plausible SQL - for a schema that doesn't exist anymore in our database. The AI wasn't 'wrong' about SQL syntax at all. It was wrong about OUR specific tables, because we never told it what they actually look like."*

Now show the corrected version, using the strong prompt's schema info:
```sql
SELECT customers.city, SUM(orders.price) AS total_revenue
FROM customers
INNER JOIN orders ON customers.customer_id = orders.customer_id
GROUP BY customers.city;
```

Run it live - Bengaluru 240, Hyderabad 150, Chennai 90.

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
Result: 240 - wrong, doubled.

> *"No error. No warning. A perfectly fluent, schema-correct query, with a silently wrong number. GenAI does not automatically know which of your tables have one-to-many relationships - it has to be told, or it has to be caught by YOU, the reviewer. Every single check from Sessions 14 and 15 - fan-out, fair comparison, schema accuracy - applies in full to AI-generated SQL. Fluency is not correctness. Ever."*

---

## Practical Block 4: Full Verification Challenge + Module 2 Wrap (10 min)

**Activity:** Pairs are handed 2 "AI-generated" queries (one genuinely correct, one containing either a hallucinated column or an unchecked fan-out) and must determine, by actually running each against the real database, which is trustworthy and why.

**Answer key with reasoning:** Walk through both live as a class at the end. For the flawed one, have the pair state explicitly which of today's or last two sessions' checks caught it.

> 💬 **Expect at least one pair to trust the fluent-sounding query without running it first.** Welcome it - this is the exact behaviour the whole session exists to interrupt. Say: *"That's the instinct to unlearn, starting today. Fluent isn't proof. Running it against real data is proof."*

**Module 2 wrap (fold into this block's final 2 minutes):** Briefly walk the room through the full arc - SELECT/WHERE (Session 9) → sorting (10) → aggregation (11) → grouping (12) → joins (13) → verifying joined insights (14) → subqueries (15) → CTEs and safe AI use (16). Name it as a complete, real analyst toolkit, not a checklist of disconnected topics.

---

## Summary & Bridge

**Recap table:**

| Concept | The one thing to remember |
|---|---|
| WITH clause | Same logic as a subquery - just named, so a human can follow it |
| Chaining CTEs | Each step can reference steps ABOVE it, never below |
| Prompt, Check, Improve for SQL | Give the AI your real schema; never skip running its output |
| Verifying GenAI SQL | Fluent and error-free is not the same as correct - check for hallucinated schema AND fan-out |

**Close on the thesis line:**

> *"At the start of today, that nested query was genuinely hard to read out loud. Now you can name every step of it clearly with a CTE - and you know that the exact same 'prove it to me' scrutiny you just learned to apply to your OWN queries has to apply to anything GenAI hands you too. A CTE doesn't calculate anything new. Careful verification doesn't slow you down, on average - it's what makes speed safe."*

**Bridge to next session - and Module 3:**

> *"That's Module 2, complete. You went from your very first SELECT statement to writing multi-step, verified, AI-assisted queries against real relational data. Next session opens Module 3 - Statistics: Probability and Uncertainty - the start of Tableau Dashboards and Storytelling. And notice: every KPI, every join, every verified number you built in SQL over these nine sessions is exactly what you'll be visualizing next."*

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
