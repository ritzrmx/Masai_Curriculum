# Lecture Script: Foundations of Data — SQL with MySQL Workbench
> **Instructor Reference** — Module 1: Foundations of Data | Academic Session 15 | Duration: 2 Hours | Instructor: [Industry Mentor / Name Placeholder]

---

## Session Overview
**Goal:** By the end, students can write SQL queries to filter, sort, and group data in MySQL Workbench, join two or more tables using INNER, LEFT, and RIGHT joins, and choose the correct join type for a given scenario.

**Student profile at this point:** Just completed the EDA & Business Thinking session and is fluent in the equivalent Pandas operations (filtering, groupby, merge) from Sessions 5.1–5.2. Likely wrong assumption: that SQL is a completely new, unrelated skill rather than the same logic in different syntax. Boredom risk is low if the Pandas parallels are made explicit throughout; frustration risk is moderate around the WHERE-vs-HAVING distinction and JOIN syntax.

**Key outcome:** Students should leave able to translate a Pandas operation they already know into its SQL equivalent, and vice versa — recognizing this as the same thinking in a new tool, not new thinking entirely.

> 🎯 **The one sentence this session must land:** *Every SQL query you write today has a Pandas equivalent you already know — WHERE is boolean indexing, GROUP BY is groupby, JOIN is merge — you're learning new syntax for logic you already have.*

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| Opening — "Same Question, New Language" | 8 min | 8 min |
| Concept + Practical Block 1: MySQL Workbench Setup & SELECT/WHERE | 22 min | 30 min |
| Concept + Practical Block 2: ORDER BY, LIMIT & DISTINCT | 18 min | 48 min |
| ☕ BREAK | 5 min | 53 min |
| Concept + Practical Block 3: GROUP BY & HAVING | 25 min | 78 min |
| Concept + Practical Block 4: JOINs & Aliases | 27 min | 105 min |
| Summary & Bridge | 5 min | 110 min |
| Q&A & Doubt Solving | 10 min | 120 min |

---

## Opening — "Same Question, New Language" (8 min)

Write on the board, side by side:
```python
df[(df["amount"] > 500) & (df["city"] == "Hyderabad")]
```
```sql
SELECT * FROM orders WHERE amount > 500 AND city = 'Hyderabad';
```

> "These two lines ask the EXACT same question of the EXACT same data. Different syntax, identical logic. Today isn't about learning a new way of thinking — it's about learning a new way of WRITING the thinking you already have."

> "Why does this matter? Because most real company data doesn't live in a CSV you download — it lives in a database, and SQL is how you ask that database for what you need, directly, often faster than pulling it into Pandas first."

Pivot line: "Let's set up MySQL Workbench and write our first real query."

---

## Concept + Practical Block 1: MySQL Workbench Setup & SELECT/WHERE (22 min)

### "Asking the librarian exactly what you want"
> "You don't browse an entire library shelf by shelf. You tell the librarian exactly what you want — 'books by this author, after 2015' — and they retrieve it. SELECT and WHERE work the same way."

Walk through MySQL Workbench setup live: connecting to a local server, opening a SQL editor tab, and running a first query against a sample database.

**Hands-on, built live:**
```sql
SELECT * FROM orders;
SELECT item, amount FROM orders;
SELECT * FROM orders WHERE amount > 500;
SELECT * FROM orders WHERE amount > 500 AND city = 'Hyderabad';
```

**Answer key / reasoning to say aloud:** After each query, pause and ask: "What's the Pandas equivalent of this line?" Build the parallel explicitly on the board each time, reinforcing the opening hook's thesis.

### 🔴 The trap / highest-value moment
Write on the board: **"SQL is strict about exact table and column names, and every statement needs a semicolon. Unlike Python, it won't guess what you meant."**

💬 **Expect an argument about:** "Why does SQL feel so much stricter than Python?" Welcome it. Say: *"Databases often handle massive, business-critical data — strictness here is a feature, not a limitation. It forces precision exactly where mistakes would be most costly."*

---

## Concept + Practical Block 2: ORDER BY, LIMIT & DISTINCT (18 min)

### "Sorted results, top 5 only, no repeats"
> "Ask the librarian for results sorted by date, only the top 5, or a list of unique authors with no repeats — that's ORDER BY, LIMIT, and DISTINCT."

**Hands-on:**
```sql
SELECT item, amount FROM orders ORDER BY amount DESC LIMIT 5;
SELECT DISTINCT city FROM orders;
```

Ask the room: "What's the Pandas equivalent of the first query?" — build it together: `df.sort_values("amount", ascending=False).head()`.

### 🔴 The trap / highest-value moment
Write on the board: **"SQL sorts FIRST, then limits — even though LIMIT is written last in the query. The order you write clauses isn't the order they execute."**

💬 **Expect an argument about:** "If LIMIT is written last, why does it matter that ORDER BY runs first logically?" Welcome it. Say: *"Because if you reversed the logic — limited first, then sorted — you'd get the wrong 5 rows entirely. SQL guarantees ORDER BY happens before LIMIT is applied, regardless of how they're visually positioned in your query."*

---

## ☕ BREAK (5 min)

---

## Concept + Practical Block 3: GROUP BY & HAVING (25 min)

### "Sorting receipts into piles, then filtering the piles themselves"
> "Recall groupby from Session 5.2 — sorting receipts into piles by category. GROUP BY is the exact same idea. HAVING then filters the PILES themselves — 'only show me categories with over ₹10,000 total' — which is different from filtering individual receipts."

**Hands-on:**
```sql
SELECT city, SUM(amount) AS total_sales
FROM orders
GROUP BY city;

SELECT city, SUM(amount) AS total_sales
FROM orders
GROUP BY city
HAVING total_sales > 10000;
```

Then deliberately trigger the trap:
```sql
SELECT city, SUM(amount) FROM orders WHERE SUM(amount) > 10000 GROUP BY city;
```

> "This errors. Why?"

**Answer key / reasoning to say aloud:** `WHERE` filters individual ROWS before any grouping happens — at that point, `SUM(amount)` doesn't exist yet, because no summing has occurred. `HAVING` filters the GROUPS after aggregation, which is the only place `SUM(amount) > 10000` makes sense.

### 🔴 The trap / highest-value moment
Write on the board: **"WHERE filters rows BEFORE grouping. HAVING filters groups AFTER aggregation. You cannot use an aggregate function like SUM() inside WHERE."**

💬 **Expect an argument about:** "Why does SQL even separate these into two different keywords — couldn't it just figure out which one I mean?" Welcome it. Say: *"Because the ORDER of operations genuinely matters here — filtering before grouping and filtering after grouping are fundamentally different operations, and having two distinct keywords forces you to be explicit about which one you actually need."*

---

## Concept + Practical Block 4: JOINs & Aliases (27 min)

### "Matching the student roster to their exam results"
> "Recall merge() from Session 5.2 — matching a student roster to exam results using student ID. SQL JOINs do the exact same thing, directly inside the database."

**Hands-on, building all three join types live:**
```sql
SELECT s.name, e.marks
FROM students AS s
INNER JOIN exam_results AS e ON s.student_id = e.student_id;

SELECT s.name, e.marks
FROM students AS s
LEFT JOIN exam_results AS e ON s.student_id = e.student_id;
```

Ask before running: "A student hasn't taken the exam yet. What happens to them in each version?"

**Answer key / reasoning to say aloud:** In the `INNER JOIN`, that student disappears entirely from the results. In the `LEFT JOIN`, they remain, with `marks` showing as `NULL` — this is the exact same behavior as Pandas' `merge()` from Session 5.2, just in SQL syntax.

Point out the aliases explicitly: "`s` and `e` are just nicknames for the table names — makes the query far more readable, especially once you're joining three or four tables."

### 🔴 The trap / highest-value moment
Write on the board: **"Defaulting to INNER JOIN without thinking silently drops unmatched rows — the exact same trap as Pandas' default merge behavior."**

💬 **Expect an argument about:** "Since I already learned this exact trap with merge(), why repeat it here?" Welcome it. Say: *"Because the SAME mistake shows up in EVERY tool that does joins — SQL, Pandas, Excel's VLOOKUP-based joins, all of it. Seeing it twice, in two different syntaxes, is exactly what makes the underlying principle stick permanently rather than feeling like a one-off Pandas quirk."*

---

## Summary & Bridge (5 min)

| Concept | The one thing to remember |
|---|---|
| SELECT & WHERE | The SQL equivalent of Pandas boolean indexing — choose columns, filter rows |
| ORDER BY, LIMIT & DISTINCT | Sorts happen before limits are applied, regardless of clause order written |
| GROUP BY & HAVING | WHERE filters rows before grouping; HAVING filters groups after aggregation |
| JOINs & aliases | INNER/LEFT/RIGHT — choose deliberately, since defaults silently drop unmatched rows |

Close on the thesis: *"Every SQL query you write today has a Pandas equivalent you already know — WHERE is boolean indexing, GROUP BY is groupby, JOIN is merge — you're learning new syntax for logic you already have."*

Bridge: "Not every team uses Python or SQL day to day — many work primarily in spreadsheets. Next session, the final session of Module 1, you'll answer these same kinds of questions using VLOOKUP, XLOOKUP, and pivot tables in **Data Analysis with Spreadsheets**."

---

## Q&A & Doubt Solving (10 min)

**Q: Can I combine GROUP BY, HAVING, ORDER BY, and LIMIT all in one query?**
→ Yes — SQL clauses combine in a fixed logical order (FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT), and you can use several together to answer precise, multi-step business questions in a single query.

**Q: Is RIGHT JOIN commonly used, or is it mostly redundant with LEFT JOIN?**
→ It's less commonly used in practice — most SQL developers achieve the same result by simply swapping the table order and using LEFT JOIN instead, though RIGHT JOIN remains valid and sometimes clearer for readability depending on context.

**Q: What happens if two tables have a column with the same name that I'm not joining on?**
→ You'd need to explicitly specify which table's version you mean using the table name or alias (e.g., `s.name` vs `e.name`), since referencing the column name alone would be ambiguous.

**Q: Do aliases change the actual data, or are they just for display?**
→ Purely for readability and reference within the query — they don't modify the underlying table or column names in the database at all.

**Q: Can I filter on multiple conditions in a JOIN's ON clause, not just one?**
→ Yes — `ON s.student_id = e.student_id AND s.year = e.year` is valid, useful when a single column isn't enough to uniquely match rows between tables.

---

## Instructor Notes
- **Words not yet earned — avoid using without defining:** "subqueries," "window functions," "indexes," "primary/foreign key constraints" (beyond the basic idea of a shared ID column). These are more advanced SQL topics for a later, dedicated SQL-focused module.
- **Biggest risk this session:** WHERE-vs-HAVING confusion in Block 3 is the SQL equivalent of the `and`/`&` trap from Session 5.1 — let students hit the error themselves before revealing the fix, exactly as in that earlier session, so the pattern of "predict, fail, understand why" repeats consistently across the module.
- **Board management:** Keep the Pandas-to-SQL side-by-side comparison from the opening hook visible or easily revisited throughout the entire session — it's the organizing thread that makes every new SQL clause feel familiar rather than foreign.
- **Common confusions, numbered:**
  1. Forgetting semicolons or misspelling table/column names, expecting SQL to "guess" intent the way informal Python sometimes seems to.
  2. Using WHERE with an aggregate function instead of HAVING.
  3. Defaulting to INNER JOIN without considering whether unmatched rows matter for the question being asked.
- **Cross-references to later sessions:** Today's GROUP BY/HAVING is the direct SQL equivalent of Session 5.2's groupby/agg; JOINs are the direct equivalent of merge() — flag both connections explicitly, since this dual-tool fluency (Python AND SQL) is exactly what most real analyst roles expect.
- **Local/cultural context notes:** The librarian analogy, student roster/exam results join, and Hyderabad-specific filtering examples continue the running Indian-context thread — the orders/city dataset deliberately reuses the same sales data structure introduced back in Session 5.1 for full continuity across the module.
