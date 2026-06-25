# Data Visualization
---

## Mental Map

```mermaid
%%{init: {'flowchart': {'nodeSpacing': 55, 'rankSpacing': 65, 'diagramPadding': 24}}}%%
flowchart TB
linkStyle default stroke-width:3px

subgraph foundation[" Foundation "]
direction TB
    CURMOD["<b>Current Module Until<br/>Previous Session</b><br/><i>Foundations of Data</i><br/>Recall and distinguish AI,…<br/>…<br/>Group and aggregate data to…"]
    CURSES["<b>Current Session</b><br/><b>Data Visualization</b><br/><i>Shift:</i> Turn numbers into decisions via visuals<br/>Create line, bar, scatter and histogram plots u…<br/>build basic interactive charts using Plotly"]
end

subgraph value[" Value "]
direction LR
    CVAL["<b>Course Value</b><br/>Core stack every AI engineer<br/>repeats daily"]
    RVAL["<b>Real-Life Value</b><br/>Skills reused in internships<br/>and AI roles"]
end

subgraph future[" Future Path "]
direction TB
    U0["<b>Upcoming Module</b><br/>Classical ML<br/><i>[scikit-learn · Statistics]</i><br/>Predictive models before LLM ground…"]
    U1["<b>Upcoming Module</b><br/>GenAI & Agents<br/><i>[LLMs · Agents]</i><br/>Ship grounded AI products and agent…"]
end

START["Course Start"] ==>|&nbsp;Begin&nbsp;| CURMOD
CURMOD ==>|&nbsp;Progress&nbsp;| CURSES
CURSES ==>|&nbsp;Course Path&nbsp;| CVAL
CURSES ==>|&nbsp;Real-Life&nbsp;| RVAL
CURSES ==>|&nbsp;Next Module&nbsp;| U0
U0 -.->|&nbsp;Ahead&nbsp;| U1

classDef prevBox fill:#E8F4FC,stroke:#2B6CB0,stroke-width:2px,color:#1A202C
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

- When to use **line, bar, scatter, and histogram** charts
- How to add **titles, labels, and legends** in Matplotlib
- How **Plotly** makes interactive charts
- How chart choice depends on **variable type and goal**
- How good visuals support decisions, not decoration

---

## A. Choosing the Right Chart

> 💡 **Analogy:** You wouldn't use a pie chart to show temperature every hour — like using a photo when you need a timeline. **Chart type** must match the question.

| Question | Chart | X | Y |
|---|---|---|---|
| Trend over time | Line | Time | Metric |
| Compare categories | Bar | Category | Value |
| Relationship | Scatter | Var A | Var B |
| Distribution | Histogram | Bins | Count |

```mermaid
flowchart TD
    Q{What are you showing?}
    Q -->|Over time| L[Line]
    Q -->|Compare groups| B[Bar]
    Q -->|Two variables| S[Scatter]
    Q -->|Spread of one| H[Histogram]
```

---

## B. Matplotlib Basics

```python
import matplotlib.pyplot as plt

months = ["Jan", "Feb", "Mar"]
sales = [120, 150, 130]
plt.bar(months, sales)
plt.title("Monthly Sales")
plt.ylabel("Units")
plt.show()
```

Always label axes and title — your future self (and your manager) will thank you.

---

## C. Plotly for Interactivity

Plotly charts zoom, hover, and filter — useful in dashboards and notebooks shared with non-coders.

---

## Practice Exercises

**1. Pattern Recognition** — Show exam scores for 30 students' distribution — histogram or line?

**2. Concept Detective** — Revenue by product category — which chart?

**3. Real-Life Application** — One misleading chart you have seen (truncated axis, etc.).

**4. Spot the Error** — Scatter plot with 2 categories on x-axis only — better alternative?

**5. Planning Ahead** — Sketch axes for website visits per day for one month.

---

> ✅ **You're done!** You can match charts to questions. Next: **EDA and business thinking** on real datasets.
