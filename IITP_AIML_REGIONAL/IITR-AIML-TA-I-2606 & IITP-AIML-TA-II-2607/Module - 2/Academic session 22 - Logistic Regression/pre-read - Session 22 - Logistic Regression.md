# Machine Learning: Logistic Regression
> **Pre-Read — Academic Session 22** | Module 2: Classical ML
---
## Mental Map
> 📄 Also provided as a printable PDF in this folder: **mental-map: Logistic Regression.pdf**

```mermaid
%%{init: {'themeVariables': {'fontSize': '32px', 'fontFamily': 'sans-serif'}, 'flowchart': {'htmlLabels': true, 'nodeSpacing': 50, 'rankSpacing': 80, 'wrappingWidth': 400, 'padding': 20}}}%%
flowchart TB

START["<b>Course Start</b>"]

subgraph foundation[" WHERE WE ARE "]
direction TB
    CURMOD["<b>CURRENT MODULE</b><br/><i>Module 2: Classical ML</i><br/>&nbsp;<br/><b>Covered so far:</b> AI/ML Landscape through Spreadsheets (S1-16), ML Workflow &amp; Problem Framing (S17: churn framed as classification), Data Preparation for ML (S18: pipeline), Master Class: Lines, Curves &amp; Errors (S19), Linear Regression (S20), Regularization (S21)<br/>This is Session 22 of 39"]
    CURSES["<b>CURRENT SESSION</b><br/><b>Logistic Regression</b><br/>&nbsp;<br/><i>The shift:</i> from predicting a number <i>to</i> <b>predicting the probability that something will happen at all</b><br/>&nbsp;<br/>LogisticRegression · predict_proba()<br/>Classification threshold · Binary vs multiclass"]
end

subgraph outcome[" OUTCOME OF THIS SESSION "]
direction TB
    OUT["<b>By the end, you can…</b><br/>&nbsp;<br/>Train a LogisticRegression model on the Session 18<br/>preprocessing pipeline, interpret predicted probabilities<br/>with predict_proba(), and adjust the classification<br/>threshold to control the precision-recall balance"]
end

subgraph value[" WHY IT MATTERS "]
direction TB
    CVAL["<b>Course Value</b><br/>Session 23 (Classification Metrics) formally measures the<br/>threshold tradeoffs made here; Session 24's probability<br/>Master Class explains the math behind predict_proba() itself"]
    RVAL["<b>Real-Life Value</b><br/>Any 'risk score' or 'likelihood to buy/leave/default' feature<br/>in a real dashboard is a predict_proba() output with a<br/>chosen threshold behind it - now you know how both work"]
end

subgraph future[" WHAT COMES NEXT "]
direction TB
    U0["<b>Next Session</b><br/>Classification Metrics<br/><i>Confusion matrices, precision, recall and F1 formally judge<br/>the threshold tradeoffs made today</i>"]
    U1["<b>Later in Module 2</b><br/>Master Class: Probability &amp; Counting · Decision Trees ·<br/>Random Forests · Model Validation · Clustering"]
    U2["<b>Upcoming Modules</b><br/>Module 3: GenAI &amp; Agents<br/><i>Threshold-and-probability thinking returns when deciding<br/>how confident a RAG answer needs to be before trusting it</i>"]
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

---

## What You'll Learn

In this pre-read, you'll discover:
- Why plain linear regression breaks down when predicting a yes/no outcome, and how logistic regression fixes it
- How to train a `LogisticRegression` model directly on top of Session 18's preprocessing pipeline
- How `predict_proba()` gives you a probability, not just a yes/no answer
- How adjusting the classification threshold changes which mistakes your model makes
- The difference between binary and multiclass classification

---

## A. From Predicting a Number to Predicting a Probability

**💡 Analogy:** Recall Session 17's Swiggy churn question — will this partner churn, yes or no? If we tried to answer this with plain linear regression, nothing would stop it from predicting nonsense values like `-0.3` or `1.4` — numbers that don't correspond to any sensible "probability of churning." We need something that always outputs a valid probability, between 0 and 1, no matter what.

**One-line definition: Logistic regression uses a mathematical function (the sigmoid) to squash any raw prediction into a valid probability between 0 and 1.**

**Worked example:** Think of the sigmoid as a pressure valve: no matter how strong the raw internal "score" going in, the output that comes out is always capped between 0 and 1 — this is what makes the output interpretable as a genuine probability rather than an arbitrary number.

**⚠️ Common trap:** Despite the name, logistic regression is a **classification** technique, not a regression one — the "regression" in the name is a historical artifact of how the underlying math developed, not a hint about what kind of problem it solves.

---

## B. Training LogisticRegression on the Session 18 Pipeline

**💡 Analogy:** Session 18 built an assembly line — wash, chop, cook, but never plate. Today, we finally attach the last station: the decision-maker.

```python
from sklearn.linear_model import LogisticRegression

pipeline = Pipeline(steps=[
    ("preprocessing", preprocessor),   # from Session 18
    ("classifier", LogisticRegression()),
])

pipeline.fit(X_train, y_train)
```

**Worked example:** Using the exact same `city`, `vehicle_type`, `orders_last_30_days`, `avg_rating`, and `months_active` columns from Session 18 — now predicting `churned` — this single `pipeline.fit()` call handles encoding, scaling, *and* training the classifier, all fit only on the training data, exactly as Session 18's leakage rule requires.

**⚠️ Common trap:** Nothing about adding a classifier changes the leakage discipline from Session 18 — `.fit()` still happens only once, on `X_train`, `y_train`. The pipeline handles keeping preprocessing and modeling in the correct order automatically.

---

## C. Interpreting `predict_proba()`

**💡 Analogy:** A weather forecast that says "70% chance of rain" is far more useful than a blunt "it will rain" or "it won't." `predict_proba()` gives you that same richer information for classification — a probability, not just a final yes/no call.

```python
probabilities = pipeline.predict_proba(X_test)
```

**Worked example:** For a given delivery partner, `predict_proba()` might return `[0.82, 0.18]` — an 82% chance of "no churn" and an 18% chance of "churn." `.predict()`, by contrast, just applies a default cutoff (0.5) and returns a single 0 or 1.

**⚠️ Common trap:** `.predict()`'s default 0.5 cutoff isn't a law of nature — it's just a default. Section D shows why changing it matters.

---

## D. Adjusting the Classification Threshold

**💡 Analogy:** Recall Session 17's cost-of-mistakes debate: missing a real churner (false negative) costs a lost partner with zero chance to intervene; flagging someone who wasn't leaving (false positive) wastes a retention incentive. The classification threshold is the exact dial that controls this balance.

**One-line definition: The classification threshold is the probability cutoff above which a prediction is called "positive" — lowering it catches more true positives but also more false alarms; raising it does the opposite.**

**Worked example, using our Swiggy churn model:**

| Threshold | Precision | Recall |
|---|---|---|
| 0.3 (lower — more cautious about missing churners) | 0.57 | 0.89 |
| 0.5 (default) | 0.83 | 0.56 |
| 0.7 (higher — more cautious about false alarms) | 1.00 | 0.11 |

At threshold 0.3, we catch 89% of actual churners, but only 57% of our "will churn" flags turn out correct. At threshold 0.7, every flag we raise is correct (100% precision), but we catch only 11% of actual churners.

**⚠️ Common trap:** There's no universally "correct" threshold — like `alpha` in Session 21, it must be chosen based on which mistake costs the business more, exactly the debate we had in Session 17.

---

## E. Binary vs. Multiclass Classification

**💡 Analogy:** Our churn question is **binary** — churn or no churn, exactly two outcomes. But imagine instead classifying each partner into "loyal," "at-risk," or "churned" — three categories, none of which is naturally "more positive" than another. That's **multiclass** classification.

**One-line definition: Binary classification has exactly two possible outcomes; multiclass classification has three or more.**

`LogisticRegression` handles both — for multiclass problems, it internally trains multiple binary comparisons (a strategy sometimes called one-vs-rest) and combines them, though the details are outside today's scope.

**⚠️ Common trap:** Don't confuse multiclass classification (multiple categories, one correct answer per row) with multi-label classification (multiple correct answers can apply to the same row) — the second is a different, more advanced problem we won't cover today.

---

## Quick Reference — Reading a Logistic Regression Model

| Your situation | Use this | Because |
|---|---|---|
| You need a probability, not just yes/no | `predict_proba()` | Returns the underlying probability for each class |
| You need a final yes/no decision at the default cutoff | `predict()` | Applies the standard 0.5 threshold automatically |
| Missing a positive case is costly | Lower the threshold | Increases recall, catches more true positives (at the cost of more false alarms) |
| False alarms are costly | Raise the threshold | Increases precision, reduces false alarms (at the cost of missing more true positives) |
| Your target has 3+ unordered categories | Multiclass classification | Binary classification only handles exactly two outcomes |

---

## Practice Exercises

1. **Concept Detective** — Why can't we just use Session 20's `LinearRegression` directly on a 0/1 churn label instead of `LogisticRegression`?

2. **Real-Life Application** — An HDFC fraud-detection model returns `predict_proba() = [0.35, 0.65]` for a transaction. In plain language, what does this mean, and what would `.predict()` return at the default threshold?

3. **Spot the Error** — A classmate says "I lowered my threshold and now my model is just better." What's incomplete about this claim?

4. **Pattern Recognition** — Using the threshold table in section D, describe in one sentence what happens to precision and recall as the threshold rises from 0.3 to 0.7.

5. **Planning Ahead** — A hospital wants to flag patients at risk of a rare but serious condition. Would you recommend a lower or higher classification threshold, and why, in terms of which mistake is more costly here?

---

> ✅ **You're done!** You can now explain why logistic regression squashes predictions into valid probabilities, train a classifier on top of a preprocessing pipeline, interpret `predict_proba()` output, adjust the classification threshold deliberately, and distinguish binary from multiclass classification.
>
> Next up: **Session 23 — Classification Metrics**, where we formally measure exactly what today's threshold choices trade off, using the confusion matrix, precision, recall, and F1.
