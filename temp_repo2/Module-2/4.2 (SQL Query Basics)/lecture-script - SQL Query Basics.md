# Lecture Script: SQL for Data Analysis - SQL Query Basics
> **Instructor Reference** - Module 2: SQL for Data Analysis | Academic Session 9 | Duration: 1.5 Hours | Instructor: Industry Mentor

---

## Session Overview

**Goal:** Students can take a plain-English business question, translate it into which columns and which row conditions it needs, and write a correct `SELECT ... FROM ... WHERE ...` query to answer it.

**Student profile at this point:** They've completed Module 1 (spreadsheets, pivot tables) and Session 8 (spread and variability, by hand, no tools). This is their **first contact with SQL** and their first new software since spreadsheets. Expect some first-tool anxiety - treat errors as routine, not alarming.

**Key outcome:** Students leave able to answer the question every entry-level analytics job actually tests: *"Can you pull me the rows I need, without me having to explain it twice?"*

> 🎯 **The one sentence this session must land:** *SELECT chooses what you see. WHERE chooses which rows you see it for. Every query in this course is built from just those two ideas.*

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| Opening - "40 million rows. No spreadsheet will open that." | 8 min | 8 min |
| Concept Block 1: Tables | 8 min | 16 min |
| Practical Block 1: Reading a table before querying it | 8 min | 24 min |
| Concept Block 2: SELECT | 8 min | 32 min |
| Practical Block 2: Writing SELECT queries live | 12 min | 44 min |
| **BREAK** | 5 min | 49 min |
| Concept Block 3: WHERE | 8 min | 57 min |
| Practical Block 3: Filtering the orders table | 12 min | 69 min |
| Concept Block 4: AND / OR | 10 min | 79 min |
| Practical Block 4: Translate-and-query challenge | 11 min | 90 min |

---

## Opening - "40 Million Rows. No Spreadsheet Will Open That." (8 min)

Walk in with no slide up. Say:

> *"Your manager says: 'Pull me every order from Bengaluru priced over ₹100.' Simple enough - except the table lives in the company database and has 40 million rows. Not 40. Forty MILLION. What do you do?"*

Take answers from the room. You'll hear "export it to Excel first" - push back immediately:

> *"Excel caps out around a million rows, and even if it didn't - would you really scroll through 40 million looking for 'Bengaluru and over ₹100' by eye? You'd make mistakes, and it would take days."*

Land the real point:

> *"Every pivot table you built in Module 1 needed clean, complete data to summarise. Today you learn how that data actually gets OUT of a real company database in the first place - not by exporting and hoping, but by asking the database precisely, in its own language, for exactly the rows you need."*

**Pivot line:**

> *"By the end of ninety minutes, you'll write a query that takes a plain business question and returns exactly the right rows - instantly, from a table of any size. That's true whether the table has 4 rows or 40 million. That's the whole point of learning SQL properly."*

**Context for the sessions ahead:** *"SELECT and WHERE are the skeleton of every query you'll write for the rest of this course. ORDER BY next session, GROUP BY and JOIN after that - they all sit on top of exactly what you learn today."*

---

## Concept Block 1: Tables (8 min)

### 💬 Instructor script

Project the `orders` table. Ask: *"If this were a page in a kirana store's order register, what's a row? What's a column?"* Let students answer before formalising row/record and column/field.

> *"You already understand this shape - you've been living in it since Module 1. The only thing that changes today is HOW you interact with it. In Sheets, you scroll and click. In a database, you write a sentence-like instruction, and the database hands you back exactly what you asked for."*

### 🔴 The trap / highest-value moment

> *"In SQL, there's no such thing as clicking one cell - you always work with a whole column, filtered down to whichever rows match your conditions. Let go of the spreadsheet habit of pointing at B3. Write this down: a column name means the whole column, every row."*

---

## Practical Block 1: Reading a Table Before Querying It (8 min)

**Activity:** Hand out a larger `orders` table (15–20 rows). Before any SQL, ask in pairs: What does one row represent? If you had to find "every Chennai order" by eye, how long would it realistically take on this table? On a 40-million-row one?

**Answer key with reasoning:** One row = one order (not one item, not one customer - say this explicitly, it matters later for aggregation). On 20 rows, manual scanning is annoying but doable; at real company scale, it's simply not possible without a tool.

> 💬 **Expect the pushback:** *"But I could just use Ctrl+F to search 'Chennai.'"* Welcome it - it's a good instinct. Say: *"True, on a small table. Now try 'Chennai orders priced over ₹100.' Ctrl+F can't combine two conditions. That's exactly the gap SQL fills."*

---

## Concept Block 2: SELECT (8 min)

### 💬 Instructor script

Write the skeleton on the board and say it stays up all session:

```
SELECT [columns]
FROM [table]
WHERE [condition];
```

Write `SELECT * FROM orders;` first, walk through the expected output, then narrow to `SELECT customer_name, item FROM orders;`.

### 🔴 The trap / highest-value moment

> *"If I see `SELECT *` in your query in this course without a reason, I'm going to ask why you need every single column. On a real table with forty columns and forty million rows, pulling everything is slow, and it makes your query harder for the next person to read. Name exactly what you need - that's the professional habit, starting today."*

---

## Practical Block 2: Writing SELECT Queries Live (12 min)

**Activity:** Cold-call students to dictate SELECT statements for `orders` while you type them live in the shared SQL sandbox. Progress from one column, to two, to `SELECT *` - explicitly contrast the last against the "name exactly what you need" rule.

**Answer key with reasoning:** For each query, confirm aloud which business need it serves (e.g., "customer_name and item alone is enough if I just need a delivery checklist - I don't need price or date for that").

> 💬 **Expect at least one typo'd column name to happen naturally.** Welcome it - don't rush to fix it. Ask: *"What is this error message actually telling us?"* This normalises reading SQL errors calmly, a skill needed constantly for the rest of the course.

---

## BREAK (5 min)

---

## Concept Block 3: WHERE (8 min)

### 💬 Instructor script

> *"WHERE always comes after FROM, never before. And text values always go in quotes - numbers never do. Watch what happens if I forget."*

Write `WHERE city = Bengaluru` (no quotes) deliberately, run it, let the error or unexpected behaviour appear, then correct it to `WHERE city = 'Bengaluru'`.

### 🔴 The trap / highest-value moment

> *"You just watched a missing pair of quotes break a query. That will happen to you again in this course - probably next week. When it does, the first thing to check is exactly this: are my text values quoted?"*

---

## Practical Block 3: Filtering the Orders Table (12 min)

**Activity:** Individually or in pairs, write WHERE queries in increasing difficulty: (1) orders from Hyderabad, (2) orders priced above ₹100, (3) orders placed on a specific date.

**Answer key with reasoning:** `WHERE city = 'Hyderabad'`; `WHERE price > 100`; `WHERE order_date = '2026-08-02'`. Say aloud for each: "notice the quotes only appear around text and dates written as text - never around a plain number."

> 💬 **Expect confusion over `>` vs `>=` for "at least ₹100."** Welcome it. Say: *"'Above ₹100' excludes exactly 100. 'At least ₹100' includes it. Read the business question word for word before picking your operator."*

---

## Concept Block 4: AND / OR (10 min)

### 💬 Instructor script

Introduce the operator table from the pre-read, then run the trap live:

```sql
SELECT customer_name, item
FROM orders
WHERE item = 'Veg Thali' AND item = 'Mini Thali';
```

Run it - zero rows. Ask the room why, before explaining.

### 🔴 The trap / highest-value moment

> *"In English, 'I want Veg Thali and Mini Thali options' sounds perfectly normal. In SQL, AND means BOTH conditions must be true for the SAME row - and no single order can be two different items at once. Write down the test that saves you every time: can one row satisfy both conditions simultaneously? If not, you need OR."*

Correct it live to `OR` and show results populate.

---

## Practical Block 4: Translate-and-Query Challenge (11 min)

**Activity:** Light competitive framing. Give the class 4–5 business questions in plain English (from the pre-read's Phase-style exercises) and have pairs race to translate and write the correct query. Reveal answers one at a time.

**Answer key with reasoning:** For each, say aloud the translation step first ("columns needed... conditions needed...") before showing the SQL - this is the actual transferable skill, not just syntax recall.

> 💬 **Expect a pair to get an OR-vs-AND answer right "by feel" without being able to explain why.** Welcome it - use it as a teaching moment: *"Getting it right once by instinct won't help you next week on a harder question. Can you state the 'same row, both true?' test out loud?"*

---

## Summary & Bridge

**Recap table:**

| Concept | The one thing to remember |
|---|---|
| Tables | Same row/column shape as a spreadsheet - just queried, not scrolled |
| SELECT | Chooses which columns you see. Name exactly what you need. |
| WHERE | Filters which rows you see. Quote text, never quote numbers. |
| AND / OR | AND = both true on the same row. OR = at least one true. Ask "can one row satisfy both?" |

**Close on the thesis line:**

> *"Ninety minutes ago, your manager wanted every Bengaluru order over ₹100, out of a 40-million-row table. Most of you would have said 'export it to Excel and hope.' What would you say now? You'd say: `SELECT customer_name, item, price FROM orders WHERE city = 'Bengaluru' AND price > 100;` - and you'd have the answer before your manager finished asking the question."*

**Bridge to next session:**

> *"Right now, if I ask for the highest-priced order in Bengaluru, you'd have to scroll your results looking for the biggest number. Next session - Sorting and Filtering in SQL - you learn ORDER BY, so the database sorts it for you instead. Same skeleton, one more clause."*

---

## Q&A & Doubt Solving

**Q: Does the order of SELECT and WHERE matter?**
→ Yes - SQL requires `SELECT ... FROM ... WHERE ...` in that order. Future clauses (ORDER BY, GROUP BY) each have a fixed position in the sequence too.

**Q: Can I filter on a column I'm not selecting?**
→ Yes. WHERE can reference any column in the table, even ones absent from your SELECT list - e.g., `SELECT customer_name FROM orders WHERE price > 100;` works without selecting `price` itself.

**Q: Is SQL case-sensitive?**
→ Keywords are conventionally uppercase for readability, but SQL doesn't require it. Column/table names can be case-sensitive depending on the database system - we'll use consistent lowercase naming throughout this course.

**Q: What happens if my WHERE condition matches nothing?**
→ The query runs successfully and returns an empty result - that's not an error. "No Chennai orders above ₹200 today" is a real, correct, useful answer.

**Q: Can I use WHERE on a column that doesn't exist in the table?**
→ No - this causes an error, because SQL checks that every referenced column actually exists before running the query. This is a good early error to get comfortable reading.

---

## Instructor Notes

- **Words not yet earned:** Avoid `ORDER BY`, `GROUP BY`, `JOIN`, aggregate functions, and subqueries - these arrive across the rest of Module 2. If asked "how do I sort this?", acknowledge it's next session rather than answering in full now.
- **The single biggest risk in this session** is first-tool anxiety - this is students' first new software since spreadsheets. Defeat it by normalising errors early: the deliberate typo in Practical Block 2 and the deliberate missing-quotes error in Concept Block 3 exist specifically to make error messages feel routine.
- **Board management:** Keep the `SELECT [columns] FROM [table] WHERE [condition];` skeleton visible on the board for the entire session - every example should be traceable back to it.
- **Common confusions, numbered:**
  1. Expecting to click a single cell the way they did in Sheets. Redirect every time to "a whole column, filtered by row conditions."
  2. Missing quotes around text values - the single most frequent error this session. Treat it lightly and consistently.
  3. Defaulting to AND when OR is needed. Tie every instance back to the "can one row satisfy both?" test.
- **Cross-references:** ORDER BY arrives next session. GROUP BY and HAVING (filtering *grouped* results, a cousin of WHERE) arrive with Aggregation Essentials and Grouping for KPIs. JOINs arrive with Joining Tables Together.
- **Local/cultural context:** The `orders` table spans Bengaluru, Hyderabad, and Chennai deliberately - this sets up the multi-city comparisons reused in later Module 2 sessions on grouping and joins, so keep this exact table and story running through the module.
