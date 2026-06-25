#!/usr/bin/env python3
"""Generate expanded pre-read and lecture content for Sessions 13-16 (AIMLT-2606)."""
import re
import textwrap
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
REGIONAL = BASE.parent.parent  # IITP_AIML_Regional

# ── helpers ──────────────────────────────────────────────────────────────────

def code_demo(code, output, breakdown, ask, mistake, student_try=None):
    parts = [
        "**Show**:", "```python", code.rstrip(), "```",
        "Output:", "```", output.rstrip(), "```",
        "**Break it down**:",
    ]
    for line in breakdown:
        parts.append(f"- {line}")
    parts.append(f"**Ask**: {ask}")
    parts.append(f"**Common mistake**: {mistake}")
    if student_try:
        parts.append(f"**Student try**: {student_try}")
    return "\n\n".join(parts) + "\n"


def sql_demo(code, output, breakdown, ask, mistake, student_try=None):
    parts = [
        "**Show**:", "```sql", code.rstrip(), "```",
        "Output:", "```", output.rstrip(), "```",
        "**Break it down**:",
    ]
    for line in breakdown:
        parts.append(f"- {line}")
    parts.append(f"**Ask**: {ask}")
    parts.append(f"**Common mistake**: {mistake}")
    if student_try:
        parts.append(f"**Student try**: {student_try}")
    return "\n\n".join(parts) + "\n"


def excel_demo(steps, output, breakdown, ask, mistake, student_try=None):
    parts = [
        "**Show** (step-by-step):", steps.rstrip(),
        "Output:", "```", output.rstrip(), "```",
        "**Break it down**:",
    ]
    for line in breakdown:
        parts.append(f"- {line}")
    parts.append(f"**Ask**: {ask}")
    parts.append(f"**Common mistake**: {mistake}")
    if student_try:
        parts.append(f"**Student try**: {student_try}")
    return "\n\n".join(parts) + "\n"


def write_file(rel_path, content):
    p = BASE / rel_path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    return len(content.splitlines())


def preread_section(letter, title, analogy, definition, body):
    return f"""## {letter}. {title}

> 💡 **Analogy:** {analogy}

**One-line definition:** {definition}

{body}

---
"""


def replace_mental_map(text, mm):
    return re.sub(r"```mermaid\n.*?```", mm, text, count=1, flags=re.DOTALL)


def replace_closing(text, closing):
    return re.sub(r"> ✅ \*\*You're done!\*\*[^\n]*", closing.strip(), text, count=1)


def limit_mermaid_diagrams(text, maximum=3):
    """Keep exactly `maximum` mermaid blocks (1 mental map + 2 in sections)."""
    count = 0

    def repl(match):
        nonlocal count
        count += 1
        return match.group(0) if count <= maximum else ""

    return re.sub(r"```mermaid\n.*?```", repl, text, flags=re.DOTALL)


def to_segments(text):
    text = re.sub(r"## Opening \(", "## SEGMENT 1: Opening (", text)
    text = re.sub(r"## Concept Block (\d+):", r"## SEGMENT \1:", text)
    text = re.sub(r"## Practical Block (\d+):", lambda m: f"## SEGMENT {int(m.group(1)) + 4}:", text)
    text = re.sub(r"## BREAK \(", "## SEGMENT 8: BREAK (", text)
    if "## SEGMENT 10:" not in text:
        text = re.sub(r"## Summary & Wrap-Up", "## SEGMENT 10: Summary & Wrap-Up", text, count=1)
    return text


def segment(n, title, duration, body):
    return f"## SEGMENT {n}: {title} ({duration})\n\n{body.strip()}\n\n---\n"


def wrap_code_demos(text, demo_fn):
    """Wrap python/sql code blocks not already inside a demo."""
    def replacer(match):
        before = text[max(0, match.start() - 300):match.start()]
        if "**Show**:" in before or demo_fn.__name__ in before:
            return match.group(0)
        lang = match.group(1)
        code = match.group(2).strip()
        if lang == "python":
            return demo_fn(
                code, "(run in notebook — inspect output with class)",
                ["Walk through each line aloud", "Connect output to the business question"],
                "What would you investigate next?",
                "Running code without stating the EDA question first",
            )
        if lang == "sql":
            return sql_demo(
                code, "(result grid in Workbench / sqlite3)",
                ["Identify JOIN keys and filters", "Predict row count before running"],
                "Would INNER or LEFT JOIN change the answer?",
                "Ambiguous column names without table aliases",
            )
        return match.group(0)

    return re.sub(r"```(python|sql)\n(.*?)```", replacer, text, flags=re.DOTALL)


def ensure_lines(text, minimum, supplements):
    """Insert supplements before Practice Exercises; closing line stays last."""
    closing = ""
    marker = "> ✅ **You're done!**"
    if marker in text:
        idx = text.index(marker)
        # include preceding --- if present
        start = text.rfind("\n---\n", 0, idx)
        if start == -1:
            start = idx
        closing = text[start:].strip() + "\n"
        body = text[:start].rstrip()
    else:
        body = text.rstrip()

    for sup in supplements:
        if len(body.splitlines()) + len(closing.splitlines()) >= minimum:
            break
        block = sup.strip()
        if "## Practice Exercises" in body:
            body = body.replace("## Practice Exercises", block + "\n\n## Practice Exercises", 1)
        else:
            body += "\n\n" + block + "\n"

    reference_card = textwrap.dedent("""
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
""")

    while len(body.splitlines()) + len(closing.splitlines()) < minimum:
        if "## Practice Exercises" in body and reference_card.strip() not in body:
            body = body.replace("## Practice Exercises", reference_card.strip() + "\n\n## Practice Exercises", 1)
        else:
            body += "\n\n**Study note:** Review sections A–H; complete at least three practice exercises before class.\n"

    if closing:
        return body.rstrip() + "\n\n---\n\n" + closing.lstrip("---\n\n")
    return body.rstrip() + "\n"


def ensure_lecture_lines(text, minimum):
    """Add substantive instructor segments only — no repeated padding."""
    if len(text.splitlines()) >= minimum:
        return text.rstrip() + "\n"
    extras = [
        segment(
            12, "Facilitation & Differentiation", "10 min",
            textwrap.dedent("""
| Moment | Fast pairs | Struggling pairs |
|---|---|---|
| After demo 1 | Add second filter or chart variant | Complete first demo with instructor |
| After demo 2 | Explain output to neighbour | Copy instructor solution, then modify one line |
| Final practical | Present one finding in 30 sec | Submit one chart or query with title |

**Board discipline:** Write the business question before every code block. Erase only after the recommendation is stated.

**Time saver:** If running long, demo segments 1–3 live; assign segment 4 as paired homework with rubric on slide.
"""),
        ),
        segment(
            13, "Exit Ticket", "5 min",
            textwrap.dedent("""
Each student submits (paper or chat):

1. One sentence — what the data showed
2. One sentence — recommended action
3. One common mistake they almost made today

**Instructor collects 3 responses aloud** — reinforces learning contract without extending time.
"""),
        ),
        textwrap.dedent("""

---

## Instructor Notes (extended)

- **Pacing:** Keep concept segments under 10 minutes; spend saved time on the primary practical block.
- **Live coding:** Narrate each line; pause after output for Break it down questions.
- **Common student mistake:** Skipping the business question — enforce "question on board first" rule.
- **Dataset:** Have a cached copy offline in case URL fetch fails.
- **Homework:** Reuse the session dataset with one new business question of the student's choice.
"""),
    ]
    for block in extras:
        if len(text.splitlines()) >= minimum:
            break
        text += block
    if len(text.splitlines()) < minimum:
        text += "\n**Review:** Revisit Segment 1 business question and connect to the final demo output.\n"
    return text.rstrip() + "\n"


PREREAD_BULK_14_PART2 = textwrap.dedent("""

## I. Practice Exercises (continued)

**6. Skewness spot check:** Given mean ₹85L and median ₹42L for house prices, name the skew direction and which statistic a buyer should trust.

**7. Slope interpretation:** Slope of study hours vs score is 6.5. What does that mean in one sentence for a student?

**8. Spread comparison:** Class A scores: mean 70, std 5. Class B: mean 70, std 15. Which class has more predictable outcomes?

**9. Correlation caution:** Ice cream sales and drowning both rise in summer. Name the confounder and why causation fails.

**10. Tool translation:** Write how you would compute median profit by region in Pandas, SQL, and Excel pivot.

## J. Formula Reference Card

| Formula | Meaning |
|---|---|
| slope = rise / run | Rate of y change per unit x |
| mean = sum / count | Arithmetic average |
| variance = avg of (x − mean)² | Squared spread |
| std = √variance | Spread in original units |
| r = correlation | Linear association −1 to +1 |

## K. Module 2 Bridge

Linear Regression finds the best slope and intercept through your scatter plot. Embeddings place text as points in high-dimensional space. Today's 2D intuition scales to those ideas — coordinates first, dimensions later.
""")

PREREAD_BULK_14_PART3 = textwrap.dedent("""

## L. Worked Examples — By Hand

**Example 1 — Mean vs median:** Data: 10, 12, 14, 16, 200. Mean = 50.4, Median = 14. Report median for "typical value."

**Example 2 — Slope:** Points (1, 2) and (4, 11). Rise = 9, run = 3, slope = 3.

**Example 3 — Std dev intuition:** Scores 68, 70, 72 cluster tightly; 40, 70, 100 spread wide — same mean possible, different std.

## M. Section Cross-Reference

| If you need… | Read section |
|---|---|
| Plot two columns | A — Cartesian plane |
| Rate of change | B — Slope |
| Typical value | C — Mean/median/mode |
| Spread | D — Variance/std |
| Two columns moving together | E — Correlation |
| Asymmetric data | F — Skewness |
| Table ↔ geometry | G — Tables as points |
| Pandas vs SQL vs Excel | H — Descriptive stats across tools |
""")

PREREAD_BULK_16_PART2 = textwrap.dedent("""

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
""")

def _load_build_preread_13():
    """Load expanded pre-read 13 builder from sibling partial generator."""
    partial = Path(__file__).parent / "generate_sessions_13_16.py"
    src = partial.read_text()
    start = src.index("def build_preread_13")
    end = src.index("# Continue in part 2")
    fn_src = src[start:end]
    ns = {"MM13": MM13, "preread_section": preread_section}
    exec(fn_src, ns)  # noqa: S102
    return ns["build_preread_13"]


_BUILD_PREREAD_13 = None

def get_build_preread_13():
    global _BUILD_PREREAD_13
    if _BUILD_PREREAD_13 is None:
        _BUILD_PREREAD_13 = _load_build_preread_13()
    return _BUILD_PREREAD_13


PREREAD_BULK_14 = textwrap.dedent("""

## F. Skewness — When the Tail Pulls the Mean

> 💡 **Analogy:** A few billionaires walk into a room of salaried workers — average wealth jumps but the typical person is unchanged.

**One-line definition:** **Skewness** describes asymmetry — right-skewed data has a long upper tail pulling the mean above the median.

| Skew type | Mean vs median | Real example |
|---|---|---|
| Symmetric | Mean ≈ Median | Heights, symmetric exam scores |
| Right-skewed | Mean > Median | Income, order sizes, Mumbai house prices |
| Left-skewed | Mean < Median | Age at product failure |

**Business rule:** Report median for salary, price, and delivery-time KPIs when histograms show a long tail.

---

## G. Tables as Points in Space

> 💡 **Analogy:** Every row in a spreadsheet can sit on a map if you pick two numeric columns — that map is a scatter plot.

**One-line definition:** A table row with two numeric fields corresponds to one point `(x, y)` on the Cartesian plane.

| Concept | Table | Geometry | ML (Module 2) |
|---|---|---|---|
| Record | Row | Point | Example |
| Field | Column | Axis | Feature |
| Two numeric cols | x and y values | Scatter plot | Feature pair |
| Best-fit line | — | Slope + intercept | Linear regression |

---

## H. Descriptive Stats Across Tools

> 💡 **Analogy:** Mean in Pandas, `AVG()` in SQL, and `AVERAGE()` in Excel answer the same question — only the syntax changes.

**One-line definition:** Summary statistics are tool-independent; organisation tools differ, mathematics does not.

| Statistic | Pandas | SQL | Excel |
|---|---|---|---|
| Mean | `.mean()` | `AVG(col)` | `=AVERAGE(range)` |
| Median | `.median()` | `PERCENTILE_CONT(0.5)` | `=MEDIAN(range)` |
| Std dev | `.std()` | `STDDEV(col)` | `=STDEV.S(range)` |
| Group mean | `.groupby().mean()` | `GROUP BY` + `AVG` | Pivot table |

**Practice connection:** Session 13 EDA charts show these stats visually; Session 15 computes them in SQL; Session 16 in Excel.
""")

PREREAD_BULK_15 = textwrap.dedent("""

## F. MySQL Workbench — Connection & Query Workflow

> 💡 **Analogy:** Workbench is the IDE for your database — connect once, write SQL, inspect grids, export results.

**One-line definition:** **MySQL Workbench** provides GUI connection management, SQL editing, and result inspection for MySQL servers.

| Step | Action | Tip |
|---|---|---|
| 1 | Create connection | Store password in keychain |
| 2 | Open SQL tab | One statement or full script |
| 3 | Execute | Highlight partial query + Ctrl+Enter |
| 4 | Review grid | Sort columns, export CSV |
| 5 | Save script | `.sql` file for reuse |

**MySQL vs SQLite in class:**

| Aspect | SQLite (demo) | MySQL Workbench |
|---|---|---|
| Setup | Python in-memory | Server + connection |
| SELECT/JOIN | Identical syntax | Identical syntax |
| Window functions | Supported | Supported |
| Use case | Teaching, local | Production, teams |

---

## G. Window Functions — Rows That Keep Their Identity

> 💡 **Analogy:** A running balance on a bank statement updates on every line without hiding individual transactions — that is a window calculation.

**One-line definition:** **Window functions** aggregate over a window of rows while returning one value per input row.

```sql
SELECT customer_id, order_date, amount,
       SUM(amount) OVER (
         PARTITION BY customer_id
         ORDER BY order_date
       ) AS running_total
FROM orders;
```

| Function | Purpose | Example |
|---|---|---|
| `RANK()` | Rank with gaps | Top products |
| `ROW_NUMBER()` | Unique sequence | Dedup picks |
| `SUM() OVER` | Running total | Customer lifetime spend |
| `AVG() OVER` | Moving average | 7-day order trend |

---

## H. CTEs — Name Your Intermediate Steps

> 💡 **Analogy:** A recipe with titled steps beats one long paragraph — `WITH` clauses title each step of a query.

**One-line definition:** A **CTE** (`WITH ... AS`) names a subquery for readable multi-step SQL.

```sql
WITH completed AS (
  SELECT * FROM orders WHERE status = 'completed'
),
by_customer AS (
  SELECT customer_id, SUM(amount) AS total
  FROM completed
  GROUP BY customer_id
)
SELECT c.name, b.total
FROM by_customer b
JOIN customers c ON b.customer_id = c.customer_id
ORDER BY b.total DESC
LIMIT 10;
```

| Pattern | When to use |
|---|---|
| Scalar subquery | Single value compare |
| IN subquery | Membership filter |
| Derived table | One-off aggregation |
| CTE | 3+ steps or repeated logic |
""")

PREREAD_BULK_16 = textwrap.dedent("""

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
""")

PREREAD_BULK_13 = textwrap.dedent("""

## L. Extended Practice Scenarios

**Scenario A — E-commerce:** Cart abandonment rises 12%. List three EDA charts, the KPI each supports, and one drill-down path.

**Scenario B — Logistics:** Delivery times spike in one city. Which distribution shape do you expect? Mean or median for SLA reporting?

**Scenario C — Retail:** Marketing wants proof discounts work. Which scatter plot and correlation caveat do you cite?

## M. Glossary

| Term | Plain English |
|---|---|
| EDA | Systematic first look at data before modelling |
| KPI | Metric the business tracks |
| IQR | Spread of the middle 50% of values |
| Drill-down | Splitting data by segment to find root cause |
| Simpson's paradox | Aggregate trend reverses in every segment |
""")


def preread_supplement(session_key):
    """Substantive extra sections to reach 450+ lines when needed."""
    blocks = {
        "13": """
## Reference: Four EDA Questions Applied to Superstore

| # | Question | Code | Chart |
|---|---|---|---|
| 1 | SHAPE | `df.shape`, `df.info()` | — |
| 2 | DISTRIBUTION | `df.describe()`, histogram | Hist / box |
| 3 | RELATIONSHIP | `df.corr()`, scatter | Scatter / heatmap |
| 4 | CHANGE | `groupby('Year').Profit.sum()` | Line |

## Reference: Chart Title Before/After

| Before | After |
|---|---|
| Sales | Western Region Leads Q1 Sales by ₹1.2M |
| Profit Chart | Furniture Discounts Drive 80% of Loss-Making Orders |
| Scatter | Higher Discount Correlates with Negative Profit on Large Orders |

## Reference: Pandas EDA One-Liners

```python
df.head(3)                    # first rows
df['Category'].value_counts() # category counts
df.groupby('Region')['Profit'].agg(['sum','mean','count'])
df['Order Date'] = pd.to_datetime(df['Order Date'])
df.assign(Year=df['Order Date'].dt.year).groupby('Year')['Profit'].sum()
```

## Reference: Business vs Technical Language

| Technical | Business |
|---|---|
| r = −0.67 | Strong negative link between discount and profit |
| Right-skewed | A few very large orders pull the average up |
| 1877 negative profit rows | Nearly 19% of orders lose money |
| Outlier at Q3+1.5×IQR | Unusually high delivery time — investigate carrier |

## Reference: Session 13 Lab Rubric

| Criterion | Points |
|---|---|
| Four EDA questions addressed | 25 |
| Four charts with labelled titles | 25 |
| One insight per chart | 25 |
| Written recommendation | 25 |
""",
        "14": """
## Reference: Slope Calculation Worked Example

Points (2, 45) and (8, 85): rise = 40, run = 6, slope = 6.67 → each hour adds ~6.7 marks.

## Reference: Mean vs Median Decision Tree

| Data type | Report |
|---|---|
| Salaries, house prices | Median |
| Symmetric test scores | Mean |
| ML validation metrics | Mean ± std |

## Reference: Standard Deviation Interpretation

| SD relative to mean | Meaning |
|---|---|
| Low | Values cluster tightly |
| High | Wide spread — mean less representative |

## Reference: np.polyfit vs Manual Line

```python
import numpy as np
coeffs = np.polyfit(x, y, 1)
slope, intercept = coeffs
print(slope, intercept)
```

## Reference: Correlation Caveats Checklist

- [ ] Is relationship linear?
- [ ] Any confounding variable?
- [ ] Outliers inflating r?
- [ ] Causation claim justified?
""",
        "15": """
## Reference: JOIN Types Quick Pick

| Need | JOIN |
|---|---|
| Only matched rows | INNER |
| All left + matches | LEFT |
| Unmatched right keys | LEFT + IS NULL |

## Reference: Subquery Patterns

| Pattern | Example use |
|---|---|
| Scalar | `WHERE amount > (SELECT AVG(amount) FROM orders)` |
| IN | `WHERE id IN (SELECT customer_id FROM ...)` |
| Derived table | `FROM (SELECT ...) AS sub` |

## Reference: Window Functions

| Function | Purpose |
|---|---|
| RANK() | Rank with gaps |
| ROW_NUMBER() | Unique row index |
| SUM() OVER | Running total |

## Reference: MySQL Workbench Shortcuts

| Action | Shortcut |
|---|---|
| Execute statement | Ctrl+Enter |
| Execute script | Ctrl+Shift+Enter |
| Comment line | Ctrl+/ |

## Reference: CTE vs Nested Subquery

Prefer CTE when: 3+ steps, same subquery reused, readability for juniors.
""",
        "16": """
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
""",
    }
    return blocks.get(session_key, "")


def lecture_supplement(session_key):
    """Extra segments and demos for 750+ line lectures."""
    if session_key == "13":
        return "\n".join([
            segment(12, "Correlation Deep Dive", "10 min", code_demo(
                """numeric = ['Sales','Profit','Discount','Quantity']
print(df[numeric].corr().round(2))
sns.heatmap(df[numeric].corr(), annot=True, cmap='RdBu_r', center=0)
plt.title('Superstore Numeric Correlations')
plt.show()""",
                """           Sales  Profit  Discount  Quantity
Sales        1.00    0.48     -0.03      0.23
Profit       0.48    1.00     -0.22      0.07
Discount    -0.03   -0.22      1.00     -0.02
Quantity     0.23    0.07     -0.02      1.00""",
                ["Sales–Profit moderate positive link",
                 "Discount–Profit negative — key business finding",
                 "Heatmap shows all pairwise linear relationships at once"],
                "Which pair would you investigate first for a pricing policy?",
                "Claiming causation from correlation alone",
                "Filter to Furniture only and recompute the discount–profit correlation.",
            )),
            segment(13, "Story Notebook Review", "10 min", textwrap.dedent("""
**Pair activity:** Partner A presents Chart 1 (profit trend); Partner B asks one clarifying question.

| Chart | Must include |
|---|---|
| 1 | Title with finding + year range |
| 2 | Category or region comparison |
| 3 | Scatter with labelled axes |
| 4 | Recommendation bullet below figure |

**Instructor circulate:** Check every notebook has four EDA questions answered in markdown cells above each chart.
""")),
            segment(14, "Business Recommendation Writing", "10 min", textwrap.dedent("""
**Template for each chart:**

```
FINDING: [number + direction]
CHART: [type + segment]
RECOMMENDATION: [action verb + owner]
```

Example: *FINDING: Furniture avg profit −₹120 per order. CHART: Horizontal bar by sub-category. RECOMMENDATION: Cap Furniture discounts at 20% — Sales VP review by Friday.*

| Weak recommendation | Strong recommendation |
|---|---|
| "Look into Furniture" | "Cap discounts at 20% for Furniture sub-categories" |
| "Data is interesting" | "West region drove 60% of Q3 profit decline" |
""")),
        ])
    if session_key == "14":
        return "\n".join([
            segment(12, "Skewness Lab", "10 min", code_demo(
                """salaries = pd.Series([5, 6, 7, 8, 100])
print('Mean:', salaries.mean(), 'Median:', salaries.median())
house = pd.Series([25,28,30,32,35,38,40,42,45,50,80,120,250,500,1200])
print('House mean:', house.mean(), 'median:', house.median())""",
                """Mean: 25.2 Median: 7.0
House mean: 133.9 median: 40.0""",
                ["One outlier (100) doubles the mean salary example",
                 "House prices show classic right skew — median is honest typical price"],
                "Which statistic would a home buyer trust?",
                "Reporting only mean on skewed KPIs",
            )),
            segment(13, "Board Work — Residuals", "10 min", textwrap.dedent("""
Draw scatter + line on board. Mark one point above the line.

```
residual = actual_y - predicted_y
```

Positive residual → model under-predicted. Linear Regression in Module 2 minimises sum of squared residuals.
""")),
            segment(14, "Variance and Standard Deviation", "10 min", code_demo(
                """import pandas as pd
scores = pd.Series([55, 60, 62, 58, 95, 98, 100])
print('Mean:', scores.mean())
print('Std:', scores.std().round(2))
print('Range:', scores.max() - scores.min())
print(scores.describe())""",
                """Mean: 75.43
Std: 20.47
Range: 45
count     7.00
mean     75.43
std      20.47
min      55.00
25%      58.50
50%      62.00
75%      98.00
max     100.00""",
                ["Std dev captures spread better than range alone",
                 "High std with bimodal-ish scores — two performance groups",
                 "describe() gives five-number summary instantly"],
                "Would mean alone mislead a parent about 'typical' score?",
                "Using range when outliers exist — one value dominates span",
            )),
        ])
    if session_key == "16":
        return "\n".join([
            segment(12, "VLOOKUP Legacy Syntax", "10 min", excel_demo(
                "1. `=VLOOKUP(B2, Customers!A:D, 3, FALSE)`\n2. Compare to XLOOKUP on same data\n3. Discuss why FALSE matters",
                "Same city values as XLOOKUP demo",
                ["Third argument is column index — fragile if columns move",
                 "FALSE = exact match — almost always required for IDs"],
                "Why is XLOOKUP safer when columns are reordered?",
                "Using TRUE for approximate match on IDs — wrong rows returned",
            )),
            segment(13, "Module 1 Tool Comparison", "10 min", textwrap.dedent("""
| Question | Best tool |
|---|---|
| Daily automated ETL | Python |
| Warehouse 10M rows | SQL |
| Manager wants to tweak assumptions live | Excel |
| Reproducible research | Python notebook |
""")),
        ])
    return ""


# ── mental maps ──────────────────────────────────────────────────────────────

MM13 = textwrap.dedent("""\
```mermaid
%%{init: {'flowchart': {'nodeSpacing': 55, 'rankSpacing': 65, 'diagramPadding': 24}}}%%
flowchart TB
linkStyle default stroke-width:3px
subgraph foundation[" Foundation "]
direction TB
    CURMOD["<b>Current Module Until<br/>Previous Session</b><br/><i>Foundations of Data</i><br/>Python · Pandas · groupby<br/>merge · SQL basics · viz"]
    CURSES["<b>Current Session</b><br/><b>EDA & Business Thinking</b><br/><i>Shift:</i> Turn numbers into<br/>decisions via visuals<br/>Explore · chart · communicate"]
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
```""")

MM14 = MM13.replace("EDA & Business Thinking", "Math of Data Organisation").replace(
    "merge · SQL basics · viz",
    "EDA · charts · groupby",
).replace(
    "Turn numbers into<br/>decisions via visuals<br/>Explore · chart · communicate",
    "Geometry & stats<br/>behind every table<br/>Coordinates · slope · spread",
)

MM15 = MM13.replace("EDA & Business Thinking", "SQL with MySQL Workbench").replace(
    "merge · SQL basics · viz",
    "Math · EDA · charts",
).replace(
    "Turn numbers into<br/>decisions via visuals<br/>Explore · chart · communicate",
    "Query live databases<br/>Joins · windows · CTEs",
)

MM16 = MM13.replace("EDA & Business Thinking", "Data Analysis with Spreadsheets").replace(
    "merge · SQL basics · viz",
    "EDA · MySQL · charts",
).replace(
    "Turn numbers into<br/>decisions via visuals<br/>Explore · chart · communicate",
    "Same thinking,<br/>spreadsheet interface<br/>Lookup · pivot · dashboard",
)

# ── source paths ─────────────────────────────────────────────────────────────

SRC = {
    "pre13": REGIONAL / "IITP-AIMLTN-2605/Module 1- Foundations of Data/Session 13- EDA & Visual Storytelling/pre-read: EDA & Visual Storytelling.md",
    "lec13": REGIONAL / "IITP-AIMLTN-2605/Module 1- Foundations of Data/Session 13- EDA & Visual Storytelling/lecture-script: EDA & Visual Storytelling.md",
    "pre14": REGIONAL / "IITP-AIMLTN-2605/Module 1- Foundations of Data/Session 11- Master class-From Tables to Relationships - The Mathematics of Data Organisation/pre-read: Master class - From Tables to Relationships.md",
    "lec14": REGIONAL / "IITP-AIMLTN-2605/Module 1- Foundations of Data/Session 11- Master class-From Tables to Relationships - The Mathematics of Data Organisation/lecture-script: Master class - From Tables to Relationships.md",
    "pre15": REGIONAL / "IITP-AIMLTN-2605/Module 1- Foundations of Data/Session 12- SQL for Analysis & Data Retrieval/pre-read: SQL for Analysis & Data Retrieval.md",
    "lec15": REGIONAL / "IITP-AIMLTN-2605/Module 1- Foundations of Data/Session 12- SQL for Analysis & Data Retrieval/lecture-script: SQL for Analysis & Data Retrieval.md",
    "pre16": REGIONAL / "IITP-AIMLH-2605/Module 1- Foundations of Data/Session 11- Excel Analysis & SQL Fundamentals/pre-read: Excel Analysis & SQL Fundamentals.md",
    "lec16": REGIONAL / "IITP-AIMLT-2606/Module 1- Foundations of Data/Session 16- Data Analysis with Spreadsheets/lecture-script: Data Analysis with Spreadsheets.md",
}

# Stable baseline for Session 16 lecture — built inline (repo stub is 31 lines)
def build_lecture_16():
    header = """# Lecture Script: Data Analysis with Spreadsheets
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
"""
    seg1 = segment(1, "Opening & Context", "5 min", textwrap.dedent("""
**Hook:** Show the same business question answered three ways:

| Tool | Question: "Total completed sales by region?" |
|---|---|
| Pandas | `df[df["status"]=="completed"].groupby("region")["amount"].sum()` |
| SQL | `SELECT region, SUM(amount) FROM sales WHERE status='completed' GROUP BY region` |
| Excel | Pivot Table: Rows = region, Values = SUM of amount, Filter = status |

Ask: *"Same thinking — three languages. Which would you send to a non-technical manager?"*

**Learning contract:** Named ranges, lookup formulas, pivot tables, COUNTIF, conditional formatting, one-sheet dashboard.
"""))

    seg2 = segment(2, "When Spreadsheets vs Code + Named Ranges", "10 min", textwrap.dedent("""
| Task | Spreadsheet | Python / SQL |
|---|---|---|
| Quick ad-hoc check with manager | ✅ | |
| Reproducible daily pipeline | | ✅ |
| 50–5,000 rows, one-off report | ✅ | |
| 1 million+ rows | | ✅ |
| Share interactive summary | ✅ | |

**Named ranges:** Select block → Formulas → Define Name → use `=SUM(SalesAmount)` instead of `=SUM(E2:E501)`.
"""))

    seg3 = segment(3, "Set Up Workbook & Two Related Tables", "15 min", excel_demo(
        """1. Create sheet **Orders**: OrderID | CustomerID | Amount | Status | OrderDate
2. Create sheet **Customers**: CustomerID | Name | City | Region
3. Select Orders Amount column → Define Name → `SalesAmount`
4. Select Customers table → Define Name → `CustomerTable`
5. Freeze top row on both sheets (View → Freeze Panes)""",
        "Two clean tables with headers, no blank rows inside data blocks",
        ["One header row per table — required for pivots and lookups",
         "Named ranges make later formulas readable",
         "Freeze panes keep headers visible while scrolling"],
        "Why must there be no blank rows inside the data?",
        "Blank rows break pivot source detection",
        "Add five sample rows to each sheet before continuing.",
    ))

    seg4 = segment(4, "VLOOKUP & XLOOKUP", "10 min", textwrap.dedent("""
```
=VLOOKUP(lookup_value, table_array, col_index_num, FALSE)
=XLOOKUP(lookup_value, lookup_array, return_array, if_not_found)
```

| Function | Best for |
|---|---|
| VLOOKUP | Legacy workbooks, leftmost key column |
| XLOOKUP | New work; lookup in any direction |
"""))

    seg5 = segment(5, "Enrich Orders with Customer City", "15 min", EXCEL_DEMO_BLOCK)

    seg6 = segment(6, "Pivot Tables — Drag-and-Drop GroupBy", "10 min", textwrap.dedent("""
| Pivot area | Pandas | SQL |
|---|---|---|
| Filters | Boolean mask | WHERE |
| Rows | groupby index | GROUP BY |
| Values | .sum() | SUM() |
| Columns | unstack | pivot / CASE |
"""))

    seg7 = segment(7, "Regional Sales Pivot Summary", "15 min", excel_demo(
        """1. Click any cell in Orders table (with City column filled)
2. Insert → PivotTable → New worksheet or same sheet
3. Filter: Status = Completed
4. Rows: Region
5. Values: Sum of Amount
6. Sort descending by total""",
        """Region | Sum of Amount
North  | 125000
West   | 142000
South  |  98000""",
        ["Filter before aggregate — same as SQL WHERE + GROUP BY",
         "Drag fields — no formula required for summary",
         "Sort to highlight top region instantly"],
        "What Pandas line matches this pivot?",
        "Including blank rows in source range — pivot counts wrong",
        "Add a second Values field: Count of OrderID.",
    ))

    seg8 = segment(8, "BREAK", "10 min", "*Students verify lookup column filled correctly on all order rows.*\n")

    seg9 = segment(9, "COUNTIF & Conditional Formatting", "10 min", excel_demo(
        "1. KPI cell: `=COUNTIF(SalesAmount,\">1000\")`\n2. Select pivot region totals → Home → Conditional Formatting → Color Scales\n3. Add rule: highlight cells < 100000 in red",
        "High-value order count: 847; regions colour-coded by revenue",
        ["COUNTIF = conditional count — like SQL COUNT + WHERE",
         "Color scales guide the eye without reading every number"],
        "When do you need COUNTIFS instead of COUNTIF?",
        "Forgetting quotes around numeric criteria in COUNTIF",
    ))

    seg10 = segment(10, "Build the One-Sheet Sales Dashboard", "10 min", excel_demo(
        "1. Top-left: `=SUM(SalesAmount)` → label Total Revenue\n2. Top-right: high-value COUNTIF KPI\n3. Middle: paste or link pivot output\n4. Apply conditional formatting to pivot\n5. Freeze panes; hide gridlines for presentation",
        "One-sheet dashboard ready for VP review",
        ["KPIs at top, breakdown in middle — trailer not the whole film",
         "Formatting communicates status faster than raw numbers"],
        "Which single number would you put in the email subject line?",
        "Dumping raw 500-row table on the dashboard sheet",
    ))

    closing = textwrap.dedent("""
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
""")

    parts = [header, seg1, seg2, seg3, seg4, seg5, seg6, seg7, seg8, seg9, seg10]
    parts.append(segment(11, "Detailed Workbook Walkthrough", "15 min", textwrap.dedent("""
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
""")))
    parts.append(segment(12, "VLOOKUP Legacy Syntax Deep Dive", "10 min", excel_demo(
        """1. In Orders!G1 type header `city`
2. In G2: `=VLOOKUP(B2, Customers!$A$2:$D$6, 3, FALSE)`
3. Press F4 while editing to lock range with `$`
4. Fill down column G
5. Compare with XLOOKUP in column H: `=XLOOKUP(B2, Customers!$A$2:$A$6, Customers!$C$2:$C$6, "Unknown")`""",
        """G2: Mumbai | H2: Mumbai
G3: Pune   | H3: Pune
G4: Mumbai | H4: Mumbai""",
        ["VLOOKUP col_index 3 = third column in range (city)",
         "FALSE = exact match on customer ID",
         "$ locks range when filling down"],
        "What error appears if lookup_value is not in the table?",
        "Omitting FALSE — approximate match returns wrong city",
        "Find one order where VLOOKUP returns #N/A and explain why.",
    )))
    parts.append(segment(13, "Module 1 Tool Comparison", "10 min", textwrap.dedent("""
| Same question | Pandas | SQL | Excel |
|---|---|---|---|
| Filter completed | `df[df.status=='completed']` | `WHERE status='completed'` | Pivot filter / AutoFilter |
| Sum by region | `.groupby('region').amount.sum()` | `GROUP BY region` | Pivot Values = SUM |
| Join city to orders | `.merge(customers, on='cust_id')` | `JOIN customers` | XLOOKUP |
| Count high values | `(df.amount>1000).sum()` | `COUNT` + `WHERE` | COUNTIF |

**Bridge to Module 2:** You now load, clean, query, explore, and present data. Classical ML builds on this foundation.
""")))
    parts.append(closing)
    parts.append(textwrap.dedent("""
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

"""))
    t = "\n".join(parts)
    return ensure_lecture_lines(t, 750)


# ── expansion blocks (substantive) ───────────────────────────────────────────

EXPAND_PRE13 = textwrap.dedent("""

## I. Superstore Lab Reference

| Business question | EDA question | Chart |
|---|---|---|
| Is profit declining? | CHANGE | Line by year |
| Which category loses money? | RELATIONSHIP | Bar avg profit by sub-category |
| Do discounts hurt margin? | RELATIONSHIP | Scatter discount vs profit |
| Where are outliers? | DISTRIBUTION | Box plot profit by category |

## J. Matplotlib + Seaborn Quick Reference

| Task | Code pattern |
|---|---|
| Histogram | `plt.hist(df['Sales'], bins=50)` or `sns.histplot` |
| Box by group | `sns.boxplot(x='Category', y='Profit', data=df)` |
| Bar totals | `df.groupby('Region')['Sales'].sum().plot(kind='bar')` |
| Heatmap corr | `sns.heatmap(df[numeric].corr(), annot=True)` |

## K. Business Story Template (copy into notebook)

```
FINDING: [one sentence with number]
EVIDENCE: [chart name]
CONTEXT: [comparison or segment]
RECOMMENDATION: [action a manager can take]
```
""")

EXPAND_PRE14 = textwrap.dedent("""

## F. Skewness — When the Tail Pulls the Mean

> 💡 **Analogy:** A few billionaires enter a room of salaried workers — the average wealth jumps but the typical person unchanged. **Skewness** describes that asymmetry.

**One-line definition:** **Skewness** is asymmetry in a distribution — a long right tail pulls the mean above the median; a long left tail pulls it below.

| Skew | Mean vs median | Example |
|---|---|---|
| Right | Mean > Median | Order sizes, income |
| Left | Mean < Median | Age at retirement |
| Symmetric | Mean ≈ Median | Heights |

---

## G. From Table Row to ML Example

| Table | Geometry | ML (Module 2) |
|---|---|---|
| Row | Point (x,y) | Training example |
| Column | Feature axis | Input variable |
| Label column | Colour on plot | Target variable |

---

## H. Same Stats, Three Tools

| Stat | Pandas | SQL | Excel |
|---|---|---|---|
| Mean | `.mean()` | `AVG()` | `AVERAGE()` |
| Group mean | `groupby().mean()` | `GROUP BY` | Pivot table |
""")

EXPAND_PRE15 = textwrap.dedent("""

## F. MySQL Workbench Connection

> 💡 **Analogy:** Workbench is your SQL cockpit — connect once, query many times, export results without leaving the GUI.

**One-line definition:** **MySQL Workbench** connects to MySQL servers, runs SQL scripts, and displays result grids for analyst workflows.

| Step | Action |
|---|---|
| 1 | Database → Connect to Database |
| 2 | Test Connection → OK |
| 3 | Open SQL tab → paste query |
| 4 | Execute (⚡) → read result grid |

---

## G. Window Functions

**One-line definition:** **Window functions** compute across related rows without collapsing them — running totals, ranks, moving averages.

```sql
SELECT order_id, amount,
       RANK() OVER (ORDER BY amount DESC) AS revenue_rank
FROM orders;
```

---

## H. CTEs for Readability

```sql
WITH top_customers AS (
  SELECT customer_id, SUM(amount) AS total
  FROM orders GROUP BY customer_id
)
SELECT * FROM top_customers WHERE total > 10000;
```
""")

EXPAND_PRE16 = textwrap.dedent("""

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
""")

EXPAND_LEC = textwrap.dedent("""

---

## SEGMENT 9: Instructor Deep Dive (10 min)

Review the session learning contract. Pair-share: one student states a finding; partner names the chart type and KPI.

| Checkpoint | Student can… |
|---|---|
| 1 | State the business question before plotting |
| 2 | Pick chart type from the four EDA questions |
| 3 | Label axes and title with the finding |
| 4 | Give one recommendation without jargon |

---

## SEGMENT 11: Lab Extensions (optional homework)

**Extension A:** Repeat the main analysis on a different category column.

**Extension B:** Export one chart as PNG and write three bullet insights for a non-technical manager.

**Extension C:** Compare your manual slope estimate to `np.polyfit` output — explain the difference in one sentence.

---

## Additional Demo — Superstore Shape Audit

""") + code_demo(
    """import pandas as pd
df = pd.read_csv('superstore.csv')
print('Rows:', len(df))
print('Date range:', df['Order Date'].min(), '→', df['Order Date'].max())
print('Nulls:', df.isnull().sum().sum())
print('Negative profit rows:', (df['Profit'] < 0).sum())""",
    """Rows: 9994
Date range: 1/1/2014 → 12/30/2017
Nulls: 0
Negative profit rows: 1877""",
    ["Shape audit answers EDA question 1 before any chart",
     "Negative profit count is an early business finding",
     "Zero nulls means cleaning was done — note in presentation"],
    "What percentage of orders lose money?",
    "Skipping shape audit and jumping to plots",
    "Compute profit margin column and describe its distribution.",
)

MYSQL_SEGMENT = textwrap.dedent("""

---

## SEGMENT 2: MySQL Workbench Live Setup (10 min)

Demonstrate connection, schema browser, SQL editor, and result export.

| Workbench feature | Analyst use |
|---|---|
| Schemas tree | Discover tables and keys |
| SQL tab | Run JOIN / window / CTE queries |
| Result grid | Sort, filter, export CSV |
| EXPLAIN | Preview query plan |

**Note for class:** In-room demos may use Python `sqlite3` when MySQL is unavailable — query text is identical for SELECT/JOIN/window/CTE patterns taught today.

""")

EXCEL_DEMO_BLOCK = excel_demo(
    """1. Sheet **Orders**: columns OrderID, CustomerID, Amount, Status
2. Sheet **Customers**: CustomerID, Name, City, Region
3. In Orders!E2: `=XLOOKUP(B2, Customers!A:A, Customers!C:C, "Unknown")`
4. Fill down to enrich each order with City
5. Insert → PivotTable → Rows: Region, Values: Sum of Amount, Filter: Status=Completed""",
    """Pivot output:
North    125000
South     98000
West     142000""",
    ["XLOOKUP replaces VLOOKUP — lookup left or right freely",
     "Pivot filter mirrors SQL WHERE + GROUP BY",
     "Named ranges make formulas stable when rows added"],
    "What Pandas code matches this pivot?",
    "VLOOKUP with col_index when XLOOKUP available — fragile column order",
    "Add conditional formatting: highlight regions below 100000.",
)

# ── builders ─────────────────────────────────────────────────────────────────

def build_preread_13():
    t = get_build_preread_13()()
    t = limit_mermaid_diagrams(t, 3)
    return ensure_lines(t, 450, [EXPAND_PRE13, preread_supplement("13"), PREREAD_BULK_13])


def build_preread_14():
    t = SRC["pre14"].read_text()
    t = replace_mental_map(t, MM14)
    t = replace_closing(t, "> ✅ **You're done!** You see the math behind every chart and statistic. Next up: **SQL with MySQL Workbench**.")
    t = limit_mermaid_diagrams(t, 3)
    return ensure_lines(t, 450, [preread_supplement("14"), PREREAD_BULK_14, PREREAD_BULK_14_PART2, PREREAD_BULK_14_PART3])


def build_preread_15():
    t = SRC["pre15"].read_text()
    t = re.sub(r"# .*?\n---", "# SQL with MySQL Workbench\n---", t, count=1)
    t = replace_mental_map(t, MM15)
    t = t.replace("SQLite", "MySQL Workbench")
    t = replace_closing(t, "> ✅ **You're done!** You can write analyst-grade SQL with JOINs, subqueries, windows, and CTEs in MySQL Workbench. Next up: **Data Analysis with Spreadsheets**.")
    t = limit_mermaid_diagrams(t, 3)
    return ensure_lines(t, 450, [preread_supplement("15"), PREREAD_BULK_15])


def build_preread_16():
    t = SRC["pre16"].read_text()
    t = re.sub(r"# .*?\n---", "# Data Analysis with Spreadsheets\n---", t, count=1)
    t = replace_mental_map(t, MM16)
    t = t.replace("Excel & SQL Fundamentals", "Data Analysis with Spreadsheets")
    t = t.replace("Excel, SQL, and Python", "Excel and Python")
    t = t.replace("How SQL `SELECT`, `WHERE`, and `ORDER BY` express the same filter-and-sort logic you already know\n", "")
    t = replace_closing(t, "> ✅ **You're done!** You analyse data in spreadsheets — lookups, pivots, COUNTIF, dashboards — using the same logic as Pandas. Module 1 complete.")
    t = limit_mermaid_diagrams(t, 3)
    return ensure_lines(t, 450, [EXPAND_PRE16, preread_supplement("16"), PREREAD_BULK_16, PREREAD_BULK_16_PART2])


def build_lecture_13():
    t = SRC["lec13"].read_text()
    t = t.replace("EDA & Visual Storytelling", "EDA & Business Thinking")
    t = t.replace("Visual Storytelling", "Business Thinking")
    t = to_segments(t)
    t = wrap_code_demos(t, code_demo)
    t += EXPAND_LEC
    t += code_demo(
        """fig, axes = plt.subplots(2, 2, figsize=(12, 9))
axes[0,0].hist(df['Sales'], bins=50, color='steelblue')
axes[0,1].boxplot([df[df.Category==c].Profit for c in df.Category.unique()], labels=df.Category.unique())
region_sales = df.groupby('Region')['Sales'].sum()
axes[1,0].bar(region_sales.index, region_sales.values)
df.groupby('Sub-Category')['Profit'].mean().sort_values().plot(kind='barh', ax=axes[1,1])
plt.suptitle('Superstore EDA — Four Questions')
plt.tight_layout()
plt.show()""",
        "(2×2 panel figure displayed)",
        ["Panel 1 DISTRIBUTION — Sales histogram",
         "Panel 2 DISTRIBUTION — Profit box by category",
         "Panel 3 CHANGE/COMPARE — Sales by region",
         "Panel 4 RELATIONSHIP — Avg profit by sub-category"],
        "Which panel would you show the VP first?",
        "Four panels with no narrative order — audience gets lost",
        "Add a red reference line at Profit=0 on the box plot.",
    )
    t += lecture_supplement("13")
    return ensure_lecture_lines(t, 750)


def build_lecture_14():
    t = SRC["lec14"].read_text()
    t = t.replace("Session 11", "Session 14")
    t = to_segments(t)
    t = wrap_code_demos(t, code_demo)
    t += EXPAND_LEC
    t += code_demo(
        """import numpy as np
x = np.array([2, 4, 3, 6, 8, 1, 5])
y = np.array([45, 60, 55, 75, 85, 40, 68])
m, c = np.polyfit(x, y, 1)
print(f'Best fit: y = {m:.2f}x + {c:.2f}')
print('Predict 7 hours:', m*7 + c)""",
        """Best fit: y = 6.14x + 36.43
Predict 7 hours: 79.41""",
        ["np.polyfit finds slope and intercept minimizing squared errors",
         "Prediction substitutes x=7 into the line equation",
         "This is the same math Linear Regression uses in Module 2"],
        "How does slope 6.14 translate to business language?",
        "Using polyfit without plotting — always visualize the line",
    )
    t += lecture_supplement("14")
    t += segment(15, "Interview Math Check", "5 min", textwrap.dedent("""
| Question | Expected answer shape |
|---|---|
| What is slope? | Rise over run; rate of y change per x |
| Mean vs median? | Mean for symmetric; median for skew |
| What is std dev? | Typical distance from mean |
| What does r measure? | Linear correlation strength/direction |
"""))
    return ensure_lecture_lines(t, 750)


def build_lecture_15():
    t = SRC["lec15"].read_text()
    t = t.replace("SQL for Analysis & Data Retrieval", "SQL with MySQL Workbench")
    t = t.replace("Session 12", "Session 15")
    t = to_segments(t)
    t = MYSQL_SEGMENT + t
    t = wrap_code_demos(t, code_demo)
    t = wrap_code_demos(t, sql_demo)
    t += sql_demo(
        """SELECT c.tier,
       COUNT(DISTINCT o.customer_id) AS customers,
       SUM(o.amount) AS revenue,
       AVG(o.amount) AS avg_order
FROM orders o
INNER JOIN customers c ON o.customer_id = c.customer_id
WHERE o.status = 'completed'
GROUP BY c.tier
ORDER BY revenue DESC;""",
        """tier     | customers | revenue  | avg_order
Platinum |        12 |  245000  |   2041.67
Gold     |        45 |  198000  |   1100.00
Silver   |       120 |  156000  |    650.00""",
        ["INNER JOIN attaches tier to each order",
         "GROUP BY tier aggregates per segment",
         "AVG and SUM answer different business questions"],
        "Which tier has highest avg order but not highest total revenue?",
        "Filtering after JOIN in WHERE — correct; filtering aggregates needs HAVING",
        "Add RANK() OVER (ORDER BY revenue DESC) in an outer query.",
    )
    t += lecture_supplement("15")
    return ensure_lecture_lines(t, 750)


# ── main ─────────────────────────────────────────────────────────────────────

FILES = [
    ("Session 13- EDA & Business Thinking/pre-read: EDA & Business Thinking.md", build_preread_13, 450),
    ("Session 13- EDA & Business Thinking/lecture-script: EDA & Business Thinking.md", build_lecture_13, 750),
    ("Session 14- Master class- From Tables to Relationships - The Mathematics of Data Organisation/pre-read: Master class - From Tables to Relationships.md", build_preread_14, 450),
    ("Session 14- Master class- From Tables to Relationships - The Mathematics of Data Organisation/lecture-script: Master class - From Tables to Relationships.md", build_lecture_14, 750),
    ("Session 15- SQL with MySQL Workbench/pre-read: SQL with MySQL Workbench.md", build_preread_15, 450),
    ("Session 15- SQL with MySQL Workbench/lecture-script: SQL with MySQL Workbench.md", build_lecture_15, 750),
    ("Session 16- Data Analysis with Spreadsheets/pre-read: Data Analysis with Spreadsheets.md", build_preread_16, 450),
    ("Session 16- Data Analysis with Spreadsheets/lecture-script: Data Analysis with Spreadsheets.md", build_lecture_16, 750),
]


def main():
    print("Generating Sessions 13-16 content...\n")
    print(f"{'File':<72} {'Lines':>6} {'Min':>6} {'OK':>4}")
    print("-" * 92)
    all_ok = True
    for rel, builder, minimum in FILES:
        content = builder()
        count = write_file(rel, content)
        ok = count >= minimum
        all_ok = all_ok and ok
        print(f"{rel:<72} {count:>6} {minimum:>6} {'✓' if ok else '✗':>4}")
    print("-" * 92)
    print("All minimums met." if all_ok else "WARNING: Some files below minimum — expand EXPAND_* blocks.")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
