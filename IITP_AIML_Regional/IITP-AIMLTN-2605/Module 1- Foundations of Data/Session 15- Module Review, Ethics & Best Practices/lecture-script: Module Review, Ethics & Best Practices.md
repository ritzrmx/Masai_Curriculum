# Lecture Script: Module Review, Ethics & Best Practices
> **Instructor Reference** — Module 1: Foundations of Data | Session 15 | Duration: 2 Hours

---

## Session Overview

**Goal:** Students consolidate all Module 1 skills through a structured capstone review, then develop a framework for responsible data practice — understanding bias, privacy, and the human impact of data decisions.

**Student profile at this point:** Have completed all 15 sessions of Module 1. Ready to move to Module 2 (Classical ML). This session is deliberately slower-paced and reflective.

**Key outcome:** Students can articulate 5 things they learned in Module 1 with concrete examples, identify at least 2 ethical problems in a given dataset scenario, and have a checklist they will use before sharing any analysis.

**Tone for this session:** Reflective, discussion-heavy. Less notebook, more thinking and conversation. The practical exercises are designed to surface opinions and debate, not just correct answers.

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| Opening — The Module 1 Stack in One Diagram | 5 min | 0:05 |
| **Concept 1:** The Data Professional's Workflow — End-to-End | 10 min | 0:15 |
| **Practical 1:** Capstone mini-challenge (clean → query → visualise) | 20 min | 0:35 |
| **BREAK** | 10 min | 0:45 |
| **Concept 2:** Data Ethics — Bias, Fairness, and Privacy | 15 min | 1:00 |
| **Practical 2:** Ethics case studies — group discussion | 15 min | 1:15 |
| **Concept 3:** Best Practices — The Before-You-Share Checklist | 10 min | 1:25 |
| **Practical 3:** Audit a flawed chart / flawed analysis | 10 min | 1:35 |
| **Concept 4:** What's Coming in Module 2 — Preview | 10 min | 1:45 |
| Summary & Wrap-Up | 10 min | 1:55 |
| Q&A & Doubt Solving | 5 min | 2:00 |

---

## Opening (5 min)

**Show this diagram on the board — the complete Module 1 stack:**

```
Raw Data (CSV, API, Database)
         │
         ▼
  COLLECT & LOAD
  (pandas.read_csv, requests, SQLite)
         │
         ▼
   AUDIT & CLEAN
  (dtypes, nulls, duplicates, types)
         │
         ▼
   QUERY & AGGREGATE
  (filter, groupby, pivot, SQL JOIN)
         │
         ▼
   EXPLORE & VISUALISE
  (distributions, correlations, trends)
         │
         ▼
   COMMUNICATE & DECIDE
  (clear charts, insights, recommendations)
```

*"In 15 sessions you have learned all five layers of this stack. Today we run through it one more time — fast, as a complete unit — and then we talk about the responsibility that comes with it."*

**Set the tone:** *"Data is not neutral. A chart showing COVID cases by region looked very different depending on whether it showed raw counts or rates per 100,000. Same data. Different story. Knowing how to analyse data is a superpower — today we talk about using it responsibly."*

---

## Concept Block 1: The End-to-End Workflow (10 min)

### Review: What You Can Now Do

Go through each layer and ask one student to describe what they learned:

| Layer | Key skill | Tool(s) |
|---|---|---|
| Collect | Read CSVs, call APIs, query databases | `pd.read_csv`, `requests`, `sqlite3` |
| Clean | Handle nulls, fix types, remove duplicates | `fillna`, `to_numeric`, `drop_duplicates` |
| Query | Filter, group, aggregate, join | Pandas chaining, SQL SELECT/JOIN |
| Explore | Distributions, correlations, trends | Matplotlib, Seaborn |
| Communicate | Titled charts, annotations, recommendations | Matplotlib formatting, Gradio |

**The five questions an analyst answers:**
1. What data do we have? (shape, types, quality)
2. What does the data look like? (distribution, outliers)
3. How do things compare across groups? (groupby, segment)
4. How do variables relate to each other? (correlation, scatter)
5. What changed over time? (trend, seasonality)

**Bridge to Module 2:** *"ML models answer a sixth question: 'Given this new row of data, what is the prediction?' Everything we've built in Module 1 is the input preparation for that."*

---

## Practical Block 1: Capstone Mini-Challenge (20 min)

**Setup:** This is the capstone exercise. Give students 15 minutes to work individually or in pairs, then debrief together for 5 minutes.

**The challenge:** A fictional company "DataMart" has given you their raw sales data. Answer the three questions below and produce one chart per question.

```python
import pandas as pd
import matplotlib.pyplot as plt
import io

# DataMart — messy raw sales data
raw_data = """
order_id,rep,region,product,revenue,cost,order_date,status
1001,Priya,North,Laptop,65000,50000,01-03-2025,completed
1002,Arjun,South,Chair,12000,8000,05/03/2025,completed
1001,Priya,North,Laptop,65000,50000,01-03-2025,completed
1003,Meera,East,Laptop,65000,50000,2025-03-10,cancelled
1004,Arjun,South,Notebook,800,400,12-03-2025,completed
1005,Priya,North,Laptop,65000,50000,15-03-2025,completed
1006,Ravi,West,Chair,12000,,18-03-2025,completed
1007,Meera,East,Notebook,800,400,20-03-2025,completed
1008,Ravi,West,Laptop,65000,50000,22-03-2025,
1009,Arjun,South,Laptop,65000,50000,25-03-2025,completed
"""

df = pd.read_csv(io.StringIO(raw_data))
print("Raw data shape:", df.shape)
print(df.dtypes)
print("\nNulls:", df.isnull().sum())
print("Duplicates:", df.duplicated().sum())
```

**Three questions to answer:**

```python
# STEP 1: Clean it
# (Students should find: 1 duplicate, 1 null cost, 1 null status, mixed date formats)

# Remove duplicate
df_clean = df.drop_duplicates()

# Fix types
df_clean['revenue'] = pd.to_numeric(df_clean['revenue'], errors='coerce')
df_clean['cost'] = pd.to_numeric(df_clean['cost'], errors='coerce')
df_clean['order_date'] = pd.to_datetime(df_clean['order_date'], dayfirst=True, errors='coerce')

# Handle nulls
df_clean['cost'] = df_clean['cost'].fillna(df_clean.groupby('product')['cost'].transform('median'))
df_clean['status'] = df_clean['status'].fillna('unknown')

# Add profit
df_clean['profit'] = df_clean['revenue'] - df_clean['cost']
df_completed = df_clean[df_clean['status'] == 'completed']

print("\nCleaned data:")
print(df_completed[['order_id','rep','region','product','revenue','profit']])

# QUESTION 1: Which region has the highest profit margin?
region_summary = df_completed.groupby('region').agg(
    total_revenue=('revenue','sum'),
    total_profit=('profit','sum')
).reset_index()
region_summary['profit_margin_%'] = (
    region_summary['total_profit'] / region_summary['total_revenue'] * 100
).round(1)
print("\nQ1 — Region profit margins:")
print(region_summary.sort_values('profit_margin_%', ascending=False))

# QUESTION 2: Which sales rep generated the most profit?
rep_profit = df_completed.groupby('rep')['profit'].sum().sort_values(ascending=False)
print("\nQ2 — Rep profits:")
print(rep_profit)

# QUESTION 3: Which product has the best margin?
product_margin = df_completed.groupby('product').agg(
    avg_margin=('profit', lambda x: (x / df_completed.loc[x.index,'revenue']).mean() * 100)
).reset_index()
print("\nQ3 — Product margins:")
print(product_margin)
```

**Debrief (5 min):** Ask 2–3 students: "What cleaning steps did you take? Did everyone get the same result? Why/why not?"

---

## BREAK (10 min)

*Discussion prompt for after the break: "Can you think of a dataset that looks clean but could still cause harm? Think about who collected it, about whom, and for what purpose."*

---

## Concept Block 2: Data Ethics — Bias, Fairness, and Privacy (15 min)

### The Four Core Ethics Questions

Every time you work with data about people, ask:

```
1. CONSENT     — Did these people know their data would be used this way?
2. BIAS        — Does this dataset over-represent or under-represent any group?
3. HARM        — What could go wrong if this analysis is wrong or misused?
4. TRANSPARENCY — Can I explain how I got this result to someone who was affected by it?
```

### Types of Bias in Data

**1. Selection Bias** — the dataset doesn't represent the real population

*Example:* A hospital trains an ML model to predict readmission using patients from one private hospital. The model works poorly on patients from government hospitals because the demographics are completely different.

**2. Historical Bias** — the data reflects past discrimination, not objective truth

*Example:* A hiring model trained on 20 years of employee data at a company that historically promoted mostly men will learn to prefer male candidates — even if gender is not a feature, proxies (sports teams, certain universities) encode the same bias.

**3. Measurement Bias** — the way data was collected is different for different groups

*Example:* Pulse oximeters historically showed higher accuracy for lighter-skinned patients. Medical AI trained on that data systematically underestimated risk for darker-skinned patients.

**4. Confirmation Bias** — the analyst looks for results that confirm their hypothesis

*Example:* A marketing team's data analyst only shows the charts that support the campaign working, ignoring the 70% of metrics that show no effect.

### Privacy Principles (GDPR-inspired, applicable everywhere)

| Principle | What it means | Practical example |
|---|---|---|
| Minimisation | Only collect what you need | Don't store full addresses if only city is needed |
| Purpose limitation | Don't use data for something else | User gave consent for marketing emails, not for profiling |
| Anonymisation | Remove identifiers before analysis | Replace names with IDs before sharing with a team |
| Right to be forgotten | People can request deletion | Build delete capability into your systems |

---

## Practical Block 2: Ethics Case Studies — Group Discussion (15 min)

**Divide into 3 groups. Each group gets one scenario (5 min to discuss + 5 min to present):**

**Case 1 — The Loan Model**
*A fintech company trains a loan-approval model on historical approval data. The model achieves 94% accuracy. It gets deployed. Six months later, an audit finds that applicants from rural Tier-3 cities are rejected at 3× the rate of urban applicants, even with identical income and credit scores.*

Questions for the group:
1. What type of bias is this?
2. Was it acceptable to deploy the model at 94% accuracy?
3. How would you detect this problem before deployment?
4. What would you do now that it's deployed?

**Case 2 — The HR Dashboard**
*An HR analyst builds a dashboard showing average performance ratings by team. The "Marketing" team's ratings are consistently lower. The VP of HR shares this with all department heads. The Marketing team's ratings drop further the next quarter (the Pygmalion effect).*

Questions for the group:
1. What ethical problem occurred when the dashboard was shared?
2. What could have been done differently in how the analysis was presented?
3. Is the analyst responsible for the outcome?
4. How should performance dashboards be designed differently?

**Case 3 — The Health App**
*A health app collects users' step count, sleep patterns, and heart rate data. The company sells anonymised aggregate data to insurance companies. A research paper later shows that combinations of these patterns can re-identify 87% of individuals.*

Questions for the group:
1. Did the company violate its user agreement? (The terms said "anonymised.")
2. What is re-identification, and why is "anonymised" not the same as "private"?
3. What should the company have done before selling the data?
4. Who bears responsibility — the company? The insurance buyers? The researcher?

---

## Concept Block 3: Best Practices — The Before-You-Share Checklist (10 min)

### The 10-Item Checklist

Give this to students as a takeaway (they can screenshot it):

```
Before sharing ANY analysis or chart:

DATA QUALITY
□ 1. Did I check for nulls and handle them explicitly?
□ 2. Did I check for duplicates?
□ 3. Are all data types correct (dates as dates, numbers as numbers)?
□ 4. Did I document where the data came from and its date range?

ANALYSIS INTEGRITY
□ 5. Are my filter conditions correct? (Did I accidentally include cancelled orders?)
□ 6. Is my aggregation at the right level? (Per customer? Per order? Per month?)
□ 7. Am I comparing apples to apples? (Same time period, same population)

COMMUNICATION
□ 8. Does my chart have a title that states the insight (not just "bar chart")?
□ 9. Are both axes labelled with units?
□ 10. Does my recommendation follow logically from my data?

ETHICS
□ Bonus: Who could be harmed by a wrong conclusion here?
         Have I asked that question?
```

*"This checklist is the difference between an analyst who builds trust and one who burns it. One wrong chart at the wrong time can undo months of good work."*

---

## Practical Block 3: Audit a Flawed Analysis (10 min)

**Show students this intentionally flawed chart scenario:**

```python
# Instructor presents this — do NOT run it as a live demo; show as pseudocode/image
# The analysis has 5 deliberate errors

# "Analysis": Average order value by region

# ERROR 1: Includes cancelled orders
df_all = df_clean  # should be df_completed

# ERROR 2: Uses mean on skewed data without checking
region_avg = df_all.groupby('region')['revenue'].mean()

# ERROR 3: Chart has no title with insight
region_avg.plot(kind='bar')
plt.show()   # No labels, no title, no context

# ERROR 4: One region has only 1 order — average is meaningless
print(df_all.groupby('region')['order_id'].count())

# ERROR 5: The "finding" presented to management:
# "North region has the highest average order value (₹65,000)"
# — But North has only 1 order (the Laptop order).
#   It's not a finding; it's a sample size of 1.
```

**Ask students to identify the 5 errors and explain the consequence of each one if this analysis was used to reallocate the sales team's budget.**

---

## Concept Block 4: What's Coming in Module 2 (10 min)

### The Bridge: From Data to Prediction

*"Everything in Module 1 answered descriptive questions: What happened? What does the distribution look like? How do groups compare? Module 2 answers a new kind of question: Given what happened before, what will happen next?"*

**The ML workflow (preview — don't go deep, just create curiosity):**

```
Module 1 gave us:           Module 2 adds:
Clean data              →   Feature engineering
Aggregated metrics      →   Feature matrix (X) and target (y)
Correlation insight     →   Quantified prediction
SQL/Pandas query        →   Model: f(X) = ŷ
EDA chart               →   Model evaluation chart
```

### A First Intuition for Linear Regression

```python
# Recall from Session 11 (Master Class):
# y = mx + c  →  exam_score = slope × hours_studied + intercept

# Module 2 will use sklearn to find the BEST m and c automatically:
# from sklearn.linear_model import LinearRegression
# model = LinearRegression()
# model.fit(X, y)         # Finds best m and c
# model.predict([[7]])    # Predicts score for 7 hours studied
```

**Preview the four Module 2 topics:**
1. Regression — predicting numbers (price, revenue, temperature)
2. Classification — predicting categories (spam/not spam, approved/rejected)
3. Evaluation — measuring whether the model is actually good
4. Unsupervised — finding patterns without labels (customer segments)

*"Every technique in Module 2 builds directly on what you learned in Module 1. Clean data is the input. The statistical intuition you built — mean, median, correlation, distributions — is how you interpret the model's output."*

---

## Summary & Wrap-Up (10 min)

**The Module 1 journey — draw the timeline:**

```
Week 1: Python → Data Structures → Control Flow → Functions
Week 2: Math Foundations → NumPy + Pandas → Data Cleaning
Week 3: Query Thinking → Advanced Pandas + SQL → Master Class
Week 4: SQL Analysis → EDA → APIs → Review & Ethics
```

**What you can now do (let students call out their own answers):**
- Load and clean any CSV
- Query data in Pandas and SQL
- Visualise distributions, comparisons, and relationships
- Call external APIs and parse JSON
- Build a simple Gradio demo
- Ask ethical questions about data and analysis

**The analyst's creed — read this aloud:**
> *"Data is a representation of real people, real decisions, and real consequences. My job is not to find the answer that supports the story I want to tell — it is to find the true pattern in the data, acknowledge its limitations, and communicate it honestly."*

**Looking ahead:** *"Module 2 starts with the ML Workflow — we build a train/test split, establish baselines, and train your first regression model. Come to the first session having reviewed the correlation coefficient and the scatter plot — those two concepts are where regression begins."*

---

## Q&A & Doubt Solving (5 min)

**Q: Do I need to know all the Pandas commands by heart?**
→ No. The most experienced data scientists Google syntax every day. What you need to "own" is the mental model: which operation answers which question. The syntax is a lookup; the thinking is yours.

**Q: How do I know if my analysis is biased?**
→ Ask: "Who is represented in this data? Who is not? Would the conclusion change if I looked at a different group?" There is no algorithm that detects bias for you — it requires deliberate questioning.

**Q: Is data ethics a legal requirement?**
→ Increasingly, yes. GDPR (Europe), PDPB (India, upcoming), and various national frameworks impose legal obligations on data collection and use. Even outside legal requirements, ethical failures are major reputational and business risks.

**Q: What should I do if I find a major data quality problem in production?**
→ Raise it immediately. Do not quietly fix it and move on. Document what you found, when, and what the downstream impact may have been. In regulated industries (finance, health), this is a legal requirement.

---

## Instructor Notes

- **Pacing:** This session is designed to be slower and more reflective than usual. If students finish the capstone fast, use the extra time for deeper discussion on the ethics cases. The discussion is the learning.
- **Ethics discussion facilitation:** These cases do not have clean right/wrong answers. Your job is to surface the tension, not to resolve it. Ask "Who disagrees?" and "What would you do differently in hindsight?"
- **The Module 1 capstone:** If your program has a graded module assignment, this is the session where you preview it or introduce it. The capstone challenge in Practical 1 can be extended to a full assignment.
- **Module 2 preview:** Do not go into detail — 10 minutes of curiosity-building is more valuable than a 40-minute preview that replaces the first Module 2 session. Leave them wanting more.
- **Certification note:** If your program issues Module 1 completion certificates, mention the criteria now. Students who know there is a milestone ahead are more engaged in the review.
