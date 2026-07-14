# Lecture Script: The ML Workflow, Data Prep & Reliability
> **Instructor Reference** — Module 2: Classical ML | Session 1 | Duration: 2 Hours

---

## Session Overview

**Goal:** Students train their first machine learning model. They take a raw DataFrame, frame it as an ML problem, separate features from target, split off a held-out test set, call `.fit()` and `.predict()`, and read an honest score. They then deliberately build a *leaky* model, watch it score a perfect 1.00, and repair it.

**Student profile at this point:** They have finished Module 1 — confident with Python, Pandas (cleaning, groupby, merge), NumPy, SQL, EDA and Matplotlib. They have **never trained a model**. `scikit-learn` is brand new. Assume zero ML vocabulary: "feature", "target", "fit", "test set" are all new words today.

**Key outcome:** A working notebook containing a trained `LinearRegression` model with a defensible test score, and a written list of leakage checks they can apply to any future dataset.

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| Opening — The Spam Filter Nobody Could Write | 5 min | 0:05 |
| **Concept 1:** ML vs Programming, Supervised vs Unsupervised | 10 min | 0:15 |
| **Practical 1:** From DataFrame to X and y | 15 min | 0:30 |
| **Concept 2:** The ML Lifecycle and the Train/Test Split | 10 min | 0:40 |
| **Practical 2:** Your first `model.fit()` | 15 min | 0:55 |
| **BREAK** | 10 min | 1:05 |
| **Concept 3:** Data Leakage — Why Perfect Scores Are Bad News | 10 min | 1:15 |
| **Practical 3:** Build a leaky model, then fix it | 15 min | 1:30 |
| **Concept 4:** Reliable, Reproducible Data Prep | 10 min | 1:40 |
| **Practical 4:** The end-to-end Pipeline on a real dataset | 10 min | 1:50 |
| Summary & Wrap-Up | 5 min | 1:55 |
| Q&A & Doubt Solving | 5 min | 2:00 |

---

## Opening (5 min)

**Hook — do this live on the board.** Ask the room: *"Write me the Python rules for detecting a spam email. Shout them out, I'll type."*

Type what they say into a visible cell — `if "lottery" in subject`, `elif "free" in subject`, `elif "winner" in subject`, and so on.

Let it run for about six rules, then push back on each one: *"'Free' — so my colleague's mail 'Are you free at 4pm?' is spam? 'Winner' — so the IPL results newsletter is spam?"* Watch the rule list collapse under its own exceptions.

*"Nobody on Earth has written a working spam filter this way. And yet Gmail catches spam with better than 99% accuracy. So where did its rules come from?"*

**What machine learning is NOT:**
- A robot that "thinks"
- Magic that works without good data
- A replacement for asking a clear question first
- Something you can trust just because the number on screen is high

**What machine learning IS:**
- A program that derives its own rules from labelled examples
- A workflow where 70% of the work happens *before* any model is trained
- A discipline built entirely on one honesty mechanism: **hold data out and test on it**

---

## Concept Block 1: ML vs Programming, Supervised vs Unsupervised (10 min)

### Write this on the board — the arrow flip

```
TRADITIONAL:   DATA  +  RULES    -->  ANSWERS
MACHINE LEARN: DATA  +  ANSWERS  -->  RULES
```

That is the entire paradigm shift, and it is worth ninety seconds of silence on the board. In Module 1 they always supplied the rules. Today they supply the *answers* instead, and the machine derives the rules.

### The two families

| | Supervised | Unsupervised |
|---|---|---|
| Data has known answers? | Yes — every row is **labelled** | No |
| Question | "What will this be?" | "How does this group?" |
| Tasks | Regression, Classification | Clustering |
| We cover it in | Sessions 1–8 | Session 9 |

### Supervised splits by the *type of answer*

| Target type | Task | Example question | Answer looks like |
|---|---|---|---|
| A number on a scale | **Regression** | What rent will this flat fetch? | ₹28,400 |
| A category from a list | **Classification** | Is this transaction fraud? | Yes / No |

**Board drill (60 seconds, ask the room):** Netflix "what to watch next" · predicting Bengaluru rainfall in mm · flagging a defective part on an assembly line · grouping IPL fans by viewing habits. Which family? Which task? Expect disagreement on Netflix — that is the point; problem framing is a judgement call, not a lookup.

**Say this out loud:** *"Choosing regression vs classification is not decided by your data. It is decided by the decision someone will make with your output."*

---

## Practical Block 1: From DataFrame to X and y (15 min)

Everything today runs on one small, inline dataset — no downloads, no file paths. Twenty-four Bengaluru rental flats.

```python
import pandas as pd
import numpy as np

rents = pd.DataFrame({
    "area_sqft":   [1583, 1200, 1271, 1526, 1143, 1380, 1450, 720, 516, 810, 792, 1498,
                    1545, 456, 1049, 1435, 607, 1406, 592, 1011, 1429, 813, 859, 784],
    "bedrooms":    [3, 2, 2, 3, 2, 3, 3, 1, 1, 1, 1, 3,
                    3, 1, 2, 3, 1, 3, 1, 2, 3, 1, 1, 1],
    "age_years":   [16, 6, 21, 10, 11, 11, 13, 12, 11, 21, 17, 17,
                    15, 14, 8, 21, 10, 5, 18, 4, 19, 13, 3, 1],
    "km_to_metro": [0.6, 3.3, 3.0, 5.5, 3.9, 3.3, 3.2, 1.8, 0.5, 1.5, 4.3, 1.5,
                    2.5, 0.4, 5.0, 1.3, 1.9, 5.3, 3.3, 5.1, 4.0, 4.6, 0.9, 3.4],
    "rent":        [42500, 35000, 31500, 37000, 26500, 35000, 39500, 15000, 14000, 9500, 18000, 39000,
                    42000, 8500, 24000, 37500, 15500, 37000, 8000, 27500, 32000, 10500, 24000, 17500],
})

print("Shape:", rents.shape)        # (24, 5)
print(rents.describe().round(1))
```

Now the single most important line of code in the whole module — separating **features** from **target**.

```python
# X = the features: everything the model is allowed to look at
# y = the target: the answer we want it to produce
X = rents.drop(columns=["rent"])   # a DataFrame  (24 rows, 4 columns)
y = rents["rent"]                  # a Series     (24 values)

print("X shape:", X.shape)         # (24, 4)
print("y shape:", y.shape)         # (24,)
print("Features:", X.columns.tolist())

# Sanity check before ML: does anything obviously relate to rent?
print(rents.corr(numeric_only=True)["rent"].sort_values(ascending=False).round(2))
```

**Expected output:** `area_sqft` and `bedrooms` correlate very strongly and positively with rent (both above 0.9). `age_years` and `km_to_metro` show almost *no* correlation on their own. Do not skip past that — flag it now and revisit it after Practical 2, because the model will still find them useful once size is accounted for. Marginal correlation is not the same as usefulness inside a model.

**Live walk-through:** Hold on the `X` / `y` cell. Say the convention out loud: *"Capital X, because it is a two-dimensional table. Lowercase y, because it is a single column."* This is universal in ML code — every book, every repo, every StackOverflow answer.

Then ask the room: **"Why did we drop `rent` from `X`?"** Push until someone says the real reason: if the answer is sitting inside the inputs, the model does not have to learn anything. Tell them to remember that sentence — you are coming back to it hard in Concept 3.

---

## Concept Block 2: The ML Lifecycle and the Train/Test Split (10 min)

### The nine steps (write on board, number them)

```
1. FRAME      What are we predicting? What decision does it change?
2. COLLECT    Get the data.
3. CLEAN      Fix nulls, types, duplicates.        <- Module 1 skills
4. FEATURES   Decide what goes into X.
5. SPLIT      Lock away a test set.                <- TODAY'S BIG IDEA
6. TRAIN      model.fit(X_train, y_train)
7. EVALUATE   Score on the test set. Once.
8. DEPLOY     Put it behind an API.
9. MONITOR    Watch it rot. Loop back to 1.
```

Point at step 6. *"That is one line. Steps 1 to 5 are the other 70% of the job. If you only remember one thing from Module 2, remember which end of this list the real work lives on."*

### Why hold data out?

**The exam analogy — say it slowly.** You practise on past papers whose answers you can see. You would never claim you were ready by re-solving those same papers with the answer key open. The real test is a paper you have never seen.

| | Training set | Test set |
|---|---|---|
| Size | ~75–80% | ~20–25% |
| Model sees the answers? | Yes | **Never**, until the very end |
| What it tells you | Whether the model *can* learn | Whether the model will work on **new** data |

**Generalisation** is the whole game: does this model work on rows it has never seen? A model that scores 1.00 on its own training data may have simply memorised it. The test set is your only honest instrument.

**The one rule, on the board, boxed:**

```
The test set is opened ONCE. At the end.
Not to tune. Not to peek. Not to "just check".
```

---

## Practical Block 2: Your First `model.fit()` (15 min)

This is the moment. Tell them so.

```python
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error

# --- Step 5: SPLIT (before anything else touches the data) ---
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.25,     # 25% held out
    random_state=42     # same split every time this runs
)

print("Train rows:", X_train.shape[0])   # 18
print("Test rows :", X_test.shape[0])    # 6

# --- Step 6: TRAIN ---
model = LinearRegression()      # 1. choose the model
model.fit(X_train, y_train)     # 2. learn from the TRAINING data only

# --- Step 7: EVALUATE ---
y_pred = model.predict(X_test)  # 3. predict on rows the model has never seen

mae = mean_absolute_error(y_test, y_pred)
print(f"Mean Absolute Error on test set: Rs {mae:,.0f}")
print(f"R2 on test set  : {model.score(X_test, y_test):.3f}")
print(f"R2 on train set : {model.score(X_train, y_train):.3f}")
```

**Expected output:** the MAE lands in the low thousands of rupees — around ₹2,500–3,000 — against rents ranging ₹8,000–₹42,500. The test R² should come out around 0.9, with the training R² a little higher. Do not promise exact numbers; read whatever the screen shows.

```python
# What rules did it actually learn? Inspect the coefficients.
for name, coef in zip(X.columns, model.coef_):
    print(f"{name:>14}: {coef:+,.1f}")
print(f"{'intercept':>14}: {model.intercept_:+,.1f}")

# --- Use it. Predict the rent for a flat that does not exist yet. ---
new_flat = pd.DataFrame([{
    "area_sqft": 900, "bedrooms": 2, "age_years": 5, "km_to_metro": 1.0
}])
print(f"Predicted rent: Rs {model.predict(new_flat)[0]:,.0f}")
```

**Expected output:** a positive coefficient on `area_sqft` (each extra square foot adds rupees), and negative coefficients on `age_years` and `km_to_metro` (older, further from the metro = cheaper). The signs should match intuition.

**Live walk-through:** Pause after `model.fit()` and let it land — *"You have now trained a machine learning model. That is it. That is the line everyone is scared of."*

Then make three points, in this order:
1. **`fit` on train, `predict` on test.** Never `fit` on the test set. Ever.
2. **Read the coefficients.** *"The model says every extra kilometre from the metro costs about a thousand rupees of rent. Does Bengaluru agree with that? Does the sign make sense?"* A model whose signs are nonsense is a model with a bug. Now close the loop from Practical 1: `km_to_metro` had almost zero correlation with rent on its own, yet the model gives it a large negative weight. Why? Because *holding size constant*, distance matters — and a plain correlation cannot hold anything constant. This is the first hint of why we build models at all.
3. **Ask the room:** *"Train R² is higher than test R². Is that a bug, or is that expected?"* Expected — the model saw the training rows. If the gap were enormous, that would be **overfitting**, which is exactly where Session 2 starts.

---

## BREAK (10 min)

*Something to chew on: our model is off by roughly ₹2,800 per flat. If the model were instead off by ₹0 — perfectly correct on every single test flat — would you be delighted, or would you be worried? Come back with an answer.*

---

## Concept Block 3: Data Leakage — Why Perfect Scores Are Bad News (10 min)

Open with the answer to the break question. *"If your model is perfect, you have almost certainly cheated. You just don't know how yet."*

### The definition (board)

```
DATA LEAKAGE = information reaching the model at TRAINING time
               that it could NOT possibly have at PREDICTION time.
```

### The IPL fireworks story — tell it, don't summarise it

You are predicting which IPL team wins. One of your columns is *"fireworks let off by the crowd"*. Your model is 100% accurate on every past match. Brilliant. But fireworks only go off *after* the winner is known. On a live match, that column is blank — and your model is worthless. It never learnt cricket. It learnt fireworks.

### The two shapes leakage takes

| Type | Mechanism | Rent-dataset example |
|---|---|---|
| **Target leakage** | A feature secretly encodes the answer | `maintenance_fee` = 8% of rent. It *is* the rent. |
| **Preprocessing leakage** | Statistics computed before splitting | Scaling with the mean of *all* rows — test rows shaped the training |

### The three questions to ask of every single column

```
1. Would I actually KNOW this value at prediction time?
2. Was this column DERIVED from the target?
3. Did I clean/scale/impute BEFORE I split?

Any "yes" to 2 or 3 -- or any "no" to 1 -- is leakage.
```

**The tell-tale sign:** an accuracy or R² that looks *too good*. 0.99. 1.00. Real data is noisy and real people are unpredictable. **Be suspicious before you are proud.**

---

## Practical Block 3: Build a Leaky Model, Then Fix It (15 min)

Deliberately sabotage the dataset. This is the most memorable fifteen minutes of the session — do not skip it.

```python
# A property portal gives us one extra column: the monthly maintenance fee.
# Looks innocent. It is not: maintenance is billed at 8% of the rent.
rents_v2 = rents.copy()
rents_v2["maintenance_fee"] = (rents_v2["rent"] * 0.08).round(0)

# --- Train WITH the leaky column ---
X_leaky = rents_v2.drop(columns=["rent"])   # keeps maintenance_fee
y = rents_v2["rent"]

Xtr, Xte, ytr, yte = train_test_split(X_leaky, y, test_size=0.25, random_state=42)
leaky_model = LinearRegression().fit(Xtr, ytr)

print(f"LEAKY  -> R2 : {leaky_model.score(Xte, yte):.4f}")
print(f"LEAKY  -> MAE: Rs {mean_absolute_error(yte, leaky_model.predict(Xte)):,.1f}")
```

**Expected output:** R² of exactly `1.0000` and an MAE of `0.0`. A flawless model. Let the room celebrate for about four seconds.

```python
# Why? Look at the coefficient it learnt.
for name, coef in zip(X_leaky.columns, leaky_model.coef_):
    print(f"{name:>18}: {coef:+,.2f}")
```

**Expected output:** the `maintenance_fee` coefficient is enormous (roughly 12.5, i.e. 1 / 0.08) and every other coefficient collapses towards zero. The model ignored area, bedrooms, age and the metro entirely. It found the shortcut and took it.

```python
# --- The fix: remove the leak, retrain, accept an honest score ---
X_clean = rents_v2.drop(columns=["rent", "maintenance_fee"])

Xtr, Xte, ytr, yte = train_test_split(X_clean, y, test_size=0.25, random_state=42)
honest_model = LinearRegression().fit(Xtr, ytr)

print(f"HONEST -> R2 : {honest_model.score(Xte, yte):.4f}")
print(f"HONEST -> MAE: Rs {mean_absolute_error(yte, honest_model.predict(Xte)):,.0f}")
```

**Expected output:** R² drops to roughly 0.9 and MAE rises to a few thousand rupees. **This is the better model.**

```python
# --- Now the second kind: preprocessing leakage ---
from sklearn.preprocessing import StandardScaler

wrong = StandardScaler().fit(X_clean)   # WRONG: fitted on ALL 24 rows
right = StandardScaler().fit(Xtr)       # RIGHT: fitted on the 18 TRAIN rows only

print("Mean used, fitted on ALL data  :", wrong.mean_.round(2))
print("Mean used, fitted on TRAIN only:", right.mean_.round(2))
```

**Expected output:** the two arrays of means differ. That difference *is* the leak — in the top row, six test flats helped decide how the training data was scaled.

**Live walk-through:** The emotional beat is the drop from 1.0000 to ~0.9. Say it plainly: *"We just made our model worse on purpose, and it is now a model I would actually deploy. The 1.00 model would predict nothing on a new flat, because you don't know its maintenance fee until you've already agreed the rent."*

Then ask: *"Where would a leak like this come from in a real company?"* Answer: joins. Someone merges a table that was populated *after* the outcome. It happens constantly.

---

## Concept Block 4: Reliable, Reproducible Data Prep (10 min)

### Reliability rule 1 — order of operations

```
   SPLIT  ->  then clean / impute / scale using TRAIN statistics only
   NOT: clean / scale  ->  then split
```

Every transformation that *learns something from the data* (a mean, a standard deviation, a category list) must learn it from the training set alone, then be **applied unchanged** to the test set.

| Transform | Learns from train | Applied to test |
|---|---|---|
| `StandardScaler` | mean, std | same mean, std |
| Fill nulls with median | the median | the *train* median |
| One-hot encode | the category list | the *train* category list |

### Reliability rule 2 — `fit` vs `transform`

```
scaler.fit_transform(X_train)   # LEARN the stats, then apply them
scaler.transform(X_test)        # APPLY the stats already learnt. Never fit again.
```

If you ever type `fit_transform(X_test)`, you have leaked. Full stop.

### Reliability rule 3 — `random_state`

`train_test_split` shuffles. Without a seed, you and your teammate get different splits, different scores, and an argument that cannot be resolved. **Set `random_state=42` everywhere randomness appears.** Same code, same answer, every run, on every machine.

### The Pipeline — reliability you cannot forget to apply

A **`Pipeline`** chains your transforms and your model into one object. Call `.fit()` and it fits every step in order, using only the data you handed it; call `.predict()` and it re-applies every step in order. You *cannot* accidentally scale with test statistics, because the pipeline never sees them.

*"A pipeline is not a convenience. It is a guardrail."*

---

## Practical Block 4: The End-to-End Pipeline on a Real Dataset (10 min)

Off the toy data and onto a real one that ships with sklearn — no download needed.

```python
from sklearn.datasets import load_diabetes
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

# Real medical dataset: 442 patients, 10 features, target = disease progression
X_d, y_d = load_diabetes(return_X_y=True, as_frame=True)
print("Features:", X_d.shape, "| Target:", y_d.shape)
print(X_d.columns.tolist())

# --- 1. SPLIT FIRST. Always. ---
Xd_train, Xd_test, yd_train, yd_test = train_test_split(
    X_d, y_d, test_size=0.2, random_state=42
)

# --- 2. Build the pipeline: scale, then model ---
pipe = Pipeline([
    ("scaler", StandardScaler()),      # learns mean/std from TRAIN only
    ("model",  LinearRegression()),
])

# --- 3. One fit call runs the whole chain ---
pipe.fit(Xd_train, yd_train)

# --- 4. One predict call re-applies the whole chain, correctly ---
preds = pipe.predict(Xd_test)

print(f"Test R2 : {pipe.score(Xd_test, yd_test):.3f}")
print(f"Test MAE: {mean_absolute_error(yd_test, preds):.1f}")
```

**Expected output:** a test R² somewhere around 0.4–0.5 and an MAE of roughly 40 on a target that ranges from about 25 to 346. Nowhere near perfect — and completely believable.

```python
# --- Prove reproducibility: same seed, same split, every time ---
for seed in [42, 42, 0]:
    a, b, c, d = train_test_split(X_d, y_d, test_size=0.2, random_state=seed)
    print(f"random_state={seed} -> first 5 test rows: {list(b.index[:5])}")
```

**Expected output:** the two `random_state=42` lines are identical; the `random_state=0` line is different. That is reproducibility, demonstrated in three lines.

**Live walk-through:** Contrast the R² of ~0.45 here against the 1.00 from the leaky rent model. *"Which of these two numbers came from a model you'd stake your job on?"*

Then finish on the pipeline: *"Everything you will build for the rest of this module goes inside one of these. It is not tidiness — it is the thing that stops you leaking without noticing."*

---

## Summary & Wrap-Up (5 min)

**The spine of today:**

1. **ML flips the arrows.** You give data + answers; the machine derives the rules.
2. **Supervised needs labels.** Number → regression. Category → classification.
3. **The lifecycle is nine steps** and `fit()` is only step 6. The work lives in steps 1–5.
4. **`X` is features, `y` is target.** Drop the target out of `X` or you have already lost.
5. **Split before you touch anything.** The test set is opened once, at the end.
6. **Leakage is the reliability threat.** A perfect score means you cheated somewhere.
7. **Pipeline + `random_state=42`** turn a correct workflow into a *repeatable* one.

**Bridge:** *"Today you learnt that a score of 1.00 means you cheated. Next session — **Avoiding ML Pitfalls & Model Generalization** — you'll meet the other way a model lies to you: overfitting. Our train R² today was higher than our test R². Next week you'll learn exactly how big that gap is allowed to get, and what to do when it's too big."*

---

## Q&A & Doubt Solving (5 min)

**Q: Why 75/25? Why not 50/50 or 90/10?**
→ It is a trade-off, not a law. More training data means a better model; more test data means a more reliable *estimate* of that model. 75/25 or 80/20 are the common defaults. With a very large dataset you can afford 95/5, because even 5% is thousands of rows. With only 24 rows, as today, every split is noisy — which is itself an honest lesson.

**Q: If I can't peek at the test set, how do I try different models?**
→ You carve a third slice out of the *training* data, called a validation set, and tune against that. Cross-validation is the systematic version of this idea. That is Session 2 and Session 12 — for today, one split, one look.

**Q: Is dropping the leaky column the only fix?**
→ It is the simplest and today's answer. Sometimes a column is only *partially* leaky — for example, a value that exists but is recorded late. The real fix there is to reconstruct the column as it would have looked at prediction time. When in doubt, drop it; a slightly weaker honest model beats a strong dishonest one every single time.

**Q: Why 42 specifically?**
→ Pure convention — a *Hitchhiker's Guide* joke that stuck. Any integer works. What matters is that you write *some* integer down and keep it fixed, so your results are reproducible.

**Q: My R² is negative. Is my code broken?**
→ Probably not. R² compares your model against the trivial baseline of always predicting the mean of `y`. A negative R² means your model is doing *worse* than that baseline — which happens with a tiny test set or badly chosen features. It is a real signal, not an error.

---

## Instructor Notes

- **Setup:** `pip install scikit-learn pandas numpy`. Nothing downloads at runtime — the rent data is inline and `load_diabetes` ships inside the sklearn package. Verify `import sklearn` works for everyone in the first five minutes; a broken install here derails the whole session.
- **Pacing:** Practical 2 is the emotional peak — protect the full 15 minutes. If you are running behind, trim the `StandardScaler` comparison at the end of Practical 3 and the reproducibility loop in Practical 4; both are worth cutting before anything else.
- **Scope discipline:** Do not mention overfitting/underfitting by name beyond a one-line teaser, do not mention cross-validation, and do not go near regularisation or classification metrics. Those are Sessions 2, 3 and 8. Today's only metrics are MAE and `.score()`.
- **The 24-row dataset is deliberately small.** Someone will notice the test set is only six flats. Praise them for it, and say the honest thing: with 6 test rows the score is unstable — re-run with `random_state=7` and it will move. That is not a bug; that is why real projects need real data.
- **The single most common student mistake:** calling `.fit()` on the full `X` and `y` instead of `X_train` / `y_train`, then evaluating on data the model already memorised. Pre-empt it by writing the rule on the board *before* Practical 2 and leaving it there all session: **"`fit` touches train. `predict` touches test. Nothing else."** Walk the room during Practical 2 and check that specific line in every notebook.
- **Second most common:** running `fit_transform` on the test set. Practical 3's scaler comparison exists to inoculate against exactly this — do not skip it unless you must.
