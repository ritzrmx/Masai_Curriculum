# Lecture Script: Linear Regression
> **Instructor Reference** — Module 2: Classical ML | Session 4 | Duration: 2 Hours

---

## Session Overview

**Goal:** Students train `LinearRegression` in scikit-learn on a real dataset, evaluate it with MAE/RMSE/R², interpret coefficients in business terms, and diagnose overfitting via train vs. test comparison.

**Student profile at this point:** Understands the math intuition (line equation, residuals, gradient descent) from Session 3; comfortable with `Pipeline`/`ColumnTransformer` from Session 2. This is their first time training a "real" scikit-learn model end to end.

**Key outcome:** Every student trains a housing-price regression model on `housing_sample.csv`, reports all three metrics on the held-out TEST set (not train), interprets at least two coefficients in plain business language, and correctly diagnoses whether a given model shows signs of overfitting.

**Dataset for this session:** `housing_sample.csv` (in this folder) — 30 rows of `sqft`, `bedrooms`, `age_years`, `price_lakhs`.

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| SEGMENT 1: Opening — From Theory to sklearn | 10 min | 0:10 |
| SEGMENT 2: Fit/Predict with LinearRegression | 20 min | 0:30 |
| SEGMENT 3: MAE, RMSE, R² Live Comparison | 25 min | 0:55 |
| **BREAK** | 10 min | 1:05 |
| SEGMENT 4: Interpreting Coefficients | 20 min | 1:25 |
| SEGMENT 5: Overfitting Diagnosis | 15 min | 1:40 |
| SEGMENT 6: Lab — Full Workflow on housing_sample.csv | 15 min | 1:55 |
| SEGMENT 7: Summary, Wrap-Up & Q&A | 5 min | 2:00 |

---

## SEGMENT 1: Opening — From Theory to sklearn (10 min)

### The Side-by-Side Reveal (6 min)

**Say:** *"Two sessions ago we hand-wrote a gradient descent loop to learn one slope value, `m`, for a toy dataset with four points. Today we do the real thing: multiple features, a real (small) dataset, and one line of code that does everything our loop did — and more."*

**Live-code this side-by-side comparison on the projector:**

```python
# What we wrote by hand in Session 3 (simplified, one feature):
m = 0.0
learning_rate = 0.01
for step in range(1000):
    predictions = [m * x for x in x_vals]
    errors = [p - y for p, y in zip(predictions, y_vals)]
    gradient = sum(e * x for e, x in zip(errors, x_vals)) / len(x_vals)
    m = m - learning_rate * gradient

# What scikit-learn does today, for many features at once:
from sklearn.linear_model import LinearRegression
model = LinearRegression()
model.fit(X_train, y_train)   # finds ALL coefficients + intercept in one call
```

**Say:** *"`LinearRegression().fit()` isn't magic — for plain linear regression it actually uses a closed-form matrix solution rather than iterating like our loop, exactly as we discussed at the end of Session 3. But conceptually it's solving the EXACT same problem: find the `m` values (now one per feature) and `c` that minimize squared error. Today we stop hand-rolling it and start using the real tool, on a real housing dataset."*

### Setting Expectations for Today (4 min)

**Say:** *"By the end of today you'll be able to do four things with any regression model: train it, generate predictions, evaluate it with three different metrics that each tell you something different, and explain what it learned in plain English to someone who has never heard of a coefficient. That last skill — translation to plain English — is arguably the most valuable one in this entire module, because it's what turns a model from a science project into something a business actually trusts and uses."*

**Learning contract for today — write on board:**

- Fit and predict with `LinearRegression`
- Compute and interpret MAE, RMSE, and R²
- Translate coefficients into plain business sentences
- Diagnose overfitting by comparing train vs. test scores

---

## SEGMENT 2: Fit/Predict with LinearRegression (20 min)

### Loading and Exploring the Data (6 min)

**Say:** *"Let's load `housing_sample.csv`, which sits right in this session's folder, and look at what we're working with before we train anything."*

**Live-code, step by step:**

```python
import pandas as pd

df = pd.read_csv("housing_sample.csv")
print(df.head())
print(df.describe())
```

**Run it and discuss the `describe()` output together.** Point out the range of `sqft` (750-2500), `bedrooms` (2-4), `age_years` (2-22), and `price_lakhs` (38-130).

**Say:** *"Already we can guess `sqft` probably correlates strongly with `price_lakhs` — bigger houses cost more. Let's let the model confirm that quantitatively rather than eyeballing it."*

**Optional quick correlation check:**

```python
print(df.corr(numeric_only=True)["price_lakhs"])
```

**Run it.** **Say:** *"This confirms `sqft` has a strong positive correlation with price — the number closest to 1 in this list. `age_years` should show a negative correlation. This is a nice preview of what our fitted coefficients should roughly agree with in a few minutes."*

### The Split and the Fit (8 min)

**Continue live-coding the split and fit:**

```python
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

X = df[["sqft", "bedrooms", "age_years"]]
y = df["price_lakhs"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)

predictions = model.predict(X_test)
print("Predicted:", predictions)
print("Actual:   ", y_test.values)
```

**Run it and read the two printed arrays side by side.**

**Ask:** *"Looking at these two lists, does the model seem to be doing a reasonable job? Which row looks like the model's biggest miss?"* Let 2-3 students point to specific rows and estimate the gap.

**Say:** *"Right now we're eyeballing 5-6 numbers side by side, which doesn't scale to a real dataset with thousands of rows. We need a single summary number — actually, we need a FEW different ones, because they each tell you something different. That's the next block."*

### Note on This Split (2 min)

**Ask:** *"Notice we did NOT use `stratify=y` here, unlike Session 1's classification example. Why not?"* Guide toward: `stratify` is specifically for preserving class proportions in a categorical target; `price_lakhs` here is a continuous number, not a category, so stratification in that sense doesn't directly apply. A plain random split is the standard default for regression targets.

### Comprehension Check (4 min)

1. *"What does `model.predict(X_test)` return — a single number, or one prediction per row?"* (One prediction per row in `X_test`.)
2. *"If we called `model.predict(X_train)` instead, what would that tell us?"* (Predictions on data the model was TRAINED on — useful for later comparing train vs. test performance, but NOT an honest generalization check on its own.)

---

## SEGMENT 3: MAE, RMSE, R² Live Comparison (25 min)

### Computing All Three (8 min)

**Live-code all three metrics together:**

```python
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np

mae = mean_absolute_error(y_test, predictions)
rmse = np.sqrt(mean_squared_error(y_test, predictions))
r2 = r2_score(y_test, predictions)

print(f"MAE:  {mae:.2f} lakh")
print(f"RMSE: {rmse:.2f} lakh")
print(f"R2:   {r2:.3f}")
```

**Run it and talk through each number as it appears:**

*"MAE says: on average, our prediction is off by about this many lakh, in either direction, all misses weighted equally."*

*"RMSE is in the same unit but weights big misses more heavily than small ones — if RMSE is noticeably bigger than MAE, that's a signal we have at least one large individual miss dragging the average up. This should feel familiar from Session 3's MSE discussion — RMSE is just the square root of MSE, brought back into the original units (lakh) instead of squared-lakh, which is easier to reason about."*

*"R² of, say, 0.85 means our model explains about 85% of the variation in house prices across this test set — the remaining 15% is unexplained by `sqft`, `bedrooms`, and `age_years` alone, possibly due to factors we haven't captured, like neighborhood or renovation quality."*

### Demonstrating RMSE's Outlier Sensitivity (10 min)

**Say:** *"Now let's demonstrate RMSE's outlier sensitivity directly — this is the most valuable moment of this block."*

**Live-code, injecting a synthetic outlier:**

```python
# Demonstrate RMSE's sensitivity to a single large miss
y_test_with_outlier = list(y_test.values)
predictions_with_outlier = list(predictions)

# Pretend one prediction missed badly (add a synthetic huge error)
y_test_with_outlier.append(150)
predictions_with_outlier.append(60)   # a 90 lakh miss on one point

mae_outlier = mean_absolute_error(y_test_with_outlier, predictions_with_outlier)
rmse_outlier = np.sqrt(mean_squared_error(y_test_with_outlier, predictions_with_outlier))

print(f"Original -> MAE: {mae:.2f}, RMSE: {rmse:.2f}")
print(f"With one bad miss -> MAE: {mae_outlier:.2f}, RMSE: {rmse_outlier:.2f}")
```

**Run it and compare the printed before/after numbers.**

**Say:** *"Watch how much MORE RMSE jumps compared to MAE, for the exact same single bad prediction added to an otherwise identical set. That's RMSE 'punishing' large errors harder — squaring a big number makes it much bigger, proportionally, than squaring a small number, exactly like we discussed with MSE in Session 3."*

**Ask:** *"If a business stakeholder says 'I care most about avoiding any single catastrophically wrong prediction, even if it means slightly worse average performance elsewhere' — which metric should they watch most closely, MAE or RMSE?"* (Answer: RMSE, precisely because it's more sensitive to large individual misses.)

### The Summary Table (4 min)

**Draw this summary table on the board:**

| Metric | Units | Sensitive to outliers? | Read as |
|---|---|---|---|
| MAE | Same as target (lakh) | Less | Average absolute miss |
| RMSE | Same as target (lakh) | More | "Typical" miss, big misses weighted more |
| R² | Unitless (0-1 typically) | — | % of variance explained |

### Quick Check-for-Understanding (3 min)

*"If a manager asks 'roughly how far off is this model, in rupees, on a typical prediction' — which metric answers that most directly, MAE or R²?"* (Answer: MAE, because it's in the same real-world unit as the target; R² is a relative/unitless number and doesn't directly translate to rupees.)

---

## BREAK (10 min)

*Suggested break prompt:* Ask students to guess, before returning, whether they expect the `bedrooms` coefficient to be larger or smaller in magnitude than the `sqft` coefficient, given that bedrooms range 2-4 while sqft ranges in the hundreds/thousands. Come back ready to compare guesses to the real printed numbers.

---

## SEGMENT 4: Interpreting Coefficients (20 min)

### Printing the Coefficients (5 min)

**Say:** *"A trained linear model isn't just a black box that spits out predictions — it hands you a coefficient for every feature, and each one has a direct, plain-English meaning."*

**Live-code:**

```python
for feature, coef in zip(X.columns, model.coef_):
    print(f"{feature}: {coef:.4f}")
print(f"Intercept: {model.intercept_:.4f}")
```

**Run it on `housing_sample.csv` and read the actual printed numbers together.** They will be close to: `sqft` positive and fairly small per-unit (since sqft ranges in the thousands), `bedrooms` positive and much larger per-unit, `age_years` negative.

**Revisit the break-time prediction:** *"Who guessed `bedrooms` would have a LARGER coefficient than `sqft`, even though bedrooms only range 2-4? Let's check the actual numbers — and discuss why that makes sense given the different SCALES these two features live on."* Guide toward: the coefficient tells you the effect PER UNIT of that specific feature. Since `sqft` moves in units of one square foot (a tiny change) while `bedrooms` moves in units of one whole bedroom (a much bigger practical change), it's completely expected for `bedrooms`' per-unit coefficient to look numerically larger even if `sqft`'s TOTAL contribution to price (coefficient times its typical range of values) is comparable or larger.

### Phrasing the Interpretation, Together (8 min)

**For each coefficient, have a student phrase the plain-English sentence out loud. Model the pattern first:**

*"For `sqft`, say the coefficient printed is `0.045`. That means: holding `bedrooms` and `age_years` fixed, each additional square foot is associated with about 0.045 lakh (roughly 4,500 rupees) more in predicted price."*

**Ask a student to do the same for `bedrooms`, then for `age_years`.** Expect:

*"Each additional bedroom, holding size and age fixed, adds roughly [X] lakh to predicted price"*

*"Each additional year of age, holding size and bedroom count fixed, is associated with about [Y] lakh LESS predicted price"* (age coefficient should be negative — confirm this matches the correlation check from SEGMENT 2).

**Write the phrasing template on the board for the class to reuse:**

```
"Holding [other features] fixed, each additional [1 unit of this feature]
is associated with [coefficient value] [more/less] [target], in [units]."
```

### The Correlated-Features Caution (5 min)

**Say:** *"Now the important caveat. Notice `sqft` and `bedrooms` are usually correlated in real housing data — bigger houses tend to have more bedrooms. When two features move together, the model can 'split credit' between them in ways that make any ONE coefficient's story less clean."*

**Ask:** *"If `bedrooms`' coefficient looked surprisingly SMALL or even slightly negative despite bigger houses obviously costing more, what would you suspect?"* Guide toward: correlated features (`sqft` and `bedrooms` moving together) can cause the model to attribute most of the price-increasing effect to whichever feature it "settles on" first, leaving the other looking artificially weak — even though both are genuinely related to price.

**Say:** *"We'll deal with this properly next session using Ridge and Lasso regularization, which give us tools specifically designed to handle this kind of correlated-feature situation more gracefully."*

---

## SEGMENT 5: Overfitting Diagnosis (15 min)

### Building an Intentionally Overfit Model (7 min)

**Say:** *"Let's deliberately build a model that overfits, so you can recognize the symptom before it ever reaches production — rather than only hearing about it in the abstract."*

**Live-code an intentionally overfit version using polynomial/interaction features on the SAME small dataset:**

```python
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import Pipeline

overfit_pipe = Pipeline(steps=[
    ("poly", PolynomialFeatures(degree=4, include_bias=False)),
    ("model", LinearRegression()),
])
overfit_pipe.fit(X_train, y_train)

print(f"Overfit model - Train R2: {overfit_pipe.score(X_train, y_train):.3f}")
print(f"Overfit model - Test R2:  {overfit_pipe.score(X_test, y_test):.3f}")

print(f"Baseline model - Train R2: {model.score(X_train, y_train):.3f}")
print(f"Baseline model - Test R2:  {model.score(X_test, y_test):.3f}")
```

**Run it and put both pairs of numbers on the board side by side.** With only 24 training rows and degree-4 polynomial features, expect the overfit model's train R² to look excellent (close to 1.0) while its test R² is noticeably worse than the plain baseline's test R² — sometimes even negative.

**Say, pointing at the gap:** *"This is overfitting in its purest form: the model has enough flexibility to trace almost perfectly through every training point, including the noise, but that memorized shape doesn't generalize to new houses it hasn't seen. The baseline model, with far fewer degrees of freedom, has closer train/test scores — even if its raw train score looks 'less impressive' by comparison."*

### What PolynomialFeatures Actually Did (3 min)

**Say, briefly:** *"`PolynomialFeatures(degree=4)` doesn't add new information — it creates new columns like `sqft²`, `sqft × bedrooms`, `age_years³`, and so on, purely by combining and raising the existing three features to different powers. With only 24 training rows and dozens of these new manufactured columns, the model has WAY more 'knobs to turn' than it has data points to constrain them — a classic recipe for overfitting."*

### The Diagnostic Table (5 min)

**Draw this diagnostic table on the board:**

| Pattern | Diagnosis |
|---|---|
| Train R² ≈ Test R², both reasonably high | Good fit |
| Train R² high, Test R² much lower | Overfitting |
| Train R² and Test R² both low | Underfitting |

**Ask:** *"Which row does our baseline model fall into? Which row does our polynomial-degree-4 model fall into?"* Confirm with the class using the actual printed numbers from this run.

---

## SEGMENT 6: Lab — Full Workflow on housing_sample.csv (15 min)

### Instructions (read aloud, step by step)

1. Load `housing_sample.csv`, split into `X` (`sqft`, `bedrooms`, `age_years`) and `y` (`price_lakhs`).
2. Split with `train_test_split(test_size=0.2, random_state=42)`.
3. Train a plain `LinearRegression`.
4. Report MAE, RMSE, and R² on the TEST set (not train).
5. Print all three coefficients and the intercept.
6. Write two full sentences: one interpreting the `sqft` coefficient, one interpreting the `age_years` coefficient, in plain business language a non-technical manager could understand.
7. Compare `model.score(X_train, y_train)` to `model.score(X_test, y_test)` and state in one sentence whether this baseline model shows signs of overfitting.

### Starter Code

```python
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

df = pd.read_csv("housing_sample.csv")
X = df[[___, ___, ___]]
y = df[___]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=___, random_state=42)

model = ___()
model.fit(___, ___)

preds = model.predict(___)
mae = mean_absolute_error(___, preds)
rmse = np.sqrt(mean_squared_error(___, preds))
r2 = r2_score(___, preds)
print(f"MAE: {mae:.2f}, RMSE: {rmse:.2f}, R2: {r2:.3f}")

for feature, coef in zip(X.columns, model.coef_):
    print(f"{feature}: {coef:.3f}")

# TODO: write your two interpretation sentences here as comments

print(f"Train R2: {model.score(X_train, y_train):.3f}")
print(f"Test R2: {model.score(X_test, y_test):.3f}")
# TODO: write your overfitting diagnosis sentence here as a comment
```

### Reference Solution

```python
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

df = pd.read_csv("housing_sample.csv")
X = df[["sqft", "bedrooms", "age_years"]]
y = df["price_lakhs"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)

preds = model.predict(X_test)
mae = mean_absolute_error(y_test, preds)
rmse = np.sqrt(mean_squared_error(y_test, preds))
r2 = r2_score(y_test, preds)
print(f"MAE: {mae:.2f}, RMSE: {rmse:.2f}, R2: {r2:.3f}")

for feature, coef in zip(X.columns, model.coef_):
    print(f"{feature}: {coef:.3f}")

# sqft: Holding bedrooms and age fixed, each additional square foot adds
# roughly [coef] lakh to predicted price.
# age_years: Holding size and bedrooms fixed, each additional year of age
# is associated with roughly [abs(coef)] lakh LESS predicted price.

print(f"Train R2: {model.score(X_train, y_train):.3f}")
print(f"Test R2: {model.score(X_test, y_test):.3f}")
# Diagnosis: train and test R2 are close to each other, so this baseline
# model does not show strong signs of overfitting.
```

**Instructor circulates**, checking specifically that students report metrics on the TEST set for the headline numbers (a common shortcut is to accidentally evaluate on train), and that the coefficient sentences hold other features "fixed" in their phrasing rather than treating each coefficient in isolation.

---

## SEGMENT 7: Summary, Wrap-Up & Q&A (5 min)

**What we covered today:**
- Trained a real `LinearRegression` model end to end, on a real (small) housing dataset
- Computed and interpreted MAE, RMSE, and R², and saw RMSE's outlier sensitivity directly
- Translated coefficients into plain business sentences, with the "holding other features fixed" caveat
- Deliberately built and diagnosed an overfit model by comparing train vs. test R²

**Bridge to next session:** *"Today you trained your first real predictive model end to end: fit, predict, evaluate with three complementary metrics, and interpret every coefficient in business language. You also saw overfitting happen live, with your own eyes, on this exact dataset. Next session tackles exactly that problem: Ridge and Lasso regularization, which give us dials to control how much a model is allowed to trust any single feature — and we'll formalize the bias-variance tradeoff you just started to feel intuitively today."*

**Homework / self-practice:**
1. Retrain the baseline model using only `sqft` as a single feature (drop `bedrooms` and `age_years`). Compare its test R² to the three-feature model's test R² — did dropping features help or hurt?
2. Compute MAE, RMSE, and R² on the TRAINING set as well as the test set for the baseline model, and compare all six numbers side by side.
3. Try `PolynomialFeatures(degree=2)` instead of `degree=4` in the overfit demo — does it overfit as badly? Write one sentence explaining what you observe.

---

## Q&A & Doubt Solving

**Likely questions and suggested answers:**

**Q: Why did we not use `stratify` when splitting for this regression problem, unlike Session 1's classification example?**
→ `stratify` preserves the proportions of a CATEGORICAL target across train/test. `price_lakhs` is continuous, not categorical, so there are no "classes" to stratify by. A plain random split is standard for regression targets.

**Q: Can a coefficient be interpreted on its own, without the "holding other features fixed" phrase?**
→ Technically no — that phrase is doing real work. A coefficient always describes the ISOLATED effect of one feature while every other feature in the model stays constant. Dropping that caveat when explaining results to stakeholders is one of the most common ways linear regression gets misinterpreted in practice.

**Q: If R² is negative, what does that even mean?**
→ It means the model performs WORSE than simply predicting the average target value for every row — a very poor fit, often a sign of severe overfitting (as we saw in the polynomial demo) or a fundamentally mismatched model for the data.

**Q: Is `random_state=42` doing anything different here compared to Session 1?**
→ Same role as before — it fixes the random shuffle used by `train_test_split` so the split is reproducible. The specific split obtained will differ between a classification target and a regression target, but the PURPOSE of `random_state` is identical in both cases.

**Q: We used `PolynomialFeatures` to force overfitting on purpose — would we ever use it in a real project?**
→ Yes, in moderation (e.g. `degree=2`) when you suspect a genuinely curved (non-linear) relationship between a feature and the target. The key is pairing it with regularization (next session) or enough data to support the added complexity — using it carelessly, as we did today with `degree=4` on 24 rows, is a textbook overfitting recipe.

**Q: Does scikit-learn have a way to get MAE, RMSE, and R2 all in one call instead of three separate imports?**
→ Not in a single function call by default, though `cross_validate` (an extension of `cross_val_score`) can compute multiple scoring metrics at once during cross-validation, which becomes useful once we're comparing several models side by side starting Session 5.

---

## Instructor Notes

- **Prerequisite check:** Confirm in the first five minutes that students recall Session 3's vocabulary bridge (`m`↔coefficient, `c`↔intercept) — today's SEGMENT 4 depends on that connection feeling natural, not newly introduced.
- **Common mistake:** Reporting R² alone without MAE/RMSE — students often gravitate to R² because it's a single, bounded, "percentage-like" number, and skip the metrics that are actually in real-world units. Catch this in the lab and ask students to always report all three together.
- **Another common mistake:** Interpreting a coefficient without the "holding other features fixed" caveat, especially when eager to summarize findings quickly. Model the correct phrasing explicitly, more than once, during SEGMENT 4.
- **Another common mistake:** Evaluating "test" performance using the training set by accident, especially when copy-pasting code between cells. Point this out explicitly if you see it during the lab — it's an easy, easy-to-miss bug.
- **Engagement tip:** The RMSE-outlier-sensitivity demo (SEGMENT 3) is the strongest "aha" moment of the day — don't rush it, and consider re-running with an even MORE extreme synthetic outlier if the effect doesn't look dramatic enough on your machine's random split.
- **Time check:** If running behind before the break, shorten SEGMENT 2's optional correlation check to a single sentence summary instead of live-running `df.corr()`.
- **If running long after the break:** Compress SEGMENT 5 to just the headline train/test R² comparison, skipping the "what PolynomialFeatures actually did" explanation (assign it as a homework reading instead).
- **Materials to prepare:** `housing_sample.csv` open and ready; a scratch notebook with SEGMENT 5's overfit demo pre-typed so the polynomial feature explosion doesn't eat live-coding time.

---

## Common Errors — Quick Reference

| Bug / mistake | Symptom | Fix |
|---|---|---|
| Reporting R² alone, no MAE/RMSE | Stakeholders can't translate the result into real-world units (rupees) | Always report all three metrics together |
| Interpreting a coefficient without "holding other features fixed" | Misleading claims like "more bedrooms always means higher price," ignoring correlated features | Use the board template: "Holding [others] fixed, each additional [feature] is associated with..." |
| Evaluating "test" performance on the training set by accident | Inflated, misleading metrics reported as if they were honest | Double-check which `X`/`y` pair is passed into `.score()` / metric functions |
| Comparing train vs. test using two DIFFERENT metrics | Apples-to-oranges comparison, invalid overfitting diagnosis | Use the SAME metric on both sides of any train/test comparison |
| Adding many polynomial features on a small dataset without regularization | Severe overfitting: high train R², much lower (or negative) test R² | Prefer simpler models on small data, or pair complexity with regularization (next session) |

---

## Appendix: Coefficient Interpretation Drill (Optional, If Time Allows)

For each printed coefficient below (hypothetical, for practice), have students phrase the plain-English sentence using the board template:

| Feature | Coefficient | Target |
|---|---|---|
| years_experience | 2.1 | salary_lakhs |
| distance_to_metro_km | -3.5 | price_lakhs |
| num_bathrooms | 8.0 | price_lakhs |
| ad_spend_thousands | 0.9 | units_sold |

**Sample expected answer for row 1:** *"Holding other features fixed, each additional year of experience is associated with about 2.1 lakh more in predicted salary."*

---

## Appendix: Metric Sensitivity Comparison Table (Instructor Reference)

For a small set of predictions with one added outlier, roughly how MAE and RMSE typically respond:

| Change | MAE effect | RMSE effect |
|---|---|---|
| One small additional error (e.g. +2) | Small increase | Small increase |
| One large additional error (e.g. +50) | Moderate increase | Large increase |
| Many small errors spread evenly | Noticeable increase | Noticeable increase, roughly proportional |
| One extreme outlier among otherwise perfect predictions | Modest increase | Disproportionately large increase |

---

## FAQ — Additional Questions

**Q: Does the ORDER of columns in `X` matter for `model.coef_`?**
→ Yes for READING the output — `model.coef_` returns coefficients in the same order as `X`'s columns, which is exactly why we `zip(X.columns, model.coef_)` rather than assuming a fixed order. It does not affect the model's actual predictions or fit quality.

**Q: If I add a feature that's completely unrelated to price (like a random number column), what would happen to R²?**
→ On the TRAINING set, R² can only stay the same or increase slightly (linear regression can always find some tiny, spurious pattern to exploit, especially with few rows) — but on the TEST set, an unrelated feature typically hurts performance slightly, since it adds noise without adding real signal. This is a good bridge into next session's regularization discussion.

**Q: Why does `model.score(X, y)` return R² specifically, and not MAE or RMSE?**
→ `.score()` is scikit-learn's convention for "the default metric for this type of estimator" — for regressors, that default is R². You can always compute MAE/RMSE separately via `sklearn.metrics`, as we did throughout today's session, when you want those specific numbers.

**Q: Is `LinearRegression` always going to be a "good enough" baseline, or should I always start with something more complex?**
→ Starting simple, with `LinearRegression`, is a strong habit for tabular regression problems specifically because it's fast, interpretable, and gives you a real number to beat. Later sessions introduce Ridge/Lasso (regularized linear models) and tree-based models (Sessions 9-10) as natural next steps if a plain linear model underperforms or clearly violates linearity assumptions.

---

## SEGMENT 8: Supplemental Code Demos (Instructor Optional, If Time or Advanced Group)

### Demo A — Single-feature vs multi-feature comparison (5 min)

```python
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

# Single-feature baseline
single = LinearRegression()
single.fit(X_train[["sqft"]], y_train)
single_preds = single.predict(X_test[["sqft"]])
print("Single-feature (sqft only) test R2:", r2_score(y_test, single_preds))

# Multi-feature baseline (from earlier in the session)
print("Multi-feature test R2:", model.score(X_test, y_test))
```

**Break it down:**
- Comparing a one-feature model to the three-feature model quantifies exactly how much `bedrooms` and `age_years` are adding beyond `sqft` alone
- If the multi-feature R² is only marginally better, that's a hint `sqft` was doing most of the work already
- This is a simple, manual precursor to the feature-selection ideas that Lasso will formalize next session

**Ask:** If the single-feature model's R2 is nearly as good as the three-feature model's, what might that suggest about `bedrooms` and `age_years`?

**Common mistake:** Assuming "more features always means a better model."

**Fix:** More features can add noise as easily as signal — always compare, don't assume.

### Demo B — Residual plot for visual diagnosis (5 min, requires matplotlib)

```python
import matplotlib.pyplot as plt

residuals = y_test.values - predictions
plt.scatter(predictions, residuals)
plt.axhline(y=0, color="red", linestyle="--")
plt.xlabel("Predicted price (lakh)")
plt.ylabel("Residual (actual - predicted)")
plt.title("Residual plot")
plt.show()
```

**Break it down:**
- A "healthy" residual plot shows points scattered randomly around the horizontal red line at zero, with no obvious pattern
- A funnel shape (residuals growing larger for bigger predicted prices) would suggest the model's errors scale with price — a common real-estate pattern worth flagging
- A curved pattern would suggest the true relationship isn't fully linear, hinting that polynomial features or a different model family might help

**Ask:** What would it mean if every residual for high-priced homes was positive (model under-predicting expensive houses)?

**Common mistake:** Only looking at aggregate metrics (MAE/RMSE/R2) and never visually inspecting residuals.

**Fix:** Make a residual plot a standard habit for any regression project — it often reveals patterns a single summary number hides.

### Demo C — Predicting on a brand-new, hand-built row (4 min)

```python
new_house = pd.DataFrame({"sqft": [1600], "bedrooms": [3], "age_years": [5]})
predicted_price = model.predict(new_house)
print(f"Predicted price for a 1600 sqft, 3-bedroom, 5-year-old house: {predicted_price[0]:.2f} lakh")
```

**Break it down:**
- This is the real-world "point" of training a model — predicting on data that was never in the original dataset at all
- Building `new_house` as a DataFrame with the SAME column names and order as `X_train` is essential — mismatched columns cause silent errors or crashes
- A great closing demo before the lab, since it makes the abstract "trained model" feel like a genuinely usable tool

**Ask:** What would happen if `new_house` had a different column order than `X_train`?

**Common mistake:** Passing raw lists/arrays instead of a properly-labelled DataFrame with matching column names.

**Fix:** Always construct new prediction inputs as a DataFrame using the exact same column names as training.

---

## Materials Checklist

- [ ] `housing_sample.csv` open and readable in the working notebook environment
- [ ] Scratch notebook with SEGMENT 5's overfit (PolynomialFeatures) demo pre-typed
- [ ] Whiteboard space for the coefficient-interpretation sentence template
- [ ] Optional: matplotlib available for Demo B's residual plot
- [ ] Timer visible for the lab segment

---

## Timing Contingencies

| Situation | Action |
|---|---|
| Running 10 min behind before break | Shorten SEGMENT 2's optional correlation check to a one-sentence summary |
| Running long after break | Compress SEGMENT 5 to just the headline train/test R² comparison |
| Low energy after lunch/break | Run the Appendix coefficient-interpretation drill as a quick group activity |
| Advanced group finishes lab early | Assign Demo A or Demo B from SEGMENT 8 as a stretch task |
| No shared screen / projector issue | Read code blocks aloud and have students type along from the printed lecture script |

---

## End-of-Session Quiz (5 Questions)

1. Which metric — MAE, RMSE, or R² — is most sensitive to a single large prediction error?
2. What does a coefficient of `-3.5` for `distance_to_metro_km` mean in plain English, assuming target is house price?
3. Why must you evaluate final metrics on the TEST set rather than the TRAINING set?
4. What pattern in train vs. test R² indicates overfitting?
5. Why did today's lab NOT use `stratify=y` in `train_test_split`?

**Answer key (instructor):**
1. RMSE — squaring residuals before averaging penalizes large errors disproportionately.
2. Holding other features fixed, each additional kilometer of distance to the metro is associated with about 3.5 lakh less in predicted price.
3. Because training-set performance reflects memorization as much as generalization; only unseen data gives an honest estimate of real-world performance.
4. Train R² noticeably higher than test R² — the model fits training data well but doesn't generalize.
5. `stratify` preserves proportions of a categorical target; `price_lakhs` is continuous, so stratification doesn't apply the same way.

---

## Homework Rubric

| Criterion | Excellent (4) | Good (3) | Needs Work (2) | Incomplete (1) |
|---|---|---|---|---|
| Single-feature vs multi-feature comparison | Correct R2 comparison with a clear interpretation | Comparison present, thin interpretation | Numbers reported, no interpretation | Not attempted |
| Train vs test metrics for all three metrics | All six numbers reported and compared correctly | Most numbers reported, minor gaps | Partial numbers, no comparison | Not attempted |
| PolynomialFeatures degree=2 comparison | Correct run, clear explanation of reduced overfitting vs degree=4 | Correct run, thin explanation | Attempted, unclear results | Not attempted |

**Total:** /12 — Pass threshold: 8/12
