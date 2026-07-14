# Lecture Script: The ML Workflow, Data Prep & Reliability
> **Instructor Reference** — Module 2: Classical ML | Session 1 | Duration: 2 Hours

---

## Session Overview

**Goal:** Students can take a raw tabular dataset and correctly frame it as a supervised ML problem, split it into train/validation/test sets without leaking information, build a baseline, and prepare features (encoding + scaling) — before ever touching a "real" model.

**Student profile at this point:** Just finished Module 1 — strong in Pandas, NumPy, data cleaning, SQL, EDA, and APIs. Zero ML vocabulary. Has never imported `sklearn`. Does not yet know what "training" a model means.

**Key outcome:** By end of class, every student can explain — and execute in code — the sequence: *frame the problem → separate features/label → split the data → beat a baseline → encode → scale*. This sequence is the backbone of every session for the rest of Module 2.

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| Opening & Context | 5 min | 0:05 |
| **Concept 1:** Problem Framing + Features vs Labels | 10 min | 0:15 |
| **Practical 1:** Explore a Dataset, Separate X / y | 15 min | 0:30 |
| **Concept 2:** Train / Validation / Test Split | 10 min | 0:40 |
| **Practical 2:** Perform the Split, Check Balance | 15 min | 0:55 |
| **BREAK** | 10 min | 1:05 |
| **Concept 3:** Baselines + Categorical Encoding | 10 min | 1:15 |
| **Practical 3:** Compute a Baseline, Encode Categoricals | 15 min | 1:30 |
| **Concept 4:** Scaling + Normalization | 10 min | 1:40 |
| **Practical 4:** Scale Features, Beat the Baseline | 10 min | 1:50 |
| Summary & Wrap-Up | 5 min | 1:55 |
| Q&A & Doubt Solving | 5 min | 2:00 |

---

## Opening (5 min)

**Hook:** Write this on the board (or show inline):

```
customer_id  tenure_months  monthly_charges  contract_type    payment_method     churn
CUST0001     7              2298.88          One year         Credit card        Yes
CUST0002     56             1839.36          Month-to-month   Bank transfer      No
CUST0003     48             884.91           Month-to-month   Bank transfer      No
```

Ask the class: *"A telecom company wants to know which customers are about to cancel their subscription. Everything you learned in Module 1 — cleaning, SQL, EDA — got the data to look like this. Now what? What decision are we actually trying to automate? What are we even trying to predict? How would we know if our prediction is any good?"*

Let a few answers land, then reveal: **that gap — between "clean data" and "a working prediction" — is the ML workflow. It has a fixed shape, every single time, regardless of the dataset or the algorithm.**

**Context to set:** Every algorithm you'll learn for the rest of this module — linear regression, logistic regression, decision trees, ensembles — sits inside the *same* five-step skeleton: frame the problem, split the data, set a baseline, prepare the features, then (and only then) fit a model. Skip any step and the model you build will lie to you convincingly. Today is entirely about that skeleton — no "real" algorithm yet.

**Learning contract for today:**
- Frame a business question as a supervised ML problem (classification vs. regression)
- Correctly separate features (X) from the label (y)
- Split data into train / validation / test sets without leaking information
- Compute a baseline and know why it is non-negotiable
- Encode categorical columns and scale numeric columns the right way

---

## Concept Block 1: Problem Framing & Features vs Labels (10 min)

### What "Machine Learning" Means Here

Forget the hype. For this module, machine learning means one specific thing: **learning a mapping from inputs to a known output, using examples where we already know the answer.**

```text
Historical Data (rows with known outcomes)
        │
        ▼
  Features (X)  +  Label (y)
        │
        ▼
   Model learns:  X  →  y
        │
        ▼
  New, unseen X  →  Predicted y
```

That's it. If you cannot point to a column in your data that is "the known answer" for past examples, you do not have a supervised learning problem yet — you have a data exploration problem.

### The Problem-Framing Checklist

Before writing a single line of `sklearn` code, answer these:

| Question | Why it matters |
|---|---|
| What decision are we automating? | "Predict churn" is vague. "Flag customers likely to cancel next month so retention can call them" is a problem. |
| What is one *row* of data? | One customer? One transaction? One day? Get this wrong and every downstream step is wrong. |
| What is the label (y)? | The column holding the known answer. Must exist in historical data. |
| Classification or regression? | Is y a category (Yes/No, spam/not-spam) or a number (price, revenue)? |
| What features are legitimately known *at prediction time*? | If a column is only available *after* the outcome happens, it can't be a feature — that's leakage (more in Concept 2). |

**Classification vs. Regression — the first fork every problem takes:**

| | Classification | Regression |
|---|---|---|
| Label type | Category / class | Continuous number |
| Example | Will this customer churn? (Yes/No) | What will this house sell for? (₹ lakhs) |
| Typical metric | Accuracy, precision, recall | MAE, RMSE, R² |
| Today's running example | Customer churn (Yes/No) | — |

### Features vs. Labels — the Vocabulary You'll Use All Module

- **Features (X):** the input columns — everything the model is allowed to look at to make a prediction. Also called *predictors*, *independent variables*, *inputs*.
- **Label (y):** the single column you are trying to predict. Also called *target*, *dependent variable*, *outcome*.

```text
X (features)                         y (label)
┌───────────────────────────────┐    ┌──────────┐
│ tenure_months │ contract_type  │    │  churn   │
│ monthly_charges │ payment_method│   │          │
└───────────────────────────────┘    └──────────┘
     "what we know"                   "what we predict"
```

**Common student mistake:** including an identifier column (`customer_id`) or a column that is really a *disguised version of the label* (e.g., `cancellation_date` when predicting churn) as a feature. An ID carries no signal and just adds noise; a disguised label causes **leakage** — the model "cheats" and looks great in testing, then fails completely in production.

**Key teaching point:** Every row must answer "features in, label out" — and every feature must be something you would *actually have on hand* at the moment you need the prediction, not something you'd only know afterward.

---

## Practical Block 1: Explore a Dataset, Separate X / y (15 min)

### Dataset

A synthetic telecom customer dataset — built in code, no internet required. We'll use this same dataset for the entire session.

```python
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)
n = 200

tenure_months = rng.integers(1, 73, size=n)
monthly_charges = rng.uniform(300, 2500, size=n).round(2)
contract_type = rng.choice(['Month-to-month', 'One year', 'Two year'],
                            size=n, p=[0.55, 0.25, 0.20])
payment_method = rng.choice(['Electronic check', 'Mailed check',
                              'Bank transfer', 'Credit card'], size=n)

# Simulate a realistic churn signal: month-to-month + short tenure + high charges -> more churn
base = 0.15
contract_boost = np.where(contract_type == 'Month-to-month', 0.35,
                   np.where(contract_type == 'One year', 0.08, -0.05))
tenure_effect = (36 - tenure_months) / 100
charge_effect = (monthly_charges - 1000) / 10000
noise = rng.normal(0, 0.05, size=n)

churn_prob = np.clip(base + contract_boost + tenure_effect + charge_effect + noise, 0.02, 0.95)
churn = np.where(rng.uniform(size=n) < churn_prob, 'Yes', 'No')

df = pd.DataFrame({
    'customer_id': [f'CUST{i:04d}' for i in range(1, n + 1)],
    'tenure_months': tenure_months,
    'monthly_charges': monthly_charges,
    'contract_type': contract_type,
    'payment_method': payment_method,
    'churn': churn
})

print(df.head(10))
print("\nShape:", df.shape)
print("\nChurn counts:")
print(df['churn'].value_counts())
print("\nChurn rate:")
print(df['churn'].value_counts(normalize=True).round(2))
```

**Output:**
```
  customer_id  tenure_months  monthly_charges   contract_type    payment_method churn
0    CUST0001              7          2298.88        One year       Credit card   Yes
1    CUST0002             56          1839.36  Month-to-month     Bank transfer    No
2    CUST0003             48           884.91  Month-to-month     Bank transfer    No
3    CUST0004             32          2432.19  Month-to-month       Credit card   Yes
4    CUST0005             32          2013.25        Two year  Electronic check   Yes
...

Shape: (200, 6)

Churn counts:
churn
No     128
Yes     72
Name: count, dtype: int64

Churn rate:
churn
No     0.64
Yes    0.36
Name: proportion, dtype: float64
```

### Now Separate Features from Label

```python
# customer_id is an identifier, not a feature — drop it
# churn is the label (y); everything else useful is a feature (X)
X = df.drop(columns=['customer_id', 'churn'])
y = df['churn']

print("Feature columns:", list(X.columns))
print("Label:", y.name)
print("X shape:", X.shape, "| y shape:", y.shape)
```

**Output:**
```
Feature columns: ['tenure_months', 'monthly_charges', 'contract_type', 'payment_method']
Label: churn
X shape: (200, 4) | y shape: (200,)
```

**Walk through:** Point out `X` is a 2D DataFrame (rows × features), `y` is a 1D Series (one label per row). This shape distinction — `X` is 2D, `y` is 1D — is exactly what every `sklearn` function expects, and mismatched shapes are the #1 error message students will hit this module.

**Ask the class:** *"Is `customer_id` a feature? What about `tenure_months` — is that legitimately known before a customer churns?"* Use this to reinforce the leakage discussion from Concept 1.

---

## Concept Block 2: Train / Validation / Test Split (10 min)

### Why We Can't Train and Test on the Same Data

If you show a model every example and then quiz it on those same examples, it can simply *memorize* the answers — like a student who saw the exam questions in advance. High score, zero understanding. We need data the model has never seen to know if it actually learned a pattern.

### Three Sets, Three Jobs

```text
┌─────────────┬─────────────────┬──────────────────────────────────┐
│   Set        │   Typical Size  │   Job                             │
├─────────────┼─────────────────┼──────────────────────────────────┤
│  Train       │   60–80%        │  Model learns patterns from this  │
│  Validation  │   10–20%        │  Tune choices, compare models     │
│  Test        │   10–20%        │  Final, one-time, honest score    │
└─────────────┴─────────────────┴──────────────────────────────────┘
```

| Split ratio | When to use |
|---|---|
| 70 / 15 / 15 | Small-to-medium datasets, default choice |
| 60 / 20 / 20 | When you'll do heavy model comparison/tuning |
| 80 / 10 / 10 | Larger datasets, where 10% is already plenty of rows |
| Train / Test only (no val) | Very small datasets or quick prototypes — use cross-validation instead of a validation set (covered later in the module) |

**The golden rule — write this on the board:** *The test set is touched exactly once, at the very end.* Not to pick features, not to choose a model, not to tune anything. The moment you make a decision based on test performance, it stops being an honest measure — it's now part of training, just with extra steps. This single mistake is one of the most common causes of models that look great in the classroom and fail in production.

**Why stratify?** For classification with an imbalanced label (here, 64% No / 36% Yes), a plain random split can accidentally dump most of the "Yes" rows into one split by chance — especially with smaller datasets. `stratify=y` forces every split to preserve the same class ratio as the original data.

```text
Full Data (200 rows, 64% No / 36% Yes)
        │
        ├── split 1 ──▶ Train (140 rows)         ~64% No / 36% Yes
        │
        └── split 2 ──▶ Validation (30 rows)     ~64% No / 36% Yes
                    └──▶ Test (30 rows)           ~64% No / 36% Yes
```

**Key teaching point:** `train_test_split` only splits into two pieces. To get three sets, you split twice — first carve off train, then split what's left into validation and test.

---

## Practical Block 2: Perform the Split, Check Balance (15 min)

```python
from sklearn.model_selection import train_test_split

# Step 1: carve off the training set (70%)
X_train, X_temp, y_train, y_temp = train_test_split(
    X, y, test_size=0.30, stratify=y, random_state=42
)

# Step 2: split what's left into validation and test (15% / 15% of the original)
X_val, X_test, y_val, y_test = train_test_split(
    X_temp, y_temp, test_size=0.50, stratify=y_temp, random_state=42
)

print("Train:", X_train.shape, "Val:", X_val.shape, "Test:", X_test.shape)

print("\nChurn rate per split:")
print("Train:", y_train.value_counts(normalize=True).round(3).to_dict())
print("Val:  ", y_val.value_counts(normalize=True).round(3).to_dict())
print("Test: ", y_test.value_counts(normalize=True).round(3).to_dict())
```

**Output:**
```
Train: (140, 4) Val: (30, 4) Test: (30, 4)

Churn rate per split:
Train: {'No': 0.643, 'Yes': 0.357}
Val:   {'No': 0.633, 'Yes': 0.367}
Test:  {'No': 0.633, 'Yes': 0.367}
```

**Walk through:** Notice the churn rate is nearly identical (~64/36) across all three splits — that's `stratify` doing its job. Re-run without `stratify=y` live and show the ratios drift; with only 200 rows the difference is visible immediately.

**random_state — explain briefly:** Fixes the "random" shuffling so everyone in the room gets the exact same split, and so re-running your own notebook reproduces the same numbers. Any integer works; the value itself is arbitrary.

**Ask the class:** *"Why split validation and test 50/50 from the leftover 30%, instead of just using validation for everything?"* → Because validation gets used repeatedly during model tuning (and can slowly become biased through repeated peeking), while test is saved untouched for one final, trustworthy number.

---

## BREAK (10 min)

*Suggested break prompt — ask students to write down, on paper, what they think "a baseline" means in plain English before we define it formally. We'll compare notes right after the break.*

---

## Concept Block 3: Baselines & Categorical Encoding (10 min)

### What Is a Baseline?

A baseline is **the dumbest reasonable prediction strategy** — one that requires no real learning. Before celebrating any model's accuracy, you must know: *how well would I do by guessing intelligently but lazily?*

| Problem type | Baseline strategy | What it predicts |
|---|---|---|
| Classification | Predict the majority class every time | Always "No churn" if that's more common |
| Regression | Predict the mean (or median) every time | Always the average house price |

### Why This Is Not Optional

Recall our data: 64% of customers did *not* churn. A model that always predicts "No" — without learning anything — is already **64% accurate**. If your "real" model scores 65% accuracy, you have built almost nothing. If it scores 85%, now you have a genuinely useful model. **You cannot tell these two situations apart without computing the baseline first.**

**Key teaching point:** A baseline turns "is my accuracy good?" (unanswerable in isolation) into "did my model beat the baseline, and by how much?" (answerable, and honest). We'll revisit this exact trap next session when we cover imbalanced data pitfalls in depth.

### Categorical Encoding

Models only do arithmetic — they cannot multiply weights by the string `"Month-to-month"`. Every categorical column must become numbers before it can be a feature.

```text
Is the category ORDERED?
  │
  ├── No (nominal) — e.g. payment_method: Credit card, Mailed check...
  │        → One-Hot Encoding: one 0/1 column per category
  │
  └── Yes (ordinal) — e.g. contract_type: Month-to-month < One year < Two year
           → Ordinal Encoding: map to 0, 1, 2 preserving the order
              (or one-hot if you're not sure the model can exploit the order)
```

| Method | How it works | Use when | Watch out for |
|---|---|---|---|
| One-Hot Encoding | New 0/1 column per category | No natural order between categories | High-cardinality columns explode column count |
| Ordinal / Label Encoding | Map categories to integers 0, 1, 2… | Categories have a genuine order | Applying it to nominal data invents a fake order (e.g. "Mailed check" > "Credit card" makes no sense) |

**Practical default for this module:** one-hot encode nominal columns with `pd.get_dummies(..., drop_first=True)`. `drop_first=True` drops one category to avoid redundant columns (if you know it's not A, B, or C, it must be D — no need for a 4th column).

**Key teaching point:** Encoders (like scalers, next block) must be **fit on training data only**, then applied to validation/test. Fitting on the full dataset before splitting leaks information about val/test categories into training — same family of mistake as touching the test set early.

---

## Practical Block 3: Compute a Baseline, Encode Categoricals (15 min)

```python
from sklearn.dummy import DummyClassifier
from sklearn.metrics import accuracy_score

# --- Baseline: always predict the majority class ---
dummy = DummyClassifier(strategy='most_frequent', random_state=42)
dummy.fit(X_train, y_train)

baseline_val_acc = accuracy_score(y_val, dummy.predict(X_val))
print("Majority class in train:", y_train.mode()[0])
print("Baseline validation accuracy:", round(baseline_val_acc, 3))
```

**Output:**
```
Majority class in train: No
Baseline validation accuracy: 0.633
```

```python
# --- Categorical encoding ---
cat_cols = ['contract_type', 'payment_method']
num_cols = ['tenure_months', 'monthly_charges']

X_train_enc = pd.get_dummies(X_train, columns=cat_cols, drop_first=True)
X_val_enc = pd.get_dummies(X_val, columns=cat_cols, drop_first=True)
X_test_enc = pd.get_dummies(X_test, columns=cat_cols, drop_first=True)

# Align val/test columns to train's columns — protects against a category
# that appears in train but not in a smaller val/test slice
X_val_enc = X_val_enc.reindex(columns=X_train_enc.columns, fill_value=0)
X_test_enc = X_test_enc.reindex(columns=X_train_enc.columns, fill_value=0)

print("Encoded columns:", list(X_train_enc.columns))
print("Encoded train shape:", X_train_enc.shape)
print(X_train_enc.head(3))
```

**Output:**
```
Encoded columns: ['tenure_months', 'monthly_charges', 'contract_type_One year', 'contract_type_Two year', 'payment_method_Credit card', 'payment_method_Electronic check', 'payment_method_Mailed check']
Encoded train shape: (140, 7)
     tenure_months  monthly_charges  contract_type_One year  contract_type_Two year  payment_method_Credit card  payment_method_Electronic check  payment_method_Mailed check
145             62          2209.03                    True                   False                       False                            False                        True
38              20          2022.02                   False                   False                       False                            False                        True
17              10          1882.82                    True                   False                       False                            False                        True
```

**Walk through:** 4 original feature columns became 7 — `contract_type` (3 categories) became 2 dummy columns, `payment_method` (4 categories) became 3 dummy columns. Point out the `reindex` step: if a rare payment method only shows up in the training rows by chance, validation/test still need that same column (filled with 0) or the model will crash on mismatched columns at prediction time.

**Ask the class:** *"`contract_type` actually has a natural order — Month-to-month < One year < Two year. Would ordinal encoding (0, 1, 2) make more sense here than one-hot?"* → Either is defensible; ordinal keeps it compact and preserves order for models that can use it (like tree-based models), one-hot avoids assuming a linear model treats "2" as literally "twice as much contract" as "1".

---

## Concept Block 4: Scaling & Normalization (10 min)

### Why Numeric Ranges Matter

Look at our two numeric features: `tenure_months` ranges roughly 1–72, while `monthly_charges` ranges roughly 300–2500. Many algorithms — anything based on distance (like k-nearest neighbors) or gradient descent (like logistic regression, neural networks) — will let the large-range column dominate the large-range column purely because of its scale, not because it's actually more important. Tree-based models (decision trees, random forests) are the exception — they split on thresholds per feature and don't care about scale.

### Standardization vs. Normalization

| | Standardization (Z-score) | Normalization (Min-Max) |
|---|---|---|
| Formula | `(x - mean) / std` | `(x - min) / (max - min)` |
| Resulting range | Centered at 0, unit variance (no fixed bounds) | Fixed to `[0, 1]` |
| Sensitive to outliers? | Less sensitive | Very sensitive — one extreme value stretches the whole range |
| `sklearn` tool | `StandardScaler` | `MinMaxScaler` |
| Use when | Data roughly bell-shaped, or algorithm assumes centered data (logistic regression, linear regression, PCA) | You need a bounded range (e.g. neural network inputs, image pixel values) |

```text
Standardization:        Normalization:
   x - mean                  x - min
  ─────────                ───────────
     std                     max - min

  centers around 0          squeezes into [0, 1]
  no fixed upper/lower       fixed upper/lower bound
```

**Golden rule (same family as encoding):** fit the scaler on **training data only** — learn the mean/std (or min/max) from train — then use those *same* learned values to transform validation and test. Never re-fit on validation or test data; that leaks their distribution into what should be an unbiased evaluation.

**Key teaching point:** Scaling changes the *numbers*, never the *order* or the *relationships* within a column. A customer with more tenure than another still has more tenure after scaling — we're just putting every column on a comparable footing for the algorithm's math.

---

## Practical Block 4: Scale Features, Beat the Baseline (10 min)

```python
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.linear_model import LogisticRegression

num_cols = ['tenure_months', 'monthly_charges']

# --- Standardization: fit on train, transform train/val/test ---
scaler = StandardScaler()
X_train_scaled = X_train_enc.copy()
X_val_scaled = X_val_enc.copy()
X_test_scaled = X_test_enc.copy()

X_train_scaled[num_cols] = scaler.fit_transform(X_train_enc[num_cols])
X_val_scaled[num_cols] = scaler.transform(X_val_enc[num_cols])
X_test_scaled[num_cols] = scaler.transform(X_test_enc[num_cols])

print("Before scaling:")
print(X_train_enc[num_cols].describe().round(2).loc[['mean', 'std', 'min', 'max']])
print("\nAfter StandardScaler:")
print(X_train_scaled[num_cols].describe().round(2).loc[['mean', 'std', 'min', 'max']])
```

**Output:**
```
Before scaling:
      tenure_months  monthly_charges
mean          37.44          1393.99
std           19.73           654.48
min            2.00           330.66
max           72.00          2483.23

After StandardScaler:
      tenure_months  monthly_charges
mean           0.00             0.00
std            1.00             1.00
min           -1.80            -1.63
max            1.76             1.67
```

```python
# --- Normalization for comparison (not used further today) ---
minmax = MinMaxScaler()
X_train_norm_demo = pd.DataFrame(minmax.fit_transform(X_train_enc[num_cols]), columns=num_cols)
print("After MinMaxScaler:")
print(X_train_norm_demo.describe().round(2).loc[['mean', 'min', 'max']])
```

**Output:**
```
After MinMaxScaler:
      tenure_months  monthly_charges
mean           0.51             0.49
min            0.00             0.00
max            1.00             1.00
```

```python
# --- Now fit a real model and compare to the baseline ---
model = LogisticRegression(max_iter=1000)
model.fit(X_train_scaled, y_train)

val_acc = accuracy_score(y_val, model.predict(X_val_scaled))
print("LogisticRegression validation accuracy:", round(val_acc, 3))
print("Baseline validation accuracy:          ", round(baseline_val_acc, 3))
print("Beats baseline?", val_acc > baseline_val_acc)

test_acc = accuracy_score(y_test, model.predict(X_test_scaled))
baseline_test_acc = accuracy_score(y_test, dummy.predict(X_test))
print("\nFinal test accuracy — model:   ", round(test_acc, 3))
print("Final test accuracy — baseline:", round(baseline_test_acc, 3))
```

**Output:**
```
LogisticRegression validation accuracy: 0.7
Baseline validation accuracy:           0.633
Beats baseline? True

Final test accuracy — model:    0.833
Final test accuracy — baseline: 0.633
```

**Walk through:** We did not tune anything — default `LogisticRegression`, one pass. It still clears the baseline on both validation (0.700 vs 0.633) and test (0.833 vs 0.633). That gap is the first evidence in this course that a model has "learned" something real from the features, not just inherited the class imbalance.

**Ask the class:** *"We only have 200 rows total, and a 15-point gap on test. Is that gap something we should trust completely?"* Do not fully answer — this is the seed for next session's "Avoiding ML Pitfalls & Model Generalization," which covers exactly how much to trust small-sample results.

---

## Summary & Wrap-Up (5 min)

**What we covered today:**
- Problem framing: turning a business question into "what is X, what is y, classification or regression?"
- Features (X) vs. Label (y), and why leakage-prone or identifier columns don't belong in X
- Train / validation / test — three sets, three jobs, and why the test set is touched exactly once
- Stratified splitting to preserve class balance across all three sets
- Baselines: the majority-class (or mean) predictor you must beat before trusting any "real" model
- Categorical encoding: one-hot for nominal data, ordinal for ordered categories, always fit on train only
- Standardization vs. normalization, and why scale-sensitive algorithms need one of them

**Bridge to next session:** *"Today our model beat the baseline — but on only 200 rows, with no tuning, no cross-validation, and one lucky-or-unlucky test split. Next class, 'Avoiding ML Pitfalls & Model Generalization,' is entirely about whether results like today's actually generalize — overfitting, data leakage, and the traps that make a model look good in the classroom and fail in the real world."*

**Homework / self-practice:** Pick any small tabular dataset (or reuse today's churn dataset with a different `random_state`). Reframe it as a regression problem instead (predict `monthly_charges` from the other columns), compute a mean baseline, and check whether a simple `LinearRegression` beats it.

---

## Q&A & Doubt Solving (5 min)

**Likely questions and suggested answers:**

**Q: Why do we need a validation set at all — can't we just use train and test?**
→ You *can*, for a quick prototype. But the moment you compare two models or tune a setting and pick based on test performance, test stops being unbiased. Validation exists to be the set you're "allowed" to peek at repeatedly during that process.

**Q: What if my baseline accuracy is really high, like 95%, because one class is rare?**
→ That's exactly the trap this session is warning about. A 95% baseline means your "real" model needs to clear 95% to prove anything — accuracy alone becomes almost useless there. We'll cover better metrics for this exact situation (precision, recall) next session.

**Q: Do I always need both a scaler and an encoder?**
→ Only if you have both numeric and categorical features and you're using a scale-sensitive algorithm. Tree-based models don't need scaling at all. But encoding categorical columns to numbers is required for virtually every `sklearn` model, tree-based or not.

**Q: Why `drop_first=True` in one-hot encoding — doesn't that lose information?**
→ No information is lost. If a column has categories A, B, C, D and you keep B, C, D as dummy columns, "not B, not C, not D" already implies A. The dropped category becomes the implicit baseline.

**Q: Can I fit the scaler on the full dataset before splitting, just to save a step?**
→ No — that is a leakage mistake, the same category as touching the test set early. The scaler would "see" the mean/std of your test rows before you ever evaluate on them, giving an overly optimistic result that won't hold up on truly new data.

**Q: My `X_val_enc` had fewer columns than `X_train_enc` after one-hot encoding — what happened?**
→ A category present in train didn't happen to appear in your smaller validation slice, so `pd.get_dummies` never created that column there. Always `reindex` val/test to match train's columns (with `fill_value=0`) before feeding them to a model.

---

## Instructor Notes

- **Dataset:** The synthetic churn dataset is generated with `np.random.default_rng(42)` — fully reproducible, no internet needed. Keep `random_state=42` consistent across all splits/models in this session so printed numbers match what's on screen for students following along.
- **Common student mistake:** Fitting `StandardScaler`/`OneHotEncoder`/`pd.get_dummies` on the *entire* dataset before splitting. Catch this early — ask "what did you `.fit()` before or after `train_test_split`?" as a standing check-in question throughout Module 2.
- **Live coding tip:** Deliberately skip `stratify=y` once and show the churn ratio drift across splits with only 200 rows — the effect is visible and makes the abstract concept concrete in seconds.
- **For advanced students:** Have them try `OrdinalEncoder` on `contract_type` (preserving Month-to-month < One year < Two year) instead of one-hot, refit the model, and compare validation accuracy. Also worth showing `ColumnTransformer` as the production-grade way to bundle encoding + scaling into one object (full depth comes later in the module).
- **Time check:** If running long after the break, merge Practical 3 and 4 into a single live-coded pass and assign the standalone accuracy comparison as a two-minute silent exercise instead of talking through every print statement.
