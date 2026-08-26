# Lecture Script: Logistic Regression
> **Instructor Reference** — Module 2: Classical ML | Session 6 | Duration: 2 Hours

---

## Session Overview

**Goal:** Students train `LogisticRegression` on a real loan-approval dataset, interpret `predict_proba()`, adjust the classification threshold and explain its effect, and distinguish binary from multiclass classification.

**Student profile at this point:** Comfortable with `LinearRegression`, coefficients, and regularization from Sessions 4-5. This is their first classifier — the shift from predicting a number to predicting a probability needs careful framing.

**Key outcome:** Every student trains a binary classifier on `loan_applications.csv`, prints probabilities (not just labels), demonstrates how predictions change under two different thresholds, and can explain in one paragraph why scikit-learn's `LogisticRegression` needs no special configuration to handle a 3+ class target.

**Dataset for this session:** `loan_applications.csv` (in this folder) — 30 rows of `applicant_id`, `age`, `income_k`, `credit_score`, `employment_type`, `loan_amount_k`, `approved`.

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| SEGMENT 1: Opening — Numbers vs Categories | 10 min | 0:10 |
| SEGMENT 2: Sigmoid Intuition & Fit/Predict | 20 min | 0:30 |
| SEGMENT 3: predict_proba() Deep Dive | 20 min | 0:50 |
| **BREAK** | 10 min | 1:00 |
| SEGMENT 4: Adjusting the Threshold | 25 min | 1:25 |
| SEGMENT 5: Binary vs Multiclass | 15 min | 1:40 |
| SEGMENT 6: Lab — Threshold Tuning on loan_applications.csv | 15 min | 1:55 |
| SEGMENT 7: Summary, Wrap-Up & Q&A | 5 min | 2:00 |

---

## SEGMENT 1: Opening — Numbers vs Categories (10 min)

### The Naive Attempt (6 min)

**Say:** *"For the last three sessions, every model we trained predicted a NUMBER — a price. Today, we predict a CATEGORY — will this loan be approved or not. Let's see what goes wrong if we naively reuse `LinearRegression` for this."*

**Live-code the naive attempt:**

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

df = pd.read_csv("loan_applications.csv")
X = df[["age", "income_k", "credit_score", "loan_amount_k"]]
y = df["approved"]   # 0 or 1

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

naive = LinearRegression()
naive.fit(X_train, y_train)
naive_preds = naive.predict(X_test)
print(naive_preds)
```

**Run it and read the printed predictions aloud.** **Say:** *"Look closely — some of these predictions are BELOW 0 or ABOVE 1. What does a predicted probability of -0.15 or 1.3 even mean? Nothing sensible — probabilities have to live between 0 and 1, and plain linear regression has no way to enforce that boundary."*

**Ask:** *"What would we need to change about the shape of our prediction function to guarantee outputs always stay between 0 and 1?"* Let students speculate for a moment before revealing the sigmoid function.

### Introducing the Sigmoid (4 min)

**Draw an S-shaped curve on the board** — flat near 0 for very negative inputs, flat near 1 for very positive inputs, steep through the middle around input 0.

**Say:** *"This S-shaped curve is called the sigmoid function. Instead of predicting `y = mx + c` directly as our final answer, logistic regression computes `mx + c` first (exactly the same linear combination as before) and then SQUASHES that result through the sigmoid curve, guaranteeing the final output always lands between 0 and 1 — a valid probability."*

**Say:** *"This is the whole trick. Everything else — coefficients, fitting, even `LinearRegression`'s underlying math — carries over. We're just adding one squashing step at the very end."*

**Learning contract for today — write on board:**

- Explain why a squashing function is needed to predict probabilities
- Train `LogisticRegression` and read both `.predict()` and `.predict_proba()`
- Adjust the classification threshold and explain the tradeoff it creates
- Distinguish binary from multiclass classification

---

## SEGMENT 2: Sigmoid Intuition & Fit/Predict (20 min)

### Fitting the Real Classifier (10 min)

**Say:** *"Let's fit the real thing now."*

```python
from sklearn.linear_model import LogisticRegression

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

predictions = model.predict(X_test)
print(predictions)
print("Test accuracy:", model.score(X_test, y_test))
```

**Run it.** **Say:** *"Notice `stratify=y` is back from Session 1 — this dataset's `approved` column is roughly balanced but on a small sample, so we keep that habit regardless."*

**Ask:** *"Why did we set `max_iter=1000` here, when `LinearRegression` needed no such setting?"* Guide toward: unlike plain linear regression's closed-form shortcut, `LogisticRegression` is fit ITERATIVELY, using an algorithm closely related to the gradient descent we hand-built in Session 3. `max_iter` caps how many iterations the solver is allowed before giving up, and small or oddly-scaled data sometimes needs more than the default.

### Connecting Back to Session 3's Gradient Descent (6 min)

**Say:** *"This is a great moment to connect back to our master class. Remember, gradient descent works by walking downhill on an error curve. `LogisticRegression`'s solver does exactly that — except instead of minimizing squared error like plain linear regression, it minimizes a different error measure suited to probabilities, called log loss. The MECHANISM — compute a gradient, take a small step, repeat — is identical to what we hand-built in Session 3."*

**Ask:** *"If we tried to minimize squared error directly on probabilities the way we did for `LinearRegression`, do you think that would work well? Why might a different error measure be more natural for a 0-1 output?"* Let students speculate; there's no need to derive log loss formally — the goal is just to plant the idea that "probabilities need their own kind of error measure," which log loss provides.

### Coefficients Still Exist (4 min)

```python
for feature, coef in zip(X.columns, model.coef_[0]):
    print(f"{feature}: {coef:.4f}")
print(f"Intercept: {model.intercept_[0]:.4f}")
```

**Run it.** **Say:** *"Notice `model.coef_` is now a 2D array (hence `[0]`), because scikit-learn's API keeps the door open for multiclass problems, which we'll see in SEGMENT 5. The interpretation is similar in spirit to Session 4 — a positive coefficient means that feature PUSHES the prediction toward the positive class, but the exact size no longer translates to 'lakhs of price' — it's now on a log-odds scale, which is a nuance we'll set aside for this course and instead focus on the more intuitive `predict_proba()` output."*

---

## SEGMENT 3: predict_proba() Deep Dive (20 min)

### Reading the Output (8 min)

**Say:** *"`.predict()` only gives you the final yes/no decision. `predict_proba()` gives you the actual CONFIDENCE behind that decision — much more useful for real business decisions."*

```python
probabilities = model.predict_proba(X_test)
print(probabilities[:8])
```

**Run it and read a few rows aloud.** **Say:** *"Each row has two numbers: probability of class 0 (rejected) and probability of class 1 (approved). They always sum to 1, since exactly one of the two outcomes must happen."*

```python
positive_probs = model.predict_proba(X_test)[:, 1]
print(positive_probs[:8])

for actual, pred, prob in zip(y_test.values[:8], model.predict(X_test)[:8], positive_probs[:8]):
    print(f"actual={actual}, predicted={pred}, P(approved)={prob:.3f}")
```

**Run it.** **Say:** *"Look for rows where the probability is close to 0.5 — those are the model's genuinely UNCERTAIN cases, versus rows where the probability is close to 0 or 1, where the model is highly confident. `.predict()` alone throws away this crucial distinction."*

### Why This Matters for Business Decisions (6 min)

**Ask:** *"Imagine two loan applicants: one gets P(approved) = 0.51, the other gets P(approved) = 0.98. `.predict()` labels BOTH as 'approved.' Does that feel right for a bank making real lending decisions?"* Guide toward: no — a human loan officer would likely want to review the 0.51 case manually, while the 0.98 case can be auto-approved with confidence. This distinction is invisible if you only look at `.predict()`.

**Say:** *"This is exactly why production ML systems almost always work with probabilities directly, using `predict_proba()`, rather than the hard label from `.predict()`. The hard label is really just `predict_proba() >= 0.5` — a threshold decision we ourselves can control, which is exactly SEGMENT 4's topic."*

### Confidence Distribution Across the Test Set (6 min)

```python
import numpy as np

print("Min probability:", positive_probs.min())
print("Max probability:", positive_probs.max())
print("How many rows are 'uncertain' (0.4-0.6)?", ((positive_probs >= 0.4) & (positive_probs <= 0.6)).sum())
```

**Run it.** **Say:** *"This kind of quick summary is a useful sanity check on any classifier — if EVERY prediction came out close to 0.5, that would be a red flag that the model isn't learning much of a real signal from the features."*

---

## BREAK (10 min)

*Suggested break prompt:* Ask students to think of one real product (banking app, hiring tool, medical app) where they'd want the decision threshold set LOWER than 0.5, and one where they'd want it set HIGHER. Come back ready to share.

---

## SEGMENT 4: Adjusting the Threshold (25 min)

### The Default Threshold Isn't Sacred (5 min)

**Say:** *"`.predict()` uses 0.5 as its cutoff by default: probability at or above 0.5 becomes the positive class, below becomes negative. But 0.5 isn't a law of nature — it's just scikit-learn's default, and we're free to override it based on the business context."*

### Live Demo — Comparing Two Thresholds (12 min)

```python
probs = model.predict_proba(X_test)[:, 1]

threshold_low = 0.3
threshold_high = 0.7

preds_low = (probs >= threshold_low).astype(int)
preds_high = (probs >= threshold_high).astype(int)

print("Default (0.5) approvals:", model.predict(X_test).sum())
print("Threshold 0.3 approvals:", preds_low.sum())
print("Threshold 0.7 approvals:", preds_high.sum())
```

**Run it and compare all three counts.** **Say:** *"Notice the pattern: LOWER threshold approves MORE applicants (we're being more lenient about what counts as 'confident enough'). HIGHER threshold approves FEWER (we're demanding more confidence before saying yes)."*

**Ask:** *"For a bank worried mainly about approving loans that later DEFAULT, would they want to move the threshold up or down from 0.5?"* Guide toward: UP — a higher threshold means the model must be more confident before approving, reducing risky approvals, at the cost of also rejecting some applicants who genuinely would have repaid.

**Ask the reverse:** *"For a business that wants to maximize how many customers get a 'yes' — perhaps a low-stakes trial signup, not a loan — would they want the threshold up or down?"* Guide toward: DOWN — more lenient, more approvals, accepting more risk of a 'wrong yes.'

### The Underlying Tradeoff (5 min)

**Write this on the board:**

```
Lower threshold  -> more positives predicted -> catches more TRUE positives,
                                                  but also more FALSE positives
Higher threshold -> fewer positives predicted -> fewer FALSE positives,
                                                  but risks missing TRUE positives
```

**Say:** *"This exact tension — catching more true positives vs. avoiding false positives — is EXACTLY what Session 7's precision and recall formalize into precise numbers. Today, just get comfortable with the DIRECTION of the tradeoff: threshold up trades recall for precision; threshold down trades precision for recall."*

### Visualizing the Threshold Sweep (3 min)

```python
for t in [0.1, 0.3, 0.5, 0.7, 0.9]:
    count = (probs >= t).astype(int).sum()
    print(f"threshold={t}: {count} applicants approved out of {len(probs)}")
```

**Run it and read the counts, noting the clear downward trend as threshold rises.**

---

## SEGMENT 5: Binary vs Multiclass (15 min)

### The Distinction (5 min)

**Say:** *"Everything so far has been BINARY — exactly two classes, approved or rejected. Many real problems have THREE OR MORE mutually exclusive categories — think 'low risk,' 'medium risk,' 'high risk' instead of just 'approved/rejected.' This is MULTICLASS classification."*

### Live Demo — A Synthetic Multiclass Target (8 min)

**Say:** *"Let's manufacture a 3-class version of this problem, purely to see scikit-learn handle it, since our real dataset is binary."*

```python
import numpy as np

# Manufacture a 3-class risk tier purely for this demo
np.random.seed(0)
risk_tier = pd.cut(df["credit_score"], bins=[0, 650, 750, 1000], labels=["high_risk", "medium_risk", "low_risk"])
X_multi = df[["age", "income_k", "loan_amount_k"]]
y_multi = risk_tier

X_train_m, X_test_m, y_train_m, y_test_m = train_test_split(
    X_multi, y_multi, test_size=0.3, random_state=42, stratify=y_multi
)

multi_model = LogisticRegression(max_iter=1000)
multi_model.fit(X_train_m, y_train_m)

print(multi_model.classes_)
print(multi_model.predict(X_test_m)[:5])
print(multi_model.predict_proba(X_test_m)[:5])
```

**Run it.** **Say:** *"Look at `multi_model.classes_` — three categories now, not two. And `predict_proba()` returns THREE numbers per row instead of two, one per class, still summing to 1. We changed absolutely nothing about how we called `LogisticRegression` — scikit-learn detected the 3-class target automatically and adjusted its internal strategy."*

**Ask:** *"If `predict_proba()` for one applicant returned `[0.1, 0.3, 0.6]` for `[high_risk, medium_risk, low_risk]`, what would `.predict()` return?"* (Answer: `low_risk` — the class with the highest probability.)

### Threshold Tuning Doesn't Work the Same Way for Multiclass (2 min)

**Say, briefly:** *"Notice our SEGMENT 4 threshold trick — comparing one probability to a single cutoff — doesn't directly generalize to 3+ classes the same simple way, since `.predict()` there just picks whichever class has the HIGHEST probability among three or more options, not a single yes/no cutoff. Threshold tuning in a multiclass setting is a more advanced topic we won't need for this course, which focuses on binary classification from here through Session 12."*

---

## SEGMENT 6: Lab — Threshold Tuning on loan_applications.csv (15 min)

### Instructions (read aloud, step by step)

1. Load `loan_applications.csv`, split `X` (`age`, `income_k`, `credit_score`, `loan_amount_k`) and `y` (`approved`) with `train_test_split(test_size=0.3, random_state=42, stratify=y)`.
2. Train a `LogisticRegression(max_iter=1000)`.
3. Print `predict_proba()` for the first 5 test rows alongside their actual labels.
4. Compute predictions at threshold 0.3, default 0.5, and 0.8. Print the count of approvals at each.
5. Write one sentence: for a bank that wants to be VERY cautious about defaults, which of these three thresholds would you recommend, and why?

### Starter Code

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

df = pd.read_csv("loan_applications.csv")
X = df[["age", "income_k", "credit_score", "loan_amount_k"]]
y = df[___]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=___, random_state=42, stratify=___)

model = ___(max_iter=1000)
model.fit(___, ___)

probs = model.predict_proba(X_test)[:, 1]
for actual, prob in zip(y_test.values[:5], probs[:5]):
    print(f"actual={actual}, P(approved)={prob:.3f}")

for t in [0.3, 0.5, 0.8]:
    count = (probs >= t).astype(int).sum()
    print(f"threshold={t}: {count} approvals")

# TODO: write your one-sentence threshold recommendation here as a comment
```

### Reference Solution

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

df = pd.read_csv("loan_applications.csv")
X = df[["age", "income_k", "credit_score", "loan_amount_k"]]
y = df["approved"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)

model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

probs = model.predict_proba(X_test)[:, 1]
for actual, prob in zip(y_test.values[:5], probs[:5]):
    print(f"actual={actual}, P(approved)={prob:.3f}")

for t in [0.3, 0.5, 0.8]:
    count = (probs >= t).astype(int).sum()
    print(f"threshold={t}: {count} approvals")

# Recommendation: a bank very cautious about defaults should prefer the
# higher threshold (0.8) -- it approves only the applicants the model is
# most confident about, reducing risky approvals, at the cost of rejecting
# some borderline-but-genuine applicants.
```

**Instructor circulates**, checking that students correctly apply the threshold to `predict_proba()`'s output (not `.predict()`'s output), and that their recommendation sentence explicitly reasons about the tradeoff rather than just picking a number.

---

## SEGMENT 7: Summary, Wrap-Up & Q&A (5 min)

**What we covered today:**
- Why plain `LinearRegression` fails for categorical targets, and how the sigmoid function fixes it
- `LogisticRegression` fit/predict, connected back to Session 3's gradient descent intuition
- `predict_proba()` gives probabilities; `.predict()` is just a 0.5-threshold shortcut on top of it
- Adjusting the threshold trades false positives against false negatives
- Binary vs multiclass — scikit-learn handles both with the same API, detected automatically from `y`

**Bridge to next session:** *"Today you learned to read a classifier's confidence and control its decision boundary. Next session, we build a full measurement toolkit — confusion matrix, precision, recall, F1 — to formally quantify the tradeoff you explored today by eye, and to pick the RIGHT metric for a given business problem."*

**Homework / self-practice:**
1. Retrain the model using only `credit_score` and `income_k` as features (drop `age` and `loan_amount_k`). Compare the approval counts at threshold 0.5 to today's four-feature model.
2. Sweep thresholds from 0.1 to 0.9 in steps of 0.1 and plot (or tabulate) approval count at each — describe the shape of this curve in one sentence.
3. For the multiclass demo in SEGMENT 5, print `multi_model.coef_.shape` and explain in one sentence why it has more rows than the binary model's `coef_`.

---

## Q&A & Doubt Solving

**Likely questions and suggested answers:**

**Q: Is `LogisticRegression` regularized by default, like Ridge from last session?**
→ Yes — scikit-learn's `LogisticRegression` applies L2 regularization by default, controlled by a parameter called `C`, which is the INVERSE of `alpha` (so smaller `C` means stronger regularization, the opposite direction from Ridge's `alpha`). This is worth flagging explicitly since the inverted convention trips people up.

**Q: Why can't we just use `.predict()` and skip `predict_proba()` entirely?**
→ You can, if you're happy with the default 0.5 threshold. But as SEGMENT 4 demonstrated, real business problems often need a DIFFERENT threshold, and you can only apply a custom one by working with `predict_proba()`'s raw probabilities first.

**Q: If I pick a very extreme threshold, like 0.99, what happens?**
→ The model becomes extremely conservative, likely approving very few or even zero applicants — useful only in scenarios where a false positive is catastrophically costly and a very high rejection rate is acceptable.

**Q: Does the sigmoid function get used anywhere else besides logistic regression?**
→ Yes — it's a fundamental building block in neural networks too, often as an "activation function" in various forms. Recognizing it here gives you a head start on later, more advanced material.

**Q: In the multiclass demo, does scikit-learn train three completely separate models internally?**
→ Conceptually, yes, in one common strategy (called "one-vs-rest") — a separate binary classifier per class, each asking "is it THIS class or not," with probabilities normalized to sum to 1 across all classes. Some solvers use a more integrated "multinomial" approach instead. Either way, this happens automatically; you don't need to configure it.

**Q: Why did we need `stratify=y` again today, given the loan dataset looks fairly balanced?**
→ Good habit-forming regardless of exact balance — with only 30 rows, even a roughly-balanced target can drift unevenly across train/test without `stratify`, echoing the Session 1 demonstration.

---

## Instructor Notes

- **Prerequisite check:** Confirm students recall Session 3's gradient descent vocabulary (iterative solving, `max_iter`-style stopping) — SEGMENT 2 leans on this connection explicitly.
- **Common mistake:** Confusing `.predict()`'s hard label with an actual probability — reinforced by printing them side by side in SEGMENT 3 every time this comes up.
- **Another common mistake:** Applying a custom threshold to `.predict()`'s OUTPUT instead of `predict_proba()`'s output. Watch for this explicitly during the SEGMENT 6 lab.
- **Engagement tip:** SEGMENT 4's "which direction would a cautious bank move the threshold" discussion tends to generate the most spontaneous class debate of the session — let it run a little long if energy is high, trimming SEGMENT 5's multiclass demo instead if needed.
- **Time check:** If running behind before the break, shorten SEGMENT 3's "confidence distribution" mini-demo to a single printed statistic instead of three.
- **If running long after the break:** Compress SEGMENT 5 to just the `classes_` and `predict_proba()` shape observations, skipping the deeper "why doesn't threshold tuning generalize" discussion.
- **Materials to prepare:** `loan_applications.csv` open and ready; a pre-typed notebook with the naive `LinearRegression` failure demo ready to run first for maximum impact.

---

## Common Errors — Quick Reference

| Bug / mistake | Symptom | Fix |
|---|---|---|
| Using `LinearRegression` for a categorical target | Predictions fall outside [0, 1], nonsensical as probabilities | Use `LogisticRegression` instead |
| Treating `.predict()`'s output as a probability | Confusion when trying to apply a custom threshold | Use `predict_proba()` for any probability-based logic |
| Applying a threshold to `.predict()`'s output instead of `predict_proba()`'s | Thresholding has no effect, or errors out | Threshold the probability column directly: `(probs >= t).astype(int)` |
| Forgetting `max_iter` on a solver that needs more iterations | `ConvergenceWarning` printed, potentially unreliable coefficients | Increase `max_iter` (e.g. to 1000 or higher) |
| Assuming multiclass needs special configuration | Unnecessary extra code or confusion | scikit-learn detects multiclass automatically from `y`'s unique values |

---

## Appendix: Threshold Sweep Reference Table (Instructor Reference)

For a hypothetical set of 20 test applicants with varying true approval status:

| Threshold | Typical approvals | Typical tradeoff |
|---|---|---|
| 0.1 | Most applicants approved | High recall, low precision — many false approvals |
| 0.5 (default) | Balanced | The "no special business context" default |
| 0.9 | Very few applicants approved | High precision, low recall — misses many true approvals |

---

## Appendix: Supplemental Practice Bank (Optional, If Time Allows)

### Drill 1 — Reading predict_proba() output

For each printed probability pair `[P(class 0), P(class 1)]`, state what `.predict()` would return:

1. `[0.2, 0.8]` → 1
2. `[0.65, 0.35]` → 0
3. `[0.49, 0.51]` → 1
4. `[0.5, 0.5]` → depends on scikit-learn's tie-breaking convention (worth a brief note that exact ties are rare with continuous probabilities)

### Drill 2 — Threshold direction reasoning

For each scenario, state whether the threshold should move UP or DOWN from 0.5:

1. A cancer-screening classifier, where missing a real case is dangerous → DOWN (catch more true positives, accept more false alarms)
2. A promotional email opt-in classifier, where false positives just waste a marketing email → DOWN is often fine, business-dependent
3. A parole-recommendation classifier, where a wrong "safe to release" prediction is very costly → UP (demand more confidence before predicting positive)

---

## FAQ — Additional Questions

**Q: Does `LogisticRegression`'s coefficient sign mean the same thing as `LinearRegression`'s did in Session 4?**
→ The DIRECTION is the same idea — positive means "pushes toward the positive class," negative means "pushes toward the negative class" — but the MAGNITUDE is on a different (log-odds) scale, so you can't directly compare a logistic regression coefficient's size to a linear regression coefficient's size the way we did with lakhs in Session 4.

**Q: Is there a way to see WHICH threshold is "best" instead of just picking one intuitively, like we did today?**
→ Yes — Session 7's precision-recall curve and F1 score give you precise, numeric ways to evaluate different thresholds, rather than reasoning about them purely qualitatively as we did today. Today built the intuition; next session adds the measurement tools.

**Q: If I have severely imbalanced classes (say 95% class 0, 5% class 1), does 0.5 still make sense as a default threshold?**
→ Often not — with severe imbalance, a model can achieve high "accuracy" by predicting the majority class almost every time, and the meaningful decision threshold often needs to be tuned well below 0.5 to catch enough of the rare positive class. This exact scenario is central to Session 7.

**Q: Can I train logistic regression with more than one feature type, like the categorical `employment_type` column in `loan_applications.csv`?**
→ Yes — exactly as in Session 2, you'd encode `employment_type` with a `OneHotEncoder` inside a `ColumnTransformer`/`Pipeline` before fitting. We used only numeric features today to keep focus on the classifier's new concepts, but combining today's model with Session 2's preprocessing skills is a natural next step, and a great homework extension.

---

## SEGMENT 8: Supplemental Code Demos (Instructor Optional, If Time or Advanced Group)

### Demo A — Logistic regression with the categorical employment_type feature (6 min)

```python
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

numeric_features = ["age", "income_k", "credit_score", "loan_amount_k"]
categorical_features = ["employment_type"]

preprocessor = ColumnTransformer(transformers=[
    ("num", StandardScaler(), numeric_features),
    ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
])

full_pipe = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("model", LogisticRegression(max_iter=1000)),
])

X_full = df[numeric_features + categorical_features]
X_train_f, X_test_f, y_train_f, y_test_f = train_test_split(
    X_full, y, test_size=0.3, random_state=42, stratify=y
)
full_pipe.fit(X_train_f, y_train_f)
print("Test accuracy with employment_type included:", full_pipe.score(X_test_f, y_test_f))
```

**Break it down:**
- This directly reuses Session 2's `ColumnTransformer`/`Pipeline` pattern, now paired with a classifier instead of a regressor
- `StandardScaler` matters more here than it did for plain `LinearRegression`, since `LogisticRegression`'s default L2 regularization penalizes coefficient size, and unscaled features would be penalized unevenly
- Comparing this accuracy to the four-numeric-feature model from earlier tells you whether `employment_type` adds real predictive value

**Ask:** Why is scaling especially important here, given LogisticRegression's default regularization?

**Common mistake:** Skipping scaling because "it worked fine without it for LinearRegression in Session 4."

**Fix:** Always scale features before any regularized model (Ridge, Lasso, or default LogisticRegression).

### Demo B — Visualizing the sigmoid function directly (5 min, requires matplotlib)

```python
import numpy as np
import matplotlib.pyplot as plt

def sigmoid(z):
    return 1 / (1 + np.exp(-z))

z_values = np.linspace(-10, 10, 200)
probabilities = sigmoid(z_values)

plt.plot(z_values, probabilities)
plt.axhline(y=0.5, linestyle="--", color="gray")
plt.axvline(x=0, linestyle="--", color="gray")
plt.xlabel("z = m1*x1 + m2*x2 + ... + c (before squashing)")
plt.ylabel("Predicted probability")
plt.title("The sigmoid function")
plt.show()
```

**Break it down:**
- This is the exact S-shaped curve drawn on the board in SEGMENT 1, now generated from the real formula
- Notice `z=0` maps to probability exactly 0.5 — the "undecided" point
- Far-negative `z` flattens toward 0, far-positive `z` flattens toward 1 — this flattening is WHY logistic regression's raw linear combination can range anywhere, but the final probability always stays bounded

**Ask:** What value of z would produce a probability very close to (but not exactly) 1?

**Common mistake:** Assuming the sigmoid can output exactly 0 or exactly 1.

**Fix:** Mathematically, the sigmoid only approaches 0 and 1 as limits — it can get arbitrarily close but technically never reaches them exactly, though floating-point rounding may display it as exactly 0.0 or 1.0 in practice for extreme inputs.

### Demo C — Manually computing one prediction's probability (5 min)

```python
sample_row = X_test.iloc[[0]]
manual_z = (model.coef_[0] * sample_row.values[0]).sum() + model.intercept_[0]
manual_prob = sigmoid(manual_z)

sklearn_prob = model.predict_proba(sample_row)[0, 1]

print(f"Manually computed probability: {manual_prob:.4f}")
print(f"sklearn's predict_proba:       {sklearn_prob:.4f}")
```

**Break it down:**
- This proves `predict_proba()` isn't a mysterious black box — it's exactly `sigmoid(coefficients · features + intercept)`, computed by hand here and matched against scikit-learn's own output
- The two numbers should match (up to floating-point precision)
- This is a strong closing demo for skeptical or curious students who want to see "under the hood"

**Ask:** If we changed one feature value slightly for this row, would you expect the probability to change smoothly or in a sudden jump?

**Common mistake:** Assuming logistic regression's decision boundary is a hard step function.

**Fix:** The sigmoid is smooth everywhere — small feature changes produce small, gradual probability changes, never sudden jumps (the DECISION from `.predict()` can flip suddenly at the threshold, but the underlying probability itself moves smoothly).

---

## Materials Checklist

- [ ] `loan_applications.csv` open and readable in the working notebook environment
- [ ] Pre-typed notebook with the naive `LinearRegression`-on-categorical-target failure demo ready to run first
- [ ] Whiteboard space for the sigmoid curve sketch
- [ ] Optional: matplotlib available for Demo B's sigmoid visualization
- [ ] Timer visible for the lab segment

---

## Timing Contingencies

| Situation | Action |
|---|---|
| Running 10 min behind before break | Shorten SEGMENT 3's confidence-distribution mini-demo to a single printed statistic |
| Running long after break | Compress SEGMENT 5 to just `classes_` and `predict_proba()` shape observations |
| Low energy after lunch/break | Run Appendix Drill 1 (reading predict_proba output) as a quick energizer |
| Advanced group finishes lab early | Assign Demo A or Demo C from SEGMENT 8 as a stretch task |
| No shared screen / projector issue | Read code blocks aloud and have students type along from the printed lecture script |

---

## End-of-Session Quiz (5 Questions)

1. Why can't plain `LinearRegression` be used directly to predict a 0/1 target reliably?
2. What does `predict_proba()` return that `.predict()` does not?
3. If you raise the classification threshold from 0.5 to 0.8, do you expect more or fewer positive predictions?
4. What must change in your code to move from binary to multiclass logistic regression?
5. What does `model.coef_[0]` represent for a binary LogisticRegression model?

**Answer key (instructor):**
1. Its raw output isn't bounded between 0 and 1, so predictions can fall outside the valid range for a probability.
2. The actual probability/confidence behind the prediction, not just the final hard label.
3. Fewer — a higher threshold demands more confidence before predicting positive.
4. Nothing — scikit-learn's `LogisticRegression` detects the number of classes automatically from `y`.
5. The learned weight for each feature, on a log-odds scale, indicating how strongly that feature pushes toward the positive class.

---

## Homework Rubric

| Criterion | Excellent (4) | Good (3) | Needs Work (2) | Incomplete (1) |
|---|---|---|---|---|
| Two-feature model comparison | Correct retrain, clear comparison of approval counts | Retrain done, thin comparison | Partial attempt | Not attempted |
| Threshold sweep 0.1-0.9 | Full sweep tabulated/plotted with a correct shape description | Sweep done, thin description | Partial sweep | Not attempted |
| Multiclass coef_ shape explanation | Correct shape reported with a clear, correct explanation | Correct shape, thin explanation | Shape reported, no explanation | Not attempted |

**Total:** /12 — Pass threshold: 8/12

---

## Appendix: Extended Practice Bank (Optional Take-Home or Fast-Finisher Set)

### Bank 1 — Threshold and count reasoning

Given predicted probabilities `[0.15, 0.42, 0.55, 0.68, 0.91]` for five applicants:

| Threshold | Number approved |
|---|---|
| 0.5 | 3 (0.55, 0.68, 0.91) |
| 0.6 | 2 (0.68, 0.91) |
| 0.9 | 1 (0.91) |

**Instructor note:** Have students compute this table themselves before revealing it, using only the five probabilities above.

### Bank 2 — Binary vs multiclass identification

For each scenario, state whether it is binary or multiclass:

1. Predicting whether an email is spam or not → Binary
2. Predicting whether a wine is low/medium/high quality → Multiclass
3. Predicting whether a transaction is fraudulent → Binary
4. Predicting which of five product categories a customer will buy from next → Multiclass

### Bank 3 — Sigmoid output estimation (no calculator needed)

For each rough `z` value, estimate whether the sigmoid output is closer to 0, 0.5, or 1:

1. `z = -8` → close to 0
2. `z = 0.1` → close to 0.5
3. `z = 6` → close to 1

---

## Closing Instructor Reflection Notes

- This session is the pivot point of the module — every remaining session (Metrics, Trees, Ensembles, Validation, Clustering) assumes comfort with `predict_proba()` and threshold thinking established here. Under-investing time in SEGMENT 3 and SEGMENT 4 tends to cost more time in Session 7, when precision/recall need this exact intuition already in place.
- If a cohort is unusually strong technically, Demo C (manually computing one prediction's probability) tends to land very well and can be promoted from "optional" to "core" for that group, since it demystifies `predict_proba()` completely.
- If a cohort is running behind, the single highest-value cut is SEGMENT 5's multiclass demo — it can be reduced to a verbal mention ("scikit-learn handles 3+ classes automatically, we won't need it for the rest of this binary-classification-focused module") without losing much.
