# Data Analysis with Spreadsheets
---

## Mental Map

```mermaid
%%{init: {'flowchart': {'nodeSpacing': 55, 'rankSpacing': 65, 'diagramPadding': 24}}}%%
flowchart TB
linkStyle default stroke-width:3px
subgraph foundation[" Foundation "]
direction TB
    CURMOD["<b>Current Module Until<br/>Previous Session</b><br/><i>Foundations of Data</i><br/>Python · Pandas · groupby<br/>EDA · MySQL · charts"]
    CURSES["<b>Current Session</b><br/><b>Data Analysis with Spreadsheets</b><br/><i>Shift:</i> Same thinking,<br/>spreadsheet interface<br/>Lookup · pivot · dashboard"]
end
subgraph value[" Value "]
direction LR
    CVAL["<b>Course Value</b><br/>Translate any dataset<br/>into a clear finding"]
    RVAL["<b>Real-Life Value</b><br/>Present insights that<br/>drive business action"]
end
subgraph future[" Future Path "]
direction TB
    U0["<b>Upcoming Module</b><br/>Classical ML<br/><i>[sklearn · stats]</i>"]
    U1["<b>Upcoming Module</b><br/>GenAI & Agents<br/><i>[LLMs · agents]</i>"]
end
START["Course Start"] ==>|&nbsp;Begin&nbsp;| CURMOD
CURMOD ==>|&nbsp;Progress&nbsp;| CURSES
CURSES ==>|&nbsp;Course Path&nbsp;| CVAL
CURSES ==>|&nbsp;Real-Life&nbsp;| RVAL
CURSES ==>|&nbsp;Next Module&nbsp;| U0
U0 -.->|&nbsp;Ahead&nbsp;| U1
classDef curModBox fill:#FFF8E6,stroke:#B7791F,stroke-width:2px,color:#1A202C
classDef curSessBox fill:#E6FFFA,stroke:#0D9488,stroke-width:3px,color:#1A202C
classDef valueBox fill:#F3E8FF,stroke:#7C3AED,stroke-width:2px,color:#1A202C
classDef futureBox fill:#ECFDF5,stroke:#047857,stroke-width:2px,color:#1A202C
classDef startBox fill:#F7FAFC,stroke:#4A5568,stroke-width:2px,color:#1A202C
class START startBox
class CURMOD curModBox
class CURSES curSessBox
class CVAL,RVAL valueBox
class U0,U1 futureBox
```

## What You'll Learn

In this pre-read, you'll discover:

- How Excel organises data and why its structure mirrors a Pandas DataFrame
- How **lookup functions** (`VLOOKUP`, `XLOOKUP`) retrieve values across sheets
- How **Pivot Tables** summarise large datasets with a few clicks — and how they map to `groupby`
- - How the same **analytical thinking** travels across Excel and Python

---

## A. Excel Basics — Familiar Structure, Different Tool

> 💡 **Analogy:** A map of a city looks different in a road atlas, on Google Maps, and on a paper sketch — but the streets are the same. **Excel, Pandas, and SQL** all work on the same idea of rows and columns; they just speak it differently.

**One-line definition:** **Excel** is a spreadsheet tool where data lives in a grid of rows and columns, formulas compute values from cells, and built-in features handle sorting, filtering, and summarising without any code.

```mermaid
flowchart LR
    subgraph excel["Excel workbook"]
        E["Sheet = table\nRow = record\nColumn = field\nCell = one value"]
    end
    subgraph pandas["Pandas DataFrame"]
        P["DataFrame = table\nRow = record\nColumn = field\nCell = df.loc[r,c]"]
    end
    excel -->|"same concept"| pandas
```

**Key Excel concepts:**

| Excel term | Equivalent in Pandas / SQL | What it is |
|---|---|---|
| Worksheet | DataFrame / table | One grid of data |
| Cell reference (A1) | `df.iloc[0, 0]` | One value by position |
| Named range | Variable pointing to a DataFrame | A labelled block of data |
| Formula | Vectorized operation | A calculation on column(s) |
| AutoFilter | Boolean filter mask | Show only rows matching a rule |
| Freeze panes | — | Keep header visible while scrolling |

**Excel strengths vs Python:**

| Task | Better in Excel | Better in Python |
|---|---|---|
| Quick ad-hoc table | ✅ | |
| Reproducible pipeline | | ✅ |
| 1 million+ rows | | ✅ |
| Sharing a chart with non-coders | ✅ | |
| Automating repeated cleaning | | ✅ |

Both tools have a place. In most AI roles, Python handles data at scale; Excel handles communication and quick checks with stakeholders.

---

## B. Lookup Functions — Fetching Values Across Tables

> 💡 **Analogy:** A school office keeps student details in one register and exam scores in another. To find a student's score, a clerk looks up the student ID in the score sheet. **VLOOKUP and XLOOKUP** automate exactly that cross-table lookup.

**One-line definition:** A **lookup function** searches for a value in one column and returns a corresponding value from another column in the same or a different table — like a join done one cell at a time.

**VLOOKUP — the classic:**

```
=VLOOKUP(lookup_value, table_array, col_index_num, [exact_match])
```

| Argument | Plain meaning | Example |
|---|---|---|
| `lookup_value` | What you are searching for | A customer ID in cell A2 |
| `table_array` | The range containing your data | `Customers!A:D` |
| `col_index_num` | Which column to return (1 = first) | `3` for the third column |
| `[exact_match]` | `FALSE` for exact, `TRUE` for approximate | `FALSE` almost always |

**XLOOKUP — the modern replacement:**

```
=XLOOKUP(lookup_value, lookup_array, return_array, [if_not_found])
```

XLOOKUP is more flexible: it searches any direction, handles missing matches gracefully with a custom message, and does not require the lookup column to be first.

**How this maps to Pandas:**

```mermaid
flowchart LR
    V["VLOOKUP / XLOOKUP\nin Excel"] -->|"same idea"| M["pd.merge()\nor df.map()\nin Pandas"]
```

| Excel | Pandas equivalent |
|---|---|
| `VLOOKUP` on one key column | `df.merge(other, on="id")` |
| Return one matching value | `df["col"].map(dict_or_series)` |
| `IFERROR(VLOOKUP(…), "Not found")` | `merge(how="left")` — NaN for no match |

**Common VLOOKUP pitfalls:**
- The lookup column **must be the leftmost** column in the range (XLOOKUP removes this constraint)
- Using `TRUE` for exact match when you meant `FALSE` — causes silent wrong answers
- Referencing a range without `$` (absolute reference) — formula breaks when copied down

---

## C. Pivot Tables — Drag-and-Drop GroupBy

> 💡 **Analogy:** A Pivot Table is like having a `groupby` with a drag-and-drop interface. You pull a column to "Rows," another to "Values," and Excel instantly collapses thousands of rows into one summary — no formula needed.

**One-line definition:** A **Pivot Table** is an interactive summary tool that groups rows by one or more categories and computes aggregates (sum, count, average) for each group, mirroring `df.groupby().agg()` in Pandas.



**Pivot Table → Pandas equivalent:**

| Pivot Table action | Pandas equivalent |
|---|---|
| Drag field to Rows | `groupby("region")` |
| Drag field to Values → Sum | `.agg(total=("sales","sum"))` |
| Drag field to Columns | `groupby(["region","product"])` |
| Filter slicer | `.loc[df["year"]==2024]` before groupby |
| Show % of total | `/ df["sales"].sum() * 100` |

**Why learn both:** Pivot Tables are what your manager or client will already have in their spreadsheet. Knowing the Pandas equivalent means you can reproduce any Pivot Table programmatically, on data 100× larger, and automate it to refresh daily.

---

## D. SQL SELECT, WHERE, and ORDER BY

> 💡 **Analogy:** SQL is like placing a precise order at a café — "I want the chicken sandwich (SELECT), no tomatoes (WHERE), served hottest first (ORDER BY)." Each clause is one specific instruction in your order.

**One-line definition:** `SELECT`, `WHERE`, and `ORDER BY` are the three core SQL clauses that choose *which columns* to show, *which rows* to keep, and *in what order* to display them.

**The anatomy of a basic query:**



**SELECT — pick your columns:**

```sql
SELECT name, salary, city          -- specific columns
SELECT *                           -- all columns (use sparingly)
SELECT name, salary * 1.1 AS new_salary  -- computed column
```

**WHERE — filter rows:**

```sql
WHERE city = 'Mumbai'
WHERE salary > 50000
WHERE city = 'Pune' AND salary > 40000
WHERE city IN ('Mumbai', 'Delhi', 'Pune')
WHERE name LIKE 'A%'               -- names starting with A
WHERE join_date BETWEEN '2023-01-01' AND '2023-12-31'
WHERE manager_id IS NULL           -- missing values
```

**ORDER BY — sort results:**

```sql
ORDER BY salary DESC               -- highest first
ORDER BY city ASC, salary DESC     -- city A→Z, then highest salary within city
```

**Pandas ↔ SQL quick map:**

| SQL | Pandas equivalent |
|---|---|
| `SELECT col1, col2` | `df[["col1","col2"]]` |
| `WHERE col > 100` | `df[df["col"] > 100]` |
| `WHERE col IN (…)` | `df[df["col"].isin([…])]` |
| `WHERE col IS NULL` | `df[df["col"].isna()]` |
| `ORDER BY col DESC` | `df.sort_values("col", ascending=False)` |
| `LIMIT 10` | `.head(10)` |

The thinking is identical — only the syntax changes. If you can write the Pandas version, you already understand the SQL version.

---

## E. The Same Query Thinking Across All Three Tools

> 💡 **Analogy:** "Where is the restroom?" sounds different in English, Hindi, or sign language — but the intent and the answer are the same. **Query thinking** is the intent; Excel, SQL, and Pandas are just three languages for expressing it.

**One-line definition:** **Query thinking** is the skill of framing a data question as a sequence of filter → select → sort → aggregate steps, independent of which tool you use to execute it.

**The universal pattern:**



**One question — three tools:**

> "What is the total sales per region for orders above ₹1000, sorted by total descending?"

| Tool | How you express it |
|---|---|
| Pandas | `df[df["amount"]>1000].groupby("region")["amount"].sum().sort_values(ascending=False)` |
| SQL | `SELECT region, SUM(amount) FROM orders WHERE amount > 1000 GROUP BY region ORDER BY SUM(amount) DESC` |
| Excel | Filter column `amount > 1000` → Pivot Table: Rows = region, Values = SUM of amount → sort Z→A |

**Practical rule:** Learn the thinking once, then translate to whichever tool is in front of you. In this course, that tool is usually Python — but in a job, it is whatever the team uses.

---

## F. Named Ranges

**One-line definition:** A **named range** labels a cell block for readable formulas (`=SUM(SalesAmount)`).

---

## G. Pivot Tables = groupby

| Pivot | Pandas |
|---|---|
| Rows | `groupby` index |
| Values SUM | `.sum()` |
| Filter | boolean mask |

---

## H. Dashboard Checklist

| Element | Formula / feature |
|---|---|
| KPI total | `=SUM(SalesAmount)` |
| By region | Pivot table |
| Below target | `COUNTIF` + conditional format |

## Reference: VLOOKUP vs XLOOKUP

| Feature | VLOOKUP | XLOOKUP |
|---|---|---|
| Lookup direction | Left column only | Any direction |
| Not found | #N/A | Custom message |
| Syntax complexity | col_index | direct columns |

## Reference: Pivot Table Settings

| Area | Maps to |
|---|---|
| Filters | WHERE |
| Rows | GROUP BY index |
| Values | agg function |

## Reference: COUNTIF Patterns

`=COUNTIF(range, criteria)` — count cells matching rule.

## Reference: Conditional Format Rules

| Rule | Use |
|---|---|
| Color scale | Show magnitude |
| Data bars | Compare within column |
| Icon sets | Traffic-light KPIs |

## Reference: Dashboard Layout

Top: KPIs → Middle: pivot → Bottom: detail table (optional, hidden sheet).

## F. Named Ranges — Readable Formulas

> 💡 **Analogy:** Street names beat grid coordinates for giving directions — **named ranges** label blocks of cells.

**One-line definition:** A **named range** assigns a label to a cell block so formulas read like `=SUM(SalesAmount)`.

| Without names | With names |
|---|---|
| `=SUM(E2:E501)` | `=SUM(SalesAmount)` |
| Fragile when columns move | Stable, self-documenting |

**Create in Excel:** Select data → Formulas → Define Name. Use the name in VLOOKUP, XLOOKUP, and pivot sources.

---

## G. Pivot Tables — Visual groupby

> 💡 **Analogy:** Dragging Region to Rows and Amount to Values is Pandas `groupby('Region')['Amount'].sum()` without code.

**One-line definition:** A **pivot table** summarises a flat table by grouping categories and aggregating numbers.

| Pivot area | Pandas equivalent | SQL equivalent |
|---|---|---|
| Filters | Boolean mask | `WHERE` |
| Rows | `groupby` index | `GROUP BY` |
| Values | `.agg('sum')` | `SUM()` |
| Columns | `unstack` | pivot / `CASE` |

---

## H. Dashboard Assembly — One Sheet, Four KPIs

> 💡 **Analogy:** A car dashboard shows speed and fuel — not every sensor reading. Your sheet shows decision metrics, not every row.

**One-line definition:** A **dashboard** combines KPI cells, pivot output, COUNTIF metrics, and conditional formatting on one view.

| Zone | Content | Tool |
|---|---|---|
| Top-left | Total revenue | `=SUM(SalesAmount)` |
| Top-right | Order count | `=COUNTA(OrderID)` |
| Middle | Region breakdown | Pivot table |
| Highlight | Below-target regions | Conditional formatting |
| Detail | Raw tables | Separate sheet (optional) |

**Session focus:** Spreadsheets only — you learned SQL in Session 15; here you deliver the same insights to Excel-first stakeholders.

## I. Formula Reference

| Formula | Purpose |
|---|---|
| `=VLOOKUP(id, table, col, FALSE)` | Legacy lookup |
| `=XLOOKUP(id, lookup_col, return_col)` | Modern lookup |
| `=COUNTIF(range, criteria)` | Conditional count |
| `=SUMIF(range, criteria, sum_range)` | Conditional sum |

## J. Practice Exercises (continued)

**6. Lookup:** Orders sheet has CustomerID; Customers has City. Write XLOOKUP formula for City.

**7. Pivot:** Build pivot — Rows: Region, Values: SUM Amount, Filter: Status=Completed.

**8. Dashboard:** List four KPI cells you would put on a sales dashboard and why.

**9. Tool choice:** Same question in Pandas — write the groupby line.

**10. Stakeholder:** Why send Excel dashboard instead of Jupyter notebook to a VP?

## Reference Card — Quick Review Before Class

| Section | Core idea | Before-class action |
|---|---|---|
| A | First major concept | Read analogy + definition aloud |
| B | Second concept | Sketch one tiny example |
| C | Third concept | Name one common mistake |
| D | Fourth concept | Link to prior session tool |
| E | Fifth concept | Complete practice #1 |
| F | Extension | Optional stretch |
| G | Extension | Optional stretch |
| H | Extension | Optional stretch |

**Active recall:** Close the doc; write one-line definitions for A, C, E from memory; reopen and check.

**Tool checklist:** Install Jupyter, MySQL Workbench, or Excel/Sheets per session overview.

**Dataset checklist:** Download Superstore or open shared workbook before class.

**Peer prep:** Bring one business question for a dataset in your domain.

**Time box:** 25–35 minutes on this pre-read; finish at least three practice exercises.

## Practice Exercises

**1. Pattern Recognition**  
A colleague sends you an Excel sheet with three worksheets: `Orders`, `Customers`, and `Products`. They want a column in `Orders` that shows each customer's city. Name which Excel function you would use, what the lookup value would be, and how you would do the equivalent in Pandas using one method name.

**2. Concept Detective**  
A VLOOKUP formula returns `#N/A` for about 30% of rows. The lookup column in the source sheet looks correct visually. Name three possible causes and one quick Excel check for each.

**3. Real-Life Application**  
Think of a business report you have seen — a sales dashboard, a school grade sheet, or a sports leaderboard. Describe it in terms of the three query-thinking steps: what filter is applied, which columns are shown, and what aggregation produces the summary number.

**4. Spot the Error**  
A SQL query reads: `SELECT name, city WHERE salary > 50000 FROM employees ORDER BY name`. It errors out immediately. Identify every clause-order mistake and write the corrected query structure in plain words.

**5. Planning Ahead**  
You have an Excel file with 5000 rows of employee data: `emp_id`, `name`, `department`, `salary`, `join_date`, `city`. Plan how you would answer this question using all three tools covered today: "Which departments have an average salary above ₹60,000, sorted highest to lowest?" For each tool, describe the steps — not code or formulas, just the logical actions in order.

**Study note:** Review sections A–H; complete at least three practice exercises before class.


**Study note:** Review sections A–H; complete at least three practice exercises before class.


**Study note:** Review sections A–H; complete at least three practice exercises before class.


**Study note:** Review sections A–H; complete at least three practice exercises before class.


**Study note:** Review sections A–H; complete at least three practice exercises before class.


**Study note:** Review sections A–H; complete at least three practice exercises before class.


**Study note:** Review sections A–H; complete at least three practice exercises before class.


**Study note:** Review sections A–H; complete at least three practice exercises before class.


**Study note:** Review sections A–H; complete at least three practice exercises before class.


**Study note:** Review sections A–H; complete at least three practice exercises before class.


**Study note:** Review sections A–H; complete at least three practice exercises before class.


**Study note:** Review sections A–H; complete at least three practice exercises before class.


**Study note:** Review sections A–H; complete at least three practice exercises before class.


**Study note:** Review sections A–H; complete at least three practice exercises before class.


**Study note:** Review sections A–H; complete at least three practice exercises before class.


**Study note:** Review sections A–H; complete at least three practice exercises before class.

---

> ✅ **You're done!** You analyse data in spreadsheets — lookups, pivots, COUNTIF, dashboards — using the same logic as Pandas. Module 1 complete.
