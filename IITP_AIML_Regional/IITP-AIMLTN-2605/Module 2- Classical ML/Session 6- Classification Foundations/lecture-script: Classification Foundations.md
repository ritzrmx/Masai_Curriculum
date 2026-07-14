# Lecture Script: Classification Foundations
> **Instructor Reference** — Module 2: Classical ML | Session 6 | Duration: 2 Hours

---

## Session Overview

**Goal:** Students can explain why classification is a fundamentally different task from regression, fit and interpret a `LogisticRegression` model using the sigmoid function and decision boundaries, and fit and interpret a `DecisionTreeClassifier` using Gini impurity and information gain.

**Student profile at this point:** Deeply comfortable with `.fit()`/`.predict()`, train-test splits, scaling, and evaluating regression models (MAE/RMSE/R²). Understands overfitting, bias-variance, and regularization from Sessions 2–5. Has never predicted a category — every model so far has output a number.

**Key outcome:** By end of class, every student has fit two classifiers on real data, can read a probability output and a tree structure, and can explain in plain language what Gini impurity and information gain measure.

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| Opening & Context | 5 min | 0:05 |
| **Concept 1:** From Predicting Numbers to Predicting Categories | 10 min | 0:15 |
| **Practical 1:** Framing the Problem — Binary vs Multiclass | 10 min | 0:25 |
| **Concept 2:** Logistic Regression & the Sigmoid Function | 15 min | 0:40 |
| **Practical 2:** Fit Logistic Regression, Read Probabilities & Boundaries | 15 min | 0:55 |
| **BREAK** | 10 min | 1:05 |
| **Concept 3:** Decision Trees — Nodes, Leaves, Splits | 10 min | 1:15 |
| **Practical 3:** Fit a Decision Tree & Read Its Structure | 15 min | 1:30 |
| **Concept 4:** Gini Impurity & Information Gain | 10 min | 1:40 |
| **Practical 4:** Hand-Compute Gini, Compare Criteria & Depths | 10 min | 1:50 |
| Summary & Wrap-Up | 5 min | 1:55 |
| Q&A & Doubt Solving | 5 min | 2:00 |

---

## Opening (5 min)

**Hook:** Write two questions on the board side by side:

```
Q1: "What will this house sell for?"      → ₹ 82,40,000
Q2: "Will this tumor turn out malignant?" → Malignant / Benign
```

Ask the class: *"Both questions use the same features — size, texture, patient history. Both use the same `.fit()` / `.predict()` API you already know. So what's actually different?"*

Let a few students guess. Land on the key distinction: **Q1's answer lives on a continuous number line. Q2's answer lives in a small, fixed set of labels.** Every model, every metric, and every plot you build today exists because of that one difference.

**Context to set:** Every model you've built so far — Linear, Ridge, Lasso — was designed to minimize the distance between a predicted number and a true number. That machinery breaks the moment your target is a category. You cannot compute "the average of Malignant and Benign." Today we build two new tools purpose-built for categories: **Logistic Regression** (draws a boundary through probability space) and **Decision Trees** (asks a sequence of yes/no questions). Both are still `.fit()` / `.predict()` — the shape of the problem changes, not the workflow.

**Learning contract for today:**
- Explain why classification needs different models and different thinking than regression
- Fit `LogisticRegression`, read predicted probabilities, and locate the decision boundary
- Fit a `DecisionTreeClassifier`, read its node/leaf structure, and explain a split using Gini impurity

---

## Concept Block 1: From Predicting Numbers to Predicting Categories (10 min)

### Regression vs Classification — Side by Side

| | Regression (Sessions 1–5) | Classification (today) |
|---|---|---|
| Target | Continuous number | Category / class label |
| Example target | House price, salary, temperature | Spam/Not spam, Malignant/Benign, species |
| Output of `.predict()` | A number (e.g. 82.4) | A label (e.g. `"malignant"` or `0`) |
| Output of `.predict_proba()` | Doesn't exist | Probability per class (e.g. `[0.12, 0.88]`) |
| "Wrong by how much?" | Meaningful (₹40,000 off) | Not meaningful — you're either right or you predicted the wrong bucket |
| Error metric | MAE, RMSE, R² | Accuracy, precision, recall (next session) |
| Geometric picture | Fit a line/curve **through** the points | Draw a **boundary** that separates the points |

**Key teaching point:** In regression, "close" has meaning — predicting ₹80L when the true price is ₹82L is a small, quantifiable error. In classification, there is no "almost malignant." You're either on the correct side of the boundary or you're not. This is why classification models don't optimize MSE — they optimize a different kind of loss built around probabilities and boundaries.

### Binary vs Multiclass

```
Binary: exactly 2 labels             Multiclass: 3+ labels
Malignant ● / Benign ○                Setosa ● / Versicolor ▲ / Virginica ■
e.g. spam detection, churn,           e.g. species ID, digit recognition,
     fraud/not fraud                       news category tagging
```

**Teaching point:** Every algorithm we cover today naturally handles binary classification. Logistic Regression extends to multiclass via a strategy called "one-vs-rest" or a built-in multinomial mode; Decision Trees handle multiclass natively — a leaf can just as easily say "class = virginica" as "class = benign." We'll build binary today because it's easier to visualize, but keep multiclass in your head as we go.

---

## Practical Block 1: Framing the Problem — Binary vs Multiclass (10 min)

### Dataset

We'll use two built-in `sklearn` datasets that need no downloads: **Breast Cancer Wisconsin** (binary — our main dataset for today) and **Iris** (multiclass — for contrast only).

```python
import numpy as np
from sklearn.datasets import load_breast_cancer, load_iris

# --- Binary classification dataset ---
cancer = load_breast_cancer()
print("Breast Cancer dataset")
print("Shape:", cancer.data.shape)
print("Target names:", cancer.target_names)
print("Class balance (0=malignant, 1=benign):", np.bincount(cancer.target))

# --- Multiclass classification dataset (for contrast) ---
iris = load_iris()
print("\nIris dataset")
print("Shape:", iris.data.shape)
print("Target names:", iris.target_names)
print("Class balance:", np.bincount(iris.target))
```

**Output:**
```
Breast Cancer dataset
Shape: (569, 30)
Target names: ['malignant' 'benign']
Class balance (0=malignant, 1=benign): [212 357]

Iris dataset
Shape: (150, 4)
Target names: ['setosa' 'versicolor' 'virginica']
Class balance: [50 50 50]
```

**Walk through it out loud:**
- Breast Cancer: 569 patients, 30 numeric features, **2** possible outcomes → binary.
- Iris: 150 flowers, 4 numeric features, **3** possible species → multiclass.
- Both are still tabular data. Both still get `train_test_split`, scaling, and `.fit()`. The only new thing is what `y` looks like.

**Discussion prompt:** *"Class balance for breast cancer is [212, 357] — not 50/50. If I built a lazy model that always predicts 'benign', what accuracy would it get?"* → Let them compute: 357/569 ≈ 62.7%. **Teaching point:** a model needs to beat this "always guess the majority class" baseline to be useful at all. Keep this number in your back pocket — we revisit baselines properly next session.

We'll use the **Breast Cancer** dataset for the rest of today's practicals, restricted to two features so we can actually plot and reason about what the model is doing.

---

## Concept Block 2: Logistic Regression & the Sigmoid Function (15 min)

### Why Not Just Use Linear Regression?

Imagine you tried to predict `y = 0` (benign) or `y = 1` (malignant) using plain Linear Regression. The line can shoot below 0 or above 1 — meaningless as a probability, and a single extreme outlier can swing the whole line.

```
Linear Regression on 0/1 labels          Logistic Regression on 0/1 labels
 1.5 |            ___---                  1.0 |          _______----
 1.0 |●  ●  ●___---                       0.5 |     ___--
 0.5 |      ●●●                                |  __-
 0.0 |__●__●___________                    0.0 |--________________
-0.5 |                                            (bounded 0 to 1, S-shaped)
     Can predict -0.3 or 1.4 — invalid          Always a valid probability
```

**Teaching point:** Logistic Regression fixes this by not predicting the label directly. It predicts a **probability**, using a function that is mathematically guaranteed to stay between 0 and 1: the **sigmoid function**.

### The Sigmoid Function

$$ \sigma(z) = \frac{1}{1 + e^{-z}} $$

Where `z` is just a linear combination of your features — exactly like regression: `z = w1*x1 + w2*x2 + ... + b`.

```
z (raw linear score)  →  sigmoid(z)  →  probability of class 1
      -∞  ─────────────────────────────────►  0.0
       0  ─────────────────────────────────►  0.5
      +∞  ─────────────────────────────────►  1.0
```

**Teaching point:** Logistic Regression is still doing linear regression under the hood — it computes `z = w·x + b` exactly like `LinearRegression`. The only new step is squashing that number through the sigmoid so it becomes a valid probability. This is why it's still called "**regression**" even though we use it for classification.

### From Probability to Decision: the Decision Boundary

Once you have a probability, you still need a label. The default rule:

```
if  P(class = 1)  >=  0.5   →  predict class 1
if  P(class = 1)  <   0.5   →  predict class 0
```

The **decision boundary** is the exact set of points where `P = 0.5` — geometrically, it's a straight line (in 2D) or a flat plane/hyperplane (in higher dimensions), because `z = 0` is what makes `sigmoid(z) = 0.5`, and `z` is linear in the features.

**Teaching point:** 0.5 is a *default*, not a law of nature. In a cancer-screening context, you might lower the threshold to 0.3 so you catch more malignant cases at the cost of more false alarms. We'll dig into threshold tuning properly in Session 8 — for today, just know the threshold exists and 0.5 is the out-of-the-box choice.

---

## Practical Block 2: Fit Logistic Regression, Read Probabilities & Boundaries (15 min)

```python
import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

data = load_breast_cancer()
X = pd.DataFrame(data.data, columns=data.feature_names)
y = data.target  # 0 = malignant, 1 = benign

# Restrict to 2 features so we can reason about the boundary geometrically
X2 = X[['mean radius', 'mean concave points']]

X_train, X_test, y_train, y_test = train_test_split(
    X2, y, test_size=0.2, random_state=42, stratify=y
)

# Logistic Regression is distance-based (like Ridge/Lasso) -- scale first
scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)
X_test_s = scaler.transform(X_test)

clf = LogisticRegression(random_state=42)
clf.fit(X_train_s, y_train)

print("Coefficients:", clf.coef_.round(3))
print("Intercept:", clf.intercept_.round(3))

y_pred = clf.predict(X_test_s)
y_proba = clf.predict_proba(X_test_s)

print("\nAccuracy:", round(accuracy_score(y_test, y_pred), 4))
```

**Output:**
```
Coefficients: [[-2.031 -2.831]]
Intercept: [0.505]

Accuracy: 0.8947
```

**Walk through it:** Both coefficients are negative. Ask the class: *"Mean radius and mean concave points are both LOWER for benign tumors in this encoding (y=1 is benign). Does a negative coefficient on a feature that's lower for the positive class make sense?"* Let them reason it through — a negative weight means "as this feature increases, the score `z` decreases, pushing the probability of class 1 (benign) down," which lines up with larger/more irregular tumors being more likely malignant.

### Reading Predicted Probabilities

```python
preview = pd.DataFrame({
    "P(malignant)": y_proba[:5, 0].round(3),
    "P(benign)": y_proba[:5, 1].round(3),
    "Predicted": y_pred[:5],
    "Actual": y_test[:5]
})
print(preview)
```

**Output:**
```
   P(malignant)  P(benign)  Predicted  Actual
0         0.999      0.001          0       0
1         0.009      0.991          1       1
2         0.680      0.320          0       0
3         0.713      0.287          0       1
4         1.000      0.000          0       0
```

**Teaching point:** Row 3 is the interesting one — the model was 71.3% confident in "malignant" but the true label was "benign." This is not a bug; it's a case that sits closer to the boundary. `.predict_proba()` gives you the full picture that `.predict()` throws away — the confidence, not just the final call.

### The Sigmoid Curve, Concretely

```python
def sigmoid(z):
    return 1 / (1 + np.exp(-z))

z_vals = np.array([-6, -3, -1, 0, 1, 3, 6])
print("z values:      ", z_vals)
print("sigmoid(z):    ", sigmoid(z_vals).round(3))
```

**Output:**
```
z values:       [-6 -3 -1  0  1  3  6]
sigmoid(z):     [0.002 0.047 0.269 0.5   0.731 0.953 0.998]
```

**Teaching point:** Notice `z=0` maps exactly to `0.5` — that's the decision boundary in raw-score space. Also notice the curve flattens fast — a `z` of 6 and a `z` of 60 both round to a probability of ~1.0. This is why extreme predictions can feel "overconfident" — the sigmoid saturates.

### Cases Near the Boundary

```python
near_boundary = np.abs(y_proba[:, 1] - 0.5) < 0.15
print(pd.DataFrame({
    "P(benign)": y_proba[near_boundary, 1].round(3),
    "Predicted": y_pred[near_boundary],
    "Actual": y_test[near_boundary]
}))
```

**Output:**
```
   P(benign)  Predicted  Actual
0      0.365          0       0
1      0.488          0       1
2      0.513          1       0
3      0.383          0       1
4      0.475          0       1
5      0.457          0       0
6      0.620          1       0
7      0.469          0       0
8      0.499          0       1
9      0.609          1       0
```

**Discussion prompt:** *"Look at these 10 rows. How many are wrong? Where do almost all the mistakes cluster — near 0.5, or near 0.99?"* Every single error in this table sits within 0.15 of the boundary. **Teaching point:** classifiers are almost never "confidently wrong." Mistakes concentrate exactly where the model is least sure — which is exactly what a well-behaved probability output should do.

---

## BREAK (10 min)

*Suggested break prompt — ask students to predict, before we touch code after the break: "If a model asked one yes/no question about your data and had to guess the label from that alone, what single feature would you pick, and why?" We'll compare their intuition to what the Decision Tree actually picks.*

---

## Concept Block 3: Decision Trees — Nodes, Leaves, Splits (10 min)

### The Mental Model: 20 Questions

A Decision Tree classifies the way you'd play "20 Questions" — ask the single most useful yes/no question first, then keep narrowing down.

```
                    [mean concave points <= 0.05?]   ← ROOT NODE
                   /                              \
                 YES                               NO
                  /                                  \
      [mean radius <= 14.98?]              [mean radius <= 14.70?]
        /              \                        /              \
      YES              NO                     YES              NO
       |                |                       |                |
   [ Benign ]     [ needs another        [ Malignant ]    [ Malignant ]
    LEAF            question... ]           LEAF              LEAF
```

### Vocabulary — Precisely

| Term | Meaning |
|---|---|
| **Root node** | The very first question, applied to 100% of the data |
| **Internal node** | Any question node that isn't the root and isn't final |
| **Leaf node** | The end of a branch — no more questions, just a predicted class |
| **Split** | The single yes/no rule at a node (e.g. `mean radius <= 14.98`) |
| **Depth** | How many questions you ask before reaching a leaf |
| **Branch** | One path from root to a leaf |

**Teaching point:** A tree doesn't compute a weighted sum like Logistic Regression does. It asks a **sequence of threshold questions on one feature at a time**. This makes trees easy to read out loud as rules — "if concave points is low AND radius is small, predict benign" — which is a real advantage over the coefficient table of a linear model.

### How Does the Tree Pick the Question?

At every node, the algorithm tries every feature and every possible threshold, and picks the split that makes the two resulting groups **as pure as possible** — i.e., as close to "all one class" as it can get. "Purity" is measured with **Gini impurity** (default) or **entropy** — the exact math is Concept Block 4.

**Teaching point:** This is a **greedy** algorithm — it picks the best split available *right now*, at every node, without looking ahead. It never reconsiders an earlier split. This is why trees can overfit: given enough depth, a greedy tree will keep splitting until every leaf contains a single training example — perfect on training data, brittle on new data. Sound familiar? This is the same overfitting idea from Session 2, wearing a different hat.

---

## Practical Block 3: Fit a Decision Tree & Read Its Structure (15 min)

```python
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.metrics import accuracy_score

# Same 2-feature split as the Logistic Regression example (no scaling needed --
# trees split on raw thresholds, they don't care about feature scale)
tree = DecisionTreeClassifier(max_depth=3, random_state=42)
tree.fit(X_train, y_train)

y_pred_tree = tree.predict(X_test)
print("Tree accuracy (max_depth=3):", round(accuracy_score(y_test, y_pred_tree), 4))

print("\nTree structure:")
print(export_text(tree, feature_names=['mean radius', 'mean concave points']))

print("Number of leaves:", tree.get_n_leaves())
print("Tree depth:", tree.get_depth())
```

**Output:**
```
Tree accuracy (max_depth=3): 0.9123

Tree structure:
|--- mean concave points <= 0.05
|   |--- mean radius <= 14.98
|   |   |--- mean concave points <= 0.04
|   |   |   |--- class: 1
|   |   |--- mean concave points >  0.04
|   |   |   |--- class: 1
|   |--- mean radius >  14.98
|   |   |--- mean concave points <= 0.04
|   |   |   |--- class: 0
|   |   |--- mean concave points >  0.04
|   |   |   |--- class: 1
|--- mean concave points >  0.05
|   |--- mean radius <= 14.70
|   |   |--- mean concave points <= 0.08
|   |   |   |--- class: 0
|   |   |--- mean concave points >  0.08
|   |   |   |--- class: 0
|   |--- mean radius >  14.70
|   |   |--- mean concave points <= 0.06
|   |   |   |--- class: 0
|   |   |--- mean concave points >  0.06
|   |   |   |--- class: 0

Number of leaves: 8
Tree depth: 3
```

**Walk through it line by line on the projector:**
- The **root split** is `mean concave points <= 0.05` — this is the single most useful question the algorithm found, echoing (or contradicting!) whatever the class guessed during the break.
- Every `|---` indent is one level deeper — one more question asked.
- `class: 1` and `class: 0` at the bottom of each branch are the **leaves** — final predictions.
- Notice this tree beat Logistic Regression on the same data: **0.9123 vs 0.8947**. Don't over-read this on a 114-row test set — the point is that trees and linear boundaries carve up the same space differently, not that trees always win.

### Feature Importances

```python
importances = dict(zip(['mean radius', 'mean concave points'],
                        tree.feature_importances_.round(3)))
print("Feature importances:", importances)
```

**Output:**
```
Feature importances: {'mean radius': 0.109, 'mean concave points': 0.891}
```

**Teaching point:** `mean concave points` did almost all the work (0.891 out of 1.0) — it's the feature used at the root and re-used deeper in the tree. `feature_importances_` sums the purity improvement each feature contributed across every split it was used in, normalized to sum to 1. This is the tree's own built-in answer to "which feature mattered most?" — no separate analysis required, unlike a linear model's coefficients (which need scaling to compare fairly).

**Discussion prompt:** *"If I fit this tree on all 30 features instead of just 2, would `mean concave points` still dominate? Would the tree necessarily use the same features Logistic Regression's coefficients found important?"* → Not necessarily — a tree can prefer a feature that creates a clean split even if it's not the feature most linearly correlated with the outcome.

---

## Concept Block 4: Gini Impurity & Information Gain (10 min)

### Gini Impurity — What "Purity" Actually Means

Gini impurity measures how mixed a group of labels is. It ranges from 0 (perfectly pure — everyone is the same class) to a max of 0.5 for a 2-class problem (perfectly mixed — 50/50).

$$ Gini = 1 - \sum_{i} p_i^2 $$

Where `p_i` is the fraction of class `i` in the node.

```
All one class (pure)          Perfectly mixed (impure)
●●●●●●                         ●●●○○○
Gini = 1 - (1.0² + 0.0²)      Gini = 1 - (0.5² + 0.5²)
     = 1 - 1.0 = 0.0               = 1 - 0.5 = 0.5
     "Best possible node"          "Worst possible node"
```

### A Tiny Hand-Worked Example

Six students, labeled by whether they studied more than 5 hours, and whether they passed:

| Student | Studied > 5 hrs? | Result |
|---|---|---|
| S1 | Yes | Pass |
| S2 | Yes | Pass |
| S3 | Yes | Fail |
| S4 | No | Fail |
| S5 | No | Fail |
| S6 | No | Pass |

**Root node** (before any split): 3 Pass, 3 Fail out of 6.

$$ Gini_{root} = 1 - \left[\left(\tfrac{3}{6}\right)^2 + \left(\tfrac{3}{6}\right)^2\right] = 1 - (0.25 + 0.25) = 0.5 $$

**Split on "Studied > 5 hrs?":**
- Left (Yes): S1, S2, S3 → Pass, Pass, Fail (2 Pass, 1 Fail)
- Right (No): S4, S5, S6 → Fail, Fail, Pass (1 Pass, 2 Fail)

$$ Gini_{left} = 1 - \left[\left(\tfrac{2}{3}\right)^2 + \left(\tfrac{1}{3}\right)^2\right] = 1 - (0.444 + 0.111) = 0.444 $$
$$ Gini_{right} = 1 - \left[\left(\tfrac{1}{3}\right)^2 + \left(\tfrac{2}{3}\right)^2\right] = 0.444 $$

**Weighted child Gini** (weight by how many samples land in each side):

$$ Gini_{split} = \tfrac{3}{6}(0.444) + \tfrac{3}{6}(0.444) = 0.444 $$

### Information Gain

$$ \text{Information Gain} = Gini_{root} - Gini_{split} = 0.5 - 0.444 = 0.056 $$

**Teaching point:** Information Gain is simply "how much purer did the children get compared to the parent?" A tree evaluates *every* candidate split at a node this exact way and picks whichever split produces the **highest** information gain (i.e. the **lowest** weighted child Gini). A gain of 0.056 here is small — this single feature only weakly separates the two classes on its own, which matches what the raw table shows: it's better than a coin flip, but not a clean split.

**Entropy — the alternative measure:** `criterion='entropy'` uses $-\sum p_i \log_2 p_i$ instead of $1 - \sum p_i^2$. It's shaped similarly (0 = pure, max = mixed) and almost always picks the same splits as Gini in practice. Gini is the default in scikit-learn because it's slightly cheaper to compute (no logarithm).

---

## Practical Block 4: Hand-Compute Gini, Compare Criteria & Depths (10 min)

```python
import pandas as pd
import numpy as np

toy = pd.DataFrame({
    "student": ["S1","S2","S3","S4","S5","S6"],
    "hours_gt_5": [1, 1, 1, 0, 0, 0],
    "result":     ["Pass","Pass","Fail","Fail","Fail","Pass"]
})

def gini(labels):
    p = pd.Series(labels).value_counts(normalize=True)
    return 1 - np.sum(p**2)

root_gini = gini(toy["result"])
left  = toy[toy["hours_gt_5"] == 1]["result"]
right = toy[toy["hours_gt_5"] == 0]["result"]

n = len(toy)
weighted_gini = (len(left)/n) * gini(left) + (len(right)/n) * gini(right)

print("Root Gini:", round(root_gini, 4))
print("Weighted child Gini:", round(weighted_gini, 4))
print("Information Gain:", round(root_gini - weighted_gini, 4))
```

**Output:**
```
Root Gini: 0.5
Weighted child Gini: 0.4444
Information Gain: 0.0556
```

**Instructor note:** This confirms the board-work from Concept Block 4 — have students verify the arithmetic matches before moving on. If it doesn't match, they've mis-grouped the students.

### Gini vs Entropy — Do They Actually Pick Different Splits?

```python
for crit in ['gini', 'entropy']:
    t = DecisionTreeClassifier(criterion=crit, max_depth=3, random_state=42)
    t.fit(X_train, y_train)
    acc = accuracy_score(y_test, t.predict(X_test))
    print(f"criterion={crit:8s} max_depth=3  test accuracy = {acc:.4f}")
```

**Output:**
```
criterion=gini     max_depth=3  test accuracy = 0.9123
criterion=entropy  max_depth=3  test accuracy = 0.9123
```

**Teaching point:** Identical result here. This is common — Gini and entropy usually agree on which splits are best. Don't spend model-tuning time swapping criteria; spend it on `max_depth` instead, which has a much bigger effect (next).

### Depth vs Overfitting — Tying Back to Session 2

```python
print(f"{'max_depth':>10} {'train_acc':>10} {'test_acc':>10} {'leaves':>8}")
for depth in [1, 2, 3, 4, 5, 8, None]:
    t = DecisionTreeClassifier(max_depth=depth, random_state=42)
    t.fit(X_train, y_train)
    train_acc = accuracy_score(y_train, t.predict(X_train))
    test_acc = accuracy_score(y_test, t.predict(X_test))
    label = depth if depth is not None else "None"
    print(f"{str(label):>10} {train_acc:>10.4f} {test_acc:>10.4f} {t.get_n_leaves():>8}")
```

**Output:**
```
 max_depth  train_acc   test_acc   leaves
         1     0.9165     0.9035        2
         2     0.9209     0.9035        4
         3     0.9253     0.9123        8
         4     0.9451     0.8947       14
         5     0.9560     0.8772       22
         8     0.9868     0.9123       41
      None     1.0000     0.9123       47
```

**Discussion prompt:** *"Training accuracy only ever goes up as depth increases — it hits 100% with unlimited depth. Test accuracy does not follow the same path. What's happening at depth 5?"* Train accuracy is climbing steadily while test accuracy dips to 0.877 — the tree is starting to memorize noise specific to the training set rather than learning the general pattern. **Teaching point:** an unlimited-depth tree (47 leaves here, on only ~455 training rows) is almost certainly memorizing near-unique paths for small clusters of points — this is overfitting, the exact same disease from Session 2, just caused by tree depth instead of polynomial degree or a too-small alpha. `max_depth`, `min_samples_leaf`, and `min_samples_split` are a tree's regularization knobs, the direct analog of Ridge/Lasso's `alpha`.

---

## Summary & Wrap-Up (5 min)

**What we covered today:**
- Classification predicts categories, not numbers — "close" doesn't mean the same thing it did in regression
- Logistic Regression computes a linear score `z`, then squashes it through the **sigmoid function** into a valid probability between 0 and 1
- The **decision boundary** is where `P = 0.5` by default — a straight line/plane in feature space
- Decision Trees ask a sequence of yes/no **splits**, from the **root** down to **leaf** nodes, choosing each split greedily
- **Gini impurity** measures how mixed a node is (0 = pure, 0.5 = maximally mixed for 2 classes); **Information Gain** measures how much a split reduces that impurity
- `max_depth` (and friends) control tree complexity — deeper trees fit training data better but risk overfitting, exactly like unregularized regression

**Bridge to next session:** *"Today you built two classifiers and judged them with a single number — accuracy. But accuracy can lie to you, especially on imbalanced data like our 63/37 benign/malignant split. Next class: Ensemble Classification Models — how combining many trees (Random Forests, Boosting) builds classifiers that are far more robust than any single tree, and why 'wisdom of the crowd' beats a single greedy decision-maker."*

**Homework / self-practice:** Load `load_wine()` from `sklearn.datasets` (a 3-class problem). Fit both a `LogisticRegression` and a `DecisionTreeClassifier` on it using all features, compare their accuracy, and print the decision tree's `feature_importances_`. Write one sentence on which feature the tree considered most important and whether that surprises you.

---

## Q&A & Doubt Solving (5 min)

**Likely questions and suggested answers:**

**Q: Why is it called "Logistic Regression" if it's used for classification?**
→ Because internally it's still fitting a linear equation (`z = w·x + b`) — the exact same math as Linear Regression. The only addition is the sigmoid function that converts that linear score into a probability. The name describes the mechanism, not the use case.

**Q: Does Logistic Regression need feature scaling like Ridge/Lasso did?**
→ Yes. It's still solving an optimization problem over weighted feature sums, so features on wildly different scales (e.g. "mean area" in the hundreds vs "mean smoothness" around 0.1) will distort the fit and slow convergence. Always scale before fitting.

**Q: Do Decision Trees need feature scaling?**
→ No — and this is worth pausing on. A tree only asks "is this feature above or below a threshold?" That comparison doesn't care whether the feature is measured in millimeters or kilometers. This is a genuine practical advantage of trees over linear/distance-based models.

**Q: Can a Decision Tree split on the same feature more than once?**
→ Yes, as we saw with `mean concave points` in today's tree — it can reappear at different thresholds deeper in the tree to further separate remaining mixed groups.

**Q: If Gini and entropy usually agree, why does scikit-learn offer both?**
→ They can diverge on close calls, and entropy is standard in information theory / other fields, so some practitioners prefer it for consistency with other tools. In practice, treat `criterion` as a minor tuning knob — `max_depth` and the `min_samples_*` parameters matter far more for model quality.

**Q: What happens if a leaf still has mixed classes when the tree stops growing (e.g. because of `max_depth`)?**
→ The leaf predicts the **majority class** among the samples that land there, and `.predict_proba()` returns the class proportions in that leaf as the probability estimate.

---

## Instructor Notes

- **Dataset:** `load_breast_cancer()` and `load_iris()` are both bundled with scikit-learn — zero downloads, zero internet dependency, safe for offline classrooms. Restricting to 2 features (`mean radius`, `mean concave points`) throughout keeps every output small enough to read on a slide and lets students reason about a boundary in 2D before trusting the same idea in 30D.
- **Common student mistake:** Confusing `.predict()` and `.predict_proba()` — students will try to average or subtract `.predict()` outputs the way they did with regression predictions. Explicitly show that `.predict()` on a classifier returns labels (or 0/1 codes), not something you can meaningfully do arithmetic on.
- **Common student mistake:** Forgetting to scale before Logistic Regression, then being confused why coefficients look strange or convergence warnings appear. Do this deliberately once, unscaled, to show the warning, then fix it — mirrors the Session 8/Module 1 "run it broken first" teaching pattern.
- **Live coding tip:** When showing `export_text()`, read the first two levels of the tree out loud as an actual sentence: "If concave points is 0.05 or less, and radius is 14.98 or less, predict benign." This translation from tree to English is what makes trees feel intuitive compared to a coefficient table.
- **For advanced students:** Have them re-fit the tree using all 30 features (`X` instead of `X2`) and compare `feature_importances_` — ask whether `mean concave points` still dominates, and whether accuracy improves meaningfully over the 2-feature version.
- **For advanced students:** Introduce `tree.plot_tree()` (from `sklearn.tree`) if a projector with color is available — the color-coded, graphical version of `export_text()` output lands especially well visually.
- **Time check:** If running long after the break, compress Practical 4 to just the hand-computed Gini example and the depth-vs-overfitting table; skip the live gini-vs-entropy comparison and mention the result verbally instead.
