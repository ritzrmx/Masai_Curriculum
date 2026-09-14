# Lecture Script: Machine Learning — Linear Regression
> **Instructor Reference** — Module 2: Classical ML | Academic Session 20 | Duration: 2 Hours | Instructor: Aswath Rao

---

## Session Overview
**Goal:** By the end of this session, students can train a `LinearRegression` model with sklearn, generate predictions, evaluate performance with MAE/RMSE/R², interpret coefficients as real business quantities, and diagnose overfitting by comparing train vs. test performance.

**Student profile at this point:** Just came from Session 19's Master Class, where they hand-derived gradient descent for a line. They understand *why* a best-fit line minimizes squared residuals, but have never used a real ML library to do it. Likely wrong assumption: some will expect `LinearRegression` to use gradient descent under the hood exactly like Session 19's demo — worth clarifying it uses a more direct mathematical shortcut for this specific case, though the goal (minimize SSR) is identical. Boredom risk: low — first real trained model of the course, energy should be naturally high.

**Key outcome:** Students should leave able to look at a train-vs-test metric comparison and immediately say whether it looks healthy or worrying.

> 🎯 **The one sentence this session must land:** *A model's coefficients tell you what it learned, and comparing train vs. test performance tells you whether what it learned will actually hold up on data it's never seen.*

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| Opening — "Hiring the Expert Hiker" | 8 min | 8 min |
| Concept Block 1: From Hand-Derived Line to sklearn's LinearRegression | 10 min | 18 min |
| Practical Block 1: Predict By Hand, Then Check | 6 min | 24 min |
| Concept Block 2: Generating Predictions with .predict() | 8 min | 32 min |
| Concept Block 3: Evaluating with MAE, RMSE, R² | 14 min | 46 min |
| Practical Block 2: Compute MAE/RMSE By Hand | 8 min | 54 min |
| **BREAK** | 10 min | 64 min |
| Concept Block 4: Interpreting Coefficients | 12 min | 76 min |
| Practical Block 3: Live Coding Demo (TA Code) | 14 min | 90 min |
| Concept Block 5: Diagnosing Overfitting — Train vs. Test | 12 min | 102 min |
| Practical Block 4: Spot the Overfit Scenario | 8 min | 110 min |
| Summary & Bridge | 5 min | 115 min |
| Q&A & Doubt Solving | 5 min | 120 min |

---

## Opening — "Hiring the Expert Hiker" (8 min)

Open with this, verbatim-ish:

> "Last session, you personally played the blindfolded hiker — you computed gradients, took small steps, and watched the error slowly fall, epoch by epoch. Today, imagine hiring an expert who already knows exactly where the valley floor is and walks straight there, instantly."

Pause. Ask the room:

> "What do you think that 'expert' looks like in code — how many lines do you think it takes to find the exact same best-fit line you built from scratch last session?"

(Let guesses land — most will overestimate.)

> "Two lines. `LinearRegression()`, then `.fit()`. Today we hand the entire gradient descent loop over to sklearn — and then we learn how to actually judge whether what it found is any good."

**Pivot line:** "Everything conceptual from Session 19 — residuals, best fit, the downhill walk — is still happening. It's just hidden behind these two lines now. Understanding what's hidden is what makes you dangerous with this tool instead of just a button-pusher."

**Context for sessions ahead:** "This exact rhythm — fit, predict, evaluate, interpret, check for overfitting — repeats for every single model for the rest of Module 2. Get comfortable with it today and every future session gets easier."

---

## Concept Block 1: From Hand-Derived Line to sklearn's LinearRegression (10 min)

Write on the board:

```python
from sklearn.linear_model import LinearRegression

model = LinearRegression()
model.fit(X_train, y_train)
```

> "That's it. `model.fit()` finds the best slope for every feature and the best intercept, minimizing squared residuals — the exact same goal as last session's gradient descent, just reached through a more direct mathematical shortcut built specifically for this case."

### 🔴 The trap / highest-value moment
> "`.fit()` only ever works on the data you hand it. Always split first — Session 17's habit — and call `.fit()` only on `X_train`, `y_train`, never the full dataset, never the test set. Write this down: *fit on train, always.*"

---

## Practical Block 1: Predict By Hand, Then Check (6 min)

Give students the Session 19 hand-derived line (`time = 3×distance + 5`) and ask them to predict the delivery time for `distance=7` by hand (mentally or on paper, 1 minute). Then reveal that sklearn's `LinearRegression`, trained on noisy real-world-like data, will produce a *slightly different* line — not exactly 3 and 5 — because real data has noise. This primes the next block.

---

## Concept Block 2: Generating Predictions with `.predict()` (8 min)

> "A Swiggy dispatcher with an ETA formula doesn't re-derive it for every new order — they just plug in distance and item count to get an instant estimate. `.predict()` does exactly this."

```python
predictions = model.predict(X_test)
```

> "Given new feature values, it applies the already-learned line to produce a number — instantly, for as many rows as you give it at once."

💬 Expect a question: "does `.predict()` retrain anything?" Welcome it. Say: "No — `.predict()` never changes the model. It only applies what `.fit()` already learned. Only `.fit()` ever updates the coefficients."

---

## Concept Block 3: Evaluating with MAE, RMSE, R² (14 min)

> "Imagine reporting to your manager how good your delivery-time predictions were last month, across hundreds of orders. You wouldn't hand over hundreds of residuals — you'd summarize."

Write the three-metric table on the board:

| Metric | Meaning |
|---|---|
| MAE | Average of `|actual − predicted|` |
| RMSE | Square root of average squared residual — penalizes big misses more |
| R² | Proportion of variation explained, 0 to 1 |

```python
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

mae = mean_absolute_error(y_test, predictions)
rmse = mean_squared_error(y_test, predictions) ** 0.5
r2 = r2_score(y_test, predictions)
```

> "MAE of 2.1 means predictions are off by about 2.1 minutes on average. R² of 0.87 means the model explains 87% of the variation in delivery times — far better than just guessing the same average every time."

### 🔴 The trap / highest-value moment
> "MAE and RMSE share the same units as your target, but if RMSE is noticeably bigger than MAE, that's a signal some individual predictions are badly off — even while the average looks fine. Write this down: *never report just one error metric without glancing at the other.*"

---

## Practical Block 2: Compute MAE/RMSE By Hand (8 min)

Give a tiny table of 4 actual/predicted pairs. Have students compute MAE and RMSE by hand in pairs, 4 minutes, then cold-call to compare answers and discuss which pair had the metric with the bigger gap and why (likely due to one larger individual miss inflating RMSE more than MAE).

---

## BREAK (10 min)

---

## Concept Block 4: Interpreting Coefficients (12 min)

> "Recall Session 19's line: `time = 3 × distance + 5`. That 3 is a coefficient — 3 extra minutes per extra kilometer, holding everything else equal. With multiple features, each one gets its own coefficient — like a surcharge card listing exactly how much each factor adds."

Write an example on the board:

```
distance_km coefficient: 2.9
num_items coefficient:   1.4
intercept:               5.2
```

> "Read aloud: each extra kilometer adds about 2.9 minutes; each extra item adds about 1.4 minutes; every delivery has a baseline 5.2-minute handling time before either factor kicks in."

### 🔴 The trap / highest-value moment
> "'Holding all other features constant' is the phrase everyone forgets. A coefficient describes the effect of one feature only if every other feature stays fixed — not what happens in a messy real world where features often move together. Write this down: *a coefficient is a holding-everything-else-equal statement, not a real-world guarantee.*"

---

## Practical Block 3: Live Coding Demo (TA Code) (14 min)

**Handoff line (must match TA code file's opening comment):** "Let's actually train, predict, and evaluate a real model in code — same Swiggy distance and item-count data from the last two sessions."

Hand off to `ta-code - Session 20 - Linear Regression.py`, narrating each `# --- EXPLAIN ---` block aloud:

1. Build the synthetic two-feature dataset (`distance_km`, `num_items` → `delivery_time_min`), reusing Session 19's true relationship pattern
2. Split with `train_test_split` (Session 17 habit)
3. `model.fit(X_train, y_train)` — point out how fast this runs compared to Session 19's 500-epoch loop
4. `model.predict(X_test)` — show a handful of predicted vs. actual values side by side
5. Compute and print MAE, RMSE, R² on **both** train and test — this is the key moment, pause and have students compare the two sets of numbers themselves before you say anything
6. Print `model.coef_` and `model.intercept_`, and interpret them aloud exactly as done in Concept Block 4

💬 Expect a question: "why are the train and test numbers so close here?" Welcome it. Say: "Because this dataset is genuinely close to linear with modest noise — a well-behaved case. You'll see what an *unhealthy* gap looks like in the next block."

---

## Concept Block 5: Diagnosing Overfitting — Train vs. Test (12 min)

> "Recall Session 17's memorizing student — perfect on an exam made of exactly the questions they studied, then struggling the moment the questions change. A model performing beautifully on training data but noticeably worse on test data is doing the exact same thing."

Write the diagnostic table on the board:

| Train R² | Test R² | Diagnosis |
|---|---|---|
| 0.87 | 0.85 | Healthy — small gap, generalizes well |
| 0.91 | 0.62 | Overfitting — memorized training noise |
| 0.55 | 0.80 | Unusual — investigate the split or leakage |

### 🔴 The trap / highest-value moment
> "A model doing *worse* on train than test isn't secretly great — it usually signals something else went wrong, like an unusually easy test split or a leakage issue from Session 18. Write this down: *any suspiciously large gap, in either direction, deserves investigation before you trust the model.*"

---

## Practical Block 4: Spot the Overfit Scenario (8 min)

Present 3 model scenarios (train/test R² pairs) on screen. Have students individually rank them from "most trustworthy" to "least trustworthy" and justify in one sentence each, then cold-call for the ranking and reasoning.

💬 Expect a debate about whether a small negative gap (test slightly better than train) is fine or worrying. Welcome it. Say: "A small gap either direction is usually just noise from the specific split — it's *large* gaps in either direction that deserve real investigation."

---

## Summary & Bridge (5 min)

| Concept | The one thing to remember |
|---|---|
| `LinearRegression().fit()` | Automates last session's gradient descent for this specific case |
| `.predict()` | Applies the already-learned line to new data; never changes the model |
| MAE / RMSE / R² | Three complementary summaries of how good the predictions are |
| Coefficients | Per-unit effect of a feature, holding everything else constant |
| Train vs. test comparison | A large gap signals overfitting or another underlying issue |

Close on the thesis line: "A model's coefficients tell you what it learned, and comparing train vs. test performance tells you whether what it learned will actually hold up on data it's never seen."

**Bridge to next session:** "Today's model behaved well — train and test numbers stayed close. Session 21 is about what to do when they *don't* — Ridge and Lasso regularization pull an overfitting model back toward simplicity, and we'll explore the bias-variance tradeoff that explains why that works."

---

## Q&A & Doubt Solving (5 min)

**Q: Does `LinearRegression` use gradient descent internally?**
→ Not for this specific problem — it uses a more direct mathematical shortcut (a closed-form solution) available specifically for linear regression's exact SSR-minimization case. The goal is identical to Session 19's gradient descent; the method is just faster for this one case.

**Q: Can I have more than two features?**
→ Yes — `LinearRegression` handles any number of numeric features. Each gets its own coefficient, interpreted the same way: effect per unit, holding others constant.

**Q: Which metric should I report to a non-technical stakeholder?**
→ MAE is usually easiest to explain, since it's in plain real-world units ("off by about 2 minutes on average"). RMSE and R² are more useful for comparing models technically.

**Q: If train and test R² are both low, is that overfitting?**
→ No — that's underfitting, a different problem entirely (the model isn't capturing the pattern well even on data it trained on). Overfitting specifically means train performance is notably *better* than test performance.

**Q: What if a coefficient comes out negative?**
→ It means that feature *decreases* the prediction as it increases — perfectly valid and often expected (e.g., a "years since last order" feature might have a negative coefficient predicting future order frequency).

---

## Instructor Notes
- **Words not yet earned:** Ridge, Lasso, alpha (regularization strength), bias-variance tradeoff, predict_proba, classification threshold — all Session 21 onward.
- **Biggest risk in this session:** overconfidence — a well-behaved dataset today might make students think overfitting is rare or easy to spot. Explicitly flag that today's data was deliberately well-behaved, and real datasets are often messier.
- **Board management:** keep the MAE/RMSE/R² table and the train-vs-test diagnostic table both visible from Concept Block 3 onward.
- **Common confusions, numbered:**
  1. Expecting `LinearRegression` to use gradient descent identically to Session 19's hand-rolled version
  2. Reporting only one of MAE/RMSE/R² without cross-checking the others
  3. Interpreting a coefficient as a real-world guarantee rather than a holding-everything-else-equal statement
  4. Treating "train performance worse than test" as automatically good news rather than worth investigating
- **Cross-references:** Session 21 (Regularization) directly extends today's model with Ridge/Lasso when overfitting appears; Session 22 (Logistic Regression) reuses today's exact fit/predict/evaluate/interpret rhythm for a classification target.
- **Local/cultural context notes:** keep the same Swiggy distance/item-count delivery-time dataset from Session 19 continuing here — the numeric consistency (true slope ≈3, true intercept ≈5) lets students directly compare Session 19's hand-rolled result to today's sklearn result.
