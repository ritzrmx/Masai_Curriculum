# Spreadsheets: Formulas for Analysis
> **Pre-Read — Academic Session 6** | Module 1: Analytics Foundations + GenAI + Spreadsheets
---
## Mental Map
> 📄 Also provided as a printable PDF in this folder: **mental-map: Formulas for Analysis.pdf**

```mermaid
%%{init: {'theme': 'default', 'themeVariables': { 'fontSize': '12px', 'fontFamily': 'sans-serif' }, 'flowchart': {'htmlLabels': true, 'useMaxWidth': false, 'nodeSpacing': 30, 'rankSpacing': 45, 'padding': 10}}}%%
flowchart LR

START["<b>Course Start</b>"]

subgraph foundation[" WHERE WE ARE "]
direction TB
    CURMOD["<b>CURRENT MODULE</b><br/><i>Module 1: Analytics Foundations + GenAI + Spreadsheets</i><br/>&nbsp;<br/><b>Covered so far:</b> Understanding Data and Averages · Analytics Workflow, Metrics & KPIs · GenAI for Analytics · Clean Up the Data · Make Data Ready for Analysis<br/>This is Session 6 of 41"]
    CURSES["<b>CURRENT SESSION</b><br/><b>Formulas for Analysis</b><br/>&nbsp;<br/><i>The shift:</i> from <i>preparing and validating data</i> to <b>actually calculating business numbers you can trust, using formulas</b><br/>&nbsp;<br/>SUM, AVERAGE, COUNT · Applying formulas across rows/columns<br/>Creating new calculated columns · Simple descriptive analysis"]
end

subgraph outcome[" OUTCOME OF THIS SESSION "]
direction TB
    OUT["<b>By the end, you can…</b><br/>&nbsp;<br/>Apply SUM, AVERAGE, and COUNT correctly across a validated dataset, build new<br/>calculated columns, and use formulas to answer simple descriptive business questions"]
end

subgraph value[" WHY IT MATTERS "]
direction LR
    CVAL["<b>Course Value</b><br/>These are the exact same operations behind SQL's SUM()/AVG()/COUNT(),<br/>Tableau's aggregations, and pandas' .sum()/.mean() — learn the logic once, reuse it everywhere"]
    RVAL["<b>Real-Life Value</b><br/>Quickly calculating total spend, average cost per person, and item<br/>counts when splitting a group trip or event budget"]
end

subgraph future[" WHAT COMES NEXT "]
direction TB
    U0["<b>Next Session</b><br/>Pivot Tables and Quick Insights<br/><i>Summarizing and comparing the same numbers across categories, without writing repeated formulas</i>"]
    U1["<b>Later in Module 1</b><br/>Module 1 wraps up after the next session"]
    U2["<b>Upcoming Modules</b><br/>Module 2: SQL for Data Analysis · Module 3: Tableau Dashboards + Storytelling · Module 4: GenAI Workflows + Python<br/><i>SUM/AVERAGE/COUNT reappear immediately as SQL's aggregation functions in Module 2</i>"]
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

linkStyle default stroke-width:2px
```

## What You'll Learn
In this pre-read, you'll discover:
- How to use the three core formulas — **SUM, AVERAGE, COUNT** — for real business questions
- How to **apply a formula across many rows and columns** without retyping it each time
- How to **create new calculated columns** that don't exist in the raw data
- How to run **simple descriptive analysis** by combining formulas with what you learned in Session 1

---

## A. Core Formulas: SUM, AVERAGE, COUNT

**💡 Analogy:** Think of these three formulas as three different questions you'd ask about a stack of exam papers: "What's the total marks across the class— (SUM), "What's the typical score— (AVERAGE), and "How many papers are there— (COUNT). Same stack, three different, equally useful answers.

**SUM adds values, AVERAGE calculates the mean (Session 1's mean, applied via formula), and COUNT tells you how many entries exist.**

| Formula | What it does | Zappy Mart example |
|---|---|---|
| `=SUM(range)` | Adds all numbers in a range | `=SUM(D2:D8)` → total weekly sales |
| `=AVERAGE(range)` | Calculates the mean of a range | `=AVERAGE(D2:D8)` → average daily sales |
| `=COUNT(range)` | Counts numeric entries in a range | `=COUNT(D2:D8)` → how many days have sales data logged |

**Worked example:** Zappy Mart's Jaipur branch has 7 days of `Sale Amount` data in cells D2:D8. `=SUM(D2:D8)` gives the week's total revenue. `=AVERAGE(D2:D8)` gives the average daily sales — the same mean calculation from Session 1, just done instantly instead of by hand. `=COUNT(D2:D8)` confirms all 7 days actually have data logged (useful as a quick validation check too).

⚠️ **Common trap:** Using `COUNT` when you meant `COUNTA`. `COUNT` only counts numeric cells; if a column has text entries mixed in, `COUNT` silently ignores them — which is sometimes what you want, and sometimes a hidden bug.

---

## B. Applying Formulas Across Rows and Columns

**💡 Analogy:** If you've calculated one classmate's total marks correctly, you don't want to retype that formula 40 times for the whole class — you drag it down once and let it apply the same logic to every row automatically.

**Applying a formula across rows and columns means writing it once, then dragging/copying it so the same logic runs automatically on every relevant row or column.**

**Core explanation:**

| Technique | What it does |
|---|---|
| Fill handle (drag) | Copies a formula down a column or across a row, auto-adjusting cell references |
| Absolute reference (`$`) | Locks a specific cell/range so it doesn't shift when copied (e.g., `$D$1`) |

**Worked example:** Zappy Mart has 5 branches, each with its own weekly total in a `SUM` formula. Instead of typing `=SUM(D2:D8)` for Jaipur, then retyping a near-identical formula for Udaipur, Kanpur, Lucknow, and Indore — write it once for Jaipur, then drag the fill handle across the row (or down a column of branches) to apply it to all five instantly, with the cell references auto-adjusting for each branch's own data.

⚠️ **Common trap:** Dragging a formula that references a fixed value (like a tax rate or a target number) without using `$` to lock it — the reference shifts along with everything else and silently breaks the calculation.

---

## C. Creating New Columns with Formulas

**💡 Analogy:** A raw grocery bill lists item prices — it doesn't automatically show you "price per 100g" unless you calculate it yourself. A new calculated column is exactly that: a value derived from existing columns, not something that existed in the raw data.

**A calculated column uses a formula referencing other columns in the same row to create a brand-new piece of information.**

**Worked example:** Zappy Mart's raw data has `Units Sold` and `Sale Amount (₹)` columns, but not "Average Price per Unit." Create it: `=Sale_Amount / Units_Sold` in a new column, dragged down for every row. This new column didn't exist in the raw export — it's a derived insight built from formulas, and it can now be used in further analysis (e.g., which branch sells at the highest average price per unit).

⚠️ **Common trap:** Dividing by a column that might contain a zero (e.g., a day with zero units sold), which produces a `#DIV/0!` error. Always check for this possibility, especially after Session 2.1/2.2's work on missing/zero values.

---

## D. Descriptive Analysis Using Formulas

**💡 Analogy:** A cricket commentator doesn't just read out scores — they combine numbers into a story: "highest partnership this season," "strike rate above 150 in three of the last five matches." Descriptive analysis is combining simple formulas into small, meaningful comparisons.

**Descriptive analysis means using SUM/AVERAGE/COUNT (and calculated columns) together to describe what the data shows — not yet predicting anything, just summarizing it clearly.**

**Worked example:** Combine formulas to answer: "Which Zappy Mart branch had the highest total weekly sales, and how does its average daily sales compare to the company-wide average— This requires: `SUM` per branch (Section A), applied across all branches (Section B), possibly a calculated column for daily averages (Section C), and then a direct comparison — exactly the kind of descriptive summary a manager would actually want to see.

⚠️ **Common trap:** Reporting a single number (e.g., "total sales: ₹4,20,000") without context. Descriptive analysis is strongest when numbers are compared — against a target, another branch, or a prior period — not reported in isolation.

---

## Quick Reference — Which Formula Do I Need?

| Your situation | Use this | Because |
|---|---|---|
| You need a total | `SUM()` | Adds every value in the range |
| You need a typical value | `AVERAGE()` | Calculates the mean directly |
| You need to know how many entries exist | `COUNT()` (numbers) or `COUNTA()` (any entry) | Confirms data completeness |
| You're repeating the same formula for many rows/branches | **Fill handle + `$` for fixed references** | Saves time and avoids retyping errors |
| You need a value that doesn't exist in the raw data | **Create a calculated column** | Derives new insight from existing columns |
| You want to actually say something meaningful | **Compare numbers, don't report them alone** | A number without context isn't yet an insight |

---

## Practice Exercises

**1. Concept Detective**
A classmate uses `=COUNT(B2:B50)` on a column of `Store City` names and gets 0. Explain why, and what formula they should have used instead.

**2. Pattern Recognition**
Zappy Mart's analyst drags a formula `=D2*$B$1` (where B1 holds a fixed tax rate) down 50 rows, and it works correctly for every row. Explain what the `$` symbols are doing here.

**3. Real-Life Application**
Describe a real spreadsheet you could build (a trip budget, a college fest expense tracker, a personal savings sheet) using at least one SUM, one AVERAGE, and one calculated column.

**4. Spot the Error**
A calculated column `=SaleAmount/UnitsSold` shows `#DIV/0!` in three rows. What's the likely cause, and how should it be handled rather than ignored?

**5. Planning Ahead**
You're asked to summarize "which branch is our best performer" for a manager. List the specific formulas and calculated columns (referring to Sections A-C) you'd combine to answer this with real evidence, not just a guess.

---
> ✅ **You're done!** You can now use SUM, AVERAGE, and COUNT confidently, apply formulas across many rows and columns efficiently, build new calculated columns, and combine formulas into simple descriptive analysis.
Next up: **Pivot Tables and Quick Insights**, where you'll summarize and compare these same numbers across categories — like branch or product — without writing a single repeated formula.
