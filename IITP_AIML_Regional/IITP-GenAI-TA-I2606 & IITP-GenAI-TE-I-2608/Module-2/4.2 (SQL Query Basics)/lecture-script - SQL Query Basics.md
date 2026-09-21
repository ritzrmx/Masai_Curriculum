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

*The core flow above fills the full 90 minutes. Concept/Practical Block 5, on `NOT` and comparison operators beyond `=`, is provided in the Extension Blocks section for a cohort that moves ahead of pace - see Timing Contingencies.*

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

**Materials note before you continue:** the `orders` table students will use all session lives in `SQL Files/module2_phase1_sessions_4.2_to_5.2.db`. It has exactly 4 rows - small enough to reason about by eye, which is deliberate. Project it now, in full, before Concept Block 1:

```
order_id  customer_name  city       item           quantity  price  order_date
--------  -------------  ---------  -------------  --------  -----  ----------
1         Ramesh         Bengaluru  Veg Thali      2         120    2026-08-01
2         Fatima         Hyderabad  Non-Veg Thali  1         150    2026-08-01
3         Arjun          Bengaluru  Veg Thali      1         120    2026-08-02
4         Priya          Chennai    Mini Thali     3          90    2026-08-02
```

---

## Concept Block 1: Tables (8 min)

### 💬 Instructor script

Project the `orders` table. Ask: *"If this were a page in a kirana store's order register, what's a row? What's a column?"* Let students answer before formalising row/record and column/field.

> *"You already understand this shape - you've been living in it since Module 1. The only thing that changes today is HOW you interact with it. In Sheets, you scroll and click. In a database, you write a sentence-like instruction, and the database hands you back exactly what you asked for."*

### 🔴 The trap / highest-value moment

> *"In SQL, there's no such thing as clicking one cell - you always work with a whole column, filtered down to whichever rows match your conditions. Let go of the spreadsheet habit of pointing at B3. Write this down: a column name means the whole column, every row."*

---

## Practical Block 1: Reading a Table Before Querying It (8 min)

**Activity:** Hand out a larger `orders` table (15–20 rows) - this is the `orders_extended` table, in the same database, built specifically for this kind of exploratory reading exercise (do not use it later for any exercise that expects an exact number - see Materials Checklist). Before any SQL, ask in pairs: What does one row represent? If you had to find "every Chennai order" by eye, how long would it realistically take on this table? On a 40-million-row one?

**Answer key with reasoning:** One row = one order (not one item, not one customer - say this explicitly, it matters later for aggregation). On 20 rows, manual scanning is annoying but doable; at real company scale, it's simply not possible without a tool.

**If you want students to actually see the larger table rather than just imagine it, project this real 15-row `orders_extended` output** (it shares the same 4 opening rows as `orders`, plus 11 more, all July/August 2026):

```
order_id  customer_name  city       item           quantity  price  order_date
--------  -------------  ---------  -------------  --------  -----  ----------
1         Ramesh         Bengaluru  Veg Thali      2         120    2026-08-01
2         Fatima         Hyderabad  Non-Veg Thali  1         150    2026-08-01
3         Arjun          Bengaluru  Veg Thali      1         120    2026-08-02
4         Priya          Chennai    Mini Thali     3          90    2026-08-02
5         Ramesh         Bengaluru  Mini Thali     1          90    2026-08-03
6         Fatima         Hyderabad  Veg Thali      2         120    2026-08-03
7         Arjun          Bengaluru  Non-Veg Thali  1         150    2026-08-04
8         Priya          Chennai    Veg Thali      2         120    2026-08-04
9         Karthik        Bengaluru  Mini Thali     1          90    2026-08-05
10        Ramesh         Bengaluru  Veg Thali      1         120    2026-08-06
11        Fatima         Hyderabad  Mini Thali     2          90    2026-08-06
12        Priya          Chennai    Non-Veg Thali  1         150    2026-08-07
13        Arjun          Bengaluru  Mini Thali     2         180    2026-08-07
14        Fatima         Hyderabad  Non-Veg Thali  1         150    2026-08-08
15        Karthik        Bengaluru  Veg Thali      1         120    2026-08-08
```

*(Verified: `sqlite3 "module2_phase1_sessions_4.2_to_5.2.db" "SELECT * FROM orders_extended;"` against the real database - 15 rows exactly as above.)*

Ask pairs to physically count "every Chennai order" here by eye - they'll find 3 (order_id 4, 8, 12). It's doable but already mildly tedious at 15 rows; use that felt tedium as the bridge to "now imagine 40 million."

> 💬 **Expect the pushback:** *"But I could just use Ctrl+F to search 'Chennai.'"* Welcome it - it's a good instinct. Say: *"True, on a small table. Now try 'Chennai orders priced over ₹100.' Ctrl+F can't combine two conditions. That's exactly the gap SQL fills."* (Check it against the table above: only order_id 8 and 12 qualify - Ctrl+F alone can find "Chennai" instantly, but has no way to also apply "priced over ₹100" in the same search.)

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

**Verified output for `SELECT * FROM orders;`:**

```
order_id  customer_name  city       item           quantity  price  order_date
--------  -------------  ---------  -------------  --------  -----  ----------
1         Ramesh         Bengaluru  Veg Thali      2         120    2026-08-01
2         Fatima         Hyderabad  Non-Veg Thali  1         150    2026-08-01
3         Arjun          Bengaluru  Veg Thali      1         120    2026-08-02
4         Priya          Chennai    Mini Thali     3          90    2026-08-02
```

**Verified output for `SELECT customer_name, item FROM orders;`:**

```
customer_name  item
-------------  -------------
Ramesh         Veg Thali
Fatima         Non-Veg Thali
Arjun          Veg Thali
Priya          Mini Thali
```

> *"Same 4 rows, same order, but only the two columns I actually asked for. Nothing about the underlying table changed - SELECT only decides what you're SHOWN."*

### 🔴 The trap / highest-value moment

> *"If I see `SELECT *` in your query in this course without a reason, I'm going to ask why you need every single column. On a real table with forty columns and forty million rows, pulling everything is slow, and it makes your query harder for the next person to read. Name exactly what you need - that's the professional habit, starting today."*

---

## Practical Block 2: Writing SELECT Queries Live (12 min)

**Activity:** Cold-call students to dictate SELECT statements for `orders` while you type them live in the shared SQL sandbox. Progress from one column, to two, to `SELECT *` - explicitly contrast the last against the "name exactly what you need" rule.

**Answer key with reasoning, in order of increasing scope:**

```sql
SELECT customer_name FROM orders;
-- Ramesh, Fatima, Arjun, Priya
```

```sql
SELECT customer_name, item FROM orders;
-- confirm aloud: "customer_name and item alone is enough if I just need a delivery
-- checklist - I don't need price or date for that"
```

```sql
SELECT customer_name, item, price, order_date FROM orders;
-- now four named columns - still not SELECT *, still deliberate
```

```sql
SELECT * FROM orders;
-- every column - explicitly ask the room: "what's actually different about
-- this last query, compared to naming four columns individually?"
```

For each, confirm aloud which business need it serves.

> 💬 **Expect at least one typo'd column name to happen naturally.** Welcome it - don't rush to fix it. Ask: *"What is this error message actually telling us?"* This normalises reading SQL errors calmly, a skill needed constantly for the rest of the course.

**If it doesn't happen naturally, force it deliberately** - run `SELECT customr_name FROM orders;` live and let the real error appear:

```
Error: in prepare, no such column: customr_name
  SELECT customr_name FROM orders;
         ^--- error here
```

> *"Read the error out loud with the class: 'no such column: customr_name.' SQLite is telling you exactly what's wrong, in plain terms - it just won't guess what you meant. Compare the spelling to the table you have projected. Errors like this are not a sign something has gone badly wrong; they're the database double-checking your spelling for you."*

---

## BREAK (5 min)

---

## Concept Block 3: WHERE (8 min)

### 💬 Instructor script

> *"WHERE always comes after FROM, never before. And text values always go in quotes - numbers never do. Watch what happens if I forget."*

Write `WHERE city = Bengaluru` (no quotes) deliberately, run it, let the error or unexpected behaviour appear, then correct it to `WHERE city = 'Bengaluru'`.

**Verified: running the unquoted version produces a real error, not just "unexpected behaviour" - show this exact output:**

```
Error: in prepare, no such column: Bengaluru
  SELECT * FROM orders WHERE city = Bengaluru;
                      error here ---^
```

> *"Notice what SQLite actually thinks is happening here: without quotes, it assumes `Bengaluru` must be another COLUMN name, not a piece of text - because that's the only thing an unquoted word can mean in SQL. There's no column called Bengaluru, so it errors. This is worth knowing precisely, because the error message won't say 'you forgot quotes' - it'll say 'no such column,' and you have to recognise that pattern yourself."*

Now run the corrected version and show the real result:

```sql
SELECT * FROM orders WHERE city = 'Bengaluru';
```

```
order_id  customer_name  city       item       quantity  price  order_date
--------  -------------  ---------  ---------  --------  -----  ----------
1         Ramesh         Bengaluru  Veg Thali  2         120    2026-08-01
3         Arjun          Bengaluru  Veg Thali  1         120    2026-08-02
```

### 🔴 The trap / highest-value moment

> *"You just watched a missing pair of quotes break a query, and you watched exactly why - SQL guessed you meant a column, not text. That will happen to you again in this course - probably next week. When it does, the first thing to check is exactly this: are my text values quoted?"*

---

## Practical Block 3: Filtering the Orders Table (12 min)

**Activity:** Individually or in pairs, write WHERE queries in increasing difficulty: (1) orders from Hyderabad, (2) orders priced above ₹100, (3) orders placed on a specific date.

**Answer key with verified output:**

```sql
SELECT * FROM orders WHERE city = 'Hyderabad';
```
```
order_id  customer_name  city       item           quantity  price  order_date
--------  -------------  ---------  -------------  --------  -----  ----------
2         Fatima         Hyderabad  Non-Veg Thali  1         150    2026-08-01
```

```sql
SELECT * FROM orders WHERE price > 100;
```
```
order_id  customer_name  city       item           quantity  price  order_date
--------  -------------  ---------  -------------  --------  -----  ----------
1         Ramesh         Bengaluru  Veg Thali      2         120    2026-08-01
2         Fatima         Hyderabad  Non-Veg Thali  1         150    2026-08-01
3         Arjun          Bengaluru  Veg Thali      1         120    2026-08-02
```

```sql
SELECT * FROM orders WHERE order_date = '2026-08-02';
```
```
order_id  customer_name  city     item           quantity  price  order_date
--------  -------------  -------  -------------  --------  -----  ----------
3         Arjun          Bengaluru Veg Thali     1         120    2026-08-02
4         Priya          Chennai  Mini Thali     3          90    2026-08-02
```

Say aloud for each: "notice the quotes only appear around text and dates written as text - never around a plain number." Point out that `price > 100` correctly excludes Priya's ₹90 order - only the three orders strictly above 100 come back.

> 💬 **Expect confusion over `>` vs `>=` for "at least ₹100."** Welcome it. Say: *"'Above ₹100' excludes exactly 100. 'At least ₹100' includes it. Read the business question word for word before picking your operator."* Demonstrate live: `SELECT * FROM orders WHERE price >= 120;` returns 3 rows (Ramesh, Fatima, Arjun, all ₹120 or ₹150), while `WHERE price > 120;` returns only Fatima's ₹150 order. *"One symbol, completely different result set - always read the business question for the word 'above' versus 'at least' or 'or more.'"*

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

**Verified: this query genuinely returns 0 rows against the real table** - confirmed by running it directly against `module2_phase1_sessions_4.2_to_5.2.db`.

### 🔴 The trap / highest-value moment

> *"In English, 'I want Veg Thali and Mini Thali options' sounds perfectly normal. In SQL, AND means BOTH conditions must be true for the SAME row - and no single order can be two different items at once. Write down the test that saves you every time: can one row satisfy both conditions simultaneously? If not, you need OR."*

Correct it live to `OR` and show results populate.

**Verified output for the corrected query:**

```sql
SELECT customer_name, item
FROM orders
WHERE item = 'Veg Thali' OR item = 'Mini Thali';
```
```
customer_name  item
-------------  ----------
Ramesh         Veg Thali
Arjun          Veg Thali
Priya          Mini Thali
```

**A second, equally important AND example - one where AND is correctly the right choice, to balance the lesson so students don't walk away thinking "AND is always wrong":**

```sql
SELECT * FROM orders WHERE city = 'Bengaluru' AND price > 100;
```
```
order_id  customer_name  city       item       quantity  price  order_date
--------  -------------  ---------  ---------  --------  -----  ----------
1         Ramesh         Bengaluru  Veg Thali  2         120    2026-08-01
3         Arjun          Bengaluru  Veg Thali  1         120    2026-08-02
```

> *"Here, AND is exactly right - both conditions describe FACTS ABOUT THE SAME ROW simultaneously. City and price are two different attributes of one order; item and item are the same attribute asked to be two things at once. That's the real test: are these two conditions about the same attribute, or two different attributes?"*

---

## Practical Block 4: Translate-and-Query Challenge (11 min)

**Activity:** Light competitive framing. Give the class 4–5 business questions in plain English (from the pre-read's Phase-style exercises) and have pairs race to translate and write the correct query. Reveal answers one at a time.

**Full answer key, verified against the real database:**

**1. "Show me every order from Chennai."**
```sql
SELECT * FROM orders WHERE city = 'Chennai';
```
```
order_id  customer_name  city     item        quantity  price  order_date
--------  -------------  -------  ----------  --------  -----  ----------
4         Priya          Chennai  Mini Thali  3          90    2026-08-02
```

**2. "Which orders were for a Veg Thali AND cost more than ₹100?"**
```sql
SELECT * FROM orders WHERE item = 'Veg Thali' AND price > 100;
```
```
order_id  customer_name  city       item       quantity  price  order_date
--------  -------------  ---------  ---------  --------  -----  ----------
1         Ramesh         Bengaluru  Veg Thali  2         120    2026-08-01
3         Arjun          Bengaluru  Veg Thali  1         120    2026-08-02
```

**3. "Show me every customer who ordered from either Bengaluru or Chennai."**
```sql
SELECT customer_name, item, price FROM orders WHERE city = 'Bengaluru' OR city = 'Chennai';
```
```
customer_name  item        price
-------------  ----------  -----
Ramesh         Veg Thali   120
Arjun          Veg Thali   120
Priya          Mini Thali  90
```

**4. "Show me every customer who did NOT order from Bengaluru."**
```sql
SELECT customer_name, city FROM orders WHERE NOT city = 'Bengaluru';
```
```
customer_name  city
-------------  ---------
Fatima         Hyderabad
Priya          Chennai
```

For each, say aloud the translation step first ("columns needed... conditions needed...") before showing the SQL - this is the actual transferable skill, not just syntax recall.

> 💬 **Expect a pair to get an OR-vs-AND answer right "by feel" without being able to explain why.** Welcome it - use it as a teaching moment: *"Getting it right once by instinct won't help you next week on a harder question. Can you state the 'same row, both true?' test out loud?"*

---

## Extension Blocks (Optional — Use if Running Ahead)

*Not part of the 90-minute core flow. Use only if Practical Block 4 finishes early - see Timing Contingencies.*

### Concept Block 5 (Extension): NOT and the Full Comparison Operator Set

#### 💬 Instructor script

> *"You already used NOT once, in the last Practical Block's fourth question. Let's make it official, alongside the full set of comparison operators SQL gives you."*

Write the operator reference on the board:

```
=      equal to
!=  or <>   not equal to
>      greater than
<      less than
>=     greater than or equal to
<=     less than or equal to
NOT    reverses a condition
```

Demonstrate `!=` directly against `NOT`:

```sql
SELECT customer_name, city FROM orders WHERE city != 'Bengaluru';
```

Verified output - identical to the `NOT city = 'Bengaluru'` result from Practical Block 4:

```
customer_name  city
-------------  ---------
Fatima         Hyderabad
Priya          Chennai
```

#### 🔴 The trap / highest-value moment

> *"`city != 'Bengaluru'` and `NOT city = 'Bengaluru'` gave you the identical result just now - so which should you use? Either is correct SQL. Most analysts reach for `!=` for a single simple condition, and save `NOT` for wrapping something more complex, like `NOT (city = 'Bengaluru' AND price > 100)`, where negating the whole combined condition would be awkward to write with `!=` alone. Write this down: know both exist, and pick whichever reads more clearly for the specific condition in front of you."*

### Practical Block 5 (Extension): Full Operator Challenge

**Activity:** Individually, students write: (1) every order NOT priced at exactly ₹120; (2) every order from a city that is not Chennai, using `!=` this time instead of `NOT`.

**Verified answer key:**

```sql
SELECT * FROM orders WHERE price != 120;
```
```
order_id  customer_name  city       item           quantity  price  order_date
--------  -------------  ---------  -------------  --------  -----  ----------
2         Fatima         Hyderabad  Non-Veg Thali  1         150    2026-08-01
4         Priya          Chennai    Mini Thali     3          90    2026-08-02
```

```sql
SELECT * FROM orders WHERE city != 'Chennai';
```
```
order_id  customer_name  city       item           quantity  price  order_date
--------  -------------  ---------  -------------  --------  -----  ----------
1         Ramesh         Bengaluru  Veg Thali      2         120    2026-08-01
2         Fatima         Hyderabad  Non-Veg Thali  1         150    2026-08-01
3         Arjun          Bengaluru  Veg Thali      1         120    2026-08-02
```

> 💬 **Expect someone to try `<>` instead of `!=` and ask if it's different.** Welcome it - confirm they're fully interchangeable in SQLite and most SQL dialects; `!=` is simply the more commonly typed form in this course.

---

## Common Errors

| Error | What causes it | Fix |
|---|---|---|
| `no such column: Bengaluru` | Forgetting quotes around a text value in WHERE | Wrap every text value in single quotes; numbers never get quotes |
| `no such column: customr_name` (or similar) | Misspelled column name in SELECT or WHERE | Compare against the actual table's column names; re-run after correcting the spelling |
| Query returns 0 rows unexpectedly with AND | Using AND on two conditions that describe the same attribute (e.g. `item = 'X' AND item = 'Y'`) | Ask "can one row be both at once?" - if no, switch to OR |
| Query returns far more rows than expected with OR | Using OR where AND was actually needed, loosening the filter instead of narrowing it | Re-read the business question - "and" in English does not always mean SQL's AND |
| `SELECT *` used out of habit on a real (large) table | Not stopping to name only the needed columns | Always list exact column names unless there's a specific reason to need every column |
| Writing WHERE before FROM, or omitting FROM | Muscle memory from spoken English word order | Keep the fixed skeleton `SELECT ... FROM ... WHERE ...` visible and check clause order before running |
| Using `>` when the business question means "at least" | Not distinguishing "above" from "at least/or more" in the plain-English request | Translate the exact wording first: "above" → `>`, "at least" → `>=` |
| Confusing `orders` and `orders_extended` results | Running a Session 9/10 "exact number" exercise against the 15-row exploratory table instead of the 4-row core table | Use `orders` for anything with a quoted exact expected result; `orders_extended` only for the open-ended reading exercise in Practical Block 1 |

---

## Materials Checklist

Before class, have ready:

- `SQL Files/module2_phase1_sessions_4.2_to_5.2.db` loaded in the shared SQL sandbox (SQLite). This is the ONLY database needed for this session.
- Confirm the `orders` table (4 rows) is what every timed/exact-number example in this script uses - `orders_extended` (15 rows, same file) is for Practical Block 1's open-ended reading exercise only. Do not swap them.
- A projector or shared screen for live query typing during Concept Block 2, Practical Block 2, and Concept Block 4's AND/OR trap demo - these are strongest done live, not pre-recorded.
- Printed or slide copies of the `orders` table (4 rows) and `orders_extended` table (15 rows) for students who prefer working from a static reference while writing queries.
- The pre-read's plain-English business questions for Practical Block 4, ready to reveal one at a time.

---

## Timing Contingencies

**If running long:**
- Compress Practical Block 1 to a single verbal pass over the projected `orders_extended` table rather than a full paired discussion - the "how long would this take by eye" point can land in under 3 minutes.
- In Practical Block 4, run only 3 of the 4 business questions live and assign the 4th as a take-home or quick individual check rather than a full-class reveal.
- Never cut the deliberate missing-quotes error in Concept Block 3 or the AND/OR zero-rows trap in Concept Block 4 - both are the two highest-value "aha" moments in the session and directly prevent the most common errors in every session that follows.

**If running short:**
- Run the Extension Blocks (NOT and the full comparison operator set) in full.
- If only a few minutes remain, skip straight to the Extension Block's `!=` vs `NOT` comparison as a quick live demo without the full paired Practical Block 5.
- Alternatively, revisit Practical Block 3's Hyderabad/price/date queries and ask students to combine all three conditions into a single WHERE clause with AND - a natural preview of Concept Block 4 that also reinforces multi-condition WHERE thinking.

---

## End-of-Session Quiz

1. **What does SELECT control, and what does WHERE control?**
   → SELECT controls which columns appear in the output. WHERE controls which rows are included.

2. **Why does `WHERE city = Bengaluru` (no quotes) cause an error?**
   → SQL interprets an unquoted word as a column name, not text - there's no column called Bengaluru, so it errors with "no such column."

3. **`SELECT customer_name, item FROM orders WHERE item = 'Veg Thali' AND item = 'Mini Thali';` returns how many rows, and why?**
   → Zero rows - no single order can be both a Veg Thali and a Mini Thali at once, so no row can ever satisfy both AND conditions simultaneously.

4. **When should you reach for OR instead of AND?**
   → When the business question describes multiple acceptable values for the same attribute (e.g. "Veg Thali or Mini Thali") - ask "can one row satisfy both conditions at once?" If not, use OR.

5. **What's the difference between `price > 100` and `price >= 100`?**
   → `>` (above) strictly excludes 100 itself; `>=` (at least) includes rows where price is exactly 100.

6. **(If Extension Block covered) What's the difference between `!=` and `NOT`?**
   → Both negate a condition and can produce identical results for a simple single condition; `NOT` is generally preferred for negating a more complex, combined condition rather than a single equality check.

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

**Q: Is there a difference between `orders` and `orders_extended`? Why two tables?**
→ `orders` (4 rows) is the table every exact number in this course's Session 9–12 scripts is calculated against. `orders_extended` (15 rows) exists purely so Practical Block 1 has a "realistically larger" table to practice reading - no exercise depends on an exact count or total from it.

**Q: Can WHERE compare two columns to each other, not just a column to a fixed value?**
→ Yes - e.g. `WHERE quantity > 1` compares a column to a number, but you can also write `WHERE price > quantity` to compare two columns directly, though that particular comparison wouldn't mean much on this dataset since they're different units. Column-to-column comparisons become genuinely useful once we reach richer tables.

---

## Instructor Notes

- **Words not yet earned:** Avoid `ORDER BY`, `GROUP BY`, `JOIN`, aggregate functions, and subqueries - these arrive across the rest of Module 2. If asked "how do I sort this?", acknowledge it's next session rather than answering in full now.
- **The single biggest risk in this session** is first-tool anxiety - this is students' first new software since spreadsheets. Defeat it by normalising errors early: the deliberate typo in Practical Block 2 and the deliberate missing-quotes error in Concept Block 3 exist specifically to make error messages feel routine.
- **Board management:** Keep the `SELECT [columns] FROM [table] WHERE [condition];` skeleton visible on the board for the entire session - every example should be traceable back to it. If running the Extension Block, add the operator reference table to a separate section of the board.
- **Common confusions, numbered:**
  1. Expecting to click a single cell the way they did in Sheets. Redirect every time to "a whole column, filtered by row conditions."
  2. Missing quotes around text values - the single most frequent error this session. Treat it lightly and consistently.
  3. Defaulting to AND when OR is needed. Tie every instance back to the "can one row satisfy both?" test.
  4. Confusing `orders_extended` (exploratory only) with `orders` (the table every exact number is calculated against) - if a student quotes a count or total from the wrong table, gently redirect them to the correct one.
- **Cross-references:** ORDER BY arrives next session. GROUP BY and HAVING (filtering *grouped* results, a cousin of WHERE) arrive with Aggregation Essentials and Grouping for KPIs. JOINs arrive with Joining Tables Together.
- **Local/cultural context:** The `orders` table spans Bengaluru, Hyderabad, and Chennai deliberately - this sets up the multi-city comparisons reused in later Module 2 sessions on grouping and joins, so keep this exact table and story running through the module.
