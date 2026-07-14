# Lecture Script: Regression Models & Regularization
> **Instructor Reference** — Module 2: Classical ML | Session 3 | Duration: 2 Hours

---

## Session Overview

**Goal:** Students can fit a Linear Regression model, read the slope and intercept as concrete real-world numbers, understand what OLS is actually minimizing, and know when and how to use Ridge and Lasso to control overfitting via the `alpha` hyperparameter.

**Student profile at this point:** Comfortable with the ML workflow (features/labels, train/test split, baselines, encoding, scaling) and aware of leakage, overfitting/underfitting, and simple cross-validation from Session 2. Have not yet studied any specific model family in depth — this is their first real model.

**Key outcome:** By end of class, every student can fit `LinearRegression`, `Ridge`, and `Lasso`, explain a coefficient in plain language, and describe — with a live demo as proof — why regularization trades a little bias for a lot less variance.

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| Opening & Context | 5 min | 0:05 |
| **Concept 1:** Linear Regression — Fitting a Line to Data | 10 min | 0:15 |
| **Practical 1:** Fit, Predict, and Read the Slope | 15 min | 0:30 |
| **Concept 2:** OLS — What `.fit()` Is Actually Minimizing | 10 min | 0:40 |
| **Practical 2:** Multiple Regression — Coefficients With Context | 15 min | 0:55 |
| **BREAK** | 10 min | 1:05 |
| **Concept 3:** When Lines Become Curves — The Overfitting Trap | 10 min | 1:15 |
| **Practical 3:** Watch a Model Overfit in Real Time | 15 min | 1:30 |
| **Concept 4:** Ridge, Lasso & the Bias–Variance Tradeoff | 10 min | 1:40 |
| **Practical 4:** Alpha Tuning — Shrinking Coefficients on Purpose | 10 min | 1:50 |
| Summary & Wrap-Up | 5 min | 1:55 |
| Q&A & Doubt Solving | 5 min | 2:00 |

---

## Opening (5 min)

**Hook:** Draw a scatter plot on the board — dots roughly trending upward, left to right. Ask: *"If I asked you to draw ONE straight line through this mess that best represents the trend, how would you decide where it goes?"*

Let 2-3 students describe their intuition ("average distance from the line," "make it look balanced," "minimize the gap"). Then reveal: *"What you just described, informally, is exactly what a computer does — except it does it with math, precisely, in milliseconds. That math has a name: Ordinary Least Squares. Today you learn to do it properly, and — just as important — to stop it from doing it *too* well."*

**Context to set:** Linear Regression is the oldest, simplest, and still one of the most-used models in the industry. It is not "basic" — it is foundational. Every regularized model, every neural network's output layer for regression, every "how much does X affect Y" business question starts here. And its biggest trap — fitting the training data too perfectly — is the exact overfitting problem you learned to detect last session. Today you learn to fix it.

**Learning contract for today:**
- Fit a Linear Regression model and explain what its coefficients mean in real units
- Understand what OLS is minimizing when you call `.fit()`
- Watch a model overfit live, and understand why
- Use Ridge and Lasso with the `alpha` parameter to control that overfitting

---

## Concept Block 1: Linear Regression — Fitting a Line to Data (10 min)

### The Idea

Linear Regression assumes the relationship between a feature `X` and a target `y` can be approximated by a straight line:

```
y = intercept + slope * X
   (also written: y = b0 + b1*X1 )
```

With more than one feature, it generalizes to a **hyperplane**:

```
y = intercept + b1*X1 + b2*X2 + ... + bn*Xn
```

Each `b` is a **coefficient** — how much `y` changes per one-unit increase in that feature, holding all other features fixed.

```
        price
          |                              *
          |                        *
          |                  *  *
          |            *  *
          |      *  *
          |   *
          +------------------------------- size (sqft)
              the line minimizes the vertical
              distance to every point
```

### Slope, Intercept, and What They Mean

| Term | Symbol | Plain-English meaning |
|---|---|---|
| Intercept | `b0` | Predicted `y` when every feature is 0 (often not realistic on its own — a starting reference point, not a real house) |
| Slope / coefficient | `b1`, `b2`, ... | How much `y` changes per +1 unit of that feature, all else held constant |
| Residual | `y - ŷ` | The error the line does NOT explain — this is what we minimize |

**Teaching point:** A coefficient is not just a number — it is a **rate**. "0.05" is meaningless on its own. "₹0.05 lakh more price for every additional sqft of size, holding other features fixed" is a business insight. Always translate coefficients into units your stakeholders understand.

---

## Practical Block 1: Fit, Predict, and Read the Slope (15 min)

### Dataset
A small, self-contained dataset of flats in an Indian metro — size in sqft vs. price in ₹ lakhs, built with a fixed random seed so every student gets identical numbers.

```python
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Build a small, self-contained housing dataset
rng = np.random.default_rng(42)
n = 20
size_sqft = rng.integers(600, 2500, n)
noise = rng.normal(0, 8, n)  # noise in lakhs
price_lakhs = 20 + 0.05 * size_sqft + noise

house_df = pd.DataFrame({
    "size_sqft": size_sqft,
    "price_lakhs": price_lakhs.round(1)
})
print(house_df)
```

**Output (first and last few rows shown on screen):**
```
    size_sqft  price_lakhs
0         769         65.5
1        2070        129.7
2        1843        112.7
3        1433        100.7
...
18       2195        133.1
19       1455         96.2
```

```python
# Fit simple linear regression: price ~ size
X = house_df[["size_sqft"]]
y = house_df["price_lakhs"]

model = LinearRegression()
model.fit(X, y)

print("Slope (coef_):", model.coef_)
print("Intercept:", model.intercept_)
```

**Output:**
```
Slope (coef_): [0.0458253]
Intercept: 28.312824093840817
```

```python
# Predict for a 1500 sqft flat
pred_1500 = model.predict(pd.DataFrame({"size_sqft": [1500]}))
print("Predicted price for 1500 sqft flat:", round(pred_1500[0], 2), "lakhs")

y_pred = model.predict(X)
print("R^2 on training data:", round(r2_score(y, y_pred), 4))
print("MSE on training data:", round(mean_squared_error(y, y_pred), 4))
```

**Output:**
```
Predicted price for 1500 sqft flat: 97.05 lakhs
R^2 on training data: 0.9676
MSE on training data: 19.9869
```

**Walk through:** `coef_` is always an array (even with one feature) because sklearn is built for multiple features by default. `0.0458` lakh per sqft = **≈ ₹4,580 more price for every extra sqft**. Say that sentence out loud — this is the moment students should feel the number become real. The intercept (₹28.3 lakh) is the model's prediction at size=0, which is not a real flat — don't over-interpret it here.

**Discussion prompt:** *"If this slope were negative, what would that mean about this housing market?"* (Bigger flats being cheaper — possible in some contexts, e.g. old dense city cores vs. new construction on the outskirts.)

---

## Concept Block 2: OLS — What `.fit()` Is Actually Minimizing (10 min)

### Ordinary Least Squares (OLS)

When you call `.fit()`, `LinearRegression` is solving an optimization problem: find the intercept and slope that make the **Sum of Squared Errors (SSE)** between actual and predicted values as small as possible.

```
SSE = Σ (y_actual - y_predicted)^2
```

```
Why SQUARED errors, not just errors?
├── Squaring makes all errors positive (no cancellation between over- and under-predictions)
├── Squaring penalizes large errors much more than small ones
└── The squared function is smooth and differentiable — calculus can find its exact minimum
```

For simple linear regression, this minimum has a **closed-form solution** — no iteration needed:

```
beta = (X^T X)^-1 X^T y        (the "Normal Equation")
```

`LinearRegression` in sklearn solves this directly (or via an equivalent stable numerical method) — this is why fitting a linear model is nearly instant even on large data, unlike models trained by gradient descent over many epochs.

| Term | Symbol | Plain-English meaning |
|---|---|---|
| SSE | Σ(y - ŷ)² | Total squared error — the quantity OLS minimizes |
| Normal Equation | (XᵀX)⁻¹Xᵀy | The formula that directly computes the minimizing coefficients |
| Closed-form | — | Solved in one calculation, not iterative search |

**Teaching point:** "Best fit line" is not a vague phrase — it has one precise mathematical definition: the line with the lowest possible sum of squared residuals across all possible lines. There is exactly one such line for a given dataset (assuming no perfectly collinear features), and `.fit()` finds it exactly, not approximately.

---

## Practical Block 2: Multiple Regression — Coefficients With Context (15 min)

We first prove OLS is really doing what we claim, then scale it up to multiple features.

```python
# Manual OLS via the Normal Equation, compared to sklearn
X_arr = house_df[["size_sqft"]].values
y_arr = house_df["price_lakhs"].values

X_design = np.column_stack([np.ones(len(X_arr)), X_arr])  # add intercept column
beta = np.linalg.inv(X_design.T @ X_design) @ X_design.T @ y_arr
print("Normal equation intercept, slope:", beta[0], beta[1])
print("sklearn intercept, slope:        ", model.intercept_, model.coef_[0])

# Prove it's a minimum: nudge the slope slightly and watch SSE go UP either way
def sse(slope, intercept):
    pred = intercept + slope * X_arr.flatten()
    return np.sum((y_arr - pred) ** 2)

print("\nSSE at OLS slope:      ", round(sse(beta[1], beta[0]), 2))
print("SSE at slope - 0.01:   ", round(sse(beta[1] - 0.01, beta[0]), 2))
print("SSE at slope + 0.01:   ", round(sse(beta[1] + 0.01, beta[0]), 2))
```

**Output:**
```
Normal equation intercept, slope: 28.312824093840817 0.045825297306094755
sklearn intercept, slope:         28.312824093840817 0.04582529730609474

SSE at OLS slope:       399.74
SSE at slope - 0.01:    6228.84
SSE at slope + 0.01:    6228.84
```

**Walk through:** sklearn's answer and the hand-rolled Normal Equation answer match to many decimal places — proof `.fit()` is not "magic," it is this formula. Nudging the slope in *either* direction from the OLS solution makes SSE jump from ~400 to ~6,229 — that's the "valley bottom" of the error curve, and OLS finds the exact bottom.

### Now scale up: multiple features

```python
# Re-seed so this cell is self-contained and reproducible on its own
# (size_sqft comes out identical to Practical 1 since it's the same
# seed and the same first draw — bedrooms/age/distance are new columns)
rng = np.random.default_rng(42)
size_sqft = rng.integers(600, 2500, n)
bedrooms = rng.integers(1, 5, n)
age_years = rng.integers(0, 25, n)
distance_km = rng.uniform(1, 20, n).round(1)
noise2 = rng.normal(0, 6, n)

price2 = (20 + 0.05 * size_sqft + 8 * bedrooms
          - 0.6 * age_years - 1.2 * distance_km + noise2)

house_df2 = pd.DataFrame({
    "size_sqft": size_sqft, "bedrooms": bedrooms,
    "age_years": age_years, "distance_km": distance_km,
    "price_lakhs": price2.round(1)
})

X2 = house_df2[["size_sqft", "bedrooms", "age_years", "distance_km"]]
y2 = house_df2["price_lakhs"]

model2 = LinearRegression()
model2.fit(X2, y2)

coef_table = pd.DataFrame({"feature": X2.columns, "coefficient": model2.coef_.round(3)})
print(coef_table)
print("Intercept:", round(model2.intercept_, 3))
print("R^2:", round(r2_score(y2, model2.predict(X2)), 4))
```

**Output:**
```
       feature  coefficient
0    size_sqft        0.047
1     bedrooms        8.040
2    age_years       -0.596
3  distance_km       -0.839

Intercept: 20.868
R^2: 0.9638
```

**Walk through — read each row as a sentence:**
- "Holding bedrooms, age, and distance fixed, each extra sqft adds ~₹4,700 to price."
- "Holding size, age, and distance fixed, each extra bedroom adds ~₹8.04 lakh to price."
- "Holding size, bedrooms, and distance fixed, each extra year of age *reduces* price by ~₹0.60 lakh."
- "Holding size, bedrooms, and age fixed, each extra km from the city center reduces price by ~₹0.84 lakh."

**Teaching point:** "Holding other features constant" is the single most important phrase in interpreting multiple regression. A coefficient never tells you what happens in isolation — it tells you what happens to `y` when *only* that one feature moves and every other feature in the model stays put.

**Discussion prompt:** *"`age_years` and `distance_km` are both negative. Does that mean old flats far from the city are worthless? What's missing from this model?"* (Interaction effects, non-linearity, neighborhood quality, etc. — a good preview that linear models assume additive, straight-line effects.)

---

## BREAK (10 min)

*Suggested break prompt — ask students to guess, before the break ends: "If I now fit an extremely flexible curve instead of a straight line to this same data, will my training error go up or down? What about test error?" Collect a few guesses on the board to revisit after the break.*

---

## Concept Block 3: When Lines Become Curves — The Overfitting Trap (10 min)

### From Line to Curve

A straight line is a **degree-1 polynomial**. Nothing stops us from fitting degree-2, degree-4, or degree-12 curves the exact same way — just by adding `X²`, `X³`, ... as extra features and running the same Linear Regression machinery on top of them (`PolynomialFeatures` + `LinearRegression`).

```
Degree 1:  y = b0 + b1*X                          (a line — can underfit)
Degree 2:  y = b0 + b1*X + b2*X^2                  (a gentle curve)
Degree 8:  y = b0 + b1*X + b2*X^2 + ... + b8*X^8   (a wiggly curve —
                                                     can memorize noise)
```

```
error
  |  \                                    ___
  |   \  train error                 ____/
  |    \______                  ____/    test error
  |           \______      ____/
  |                  \____/
  +---------------------------------------------- model flexibility
      underfit      "just right"        overfit
```

This is exactly the overfitting story from Session 2 — but now you will *watch it happen with numbers*, not just hear about it.

### Why This Matters for Regression Specifically

| Degree | Training error | Test error | What's happening |
|---|---|---|---|
| Too low (e.g. 1 on curved data) | High | High | Underfitting — model too simple to capture the pattern |
| Just right | Low-ish | Low | Good generalization |
| Too high (e.g. 12 on 12 data points) | Near zero | Wildly unstable / huge | Overfitting — model memorizes noise, not signal |

**Teaching point:** A model that gets *perfect* training accuracy is not a good sign — with a small, noisy dataset, it usually means the model has enough flexibility to fit the noise itself, and noise never repeats the same way on new data. This is precisely why we always evaluate on a held-out test set, as you learned last session.

---

## Practical Block 3: Watch a Model Overfit in Real Time (15 min)

```python
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split

# Small, noisy 1-D dataset -- easy to overfit with high-degree polynomials
rng2 = np.random.default_rng(7)
n2 = 18
size2 = np.sort(rng2.uniform(600, 2500, n2))
true_price = 20 + 0.05 * size2
noise3 = rng2.normal(0, 10, n2)
price3 = true_price + noise3

Xp = size2.reshape(-1, 1)
yp = price3
X_train, X_test, y_train, y_test = train_test_split(Xp, yp, test_size=0.3, random_state=42)
print("Train size:", len(X_train), " Test size:", len(X_test))

results = []
for degree in [1, 2, 4, 8, 12]:
    poly_model = make_pipeline(PolynomialFeatures(degree), LinearRegression())
    poly_model.fit(X_train, y_train)
    train_mse = mean_squared_error(y_train, poly_model.predict(X_train))
    test_mse = mean_squared_error(y_test, poly_model.predict(X_test))
    results.append((degree, round(train_mse, 2), round(test_mse, 2)))

results_df = pd.DataFrame(results, columns=["degree", "train_mse", "test_mse"])
print(results_df)
```

**Output:**
```
Train size: 12  Test size: 6
   degree  train_mse  test_mse
0       1      56.01     95.73
1       2      46.74    164.74
2       4      36.27   6492.79
3       8      29.12    222.72
4      12      31.63    252.71
```

**Walk through:** Train MSE mostly falls as degree increases (the model bends to fit every training point more closely). But test MSE does *not* fall in step — it becomes wildly unstable, spiking to 6,492 at degree 4. This instability is itself the signature of overfitting: with only 12 training points, high-degree curves swing wildly between them, and small changes in which points happen to be "held out" produce huge swings in test error. **A flexible model on a small dataset is not a more accurate model — it is a less trustworthy one.**

**Discussion prompt:** *"We only have 18 data points total. If we had 18,000 instead, would degree-12 still overfit this badly?"* (More data usually tames overfitting for a given model complexity — but we can't always collect more data, which is exactly why regularization exists.)

---

## Concept Block 4: Ridge, Lasso & the Bias–Variance Tradeoff (10 min)

### The Core Idea: Penalize Large Coefficients

Both Ridge and Lasso start from the same OLS objective and add a **penalty term** that discourages large coefficients:

```
OLS:    minimize   SSE
Ridge:  minimize   SSE + alpha * Σ(b_i)^2        <- L2 penalty ("squared")
Lasso:  minimize   SSE + alpha * Σ|b_i|          <- L1 penalty ("absolute value")
```

`alpha` controls how much we penalize large coefficients:

```
alpha = 0        -> identical to plain LinearRegression (no penalty)
alpha small      -> mild shrinkage, still flexible
alpha large      -> strong shrinkage, coefficients pushed toward 0
alpha huge       -> almost every coefficient forced to (near) 0
```

### Ridge vs. Lasso — the Key Difference

| | Ridge (L2) | Lasso (L1) |
|---|---|---|
| Penalty | Sum of squared coefficients | Sum of absolute coefficients |
| Effect on coefficients | Shrinks all toward 0, rarely exactly 0 | Can shrink coefficients to **exactly 0** |
| Practical use | Keep all features, reduce their influence | Automatic feature selection |
| Good when | Most features are somewhat useful | Many features are irrelevant / redundant |

### Tying This to the Bias–Variance Tradeoff (Session 2)

```
alpha too low  -> behaves like plain OLS -> LOW bias, HIGH variance -> overfits
alpha too high -> coefficients crushed to 0 -> HIGH bias, LOW variance -> underfits
alpha "just right" -> the sweet spot that minimizes TEST error
```

**Teaching point:** Regularization does not make a model "smarter" — it deliberately makes it *less* flexible, trading a small amount of bias (it can no longer fit training data perfectly) for a large reduction in variance (it stops chasing noise). `alpha` is the dial that controls exactly how much of that trade you make, and there is no universally correct value — it must be tuned per dataset (a topic we formalize with cross-validation search in a later session).

---

## Practical Block 4: Alpha Tuning — Shrinking Coefficients on Purpose (10 min)

We reuse the same degree-8 polynomial features that just overfit catastrophically, and apply Ridge and Lasso on top.

```python
from sklearn.linear_model import Ridge, Lasso
from sklearn.preprocessing import StandardScaler

poly = PolynomialFeatures(degree=8)
X_train_poly = poly.fit_transform(X_train)
X_test_poly = poly.transform(X_test)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train_poly)
X_test_scaled = scaler.transform(X_test_poly)

alphas = [0.01, 0.1, 1, 10, 100]

# Plain LinearRegression for comparison
lin = LinearRegression()
lin.fit(X_train_scaled, y_train)
print("Plain LinearRegression:")
print(" Coef L2 norm:", round(np.linalg.norm(lin.coef_), 2))
print(" Test MSE:", round(mean_squared_error(y_test, lin.predict(X_test_scaled)), 2))
```

**Output:**
```
Plain LinearRegression:
 Coef L2 norm: 176290754.43
 Test MSE: 24907629.27
```

**Walk through:** Look at that coefficient norm — 176 million. With only 12 training points and 9 polynomial features, unregularized Linear Regression's coefficients explode to nonsensical magnitudes trying to thread through every point exactly, and test MSE explodes with them (~25 million!). This is overfitting in its most dramatic, unmistakable form.

```python
ridge_rows = []
for alpha in alphas:
    ridge = Ridge(alpha=alpha)
    ridge.fit(X_train_scaled, y_train)
    train_mse = mean_squared_error(y_train, ridge.predict(X_train_scaled))
    test_mse = mean_squared_error(y_test, ridge.predict(X_test_scaled))
    ridge_rows.append((alpha, round(np.linalg.norm(ridge.coef_), 2), round(train_mse, 2), round(test_mse, 2)))
print(pd.DataFrame(ridge_rows, columns=["alpha", "coef_L2_norm", "train_mse", "test_mse"]))

lasso_rows = []
for alpha in alphas:
    lasso = Lasso(alpha=alpha, max_iter=20000)
    lasso.fit(X_train_scaled, y_train)
    train_mse = mean_squared_error(y_train, lasso.predict(X_train_scaled))
    test_mse = mean_squared_error(y_test, lasso.predict(X_test_scaled))
    n_nonzero = int(np.sum(lasso.coef_ != 0))
    lasso_rows.append((alpha, n_nonzero, round(train_mse, 2), round(test_mse, 2)))
print(pd.DataFrame(lasso_rows, columns=["alpha", "nonzero_coefs", "train_mse", "test_mse"]))
```

**Output:**
```
   alpha  coef_L2_norm  train_mse  test_mse
0   0.01         53.05      44.28    188.99
1   0.10         27.85      50.00    106.56
2   1.00         16.12      62.11    130.08
3  10.00          8.58     112.42    346.05
4 100.00          3.98     278.50    945.00

   alpha  nonzero_coefs  train_mse  test_mse
0   0.01              4      43.12    248.78
1   0.10              2      49.48    109.56
2   1.00              1      57.01    100.90
3  10.00              1     156.01    392.60
4 100.00              0     661.75   1805.85
```

**Walk through, point by point:**
- The instant we add *any* regularization (alpha=0.01), the coefficient norm crashes from 176 million to ~53 — Ridge is doing exactly what it promises.
- As alpha climbs, `coef_L2_norm` shrinks steadily: 53 → 28 → 16 → 8.6 → 4.0. More penalty, smaller coefficients — visible, monotonic, predictable.
- Test MSE is best around alpha=0.1 (106.56) for Ridge — too little regularization (0.01) still leaves some overfitting; too much (100) underfits and test error rises again to 945. That's the bias–variance sweet spot, live in a table.
- Lasso's `nonzero_coefs` column tells its own story: 4 → 2 → 1 → 1 → **0**. At alpha=100, Lasso has zeroed out *every* coefficient — the model has been regularized into predicting a constant. This is Lasso doing automatic feature selection, something Ridge structurally cannot do.

```python
print("Ridge coefficients, first 5, by alpha:")
for a in [0.01, 1, 100]:
    r = Ridge(alpha=a).fit(X_train_scaled, y_train)
    print(f" alpha={a}: {np.round(r.coef_[:5], 3)}")

print("\nLasso coefficients, first 5, by alpha:")
for a in [0.01, 1, 100]:
    l = Lasso(alpha=a, max_iter=20000).fit(X_train_scaled, y_train)
    print(f" alpha={a}: {np.round(l.coef_[:5], 3)}")
```

**Output:**
```
Ridge coefficients, first 5, by alpha:
 alpha=0.01: [  0.     46.362   2.147 -15.79  -15.972]
 alpha=1: [ 0.    12.45   8.199  4.807  2.258]
 alpha=100: [0.    1.692 1.608 1.518 1.429]

Lasso coefficients, first 5, by alpha:
 alpha=0.01: [  0.     58.982  -0.    -49.921  -0.   ]
 alpha=1: [ 0.    23.612  0.     0.     0.   ]
 alpha=100: [0. 0. 0. 0. 0.]
```

**Walk through:** Watch Ridge's coefficients shrink toward zero *without ever quite reaching it*, even at alpha=100. Now watch Lasso: several entries are already exactly `-0.`/`0.` at alpha=0.01, and by alpha=1 only one survives. This side-by-side is the cleanest way to make the L1-vs-L2 distinction land — Ridge shrinks, Lasso selects.

**Discussion prompt:** *"If you had 200 features and suspected only 10 actually mattered, would you reach for Ridge or Lasso first? Why?"* (Lasso — its ability to zero out coefficients doubles as a feature-selection tool, which Ridge cannot do because L2 shrinkage rarely produces exact zeros.)

---

## Summary & Wrap-Up (5 min)

**What we covered today:**
- Linear Regression fits a line/hyperplane; each coefficient is a rate — "Δy per +1 unit of X, holding others constant"
- OLS is the precise mathematical objective `.fit()` solves: minimize the sum of squared residuals, via the Normal Equation
- Multiple regression coefficients must always be read "holding other features constant"
- Polynomial features let a linear model fit curves — and with too much flexibility on too little data, it overfits catastrophically (we saw coefficient norms explode to 176 million)
- Ridge (L2) shrinks all coefficients smoothly; Lasso (L1) can shrink coefficients to exactly zero, giving free feature selection
- `alpha` is the bias–variance dial: too low overfits, too high underfits, and the sweet spot must be found empirically

**Bridge to next session:** *"Today we fit models and eyeballed MSE and R² to judge them. Next class — Evaluating Regression Performance — we formalize exactly how to measure and compare regression models properly, including metrics beyond MSE and what each one tells you that the others don't."*

**Homework / self-practice:** Take the `house_df2` (multiple-feature) dataset from Practical 2, fit Ridge and Lasso with `alpha` in `[0.01, 1, 10, 100]`, and write down: at what alpha does Lasso first zero out the `age_years` coefficient? What does that tell you about how much `age_years` was contributing versus `size_sqft`?

---

## Q&A & Doubt Solving (5 min)

**Likely questions and suggested answers:**

**Q: Do I always need to scale my features before Ridge/Lasso?**
→ Yes, strongly recommended. Both penalties are applied to the raw coefficient values, and coefficients are scale-dependent — a feature measured in thousands will naturally get a tiny coefficient and a feature measured in single digits will get a large one, so the penalty would unfairly punish one over the other. `StandardScaler` first, then regularize.

**Q: If alpha=0 makes Ridge identical to plain LinearRegression, why not just always use a tiny alpha "to be safe"?**
→ You can, and many practitioners do use a small default. But "safe" is dataset-dependent — the only way to know the right alpha is to tune it against a validation set (or cross-validation, which we formalize soon). A tiny alpha on a dataset that badly needs regularization won't help much.

**Q: Why does Lasso zero out coefficients but Ridge doesn't?**
→ It's a geometry argument: the L1 penalty region has sharp corners exactly on the axes, and the OLS solution is more likely to land on one of those corners (where a coefficient is exactly 0). The L2 penalty region is a smooth circle/sphere with no corners, so the solution can get close to an axis but essentially never lands exactly on it.

**Q: Can I mix Ridge and Lasso?**
→ Yes — that's called **ElasticNet**, which combines both L1 and L2 penalties with a mixing ratio. Worth mentioning it exists; we won't code it today, but it's a one-line swap once you understand Ridge and Lasso.

**Q: My R² went DOWN after adding Ridge. Did I do something wrong?**
→ Not necessarily. Training R² almost always drops slightly with regularization — that's the "bias" you're intentionally trading for lower variance. What matters is whether *test* R² improved. Always compare on held-out data, never on training data alone.

**Q: Is a negative coefficient always a "bad" thing, like `age_years` being negative for house price?**
→ No — negative just means an inverse relationship. Older flats being cheaper is intuitive, not "bad." Only worry if a coefficient's sign contradicts domain knowledge you're confident about (that's usually a sign of leakage, multicollinearity, or a data problem, not a modeling mistake).

---

## Instructor Notes

- **Dataset:** All data in this session is synthetically generated with `numpy.random.default_rng(seed)` — fully reproducible, no internet dependency, and every student sees identical numbers, which makes debugging shared errors far easier.
- **Common student mistake:** Forgetting to scale features before Ridge/Lasso, then being confused why regularization "did nothing" or shrank one feature much faster than another. Make scaling a checklist item every time regularization comes up.
- **Common student mistake:** Reading `model.coef_` without checking which column order `X` was built in — coefficients line up positionally with `X.columns`, and mismatched interpretation is an easy, silent error. Always print a coefficient table with feature names attached, as done in Practical 2.
- **Live-coding tip:** The "coefficient norm explodes to 176 million" moment in Practical 4 is the single best gasp-inducing moment in this session — slow down there, let it sink in, and consider re-running with a different `random_state` live to show it's not a one-off fluke.
- **Notes for advanced students:** Mention `RidgeCV` and `LassoCV`, which pick `alpha` automatically via built-in cross-validation — useful to preview since manual alpha sweeps like today's do not scale well to many features.
- **Time-check contingency:** If running behind after the break, compress Practical 3 to just degrees `[1, 4, 12]` instead of five values — the overfitting story still lands with three points, and it buys 3-4 minutes for Practical 4, which is the session's core payoff.
