# Lecture Script: Evaluating Regression Performance
> **Instructor Reference** — Module 2: Classical ML | Session 4 | Duration: 2 Hours

---

## Session Overview

**Goal:** Students take a fitted regression model and produce a complete, defensible evaluation of it — residuals computed by hand and with `sklearn.metrics`, a four-metric report card, three diagnostic plots, a `DummyRegressor` baseline to compare against, and a train-vs-test table that lets them *name* overfitting out loud.

**Student profile at this point:** They have completed Session 1 (the ML workflow, `train_test_split`), Session 2 (overfitting, underfitting, generalisation) and Session 3 (`LinearRegression`, Ridge, Lasso). They can fit a model and call `.predict()`. What they cannot yet do is answer the question *"is this model any good?"* with anything more rigorous than a vibe. That is today's entire job.

**Key outcome:** A reusable `evaluate(model, X_train, X_test, y_train, y_test)` function that prints a metric report card against a baseline, plus the three diagnostic plots — a notebook they will paste into every regression project for the rest of the course.

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| Opening — Two models, one number, wrong answer | 5 min | 0:05 |
| **Concept 1:** The residual — the atom of every metric | 10 min | 0:15 |
| **Practical 1:** Residuals by hand, then with sklearn | 15 min | 0:30 |
| **Concept 2:** MAE vs MSE vs RMSE vs R² — when to use which | 10 min | 0:40 |
| **Practical 2:** Build the metric report card | 15 min | 0:55 |
| **BREAK** | 10 min | 1:05 |
| **Concept 3:** Diagnosis by plotting — errors have a shape | 10 min | 1:15 |
| **Practical 3:** The three diagnostic plots, healthy vs broken | 15 min | 1:30 |
| **Concept 4:** The baseline and the train–test gap | 10 min | 1:40 |
| **Practical 4:** DummyRegressor + naming overfitting | 10 min | 1:50 |
| Summary & Wrap-Up | 5 min | 1:55 |
| Q&A & Doubt Solving | 5 min | 2:00 |

---

## Opening (5 min)

**Hook — run this live before you say anything.** Put two lines on the screen:

```
Model A:  R² = 0.91
Model B:  R² = 0.91
```

*"Identical scores. One of these models is production-ready. The other is dangerously broken — it under-predicts every single expensive flat by ₹30 lakh, and it will lose the company money on exactly the deals that matter. The R² cannot tell them apart. Nothing in a single number can. So what do we do?"*

Let that hang. Then flip to a slide with two residual plots side by side — one a shapeless cloud, one a clean curve. *"This is what the number was hiding."*

**What model evaluation is NOT:**
- Printing `r2_score` and moving on
- Reporting a metric from the training set
- Comparing a score to a number you feel is "good", like 0.8
- Assuming a high score means the model is correct everywhere

**What model evaluation IS:**
- Building every metric from the same atom — the residual
- Choosing a metric because of what it *punishes*, not because it is famous
- Comparing your score against a deliberately stupid baseline
- Looking at the *picture* of your errors to find the structure you missed

---

## Concept Block 1: The Residual — The Atom of Every Metric (10 min)

### Write on the board, and leave it there all session

```
residual  =  y_true  -  y_pred

    positive residual  →  truth was HIGHER  →  we UNDER-predicted
    negative residual  →  truth was LOWER   →  we OVER-predicted
```

**Say it plainly:** one residual per row. Eighty test flats, eighty residuals. Every metric in `sklearn.metrics` is a rule for squashing those eighty numbers into one. There is no magic anywhere in this session — only different ways of adding up the same list.

### The first question to ask the room

*"Why can't we just take the mean of the residuals?"*

Let them fight it out for thirty seconds, then show why. Put this on the board:

```
Flat 1:  actual 120,  predicted 100   →  residual = +20
Flat 2:  actual 100,  predicted 120   →  residual = -20
                                   mean residual =   0
```

A model that is ₹20 lakh too high on one flat and ₹20 lakh too low on the next scores a *perfect zero*. It is a disaster of a model. **The signs cancel.**

### The two escape routes

| Route | Operation | Metric it leads to | Personality |
|---|---|---|---|
| Absolute value | `abs(residual)` | MAE | Democratic — every rupee of error counts once |
| Squaring | `residual ** 2` | MSE, RMSE | Dramatic — one huge miss drowns out ten small ones |

Everything else today is a consequence of this one fork in the road. Make them see that MAE and RMSE are not "two metrics you should memorise" — they are **two different opinions about how much a catastrophe should hurt.**

---

## Practical Block 1: Residuals by Hand, Then with sklearn (15 min)

We build a synthetic Bengaluru flat dataset so nothing depends on a download and the units are ₹ lakh — readable, and a residual of "7" means something you can say out loud.

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

def make_flats(n=400, seed=42):
    """Synthetic Bengaluru flats. Price in ₹ lakh."""
    rng = np.random.default_rng(seed)
    area     = rng.uniform(500, 2500, n)     # sq ft
    bedrooms = rng.integers(1, 5, n)
    age      = rng.uniform(0, 30, n)         # years
    metro_km = rng.uniform(0.2, 12, n)       # km to nearest metro
    noise    = rng.normal(0, 8, n)           # the part nobody can predict
    price = 30 + 0.04*area + 4*bedrooms - 0.5*age - 1.5*metro_km + noise
    return pd.DataFrame({
        "area_sqft": area.round(0),
        "bedrooms": bedrooms,
        "age_years": age.round(1),
        "metro_km": metro_km.round(2),
        "price_lakh": price.round(1),
    })

flats = make_flats()
X = flats.drop(columns="price_lakh")
y = flats["price_lakh"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = LinearRegression().fit(X_train, y_train)
y_pred = model.predict(X_test)

# THE ATOM. Everything today is built from this one line.
residuals = y_test - y_pred

print(pd.DataFrame({
    "actual":   y_test.values[:5].round(1),
    "predicted": y_pred[:5].round(1),
    "residual":  residuals.values[:5].round(1),
}))
print("\nMean residual:", round(residuals.mean(), 3))
```

**Expected output:** five rows showing actual, predicted and residual side by side — a mix of positive and negative residuals, most within about ±12 lakh. The mean residual prints as a number very close to zero.

**Live walk-through:** Point at a row with a *negative* residual and say it out loud: *"This flat sold for ₹67 lakh. We said ₹80 lakh. We over-predicted by ₹13 lakh. If a bank had lent against our number, they would be under-collateralised."* Give the error a consequence — that is what makes it stick.

Then point at the mean residual, which is essentially zero, and ask: **"So — is this a perfect model?"** Someone will say yes. That is the trap from Concept 1 springing shut, and it is the best possible moment to move to metrics. Have them run:

```python
print("Largest over-prediction:", round(residuals.min(), 1), "lakh")
print("Largest under-prediction:", round(residuals.max(), 1), "lakh")
```

*"The mean said zero. The extremes say ±20. Which of those two facts would you want before deploying?"*

---

## Concept Block 2: MAE vs MSE vs RMSE vs R² (10 min)

### Board content — the four metrics, one list of residuals

```
MAE   = mean( |y_true - y_pred| )        →  average miss, in ₹ lakh
MSE   = mean( (y_true - y_pred)² )       →  average squared miss, in lakh²  ← unreadable
RMSE  = sqrt(MSE)                        →  back in ₹ lakh, but still punishes big misses
R²    = 1 - (your error / mean-guess error)  →  no units; how much better than dumb
```

### The "when to use which" table — the single most important table of the session

| Metric | Units | What it punishes | Reach for it when | Do not use when |
|---|---|---|---|---|
| **MAE** | Same as target (₹ lakh) | Every rupee equally | You have outliers you don't want dominating the score | A single huge miss is genuinely catastrophic |
| **MSE** | Target **squared** | Big misses, hard | Optimising *inside* code (it is what the model minimises) | Reporting to a human — the units are nonsense |
| **RMSE** | Same as target (₹ lakh) | Big misses, hard | One terrible prediction is much worse than five mediocre ones | Your data has a few known, harmless outliers |
| **R²** | None (a fraction) | Nothing directly | Comparing across datasets; explaining "how much signal" | Alone — it hides the *size* of the error |

### Two facts to hammer

**1. RMSE ≥ MAE. Always.** It is a mathematical guarantee. So the *gap between them is a diagnostic in itself*:

```
RMSE ≈ MAE        →  errors are all roughly the same size. Boring. Healthy.
RMSE >> MAE       →  a few catastrophic predictions are hiding in there. GO FIND THEM.
```

**2. R² can be negative.** Write it on the board and underline it, because half the room believes otherwise. `R² = 0` means you exactly matched a model that ignores every feature and always predicts the mean. `R² < 0` means you did **worse than that**. On the training set that is impossible for a linear model. On the **test set** it is not only possible, it is common — and it is the single loudest alarm bell for overfitting you will meet in this module. We will make one happen in Practical 4.

**MAPE — mention it, warn about it (2 min):**

```
MAPE = mean( |(y_true - y_pred) / y_true| ) * 100
```

Stakeholders love it: *"we're 9% off"* needs no explanation. But it **divides by `y_true`**. One row where the truth is zero — a kirana store closed on Sunday, zero rainfall in a dry month — and your MAPE is `inf`. Even a truth of *1* produces a percentage error in the hundreds. Use it only when the target is comfortably above zero.

---

## Practical Block 2: Build the Metric Report Card (15 min)

```python
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

mae  = mean_absolute_error(y_test, y_pred)
mse  = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)                          # works on every sklearn version
r2   = r2_score(y_test, y_pred)

print(f"MAE  : {mae:.2f} lakh   <- typical miss")
print(f"MSE  : {mse:.2f} lakh²  <- unreadable, but it's what the model minimises")
print(f"RMSE : {rmse:.2f} lakh   <- typical miss, big errors weighted heavier")
print(f"R²   : {r2:.3f}         <- fraction of price variation explained")
```

**Expected output:** MAE lands around 7 lakh, RMSE a little above it (around 8), and R² comes in around 0.90. Do not promise exact digits — have them read their own numbers off the screen.

**Live walk-through — three things to call out, in this order:**

1. **Say the MAE as an English sentence.** *"On a typical Bengaluru flat, we are about ₹7 lakh off."* Then ask: **"Is that good?"** They cannot answer. Nobody can, yet. Plant that flag — Concept 4 pays it off.
2. **Compare RMSE to MAE.** RMSE is only slightly larger here, so the errors are fairly uniform — no hidden catastrophes. On a messier dataset that gap would yawn open, and the gap is free information.
3. **Read the MSE aloud, with units.** *"Seventy-one point six lakh-squared."* Wait for the laugh. That is the entire argument for RMSE, delivered in three seconds.

Now show them how the *choice of metric picks a different winner*, by poisoning one prediction:

```python
# What if ONE prediction is catastrophically wrong?
y_pred_bad = y_pred.copy()
y_pred_bad[0] = y_pred_bad[0] + 100      # one flat, off by ₹1 crore

print("           MAE     RMSE")
print(f"clean  : {mean_absolute_error(y_test, y_pred):6.2f}  {np.sqrt(mean_squared_error(y_test, y_pred)):6.2f}")
print(f"poison : {mean_absolute_error(y_test, y_pred_bad):6.2f}  {np.sqrt(mean_squared_error(y_test, y_pred_bad)):6.2f}")
```

**Expected output:** MAE creeps up modestly. RMSE jumps sharply. **Ask the room: *"One bad flat out of eighty. Which metric noticed?"*** This is the whole MAE-vs-RMSE lesson in one printout — and it is the moment students stop treating metric choice as trivia.

And the MAPE landmine, in three lines:

```python
y_true_z = np.array([0.0, 10.0, 20.0])   # a shop closed on Sunday
y_pred_z = np.array([2.0, 11.0, 19.0])
print("MAPE:", np.mean(np.abs((y_true_z - y_pred_z) / y_true_z)) * 100)
```

**Expected output:** `inf` (with a divide-by-zero RuntimeWarning). *"Your dashboard now says the model is infinitely wrong. Your manager is calling."*

---

## BREAK (10 min)

*Leave this on the screen: our R² is about 0.90. Is that good? Good compared to **what**? Nobody has told you what a bad model would have scored. Come back and we will build one on purpose.*

---

## Concept Block 3: Diagnosis by Plotting — Errors Have a Shape (10 min)

### The pitch

A metric compresses eighty residuals into one number. Compression **destroys information** — and the information it destroys is exactly the information you need to *fix* the model. `RMSE = 8.4` tells you *that* you are wrong. It cannot tell you *where*, or *why*.

So: plot the errors. This is Module 1's EDA instinct, pointed at the residuals instead of the raw data.

### The three plots — write this table on the board

| Plot | x-axis | y-axis | Healthy looks like |
|---|---|---|---|
| **Predicted vs Actual** | `y_pred` | `y_test` | Points hug the 45° diagonal |
| **Residual plot** | `y_pred` | `residual` | A shapeless cloud around zero |
| **Residual histogram** | `residual` | count | One bell, centred on zero |

### Reading the residual plot — the four shapes

```
RANDOM CLOUD    →  Healthy. Whatever is left is noise, and noise cannot be learnt.
                   This is the goal. Stop here.

CURVE / SMILE   →  Positive at both ends, negative in the middle (or the reverse).
                   Your straight line is being forced onto a bent relationship.
                   FIX: a better feature (area², log), not a better metric.

FUNNEL          →  Errors tiny for cheap flats, huge for expensive ones.
                   Error scales with the target.
                   FIX: predict log(price) instead of price.

CLOUD OFF ZERO  →  Consistently biased. Every prediction leans one way.
                   FIX: check for a missing feature or a broken preprocessing step.
```

**The sentence to leave them with:** *A metric tells you how much you are wrong. A residual plot tells you why.* If a residual plot has a **shape**, there is signal your model failed to eat — and no amount of switching from Ridge to Lasso will help you, because the problem is the *features*, not the *regularisation*.

---

## Practical Block 3: The Three Diagnostic Plots (15 min)

**Part A — the healthy model.** Wrap it in a function they will keep forever.

```python
def diagnose(y_true, y_pred, title=""):
    """The three plots every regression model must pass."""
    resid = y_true - y_pred
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))

    # 1. Predicted vs Actual — do we hug the diagonal?
    axes[0].scatter(y_pred, y_true, alpha=0.5, color="steelblue")
    lo, hi = min(y_true.min(), y_pred.min()), max(y_true.max(), y_pred.max())
    axes[0].plot([lo, hi], [lo, hi], "r--", lw=2, label="perfect prediction")
    axes[0].set_xlabel("Predicted (₹ lakh)")
    axes[0].set_ylabel("Actual (₹ lakh)")
    axes[0].set_title("Predicted vs Actual")
    axes[0].legend()

    # 2. Residual plot — is it a shapeless cloud?
    axes[1].scatter(y_pred, resid, alpha=0.5, color="darkorange")
    axes[1].axhline(0, color="red", lw=2, linestyle="--")
    axes[1].set_xlabel("Predicted (₹ lakh)")
    axes[1].set_ylabel("Residual (₹ lakh)")
    axes[1].set_title("Residual plot — want NO pattern")

    # 3. Residual histogram — one bell, centred on zero?
    axes[2].hist(resid, bins=25, color="seagreen", edgecolor="white")
    axes[2].axvline(0, color="red", lw=2, linestyle="--")
    axes[2].set_xlabel("Residual (₹ lakh)")
    axes[2].set_ylabel("Count")
    axes[2].set_title("Residual distribution")

    plt.suptitle(title, fontsize=13)
    plt.tight_layout()
    plt.show()

diagnose(y_test, y_pred, "HEALTHY MODEL — Bengaluru flats")
```

**Expected output:** three panels. Points cluster tightly along the red diagonal; the residual plot is a formless orange cloud with no drift; the histogram is a single bell centred on zero.

**Part B — now break it on purpose.** This is the part they will remember.

```python
def make_curved_flats(n=400, seed=7):
    """Luxury premium: price grows with area SQUARED, not linearly."""
    rng = np.random.default_rng(seed)
    area = rng.uniform(500, 2500, n)
    price = 20 + 0.00003 * (area ** 2) + rng.normal(0, 6, n)
    return pd.DataFrame({"area_sqft": area.round(0), "price_lakh": price.round(1)})

curved = make_curved_flats()
Xc, yc = curved[["area_sqft"]], curved["price_lakh"]

# Fit a STRAIGHT line to a BENT relationship
bad_model = LinearRegression().fit(Xc, yc)
yc_pred = bad_model.predict(Xc)

print("R² of the bad model:", round(r2_score(yc, yc_pred), 3))
diagnose(yc, yc_pred, "BROKEN MODEL — a straight line on a curved truth")
```

**Expected output:** the R² prints as a *high* number — comfortably above 0.9. But the residual plot is unmistakably curved: residuals are **positive at both ends and negative in the middle** — a clear smile.

**Live walk-through — this is the money moment of the session.** Put the R² and the residual plot on screen together and ask:

> *"The R² is above 0.95. By this morning's standards, we ship it. Now look at the residual plot. Would you ship it?"*

Then land it: *"This model systematically under-prices small flats, over-prices mid-size ones, and under-prices the big ones. It is wrong in a predictable, exploitable, expensive way — and the R² was **delighted**. The metric could not see the shape. Your eyes can."*

Ask for the fix. Steer them away from "use Ridge" and towards **"add an `area²` feature"** — the problem is a missing ingredient, not too much complexity.

---

## Concept Block 4: The Baseline and the Train–Test Gap (10 min)

### Part 1 — Every metric is meaningless without a baseline

Ask the room: *"My model has an RMSE of 8.46. Good?"* They will guess. Stop them. **They cannot know, and neither can you.** A number in isolation is not information — it becomes information only next to a comparison.

So build the dumbest model that could possibly work:

```
DummyRegressor(strategy="mean")
    → ignores every single feature
    → predicts the training mean for every row
    → this is the FLOOR. Beat it, or your features are decoration.
```

**Then and only then:** *"RMSE 8.46, versus a baseline of 27.5."* ← **Now** you know something.

By construction, the mean-predictor scores **exactly R² = 0** on the data it was fitted on. That is not a coincidence — it is the *definition* of R². R² **is** "how far above the baseline are you, on a 0-to-1 scale."

### Part 2 — Train vs test: naming the failure

Session 2 taught them overfitting as a concept. Today it becomes a number they can read off a table.

| Train score | Test score | Diagnosis | What to do |
|---|---|---|---|
| Good | Good, similar | **Healthy** | Ship it |
| Excellent | Much worse | **Overfitting** | More data, fewer features, or Ridge/Lasso from Session 3 |
| Poor | Poor | **Underfitting** | Better features, more model capacity |
| Poor | Better than train | Fluke or split bug | Check for leakage or a tiny test set |

**The rule, on the board, boxed:**

```
Every metric you REPORT comes from the TEST set.
Training metrics exist only to be COMPARED against test metrics,
so you can name the gap.
```

---

## Practical Block 4: DummyRegressor + Naming Overfitting (10 min)

**Part A — the baseline, on our healthy flats model.**

```python
from sklearn.dummy import DummyRegressor

baseline = DummyRegressor(strategy="mean").fit(X_train, y_train)
base_pred = baseline.predict(X_test)

print("           MAE     RMSE      R²")
print(f"baseline : {mean_absolute_error(y_test, base_pred):6.2f}  "
      f"{np.sqrt(mean_squared_error(y_test, base_pred)):6.2f}  "
      f"{r2_score(y_test, base_pred):7.3f}")
print(f"model    : {mean_absolute_error(y_test, y_pred):6.2f}  "
      f"{np.sqrt(mean_squared_error(y_test, y_pred)):6.2f}  "
      f"{r2_score(y_test, y_pred):7.3f}")
```

**Expected output:** the baseline's MAE and RMSE are roughly **three times** the model's, and its test R² sits at approximately zero — in fact it will print as a *very slightly negative* number.

**Ask that immediately:** *"Why is the baseline's R² a hair below zero and not exactly zero?"* → Because it predicts the **training** mean, but is scored on the **test** set, whose mean is very slightly different. Beautiful, tiny, honest detail — and it proves they now understand what the zero means.

**Part B — make R² go negative, on purpose.**

```python
from sklearn.datasets import make_regression

# 60 rows, 40 features, only 5 of them real. A memorisation trap.
X_of, y_of = make_regression(
    n_samples=60, n_features=40, n_informative=5,
    noise=25.0, random_state=42
)
Xo_tr, Xo_te, yo_tr, yo_te = train_test_split(
    X_of, y_of, test_size=0.4, random_state=42
)

overfit = LinearRegression().fit(Xo_tr, yo_tr)
dummy   = DummyRegressor(strategy="mean").fit(Xo_tr, yo_tr)

print("                   R²        RMSE")
print(f"TRAIN (model)  : {r2_score(yo_tr, overfit.predict(Xo_tr)):7.3f}  "
      f"{np.sqrt(mean_squared_error(yo_tr, overfit.predict(Xo_tr))):8.2f}")
print(f"TEST  (model)  : {r2_score(yo_te, overfit.predict(Xo_te)):7.3f}  "
      f"{np.sqrt(mean_squared_error(yo_te, overfit.predict(Xo_te))):8.2f}")
print(f"TEST  (dummy)  : {r2_score(yo_te, dummy.predict(Xo_te)):7.3f}  "
      f"{np.sqrt(mean_squared_error(yo_te, dummy.predict(Xo_te))):8.2f}")
```

**Expected output:** train R² prints as **1.000** with an RMSE of essentially **0.00** — a flawless fit. Test R² prints as a **large negative number**, and the test RMSE is *several times worse than the dummy's*.

**Live walk-through.** Read the three lines aloud, then say it slowly:

> *"This model is perfect on the data it has seen. On data it has not seen, it is **worse than a model that ignores every feature and guesses the average**. It did not learn housing. It memorised sixty rows."*

Ask: **"What would you do about it?"** They should reach, unprompted, for Session 3's Ridge and Lasso. Let one student say it. That is the whole module clicking into place.

---

## Summary & Wrap-Up (5 min)

**The spine of today, in five steps:**

1. **The residual is the atom.** `y_true - y_pred`, one per row. Every metric is a rule for squashing that list into one number. Nothing more.
2. **Choose your metric by what it punishes.** MAE treats every rupee equally. RMSE hunts catastrophes. MSE is for the machine, not the human. MAPE is for percentage-thinking audiences — and it explodes on zeros.
3. **R² is a comparison, not a percentage.** Zero means you matched a model that ignores your features. **Negative means you lost to it.**
4. **Plot the errors.** Predicted-vs-actual, residual plot, residual histogram. A random cloud is health. A curve or a funnel means your model is missing structure — and *no metric will ever tell you that*.
5. **No score means anything without two comparisons:** against a **`DummyRegressor` baseline**, and between **train and test**.

**The one line to leave on the board:** *A metric tells you how much you are wrong. A residual plot tells you why. A baseline tells you whether you should have bothered.*

**Bridge:** *"You have now spent four sessions treating the model's error function as a black box — something you measure after the fact. Next session, **Master Class: The Mathematics Behind Learning — Lines, Curves & Errors**, we open it. You will see that the MSE you computed today is the very thing the model was climbing down all along, and you will watch it descend."*

---

## Q&A & Doubt Solving (5 min)

**Q: If RMSE and MAE always rank models the same way, why do I need both?**
→ They *don't* always rank them the same way — that is precisely the point. A model with many small errors can beat one with a few enormous errors on MAE while losing on RMSE, because squaring punishes catastrophes disproportionately. When the two disagree about which model is better, that disagreement is telling you something real about your error distribution. Report both; investigate when they differ.

**Q: My test R² is higher than my train R². Is that good news?**
→ Usually a warning, not a prize. Most likely your test set is small and happened to get the easy rows, or your split leaked information. Re-split with a different `random_state` and see if it holds. If it evaporates, it was noise — which is itself the argument for cross-validation over a single split.

**Q: Should I always aim for R² above 0.9?**
→ No. "Good" R² is entirely domain-dependent. Predicting a flat's price from its area? 0.9 is achievable. Predicting tomorrow's stock return? An R² of 0.05 would be extraordinary. This is exactly why the **baseline** matters more than any absolute threshold — it tells you what "good" means *for your problem*, instead of importing a number from someone else's.

**Q: My residual plot has a funnel shape. Which metric should I switch to?**
→ Wrong instinct — and the most common one in this room. A funnel is a **modelling** problem, not a **metric** problem. Switching metrics changes what you *measure*; it does nothing to what the model *does*. Fix the model: try predicting `log(y)` instead of `y`, which turns multiplicative error into additive error and usually flattens the funnel.

**Q: `mean_squared_error(..., squared=False)` gives me an error. Why?**
→ The `squared` parameter was deprecated and then removed in recent scikit-learn versions. Use `np.sqrt(mean_squared_error(y, y_pred))`, which works everywhere, or `root_mean_squared_error` from `sklearn.metrics` on version 1.4+. This lecture uses `np.sqrt` throughout so nothing breaks in your environment.

---

## Instructor Notes

- **No downloads needed.** Every dataset here is generated inline with a fixed seed, so flaky classroom Wi-Fi cannot derail the session. You need only `numpy`, `pandas`, `matplotlib` and `scikit-learn` — all already installed from Sessions 1–3.
- **Do not skip the "poisoned prediction" demo in Practical 2.** Four lines of code, and the only moment where students *feel* the MAE/RMSE difference rather than reading it in a table. If running behind, cut a diagnostic plot instead — never cut this.
- **The `squared=False` trap.** Students copy-pasting RMSE code from old blog posts will hit a `TypeError` on modern scikit-learn. Pre-empt it early: "we always use `np.sqrt(mean_squared_error(...))` in this course."
- **Pacing.** Practical 3 Part B (the curved residual plot) is the intellectual peak of the session — protect its full fifteen minutes. If you must borrow time, take it from Practical 4 Part A; the baseline printout explains quickly even in a rush.
- **The single most common student mistake:** *reporting the training metric.* They fit on `X_train`, absent-mindedly call `model.score(X_train, y_train)`, see 0.95, and celebrate. Pre-empt it in Concept 4 — have everyone write in their notes: **"the number I show anyone comes from `X_test`."** Then in Practical 4, when the overfit model prints train R² = 1.000, ask *"who would have shipped this?"* The point lands far harder as a near-miss than as a warning.
- **A close second:** treating a residual *pattern* as something to fix by changing the metric or the regularisation strength. It cannot be. A shaped residual plot means a missing *feature*. Say this at least twice.
