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

*The core flow fills all 90 minutes. Concept/Practical Block 5, on verifying row counts as a general-purpose fan-out detector, is in the Extension Blocks section - use only if ahead of pace.*

---

## Opening - "Ramesh Spent HOW Much?" (8 min)

Walk in and project a query live: join `orders` to `customer_addresses` (from the pre-read), then run `SELECT customer_id, SUM(price) AS total_spent FROM ... GROUP BY customer_id;` on top of it - showing Ramesh at ₹240.

**Verified query and output, run against `SQL Files/module2_phase2_sessions_6.1_to_6.2.db`:**

```sql
SELECT orders.customer_id, SUM(orders.price) AS naive_total
FROM orders
INNER JOIN customer_addresses ON orders.customer_id = customer_addresses.customer_id
WHERE orders.customer_id = 1
GROUP BY orders.customer_id;
```
```
customer_id  naive_total
-----------  -----------
1            240
```

> *"According to this query, Ramesh spent ₹240 with us. Let's pull up his actual order history."*

Show the real `orders` table - Ramesh has exactly **one** order, ₹120.

**Verified:**
```sql
SELECT * FROM orders WHERE customer_id = 1;
```
```
order_id  customer_id  item       quantity  price  order_date
--------  -----------  ---------  --------  -----  ----------
1         1            Veg Thali  2         120    2026-08-01
```

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

*(Verified again here for continuity: `SELECT customers.loyalty_tier, SUM(orders.price) AS total_revenue FROM customers INNER JOIN orders ON customers.customer_id = orders.customer_id GROUP BY customers.loyalty_tier ORDER BY total_revenue DESC;` → Silver 270, Gold 210 - unchanged from last session.)*

> *"'Gold revenue is 210, Silver is 270' - is that an insight, or just a fact?"*

Let the room debate. Land on: it's a fact. Then reveal the insight version: *"Silver-tier customers are currently generating more total revenue than Gold - our 'premium' tier - which is worth investigating before we invest further in Gold-specific perks."*

### 🔴 The trap / highest-value moment

> *"The difference between those two sentences is THREE things: a comparison, something surprising flagged, and a suggested next step. From today onward, no joined or grouped query result leaves this room without at least an attempt at those three things. A number is not done until someone has asked 'so what?'"*

---

## Practical Block 1: Fact vs. Insight Sorting Exercise (8 min)

**Activity:** Hand out 5 short statements (mix of bare facts and real insights, e.g., "Chennai had 1 order this week" vs. "Chennai is currently our lowest-activity city - worth checking if our delivery radius even covers it properly"). Pairs sort them into "fact only" vs. "insight."

**Full statement set (verified against the real data where a statement cites a specific number):**

1. *"Bengaluru has 2 orders."* → fact only. (Verified: `SELECT COUNT(*) FROM orders o JOIN customers c ON o.customer_id=c.customer_id WHERE c.city='Bengaluru';` = 2.)
2. *"Bengaluru is generating the most revenue of any city we operate in (₹240), nearly triple Chennai's ₹90 - worth understanding whether that's genuine demand or just where we've marketed hardest."* → insight (comparison + flag + implication).
3. *"Karthik signed up and has never placed an order."* → fact only.
4. *"Karthik represents a real churn-risk signal - a signed-up customer with zero purchases is worth a re-engagement nudge before we assume he's simply inactive."* → insight.
5. *"Gold tier's average order value is ₹105; Silver's is ₹135."* → fact only, until a comparison and implication are added.

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
  ON orders.customer_id = customer_addresses.customer_id
WHERE orders.customer_id = 1;
```

Run it live - Ramesh's order appears **twice**, once per saved address (Home, Office).

**Verified output:**
```
order_id  price  address_label
--------  -----  -------------
1         120    Home
1         120    Office
```

> *"His one real order just became two rows. If I SUM the price column now, without noticing, I get 240 - double his actual spend. This is called a fan-out: joining to a table where one side has MULTIPLE matches duplicates the rows on the other side."*

### 🔴 The trap / highest-value moment

> *"Here's the part that should genuinely worry you: this query has ZERO errors. It ran perfectly. SQL will never warn you that a join fanned out - it's not a bug, it's working exactly as designed. Catching this is entirely on you, the analyst. Before trusting any SUM or COUNT after a join, ask: could either side have more than one match on the other side? If yes, stop and check your row counts before you trust the total."*

---

## Practical Block 2: Catching the Fan-Out Live (12 min)

**Activity:** Pairs run the full `orders` + `customer_addresses` join (all customers, not just Ramesh) and identify: which customers get duplicated, and by how much does the naive `SUM(price)` overstate total revenue compared to the real `orders` table total?

**Full worked answer key, verified against the real database:**

```sql
SELECT orders.customer_id, orders.order_id, orders.price, customer_addresses.address_label
FROM orders
INNER JOIN customer_addresses ON orders.customer_id = customer_addresses.customer_id;
```
```
customer_id  order_id  price  address_label
-----------  --------  -----  -------------
1            1         120    Home
1            1         120    Office
2            2         150    Home
3            3         120    Home
4            4         90     Home
```

```sql
-- naive total per customer (inflated)
SELECT orders.customer_id, SUM(orders.price) AS naive_total
FROM orders
INNER JOIN customer_addresses ON orders.customer_id = customer_addresses.customer_id
GROUP BY orders.customer_id;
```
```
customer_id  naive_total
-----------  -----------
1            240
2            150
3            120
4            90
```

```sql
-- real total per customer (correct)
SELECT customer_id, SUM(price) AS real_total FROM orders GROUP BY customer_id;
```
```
customer_id  real_total
-----------  ----------
1            120
2            150
3            120
4            90
```

**Answer key with reasoning:** Only Ramesh (customer_id 1) has 2 addresses, so only his order duplicates; naive SUM across all customers totals 240+150+120+90 = 600, while the real total is 120+150+120+90 = 480 - inflated by exactly Ramesh's ₹120, once. Say aloud: *"Notice it's not even a big, obvious distortion - ₹120 out of 480 is a 25% overstatement of total revenue, and it could easily slip past a tired analyst at 6pm. Small, quiet errors like this are exactly the dangerous kind."*

**A second verification worth demonstrating: comparing raw row counts, before any aggregation, as an early-warning check:**
```sql
SELECT COUNT(*) FROM orders;
-- 4
SELECT COUNT(*) FROM orders INNER JOIN customer_addresses ON orders.customer_id = customer_addresses.customer_id;
-- 5
```
> *"4 orders went in. 5 rows came out of the join. That mismatch, on its own, before you've even calculated a single total, is your earliest warning sign that something duplicated. Make this comparison a habit, not an afterthought."*

> 💬 **Expect a pair to suggest "just don't join to customer_addresses then."** Welcome it - it's a valid instinct here, but push further: *"True for THIS specific report. But real analysis constantly needs multi-table joins. The actual fix isn't avoiding joins - it's aggregating BEFORE joining when possible, or explicitly checking for duplication after. We'll practice the fix directly next."*

**Quick fix demo (2 min, folded into this block):** Show the corrected approach - aggregate `orders` by customer first, THEN join to `customer_addresses` only if address detail is genuinely needed for that specific question, never for a revenue total.

```sql
SELECT customer_totals.customer_id, customer_totals.real_total, customer_addresses.address_label
FROM (SELECT customer_id, SUM(price) AS real_total FROM orders GROUP BY customer_id) AS customer_totals
INNER JOIN customer_addresses ON customer_totals.customer_id = customer_addresses.customer_id
WHERE customer_totals.customer_id = 1;
```
```
customer_id  real_total  address_label
-----------  ----------  -------------
1            120         Home
1            120         Office
```

> *"Notice: Ramesh's row STILL appears twice here, once per address - that part is unavoidable if you genuinely want both addresses listed. But his `real_total` now correctly reads 120 on both rows, not 240, because we summed BEFORE joining to the table that causes duplication. The address list fanning out is fine; the REVENUE NUMBER silently fanning out with it is what was actually dangerous."*

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

*(Instructor note: this specific 5-vs-2-customer table is an illustrative example from the pre-read, not this session's actual `customers` table, which has only 2 Gold and 2 Silver customers with matching orders - see Practical Block 3 for the real, verified version of this exact comparison against our own data.)*

### 🔴 The trap / highest-value moment

> *"Any time you're ranking or comparing groups of different sizes - cities, tiers, branches - a raw SUM or COUNT flatters whichever group is simply BIGGER. The fix in SQL is almost always the same: pair your SUM with a COUNT of the group's size, in the same GROUP BY query, and divide. Write this down: total tells you scale. Rate tells you value."*

---

## Practical Block 3: Rate vs. Raw Total Challenge (10 min)

**Activity:** Pairs write a query computing `SUM(price)` and `COUNT(DISTINCT customer_id)` per city, then manually calculate revenue-per-customer for each, and identify whether the city with the highest total revenue is still the city with the highest revenue-per-customer.

**Full worked answer key, verified against the real database:**

```sql
SELECT customers.city,
       COUNT(DISTINCT orders.customer_id) AS num_customers,
       SUM(orders.price) AS total_revenue
FROM customers
INNER JOIN orders ON customers.customer_id = orders.customer_id
GROUP BY customers.city;
```
```
city       num_customers  total_revenue
---------  -------------  -------------
Bengaluru  2              240
Chennai    1              90
Hyderabad  1              150
```

Manually calculated revenue-per-customer: Bengaluru = 240 ÷ 2 = **₹120**; Chennai = 90 ÷ 1 = **₹90**; Hyderabad = 150 ÷ 1 = **₹150**.

> *"Walk one pair's numbers live and confirm: by total revenue, Bengaluru wins clearly (₹240). But per customer, Hyderabad actually leads at ₹150 - Bengaluru's bigger total is partly just because it has 2 customers ordering instead of 1. The ranking genuinely flips depending which number you lead with."*

**A second, real worked example on loyalty tier - the exact comparison from Concept Block 3, but with our actual data instead of the illustrative pre-read numbers:**
```sql
SELECT customers.loyalty_tier,
       COUNT(DISTINCT customers.customer_id) AS num_customers,
       SUM(orders.price) AS total_revenue,
       ROUND(SUM(orders.price) * 1.0 / COUNT(DISTINCT customers.customer_id), 2) AS revenue_per_customer
FROM customers
INNER JOIN orders ON customers.customer_id = orders.customer_id
GROUP BY customers.loyalty_tier;
```
```
loyalty_tier  num_customers  total_revenue  revenue_per_customer
------------  -------------  -------------  ---------------------
Gold          2              210            105.0
Silver        2              270            135.0
```

> *"Here, Gold and Silver both have exactly 2 customers with orders - so the ranking doesn't actually flip in our real dataset. Silver leads on both total AND per-customer. That's worth saying honestly too: sometimes the fairer number confirms the raw total's story instead of overturning it. The habit of checking is what matters, not manufacturing a dramatic reversal every time."*

> 💬 **Expect a pair to use `COUNT(*)` instead of `COUNT(DISTINCT customer_id)`.** Welcome it. Verified: for this table, `COUNT(*)` and `COUNT(DISTINCT orders.customer_id)` happen to give identical results per group, purely because no customer here places more than one order. Say: *"They match today, by coincidence of this small dataset - remember Session 11? A customer with 3 orders would count as 3 with `COUNT(*)`, quietly changing your 'per customer' math into something closer to 'per order.' Which one does the question actually need? Always reach for `COUNT(DISTINCT customer_id)` for a genuine 'per customer' rate, even when the numbers happen to coincide today."*

---

## Concept Block 4: Writing the Insight, Without Overreaching (8 min)

### 💬 Instructor script

> *"Last piece: turning a checked, fair number into a sentence you'd actually put in front of a manager."*

Write the three-part structure on the board: **Finding → Evidence → Implication.**

> *"Finding: Silver-tier customers generate more revenue per customer than Gold. Evidence: ₹135 vs ₹105 per customer, despite both tiers having the same number of customers with orders. Implication: worth understanding why Silver customers spend more individually before expanding Gold perks."*

*(Instructor note: the exact evidence figures above - ₹135 vs ₹105 - are this session's own verified per-customer numbers from Practical Block 3, not the illustrative ₹1,500-vs-₹1,000 figures from the pre-read's Concept Block 3 example. Use whichever pair of numbers the class actually derived live.)*

### 🔴 The trap / highest-value moment

> *"Now the trap almost everyone falls into eventually: 'Silver customers spend more BECAUSE they're Silver tier.' Is that actually what the data proved?"*
> Let the room reason it out - no, the data shows association, not cause. *"Write this down, underline it: a joined, grouped SQL result can show you that two things move together. It essentially never proves WHY, on its own. 'Worth investigating' is honest. 'This is definitely because of X' is a claim your query never actually made."*

---

## Practical Block 4: Full Insight-Writing Challenge (9 min)

**Activity:** Individually, students take last session's "revenue by city" result and write a full Finding/Evidence/Implication insight, explicitly avoiding a causal claim. Cold-call 3–4 students to read theirs aloud.

**Model answer, using this session's own verified numbers, to reveal after cold-calling:**

> *"Finding: Hyderabad generates the highest revenue per customer of the three cities we operate in. Evidence: ₹150 per customer in Hyderabad, versus ₹120 in Bengaluru and ₹90 in Chennai - even though Bengaluru's total revenue (₹240) is the highest of the three in raw terms, because it has more ordering customers. Implication: worth investigating what's different about Hyderabad's single customer's ordering pattern before assuming Bengaluru is automatically our strongest market."*

**Answer key with reasoning:** For each read-aloud, ask the room: *"Does this claim anything the data can't actually prove?"* Correct live if a causal overreach slips in.

> 💬 **Expect at least one student to write a strong Finding and Evidence but a vague, non-actionable Implication** ("this is interesting"). Welcome it. Say: *"'Interesting' isn't an implication - what would you actually DO with this, or what would you check next? Push one level further."*

---

## Extension Blocks (Optional — Use if Running Ahead)

*Not part of the 90-minute core flow. Use only if Practical Block 4 finishes early - see Timing Contingencies.*

### Concept Block 5 (Extension): The Row-Count Check as a General-Purpose Habit

#### 💬 Instructor script

> *"Practical Block 2 showed one specific check - comparing `orders`' row count to the joined result's row count. Let's generalize that into a habit you can run before trusting ANY joined aggregate, on any two tables."*

Write the three-step check on the board:

```
1. COUNT(*) on your anchor table, before any join.
2. COUNT(*) on the joined result, after the join.
3. If step 2 > step 1, at least one row duplicated somewhere - find out where before trusting a SUM/COUNT.
```

Demonstrate it on a join students haven't specifically checked yet - `customers` joined to `orders`:

```sql
SELECT COUNT(*) FROM customers;              -- 5
SELECT COUNT(*) FROM customers
  INNER JOIN orders ON customers.customer_id = orders.customer_id;  -- 4
```

**Verified:** 5 customers, but only 4 rows in the INNER JOIN result.

> *"This time the joined count is SMALLER than the anchor table, not bigger - that's a different signal entirely. It means INNER JOIN silently dropped a row (Karthik, with zero orders) rather than duplicating one. Smaller means 'something got excluded.' Bigger means 'something got duplicated.' Both are worth investigating; neither is inherently wrong, but neither should go unnoticed either."*

#### 🔴 The trap / highest-value moment

> *"This check has a blind spot worth naming honestly: if a join BOTH drops some rows AND duplicates others in the same query, the final count could coincidentally land back at the original number, and this simple check would miss it entirely. The row-count check is a fast, valuable first pass - not a guarantee. For anything going into a real business decision, actually trace a specific row (like we did with Ramesh) rather than trusting the count alone."*

### Practical Block 5 (Extension): Running the Row-Count Check on a New Join

**Activity:** Pairs run the row-count check (anchor table count vs. joined count) on `customers` LEFT JOIN `orders`, and explain what the result means.

**Verified answer key:**
```sql
SELECT COUNT(*) FROM customers;  -- 5
SELECT COUNT(*) FROM customers LEFT JOIN orders ON customers.customer_id = orders.customer_id;  -- 5
```
Both counts are 5 - no duplication, no silent drops. *"This matches exactly what we'd expect: LEFT JOIN preserves every customer row, Karthik included, and since no customer here has more than one order, nothing duplicates either. A matching count is a good sign, though - per the trap above - never a complete guarantee on more complex real data."*

> 💬 **Expect a pair to ask if this check should just become a habit for every single joined query, even simple ones.** Welcome it - say: *"For a quick exploratory query, it can feel like overkill. For anything that's about to be reported to someone else as a real number, yes - it costs you ten seconds and it's the single cheapest insurance policy in this entire module."*

---

## Common Errors

| Error | What causes it | Fix |
|---|---|---|
| Trusting a SUM/COUNT immediately after any join, without checking | Assuming "no error" means "correct" | Compare the joined result's row count against the anchor table's row count before trusting any aggregate on top |
| Reporting a bare fact as if it were a finished insight | Skipping the comparison, flag, and implication that turn a number into a decision-ready sentence | Apply the three-part test: does this statement compare, flag something notable, and suggest a next step? |
| Comparing raw SUM/COUNT across groups of very different sizes | Not checking group size before ranking groups against each other | Always compute a rate (SUM ÷ COUNT of group size) alongside the raw total when comparing groups |
| Using `COUNT(*)` when a genuine "per customer" or "per entity" rate was needed | Not distinguishing "count of rows" from "count of distinct real-world entities" | Use `COUNT(DISTINCT <key column>)` whenever the denominator should represent unique entities, not rows |
| Writing an insight that claims causation ("because of X") | Treating an observed association as if it were proven cause | State association plainly ("worth investigating") rather than asserting a mechanism the query never tested |
| Assuming GROUP BY somehow "protects" a query from fan-out | Not realizing GROUP BY runs AFTER the join, on whatever rows (duplicated or not) already exist | Check for fan-out before grouping, not after - GROUP BY faithfully sums duplicated rows too |
| Aggregating after a join to a table with a one-to-many relationship, instead of aggregating first | Joining first out of habit, without checking whether either side can have multiple matches | Aggregate the "one" side first in a subquery, then join to the potentially-duplicating table only if row-level detail is genuinely needed |
| Treating a matching row-count check as a complete guarantee of correctness | Not accounting for a join that both drops and duplicates rows, landing back at a coincidentally-matching count | Trace at least one specific row's real value (like Ramesh's ₹120) through the query when the result is going into an actual business decision |

---

## Materials Checklist

Before class, have ready:

- `SQL Files/module2_phase2_sessions_6.1_to_6.2.db` loaded in the shared SQL sandbox - same database as last session (`customers`, `orders`, `customer_addresses`).
- A projector for live queries - the Opening's ₹120-vs-₹240 reveal, the Practical Block 2 row-count comparison, and the Concept Block 3 rate-vs-total flip are the three moments that land hardest live, not pre-described.
- Last session's "revenue by loyalty tier" result (Silver 270, Gold 210) ready to re-project for Concept Block 1 and Practical Block 4.
- The pre-read's illustrative 5-Gold/2-Silver loyalty table for Concept Block 3's initial teaching example, clearly distinguished from this session's own real (2-and-2) loyalty tier numbers used in Practical Block 3.
- 5 printed or slide fact/insight statements for Practical Block 1's sorting exercise.

---

## Timing Contingencies

**If running long:**
- In Practical Block 1, hand out only 3 of the 5 fact/insight statements rather than all 5.
- Compress Practical Block 3 to the city-based rate comparison only, and present the loyalty-tier rate comparison as a quick verbal callback instead of a second full worked query.
- Never cut the Concept Block 2 fan-out demonstration or the Practical Block 2 row-count check - together they are this session's central, non-negotiable skill, and the entire second half (fair comparison, insight-writing) assumes students already trust that a query can run clean and still be wrong.

**If running short:**
- Run the Extension Blocks (the general-purpose row-count check habit) in full.
- If only a few minutes remain, demonstrate the single `customers` vs. `customers INNER JOIN orders` count comparison from Concept Block 5 live, without the paired Practical Block 5.
- Alternatively, revisit the Opening's Ramesh mystery and ask pairs to write their own Finding/Evidence/Implication insight specifically about the fan-out bug itself (e.g., "our reporting query overstates revenue by 25% due to an address join") - a strong combined reinforcement of both this session's major skills at once.

---

## End-of-Session Quiz

1. **What are the three ingredients that turn a bare fact into a real insight?**
   → A comparison, something notable flagged, and a suggested implication or next step.

2. **Why does joining `orders` to `customer_addresses` double Ramesh's row in the result?**
   → Ramesh has two saved addresses, so his one order matches two rows in `customer_addresses` - a one-to-many relationship causing a join fan-out.

3. **What's the fastest early-warning check for a possible fan-out, before calculating any aggregate?**
   → Compare the row count of the joined result to the row count of the original (anchor) table - if the joined count is higher, something likely duplicated.

4. **Bengaluru has the highest total revenue (₹240) but not the highest revenue per customer. What does that tell you?**
   → Bengaluru's higher total is partly just a function of having more ordering customers (2, versus 1 each for Hyderabad and Chennai) - not necessarily that each Bengaluru customer is individually more valuable.

5. **What's wrong with the sentence "Silver customers spend more because they're Silver tier"?**
   → It claims causation from data that only shows association - the query never tested WHY Silver customers spend more, only THAT they do.

6. **(If Extension Block covered) If a joined result's row count is SMALLER than the anchor table's, what does that suggest, as opposed to a LARGER count?**
   → A smaller count suggests rows were dropped (e.g. by an INNER JOIN excluding unmatched rows), while a larger count suggests rows were duplicated (fan-out) - both are worth investigating, but they point to different causes.

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

**Q: In Practical Block 3, why did the loyalty-tier ranking NOT flip between total revenue and revenue-per-customer, while the city ranking DID flip?**
→ Pure coincidence of this dataset's exact numbers - Gold and Silver happen to have equal customer counts (2 each), so dividing by group size doesn't change which tier leads. Cities have unequal customer counts (2 for Bengaluru, 1 each for the others), so the rate calculation changes the ranking there. Always check both; don't assume either outcome in advance.

**Q: Is there a way to detect fan-out automatically, without manually comparing row counts every time?**
→ Not built into standard SQL directly - the row-count check from the Extension Block is the standard manual habit. Some analytics tools and dbt-style data testing frameworks can automate a version of this check in production pipelines, but that's beyond this course's current scope.

---

## Instructor Notes

- **Words not yet earned:** Avoid subqueries, CTEs, and window functions - subqueries arrive next session specifically to solve problems like "compare each row to an overall average," which is a natural extension of today's fair-comparison theme. If a student asks how to compute "average per city" and compare individual customers against it, acknowledge that's exactly next session's tool.
- **The single biggest risk in this session** is students walking away thinking "joins are dangerous, avoid them" rather than "joins need a specific check before trusting an aggregate." Correct this framing explicitly at least once - the skill is verification, not avoidance.
- **Board management:** Keep the Opening's ₹120-vs-₹240 mystery visible (or referenced) throughout the whole session - it's the through-line every later block should loop back to by name.
- **Common confusions, numbered:**
  1. Believing a query that runs without errors must be producing a correct number.
  2. Comparing raw SUM/COUNT across groups of different sizes without checking group size first.
  3. Using COUNT(*) when COUNT(DISTINCT customer_id) was actually needed for a "per customer" rate - especially risky here since they coincidentally match on this session's small dataset.
  4. Writing an insight that claims causation ("because of") when the data only shows association.
- **Cross-references:** Subqueries and CTEs (next two sessions) are frequently the actual fix for fan-out - aggregating in a subquery *before* joining, rather than joining first and aggregating after (the Practical Block 2 "quick fix demo" is a direct, hand-written preview of exactly this). Tableau's data-blending warnings (Module 3) and pandas' `.merge()` duplicate-row surprises (Module 4) are this exact same trap in different tools.
- **Local/cultural context:** Keep Ramesh's two-address story as the running anchor for fan-out across the rest of the module - it's concrete, small, and easy to recall precisely because the numbers are simple (₹120 → ₹240).
