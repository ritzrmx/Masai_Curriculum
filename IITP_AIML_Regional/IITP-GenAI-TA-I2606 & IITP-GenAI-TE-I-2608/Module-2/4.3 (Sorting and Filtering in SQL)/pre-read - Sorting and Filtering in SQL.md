# SQL for Data Analysis: Sorting and Filtering in SQL
> **Pre-Read - Academic Session 10** | Module 2: SQL for Data Analysis

---

## Mental Map
> 📄 Also provided as a printable PDF in this folder: **mental-map: Sorting and Filtering in SQL.pdf**

```mermaid
%%{init: {'theme': 'default', 'themeVariables': { 'fontSize': '12px', 'fontFamily': 'sans-serif' }, 'flowchart': {'htmlLabels': true, 'useMaxWidth': false, 'nodeSpacing': 30, 'rankSpacing': 45, 'padding': 10}}}%%
flowchart TB

START["<b>Course Start</b>"]

subgraph foundation[" WHERE WE ARE "]
direction TB
    CURMOD["<b>CURRENT MODULE</b><br/><i>Module 2: SQL for Data Analysis</i><br/>&nbsp;<br/><b>Covered so far:</b> Understanding Data &amp; Averages - Analytics Workflow &amp; KPIs - GenAI for Analytics - Clean Up the Data - Make Data Ready for Analysis - Formulas for Analysis - Pivot Tables &amp; Quick Insights - Spread, Variability &amp; Outliers - SQL Query Basics<br/>This is Session 10 of 41"]
    CURSES["<b>CURRENT SESSION</b><br/><b>Sorting and Filtering in SQL</b><br/>&nbsp;<br/><i>The shift:</i> from filtering to the right rows <i>to</i> <b>ranking them and pulling only the top or bottom results</b><br/>&nbsp;<br/>ORDER BY (ASC/DESC) - Multi-column sorting<br/>LIMIT - WHERE + ORDER BY + LIMIT together"]
end

subgraph outcome[" OUTCOME OF THIS SESSION "]
direction TB
    OUT["<b>By the end, you can...</b><br/>&nbsp;<br/>Sort query results ascending or descending, sort by more than<br/>one column, and pull only the top or bottom N rows to answer<br/>'who's the best/worst' business questions in one query"]
end

subgraph value[" WHY IT MATTERS "]
direction LR
    CVAL["<b>Course Value</b><br/>ORDER BY and LIMIT feed directly into ranking and 'top customer'<br/>questions once GROUP BY and aggregation arrive next"]
    RVAL["<b>Real-Life Value</b><br/>'Show me our top 5 customers' or 'find our slowest-selling item'<br/>are everyday manager requests - this is how you answer them instantly"]
end

subgraph future[" WHAT COMES NEXT "]
direction TB
    U0["<b>Next Session</b><br/>Aggregation Essentials<br/><i>SUM, COUNT, AVG - turning rows into totals</i>"]
    U1["<b>Later in Module 2</b><br/>Grouping for KPIs (GROUP BY) - Joining Tables Together - Insights from Combined Data"]
    U2["<b>Upcoming Modules</b><br/>Module 3: Tableau Dashboards + Storytelling - Module 4: GenAI Workflows + Basic Python<br/><i>Tableau's sort-and-filter panel and pandas' .sort_values()/.head() mirror exactly what you learn today</i>"]
end

START ==>|" begin "| CURMOD
CURMOD ==>|" progress "| CURSES
CURSES ==>|" you get "| OUT
OUT ==>|" course "| CVAL
OUT ==>|" real life "| RVAL
CURSES ==>|" next up "| U0
U0 -.->|" then "| U1
U1 -.->|" ahead "| U2

classDef startBox fill:#F7FAFC,stroke:#4A5568,stroke-width:2px,color:#1A202C
classDef curModBox fill:#FFF8E6,stroke:#B7791F,stroke-width:2px,color:#1A202C
classDef curSessBox fill:#E6FFFA,stroke:#0D9488,stroke-width:3px,color:#1A202C
classDef outBox fill:#FEF2F2,stroke:#DC2626,stroke-width:3px,color:#1A202C
classDef valueBox fill:#F3E8FF,stroke:#7C3AED,stroke-width:2px,color:#1A202C
classDef futureBox fill:#ECFDF5,stroke:#047857,stroke-width:2px,color:#1A202C

class START startBox
class CURMOD curModBox
class CURSES curSessBox
class OUT outBox
class CVAL,RVAL valueBox
class U0,U1,U2 futureBox
```

---

## What You'll Learn

In this pre-read, you'll discover:
- How to sort query results with `ORDER BY`, ascending or descending
- How to sort by more than one column, in a specific priority order
- How to pull only the top or bottom N rows with `LIMIT`
- How to combine `WHERE`, `ORDER BY`, and `LIMIT` in one query to answer real ranking questions

---

## A. ORDER BY - sorting your results

**💡 Analogy:** Imagine handing someone the `orders` table on loose index cards and asking them to arrange the cards from cheapest order to most expensive. `ORDER BY` is you telling the database to do exactly that arranging, instantly, on any column you choose.

**`ORDER BY` sorts the rows returned by a query, based on one or more columns, in ascending or descending order.**

```sql
SELECT customer_name, price
FROM orders
ORDER BY price ASC;
```

**Worked example:** Using this session's running `orders` table:

| customer_name | price |
|---|---|
| Priya | 90 |
| Ramesh | 120 |
| Arjun | 120 |
| Fatima | 150 |

`ASC` (ascending) means low to high - and it's the default, so `ORDER BY price` alone sorts the same way. To reverse it:

```sql
SELECT customer_name, price
FROM orders
ORDER BY price DESC;
```

**⚠️ Common trap:** Forgetting that `ASC` is the default and assuming an unlabeled `ORDER BY` sorts high to low. It doesn't - `ORDER BY price` with nothing after it always means ascending, smallest first. If you want largest first, you must write `DESC` explicitly.

---

## B. Sorting by Multiple Columns - setting a priority order

**💡 Analogy:** A restaurant seats reservations first by table size, and *within* each table size, by earliest booking time. That's sorting by two columns - the second column only matters when the first column ties.

**Sorting by multiple columns lets you set a priority: the first column sorts everything, and the second column breaks ties within groups that share the same first-column value.**

```sql
SELECT customer_name, city, price
FROM orders
ORDER BY city ASC, price DESC;
```

This sorts alphabetically by city first, and *within* each city, by price from highest to lowest.

**Worked example:**

| customer_name | city | price |
|---|---|---|
| Arjun | Bengaluru | 120 |
| Ramesh | Bengaluru | 120 |
| Priya | Chennai | 90 |
| Fatima | Hyderabad | 150 |

**⚠️ Common trap:** Assuming the second column re-sorts the *entire* result. It doesn't - it only breaks ties *within* rows that already share the same value in the first sort column. If every city were different, the second column (`price`) would never even come into play.

---

## C. LIMIT - pulling only the top or bottom rows

**💡 Analogy:** A cricket scoreboard doesn't show every player who's ever batted - it shows the top run-scorers of the season. `LIMIT` is how you tell SQL "just show me the top few," instead of every row.

**`LIMIT` restricts the number of rows returned by a query - almost always used together with `ORDER BY` to get a meaningful "top N" or "bottom N."**

```sql
SELECT customer_name, price
FROM orders
ORDER BY price DESC
LIMIT 3;
```

This returns only the 3 highest-priced orders.

**⚠️ Common trap:** Using `LIMIT` without `ORDER BY`. `LIMIT 3` on its own just returns *any* 3 rows the database happens to return first - there's no guarantee they're the highest, lowest, or anything meaningful. `LIMIT` only becomes a "top N" tool when it's paired with `ORDER BY` to define what "top" even means.

```mermaid
flowchart TB
    A[Raw table, any order] --> B[Painful: LIMIT alone - 3 random-ish rows]
    A --> C[Better: ORDER BY + LIMIT - 3 meaningful rows]
    C --> D[A real 'top 3' answer]
```

---

## D. Combining WHERE, ORDER BY, and LIMIT - answering real ranking questions

**💡 Analogy:** A manager rarely asks for a sorted list of *everything*. They ask for a sorted list of *something specific* - "our top 3 Bengaluru orders by price," not "every order ever, sorted." That's WHERE narrowing the field, then ORDER BY ranking what's left, then LIMIT trimming to the headline number.

**The clauses combine in a fixed order: `SELECT ... FROM ... WHERE ... ORDER BY ... LIMIT ...`.** WHERE always filters rows *before* they're sorted; LIMIT always trims *after* sorting.

**Worked example:**
```sql
SELECT customer_name, price
FROM orders
WHERE city = 'Bengaluru'
ORDER BY price DESC
LIMIT 3;
```

Read left to right, in plain English: *"Start with the orders table. Keep only Bengaluru orders. Sort what's left from highest price to lowest. Show me the top 3."*

**⚠️ Common trap:** Writing the clauses out of order (e.g., `ORDER BY` before `WHERE`). SQL requires this exact sequence - `SELECT`, `FROM`, `WHERE`, `ORDER BY`, `LIMIT` - and will error if it's scrambled. When stuck, say the query out loud in plain English first, then translate line by line in that order.

---

## Quick Reference - Choosing the Right Clause

| Your Situation | Use This | Because |
|---|---|---|
| You want results sorted low to high | `ORDER BY column ASC` (or just `ORDER BY column`) | ASC is the default |
| You want results sorted high to low | `ORDER BY column DESC` | Must be stated explicitly |
| You want ties broken by a second factor | `ORDER BY col1, col2` | Second column only matters when the first ties |
| You want only the top or bottom few rows | `ORDER BY ... LIMIT n` | LIMIT alone has no defined "top" without a sort |
| You want a ranked answer to a specific business question | `WHERE ... ORDER BY ... LIMIT` together | Filters first, ranks what's left, trims to the headline number |

---

## Practice Exercises

Using the `orders` table from Session 9 (SQL Query Basics):

**1. Pattern Recognition:** Write a query that sorts all orders by `price`, highest first. Which order appears at the very top?

**2. Concept Detective:** Write a query that sorts orders by `city` (A–Z), and within each city, by `quantity` (highest first). Explain in one sentence what the second sort column is actually doing.

**3. Real-Life Application:** List 3 real workplace questions ("who are our top...", "what's our slowest...") that would each require an `ORDER BY ... LIMIT` combination to answer.

**4. Spot the Error:** A classmate writes `SELECT customer_name FROM orders LIMIT 2;` intending to find the 2 cheapest orders. What's missing, and why won't this reliably return the cheapest?

**5. Planning Ahead:** Write a single query that returns the top 2 highest-priced orders from Hyderabad only. Say the query out loud in plain English before writing the SQL.

---

> ✅ **You're done!** You can now rank query results and pull exactly the top or bottom rows a business question is really asking for - not just filter to the right rows, but order and trim them into a headline answer.
>
> Next up: **Aggregation Essentials** - where you learn `SUM`, `COUNT`, and `AVG` to turn many rows into a single meaningful total.
