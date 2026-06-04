# Lecture Script: Master Class — From Tables to Relationships: The Mathematics of Data Organisation
> **Instructor Reference** — Module 1: Foundations of Data | Session 11 | Duration: 2 Hours

---

## Session Overview

**Goal:** Students understand the mathematical ideas that power every data visualisation and every descriptive statistic — not by memorising formulas, but by seeing *why* these concepts were invented and what they reveal.

**Student profile at this point:** Have cleaned data, queried it, and pivoted it. This is a "why does this work?" class — building intuition before it becomes mechanical in later sessions.

**Key outcome:** Students can look at a scatter plot and describe the relationship between variables. They can compute mean, median, and standard deviation on a small dataset by hand and explain what each one reveals (and hides).

**Tone for this session:** Conversational, conceptual. This is a master class — fewer notebooks, more discussion, more drawing on the board. Let students reason through examples before showing answers.

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| Opening — Why Math Underpins Data | 5 min | 0:05 |
| **Concept 1:** The Cartesian Plane — What "Plotting Data" Actually Means | 10 min | 0:15 |
| **Practical 1:** Scatter plots from raw data — manual + Matplotlib | 15 min | 0:30 |
| **Concept 2:** Slope of a Line — The First Hint of Machine Learning | 10 min | 0:40 |
| **Practical 2:** "Best fit" intuition — drawing a line through points | 15 min | 0:55 |
| **BREAK** | 10 min | 1:05 |
| **Concept 3:** Descriptive Statistics — Mean, Median, Mode, Spread | 10 min | 1:15 |
| **Practical 3:** Compute by hand + verify with Pandas + real examples | 15 min | 1:30 |
| **Concept 4:** Why the Mean Lies When Data Is Skewed | 10 min | 1:40 |
| **Practical 4:** Comparing mean vs median on skewed real datasets | 10 min | 1:50 |
| Summary & Wrap-Up | 5 min | 1:55 |
| Q&A & Doubt Solving | 5 min | 2:00 |

---

## Opening (5 min)

**Ask the class:** *"When you look at a graph, what do you actually see?"*

Let them answer — they'll say lines, bars, points. Then reframe:

*"You are looking at numbers mapped to positions in space. Every visualisation you have ever seen is just pairs of numbers — (x, y) — drawn as dots, lines, or bars. The entire field of data visualisation is built on one ancient idea: the Cartesian coordinate system. Today we understand that system, and we understand what we're actually measuring when we summarise data."*

**Why this matters for AI/ML:** Every ML model is finding a mathematical relationship in data. A linear regression is literally finding the slope of the best line through your data points. An embedding is a point in a 1536-dimensional Cartesian space. Understanding the 2D case makes everything that follows less mysterious.

---

## Concept Block 1: The Cartesian Plane — What "Plotting Data" Means (10 min)

### The Key Insight

A Cartesian plane assigns two numbers to every point in a 2D space — its x-coordinate (horizontal position) and y-coordinate (vertical position). When you "plot data," you are simply placing each row of your table at the position `(x_value, y_value)`.

**Draw on board:**

```
   y (Revenue)
   |
10 |         . (Age=30, Rev=10k)
 8 |   . (Age=22, Rev=8k)
 6 |
 4 |
 2 |
   +----+----+----+--- x (Age)
   0    10   20   30
```

A scatter plot is a table, viewed as a picture.

| Row | Age | Revenue | Plotted as |
|---|---|---|---|
| Alice | 30 | 10,000 | Point at (30, 10000) |
| Bob | 22 | 8,000 | Point at (22, 8000) |
| Charlie | 45 | 15,000 | Point at (45, 15000) |

**The question a scatter plot answers:** "When x increases, does y tend to increase, decrease, or stay the same?" That *tendency* is called **correlation** — and it is the seed of prediction.

### Variables: Independent vs Dependent

- **x-axis (independent):** The variable we control or observe first (age, hours studied, budget)
- **y-axis (dependent):** The outcome we are trying to understand or predict (revenue, exam score, sales)

*"Always put what you're trying to explain on the y-axis."*

---

## Practical Block 1: Scatter Plots — Manual + Matplotlib (15 min)

### Manual first (5 minutes)

Give students this table and ask them to draw the scatter plot on paper (3 × 3 grid is fine):

```
hours_studied | exam_score
     2        |    45
     4        |    60
     3        |    55
     6        |    75
     8        |    85
     1        |    40
     5        |    68
```

*"What pattern do you see? If a student studied 7 hours, where would their dot be?"*

### Then code it (10 minutes)

```python
import pandas as pd
import matplotlib.pyplot as plt

study_data = pd.DataFrame({
    'hours_studied': [2, 4, 3, 6, 8, 1, 5],
    'exam_score':    [45, 60, 55, 75, 85, 40, 68]
})

plt.figure(figsize=(8, 5))
plt.scatter(study_data['hours_studied'], study_data['exam_score'],
            color='steelblue', s=100, edgecolors='white')
plt.xlabel('Hours Studied')
plt.ylabel('Exam Score')
plt.title('Study Hours vs Exam Score')
plt.grid(True, alpha=0.3)
plt.show()

# Check correlation
print("Correlation:", study_data['hours_studied'].corr(study_data['exam_score']).round(3))
```

**Explain the correlation coefficient:**
- Close to +1: strong positive relationship (as x increases, y increases)
- Close to -1: strong negative relationship (as x increases, y decreases)
- Close to 0: no linear relationship

---

## Concept Block 2: Slope of a Line — The First Hint of ML (10 min)

### The Equation of a Line

```
y = mx + c
     │    └── y-intercept (where the line crosses the y-axis)
     └─────── slope (rise over run)
```

**Slope = rise / run = (change in y) / (change in x)**

Draw on board: two points (2, 45) and (8, 85). Rise = 85-45 = 40. Run = 8-2 = 6. Slope = 40/6 ≈ 6.7.

*"A slope of 6.7 means: for every extra hour of study, exam score increases by about 6.7 points. That's prediction. That's Linear Regression."*

### Residuals — The Gap Between the Line and the Point

Draw a line through the scatter plot. Each point sits either above or below the line.

```
Residual = Actual value − Predicted value (from the line)
```

A point above the line has a **positive residual** (we underpredicted).
A point below has a **negative residual** (we overpredicted).

**The goal of Linear Regression:** Find the slope `m` and intercept `c` that make the residuals as small as possible — specifically, that minimises the *sum of squared residuals*.

*"We'll formalise this in Module 2. Today, just feel what a residual means — it's the distance from reality to your prediction."*

---

## Practical Block 2: Best-Fit Line Intuition (15 min)

```python
import numpy as np

# Our data
x = study_data['hours_studied'].values
y = study_data['exam_score'].values

# --- Draw scatter + manually try a line ---
m_manual = 7    # guess: 7 points per hour
c_manual = 35   # guess: baseline score of 35

y_predicted = m_manual * x + c_manual
residuals = y - y_predicted

print("Manual line: y =", m_manual, "x +", c_manual)
print("\nPredictions vs actuals:")
comparison = pd.DataFrame({'hours': x, 'actual': y, 'predicted': y_predicted, 'residual': residuals})
print(comparison)
print("\nSum of squared residuals:", round(sum(residuals**2), 1))

# --- Now let numpy find the best line ---
coeffs = np.polyfit(x, y, deg=1)
m_best, c_best = coeffs
print(f"\nBest fit: y = {m_best:.2f}x + {c_best:.2f}")

y_best = m_best * x + c_best
residuals_best = y - y_best
print("Sum of squared residuals (best):", round(sum(residuals_best**2), 1))

# --- Plot both ---
plt.figure(figsize=(9, 5))
plt.scatter(x, y, color='steelblue', s=120, label='Data', zorder=5)
plt.plot(x, y_predicted, 'r--', label=f'Manual: y={m_manual}x+{c_manual}')
x_line = np.linspace(min(x), max(x), 100)
plt.plot(x_line, m_best*x_line + c_best, 'g-', lw=2, label=f'Best fit: y={m_best:.2f}x+{c_best:.2f}')
plt.xlabel('Hours Studied')
plt.ylabel('Exam Score')
plt.title('Best Fit Line')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
```

**Discussion:** *"Which line is closer to more points? Why does squaring the residuals matter?"* (Squaring prevents positive and negative residuals from cancelling out.)

---

## BREAK (10 min)

*Ask students to think: "What does the average exam score tell you? What doesn't it tell you if half the class scored 100 and the other half scored 0?"*

---

## Concept Block 3: Descriptive Statistics (10 min)

### The Three Centres

| Statistic | Formula | Best for | Worst for |
|---|---|---|---|
| **Mean** | Sum ÷ Count | Symmetric data | Skewed data, outliers |
| **Median** | Middle value | Skewed data, outliers | — |
| **Mode** | Most frequent | Categorical, discrete | Continuous data |

**Variance and Standard Deviation — Measuring Spread**

- **Variance:** Average of squared distances from the mean
- **Standard Deviation (σ):** Square root of variance — in the same units as the data

**Why standard deviation and not just range?**
Range ignores where all the middle values are. Std dev captures how "spread out" the whole distribution is.

### The Five-Number Summary

```
Min | Q1 (25th percentile) | Median | Q3 (75th percentile) | Max
         └─────────── IQR (Interquartile Range) ───────────┘
```

**IQR** = Q3 - Q1. Values below `Q1 - 1.5×IQR` or above `Q3 + 1.5×IQR` are statistical outliers.

---

## Practical Block 3: Compute by Hand + Pandas (15 min)

### By hand first (5 min)

Give students this small dataset and ask them to compute mean, median, and std:

```
Salaries (₹ lakhs): 5, 6, 7, 8, 100
```

Walk through:
- Mean = (5+6+7+8+100)/5 = 126/5 = **25.2**
- Median = **7** (middle value when sorted)
- Ask: *"Which is more representative of a 'typical' salary here?"*

### Pandas verification (10 min)

```python
import pandas as pd

salaries = pd.Series([5, 6, 7, 8, 100])

print("Mean:    ", salaries.mean())    # 25.2
print("Median:  ", salaries.median())  # 7.0
print("Std dev: ", salaries.std().round(2))
print("Variance:", salaries.var().round(2))
print()
print("Full describe():")
print(salaries.describe())

# --- On a real dataset ---
import numpy as np
np.random.seed(42)
exam_scores = pd.Series(np.concatenate([
    np.random.normal(65, 10, 80),  # Most students: around 65
    np.random.normal(95, 3, 20)    # High achievers: around 95
]).clip(0, 100).round(0))

print("\nExam Score Distribution:")
print(f"Mean:   {exam_scores.mean():.1f}")
print(f"Median: {exam_scores.median():.1f}")
print(f"Std:    {exam_scores.std():.1f}")

# Visualise
import matplotlib.pyplot as plt
plt.figure(figsize=(9, 4))
plt.hist(exam_scores, bins=20, color='steelblue', edgecolor='white')
plt.axvline(exam_scores.mean(), color='red', lw=2, label=f'Mean={exam_scores.mean():.1f}')
plt.axvline(exam_scores.median(), color='green', lw=2, linestyle='--',
            label=f'Median={exam_scores.median():.1f}')
plt.xlabel('Exam Score')
plt.title('Distribution of Exam Scores')
plt.legend()
plt.show()
```

---

## Concept Block 4: Why the Mean Lies When Data Is Skewed (10 min)

### Skewness — When the Tail Pulls the Mean

```
Symmetric (normal):    Mean ≈ Median ≈ Mode — all three align

Right-skewed:          Mode < Median < Mean
                       (a few very high values pull the mean up)
                       Example: income distribution, house prices

Left-skewed:           Mean < Median < Mode
                       (a few very low values pull the mean down)
                       Example: age at retirement, product lifetimes
```

**The classic example:** India's average per capita income includes both ₹5,000/month workers and ₹50 crore/year executives. The mean is pulled dramatically toward the wealthy minority. The median tells you what the "middle person" earns.

**Practical implication:** When a news headline says "average house price in Mumbai," ask: *"Is that mean or median?"* If it's mean, a few ₹20 crore properties drag it far above the price a typical buyer would pay.

### When to report which:

| Data type | Report |
|---|---|
| Salaries, house prices, wealth | Median |
| Heights, test scores (symmetric) | Mean |
| Product defect counts (discrete) | Median or mode |
| ML model performance metrics | Mean (with std dev) |

---

## Practical Block 4: Mean vs Median on Skewed Data (10 min)

```python
# --- House prices (right-skewed) ---
house_prices = pd.Series([
    25, 28, 30, 32, 35, 38, 40, 42, 45, 50,  # Most homes
    80, 120, 250, 500, 1200                    # A few luxury properties (lakhs)
])

print("House Prices Summary:")
print(f"Mean:   ₹{house_prices.mean():.1f} lakhs")
print(f"Median: ₹{house_prices.median():.1f} lakhs")
print(f"Mode:   ₹{house_prices.mode()[0]} lakhs")
print(f"Std:    ₹{house_prices.std():.1f} lakhs")

plt.figure(figsize=(9, 4))
plt.hist(house_prices, bins=15, color='coral', edgecolor='white')
plt.axvline(house_prices.mean(), color='red', lw=2,
            label=f'Mean = ₹{house_prices.mean():.0f}L')
plt.axvline(house_prices.median(), color='green', lw=2, linestyle='--',
            label=f'Median = ₹{house_prices.median():.0f}L')
plt.xlabel('Price (₹ Lakhs)')
plt.title('House Price Distribution — Right Skewed')
plt.legend()
plt.show()

# Ask: which would you use to price your own home?
```

**Discussion point:** *"If you were a home seller, which number would you prefer to quote — mean or median? As a buyer? As a policymaker?"* There is no single right answer — it depends on purpose. This is a data ethics question too.

---

## Summary & Wrap-Up (5 min)

**The mathematical ideas from today:**

1. **Cartesian coordinates** — every data point is an `(x, y)` position in space
2. **Scatter plots** = tables viewed as pictures; the pattern reveals relationships
3. **Slope** = rise/run = "how much does y change per unit of x?" → the heart of linear regression
4. **Residuals** = actual − predicted → we will minimise these in Module 2
5. **Mean** = balancing point; **Median** = middle value; choose based on skewness
6. **Standard deviation** = typical distance from the mean — not just max minus min

**Bridge to next sessions:** *"Session 12 goes deep into SQL joins. Everything you've seen today — especially groupby and aggregation — maps directly to GROUP BY and subqueries in SQL. The pivot table you built is the same as a SQL CASE WHEN pivot."*

---

## Q&A & Doubt Solving (5 min)

**Q: What does a negative correlation coefficient mean?**
→ As x increases, y tends to decrease (e.g., more hours of TV watched, lower exam score). A value of -0.95 means a very strong negative linear relationship.

**Q: Can the median ever equal the mean?**
→ Yes — in a perfectly symmetric distribution. For any roughly symmetric dataset (heights, IQ scores), mean and median are very close.

**Q: What does a slope of 0 mean on a scatter plot?**
→ No relationship between x and y — the "best fit" line is flat. Knowing x tells you nothing about y.

**Q: Why do we square residuals instead of just taking the absolute value?**
→ Squaring heavily penalises large errors more than small ones — a residual of 10 contributes 100 to the sum of squares, while ten residuals of 1 each only contribute 10. It also makes the math (calculus-based minimisation) much cleaner.

---

## Instructor Notes

- **This is a concept-heavy session** — prioritise discussion over quantity of code. If students are engaged in discussing skewness, let it run and cut a practical block short.
- **Board work is essential here.** Draw the Cartesian plane, the slope triangle, and the skewness diagrams by hand — it is more impactful than slides.
- **Real-world examples:** India's income distribution, Mumbai house prices, and BCCI cricket batting averages are all excellent local examples of skewed distributions.
- **For advanced students:** Introduce the concept of the **normal distribution** (bell curve) briefly — why mean = median = mode in the normal case, and why so many natural phenomena follow it (Central Limit Theorem intuition).
- **Common question:** "Is variance the same as standard deviation?" — Draw the formula connection explicitly: `std = sqrt(variance)`. Variance is in squared units (e.g., ₹² ), which is not meaningful; std dev is in original units.
