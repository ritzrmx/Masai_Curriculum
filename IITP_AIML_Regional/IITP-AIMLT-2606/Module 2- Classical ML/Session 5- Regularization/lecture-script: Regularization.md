# Lecture Script: Regularization
> **Instructor Reference** — Module 2: Classical ML | Session 5 | Duration: 2 Hours

---

## Session Overview

**Goal:** Students train Ridge and Lasso regression alongside an unregularized baseline on a correlated-feature housing dataset, tune the `alpha` hyperparameter, observe its effect on coefficients, and explain the bias-variance tradeoff in plain language.

**Student profile at this point:** Just trained and diagnosed an overfit `LinearRegression` model in Session 4, including deliberately overfitting with `PolynomialFeatures`. Comfortable with coefficients, MAE/RMSE/R², and the train-vs-test overfitting diagnostic.

**Key outcome:** Every student produces a 3-way comparison table (baseline, tuned Ridge, tuned Lasso) on `housing_multicollinear.csv`, can point to a specific coefficient that shrank or hit zero, and can explain in one paragraph why `alpha` trades bias for variance.

**Dataset for this session:** `housing_multicollinear.csv` (in this folder) — 30 rows of `sqft`, `num_rooms`, `age_years`, `distance_center_km`, `price_lakhs`. `sqft` and `num_rooms` are deliberately correlated, as are `age_years` and `distance_center_km`, to make regularization's effect visible.

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| SEGMENT 1: Opening — Recall the Overfit Model | 10 min | 0:10 |
| SEGMENT 2: Why Unregularized Models Struggle with Correlated Features | 15 min | 0:25 |
| SEGMENT 3: Ridge — Shrinking Coefficients Smoothly | 20 min | 0:45 |
| SEGMENT 4: Lasso — Shrinking and Selecting | 15 min | 1:00 |
| **BREAK** | 10 min | 1:10 |
| SEGMENT 5: Tuning alpha with Cross-Validation | 20 min | 1:30 |
| SEGMENT 6: Bias-Variance Tradeoff, in Plain Language | 10 min | 1:40 |
| SEGMENT 7: Lab — Baseline vs Ridge vs Lasso Comparison Table | 15 min | 1:55 |
| SEGMENT 8: Summary, Wrap-Up & Q&A | 5 min | 2:00 |

---

## SEGMENT 1: Opening — Recall the Overfit Model (10 min)

**Say:** *"Last session, we deliberately built a model that overfit — remember the `PolynomialFeatures(degree=4)` demo, where train R² looked almost perfect but test R² collapsed? Today we fix exactly that failure mode, using a tool that keeps every feature but stops the model from trusting any single one too much."*

**Ask:** *"Before we start, can anyone recall WHY that polynomial model overfit so badly?"* Guide toward: too many manufactured features (from raising existing ones to powers 2-4) relative to only 24 training rows gave the model far more 'knobs to turn' than it had data points to constrain them.

**Live-code a quick refresher, reusing today's new dataset instead:**

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

df = pd.read_csv("housing_multicollinear.csv")
print(df.head())
print(df.corr(numeric_only=True))
```

**Run it and point directly at the correlation matrix.** **Say:** *"Look at the correlation between `sqft` and `num_rooms` — it should be very high, close to 1. Same story for `age_years` and `distance_center_km` — older homes in this toy dataset also tend to sit farther from the center. This is called MULTICOLLINEARITY: when two or more features move together so strongly that a model struggles to tell which one is 'really' driving the outcome."*

**Say, setting up the session:** *"Today's tools — Ridge and Lasso — are scikit-learn's answer to exactly this problem, plus the more general overfitting problem from last session. By the end of today you'll be able to train both, tune their strength, and explain in one paragraph why this trade is worth making."*

**Learning contract for today — write on board:**

- Explain why correlated features destabilize plain linear regression coefficients
- Train Ridge and Lasso and compare their coefficients to an unregularized baseline
- Tune `alpha` using cross-validation, watching coefficients shrink as it increases
- Explain the bias-variance tradeoff in plain language, no formulas required

---

## SEGMENT 2: Why Unregularized Models Struggle with Correlated Features (15 min)

### The Baseline Model, Live (8 min)

**Say:** *"Let's fit the plain baseline first and look closely at its coefficients."*

```python
X = df[["sqft", "num_rooms", "age_years", "distance_center_km"]]
y = df["price_lakhs"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

baseline = LinearRegression()
baseline.fit(X_train, y_train)

print("Baseline test R2:", baseline.score(X_test, y_test))
for feature, coef in zip(X.columns, baseline.coef_):
    print(f"{feature}: {coef:.4f}")
```

**Run it and read the coefficients aloud.** **Say:** *"Watch `sqft` and `num_rooms` specifically. Since they move together in this data, the model has some freedom in how it 'splits credit' between them — one might get an unusually large coefficient, the other unusually small, or even a sign that looks counterintuitive, even though both clearly relate to price in reality."*

**Ask:** *"If I told you both `sqft` and `num_rooms` obviously make a house MORE valuable, but one of the two coefficients came out negative — what would that tell you about the model, versus about reality?"* Guide toward: it doesn't mean bigger homes with more rooms are actually cheaper — it means the model is unstable when features are this correlated, arbitrarily assigning credit between two things that are hard to tell apart statistically.

### Demonstrating Instability Directly (7 min)

**Say:** *"Let's prove this instability with a small experiment: refit the baseline on slightly different subsets of the training data and watch the coefficients move."*

```python
import numpy as np

for seed in [1, 2, 3]:
    sample = X_train.sample(frac=0.8, random_state=seed)
    y_sample = y_train.loc[sample.index]
    m = LinearRegression().fit(sample, y_sample)
    print(f"seed={seed}:", dict(zip(X.columns, np.round(m.coef_, 3))))
```

**Run it and compare the three printed dictionaries.** **Say:** *"Notice `sqft` and `num_rooms`'s coefficients swing around more than `age_years` and `distance_center_km`'s do, relative to their own scale — though in a small dataset like this, expect some instability across the board. This swinginess, especially pronounced for the correlated pair, is the practical symptom of multicollinearity: small changes in which rows you train on cause disproportionately large changes in the coefficients of correlated features."*

**Say, transitioning:** *"Ridge and Lasso both fix this by adding a penalty that discourages any coefficient from growing too large — which, as a side effect, makes the model far less sensitive to exactly this kind of instability."*

---

## SEGMENT 3: Ridge — Shrinking Coefficients Smoothly (20 min)

### The Coach Analogy and the Math Idea (5 min)

**Say:** *"Ridge is like a strict but fair coach: every player (feature) gets to play, but no single player gets to dominate the game — everyone's role is toned down proportionally. Mathematically, Ridge adds a penalty to the training objective equal to the SUM OF SQUARED coefficients — so the bigger a coefficient tries to grow, the more it's penalized. This is called an L2 penalty."*

**Write on the board:**

```
Plain linear regression minimizes:  sum of squared residuals
Ridge minimizes:                    sum of squared residuals + alpha * sum(coefficient^2)
```

**Say:** *"`alpha` controls how much weight that penalty term carries. Set `alpha=0` and Ridge becomes identical to plain `LinearRegression`. Increase `alpha` and the model is pushed harder to keep coefficients small, trading a little bit of training fit for a lot more stability."*

### Live Demo — Ridge vs Baseline Coefficients (10 min)

```python
from sklearn.linear_model import Ridge

ridge = Ridge(alpha=1.0)
ridge.fit(X_train, y_train)

print("Ridge test R2:", ridge.score(X_test, y_test))
for feature, coef in zip(X.columns, ridge.coef_):
    print(f"{feature}: {coef:.4f}")
```

**Run it and put the Ridge coefficients directly next to the baseline's on the board, feature by feature.** **Say:** *"Notice every coefficient moved CLOSER to zero compared to the baseline — some by a little, some by more, especially the correlated pair. None of them hit exactly zero though — that's the Ridge signature: shrink everything, drop nothing."*

**Now demonstrate a much larger `alpha` for contrast:**

```python
ridge_strong = Ridge(alpha=100)
ridge_strong.fit(X_train, y_train)

print("Strong Ridge (alpha=100) test R2:", ridge_strong.score(X_test, y_test))
for feature, coef in zip(X.columns, ridge_strong.coef_):
    print(f"{feature}: {coef:.4f}")
```

**Run it.** **Say:** *"With `alpha=100`, every coefficient should look noticeably smaller still — the model has become much more conservative. Watch what happens to test R2 though — it may actually get WORSE here, because we've over-constrained the model. This previews SEGMENT 5's tuning process: there's a sweet spot, not 'more regularization is always better.'"*

### Stability Re-Check (5 min)

**Say:** *"Let's re-run our earlier instability experiment, this time with Ridge instead of plain linear regression."*

```python
for seed in [1, 2, 3]:
    sample = X_train.sample(frac=0.8, random_state=seed)
    y_sample = y_train.loc[sample.index]
    m = Ridge(alpha=1.0).fit(sample, y_sample)
    print(f"seed={seed}:", dict(zip(X.columns, np.round(m.coef_, 3))))
```

**Run it and compare to SEGMENT 2's baseline version.** **Say:** *"The coefficients here should look noticeably more STABLE across the three seeds than the plain baseline's did. That's the real-world payoff of Ridge: not just smaller numbers, but more TRUSTWORTHY, reproducible ones."*

---

## SEGMENT 4: Lasso — Shrinking and Selecting (15 min)

### The Stricter Coach (4 min)

**Say:** *"Lasso is a stricter coach who benches weak players entirely. Instead of penalizing the SUM OF SQUARED coefficients like Ridge, Lasso penalizes the SUM OF ABSOLUTE coefficients — an L1 penalty. This mathematical difference has a striking practical effect: some coefficients get pushed all the way to exactly zero, effectively removing those features from the model."*

**Write on the board:**

```
Lasso minimizes: sum of squared residuals + alpha * sum(|coefficient|)
```

### Live Demo — Lasso and Feature Selection (8 min)

```python
from sklearn.linear_model import Lasso

lasso = Lasso(alpha=0.5)
lasso.fit(X_train, y_train)

print("Lasso test R2:", lasso.score(X_test, y_test))
for feature, coef in zip(X.columns, lasso.coef_):
    print(f"{feature}: {coef:.4f}")

non_zero = sum(c != 0 for c in lasso.coef_)
print(f"Non-zero coefficients: {non_zero} out of {len(lasso.coef_)}")
```

**Run it and look for at least one coefficient printed as exactly `0.0000`.** **Say:** *"If one of `num_rooms` or `age_years`/`distance_center_km` came out at exactly zero, that's Lasso telling you: 'given the OTHER correlated feature is already in the model, this one isn't adding enough independent information to be worth keeping.' This is automatic feature selection, entirely as a side effect of the L1 penalty's shape — no separate feature-selection step required."*

**Now sweep alpha to show the selection effect scaling:**

```python
for a in [0.01, 0.1, 0.5, 2.0]:
    l = Lasso(alpha=a).fit(X_train, y_train)
    nz = sum(c != 0 for c in l.coef_)
    print(f"alpha={a}: non-zero coefficients = {nz}, test R2 = {l.score(X_test, y_test):.3f}")
```

**Run it.** **Say:** *"Watch the non-zero count SHRINK as alpha grows — larger alpha means Lasso is willing to drop more features entirely. But also watch test R2 — at some point, dropping too much genuinely useful information starts to hurt."*

### Ridge vs Lasso, Side by Side (3 min)

**Draw this comparison table on the board, having the class fill in the "good for" column from what they just observed:**

| | Ridge (L2) | Lasso (L1) |
|---|---|---|
| Penalty | Sum of squared coefficients | Sum of absolute coefficients |
| Coefficients can hit exactly 0? | No | Yes |
| Good for | Many correlated features, keep them all but tame them | Feature selection — actively suspect some features are dead weight |

---

## BREAK (10 min)

*Suggested break prompt:* Ask students to guess whether increasing `alpha` moves a Lasso model TOWARD or AWAY FROM the unregularized baseline, and come back ready to defend their guess with the leash analogy.

---

## SEGMENT 5: Tuning alpha with Cross-Validation (20 min)

### Why We Can't Just Guess alpha (5 min)

**Say:** *"We've seen `alpha=1`, `alpha=100`, and a small sweep for Lasso — but how do we actually CHOOSE the right value for a new project, rather than guessing? Same tool as Session 1: cross-validation."*

### Live Demo — The Full alpha Sweep (10 min)

```python
from sklearn.model_selection import cross_val_score

alphas = [0.001, 0.01, 0.1, 1, 10, 100]
print("Ridge alpha sweep:")
for a in alphas:
    scores = cross_val_score(Ridge(alpha=a), X_train, y_train, cv=5, scoring="r2")
    print(f"  alpha={a}: mean R2 = {scores.mean():.3f} (+/- {scores.std():.3f})")
```

**Run it and read the results aloud, row by row.** **Ask:** *"Which alpha gave the highest mean R2? Is the difference between the best and second-best alpha large or small?"*

**Say:** *"Notice the shape: very small alpha should look close to the unregularized baseline's performance; very large alpha should get noticeably WORSE, since we're over-constraining the model. Somewhere in the middle is the sweet spot — and cross-validation, not a single train/test split, is what lets us find it reliably, exactly as we learned in Session 1."*

**Now do the same sweep for Lasso:**

```python
print("Lasso alpha sweep:")
for a in alphas:
    scores = cross_val_score(Lasso(alpha=a, max_iter=5000), X_train, y_train, cv=5, scoring="r2")
    print(f"  alpha={a}: mean R2 = {scores.mean():.3f} (+/- {scores.std():.3f})")
```

**Run it.** **Say:** *"Note the `max_iter=5000` — Lasso is fit iteratively (echoing Session 3's gradient descent discussion), and small datasets with certain alpha values can need more iterations to fully converge; scikit-learn will warn you if it needs more."*

### Picking the Best alpha Programmatically (5 min)

```python
best_alpha, best_score = None, -float("inf")
for a in alphas:
    scores = cross_val_score(Ridge(alpha=a), X_train, y_train, cv=5, scoring="r2")
    mean_score = scores.mean()
    if mean_score > best_score:
        best_alpha, best_score = a, mean_score

print(f"Best alpha: {best_alpha}, CV R2: {best_score:.3f}")

final_ridge = Ridge(alpha=best_alpha)
final_ridge.fit(X_train, y_train)
print("Final test R2:", final_ridge.score(X_test, y_test))
```

**Say:** *"Notice the process: we used `X_train`/`y_train` for the ENTIRE alpha search via cross-validation — the test set stays completely untouched until this very last line, exactly as Session 1 taught us. This is model SELECTION happening honestly, without any test-set leakage."*

**Mention briefly, without live-coding:** *"scikit-learn also offers `RidgeCV` and `LassoCV`, which automate this exact sweep-and-pick process in one line. We built it manually today so the mechanism is fully visible — feel free to use the CV-suffixed versions in your own projects going forward."*

---

## SEGMENT 6: Bias-Variance Tradeoff, in Plain Language (10 min)

### The Leash Analogy, Revisited (4 min)

**Say:** *"Let's connect everything we did today to one unifying idea: the bias-variance tradeoff. Think of `alpha` as a leash length on a dog — the model. Leash too long (alpha too small) — the dog wanders anywhere, chasing every squirrel. That's HIGH VARIANCE: the model is too sensitive to the specific training data and won't generalize, which is just another word for overfitting. Leash too short (alpha too large) — the dog barely moves, ignoring real scents. That's HIGH BIAS: the model is too simple or too constrained and misses real patterns, which is underfitting."*

Draw this on the board:

```
Low alpha  -> flexible  -> high variance -> risk of overfitting
High alpha -> rigid     -> high bias     -> risk of underfitting
                    \            /
                  Sweet spot: tuned alpha
```

### Connecting Back to Today's Numbers (4 min)

**Say:** *"Look back at your printed alpha sweep from SEGMENT 5. The smallest alphas behaved close to the unregularized baseline — flexible, potentially high variance. The largest alphas pushed every coefficient toward zero — rigid, high bias, and you likely saw test R2 drop. The alpha your sweep picked as 'best' is the point where these two failure modes roughly balance out for THIS dataset."*

**Ask:** *"If you doubled the size of your training dataset, would you expect the 'best' alpha to move up or down?"* Guide toward: with more data, the model has less need for a strong penalty to stay stable — the best alpha would likely move DOWN, since variance naturally decreases with more training examples.

### Plain-Language Summary Sentence (2 min)

**Say, and have students write this down:** *"Regularization doesn't make a model 'smarter' — it makes a deliberate trade: give up a little bit of fit on the training data, in exchange for a lot more stability and generalization on new data. `alpha` is the dial that controls how much of that trade you're making."*

---

## SEGMENT 7: Lab — Baseline vs Ridge vs Lasso Comparison Table (15 min)

### Instructions (read aloud, step by step)

1. Load `housing_multicollinear.csv`, split `X` (`sqft`, `num_rooms`, `age_years`, `distance_center_km`) and `y` (`price_lakhs`) with `train_test_split(test_size=0.2, random_state=42)`.
2. Train a baseline `LinearRegression`.
3. Use cross-validation to find the best `alpha` for Ridge from `[0.001, 0.01, 0.1, 1, 10, 100]`, then fit a final Ridge with that alpha.
4. Use cross-validation to find the best `alpha` for Lasso from the same grid, then fit a final Lasso with that alpha.
5. Build a comparison table: model | test R2 | number of non-zero coefficients.
6. Write one sentence identifying which single coefficient shrank the most going from baseline to Ridge, and one sentence naming any feature Lasso dropped entirely (if any).

### Starter Code

```python
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LinearRegression, Ridge, Lasso

df = pd.read_csv("housing_multicollinear.csv")
X = df[[___, ___, ___, ___]]
y = df[___]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=___, random_state=42)

baseline = ___().fit(X_train, y_train)

alphas = [0.001, 0.01, 0.1, 1, 10, 100]

# TODO: find best Ridge alpha via cross_val_score, fit final_ridge
# TODO: find best Lasso alpha via cross_val_score, fit final_lasso

for name, m in [("Baseline", baseline), ("Ridge", ___), ("Lasso", ___)]:
    nz = sum(c != 0 for c in m.coef_)
    print(f"{name}: test R2 = {m.score(X_test, y_test):.3f}, non-zero coefs = {nz}")
```

### Reference Solution

```python
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LinearRegression, Ridge, Lasso

df = pd.read_csv("housing_multicollinear.csv")
X = df[["sqft", "num_rooms", "age_years", "distance_center_km"]]
y = df["price_lakhs"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

baseline = LinearRegression().fit(X_train, y_train)

alphas = [0.001, 0.01, 0.1, 1, 10, 100]

best_ridge_alpha, best_ridge_score = None, -float("inf")
for a in alphas:
    scores = cross_val_score(Ridge(alpha=a), X_train, y_train, cv=5, scoring="r2")
    if scores.mean() > best_ridge_score:
        best_ridge_alpha, best_ridge_score = a, scores.mean()
final_ridge = Ridge(alpha=best_ridge_alpha).fit(X_train, y_train)

best_lasso_alpha, best_lasso_score = None, -float("inf")
for a in alphas:
    scores = cross_val_score(Lasso(alpha=a, max_iter=5000), X_train, y_train, cv=5, scoring="r2")
    if scores.mean() > best_lasso_score:
        best_lasso_alpha, best_lasso_score = a, scores.mean()
final_lasso = Lasso(alpha=best_lasso_alpha, max_iter=5000).fit(X_train, y_train)

for name, m in [("Baseline", baseline), ("Ridge", final_ridge), ("Lasso", final_lasso)]:
    nz = sum(c != 0 for c in m.coef_)
    print(f"{name}: test R2 = {m.score(X_test, y_test):.3f}, non-zero coefs = {nz}")

# Note: sqft and num_rooms typically shrink the most from baseline to Ridge,
# since they are the most correlated pair in this dataset. Lasso may drop
# num_rooms or distance_center_km entirely depending on the chosen alpha.
```

**Instructor circulates**, checking that students used cross-validation (not the test set) to select `alpha`, and that the final comparison correctly reuses the SAME test set for all three models.

---

## SEGMENT 8: Summary, Wrap-Up & Q&A (5 min)

**What we covered today:**
- Multicollinearity destabilizes plain linear regression's coefficients
- Ridge (L2) shrinks all coefficients smoothly, never to exactly zero
- Lasso (L1) shrinks and can zero out coefficients, giving automatic feature selection
- `alpha` controls regularization strength, tuned honestly via cross-validation on the training set
- The bias-variance tradeoff: low alpha risks high variance/overfitting, high alpha risks high bias/underfitting

**Bridge to next session:** *"Today you learned to control HOW MUCH a regression model trusts its features. Next session, we shift from predicting NUMBERS to predicting CATEGORIES — logistic regression, `predict_proba()`, and the classification threshold. You'll recognize the same 'controlled flexibility' mindset showing up again."*

**Homework / self-practice:**
1. Re-run the alpha sweep for Ridge with a finer grid (e.g. `[0.5, 1, 2, 5]`) around today's best alpha — does the best value change?
2. Compare the coefficient for `sqft` across baseline, best Ridge, and best Lasso in a single printed table. Which model shrank it the most?
3. Try `Lasso(alpha=0.001)` — does it behave close to the unregularized baseline? Explain why in one sentence.

---

## Q&A & Doubt Solving

**Likely questions and suggested answers:**

**Q: Can I use both Ridge and Lasso penalties together?**
→ Yes — this is called `ElasticNet` in scikit-learn, which combines both an L1 and L2 penalty with a mixing ratio. It's a natural "further reading" topic once Ridge and Lasso feel comfortable individually.

**Q: Does regularization ever help even when features AREN'T correlated?**
→ Yes — it also generally guards against overfitting whenever you have many features relative to your number of rows, or noisy features, regardless of correlation. Multicollinearity is just the clearest, most visually demonstrable case.

**Q: Why did Lasso need `max_iter=5000` but Ridge didn't?**
→ Ridge has a closed-form solution (much like plain linear regression) for most solvers, so it doesn't need iteration. Lasso's L1 penalty doesn't have as clean a closed-form solution, so scikit-learn fits it iteratively — small or oddly-scaled datasets can need more iterations than the default to fully converge.

**Q: If Lasso drops a feature (coefficient = 0), does that mean the feature is truly useless in the real world?**
→ Not necessarily — it means that feature wasn't adding independent predictive value GIVEN the other features already in the model. A dropped feature might still matter a great deal on its own, or in a different combination of features.

**Q: Should I always scale my features before using Ridge or Lasso?**
→ Yes, strongly recommended — since the penalty is based on the SIZE of coefficients, features on very different scales (like `sqft` in the thousands vs. `age_years` in the tens) would be penalized unevenly without scaling. Today's toy dataset happens to work reasonably without it, but combining `StandardScaler` (Session 2) with Ridge/Lasso inside a `Pipeline` is the standard, safer practice.

**Q: How is choosing `alpha` different from choosing which ALGORITHM to use (e.g. Ridge vs Lasso vs plain linear regression)?**
→ Both are technically "hyperparameter" or "model selection" decisions, and both should be made using cross-validation on the training set only — exactly the same honest process, just searching over a different kind of choice.

---

## Instructor Notes

- **Prerequisite check:** Confirm students recall Session 4's coefficient interpretation and overfitting diagnosis — today directly extends both.
- **Common mistake:** Assuming Lasso is always "better" because it does feature selection. Correct this explicitly in SEGMENT 4 — Lasso can underperform Ridge when most features genuinely matter and none deserve to be dropped to zero.
- **Another common mistake:** Tuning `alpha` by checking test-set performance directly instead of using cross-validation on the training set. Watch for this during the lab and correct immediately, tying it back to Session 1's core rule.
- **Engagement tip:** SEGMENT 2's "instability across random subsamples" demo is the strongest justification for WHY regularization matters at all — don't skip it, even under time pressure, since it's what makes SEGMENT 3's payoff concrete rather than abstract.
- **Time check:** If running behind before the break, shorten SEGMENT 4's alpha sweep for Lasso to two values (`0.1` and `1.0`) instead of four.
- **If running long after the break:** Compress SEGMENT 6 to just the leash analogy and the plain-language summary sentence, skipping the "what happens if you double your data" discussion question.
- **Materials to prepare:** `housing_multicollinear.csv` open and ready; a pre-typed notebook with all live demos ready to run in sequence.

---

## Common Errors — Quick Reference

| Bug / mistake | Symptom | Fix |
|---|---|---|
| Tuning alpha using the test set directly | Overly optimistic, dishonest alpha selection | Use `cross_val_score` on `X_train, y_train` only |
| Assuming Lasso is always superior to Ridge | Poor performance when most features genuinely matter | Compare both via cross-validation; don't assume |
| Forgetting `max_iter` on Lasso with small/tricky data | Convergence warning, possibly unreliable coefficients | Increase `max_iter` (e.g. to 5000 or 10000) |
| Not scaling features before Ridge/Lasso | Penalty applied unevenly across differently-scaled features | Combine `StandardScaler` with Ridge/Lasso inside a `Pipeline` |
| Interpreting alpha=0 as "regularized" | Misunderstanding that alpha=0 is identical to unregularized regression | Alpha=0 means NO penalty at all |

---

## Appendix: Ridge vs Lasso Coefficient Behavior (Instructor Reference)

For a toy 4-feature model as `alpha` increases from 0 to very large:

| alpha | Ridge coefficients | Lasso coefficients |
|---|---|---|
| 0 (no penalty) | Same as unregularized baseline | Same as unregularized baseline |
| Small | Slightly shrunk, none at zero | Slightly shrunk, none at zero yet |
| Medium | Noticeably shrunk, none at zero | Some coefficients may hit exactly zero |
| Very large | All coefficients near zero, none exactly zero | Most or all coefficients at exactly zero |

---

## Appendix: Supplemental Practice Bank (Optional, If Time Allows)

### Drill 1 — Predict the effect of alpha

For each scenario, state whether coefficients would be LARGER or SMALLER in magnitude:

1. Ridge with `alpha=0.01` vs Ridge with `alpha=50` → alpha=0.01 gives larger coefficients
2. Lasso with `alpha=0.001` vs unregularized baseline → nearly identical, both relatively large
3. Ridge with `alpha=1000` vs Lasso with `alpha=1000` → Ridge coefficients shrink toward zero but stay non-zero; Lasso coefficients likely hit exactly zero

### Drill 2 — Bias-variance classification

For each described model behavior, classify as "high bias" or "high variance":

1. Train R² = 0.99, Test R² = 0.40 → High variance (overfitting)
2. Train R² = 0.35, Test R² = 0.33 → High bias (underfitting)
3. Train R² = 0.85, Test R² = 0.83 → Neither — good fit

---

## FAQ — Additional Questions

**Q: Is there a rule of thumb for the RANGE of alpha values worth trying?**
→ A common practice is a logarithmic sweep — `[0.001, 0.01, 0.1, 1, 10, 100]`, as we used today — since regularization strength effects tend to change more meaningfully on a multiplicative scale rather than an additive one.

**Q: Does regularization change how you'd interpret a coefficient in plain English (from Session 4)?**
→ The interpretation TEMPLATE stays the same ("holding other features fixed, each additional unit is associated with..."), but the actual VALUE is now influenced by the penalty, not purely by the raw relationship in the data. It's still meaningful, just slightly "dampened" by design.

**Q: If my Ridge and Lasso models both perform about the same as the baseline, was today's work wasted?**
→ Not at all — even matching baseline performance while gaining STABILITY (as demonstrated in the resampling experiment) is valuable, especially for a model that will be retrained periodically on new data in production. Stability itself is often worth the trade even without a raw performance gain.

**Q: Can regularization be applied to logistic regression too, not just linear regression?**
→ Yes, and in fact scikit-learn's `LogisticRegression` applies L2 regularization BY DEFAULT (controlled by its `C` parameter, which is the inverse of `alpha`) — a detail we'll pick up naturally next session.

---

## SEGMENT 9: Supplemental Code Demos (Instructor Optional, If Time or Advanced Group)

### Demo A — Watching one coefficient shrink continuously as alpha grows (5 min)

```python
import matplotlib.pyplot as plt

alphas_fine = [0.001, 0.01, 0.1, 1, 5, 10, 50, 100, 500]
sqft_coefs = []
for a in alphas_fine:
    m = Ridge(alpha=a).fit(X_train, y_train)
    sqft_coefs.append(m.coef_[0])   # sqft is the first column

plt.plot(alphas_fine, sqft_coefs, marker="o")
plt.xscale("log")
plt.xlabel("alpha (log scale)")
plt.ylabel("sqft coefficient")
plt.title("Ridge coefficient path for sqft")
plt.show()
```

**Break it down:**
- This plots exactly the "shrinking toward zero" story from SEGMENT 3, but continuously across many alpha values instead of just two snapshots
- The log-scaled x-axis is standard practice for regularization strength plots, since effects compound multiplicatively
- This kind of "coefficient path" plot is a common way real ML teams visually communicate a regularization sweep to stakeholders

**Ask:** Would you expect this curve to ever cross zero and become negative for a feature we know is positively related to price?

**Common mistake:** Assuming a coefficient can never change sign as alpha increases.

**Fix:** For a feature involved in strong multicollinearity, sign changes ARE possible as the model's "credit-splitting" shifts — worth flagging as an advanced nuance, not something to worry about for this dataset's dominant features.

### Demo B — ElasticNet as a preview of "best of both" (5 min)

```python
from sklearn.linear_model import ElasticNet

elastic = ElasticNet(alpha=0.5, l1_ratio=0.5)
elastic.fit(X_train, y_train)
print("ElasticNet test R2:", elastic.score(X_test, y_test))
print("Non-zero coefficients:", sum(c != 0 for c in elastic.coef_))
```

**Break it down:**
- `l1_ratio=0.5` splits the penalty evenly between Lasso-style (L1) and Ridge-style (L2) behavior
- `l1_ratio=1.0` makes ElasticNet identical to Lasso; `l1_ratio=0.0` makes it identical to Ridge
- This is flagged as "further reading" — not required knowledge for this course, but useful to know it exists

**Ask:** If you wanted SOME feature selection but also wanted the stability benefits of Ridge, what `l1_ratio` might you start experimenting with?

**Common mistake:** Assuming ElasticNet requires learning an entirely new mental model.

**Fix:** It's simply a blend of the two ideas already covered today — no new penalty concept required.

### Demo C — Regularization inside a full Pipeline with scaling (4 min)

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

scaled_ridge = Pipeline(steps=[
    ("scaler", StandardScaler()),
    ("model", Ridge(alpha=1.0)),
])
scaled_ridge.fit(X_train, y_train)
print("Scaled Ridge test R2:", scaled_ridge.score(X_test, y_test))
```

**Break it down:**
- This directly reuses Session 2's `Pipeline` skills, combined with today's Ridge model
- Scaling before regularizing ensures the penalty treats every feature fairly, regardless of its raw numeric scale
- This is the pattern to default to in real projects, rather than applying Ridge/Lasso to unscaled raw features as we did for teaching clarity today

**Ask:** Why might skipping the scaler cause `distance_center_km` and `sqft` to be penalized unevenly?

**Common mistake:** Applying Ridge/Lasso directly to unscaled data in a real project.

**Fix:** Always scale numeric features first when regularization is in play — wrap both in one `Pipeline`.

---

## Materials Checklist

- [ ] `housing_multicollinear.csv` open and readable in the working notebook environment
- [ ] Pre-typed notebook with all live demos ready to run in sequence
- [ ] Whiteboard space for the Ridge/Lasso penalty formulas and the bias-variance leash diagram
- [ ] Optional: matplotlib available for Demo A's coefficient path plot
- [ ] Timer visible for the lab segment

---

## Timing Contingencies

| Situation | Action |
|---|---|
| Running 10 min behind before break | Shorten SEGMENT 4's alpha sweep for Lasso to two values instead of four |
| Running long after break | Compress SEGMENT 6 to the leash analogy and summary sentence only |
| Low energy after lunch/break | Run Appendix Drill 2 (bias-variance classification) as a quick energizer |
| Advanced group finishes lab early | Assign Demo A or Demo B from SEGMENT 9 as a stretch task |
| No shared screen / projector issue | Read code blocks aloud and have students type along from the printed lecture script |

---

## End-of-Session Quiz (5 Questions)

1. What penalty does Ridge add to the loss function, and what penalty does Lasso add?
2. Can a Ridge coefficient ever become exactly zero? Can a Lasso coefficient?
3. If increasing alpha causes test R2 to get worse, what does that suggest?
4. Why should you tune alpha using cross-validation on the training set rather than the test set?
5. In plain language, what is the bias-variance tradeoff?

**Answer key (instructor):**
1. Ridge adds the sum of squared coefficients (L2); Lasso adds the sum of absolute coefficients (L1).
2. Ridge coefficients shrink but never hit exactly zero; Lasso coefficients can hit exactly zero.
3. The model has become too constrained (high bias/underfitting) — alpha is likely too large.
4. To avoid leaking the test set into model selection, keeping the final test evaluation honest.
5. A model too simple/constrained misses real patterns (high bias, underfitting); a model too flexible fits training noise and fails to generalize (high variance, overfitting) — regularization trades some of one for less of the other.

---

## Homework Rubric

| Criterion | Excellent (4) | Good (3) | Needs Work (2) | Incomplete (1) |
|---|---|---|---|---|
| Finer alpha grid sweep | Correct sweep, clear comparison to original best alpha | Sweep run, thin comparison | Numbers reported, no comparison | Not attempted |
| Coefficient comparison table (baseline/Ridge/Lasso) | All three models compared for sqft coefficient with correct interpretation | Comparison present, thin interpretation | Partial table | Not attempted |
| Lasso alpha=0.001 explanation | Correct, clearly ties to "near-zero penalty behaves like baseline" | Mostly correct | Vague | Not attempted |

**Total:** /12 — Pass threshold: 8/12
