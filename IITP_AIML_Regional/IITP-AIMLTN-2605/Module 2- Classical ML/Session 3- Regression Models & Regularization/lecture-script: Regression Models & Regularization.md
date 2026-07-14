# Lecture Script: Regression Models & Regularization
> **Instructor Reference** — Module 2: Classical ML | Session 3 | Duration: 2 Hours

---

## Session Overview

**Goal:** Students fit and *read* a multi-feature linear regression, deliberately break it with a high-degree polynomial, then repair it with scaling and a regularisation penalty whose strength they tune with cross-validation.

**Student profile at this point:** They have completed Sessions 1–2. They know the ML workflow, `train_test_split`, `.fit()` / `.predict()`, what overfitting is, and how cross-validation works. They have never fitted a regression model with more than an intuitive sense of "a line through points". scikit-learn is still new.

**Key outcome:** A notebook in which they can point at a coefficient and say what the model learned, show a train/test score gap opening up as complexity rises, and close that gap with `Ridge` / `Lasso` at a cross-validated alpha.

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| Opening — The Model That Scored 0.84 and Was Useless | 5 min | 0:05 |
| **Concept 1:** Linear Regression — One Weight Per Feature | 10 min | 0:15 |
| **Practical 1:** Fit, read `coef_` and `intercept_`, predict | 15 min | 0:30 |
| **Concept 2:** Polynomial Regression — Flexibility Invites Overfitting | 10 min | 0:40 |
| **Practical 2:** `PolynomialFeatures` at degree 1, 2, 5, 15 | 15 min | 0:55 |
| **BREAK** | 10 min | 1:05 |
| **Concept 3:** Regularisation — A Penalty for Large Coefficients | 10 min | 1:15 |
| **Practical 3:** Scaling, then Ridge vs Lasso vs ElasticNet | 15 min | 1:30 |
| **Concept 4:** Alpha — The Bias–Variance Dial | 10 min | 1:40 |
| **Practical 4:** Coefficient shrinkage + `RidgeCV` / `LassoCV` | 10 min | 1:50 |
| Summary & Wrap-Up | 5 min | 1:55 |
| Q&A & Doubt Solving | 5 min | 2:00 |

---

## Opening (5 min)

**Hook — run this live, before explaining anything.** Fit two models to the same 30 points and put only the two score-pairs on screen:

```
Degree 2  ->  train R2 = 0.677   test R2 =  0.680
Degree 15 ->  train R2 = 0.842   test R2 = -1,550,989
```

*"The second model fits the training data better — it sits measurably closer to the points it was trained on. By that measure it is the superior model. Would you ship it?"*

Let them sit with the negative number. Someone will ask how R² can be negative — tell them it means the model is spectacularly worse than just guessing the average every time, and that we will not dwell on the metric itself today because Session 4 is entirely about metrics.

**What regression is NOT:**
- Drawing the line that gets closest to your training points at any cost
- A method where "more flexible model" reliably means "better model"
- Something you can trust without ever looking at what it learned

**What regression IS:**
- Learning one weight per feature, which you can read back and sanity-check
- A constant negotiation between fitting the data and staying simple
- A model whose complexity you *control on purpose*, with a dial

---

## Concept Block 1: Linear Regression — One Weight Per Feature (10 min)

### Write on the board

```
    y = m1*x1 + m2*x2 + m3*x3 + ... + c

    y = the number we predict     (flat price, in lakh)
    x = a feature                 (area, bedrooms, age...)
    m = a COEFFICIENT -> LEARNED  (the weight of that feature)
    c = the INTERCEPT -> LEARNED  (value when all x are 0)

    "Fitting" = search for the m's and c whose predictions
                sit closest to the real answers.
```

Emphasise the shift from Session 1: they already know `.fit()` / `.predict()`. What is new is that **the model is now readable**. A fitted linear regression is not a black box — it is an equation whose numbers you can interrogate.

### The two things a coefficient tells you

A coefficient carries a **sign** — does this feature push the prediction up or down? — and a **size** — how much does `y` move when this feature goes up by one unit, with everything else held still? Sanity-check the signs out loud with the room; they are the fastest way to catch a broken model.

**The trap to flag now** (it pays off in Concept 3): you **cannot** compare coefficient sizes across features that use different units. A coefficient of `0.046` on square feet and `3.10` on bedrooms does not mean bedrooms matter 67 times more. Square feet run into the thousands; bedrooms run from 1 to 5.

In scikit-learn the learned numbers live in `model.coef_` (an array, one per feature) and `model.intercept_` (a single number).

---

## Practical Block 1: Fit, Read, Predict (15 min)

We build the flats data ourselves from a **known** equation. That is deliberate: it lets us check whether the model recovers the truth.

```python
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# 200 flats from a TRUE equation: 25 + 0.045*area + 3.5*bed - 0.6*age - 1.8*metro + noise
rng = np.random.default_rng(42)
n = 200
area     = rng.uniform(450, 2400, n).round(0)
bedrooms = rng.integers(1, 6, n)
age      = rng.uniform(0, 25, n).round(1)
metro_km = rng.uniform(0.3, 12, n).round(2)
price    = (25 + 0.045*area + 3.5*bedrooms - 0.6*age - 1.8*metro_km
            + rng.normal(0, 6, n)).round(1)          # noise = the real world

flats = pd.DataFrame({"area_sqft": area, "bedrooms": bedrooms,
                      "age_years": age, "metro_km": metro_km,
                      "price_lakh": price})

X = flats.drop(columns="price_lakh")
y = flats["price_lakh"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)

# What did the model LEARN? Compare it against the truth we hid in the data.
print(pd.DataFrame({"learned": model.coef_.round(3),
                    "true":    [0.045, 3.5, -0.6, -1.8]}, index=X.columns))
print("intercept:", round(model.intercept_, 2), " (true: 25)")

print("\nTrain R2:", round(model.score(X_train, y_train), 3))
print("Test  R2:", round(model.score(X_test,  y_test),  3))
```

**Expected output:** the learned coefficients land very close to the true ones — roughly `+0.046` vs `0.045`, `+3.10` vs `3.5`, `-0.66` vs `-0.6`, `-1.64` vs `-1.8`, intercept ≈ `24.5` vs `25`. Train R² ≈ 0.95, test R² ≈ 0.93.

Then predict for a new flat:

```python
new_flat = pd.DataFrame([{"area_sqft": 1200, "bedrooms": 2,
                          "age_years": 5, "metro_km": 1.5}])
print("Predicted price:", round(model.predict(new_flat)[0], 1), "lakh")
```

**Live walk-through:** Put the learned-vs-true table on screen and let it land — *"we hid the equation in the data, and the model found it."* Call out that `age_years` and `metro_km` came back **negative**, exactly as common sense demands: older flats and flats far from a metro are cheaper. Then ask the room: *"The coefficient on bedrooms is 3.10 and on area is 0.046. Does that mean bedrooms matter 67 times more than area?"* Let them argue. The answer is no — and the reason (units) is the seed of Concept 3.

---

## Concept Block 2: Polynomial Regression — Flexibility Invites Overfitting (10 min)

### The idea, on the board

```
  A straight line can't fit a curve. So give the model curved COLUMNS.

  PolynomialFeatures(degree=2)  on  [x]  ->  [x, x^2]
  PolynomialFeatures(degree=3)  on  [x]  ->  [x, x^2, x^3]

  The MODEL is still LinearRegression: y = m1*x1 + m2*x2 + c.
  We just handed it new columns to weight.
```

This is the key mental unlock: **polynomial regression is not a new algorithm.** It is linear regression fed engineered columns. The line is still straight — in a higher-dimensional space we cannot draw.

### Degree is a complexity dial

| Degree | Shape it can draw | Typical failure |
|---|---|---|
| 1 | Straight line | **Underfits** — too rigid to catch a real curve |
| 2–3 | Gentle curve | Usually about right |
| 10+ | Wild, wiggly curve | **Overfits** — memorises noise, dies on new data |

Connect explicitly back to Session 2: this is the bias–variance trade-off, now with a knob they can turn. The tell is always the same — **training score climbing while test score falls.**

---

## Practical Block 2: Degrees 1, 2, 5, 15 (15 min)

```python
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline

# A genuinely curved relationship, with noise
rs = np.random.RandomState(42)
X_c = np.sort(rs.uniform(0, 5, 30)).reshape(-1, 1)
y_c = 2 + 1.5*X_c.ravel() - 0.4*X_c.ravel()**2 + rs.normal(0, 0.6, 30)

Xc_tr, Xc_te, yc_tr, yc_te = train_test_split(
    X_c, y_c, test_size=0.3, random_state=42)

print(f"{'degree':>6} {'terms':>6} {'train R2':>9} {'test R2':>14}")
for degree in [1, 2, 5, 15]:
    model = make_pipeline(PolynomialFeatures(degree=degree),
                          LinearRegression())
    model.fit(Xc_tr, yc_tr)
    n_terms = model[0].fit_transform(Xc_tr).shape[1]
    print(f"{degree:6d} {n_terms:6d} "
          f"{model.score(Xc_tr, yc_tr):9.3f} "
          f"{model.score(Xc_te, yc_te):14.3f}")
```

**Expected output:** degree 1 underfits (train ≈ 0.15). Degree 2 is the sweet spot — train and test both land near 0.68, and they *agree*. Degree 5 is slightly worse on test. Degree 15 pushes train up to ≈ 0.84 while test collapses to a huge negative number in the millions.

Now show them the curves, because the numbers alone do not convey the wiggle:

```python
import matplotlib.pyplot as plt

grid = np.linspace(0, 5, 300).reshape(-1, 1)
fig, axes = plt.subplots(1, 3, figsize=(15, 4), sharey=True)

for ax, degree in zip(axes, [1, 2, 15]):
    m = make_pipeline(PolynomialFeatures(degree=degree), LinearRegression())
    m.fit(Xc_tr, yc_tr)
    ax.scatter(Xc_tr, yc_tr, color="steelblue", label="train")
    ax.scatter(Xc_te, yc_te, color="coral", marker="^", label="test")
    ax.plot(grid, m.predict(grid), color="black", lw=2)
    ax.set_title(f"degree {degree}  |  test R2 = {m.score(Xc_te, yc_te):.2f}")
    ax.set_ylim(-4, 6)
    ax.legend()

plt.tight_layout()
plt.show()
```

**Live walk-through:** The degree-15 panel is the money shot — the curve lunges violently between training points in order to pass through every one of them, and rockets straight off the top and bottom of the axes. (The `ylim` is clamped deliberately; without it the wild curve would squash every other panel flat.) Drive the point home with the real numbers: *"Every actual y value in this data sits between 0.4 and 4. This curve swings from about minus 3,800 to plus 26,000. It isn't learning the pattern — it's contorting itself to touch the dots."* Then run `m[-1].coef_` and show that its largest coefficient is in the **thousands**, while the degree-2 model's are single digits. Pose the bridge question: *"We got here by letting coefficients grow as large as they liked. What if largeness had a cost?"*

---

## BREAK (10 min)

*Mull this over: the degree-15 model's coefficients run into the thousands. The degree-2 model's are single digits. If we simply made large coefficients "expensive", which model would survive?*

---

## Concept Block 3: Regularisation — A Penalty for Large Coefficients (10 min)

### The one equation that matters (board)

```
  Plain regression minimises:  prediction error

  Regularised regression minimises:
      prediction error   +   alpha * (penalty on coefficient size)
      "fit the data"             "stay simple"

  Ridge (L2):  penalty = sum of  m^2   -> shrinks all coefficients toward 0
  Lasso (L1):  penalty = sum of |m|    -> can push coefficients EXACTLY to 0
  ElasticNet:  a blend of both
```

A coefficient now has to *earn* its size. That single change is what tames the wiggle.

| Model | Penalty | Effect on coefficients | Use when |
|---|---|---|---|
| **Ridge** | Squared, `sum(m²)` | Shrinks all toward zero, never *to* zero | Most features carry some signal |
| **Lasso** | Absolute, `sum(abs(m))` | Zeroes some out → **feature selection** | You suspect useless features |
| **ElasticNet** | Mix of both | Shrinks and can zero out | You want a middle ground |

### Why you MUST scale first

The penalty punishes *numerically large* coefficients. But a coefficient is only large or small because of the feature's **units**. `area_sqft` runs to 2000+, so its coefficient is naturally tiny (0.046) — and a tiny coefficient is nearly free under the penalty. `bedrooms` runs 1–5, so its coefficient is naturally larger (3.10) — and gets hammered.

**The penalty ends up punishing features for their units, not for their uselessness.** `StandardScaler` puts every feature on a common ruler first, so the penalty judges them fairly. Practical 3 proves this with numbers.

---

## Practical Block 3: Scaling, then Ridge vs Lasso vs ElasticNet (15 min)

### Part A — Prove that scaling matters (use the flats data from Practical 1)

```python
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge

ALPHA = 10_000    # deliberately strong, to make the effect visible

# --- Ridge on RAW, unscaled features ---
ols_raw   = LinearRegression().fit(X_train, y_train)
ridge_raw = Ridge(alpha=ALPHA).fit(X_train, y_train)
pct_raw   = 100 * np.abs(ridge_raw.coef_) / np.abs(ols_raw.coef_)

# --- Ridge on SCALED features ---
scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)   # fit on TRAIN only
X_test_s  = scaler.transform(X_test)        # never fit on test

ols_s   = LinearRegression().fit(X_train_s, y_train)
ridge_s = Ridge(alpha=ALPHA).fit(X_train_s, y_train)
pct_s   = 100 * np.abs(ridge_s.coef_) / np.abs(ols_s.coef_)

print(pd.DataFrame({
    "typical value":   [X_train[c].mean().round(1) for c in X.columns],
    "RAW % of coef kept":    pct_raw.round(1),
    "SCALED % of coef kept": pct_s.round(1),
}, index=X.columns).to_string())
```

**Expected output:** on **raw** features the penalty is wildly uneven — `area_sqft` keeps about **99%** of its coefficient while `bedrooms` keeps only about **3%**. On **scaled** features every feature keeps a comparable share (all low single digits, because alpha is huge — but crucially, *comparable*).

**Live walk-through:** This is the most important table of the session. *"Ridge nearly deleted `bedrooms` and barely touched `area`. Did it decide bedrooms don't affect price? No — it decided bedrooms had a numerically bigger coefficient, and punished it for that. It punished a feature for its units."* Stress that the fix is one line: scale first. Also flag the discipline they learnt in Session 2 — `fit_transform` on train, `transform` on test. Fitting the scaler on test data is leakage.

### Part B — Ridge vs Lasso vs ElasticNet on a real dataset

```python
from sklearn.datasets import load_diabetes
from sklearn.linear_model import Lasso, ElasticNet

dia = load_diabetes(as_frame=True)
Xd, yd = dia.data, dia.target      # 10 features, predict disease progression

Xd_tr, Xd_te, yd_tr, yd_te = train_test_split(
    Xd, yd, test_size=0.2, random_state=42)

sc = StandardScaler()
Xd_tr_s = sc.fit_transform(Xd_tr)
Xd_te_s = sc.transform(Xd_te)

models = {
    "LinearRegression": LinearRegression(),
    "Ridge(alpha=1)":   Ridge(alpha=1.0),
    "Lasso(alpha=1)":   Lasso(alpha=1.0),
    "ElasticNet(a=1)":  ElasticNet(alpha=1.0, l1_ratio=0.5),
}

coefs = pd.DataFrame(index=Xd.columns)
for name, m in models.items():
    m.fit(Xd_tr_s, yd_tr)
    coefs[name] = m.coef_.round(1)
    zeros = int((np.abs(m.coef_) < 1e-8).sum())
    print(f"{name:18s} train R2 {m.score(Xd_tr_s, yd_tr):.3f} | "
          f"test R2 {m.score(Xd_te_s, yd_te):.3f} | zeroed {zeros}")

print("\n" + coefs.to_string())
```

**Expected output:** all four land in a similar test-score range (roughly 0.45–0.47), but the *coefficients* tell the story. Plain regression puts a large weight (about `-44`) on `s1`; Ridge pulls that in to roughly `-35`; Lasso pulls it all the way to about `-8` and **zeroes out `s2` entirely**.

**Live walk-through:** Point at the `s2` row. *"Lasso set that to exactly zero. That feature is now gone from the model — Lasso did feature selection for you, without being asked."* Then note the honest result: test scores barely moved here. Say so out loud — regularisation is insurance against overfitting, and this dataset was not badly overfitting to begin with. Its payoff is largest exactly where Practical 2 hurt: many features, high flexibility, little data.

---

## Concept Block 4: Alpha — The Bias–Variance Dial (10 min)

### Write on the board

```
   alpha = 0     -> no penalty       -> plain LinearRegression
   alpha small   -> coefficients big -> risk: OVERFIT  (high variance)
   alpha "right" -> best test score
   alpha huge    -> coefficients ~0  -> risk: UNDERFIT (high bias)

   As alpha increases:  bias UP,  variance DOWN.
   Train score only ever falls.  Test score RISES, peaks, then falls.
   -> that peak is the alpha you want.
```

### How to choose alpha — and how NOT to

**Never** try alphas against the test set and keep the winner. That is how the test set stops being a fair estimate of new data — the leakage trap from Session 2.

Instead use **cross-validation** on the training data. scikit-learn wraps the whole loop for you:

- `RidgeCV(alphas=[...], cv=5)` — tries every alpha across 5 folds, keeps the best
- `LassoCV(alphas=[...], cv=5)` — same, for Lasso

After fitting, the chosen value sits in `.alpha_`. The test set stays sealed until the very end.

---

## Practical Block 4: Shrinkage + Cross-Validated Alpha (10 min)

```python
from sklearn.linear_model import RidgeCV, LassoCV

# --- Watch the coefficients shrink as alpha grows ---
rows = []
for a in [0.01, 0.1, 1, 10, 100, 1000]:
    r = Ridge(alpha=a).fit(Xd_tr_s, yd_tr)
    rows.append({"alpha": a,
                 "sum |coef|":     round(float(np.abs(r.coef_).sum()), 1),
                 "biggest |coef|": round(float(np.abs(r.coef_).max()), 1),
                 "train R2":       round(r.score(Xd_tr_s, yd_tr), 3),
                 "test R2":        round(r.score(Xd_te_s, yd_te), 3)})
print(pd.DataFrame(rows).to_string(index=False), "\n")

# --- Watch Lasso DROP features as alpha grows ---
for a in [0.01, 0.1, 1, 5, 10]:
    l = Lasso(alpha=a, max_iter=10_000).fit(Xd_tr_s, yd_tr)
    kept = int((np.abs(l.coef_) > 1e-8).sum())
    print(f"alpha={a:6.2f} | features kept: {kept:2d} / {Xd.shape[1]} "
          f"| test R2 {l.score(Xd_te_s, yd_te):.3f}")
```

**Expected output:** `sum |coef|` falls steadily and dramatically — from roughly 183 at alpha 0.01 down to about 41 at alpha 1000. Train R² slips gently at first, then falls off a cliff at alpha 1000 (≈ 0.36) — that is underfitting arriving. Meanwhile Lasso keeps all 10 features at small alpha and progressively drops them; by alpha 10 only about 4 survive.

```python
# --- Let cross-validation pick alpha for us (test set untouched) ---
ridge_cv = RidgeCV(alphas=np.logspace(-3, 3, 100), cv=5).fit(Xd_tr_s, yd_tr)
lasso_cv = LassoCV(alphas=np.logspace(-3, 1, 100), cv=5,
                   random_state=42, max_iter=10_000).fit(Xd_tr_s, yd_tr)

print("RidgeCV chose alpha =", round(float(ridge_cv.alpha_), 3),
      "| test R2:", round(ridge_cv.score(Xd_te_s, yd_te), 3))
print("LassoCV chose alpha =", round(float(lasso_cv.alpha_), 3),
      "| test R2:", round(lasso_cv.score(Xd_te_s, yd_te), 3))

kept    = [f for f, c in zip(Xd.columns, lasso_cv.coef_) if abs(c) > 1e-8]
dropped = [f for f, c in zip(Xd.columns, lasso_cv.coef_) if abs(c) <= 1e-8]
print("Lasso kept   :", kept)
print("Lasso dropped:", dropped)
```

**Expected output:** `RidgeCV` settles on a fairly strong alpha (around 40) and `LassoCV` on a small one (around 1.5). Both edge out the unregularised model on test. LassoCV drops roughly three of the ten features.

**Live walk-through:** *"We never once looked at the test set to choose alpha — cross-validation did it all inside the training data. That is the whole discipline of Session 2, now doing real work for us."* Close on the Lasso output: *"The model just handed you a shortlist of which measurements actually matter. That is a finding you can take to a doctor."*

---

## Summary & Wrap-Up (5 min)

1. **Linear regression** learns `y = m1*x1 + ... + c` — one coefficient per feature, plus an intercept. Read them; they are what the model learned.
2. Coefficient **signs** must pass a common-sense check. Coefficient **sizes** cannot be compared across different units.
3. **Polynomial features** let a linear model draw curves. Raise the degree far enough and it will memorise noise — train score up, test score off a cliff.
4. **Regularisation** adds `alpha * penalty on coefficient size` to the goal. **Ridge** shrinks; **Lasso** shrinks *and zeroes out* (free feature selection); **ElasticNet** blends the two.
5. **Always `StandardScaler` before a penalised model** — otherwise the penalty punishes features for their units rather than their uselessness.
6. **Alpha** trades bias for variance. Pick it with **cross-validation** (`RidgeCV` / `LassoCV`), never against the test set.

**Bridge:** *"Every score today was R² — one number, hiding a lot. Next session, **Evaluating Regression Performance**, we open it up: how far off is a typical prediction, in rupees? Are we wrong by a little on everything, or badly wrong on a few? R² will never satisfy you again."*

---

## Q&A & Doubt Solving (5 min)

**Q: If Lasso does feature selection for me, why would I ever use Ridge?**
→ When your features are correlated, Lasso tends to pick one of a correlated group essentially at random and zero the rest — which looks decisive but is unstable, and can flip if you reshuffle the data. Ridge keeps them all and shares the weight between them. Use Lasso when you genuinely believe some features are useless; use Ridge when you think most carry a bit of signal.

**Q: Why does scaling not change plain `LinearRegression`'s predictions, but does change Ridge's?**
→ Plain regression has no penalty, so it just rescales the coefficient to compensate for the unit — halve a feature's values and it doubles the coefficient, predictions unchanged. Ridge *does* have a penalty, and that penalty is computed on the coefficient's numeric size. Change the units, change the coefficient's size, change how hard it gets penalised. The penalty is what makes units suddenly matter.

**Q: My R² is negative. Is that a bug?**
→ No. R² compares your model to the trivial baseline of always predicting the mean. Zero means you tied that baseline; negative means you did *worse* than it. A wildly overfitted model can be arbitrarily bad on new data, so R² has no lower bound. Session 4 unpacks this properly.

**Q: What alpha should I start with, and do I still need polynomial features?**
→ Never guess a single alpha — search a wide range on a *log* scale, like `np.logspace(-3, 3, 100)`, and let `RidgeCV` / `LassoCV` choose; the interesting difference is between 0.01 and 1, not between 500 and 501. As for `PolynomialFeatures`: reach for it only when you have few features and see genuine curvature. It explodes combinatorially — 10 features at degree 2 becomes 65 columns, at degree 3 becomes 285 — so with many features it is a fast route straight back to overfitting.

---

## Instructor Notes

- **No downloads needed.** Practicals 1–2 generate data inline with a seed; Practicals 3–4 use `load_diabetes`, which ships with scikit-learn. Only `scikit-learn`, `numpy`, `pandas`, `matplotlib` are required — all already installed from Sessions 1–2.
- **Be honest about the diabetes results.** Two traps here. Its features arrive *already* mean-centred and scaled, so `StandardScaler` is nearly a no-op on it — keep it in the code as correct habit, but do not claim it rescued the score. And regularisation only nudges the test score (≈0.45 → ≈0.47). That is the truthful result: regularisation is *insurance*, and this dataset was not badly overfitting. Its real payoff was Practical 2 and Lasso's interpretability. Overclaiming here is the fastest way to lose a sceptical room; if a sharp student catches either point, reward them.
- **Two numbers are deliberately extreme.** `ALPHA = 10_000` in Practical 3A — at a realistic alpha the unfairness is real but too small to see on screen, so say out loud you have turned the dial to eleven to expose the mechanism. And the degree-15 test R² is a wildly ill-conditioned fit: the exact figure may differ on your machine or scikit-learn version. Never mind the digits — the only claim is that it is catastrophically negative.
- **Pacing:** Practical 2's plot is the emotional centre of the session — protect its time. If you are running late, compress Practical 3 Part B to just the printed coefficient table and skip discussing ElasticNet in depth.
- **Keep metrics out of it.** Use `.score()` and say "R²" without dissecting it. RMSE, MAE and residual plots belong to Session 4; introducing them here will crowd out regularisation, which is the actual objective.
- **The single most common student mistake:** applying `StandardScaler` to the *whole* dataset before `train_test_split`. It runs fine, gives slightly better scores, and is leakage — the scaler has seen the test set's mean. Pre-empt it by writing `fit_transform(X_train)` / `transform(X_test)` on the board and asking the room *why* it is not `fit_transform` twice.
