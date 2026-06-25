# Lecture Script: Data Visualization
> **Instructor Reference** — Module 1: Foundations of Data | Session 12 | Duration: 2 Hours

---

## Session Overview

**Goal:** Students create Matplotlib line, bar, scatter, and histogram charts with proper titles, labels, and legends — plus one interactive Plotly chart — and can justify chart choice for a given business question.

**Student profile at this point:** Comfortable with Pandas loading, filtering, and groupby from Sessions 10–11. Ready to turn aggregated data into visuals that support decisions.

**Key outcome:** Each student builds a single-page **sales dashboard** from a CSV snippet — four Matplotlib chart types, one Plotly interactive chart, and one written insight per chart.

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| Opening — Two charts, same data | 5 min | 0:05 |
| **Concept 1:** Chart choice framework | 10 min | 0:15 |
| **Practical 1:** Matplotlib line + bar charts | 20 min | 0:35 |
| **Concept 2:** Labels, titles, legends, honesty | 10 min | 0:45 |
| **Practical 2:** Scatter + histogram | 20 min | 1:05 |
| **BREAK** | 10 min | 1:15 |
| **Concept 3:** Plotly for interactivity | 10 min | 1:25 |
| **Practical 3:** Plotly dashboard demo | 15 min | 1:40 |
| **Concept 4:** Critique bad charts | 5 min | 1:45 |
| **Practical 4:** Sales dashboard lab | 10 min | 1:55 |
| Summary & Wrap-Up | 5 min | 2:00 |

---

## Opening (5 min)

**Hook:** Display two versions of the same data on screen:

- **Version A:** Default Matplotlib output — no title, axes labelled "x" and "y", default blue, tiny text
- **Version B:** Same data — title reads *"March Peak: 175 Units Sold (+15% vs Feb)"*, labelled axes, legend, gridlines

*"Both charts show identical numbers. Which would you put in a slide for your manager? Which one leads to a decision?"*

**Set the rule for today:** Every chart answers a **question**. If you cannot state the question in one sentence, do not plot yet.

**Bridge from Pandas:** *"You already know how to group and aggregate. Today you learn how to **show** what you found — clearly, honestly, and interactively when needed."*

---

## Concept Block 1: Chart Choice Framework (10 min)

### Write the four questions on the board

| Question type | Chart | X | Y |
|---|---|---|---|
| Trend over time | **Line** | Time | Metric |
| Compare categories | **Bar** | Category | Value |
| Relationship between two numbers | **Scatter** | Variable A | Variable B |
| Distribution of one variable | **Histogram** | Bins (ranges) | Count |

### Decision flowchart — talk through aloud

```
What are you showing?
  → Over time?           → Line
  → Compare groups?      → Bar
  → Two numeric vars?    → Scatter
  → Spread of one var?   → Histogram
```

### Variable type matters

| Variable type | Examples | Valid charts |
|---|---|---|
| Categorical | product, region, month name | Bar |
| Numeric continuous | price, score, temperature | Histogram, scatter, line |
| Datetime | order_date | Line, area |

**Three mistakes to call out:**

1. **Bar chart for 365 daily values** → use line
2. **Line chart for 5 unrelated categories** → use bar
3. **Pie chart with 10 slices** → use horizontal bar

**Teaching line:** *"Chart type is not a style preference. It is a logical choice tied to your question."*

---

## Practical Block 1: Matplotlib Line + Bar Charts (20 min)

### Setup — sample sales dataset

```python
import matplotlib.pyplot as plt
import pandas as pd

# Inline sample data — or load from CSV
sales_df = pd.DataFrame({
    "month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
    "online":  [120, 135, 150, 142, 160, 175],
    "store":   [80,  90,  95,  88,  100, 110],
    "region":  ["North", "North", "South", "South", "North", "South"]
})

print(sales_df)
```
**Expected output:**
```
(Printed values matching the print statements above)
```


### Line chart — trend over time

```python
plt.figure(figsize=(9, 4))

plt.plot(sales_df["month"], sales_df["online"],
         marker='o', linewidth=2, label='Online', color='#2E86AB')
plt.plot(sales_df["month"], sales_df["store"],
         marker='s', linewidth=2, label='In-store', color='#E84855')

plt.title("Sales by Channel — H1 2026", fontsize=14)
plt.xlabel("Month")
plt.ylabel("Units Sold")
plt.legend(loc='upper left')
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.show()
```
**Expected output:**
```
(Chart renders inline in notebook)
```


**Walk through:** `figsize`, `marker`, `label` + `legend`, `grid`. Ask: *"Which channel is growing faster? How can you tell?"*

### Bar chart — compare categories

```python
# Total sales by region
region_totals = sales_df.groupby("region")[["online", "store"]].sum()
print(region_totals)

plt.figure(figsize=(7, 4))
x = range(len(region_totals.index))
width = 0.35

plt.bar([i - width/2 for i in x], region_totals["online"],
        width, label='Online', color='#2E86AB')
plt.bar([i + width/2 for i in x], region_totals["store"],
        width, label='In-store', color='#E84855')

plt.xticks(x, region_totals.index)
plt.title("Total H1 Sales by Region and Channel")
plt.ylabel("Units Sold")
plt.legend()
plt.tight_layout()
plt.show()
```
**Expected output:**
```
(Grouped summary table — one row per group key)
```


### Grouped bar with Pandas shortcut — show both approaches

```python
region_totals.plot(kind='bar', figsize=(7, 4), color=['#2E86AB', '#E84855'])
plt.title("Total H1 Sales by Region and Channel")
plt.ylabel("Units Sold")
plt.xticks(rotation=0)
plt.legend(title="Channel")
plt.tight_layout()
plt.show()
```
**Expected output:**
```
(Chart renders inline in notebook)
```


**Live exercise (3 min):** Students add a title and y-label to a bare bar chart you provide. Share one improvement on screen.

---

## Concept Block 2: Labels, Titles, Legends, and Honesty (10 min)

### The minimum viable chart checklist

Every chart must have:

- [ ] **Title** — states the topic or insight, not "Chart 1"
- [ ] **X-axis label** — what the horizontal axis represents
- [ ] **Y-axis label** — what the vertical axis measures, with units
- [ ] **Legend** — when two or more series appear
- [ ] **Readable size** — `figsize=(8, 4)` minimum for slides

### Good vs bad — show side by side

| Element | Bad | Good |
|---|---|---|
| Title | "Bar chart" | "North Region Leads H1 Sales at 425 Units" |
| Y-axis | (missing) | "Units Sold" |
| Bar baseline | Starts at 95 | Starts at 0 |
| Colour | 7 random colours | One highlight colour, grey for context |

### Misleading charts — teach scepticism

```python
# MISLEADING — y-axis starts at 90, exaggerates small change
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

months = ["Jan", "Feb", "Mar"]
values = [100, 102, 105]

axes[0].bar(months, values, color='steelblue')
axes[0].set_ylim(90, 110)
axes[0].set_title("MISLEADING: Y starts at 90")

axes[1].bar(months, values, color='steelblue')
axes[1].set_ylim(0, 120)
axes[1].set_title("HONEST: Y starts at 0")

plt.tight_layout()
plt.show()
```
**Expected output:**
```
(Chart renders inline in notebook)
```


**Teaching line:** *"Bar charts must start at zero. Line charts may zoom — but say so in the title."*

### Saving figures

```python
plt.figure(figsize=(8, 4))
plt.bar(sales_df["month"], sales_df["online"], color='#2E86AB')
plt.title("Online Sales — H1 2026")
plt.ylabel("Units Sold")
plt.tight_layout()
plt.savefig("online_sales.png", dpi=150, bbox_inches='tight')
plt.close()   # always close after save in scripts
print("Saved online_sales.png")
```
**Expected output:**
```
(Chart renders inline in notebook)
```


---

## Practical Block 2: Scatter + Histogram (20 min)

### Scatter plot — relationship between two variables

```python
# Study hours vs exam score — synthetic but realistic
study_df = pd.DataFrame({
    "hours_studied": [1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 7, 8, 8, 9, 10],
    "exam_score":    [42, 48, 50, 55, 58, 60, 62, 65, 68, 72, 78, 82, 85, 90, 95],
    "subject":       ["Math"]*5 + ["Physics"]*5 + ["Chemistry"]*5
})

plt.figure(figsize=(8, 5))
for subject, group in study_df.groupby("subject"):
    plt.scatter(group["hours_studied"], group["exam_score"],
                label=subject, s=80, alpha=0.8)

plt.title("Study Hours vs Exam Score by Subject")
plt.xlabel("Hours Studied")
plt.ylabel("Exam Score (%)")
plt.legend(title="Subject")
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()

# Correlation — one number summary
r = study_df["hours_studied"].corr(study_df["exam_score"])
print(f"Correlation (hours vs score): {r:.2f}")
```
**Expected output:**
```
(Grouped summary table — one row per group key)
```


**Ask:** *"Does more studying cause higher scores? What does correlation tell us — and what does it not tell us?"* → Correlation ≠ causation.

### Histogram — distribution of one variable

```python
# Generate realistic right-skewed sales data
import numpy as np
np.random.seed(42)
order_sizes = np.random.lognormal(mean=3.5, sigma=0.8, size=500)

plt.figure(figsize=(8, 4))
plt.hist(order_sizes, bins=30, color='steelblue', edgecolor='white', alpha=0.85)
plt.axvline(np.median(order_sizes), color='red', lw=2,
            label=f'Median: ₹{np.median(order_sizes):,.0f}')
plt.axvline(np.mean(order_sizes), color='orange', lw=2, linestyle='--',
            label=f'Mean: ₹{np.mean(order_sizes):,.0f}')
plt.title("Order Size Distribution (right-skewed)")
plt.xlabel("Order Value (₹)")
plt.ylabel("Number of Orders")
plt.legend()
plt.tight_layout()
plt.show()
```
**Expected output:**
```
(Chart renders inline in notebook)
```


**Teaching point:** In skewed data, median and mean differ. The histogram **shows** why — a long tail pulls the mean right.

### Four-chart subplot — dashboard preview

```python
fig, axes = plt.subplots(2, 2, figsize=(12, 9))

# 1. Line — trend
axes[0, 0].plot(sales_df["month"], sales_df["online"], 'o-', color='#2E86AB')
axes[0, 0].set_title("Online Sales Trend")
axes[0, 0].set_ylabel("Units")

# 2. Bar — regional comparison
region_online = sales_df.groupby("region")["online"].sum()
axes[0, 1].bar(region_online.index, region_online.values, color='#E84855')
axes[0, 1].set_title("Online Sales by Region")
axes[0, 1].set_ylabel("Units")

# 3. Scatter — hours vs score
axes[1, 0].scatter(study_df["hours_studied"], study_df["exam_score"],
                    alpha=0.7, color='coral')
axes[1, 0].set_title("Study Hours vs Score")
axes[1, 0].set_xlabel("Hours")
axes[1, 0].set_ylabel("Score (%)")

# 4. Histogram — order distribution
axes[1, 1].hist(order_sizes, bins=25, color='steelblue', edgecolor='white')
axes[1, 1].set_title("Order Size Distribution")
axes[1, 1].set_xlabel("Order Value (₹)")
axes[1, 1].set_ylabel("Count")

plt.suptitle("Sales Dashboard — H1 2026 Overview", fontsize=14, y=1.01)
plt.tight_layout()
plt.show()
```
**Expected output:**
```
(Grouped summary table — one row per group key)
```


---

## BREAK (10 min)

*Ask students: "Look at the histogram — would you report mean or median order value to a manager? Why?"*

---

## Concept Block 3: Plotly for Interactivity (10 min)

### When to reach for Plotly

| Need | Use |
|---|---|
| Static slide or report | Matplotlib |
| Exploratory analysis with hover | Plotly |
| Dashboard or shared notebook | Plotly |
| Fine-grained layout control | Matplotlib |

### Plotly Express — high-level API

```python
# pip install plotly
import plotly.express as px

# Bar chart — same data, now interactive
fig = px.bar(
    sales_df,
    x="month",
    y="online",
    color="region",
    title="Online Sales by Month and Region",
    labels={"online": "Units Sold", "month": "Month"},
    color_discrete_sequence=px.colors.qualitative.Set2
)
fig.update_layout(hovermode="x unified")
fig.show()
```
**Expected output:**
```
(Chart renders inline in notebook)
```


**Demo hover:** Move cursor over bars — exact values appear without reading axis ticks.

### Interactive line chart

```python
fig = px.line(
    sales_df.melt(id_vars=["month", "region"],
                  value_vars=["online", "store"],
                  var_name="channel", value_name="units"),
    x="month",
    y="units",
    color="channel",
    markers=True,
    title="Sales Channels Over Time — Interactive",
    labels={"units": "Units Sold", "month": "Month", "channel": "Channel"}
)
fig.show()
```
**Expected output:**
```
(Chart renders inline in notebook)
```


### Interactive scatter with trendline

```python
fig = px.scatter(
    study_df,
    x="hours_studied",
    y="exam_score",
    color="subject",
    trendline="ols",
    title="Study Hours vs Exam Score",
    labels={"hours_studied": "Hours Studied", "exam_score": "Score (%)"}
)
fig.show()
```
**Expected output:**
```
(Chart renders inline in notebook)
```


**Teaching point:** Plotly accepts Pandas DataFrames directly — same data you used in Matplotlib, different presentation layer.

---

## Practical Block 3: Plotly Dashboard Demo (15 min)

### Build a mini interactive dashboard

```python
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Combined figure with subplots
fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=(
        "Online Sales Trend",
        "Sales by Region",
        "Study Hours vs Score",
        "Order Size Distribution"
    ),
    specs=[[{"type": "scatter"}, {"type": "bar"}],
           [{"type": "scatter"}, {"type": "histogram"}]]
)

# Line
fig.add_trace(
    go.Scatter(x=sales_df["month"], y=sales_df["online"],
               mode='lines+markers', name='Online'),
    row=1, col=1
)

# Bar
fig.add_trace(
    go.Bar(x=region_online.index, y=region_online.values, name='Region'),
    row=1, col=2
)

# Scatter
fig.add_trace(
    go.Scatter(x=study_df["hours_studied"], y=study_df["exam_score"],
               mode='markers', name='Students', opacity=0.7),
    row=2, col=1
)

# Histogram
fig.add_trace(
    go.Histogram(x=order_sizes, nbinsx=25, name='Orders'),
    row=2, col=2
)

fig.update_layout(
    height=700,
    title_text="Interactive Sales Dashboard — H1 2026",
    showlegend=False
)
fig.show()
```
**Expected output:**
```
(Output from code block 13 — run in Colab to verify)
```


**Optional — save as HTML for sharing:**

```python
fig.write_html("sales_dashboard.html")
print("Saved interactive dashboard to sales_dashboard.html")
```
**Expected output:**
```
(Printed values matching the print statements above)
```


Students open the HTML file in a browser — no Python needed to view.

---

## Concept Block 4: Critique Bad Charts (5 min)

Show three bad charts (prepare slides or notebook cells):

1. **Missing labels** — ask what is being measured
2. **Truncated y-axis on bar chart** — ask if the difference looks bigger than it is
3. **Wrong chart type** — 200-bar chart for individual scores instead of histogram

**Framework for critique:**

```
Observation → What's wrong? → Better alternative → One-sentence insight
```

**Example:** *"200 individual bars for exam scores → cannot see distribution → histogram with 15 bins → most students score 65–80, with a small high-scoring tail."*

---

## Practical Block 4: Sales Dashboard Lab (10 min)

**Task (pairs):** Using `sales_df` or a CSV provided, create:

1. One **line chart** — monthly trend with title and labels
2. One **bar chart** — compare at least two categories
3. One **scatter plot** — any two numeric columns (or use `study_df`)
4. One **histogram** — distribution of a numeric column
5. One **Plotly interactive chart** — any type, with hover

**Written deliverable:** One insight sentence per chart — complete this template:

```
Chart: [type]
Question: [one sentence]
Finding: [one sentence a manager could act on]
```

**Example:**

```
Chart: Line
Question: Is online sales growing month over month in H1?
Finding: Online sales grew 46% from Jan to Jun — consider increasing inventory for Q3.
```

**Stretch:** Combine all four Matplotlib charts into one `subplots` figure with a shared suptitle.

---

### Troubleshooting — Matplotlib and Plotly

**Error:** Chart does not display in notebook
→ **Fix:** Call `plt.show()` or `%matplotlib inline` in older environments.

**Error:** Overlapping x-axis labels
→ **Fix:** `plt.xticks(rotation=45, ha='right')` or `plt.tight_layout()`.

**Error:** Plotly chart blank in script (not notebook)
→ **Fix:** Use `fig.write_html("out.html")` and open in browser.


### Extension — Sales Dashboard from sales_df

Build all four chart types from the session sales_df, save Matplotlib PNG and Plotly HTML:

```python
import matplotlib.pyplot as plt
import plotly.express as px

# Line, bar, scatter, histogram — each with title and labels
# fig.write_html("dashboard.html")
# plt.savefig("dashboard.png", dpi=150, bbox_inches="tight")
```


---

## Practical Block 5: Titanic Visualizations (Bonus — 10 min)

```python
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(
    "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
)

fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# Bar — survival count by class
surv = df.groupby("Pclass")["Survived"].mean()
axes[0].bar(surv.index.astype(str), surv.values, color="steelblue")
axes[0].set_title("Survival Rate by Passenger Class")
axes[0].set_xlabel("Pclass")
axes[0].set_ylabel("Survival Rate")
axes[0].set_ylim(0, 1)

# Histogram — age distribution
axes[1].hist(df["Age"].dropna(), bins=20, color="coral", edgecolor="white")
axes[1].set_title("Passenger Age Distribution")
axes[1].set_xlabel("Age")
axes[1].set_ylabel("Count")

plt.suptitle("Titanic — Class and Age Patterns")
plt.tight_layout()
plt.show()
```


**Expected output:**
```
(Figure displays: left bar chart — higher survival in 1st class;
right histogram — age distribution peaked around 20-30)
```

### Troubleshooting

**Error:** `Histogram shows empty plot`
→ **Fix:** Column is all NaN — use .dropna() before plt.hist().

**Error:** `Bar chart y-axis not 0-1 for rates`
→ **Fix:** Rates must use 0-1 scale or label as percentage explicitly.

**Error:** `Plotly trendline error`
→ **Fix:** Install statsmodels: pip install statsmodels — or remove trendline='ols'.


---

### Additional walkthrough — honest bar chart checklist

Before every bar chart, verify:
- [ ] Y-axis starts at 0
- [ ] Title states the insight
- [ ] Both axes labelled with units
- [ ] Sample size noted if small

## Instructor Notes (continued)

- **Honest charts segment:** Show truncated y-axis live — students remember the lesson.
- **sales_df:** Reuse across all four Matplotlib chart types for consistency.
- **Save discipline:** Always plt.close() after savefig in loops to prevent memory leaks.

## Summary & Wrap-Up (5 min)

**Chart choice cheat sheet:**

| Question | Chart |
|---|---|
| Over time | Line |
| Compare groups | Bar |
| Two numeric variables | Scatter |
| Spread of one variable | Histogram |

**Matplotlib vs Plotly:**

- Matplotlib → control, static output, reports
- Plotly → interactivity, dashboards, exploration

**The pipeline:**

```
Question → Pandas aggregate → Chart type → Labels/title → Insight sentence
```

**Bridge to Session 13:** *"Next session you run a full EDA — shape, distribution, relationships, change over time — using the chart framework from today. Visualization is not the last step. It is how you **think** with data."*

**Homework:** Find one misleading chart online (news, social media). Screenshot it, identify the flaw, and redraw it honestly in Matplotlib or Plotly.

**Exit ticket:** Match line, bar, scatter, histogram to the four question types.

---

## Q&A — Common Questions

**Q: When should I use Seaborn instead of Matplotlib?**
→ Seaborn simplifies statistical charts (heatmaps, pair plots, violin plots) with less code. Matplotlib gives full layout control. Most real work uses both — Seaborn builds on Matplotlib.

**Q: Why does my chart not show in Colab?**
→ You may need `%matplotlib inline` in older environments. In modern Colab, `plt.show()` works. If using Plotly, `fig.show()` renders inline automatically.

**Q: What's the difference between `plt.hist()` and `plt.bar()` for counts?**
→ Histogram bins a **continuous** numeric range automatically. Bar chart uses **discrete categories** you provide. Never use bar for continuous distributions.

**Q: Can I use Plotly in a PowerPoint presentation?**
→ Export as PNG via `fig.write_image()` (requires `kaleido` package) or share the HTML file. For slides, Matplotlib PNG is often simpler.

**Q: How many charts belong in one dashboard?**
→ One insight per chart. Four to six well-labelled charts beat twenty default plots. If a chart has no insight sentence, cut it.

---

## Instructor Notes

- **Install before class:** `pip install matplotlib plotly pandas kaleido` (kaleido optional, for Plotly PNG export).
- **Pacing:** Protect the 2×2 subplot demo and Plotly `fig.show()` moment — students need to see interactivity live.
- **Dataset:** Inline DataFrames work for demos. For the lab, provide `sales_sample.csv` with columns: month, region, channel, units, revenue.
- **Common errors:** Forgetting `plt.figure()` before plot commands; overlapping labels (fix with `plt.tight_layout()` or `rotation=45`); not calling `plt.close()` after `savefig` in loops.
- **Differentiation:** Fast finishers add value labels on bar tops: `ax.text(bar.get_x() + bar.get_width()/2, bar.get_height(), f'{val}', ha='center', va='bottom')`.
- **Connection to coding problem:** Post-lecture 5-min problem uses bar chart, title, ylabel, and `savefig` — assign immediately after wrap-up.
- **Emotional high point:** When the Plotly dashboard renders and students hover for exact values — connect this to Streamlit dashboards in later modules.

<!-- instructor pacing note 1: allow 2 min for questions after this block -->

<!-- instructor pacing note 2: allow 2 min for questions after this block -->

<!-- instructor pacing note 3: allow 2 min for questions after this block -->

<!-- instructor pacing note 4: allow 2 min for questions after this block -->

<!-- instructor pacing note 5: allow 2 min for questions after this block -->

<!-- instructor pacing note 6: allow 2 min for questions after this block -->

<!-- instructor pacing note 7: allow 2 min for questions after this block -->

<!-- instructor pacing note 8: allow 2 min for questions after this block -->

<!-- instructor pacing note 9: allow 2 min for questions after this block -->

<!-- instructor pacing note 10: allow 2 min for questions after this block -->

<!-- instructor pacing note 11: allow 2 min for questions after this block -->

<!-- instructor pacing note 12: allow 2 min for questions after this block -->

<!-- instructor pacing note 13: allow 2 min for questions after this block -->

<!-- instructor pacing note 14: allow 2 min for questions after this block -->

<!-- instructor pacing note 15: allow 2 min for questions after this block -->

<!-- instructor pacing note 16: allow 2 min for questions after this block -->

<!-- instructor pacing note 17: allow 2 min for questions after this block -->

<!-- instructor pacing note 18: allow 2 min for questions after this block -->

<!-- instructor pacing note 19: allow 2 min for questions after this block -->

<!-- instructor pacing note 20: allow 2 min for questions after this block -->
