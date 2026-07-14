# Lecture Script: Classification Foundations
> **Instructor Reference** — Module 2: Classical ML | Session 6 | Duration: 2 Hours

---

## Session Overview

**Goal:** Students train their first classifiers. By the end they will have fitted Logistic Regression, K-Nearest Neighbours and a Decision Tree on the same dataset, compared them on accuracy, read a model's probability output, tuned the overfitting dial on each, and seen a printed decision tree they can explain to a non-technical person.

**Student profile at this point:** They have completed Sessions 1–5. They are fluent in the `fit` / `predict` / `score` workflow, they understand train-test split, overfitting vs underfitting, `StandardScaler`, and they have built and evaluated regression models (RMSE, R², regularisation). They have never predicted a category before today.

**Key outcome:** One notebook containing three trained classifiers on the breast-cancer dataset, a plotted decision boundary, a printed `plot_tree` diagram, and a written one-line answer to "which model would you actually ship, and why?"

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| Opening — The Thermometer and the Traffic Light | 5 min | 0:05 |
| **Concept 1:** Classification vs Regression, and the Decision Boundary | 10 min | 0:15 |
| **Practical 1:** Your first classifier — LogisticRegression end to end | 15 min | 0:30 |
| **Concept 2:** Inside Logistic Regression — Sigmoid, Threshold, Coefficients | 10 min | 0:40 |
| **Practical 2:** predict vs predict_proba, plotting the sigmoid and the boundary | 15 min | 0:55 |
| **BREAK** | 10 min | 1:05 |
| **Concept 3:** K-Nearest Neighbours — the k dial and the scaling trap | 10 min | 1:15 |
| **Practical 3:** KNN with and without scaling, sweeping k | 15 min | 1:30 |
| **Concept 4:** Decision Trees — splits, purity, max_depth, interpretability | 10 min | 1:40 |
| **Practical 4:** plot_tree, the max_depth dial, and the accuracy trap | 10 min | 1:50 |
| Summary & Wrap-Up | 5 min | 1:55 |
| Q&A & Doubt Solving | 5 min | 2:00 |

---

## Opening (5 min)

**Hook:** Put two questions on the board, side by side. Ask the room to answer both out loud.

```
Question A:  How much will this flat in Pune sell for?
Question B:  Will this loan be repaid — yes or no?
```

Then ask: *"You spent the last three sessions building models that answer Question A. What breaks if you point that exact same LinearRegression at Question B?"*

Let them try. Someone will say "it predicts 0.7, and 0.7 is not an answer." Exactly. Push further: *"And what if it predicts 1.4? Or minus 0.3? What is a minus 0.3 loan repayment?"*

**What classification is NOT:**
- Not a different workflow — split, fit, predict, score is unchanged
- Not "regression with rounding" — a model that outputs 1.4 is broken, not nearly right
- Not judged by how *close* you got — there is no partial credit for a wrong label

**What classification IS:**
- Predicting a label from a fixed, finite list instead of a number on a scale
- Drawing a **boundary** through the data so that each side gets a different verdict
- The single most common ML task in industry — spam, fraud, churn, diagnosis, approval

*"Everything today is one idea in three costumes: draw a line between the classes. The three algorithms differ only in what shape of line they are allowed to draw."*

---

## Concept Block 1: Classification vs Regression, and the Decision Boundary (10 min)

### Write on the board

```
REGRESSION       →  predict a NUMBER   →  47.3 lakh
CLASSIFICATION   →  predict a CLASS    →  "repaid" / "defaulted"

Same workflow:  split → fit → predict → score
Only two things change:
    1. the target column  (categories, not numbers)
    2. the metric         (accuracy, not RMSE)
```

| | Regression | Classification |
|---|---|---|
| Target | Continuous number | Discrete label |
| Model examples | `LinearRegression`, `Ridge` | `LogisticRegression`, `KNeighborsClassifier`, `DecisionTreeClassifier` |
| `predict` returns | `47.3` | `1` |
| Metric today | RMSE, R² | Accuracy |
| Is "nearly right" a thing? | Yes | **No** |

### The decision boundary — the one picture

Draw a scatter plot on the board: two features on the axes, red dots bottom-left, blue dots top-right. Draw a line between them.

*"That line is the **decision boundary**. It IS the model. Everything else — sigmoid, neighbours, Gini — is just a different method for choosing where the line goes."*

Now sketch three versions of the same picture:

| Model | Boundary shape | Failure mode |
|---|---|---|
| Logistic Regression | One straight line | Too rigid — underfits curved data |
| K-Nearest Neighbours | Wiggly, hugs the data | Too flexible at low `k` — overfits |
| Decision Tree | Staircase — axis-aligned steps | Too deep — memorises every row |

**Tie it back to Session 2:** a boundary that bends around every training point has overfit. A boundary that is a straight line through obviously curved data has underfit. Today's hyperparameters — `k`, `max_depth` — are literally dials on boundary wiggliness.

---

## Practical Block 1: Your First Classifier (15 min)

```python
import numpy as np
import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.metrics import accuracy_score

# 569 tumour scans, 30 measurements each. Target: 0 = malignant, 1 = benign.
data = load_breast_cancer()
X = pd.DataFrame(data.data, columns=data.feature_names)
y = pd.Series(data.target)

print("Rows, columns:", X.shape)
print("Label counts:")
print(y.value_counts())          # roughly 357 benign, 212 malignant
print("Label meaning:", dict(enumerate(data.target_names)))

# stratify=y keeps the same class ratio in train and test — always do this for classification
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Scaler + classifier in one object, exactly as in Session 3
clf = make_pipeline(StandardScaler(),
                    LogisticRegression(max_iter=1000, random_state=42))
clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)
print("Test accuracy:", round(accuracy_score(y_test, y_pred), 3))
print("First 10 predictions:", y_pred[:10])
print("First 10 true labels:", y_test.values[:10])
```

Expected: accuracy lands very high on this dataset — somewhere around 0.97–0.98. Do not promise an exact figure; let them read it off the screen.

**Live walk-through:** Three things to call out, in this order.

1. *"Point at the `fit` line. Is it different from Session 3? No. You already knew how to do this."*
2. `stratify=y` — *"Without this, a random split could hand you a test set with 80% benign by chance, and your accuracy number becomes meaningless. For classification, always stratify."*
3. The predictions are `0`s and `1`s, not decimals. Ask the room: *"Where did the decimals go?"* Do not answer. That is Concept Block 2.

---

## Concept Block 2: Inside Logistic Regression (10 min)

### The name is a lie

Write this on the board and underline it: **Logistic Regression is a CLASSIFIER.** The word "regression" is a historical accident. Every student mis-uses it once; get it out of the way now.

### The three steps

```
STEP 1  — the same line as Session 5:
          z = w1*x1 + w2*x2 + ... + b
          z can be ANY number:  -40, 0, +900.   Useless as a probability.

STEP 2  — squash it with the sigmoid:
          sigmoid(z) = 1 / (1 + e^(-z))     →  always lands in 0 to 1

STEP 3  — apply the threshold:
          probability > 0.5  →  class 1
          probability <= 0.5 →  class 0
```

Write the sigmoid table too — it lands better than the formula does.

| `z` | `sigmoid(z)` | Reading |
|---|---|---|
| -4 | 0.02 | Very sure: class 0 |
| -1 | 0.27 | Leaning class 0 |
| 0 | **0.50** | Perfectly undecided |
| +1 | 0.73 | Leaning class 1 |
| +4 | 0.98 | Very sure: class 1 |

**The punchline:** `sigmoid(z) = 0.5` exactly when `z = 0`. So the line `z = 0` *is* the decision boundary. The sigmoid is not doing the deciding — the line is. The sigmoid just converts the line's output into readable confidence.

### Reading the coefficients

Each weight `w` is a **push**: large positive → this feature rising pushes towards class 1. Large negative → pushes towards class 0. Near zero → the feature barely matters.

*"This is why hospitals and banks still reach for Logistic Regression first. It can be audited. Someone can ask 'why was I rejected?' and you can actually answer."*

Caveat to say out loud: coefficients are only comparable to each other **if the features were scaled**. Unscaled, a big coefficient may just mean the feature had small units.

---

## Practical Block 2: predict vs predict_proba (15 min)

```python
import matplotlib.pyplot as plt

# --- The sigmoid curve itself ---
z = np.linspace(-8, 8, 200)
sigmoid = 1 / (1 + np.exp(-z))

plt.figure(figsize=(7, 4))
plt.plot(z, sigmoid, lw=2)
plt.axhline(0.5, color="red", ls="--", lw=1, label="0.5 threshold")
plt.axvline(0, color="grey", ls=":", lw=1)
plt.title("The sigmoid squashes any number into the range 0 to 1")
plt.xlabel("z  — the raw linear score")
plt.ylabel("Probability of class 1")
plt.legend()
plt.tight_layout()
plt.show()

# --- predict vs predict_proba on the SAME rows ---
probs = clf.predict_proba(X_test)     # shape: (n_test, 2) — one column per class
preds = clf.predict(X_test)

comparison = pd.DataFrame({
    "P(malignant)": probs[:8, 0].round(3),
    "P(benign)":    probs[:8, 1].round(3),
    "predict()":    preds[:8],
    "true label":   y_test.values[:8],
})
print(comparison)
print("\nEach row of predict_proba sums to 1.0:", probs[0].sum())

# --- Reading the coefficients as pushes ---
logreg = clf.named_steps["logisticregression"]
coefs = pd.Series(logreg.coef_[0], index=X.columns).sort_values()
print("\nStrongest pushes towards class 0 (malignant):")
print(coefs.head(3).round(3))
print("\nStrongest pushes towards class 1 (benign):")
print(coefs.tail(3).round(3))
```

Expect most `predict_proba` rows to be extremely confident (0.99+) with the occasional borderline row near 0.5. **Hunt for a borderline row on screen** — it is the most valuable thing on this slide.

```python
# --- Seeing the boundary, with just 2 features ---
from sklearn.datasets import make_blobs

Xb, yb = make_blobs(n_samples=200, centers=2, n_features=2,
                    cluster_std=1.8, random_state=42)
bclf = LogisticRegression(random_state=42).fit(Xb, yb)

# Predict the class of every point on a fine grid, then colour the grid in
xx, yy = np.meshgrid(np.linspace(Xb[:, 0].min() - 1, Xb[:, 0].max() + 1, 200),
                     np.linspace(Xb[:, 1].min() - 1, Xb[:, 1].max() + 1, 200))
Z = bclf.predict(np.c_[xx.ravel(), yy.ravel()]).reshape(xx.shape)

plt.figure(figsize=(6, 5))
plt.contourf(xx, yy, Z, alpha=0.2, cmap="coolwarm")
plt.scatter(Xb[:, 0], Xb[:, 1], c=yb, cmap="coolwarm", edgecolor="k", s=35)
plt.title("The decision boundary drawn by Logistic Regression")
plt.xlabel("Feature 1")
plt.ylabel("Feature 2")
plt.tight_layout()
plt.show()
```

**Live walk-through:** Point at the straight edge between the two coloured regions. *"That is the model. Not the code — that line. Everything else was scaffolding to find it."* Then ask the room: *"If the two blobs were shaped like a crescent moon wrapped around a ball, could a straight line separate them?"* No. That is exactly the limitation KNN and trees exist to solve.

---

## BREAK (10 min)

*Mull this over: a KNN model with `k = 1` scores a perfect 1.00 on the training set, every single time, on every dataset. Why is that guaranteed — and why is it terrible news?*

---

## Concept Block 3: K-Nearest Neighbours (10 min)

### The whole algorithm, in one sentence

*"You are the average of the k people standing nearest to you."*

To classify a new point: measure its distance to **every** training point, take the `k` closest, return the majority label among them. That is all of it.

```
fit()      →  memorise the training data.  (There is no "learning".)
predict()  →  measure distances, vote.     (ALL the work happens here.)
```

KNN is the odd one out: training is instant, prediction is slow. Every other model in this module is the reverse.

### The `k` dial

| `k` | Boundary | Diagnosis |
|---|---|---|
| 1 | Jagged, wraps every point | **Overfit.** Train accuracy = 1.00, always |
| 5–15 | Smooth but responsive | Usually the sweet spot |
| Very large | Almost flat | **Underfit.** Collapses to "predict the majority class" |

*"If k equals the number of training rows, every prediction is the same — the overall majority class. The model has become a coin that always lands the same way."*

### The scaling trap — the most important slide of the block

Put this on the board:

```
Order A:  distance = 2 km,  order value = ₹500
Order B:  distance = 9 km,  order value = ₹540

As KNN measures it:
    km gap     =  7   →   7² = 49
    rupee gap  = 40   →  40² = 1600     ← DROWNS the km gap
```

**KNN measures distance, so any feature on a bigger numeric scale automatically shouts louder.** Here the model has silently become a one-feature model. A `StandardScaler` in front of the classifier is not a nice-to-have — without it, KNN is quietly broken. This is the single most common student mistake in this session.

Trees and Logistic Regression tolerate unscaled data. KNN does not.

---

## Practical Block 3: KNN, Scaling, and the k Sweep (15 min)

```python
from sklearn.neighbors import KNeighborsClassifier

# --- The scaling experiment: same k, same data, one difference ---
knn_raw = KNeighborsClassifier(n_neighbors=5)
knn_raw.fit(X_train, y_train)
print("KNN accuracy WITHOUT scaling:", round(knn_raw.score(X_test, y_test), 3))

knn_scaled = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=5))
knn_scaled.fit(X_train, y_train)
print("KNN accuracy WITH scaling   :", round(knn_scaled.score(X_test, y_test), 3))

# --- The k sweep: watch train and test diverge ---
print(f"\n{'k':>4} | {'train':>6} | {'test':>6}")
print("-" * 24)
for k in [1, 3, 5, 11, 25, 51, 101]:
    m = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=k))
    m.fit(X_train, y_train)
    print(f"{k:>4} | {m.score(X_train, y_train):>6.3f} | {m.score(X_test, y_test):>6.3f}")
```

Expected: the scaled version wins clearly — a jump of several percentage points. Do not quote a number; run it and read it off the screen.

*"Same algorithm. Same k. Same rows. The only difference is one line of preprocessing — and it is worth several percent of accuracy. In this dataset the features range from 0.05 to 4000. Guess which one KNN was listening to."*

**Live walk-through:** Look at the `k = 1` row *first*. Train accuracy is exactly `1.000`. Ask: *"Is this our best model?"*

Someone will say yes. Then: *"It is looking up the answer. Each training point's nearest neighbour is itself — distance zero. It has memorised a table. Look at its test score compared to `k = 11`."*

Then walk down the column: as `k` grows, train accuracy falls (the model stops memorising) while test accuracy first improves, then plateaus, then begins to sag. That U-shape is the bias-variance trade-off from Session 2, appearing in a completely new algorithm. Same story, new costume.

---

## Concept Block 4: Decision Trees (10 min)

### The mental model

*"A decision tree is a customer care phone menu that the machine wrote for itself."*

Sketch this on the board — it is a simplified version of the tree they will actually plot in Practical 4:

```
                  Is worst_radius <= 16.8 ?
                 /                        \
              YES                          NO
               |                            |
     Is worst_concave_points          (mostly MALIGNANT —
        <= 0.14 ?                      splits further)
       /          \
    YES            NO
     |              |
  BENIGN        MALIGNANT
```

Each internal node is a yes/no question about **one feature and one cut-off**. Each leaf is a predicted class. To predict, walk from the root down to a leaf. That is it.

### How is a split chosen?

The tree tries **every feature × every possible cut-off** and keeps the one that leaves the two child groups as **pure** as possible. "Pure" means mostly one class. Purity is scored by **Gini impurity** (sklearn's default) or **entropy** — they behave almost identically, so do not let students agonise over the choice.

| Group of 10 | Gini impurity | Meaning |
|---|---|---|
| 10 malignant, 0 benign | 0.00 | Perfectly pure — stop splitting |
| 7 malignant, 3 benign | 0.42 | Getting there |
| 5 malignant, 5 benign | 0.50 | Maximally mixed — worst case |

The tree greedily takes the split with the biggest impurity drop, then repeats on each child. It never looks ahead. That greediness is why one tree is decent but not brilliant — exactly the gap Session 7 fills.

**`max_depth` is the overfitting dial.** Unlimited depth → the tree splits until every leaf holds one training row → **train accuracy 1.00, test accuracy drops.** It has memorised the training set, exactly like `k = 1` KNN.

**Their superpower is interpretability.** `plot_tree` gives you a picture a doctor can read without knowing any maths. Neither Logistic Regression nor KNN can do that. When someone asks *"why did the model say that?"*, the tree just shows them the path.

---

## Practical Block 4: plot_tree, max_depth, and the Accuracy Trap (10 min)

```python
from sklearn.tree import DecisionTreeClassifier, plot_tree

# --- The max_depth dial ---
print(f"{'max_depth':>10} | {'train':>6} | {'test':>6}")
print("-" * 30)
for d in [1, 2, 3, 5, None]:
    t = DecisionTreeClassifier(max_depth=d, random_state=42)
    t.fit(X_train, y_train)
    label = str(d) if d else "None"
    print(f"{label:>10} | {t.score(X_train, y_train):>6.3f} | {t.score(X_test, y_test):>6.3f}")

# --- The superpower: an actual readable picture ---
tree = DecisionTreeClassifier(max_depth=3, random_state=42)
tree.fit(X_train, y_train)

plt.figure(figsize=(16, 8))
plot_tree(tree,
          feature_names=list(X.columns),
          class_names=list(data.target_names),
          filled=True, rounded=True, fontsize=9)
plt.title("Decision Tree, max_depth = 3")
plt.tight_layout()
plt.show()

# Which features did it actually use?
importances = pd.Series(tree.feature_importances_, index=X.columns)
print(importances.sort_values(ascending=False).head(4).round(3))
```

**Live walk-through:** In the depth table, at `max_depth=None` train accuracy is exactly `1.000` while test accuracy is *lower* than at a modest depth. That gap is overfitting, visible in one table — the same story as `k = 1`. Then trace one path of the plotted tree aloud, as plain English: *"If worst radius is under this value, and worst concave points is under that value, then benign."* And land it: *"Hand that picture to a doctor. They can check it, argue with it, and trust it. Now try handing them the 30 coefficients from our Logistic Regression."*

```python
# --- The accuracy trap: why accuracy alone is not enough ---
rng = np.random.RandomState(42)
n = 1000
fraud = np.zeros(n, dtype=int)
fraud[rng.choice(n, size=20, replace=False)] = 1   # only 20 frauds in 1000 txns

lazy_prediction = np.zeros(n, dtype=int)           # "nothing is ever fraud"

print("Frauds in the data:", fraud.sum(), "out of", n)
print("Accuracy of a model that ALWAYS says 'not fraud':",
      round(accuracy_score(fraud, lazy_prediction), 3))
print("Frauds actually caught:", int(((lazy_prediction == 1) & (fraud == 1)).sum()))
```

**Live walk-through:** The lazy model scores 98% accuracy and catches zero frauds. Ask: *"Would you deploy this to a bank?"* Then land it: *"Accuracy just counts correct answers. When one class is rare, guessing the common class every time wins on paper and fails in production. Today our data is balanced, so accuracy is fine. Session 8 gives you the metrics that survive imbalance."*

---

## Summary & Wrap-Up (5 min)

1. **Classification predicts a label, not a number.** Same workflow — split, fit, predict, score. Only the target and the metric change.
2. **Every classifier draws a decision boundary.** They differ only in the shape they can draw: straight line, wiggly, or staircase.
3. **Logistic Regression** = a line, squashed by the sigmoid into a 0–1 probability, cut at 0.5. Coefficients read as pushes towards a class. Auditable.
4. **KNN** = majority vote of the `k` nearest points. Small `k` overfits, large `k` underfits, and **it is broken without a scaler**.
5. **Decision Trees** = a self-written flowchart. Splits chosen by purity (Gini). `max_depth` is the overfitting dial. Unbeatable for interpretability.
6. **`predict` gives the label; `predict_proba` gives the confidence** — and **accuracy is a trap on imbalanced data.** Hold that thought.

**Bridge:** *"You have seen that one tree is decent, but a deep one memorises and a shallow one is too simple. Next session — **Ensemble Classification Models** — you will grow hundreds of imperfect trees and let them vote. Random Forests and Gradient Boosting are built on exactly the tree you plotted today, and they will beat every model in this notebook."*

---

## Q&A & Doubt Solving (5 min)

**Q: If Logistic Regression outputs a probability, why is it not a regression model?**
→ Because the probability is only an intermediate step. The final output is a label, and the model is trained to separate classes, not to minimise squared error on a number. The name is a historical hangover from statistics — the "regression" refers to fitting a linear equation to the log-odds, not to predicting a continuous target.

**Q: Do I have to scale my features for Decision Trees too?**
→ No, and this surprises people. A tree only ever asks "is this feature above or below a cut-off?" Multiplying a feature by 1000 changes the cut-off to a bigger number but produces exactly the same split. Trees are scale-invariant. KNN is the opposite — it measures raw distance, so scale is everything. Logistic Regression sits in between: it works unscaled, but it converges faster and its coefficients only become comparable when scaled.

**Q: How do I pick the right value of `k`, and what if a probability comes out at exactly 0.5?**
→ For `k`: sweep it and read the test score, as in Practical 3. Start with odd values (avoids ties in binary problems) around the square root of your training set size, and never trust `k = 1` just because its training score is perfect — that number is meaningless by construction. For the threshold: scikit-learn's rule is `probability > 0.5 → class 1`, so an exact 0.5 goes to class 0. What *should* worry you is a pile of predictions clustered near 0.5 — that means the model is guessing.

**Q: Which of these three should I actually use in a real project?**
→ Start with Logistic Regression as your baseline — it is fast, it is auditable, and if it does well you are done. Reach for a tree when you need to explain the decision to a human or the relationship is clearly not a straight line. Use KNN mainly for small, low-dimensional, well-scaled datasets — it gets slow and unreliable as the number of features climbs.

---

## Instructor Notes

- **No downloads needed.** Everything runs on `load_breast_cancer()` and `make_blobs()`, both bundled with scikit-learn. Only `pip install scikit-learn matplotlib pandas` is required, and students have all three from Sessions 1–5.
- **`max_iter=1000` on LogisticRegression is deliberate.** The default (100) throws a `ConvergenceWarning` on this dataset. If a student's screen fills with red text, this is why — and it makes a good 30-second detour on what "converge" means, linking back to gradient descent in Session 5.
- **The single most common mistake: forgetting `StandardScaler` before KNN.** Pre-empt it by running the unscaled version *first* in Practical 3, so they see the accuracy drop with their own eyes before you explain it. Telling them does not stick; showing them does.
- **Second most common mistake: celebrating `k = 1` or `max_depth=None` because train accuracy is 1.00.** Every time a student reports a perfect training score, ask "and the test score?" until it becomes reflex.
- **Pacing:** Practical 2's boundary plot is the thing to cut if you are running late — the sigmoid plot and the `predict_proba` table are load-bearing. Never cut the `plot_tree` in Practical 4; it is the most memorable minute of the session.
- **Do not let the discussion drift to precision, recall, or ROC-AUC.** Students who have read ahead will ask. Acknowledge it, write "Session 8" on the board, and move on — the accuracy-trap demo is deliberately the cliff-hanger for that session.
