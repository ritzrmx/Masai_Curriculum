# Lecture Script: Data Analysis with Spreadsheets
> **Instructor Reference** — Module 1: Foundations of Data | Session 16 | Duration: 2 Hours

---

## Session Overview

**Goal:** Students use Excel or Google Sheets to enrich tables with `VLOOKUP`/`XLOOKUP`, summarise data with pivot tables, count with `COUNTIF`, highlight patterns with conditional formatting, and organise ranges with named ranges — building a one-sheet sales dashboard from two related tables without writing Python.

**Student profile at this point:** Fluent in Pandas load/filter/groupby/merge and SQL JOINs from Sessions 10–15. May have used Excel casually but not systematically for analysis.

**Key outcome:** Every student completes a regional sales summary dashboard on a shared workbook — demonstrating that spreadsheet logic mirrors Pandas and SQL, and knowing when each tool fits best.

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| SEGMENT 1: Opening & Context | 5 min | 0:05 |
| SEGMENT 2: When Spreadsheets vs Code + Named Ranges | 10 min | 0:15 |
| SEGMENT 3: Set Up Workbook & Two Related Tables | 15 min | 0:30 |
| SEGMENT 4: VLOOKUP & XLOOKUP | 10 min | 0:40 |
| SEGMENT 5: Enrich Orders with Customer City | 15 min | 0:55 |
| SEGMENT 8: BREAK | 10 min | 1:05 |
| SEGMENT 6: Pivot Tables — Drag-and-Drop GroupBy | 10 min | 1:15 |
| SEGMENT 7: Regional Sales Pivot Summary | 15 min | 1:30 |
| SEGMENT 9: COUNTIF & Conditional Formatting | 10 min | 1:40 |
| SEGMENT 10: Build the One-Sheet Sales Dashboard | 10 min | 1:50 |
| SEGMENT 11: Summary & Module 1 Recap | 5 min | 1:55 |
| Q&A & Instructor Notes | 5 min | 2:00 |

---

## SEGMENT 1: Opening & Context (5 min)

**Hook:** Show the same business question answered three ways:

| Tool | Question: "Total completed sales by region?" |
|---|---|
| Pandas | `df[df["status"]=="completed"].groupby("region")["amount"].sum()` |
| SQL | `SELECT region, SUM(amount) FROM sales WHERE status='completed' GROUP BY region` |
| Excel | Pivot Table: Rows = region, Values = SUM of amount, Filter = status |

Ask: *"Same thinking — three languages. Which would you send to a non-technical manager?"*

**Learning contract:** Named ranges, lookup formulas, pivot tables, COUNTIF, conditional formatting, one-sheet dashboard.

---

## SEGMENT 2: When Spreadsheets vs Code + Named Ranges (10 min)

| Task | Spreadsheet | Python / SQL |
|---|---|---|
| Quick ad-hoc check with manager | ✅ | |
| Reproducible daily pipeline | | ✅ |
| 50–5,000 rows, one-off report | ✅ | |
| 1 million+ rows | | ✅ |
| Share interactive summary | ✅ | |

**Named ranges:** Select block → Formulas → Define Name → use `=SUM(SalesAmount)` instead of `=SUM(E2:E501)`.

---

## SEGMENT 3: Set Up Workbook & Two Related Tables (15 min)

**Show** (step-by-step):

1. Create sheet **Orders**: OrderID | CustomerID | Amount | Status | OrderDate
2. Create sheet **Customers**: CustomerID | Name | City | Region
3. Select Orders Amount column → Define Name → `SalesAmount`
4. Select Customers table → Define Name → `CustomerTable`
5. Freeze top row on both sheets (View → Freeze Panes)

Output:

```

Two clean tables with headers, no blank rows inside data blocks

```

**Break it down**:

- One header row per table — required for pivots and lookups

- Named ranges make later formulas readable

- Freeze panes keep headers visible while scrolling

**Ask**: Why must there be no blank rows inside the data?

**Common mistake**: Blank rows break pivot source detection

**Student try**: Add five sample rows to each sheet before continuing.

---

## SEGMENT 4: VLOOKUP & XLOOKUP (10 min)

```
=VLOOKUP(lookup_value, table_array, col_index_num, FALSE)
=XLOOKUP(lookup_value, lookup_array, return_array, if_not_found)
```

| Function | Best for |
|---|---|
| VLOOKUP | Legacy workbooks, leftmost key column |
| XLOOKUP | New work; lookup in any direction |

---

## SEGMENT 5: Enrich Orders with Customer City (15 min)

**Show** (step-by-step):

1. Sheet **Orders**: columns OrderID, CustomerID, Amount, Status
2. Sheet **Customers**: CustomerID, Name, City, Region
3. In Orders!E2: `=XLOOKUP(B2, Customers!A:A, Customers!C:C, "Unknown")`
4. Fill down to enrich each order with City
5. Insert → PivotTable → Rows: Region, Values: Sum of Amount, Filter: Status=Completed

Output:

```

Pivot output:
North    125000
South     98000
West     142000

```

**Break it down**:

- XLOOKUP replaces VLOOKUP — lookup left or right freely

- Pivot filter mirrors SQL WHERE + GROUP BY

- Named ranges make formulas stable when rows added

**Ask**: What Pandas code matches this pivot?

**Common mistake**: VLOOKUP with col_index when XLOOKUP available — fragile column order

**Student try**: Add conditional formatting: highlight regions below 100000.

---

## SEGMENT 6: Pivot Tables — Drag-and-Drop GroupBy (10 min)

| Pivot area | Pandas | SQL |
|---|---|---|
| Filters | Boolean mask | WHERE |
| Rows | groupby index | GROUP BY |
| Values | .sum() | SUM() |
| Columns | unstack | pivot / CASE |

---

## SEGMENT 7: Regional Sales Pivot Summary (15 min)

**Show** (step-by-step):

1. Click any cell in Orders table (with City column filled)
2. Insert → PivotTable → New worksheet or same sheet
3. Filter: Status = Completed
4. Rows: Region
5. Values: Sum of Amount
6. Sort descending by total

Output:

```

Region | Sum of Amount
North  | 125000
West   | 142000
South  |  98000

```

**Break it down**:

- Filter before aggregate — same as SQL WHERE + GROUP BY

- Drag fields — no formula required for summary

- Sort to highlight top region instantly

**Ask**: What Pandas line matches this pivot?

**Common mistake**: Including blank rows in source range — pivot counts wrong

**Student try**: Add a second Values field: Count of OrderID.

---

## SEGMENT 8: BREAK (10 min)

*Students verify lookup column filled correctly on all order rows.*

---

## SEGMENT 9: COUNTIF & Conditional Formatting (10 min)

**Show** (step-by-step):

1. KPI cell: `=COUNTIF(SalesAmount,">1000")`
2. Select pivot region totals → Home → Conditional Formatting → Color Scales
3. Add rule: highlight cells < 100000 in red

Output:

```

High-value order count: 847; regions colour-coded by revenue

```

**Break it down**:

- COUNTIF = conditional count — like SQL COUNT + WHERE

- Color scales guide the eye without reading every number

**Ask**: When do you need COUNTIFS instead of COUNTIF?

**Common mistake**: Forgetting quotes around numeric criteria in COUNTIF

---

## SEGMENT 10: Build the One-Sheet Sales Dashboard (10 min)

**Show** (step-by-step):

1. Top-left: `=SUM(SalesAmount)` → label Total Revenue
2. Top-right: high-value COUNTIF KPI
3. Middle: paste or link pivot output
4. Apply conditional formatting to pivot
5. Freeze panes; hide gridlines for presentation

Output:

```

One-sheet dashboard ready for VP review

```

**Break it down**:

- KPIs at top, breakdown in middle — trailer not the whole film

- Formatting communicates status faster than raw numbers

**Ask**: Which single number would you put in the email subject line?

**Common mistake**: Dumping raw 500-row table on the dashboard sheet

---

## SEGMENT 11: Detailed Workbook Walkthrough (15 min)

### Orders sheet — enter sample data (instructor types live)

| A: order_id | B: cust_id | C: product | D: region | E: amount | F: status |
|---|---|---|---|---|---|
| O1001 | C01 | Laptop | North | 65000 | completed |
| O1002 | C02 | Chair | South | 12000 | completed |
| O1003 | C01 | Notebook | North | 800 | cancelled |
| O1004 | C03 | Laptop | East | 65000 | completed |
| O1005 | C02 | Laptop | South | 65000 | completed |
| O1006 | C03 | Chair | East | 12000 | cancelled |
| O1007 | C04 | Monitor | West | 15000 | completed |
| O1008 | C02 | Desk | South | 22000 | completed |
| O1009 | C01 | Laptop | North | 65000 | completed |
| O1010 | C05 | Chair | North | 12000 | pending |

**Formatting checklist:** Row 1 bold headers · Insert → Table · Freeze top row · Column E number format.

### Customers sheet

| A: cust_id | B: name | C: city | D: segment |
|---|---|---|---|
| C01 | Alice | Mumbai | Enterprise |
| C02 | Bob | Pune | SMB |
| C03 | Charlie | Mumbai | Enterprise |
| C04 | Diana | Delhi | SMB |
| C05 | Eve | Bangalore | SMB |

**Ask:** *Why separate Orders and Customers instead of one wide table?* → Same as normalised DB / Pandas merge.

---

## SEGMENT 12: VLOOKUP Legacy Syntax Deep Dive (10 min)

**Show** (step-by-step):

1. In Orders!G1 type header `city`
2. In G2: `=VLOOKUP(B2, Customers!$A$2:$D$6, 3, FALSE)`
3. Press F4 while editing to lock range with `$`
4. Fill down column G
5. Compare with XLOOKUP in column H: `=XLOOKUP(B2, Customers!$A$2:$A$6, Customers!$C$2:$C$6, "Unknown")`

Output:

```

G2: Mumbai | H2: Mumbai
G3: Pune   | H3: Pune
G4: Mumbai | H4: Mumbai

```

**Break it down**:

- VLOOKUP col_index 3 = third column in range (city)

- FALSE = exact match on customer ID

- $ locks range when filling down

**Ask**: What error appears if lookup_value is not in the table?

**Common mistake**: Omitting FALSE — approximate match returns wrong city

**Student try**: Find one order where VLOOKUP returns #N/A and explain why.

---

## SEGMENT 13: Module 1 Tool Comparison (10 min)

| Same question | Pandas | SQL | Excel |
|---|---|---|---|
| Filter completed | `df[df.status=='completed']` | `WHERE status='completed'` | Pivot filter / AutoFilter |
| Sum by region | `.groupby('region').amount.sum()` | `GROUP BY region` | Pivot Values = SUM |
| Join city to orders | `.merge(customers, on='cust_id')` | `JOIN customers` | XLOOKUP |
| Count high values | `(df.amount>1000).sum()` | `COUNT` + `WHERE` | COUNTIF |

**Bridge to Module 2:** You now load, clean, query, explore, and present data. Classical ML builds on this foundation.

---


## SEGMENT 11: Summary & Module 1 Recap (5 min)

1. Spreadsheets mirror Pandas/SQL — filter, aggregate, join
2. XLOOKUP / VLOOKUP enrich tables across sheets
3. Pivot tables = drag-and-drop groupby
4. COUNTIF + conditional formatting highlight exceptions
5. Module 1 complete — Module 2 brings Classical ML

---

## Q&A & Doubt Solving (5 min)

**Q: XLOOKUP not available?** → Use VLOOKUP with FALSE; or Google Sheets XLOOKUP.

**Q: Pivot shows wrong totals?** → Check for blank rows and text-formatted numbers.

---

## Instructor Notes

- Demo Excel if available; note Google Sheets equivalents in parentheses.
- Pair students: one writes lookup, one builds pivot, then swap.
- Emphasise spreadsheets for stakeholder delivery, Python/SQL for scale and automation.
- Common pain point: absolute vs relative references when filling formulas — press F4.


---

## SEGMENT 14: SUMIF and Segment KPIs (10 min)

**Show** (step-by-step):

1. On Dashboard — Enterprise revenue: `=SUMIF(Customers!$D:$D,"Enterprise",Orders!$E:$E)` *(requires aligned rows or use helper column)*
2. Better pattern — add `segment` column via XLOOKUP from Customers, then: `=SUMIF(Orders!$H:$H,"Enterprise",Orders!$E:$E)`
3. SMB order count: `=COUNTIF(Orders!$H:$H,"SMB")`
4. Average completed order: `=AVERAGEIF(Orders!$F:$F,"completed",Orders!$E:$E)`

Output:

```
Enterprise revenue: 196800
SMB orders: 4
Avg completed order: 38222
```

**Break it down**:

- SUMIF/COUNTIF/AVERAGEIF = conditional aggregates — SQL WHERE + aggregate in one formula

- Enrich with lookup columns first when tables are normalised

**Ask**: Why is a helper `segment` column cleaner than a 3-sheet SUMIF?

**Common mistake**: SUMIF ranges different lengths — Excel returns #VALUE!

**Student try**: Add KPI cell for count of cancelled orders using COUNTIF.

---

## SEGMENT 15: Google Sheets Equivalents (5 min)

| Excel | Google Sheets |
|---|---|
| Formulas → Define Name | Data → Named ranges |
| Insert → PivotTable | Insert → Pivot table |
| XLOOKUP | XLOOKUP (same syntax) |
| Conditional Formatting | Format → Conditional formatting |
| Ctrl+Enter execute | Same |

**Say:** *Logic is identical — only menu paths differ. Export dashboard as PDF for stakeholders without Excel.*

---

## SEGMENT 16: Troubleshooting Clinic (10 min)

| Symptom | Likely cause | Fix |
|---|---|---|
| #N/A in lookup | ID not in Customers / typo | TRIM spaces; check case |
| Pivot count too high | Blank rows in source | Select Table object, not whole columns |
| SUM shows 0 | Amount stored as text | Text to Columns → General |
| Wrong city after fill | Missing `$` in VLOOKUP range | F4 to lock table_array |
| Chart/Pivot empty | Filter excludes all rows | Clear pivot filters |

**Show** (step-by-step):

1. Select amount column → Data → Text to Columns → Finish (fixes text numbers)
2. Rebuild pivot from Insert → Table source only
3. Re-run XLOOKUP on cleaned IDs

Output:

```
Amount column now numeric — pivot totals match manual SUM
```

**Break it down**:

- Most spreadsheet bugs are data types and range selection — not formula logic

**Ask**: Which issue have you hit most often in real spreadsheets?

**Common mistake**: Deleting #N/A rows instead of fixing the join key

---

## SEGMENT 17: Module 1 Capstone Reflection (10 min)

**Pair activity (8 min):** Each pair picks one Module 1 tool chain for this question:

> *"Which region had the highest completed revenue last quarter, and how does that compare to the prior quarter?"*

| Step | Python | SQL | Excel |
|---|---|---|---|
| Load / connect | `read_csv` / DB | Workbench | Open workbook |
| Filter completed | boolean mask | WHERE | pivot filter |
| Filter quarter | date parse | WHERE date | slicer / filter |
| Aggregate | groupby | GROUP BY | pivot |
| Present | matplotlib / notebook | export CSV | dashboard |

**Share (2 min):** One pair names their preferred tool for a VP vs for a daily pipeline.

**Write on board:** THINKING is shared · TOOLS differ · pick by audience and scale.

---

## SEGMENT 18: Homework — Extend the Dashboard (reference)

**Task:** Starting from today's workbook:

1. Add a `segment` column via XLOOKUP (Enterprise / SMB)
2. Second pivot — Rows: segment, Values: SUM amount, Filter: completed
3. KPI — count of orders above ₹50,000
4. One-sentence recommendation on Dashboard sheet
5. Optional — replicate the same summary in Pandas in 5 lines

**Rubric:**

| Criterion | Points |
|---|---|
| Lookup column correct on all rows | 20 |
| Two pivots or one pivot + segment split | 20 |
| KPI formulas with labels | 20 |
| Conditional formatting applied | 20 |
| Written recommendation | 20 |

---

## SEGMENT 19: Enrich Orders — Full Formula Walkthrough (15 min)

**Show** (step-by-step):

1. Open Orders sheet — confirm `cust_id` column B has values C01–C05
2. Insert column G — header `city`
3. Cell G2: `=XLOOKUP(B2, Customers!$A$2:$A$6, Customers!$C$2:$C$6, "Unknown")`
4. Double-click fill handle (or drag) through row 11
5. Insert column H — header `segment`
6. Cell H2: `=XLOOKUP(B2, Customers!$A$2:$A$6, Customers!$D$2:$D$6, "Unknown")`
7. Fill down column H
8. Spot-check: O1001 → Mumbai, Enterprise · O1002 → Pune, SMB

Output:

```
G2:G11 filled — no #N/A if all cust_ids exist in Customers
H2:H11 shows Enterprise or SMB per order
```

**Break it down**:

- XLOOKUP takes four arguments: key, lookup column, return column, if-not-found

- Separate sheets mirror Pandas `merge(customers, on='cust_id')` done twice for city and segment

- `"Unknown"` prevents blank cells when a new ID appears in Orders before Customers is updated

**Ask**: What Pandas code adds both city and segment columns in one step?

**Common mistake**: Forgetting `$` on lookup range — fill-down shifts Customers range incorrectly

**Student try**: Add column I `customer_name` using XLOOKUP returning column B from Customers.

---

## SEGMENT 20: Pivot Table — Field-by-Field Configuration (15 min)

**Show** (step-by-step):

1. Click any cell inside Orders table (include city/segment columns)
2. **Insert → PivotTable →** choose location: new sheet `Pivot_Region` or Dashboard area
3. **PivotTable Fields pane:**
   - Drag `status` to **Filters** → select only `completed`
   - Drag `region` to **Rows**
   - Drag `amount` to **Values** → ensure **Sum of amount** (not Count)
4. Click dropdown on Row Labels → Sort Z→A by Sum of amount
5. Optional — drag `segment` to **Columns** for region × segment matrix
6. Format numbers: right-click values → Number Format → Currency ₹ no decimals

Output:

```
Filter: status = completed
Rows: North, South, East, West
Values: Sum of amount (sorted high to low)
Optional columns: Enterprise | SMB per region
```

**Break it down**:

- Filter before aggregate = SQL `WHERE status='completed'` before `GROUP BY region`

- Values must be Sum not Count — Count answers "how many orders" not "how much revenue"

- Column field adds second groupby dimension — `groupby(['region','segment'])`

**Ask**: Why does a pivot on the whole column E (not Table) sometimes include a grand total row that double-counts?

**Common mistake**: Leaving `status` in Rows instead of Filters — splits completed/cancelled into separate rows

**Student try**: Duplicate pivot filtered to `Enterprise` segment only; compare North total to full pivot.

---

## SEGMENT 21: Dashboard Layout — Cell-by-Cell Build (15 min)

**Show** (step-by-step):

1. Create sheet **Dashboard** — hide gridlines (View → uncheck Gridlines)
2. **A1:** label `Total Completed Revenue` · **B1:** `=SUMIF(Orders!$F:$F,"completed",Orders!$E:$E)`
3. **A2:** label `High-Value Orders (>₹50K)` · **B2:** `=COUNTIFS(Orders!$F:$F,"completed",Orders!$E:$E,">50000")`
4. **A3:** label `Top Region` · **B3:** `=INDEX(PivotRange, MATCH(MAX(PivotRange), PivotRange, 0))` *(or type from pivot)*
5. Rows 5–10: paste pivot output (Paste Values — not formulas — so layout is stable)
6. Select pivot values → **Home → Conditional Formatting → Color Scales → Green-Yellow-Red**
7. Add **Insert → Text Box:** *"Recommendation: West leads revenue — replicate North campaign playbook in Q2."*
8. **View → Freeze Panes** below row 4 so KPIs stay visible when scrolling

Output:

```
Dashboard shows 3 KPI cells, colour-coded region table, one recommendation sentence
Ready to PDF-export or present in 30-second readout
```

**Break it down**:

- SUMIF/COUNTIFS restrict KPIs to completed orders — same business rule as SQL WHERE

- Paste Values decouples dashboard from pivot refresh errors during presentation

- Text box recommendation completes Session 13 business-thinking pipeline

**Ask**: Which KPI would you put in the email subject line to a VP?

**Common mistake**: Linking dashboard cells directly to pivot cells that move when pivot refreshes

**Student try**: Add conditional rule — red fill if any region total is below ₹100,000.

---

## SEGMENT 22: Absolute vs Relative References — F4 Drill (10 min)

**Show** (step-by-step):

1. In empty column write `=B2` — fill down — references shift B3, B4… *(relative)*
2. Rewrite `=$B$2` — fill down — all rows point to B2 *(absolute)*
3. VLOOKUP pattern: `=VLOOKUP(B2, $A$2:$D$6, 3, FALSE)` — only lookup_value shifts per row
4. Press **F4** while cursor is in a reference to cycle: A1 → $A$1 → A$1 → $A1

Output:

```
Row 2: looks up B2 in fixed table A2:D6
Row 3: looks up B3 in same fixed table
```

**Break it down**:

- Relative = changes when copied · Absolute = locked with `$`

- Lookup formulas almost always need absolute table_array

**Ask**: What breaks if you copy VLOOKUP without locking the Customers range?

**Common mistake**: Mixing relative table range — row 10 looks up in wrong rows of Customers

---

## SEGMENT 23: Module 1 Journey Recap (5 min)

| Session | Skill | Tool |
|---|---|---|
| 1–8 | Python, data structures, files | Jupyter |
| 9–11 | NumPy, Pandas load/filter/groupby | Jupyter |
| 12 | Charts | Matplotlib |
| 13 | EDA + business thinking | Jupyter |
| 14 | Math behind stats | Jupyter + board |
| 15 | SQL joins, windows, CTEs | MySQL Workbench |
| 16 | Spreadsheets for stakeholders | Excel / Sheets |

**Say:** *You can now go from raw data to a decision in Python, SQL, or Excel — pick the tool your audience needs.*

---

## SEGMENT 24: Google Sheets Export & Share (5 min)

**Show** (step-by-step):

1. **File → Share →** restrict edit access to analysts; view access for managers
2. **File → Download → PDF** for email attachment
3. In Google Sheets: **File → Publish to web** (single sheet) for read-only link
4. Note version history if stakeholders change formulas accidentally

Output:

```
PDF dashboard attached to email — VP reads KPIs without opening Excel
```

**Break it down**:

- Spreadsheets are communication tools — sharing settings matter as much as formulas

**Ask**: When would you send Python notebook instead of PDF?

**Common mistake**: Sharing edit link with entire company — someone breaks a formula silently

---

## SEGMENT 25: Practice Data — Copy-Paste Starter Tables (reference)

**Orders (paste into A1):**

```
order_id,cust_id,product,region,amount,status
O1001,C01,Laptop,North,65000,completed
O1002,C02,Chair,South,12000,completed
O1003,C01,Notebook,North,800,cancelled
O1004,C03,Laptop,East,65000,completed
O1005,C02,Laptop,South,65000,completed
O1006,C03,Chair,East,12000,cancelled
O1007,C04,Monitor,West,15000,completed
O1008,C02,Desk,South,22000,completed
O1009,C01,Laptop,North,65000,completed
O1010,C05,Chair,North,12000,pending
```

**Customers (paste into A1 on second sheet):**

```
cust_id,name,city,segment
C01,Alice,Mumbai,Enterprise
C02,Bob,Pune,SMB
C03,Charlie,Mumbai,Enterprise
C04,Diana,Delhi,SMB
C05,Eve,Bangalore,SMB
```

**Instructor tip:** Provide this CSV block in chat so students who fall behind can paste and catch up in under 2 minutes.

---

## SEGMENT 12: Facilitation & Differentiation (10 min)

| Moment | Fast pairs | Struggling pairs |
|---|---|---|
| After demo 1 | Add second filter or chart variant | Complete first demo with instructor |
| After demo 2 | Explain output to neighbour | Copy instructor solution, then modify one line |
| Final practical | Present one finding in 30 sec | Submit one chart or query with title |

**Board discipline:** Write the business question before every code block. Erase only after the recommendation is stated.

**Time saver:** If running long, demo segments 1–3 live; assign segment 4 as paired homework with rubric on slide.

---
## SEGMENT 13: Exit Ticket (5 min)

Each student submits (paper or chat):

1. One sentence — what the data showed
2. One sentence — recommended action
3. One common mistake they almost made today

**Instructor collects 3 responses aloud** — reinforces learning contract without extending time.

---


---

## Instructor Notes (extended)

- **Pacing:** Keep concept segments under 10 minutes; spend saved time on the primary practical block.
- **Live coding:** Narrate each line; pause after output for Break it down questions.
- **Common student mistake:** Skipping the business question — enforce "question on board first" rule.
- **Dataset:** Have a cached copy offline in case URL fetch fails.
- **Homework:** Reuse the session dataset with one new business question of the student's choice.

**Homework:** Extend the dashboard with segment pivot and written recommendation — rubric on slide.

**Final check:** Every student shows one XLOOKUP and one pivot field configuration before leaving.

**Module 1 complete:** Students can load, clean, query, explore, and present data in Python, SQL, and Excel — ready for Classical ML in Module 2.

**Celebration moment:** Ask class to name one Module 1 skill they will use in their first week on a job — write answers on sticky notes for wall display.

**Q&A reminder:** Leave 5 minutes for XLOOKUP vs pivot troubleshooting questions before dismissing.
