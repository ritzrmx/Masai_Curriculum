# Lecture Script: SQL for Data Analysis - Insights from Combined Data
> **Instructor Reference** - Module 2: SQL for Data Analysis | Academic Session 14 | Duration: 1.5 Hours | Instructor: Professor

---

## Session Overview

**Goal:** Students can take a joined, grouped SQL result and (1) check it for join fan-out inflation, (2) compare groups fairly using rates instead of raw totals, and (3) write a Finding/Evidence/Implication insight that doesn't overreach into causation.

**Student profile at this point:** They completed Session 13 (INNER JOIN, LEFT JOIN) and can technically write a correct joined query. They have **not yet been taught that a technically correct joined query can still produce a misleading number** - that's the entire point of today.

**Key outcome:** Students leave with a reflex: before sharing any number from a joined table, ask *"could this be duplicated, and am I comparing fairly?"* - the exact judgment that separates a query that runs from a number a manager can actually trust.

> 🎯 **The one sentence this session must land:** *A joined query can run perfectly and still lie to you - correctness of syntax and correctness of meaning are two different things, and today is about the second one.*

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| Opening - "Ramesh spent HOW much?" | 8 min | 8 min |
| Concept Block 1: From numbers to insight | 8 min | 16 min |
| Practical Block 1: Fact vs. insight sorting exercise | 8 min | 24 min |
| Concept Block 2: The join fan-out trap | 12 min | 36 min |
| Practical Block 2: Catching the fan-out live | 12 min | 48 min |
| **BREAK** | 5 min | 53 min |
| Concept Block 3: Comparing groups fairly | 10 min | 63 min |
| Practical Block 3: Rate vs. raw total challenge | 10 min | 73 min |
| Concept Block 4: Writing the insight, without overreaching | 8 min | 81 min |
| Practical Block 4: Full insight-writing challenge | 9 min | 90 min |

---

## Opening - "Ramesh Spent HOW Much?" (8 min)

Walk in and project a query live: join `orders` to `customer_addresses` (from the pre-read), then run `SELECT customer_id, SUM(price) AS total_spent FROM ... GROUP BY customer_id;` on top of it - showing Ramesh at ₹240.

> *"According to this query, Ramesh spent ₹240 with us. Let's pull up his actual order history."*

Show the real `orders` table - Ramesh has exactly **one** order, ₹120.

> *"So which is it - ₹120, or ₹240? Both numbers came out of SQL. Both queries ran without a single error. One of them is simply wrong. If you can't explain why, you are not ready to hand a joined number to a manager - and by the end of today, you will be."*

**Pivot line:**

> *"Everything we've done in this module so far has been about writing SQL that RUNS correctly. Today is about something different and, honestly, more important: writing SQL - and reading its output - in a way that's actually TRUE. A query with zero syntax errors can still produce a completely misleading number, and today you learn to catch it before it reaches someone's inbox."*

**Context for the sessions ahead:** *"This exact judgment - is this number real, and am I comparing fairly - is what separates someone who can run SQL from someone a manager actually trusts with numbers. It's the same judgment you'll need reading a Tableau dashboard next module, and writing insights with GenAI later in the course."*

---

## Concept Block 1: From Numbers to Insight (8 min)

### 💬 Instructor script

> *"Quick callback to Session 2 - a query result is like a doctor's printout of vitals. It's not yet a diagnosis."*

Project last session's result:

| loyalty_tier | total_revenue |
|---|---|
| Gold | 210 |
| Silver | 270 |

> *"'Gold revenue is 210, Silver is 270' - is that an insight, or just a fact?"*

Let the room debate. Land on: it's a fact. Then reveal the insight version: *"Silver-tier customers are currently generating more total revenue than Gold - our 'premium' tier - which is worth investigating before we invest further in Gold-specific perks."*

### 🔴 The trap / highest-value moment

> *"The difference between those two sentences is THREE things: a comparison, something surprising flagged, and a suggested next step. From today onward, no joined or grouped query result leaves this room without at least an attempt at those three things. A number is not done until someone has asked 'so what?'"*

---

## Practical Block 1: Fact vs. Insight Sorting Exercise (8 min)

**Activity:** Hand out 5 short statements (mix of bare facts and real insights, e.g., "Chennai had 1 order this week" vs. "Chennai is currently our lowest-activity city - worth checking if our delivery radius even covers it properly"). Pairs sort them into "fact only" vs. "insight."

**Answer key with reasoning:** Confirm as a class, and for every "fact only" statement, ask the room to upgrade it live into a real insight by adding a comparison, a flagged pattern, or an implication.

> 💬 **Expect a pair to over-correct and add speculation not supported by any number at all.** Welcome it. Say: *"An insight still has to be tied to actual evidence - 'worth investigating' is fine, 'this is definitely because of X' with no evidence behind it is not. We'll draw that line precisely in Concept Block 4."*

---

## Concept Block 2: The Join Fan-Out Trap (12 min)

### 💬 Instructor script

Return to the Opening's ₹240-vs-₹120 mystery.

> *"Let's actually find out what happened. Here's Ramesh's single order, joined to his saved addresses."*

```sql
SELECT orders.order_id, orders.price, customer_addresses.address_label
FROM orders
INNER JOIN customer_addresses
  ON orders.customer_id = customer_addresses.customer_id;
```

Run it live - Ramesh's order appears **twice**, once per saved address (Home, Office).

> *"His one real order just became two rows. If I SUM the price column now, without noticing, I get 240 - double his actual spend. This is called a fan-out: joining to a table where one side has MULTIPLE matches duplicates the rows on the other side."*

### 🔴 The trap / highest-value moment

> *"Here's the part that should genuinely worry you: this query has ZERO errors. It ran perfectly. SQL will never warn you that a join fanned out - it's not a bug, it's working exactly as designed. Catching this is entirely on you, the analyst. Before trusting any SUM or COUNT after a join, ask: could either side have more than one match on the other side? If yes, stop and check your row counts before you trust the total."*

---

## Practical Block 2: Catching the Fan-Out Live (12 min)

**Activity:** Pairs run the full `orders` + `customer_addresses` join (all customers, not just Ramesh) and identify: which customers get duplicated, and by how much does the naive `SUM(price)` overstate total revenue compared to the real `orders` table total?

**Answer key with reasoning:** Only Ramesh has 2 addresses, so only his order duplicates; total naive SUM is inflated by exactly his order's price (₹120 extra). Say aloud: *"Notice it's not even a big, obvious distortion - ₹120 out of a few hundred could easily slip past a tired analyst at 6pm. Small, quiet errors like this are exactly the dangerous kind."*

> 💬 **Expect a pair to suggest "just don't join to customer_addresses then."** Welcome it - it's a valid instinct here, but push further: *"True for THIS specific report. But real analysis constantly needs multi-table joins. The actual fix isn't avoiding joins - it's aggregating BEFORE joining when possible, or explicitly checking for duplication after. We'll practice the fix directly next."*

**Quick fix demo (2 min, folded into this block):** Show the corrected approach - aggregate `orders` by customer first, THEN join to `customer_addresses` only if address detail is genuinely needed for that specific question, never for a revenue total.

---

## BREAK (5 min)

---

## Concept Block 3: Comparing Groups Fairly (10 min)

### 💬 Instructor script

> *"New trap, unrelated to fan-out. Even a perfectly correct, non-duplicated SUM can still mislead you - if you're comparing groups of very different sizes."*

Project the extended loyalty-tier table from the pre-read:

| loyalty_tier | number_of_customers | total_revenue | revenue_per_customer |
|---|---|---|---|
| Gold | 5 | 5000 | 1000 |
| Silver | 2 | 3000 | 1500 |

> *"By total revenue, which tier looks stronger?"* (Gold.) *"Now look at revenue per customer."* (Silver, by 50%.) *"Gold's bigger total is just because it has more than double the customers - not because each Gold customer is more valuable. Which number would you actually put in front of a manager deciding where to invest in perks?"*

### 🔴 The trap / highest-value moment

> *"Any time you're ranking or comparing groups of different sizes - cities, tiers, branches - a raw SUM or COUNT flatters whichever group is simply BIGGER. The fix in SQL is almost always the same: pair your SUM with a COUNT of the group's size, in the same GROUP BY query, and divide. Write this down: total tells you scale. Rate tells you value."*

---

## Practical Block 3: Rate vs. Raw Total Challenge (10 min)

**Activity:** Pairs write a query computing `SUM(price)` and `COUNT(DISTINCT customer_id)` per city, then manually calculate revenue-per-customer for each, and identify whether the city with the highest total revenue is still the city with the highest revenue-per-customer.

**Answer key with reasoning:** Walk one pair's numbers live and confirm whether the ranking flips once divided by customer count - the specific numbers matter less than the habit of checking.

> 💬 **Expect a pair to use `COUNT(*)` instead of `COUNT(DISTINCT customer_id)`.** Welcome it. Say: *"COUNT(*) counts ORDER rows, not customers - remember Session 11? A customer with 3 orders would count as 3 there, quietly changing your 'per customer' math into something closer to 'per order.' Which one does the question actually need?"*

---

## Concept Block 4: Writing the Insight, Without Overreaching (8 min)

### 💬 Instructor script

> *"Last piece: turning a checked, fair number into a sentence you'd actually put in front of a manager."*

Write the three-part structure on the board: **Finding → Evidence → Implication.**

> *"Finding: Silver-tier customers generate more revenue per customer than Gold. Evidence: ₹1,500 vs ₹1,000 per customer, despite Gold having more than double the customers. Implication: worth understanding why Silver customers spend more individually before expanding Gold perks."*

### 🔴 The trap / highest-value moment

> *"Now the trap almost everyone falls into eventually: 'Silver customers spend more BECAUSE they're Silver tier.' Is that actually what the data proved?"*
> Let the room reason it out - no, the data shows association, not cause. *"Write this down, underline it: a joined, grouped SQL result can show you that two things move together. It essentially never proves WHY, on its own. 'Worth investigating' is honest. 'This is definitely because of X' is a claim your query never actually made."*

---

## Practical Block 4: Full Insight-Writing Challenge (9 min)

**Activity:** Individually, students take last session's "revenue by city" result and write a full Finding/Evidence/Implication insight, explicitly avoiding a causal claim. Cold-call 3–4 students to read theirs aloud.

**Answer key with reasoning:** For each read-aloud, ask the room: *"Does this claim anything the data can't actually prove?"* Correct live if a causal overreach slips in.

> 💬 **Expect at least one student to write a strong Finding and Evidence but a vague, non-actionable Implication** ("this is interesting"). Welcome it. Say: *"'Interesting' isn't an implication - what would you actually DO with this, or what would you check next? Push one level further."*

---

## Summary & Bridge

**Recap table:**

| Concept | The one thing to remember |
|---|---|
| Numbers vs. insight | A number needs a comparison, a flag, and an implication before it's an insight |
| Join fan-out | A one-to-many join duplicates rows and silently inflates SUM/COUNT - SQL won't warn you |
| Fair comparison | Raw totals flatter bigger groups - divide by group size to get a rate |
| Writing the insight | Finding + Evidence + Implication - association is not proof of cause |

**Close on the thesis line:**

> *"At the start of today, two different queries gave two different numbers for Ramesh's spending, and both ran without a single error. Now you know why, and you know how to catch it - check for fan-out, compare with rates not raw totals, and write what you find as an honest Finding, Evidence, and Implication, never a causal claim your data didn't actually prove. A joined query can run perfectly and still lie to you. Today, you learned to catch it before it reaches someone's inbox."*

**Bridge to next session:**

> *"So far, every question you've answered has needed just one query. Next session - Subqueries in Action - you learn to answer questions that genuinely need a query built entirely from the RESULT of another query - like 'which customers spent more than the average customer,' where you don't even know the average until you've calculated it first."*

---

## Q&A & Doubt Solving

**Q: Is fan-out always a bad thing?**
→ No - sometimes you genuinely want every combination (e.g., listing every order alongside every saved address for a delivery-options screen). Fan-out only becomes a *trap* when you aggregate (SUM/COUNT) afterward without accounting for the duplication it introduced.

**Q: How do I actually check for fan-out before trusting a SUM?**
→ A reliable habit: compare the row count of your joined result to the row count of your original table before the join. If the joined result has more rows than the original `orders` table, something duplicated - go find out what and why.

**Q: Is "revenue per customer" always the right rate to use?**
→ Not always - the right denominator depends on the question. "Revenue per order" answers a different question than "revenue per customer." Always ask what unit the comparison is actually supposed to be fair across.

**Q: Can I ever claim causation from SQL data alone?**
→ Rarely, and only with strong supporting evidence beyond a single query - a controlled experiment, a known mechanism, or corroborating data. As a habit in this course, treat SQL-derived patterns as findings worth investigating, not proven causes, unless you have a specific, strong reason to claim otherwise.

**Q: Does GROUP BY protect me from fan-out automatically?**
→ No - GROUP BY happens *after* the join, so if the join already duplicated rows, GROUP BY will faithfully sum up the duplicated rows too. GROUP BY groups whatever rows exist at that point in the query; it doesn't know or care whether they're genuine or duplicated.

---

## Instructor Notes

- **Words not yet earned:** Avoid subqueries, CTEs, and window functions - subqueries arrive next session specifically to solve problems like "compare each row to an overall average," which is a natural extension of today's fair-comparison theme. If a student asks how to compute "average per city" and compare individual customers against it, acknowledge that's exactly next session's tool.
- **The single biggest risk in this session** is students walking away thinking "joins are dangerous, avoid them" rather than "joins need a specific check before trusting an aggregate." Correct this framing explicitly at least once - the skill is verification, not avoidance.
- **Board management:** Keep the Opening's ₹120-vs-₹240 mystery visible (or referenced) throughout the whole session - it's the through-line every later block should loop back to by name.
- **Common confusions, numbered:**
  1. Believing a query that runs without errors must be producing a correct number.
  2. Comparing raw SUM/COUNT across groups of different sizes without checking group size first.
  3. Using COUNT(*) when COUNT(DISTINCT customer_id) was actually needed for a "per customer" rate.
  4. Writing an insight that claims causation ("because of") when the data only shows association.
- **Cross-references:** Subqueries and CTEs (next two sessions) are frequently the actual fix for fan-out - aggregating in a subquery *before* joining, rather than joining first and aggregating after. Tableau's data-blending warnings (Module 3) and pandas' `.merge()` duplicate-row surprises (Module 4) are this exact same trap in different tools.
- **Local/cultural context:** Keep Ramesh's two-address story as the running anchor for fan-out across the rest of the module - it's concrete, small, and easy to recall precisely because the numbers are simple (₹120 → ₹240).
