# Lecture Script: Machine Learning — Logistic Regression
> **Instructor Reference** — Module 2: Classical ML | Academic Session 22 | Duration: 2 Hours | Instructor: Aswath Rao

---

## Session Overview
**Goal:** By the end of this session, students can train a `LogisticRegression` model on top of the Session 18 pipeline, interpret `predict_proba()` output, adjust the classification threshold deliberately, and distinguish binary from multiclass classification.

**Student profile at this point:** Comfortable with `LinearRegression`, MAE/RMSE/R², and regularization from Sessions 20-21. They framed the Swiggy churn problem as classification all the way back in Session 17 but have never actually trained a classifier on it. Likely wrong assumption: several will expect `LogisticRegression` to work like `LinearRegression` with a 0/1 target, not realizing why that breaks down. Boredom risk: low — this closes a loop opened five sessions ago, which should feel satisfying.

**Key outcome:** Students should leave instinctively reaching for `predict_proba()` before `predict()` whenever the actual probability matters more than a blunt yes/no.

> 🎯 **The one sentence this session must land:** *A classifier doesn't just say yes or no — it hands you a probability, and where you draw the line on that probability is a business decision, not a technical default.*

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| Opening — "The Risk Score" | 8 min | 8 min |
| Concept Block 1: From a Number to a Probability | 10 min | 18 min |
| Practical Block 1: Why Raw Regression Breaks for Probabilities | 6 min | 24 min |
| Concept Block 2: Training LogisticRegression on the Pipeline | 12 min | 36 min |
| Practical Block 2: Predict Which Pipeline Step Changes | 6 min | 42 min |
| **BREAK** | 10 min | 52 min |
| Concept Block 3: Interpreting predict_proba() | 10 min | 62 min |
| Practical Block 3: Live Coding Demo (TA Code) | 14 min | 76 min |
| Concept Block 4: Adjusting the Classification Threshold | 14 min | 90 min |
| Practical Block 4: Threshold Tradeoff Table Exercise | 10 min | 100 min |
| Concept Block 5: Binary vs. Multiclass Classification | 10 min | 110 min |
| Summary & Bridge | 5 min | 115 min |
| Q&A & Doubt Solving | 5 min | 120 min |

---

## Opening — "The Risk Score" (8 min)

Open with this, verbatim-ish:

> "All the way back in Session 17, we framed a question: will this Swiggy delivery partner churn? We called it classification, we built a `DummyClassifier` baseline, and we walked away with an uncomfortable number — 91% accuracy that meant almost nothing. Today, five sessions later, we finally train a real classifier on that exact question."

Pause. Ask the room:

> "If I told you the model outputs a number like 0.82 for a given partner, what do you think that number means?"

(Let guesses land — most will correctly guess "probability of churning" or similar.)

> "Exactly — and that's the whole shift today. We're not just getting a yes or no anymore. We're getting a risk score, and it's on us to decide what to do with it."

**Pivot line:** "Everything from Sessions 18 through 21 — the pipeline, the math behind fitting a line, regularization — all of it feeds directly into today. This is where the Session 17 story finally gets its model."

**Context for sessions ahead:** "Next session formally measures exactly what today's threshold choices trade off. Today we build the tool; next session we learn to judge it properly."

---

## Concept Block 1: From a Number to a Probability (10 min)

> "Our churn label is 0 or 1 — binary. What happens if we just throw Session 20's `LinearRegression` at it directly?"

Write on the board:

> "Nothing stops linear regression from predicting -0.3, or 1.4 for a 'probability of churning.' Those numbers are nonsense — a probability has to sit between 0 and 1, always."

> "Logistic regression fixes this with a function called the sigmoid — think of it as a pressure valve. No matter how strong the raw internal score, the sigmoid's output is always squeezed into the 0-to-1 range. That's what makes it a genuine, interpretable probability."

### 🔴 The trap / highest-value moment
> "Despite the name, logistic regression is a classification technique, not a regression one — 'regression' here is a historical naming artifact from how the math was developed, not a hint about the kind of problem it solves. Write this down: *logistic regression classifies; the name is misleading.*"

---

## Practical Block 1: Why Raw Regression Breaks for Probabilities (6 min)

Show a tiny table of 4 partners with a plain `LinearRegression` fit directly to the 0/1 churn label, with at least one predicted value below 0 and one above 1. Ask the room what's wrong with those two specific predictions and why sigmoid fixes it. Cold-call 2 students.

---

## Concept Block 2: Training LogisticRegression on the Pipeline (12 min)

> "Session 18 built an assembly line — wash, chop, cook — but never plated the dish. Today we attach the last station: the decision-maker."

Write the code on the board, building on Session 18's pipeline object:

```python
from sklearn.linear_model import LogisticRegression

pipeline = Pipeline(steps=[
    ("preprocessing", preprocessor),   # from Session 18
    ("classifier", LogisticRegression()),
])

pipeline.fit(X_train, y_train)
```

> "Same `city`, `vehicle_type`, `orders_last_30_days`, `avg_rating`, `months_active` columns from Session 18 — now predicting `churned`. One `.fit()` call handles encoding, scaling, and training, all on training data only."

### 🔴 The trap / highest-value moment
> "Nothing about adding a classifier changes Session 18's leakage discipline. `.fit()` still happens once, on `X_train`, `y_train` only. Write this down: *the pipeline pattern doesn't change just because the last step changed.*"

---

## Practical Block 2: Predict Which Pipeline Step Changes (6 min)

Ask the room: "compared to Session 20's regression pipeline, which step in this pipeline is new, and which steps are completely unchanged?" Quick verbal check — the preprocessing steps (ColumnTransformer, OneHotEncoder, StandardScaler) are identical; only the final estimator changed from `LinearRegression` to `LogisticRegression`.

---

## BREAK (10 min)

---

## Concept Block 3: Interpreting `predict_proba()` (10 min)

> "A weather forecast saying '70% chance of rain' is far more useful than a blunt 'it will rain.' `predict_proba()` gives classification that same richness."

```python
probabilities = pipeline.predict_proba(X_test)
```

> "For one partner, this might return `[0.82, 0.18]` — 82% chance of 'no churn,' 18% chance of 'churn.' `.predict()`, by contrast, just applies a default 0.5 cutoff and hands you a single 0 or 1."

💬 Expect a question: "which column is which?" Welcome it. Say: "By default, `predict_proba()` returns columns in the order of the model's classes — column 0 for class 0, column 1 for class 1. Always check `model.classes_` if you're unsure."

---

## Practical Block 3: Live Coding Demo (TA Code) (14 min)

**Handoff line (must match TA code file's opening comment):** "Let's actually train this classifier and look at real probabilities - same Swiggy churn scenario framed all the way back in Session 17."

Hand off to `ta-code - Session 22 - Logistic Regression.py`, narrating each `# --- EXPLAIN ---` block aloud:

1. Rebuild the Session 17/18-style churn dataset (city, vehicle_type, orders, rating, months, churned)
2. Build the full pipeline (Session 18 preprocessing + `LogisticRegression`)
3. `.fit()` on training data, then call `.predict_proba()` on test data — show several rows of actual probabilities on screen
4. Compare `.predict()`'s default output to the underlying probabilities for the same rows — point out cases sitting close to 0.5, where the "confidence" is genuinely low
5. Print accuracy at the default threshold and compare it explicitly to the Session 17 baseline's 88% "always predict no-churn" accuracy — pause here and let the room react

💬 Expect a question: "so is our new model actually better than the baseline?" Welcome it. Say: "By accuracy, yes — but hold that thought. We haven't yet checked whether it's better where it actually matters: catching real churners. That's next session."

---

## Concept Block 4: Adjusting the Classification Threshold (14 min)

> "Recall Session 17's cost-of-mistakes debate: missing a real churner costs a lost partner with zero chance to intervene; a false alarm wastes a retention incentive. The threshold is the exact dial controlling this balance."

Write the demo's actual threshold table on the board:

| Threshold | Precision | Recall |
|---|---|---|
| 0.3 | 0.57 | 0.89 |
| 0.5 (default) | 0.83 | 0.56 |
| 0.7 | 1.00 | 0.11 |

> "At 0.3, we catch 89% of actual churners, but only 57% of our flags are correct. At 0.7, every flag is correct, but we catch only 11% of actual churners."

### 🔴 The trap / highest-value moment
> "There's no universally correct threshold — like `alpha` in Session 21, it has to be chosen based on which mistake costs the business more. Write this down: *the threshold is a business decision wearing a technical costume.*"

---

## Practical Block 4: Threshold Tradeoff Table Exercise (10 min)

Give students 2 new business scenarios: (1) a hospital screening for a serious but treatable condition, (2) a spam filter for a personal inbox. Ask each pair to decide, for each scenario, whether they'd want a lower or higher threshold than default, and justify in one sentence. Cold-call for both scenarios.

**Answer key reasoning to say aloud:** Hospital screening — lower threshold, since missing a real case (false negative) is far costlier than a false alarm that leads to a follow-up test. Spam filter — higher threshold, since a false positive (real email marked as spam) is often more annoying than a few spam emails getting through.

---

## Concept Block 5: Binary vs. Multiclass Classification (10 min)

> "Our churn question is binary — churn or no churn, exactly two outcomes. But imagine instead classifying partners into 'loyal,' 'at-risk,' or 'churned' — three categories, none more 'positive' than another. That's multiclass."

> "`LogisticRegression` handles both — for multiclass, it internally trains multiple binary comparisons and combines them, a strategy sometimes called one-vs-rest. We won't go deep into the mechanics today."

### 🔴 The trap / highest-value moment
> "Don't confuse multiclass classification — multiple categories, one correct answer per row — with multi-label classification, where multiple correct answers can apply to the same row at once. That's a different, more advanced problem outside today's scope. Write this down: *multiclass = one answer from many options; multi-label = several answers can all be true at once.*"

---

## Summary & Bridge (5 min)

| Concept | The one thing to remember |
|---|---|
| Sigmoid | Squashes any raw score into a valid 0-to-1 probability |
| LogisticRegression on a pipeline | Same leakage discipline as Session 18, just a new final step |
| predict_proba() | Gives the actual probability, richer than predict()'s yes/no |
| Classification threshold | Controls the precision-recall balance; a business decision, not a default |
| Binary vs. multiclass | Two outcomes vs. three or more unordered categories |

Close on the thesis line: "A classifier doesn't just say yes or no — it hands you a probability, and where you draw the line on that probability is a business decision, not a technical default."

**Bridge to next session:** "Today we adjusted the threshold by eye, watching precision and recall shift. Session 23 formalizes exactly this: the confusion matrix, precision, recall, and F1 — the tools to measure, not just eyeball, whether a threshold choice is actually good for the business."

---

## Q&A & Doubt Solving (5 min)

**Q: Why not always use the lowest possible threshold to catch every positive case?**
→ Because that maximizes false alarms too — at the extreme, a threshold of 0 flags everyone as positive, giving perfect recall but useless precision. It's always a tradeoff, not a free win.

**Q: Does `LogisticRegression` support regularization like Session 21?**
→ Yes — it has a built-in penalty parameter (by default, L2-style regularization is already on), controlled similarly to Ridge's `alpha`. We didn't tune it explicitly today, but it's there.

**Q: How is `predict()`'s 0.5 default threshold chosen?**
→ It's simply the natural midpoint of the 0-to-1 probability range — a sensible default when you have no other information, but not something to treat as automatically correct for every business scenario.

**Q: Can I get `predict_proba()` from any classifier?**
→ Most sklearn classifiers support it, including the tree-based models coming in Sessions 25-26, though the deep reasons for why the probabilities are trustworthy can vary between algorithms.

---

## Instructor Notes
- **Words not yet earned:** confusion matrix, precision, recall, F1, precision-recall curve, ROC-AUC — all Session 23. Sample space, conditional probability, Bayes' Theorem — Session 24.
- **Biggest risk in this session:** students walking away thinking "higher accuracy = better model" after seeing the demo's accuracy beat the baseline — deliberately leave this unresolved and hand it to Session 23.
- **Board management:** keep the threshold tradeoff table (0.3 / 0.5 / 0.7) visible from Concept Block 4 through the end of the session.
- **Common confusions, numbered:**
  1. Expecting `LinearRegression` to work fine on a 0/1 target
  2. Treating 0.5 as an objectively "correct" threshold rather than a default
  3. Confusing multiclass with multi-label classification
  4. Assuming higher accuracy automatically means a better classifier (deliberately left open for Session 23)
- **Cross-references:** Session 23 (Classification Metrics) formally measures today's threshold tradeoffs; Session 24 (Master Class: Probability & Counting) explains the mathematical basis of `predict_proba()`'s probabilities via Bayes' Theorem.
- **Local/cultural context notes:** this session closes the loop opened in Session 17 — explicitly remind students this is the same churn dataset and question introduced there, now with a real trained model instead of `DummyClassifier`.
