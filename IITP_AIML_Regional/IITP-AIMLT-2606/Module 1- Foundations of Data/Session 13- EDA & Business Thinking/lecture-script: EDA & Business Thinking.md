# Lecture Script: EDA & Business Thinking
> **Instructor Reference** — Module 1: Foundations of Data | Session 13 | Duration: 2 Hours

---

## Session Overview

**Goal:** Students conduct a complete Exploratory Data Analysis (EDA) on a real dataset — discovering shape, distribution, relationships, and outliers — and then translate findings into clean, labelled charts that tell a story a business audience can act on.

**Student profile at this point:** Comfortable with Pandas cleaning, groupby, and basic Matplotlib. This session adds structure and intent to their visualisation work.

**Key outcome:** Students complete a guided EDA on the Superstore dataset and produce 4 publication-ready charts with titles, labels, and one-line insights — in a single Jupyter notebook.

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| Opening — What Is EDA and Why Does It Come First? | 5 min | 0:05 |
| **Concept 1:** The EDA Framework — 4 Questions Before Any Chart | 10 min | 0:15 |
| **Practical 1:** Dataset audit, describe(), distributions | 15 min | 0:30 |
| **Concept 2:** Chart Types — Match the Chart to the Question | 10 min | 0:40 |
| **Practical 2:** Histograms, boxplots, bar charts | 15 min | 0:55 |
| **BREAK** | 10 min | 1:05 |
| **Concept 3:** Relationships — Correlation, Scatter, Heatmap | 10 min | 1:15 |
| **Practical 3:** Scatter plots, correlation matrix, heatmap | 15 min | 1:30 |
| **Concept 4:** Storytelling with Data — Chart polish and annotation | 10 min | 1:40 |
| **Practical 4:** Build the 4-chart "story" notebook | 10 min | 1:50 |
| Summary & Wrap-Up | 5 min | 1:55 |
| Q&A & Doubt Solving | 5 min | 2:00 |

---

## SEGMENT 1: Opening (5 min)

**Hook:** Show two versions of the same chart on screen:
- Version A: A plain default matplotlib bar chart, no labels, no title, default blue
- Version B: The same chart with a clear title ("Q1 2025: Mumbai Led Regional Sales by ₹1.2M"), axis labels, readable colours, and a one-line annotation pointing to the peak

*"Both charts show identical data. Which one would you show to your manager? Which one would you act on?"*

**What EDA is NOT:**
- Making pretty charts first, then finding questions to ask
- Running `df.describe()` and calling it done
- Confirming what you already expect to see

**What EDA IS:**
- A systematic process of asking questions and using data to answer them
- Discovering what the data *actually contains* vs what you were told it contains
- Finding surprising things — outliers, unexpected correlations, missing segments — before they embarrass you in a presentation

---

## SEGMENT 1: The EDA Framework — 4 Questions (10 min)

### The Four EDA Questions (write on board)

```
1. SHAPE    — What does this data contain?
             (rows, columns, types, nulls, duplicates)

2. DISTRIBUTION — What does each column look like?
             (min/max, mean/median, skew, outliers, unique values)

3. RELATIONSHIP — Do variables move together?
             (correlation, scatter patterns, category breakdowns)

4. CHANGE    — Does anything vary over time or across groups?
             (trends, seasonality, segment differences)
```

**The EDA process never starts with a chart. It starts with a question.**

Always write the question first: *"Which product category has the highest profit margin?"* THEN choose the chart. Never the reverse.

### The EDA Mindset

| After seeing each output, ask: | What to do |
|---|---|
| "That seems high/low" | Drill down — why? Is it an error or reality? |
| "That's what I expected" | Good — document it and move on |
| "That's surprising" | This is a finding — investigate further |
| "I don't understand this column" | Clarify with the data owner before analysis |

---

## SEGMENT 5: Dataset Audit + Distributions (15 min)

### Dataset — Superstore Sales (use a realistic subset)

**Show**:

```python

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the Superstore dataset
# Download from: https://www.kaggle.com/datasets/vivek468/superstore-dataset-final
# Or use this representative subset:
url = 'https://raw.githubusercontent.com/dsrscientist/dataset1/master/superstore.csv'
try:
    df = pd.read_csv(url)
except:
    # Fallback: load from local file
    df = pd.read_csv('superstore.csv')

# Quick shape + types
print("Shape:", df.shape)
print("\nColumn types:")
print(df.dtypes)
print("\nNull counts:")
print(df.isnull().sum())

```

Output:

```

(run in notebook — inspect output with class)

```

**Break it down**:

- Walk through each line aloud

- Connect output to the business question

**Ask**: What would you investigate next?

**Common mistake**: Running code without stating the EDA question first


**Show**:

```python

# --- Question 1: Shape audit ---
print("=== SHAPE ===")
print(f"Rows: {len(df):,}")
print(f"Columns: {df.shape[1]}")
print(f"Date range: {df['Order Date'].min()} → {df['Order Date'].max()}")
print(f"Unique customers: {df['Customer ID'].nunique():,}")
print(f"Unique products: {df['Product ID'].nunique():,}")

# --- Question 2: Numeric distributions ---
print("\n=== DISTRIBUTIONS ===")
print(df[['Sales', 'Profit', 'Discount', 'Quantity']].describe().round(2))

```

Output:

```

(run in notebook — inspect output with class)

```

**Break it down**:

- Walk through each line aloud

- Connect output to the business question

**Ask**: What would you investigate next?

**Common mistake**: Running code without stating the EDA question first


**Live walk-through:** Look at the `describe()` output together. Call out:
- Is `Profit` min negative? → Yes — some items sold at a loss. This is a finding.
- Is `Discount` max = 1? → Full discounts exist. Why?
- What is the spread between 25th and 75th percentile of Sales? → High variance.

---

## SEGMENT 2: Chart Types — Match the Chart to the Question (10 min)

### The Decision Framework

| Question type | Best chart | When NOT to use it |
|---|---|---|
| Distribution of one numeric column | Histogram, KDE | When categories are more important than range |
| Spread + outliers of one column | Box plot | When distribution shape matters |
| Compare a metric across categories | Bar chart | When there are 20+ categories (use a table) |
| Two numeric variables — relationship | Scatter plot | When one variable is categorical |
| Many variables — correlation matrix | Heatmap | When there are < 3 variables (just use scatter) |
| A metric over time | Line chart | When time intervals are irregular and sparse |
| Part of a whole | Stacked bar / pie | Pie charts only for 2-3 slices |

**The three most common EDA mistakes:**

1. **Using a bar chart for distribution** — use histogram instead; bars imply categories
2. **Skipping the y-axis label** — "what are those numbers?" makes the chart useless
3. **Plotting too many lines/bars** — more than 5–7 categories on one chart = unreadable

---

## SEGMENT 6: Histograms, Boxplots, Bar Charts (15 min)

**Show**:

```python

fig, axes = plt.subplots(2, 2, figsize=(12, 9))

# --- 1. Histogram: Sales distribution ---
axes[0, 0].hist(df['Sales'], bins=50, color='steelblue', edgecolor='white')
axes[0, 0].axvline(df['Sales'].median(), color='red', lw=2, label=f"Median: ${df['Sales'].median():.0f}")
axes[0, 0].set_title('Sales Distribution (right-skewed)', fontsize=12)
axes[0, 0].set_xlabel('Order Sales ($)')
axes[0, 0].set_ylabel('Frequency')
axes[0, 0].legend()

# --- 2. Box plot: Profit by Category ---
categories = df['Category'].unique()
profit_data = [df[df['Category'] == cat]['Profit'].values for cat in categories]
axes[0, 1].boxplot(profit_data, labels=categories, patch_artist=True,
                    boxprops=dict(facecolor='lightblue'))
axes[0, 1].axhline(0, color='red', lw=1, linestyle='--', label='Break-even')
axes[0, 1].set_title('Profit by Category (note: negatives exist)', fontsize=12)
axes[0, 1].set_ylabel('Profit ($)')
axes[0, 1].legend()

# --- 3. Bar chart: Total Sales by Region ---
region_sales = df.groupby('Region')['Sales'].sum().sort_values(ascending=False)
bars = axes[1, 0].bar(region_sales.index, region_sales.values, color='coral', edgecolor='white')
axes[1, 0].set_title('Total Sales by Region', fontsize=12)
axes[1, 0].set_ylabel('Total Sales ($)')
# Add value labels on top of bars
for bar, val in zip(bars, region_sales.values):
    axes[1, 0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2000,
                     f'${val/1000:.0f}K', ha='center', va='bottom', fontsize=9)

# --- 4. Bar chart: Avg Profit by Category + Sub-Category (top 10) ---
sub_profit = df.groupby('Sub-Category')['Profit'].mean().sort_values()
colors = ['red' if x < 0 else 'steelblue' for x in sub_profit.values]
sub_profit.plot(kind='barh', ax=axes[1, 1], color=colors)
axes[1, 1].axvline(0, color='black', lw=1)
axes[1, 1].set_title('Avg Profit by Sub-Category\n(red = loss-making)', fontsize=12)
axes[1, 1].set_xlabel('Avg Profit ($)')

plt.suptitle('Superstore EDA — Overview', fontsize=14, y=1.02)
plt.tight_layout()
plt.show()

```

Output:

```

(run in notebook — inspect output with class)

```

**Break it down**:

- Walk through each line aloud

- Connect output to the business question

**Ask**: What would you investigate next?

**Common mistake**: Running code without stating the EDA question first


**After displaying:** Walk through each panel. Point to the loss-making sub-categories. *"If you were the VP of Sales, which one sub-category would you investigate immediately?"*

---

## SEGMENT 8: BREAK (10 min)

*Ask students to look at the box plot for Furniture profit — there are negative outliers. Where do they come from? They will investigate after the break.*

---

## SEGMENT 3: Relationships — Correlation, Scatter, Heatmap (10 min)

### Correlation — What It Measures

**Pearson correlation coefficient (r):**
- Measures linear relationship between two numeric variables
- Range: -1 (perfect negative) to +1 (perfect positive)
- 0 = no linear relationship (but could have a non-linear one)

**Critical caveats to teach:**
1. **Correlation ≠ causation.** Ice cream sales and drowning rates are both high in summer (confounded by heat). Correlation is a clue, not a conclusion.
2. **Only detects LINEAR relationships.** A U-shaped relationship (e.g., too little or too much discount both hurt profit) might show r ≈ 0.
3. **Sensitive to outliers.** One extreme point can pull r significantly.

### The Correlation Matrix

A correlation matrix computes r for every pair of numeric columns — displayed as a colour-coded grid (heatmap) where:
- Dark red = strong positive
- Dark blue = strong negative
- White/light = no relationship

---

## SEGMENT 7: Scatter, Correlation, Heatmap (15 min)

**Show**:

```python

import numpy as np

# --- Q: Does higher discount always mean lower profit? ---
plt.figure(figsize=(8, 5))
scatter = plt.scatter(df['Discount'], df['Profit'],
                       c=df['Sales'], cmap='viridis',
                       alpha=0.4, s=30)
plt.colorbar(scatter, label='Order Sales ($)')
plt.axhline(0, color='red', lw=1, linestyle='--')
plt.xlabel('Discount Rate')
plt.ylabel('Profit ($)')
plt.title('Discount vs Profit — Coloured by Sales Volume\nHigher discount = more losses')
print("Correlation (Discount vs Profit):", df['Discount'].corr(df['Profit']).round(3))
plt.show()

```

Output:

```

(run in notebook — inspect output with class)

```

**Break it down**:

- Walk through each line aloud

- Connect output to the business question

**Ask**: What would you investigate next?

**Common mistake**: Running code without stating the EDA question first


**Show**:

```python

# --- Correlation matrix of numeric columns ---
numeric_cols = ['Sales', 'Profit', 'Discount', 'Quantity']
corr_matrix = df[numeric_cols].corr()

plt.figure(figsize=(6, 5))
sns.heatmap(corr_matrix,
            annot=True, fmt='.2f',
            cmap='RdBu_r', center=0,
            square=True, linewidths=0.5)
plt.title('Correlation Matrix\n(Discount → negative profit relationship is clear)')
plt.tight_layout()
plt.show()

print("Interpretation:")
print("Sales vs Profit:", corr_matrix.loc['Sales','Profit'].round(3), "(positive but weak)")
print("Discount vs Profit:", corr_matrix.loc['Discount','Profit'].round(3), "(negative!)")

```

Output:

```

(run in notebook — inspect output with class)

```

**Break it down**:

- Walk through each line aloud

- Connect output to the business question

**Ask**: What would you investigate next?

**Common mistake**: Running code without stating the EDA question first


**Show**:

```python

# --- Group-level analysis: Profit margin by segment and category ---
pivot = df.pivot_table(
    values='Profit',
    index='Segment',
    columns='Category',
    aggfunc='mean'
).round(1)

plt.figure(figsize=(7, 4))
sns.heatmap(pivot, annot=True, fmt='.1f', cmap='RdYlGn', center=0)
plt.title('Average Profit by Segment × Category')
plt.tight_layout()
plt.show()

```

Output:

```

(run in notebook — inspect output with class)

```

**Break it down**:

- Walk through each line aloud

- Connect output to the business question

**Ask**: What would you investigate next?

**Common mistake**: Running code without stating the EDA question first


---

## SEGMENT 4: Storytelling with Data (10 min)

### What Makes a Chart "Tell a Story"?

A chart is not a story until it has:

| Element | Bad | Good |
|---|---|---|
| Title | "Bar chart" | "Western Region Leads Sales; Tables Category Drags Profits" |
| Axis labels | "x", "y" | "Order Sales ($)" / "Number of Orders" |
| Annotation | None | Arrow pointing to outlier with "Chairs: -$2,400 avg profit" |
| Colour | 7 different colours | One colour with one highlight to draw the eye |
| Conclusion | "Here is the data" | "Recommendation: review discount policy for Furniture" |

### The Chart → Insight → Recommendation Pipeline

```
Observation:    "Furniture has the most negative profit outliers"
     ↓
Context:        "Average discount on Furniture is 35% vs 15% for Tech"
     ↓
Insight:        "Deep discounts on Furniture destroy margins"
     ↓
Recommendation: "Cap Furniture discounts at 20%; review pricing on Tables sub-category"
```

Every chart you build should be able to complete this pipeline. If it can't, the chart is not analysis — it's decoration.

---

## SEGMENT 8: The 4-Chart Story Notebook (10 min)

**Task:** Build the final notebook. Assign to pairs. One person narrates the finding, one writes the code.

**Business question for the story:**
> *"Our profit is declining. Where is the problem, and what should we do about it?"*

**Chart 1:** Profit trend over time (line chart — is profit declining year over year?)

**Show**:

```python

df['Order Date'] = pd.to_datetime(df['Order Date'])
df['Year'] = df['Order Date'].dt.year
yearly = df.groupby('Year')[['Sales','Profit']].sum()

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(yearly.index, yearly['Profit'], 'o-', color='coral', lw=2, ms=8)
ax.fill_between(yearly.index, yearly['Profit'], alpha=0.1, color='coral')
ax.axhline(0, color='grey', lw=0.8, linestyle='--')
ax.set_title('Annual Profit Trend — Is Profit Growing?', fontsize=13)
ax.set_xlabel('Year')
ax.set_ylabel('Total Profit ($)')
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'${x/1000:.0f}K'))
plt.tight_layout()
plt.show()

```

Output:

```

(run in notebook — inspect output with class)

```

**Break it down**:

- Walk through each line aloud

- Connect output to the business question

**Ask**: What would you investigate next?

**Common mistake**: Running code without stating the EDA question first


**Charts 2-4:** Sub-category loss-makers, discount vs profit scatter (already built), and a "fix" recommendation chart showing profit if Furniture discounts were capped.

*Walk through the story together: "Profit declined in 2017. Drilling down shows Furniture is loss-making. The cause is aggressive discounting. The fix is a discount cap."*

---

## SEGMENT 10: Summary & Wrap-Up (5 min)

**The EDA framework:**
1. Shape → Distribution → Relationship → Change over time
2. Chart type = answer to "what question am I answering with this visual?"
3. Every chart needs: title with insight, labelled axes, and a recommendation

**The four charts we built today:**
- Histogram: sales distribution → right-skewed, median matters more than mean
- Box plot: profit by category → Furniture has loss-making outliers
- Scatter + heatmap: discount vs profit → strong negative correlation
- Line chart: profit trend → year-over-year context

**Bridge:** *"Next session you'll connect code to live external data via APIs — you'll call a real weather API, process the JSON, and build a mini interface. This is how AI applications get their live data."*

---

## Q&A & Doubt Solving (5 min)

**Q: How many charts is enough for an EDA?**
→ There is no fixed number. A good EDA answers all four framework questions. For a clean dataset with 10 columns, 5–8 charts is typically sufficient. For messy, unknown data — more.

**Q: When should I use Seaborn vs Matplotlib?**
→ Seaborn for statistical charts that would be verbose in Matplotlib (heatmaps, pairplots, violin plots). Matplotlib for full control over layout, annotations, and multi-subplot figures. Most real work uses both.

**Q: What's the difference between a histogram and a bar chart?**
→ Histograms are for continuous numeric data — the x-axis is a continuous range, bars represent frequency in each range (bin). Bar charts are for categorical data — each bar represents a distinct category. Never use a bar chart for a numeric distribution.

**Q: Should I always use correlation before scatter plots?**
→ Look at correlation first as a quick screen — it tells you which pairs are worth plotting. Then plot scatter for the interesting pairs to see the actual shape of the relationship (linear? curved? clustered?).

---

## Instructor Notes

- **Dataset:** The Superstore dataset is ideal — it has enough columns (21) and rows (~10,000) to produce interesting EDA findings without being overwhelming. Make sure students download it before class or have a cached version ready.
- **Seaborn import:** Requires installation — `pip install seaborn`. Confirm this before the session. Seaborn is importable in most Jupyter environments.
- **Pacing:** Practical 4 is intentionally open-ended. If time is short, reduce to 2 charts in the "story" section and treat it as a take-home project.
- **Common student mistake:** Building 20 charts with no narrative. Teach the principle: "One insight per chart. One chart per page of your story. If your chart doesn't have an insight, either the chart is wrong or the data doesn't have the answer you expected — that's also a valid finding."


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

**Show**:

```python

import pandas as pd
df = pd.read_csv('superstore.csv')
print('Rows:', len(df))
print('Date range:', df['Order Date'].min(), '→', df['Order Date'].max())
print('Nulls:', df.isnull().sum().sum())
print('Negative profit rows:', (df['Profit'] < 0).sum())

```

Output:

```

Rows: 9994
Date range: 1/1/2014 → 12/30/2017
Nulls: 0
Negative profit rows: 1877

```

**Break it down**:

- Shape audit answers EDA question 1 before any chart

- Negative profit count is an early business finding

- Zero nulls means cleaning was done — note in presentation

**Ask**: What percentage of orders lose money?

**Common mistake**: Skipping shape audit and jumping to plots

**Student try**: Compute profit margin column and describe its distribution.
**Show**:

```python

fig, axes = plt.subplots(2, 2, figsize=(12, 9))
axes[0,0].hist(df['Sales'], bins=50, color='steelblue')
axes[0,1].boxplot([df[df.Category==c].Profit for c in df.Category.unique()], labels=df.Category.unique())
region_sales = df.groupby('Region')['Sales'].sum()
axes[1,0].bar(region_sales.index, region_sales.values)
df.groupby('Sub-Category')['Profit'].mean().sort_values().plot(kind='barh', ax=axes[1,1])
plt.suptitle('Superstore EDA — Four Questions')
plt.tight_layout()
plt.show()

```

Output:

```

(2×2 panel figure displayed)

```

**Break it down**:

- Panel 1 DISTRIBUTION — Sales histogram

- Panel 2 DISTRIBUTION — Profit box by category

- Panel 3 CHANGE/COMPARE — Sales by region

- Panel 4 RELATIONSHIP — Avg profit by sub-category

**Ask**: Which panel would you show the VP first?

**Common mistake**: Four panels with no narrative order — audience gets lost

**Student try**: Add a red reference line at Profit=0 on the box plot.
## SEGMENT 12: Correlation Deep Dive (10 min)

**Show**:

```python

numeric = ['Sales','Profit','Discount','Quantity']
print(df[numeric].corr().round(2))
sns.heatmap(df[numeric].corr(), annot=True, cmap='RdBu_r', center=0)
plt.title('Superstore Numeric Correlations')
plt.show()

```

Output:

```

           Sales  Profit  Discount  Quantity
Sales        1.00    0.48     -0.03      0.23
Profit       0.48    1.00     -0.22      0.07
Discount    -0.03   -0.22      1.00     -0.02
Quantity     0.23    0.07     -0.02      1.00

```

**Break it down**:

- Sales–Profit moderate positive link

- Discount–Profit negative — key business finding

- Heatmap shows all pairwise linear relationships at once

**Ask**: Which pair would you investigate first for a pricing policy?

**Common mistake**: Claiming causation from correlation alone

**Student try**: Filter to Furniture only and recompute the discount–profit correlation.

---

## SEGMENT 13: Story Notebook Review (10 min)

**Pair activity:** Partner A presents Chart 1 (profit trend); Partner B asks one clarifying question.

| Chart | Must include |
|---|---|
| 1 | Title with finding + year range |
| 2 | Category or region comparison |
| 3 | Scatter with labelled axes |
| 4 | Recommendation bullet below figure |

**Instructor circulate:** Check every notebook has four EDA questions answered in markdown cells above each chart.

---

## SEGMENT 14: Business Recommendation Writing (10 min)

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
