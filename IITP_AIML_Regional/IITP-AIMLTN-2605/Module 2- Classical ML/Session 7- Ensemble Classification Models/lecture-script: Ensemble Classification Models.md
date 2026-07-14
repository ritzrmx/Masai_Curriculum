# Lecture Script: Ensemble Classification Models
> **Instructor Reference** — Module 2: Classical ML | Session 7 | Duration: 2 Hours

---

## Session Overview

**Goal:** Students take a single overfitting decision tree from Session 6, watch it wobble, and then progressively beat it — first with a voting classifier, then with bagging, then with a Random Forest, and finally with gradient boosting. They finish with a leaderboard of five models on one dataset and can explain *why* each one improved on the last.

**Student profile at this point:** They can train and score `LogisticRegression`, `KNeighborsClassifier`, and `DecisionTreeClassifier` (Session 6). They know `train_test_split`, `accuracy_score`, and the bias–variance trade-off (Session 2). They have never used `sklearn.ensemble`. They do NOT yet know precision, recall, ROC-AUC, or thresholds — that is Session 8. Keep evaluation to accuracy plus a glance at the confusion matrix.

**Key outcome:** A single notebook containing a model leaderboard — single tree → voting → bagging → Random Forest → boosting — plus a feature importance bar chart they can explain to a non-technical stakeholder.

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| Opening — The Jar of Sweets | 5 min | 0:05 |
| **Concept 1:** Why One Deep Tree Cannot Be Trusted | 10 min | 0:15 |
| **Practical 1:** The wobbling tree + first voting ensemble | 15 min | 0:30 |
| **Concept 2:** Bagging — Bootstrap, Then Aggregate | 10 min | 0:40 |
| **Practical 2:** BaggingClassifier and the n_estimators curve | 15 min | 0:55 |
| **BREAK** | 10 min | 1:05 |
| **Concept 3:** Random Forest and Feature Importance | 10 min | 1:15 |
| **Practical 3:** Random Forest, its three knobs, importance plot | 15 min | 1:30 |
| **Concept 4:** Boosting — Sequential Error Correction | 10 min | 1:40 |
| **Practical 4:** Gradient boosting and the final leaderboard | 10 min | 1:50 |
| Summary & Wrap-Up | 5 min | 1:55 |
| Q&A & Doubt Solving | 5 min | 2:00 |

---

## Opening (5 min)

**Hook — run this live, do not skip it.** Put a photo of a jar of sweets on screen (or hold up an actual jar). Ask every student to type one guess into the chat for how many are inside. Collect all the guesses, then compute the mean on screen.

Almost every time, the *average of the whole room* lands closer to the true count than the vast majority of individual guesses — often closer than the single best guesser. Individual errors point in every direction and cancel; the collective signal survives.

*"So here is my question. Last week you each built one carefully tuned decision tree. What if the better move was never to build one great model — but to build a hundred mediocre ones and let them vote?"*

**What an ensemble is NOT:**
- A single, bigger, deeper model
- A way to fix bad data or bad features
- Magic — if all your models make the *same* mistake, averaging them changes nothing
- Guaranteed to beat a well-tuned single model on every dataset

**What an ensemble IS:**
- Many models, deliberately made *different* from one another, whose predictions are pooled
- The single most reliable accuracy upgrade available on tabular data
- The reason Random Forest and XGBoost dominate real-world ML on spreadsheets
- A direct, targeted attack on the bias–variance trade-off from Session 2

---

## Concept Block 1: Why One Deep Tree Cannot Be Trusted (10 min)

### Write this on the board

```
TOTAL ERROR  =  BIAS²  +  VARIANCE  +  irreducible noise

BIAS     = how wrong the model is ON AVERAGE
           (too simple → underfits)

VARIANCE = how much the model CHANGES when the
           training data changes slightly
           (too complex → overfits)
```

Now place last week's decision tree on that map.

A decision tree grown with no `max_depth` keeps splitting until every leaf is pure. Training accuracy: 1.00. Every single time. It has *memorised* the rows.

**The critical property: a deep tree is LOW BIAS but HIGH VARIANCE.** On average it aims at the right answer. But move ten rows in or out of the training set and you get a structurally different tree with different predictions.

### The board diagram — where each model sits

| Model | Bias | Variance | Symptom |
|---|---|---|---|
| Logistic regression | High | Low | Underfits curvy boundaries |
| Shallow tree, `max_depth=2` | High | Low | Boundary too blocky |
| **Deep tree, no limit** | **Low** | **HIGH** | Train 1.00, test wobbles |
| KNN with `k=1` | Low | High | Memorises neighbours |

### The strategy that follows

If a deep tree is *unbiased but noisy*, then you do not need a smarter tree. You need **many noisy trees whose noise cancels out**. That is the whole idea of this session.

> **The one rule:** ensembling only works if the members make *different* mistakes. Say this three times today. Every technique that follows — bootstrapping, feature subsampling, using different model types — exists purely to manufacture that difference.

### The simplest ensemble: the Voting Classifier

Take three models that are *already different by nature* — a linear one, a distance-based one, a rule-based one — and pool their answers.

| | **Hard voting** | **Soft voting** |
|---|---|---|
| Combines | Predicted labels | Predicted probabilities |
| Rule | Majority wins | Highest average probability wins |
| Requires | `predict` | `predict_proba` |
| Character | Blunt, robust | Confidence-aware, usually better |

---

## Practical Block 1: The Wobbling Tree + First Ensemble (15 min)

```python
import numpy as np
import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

data = load_breast_cancer(as_frame=True)
X, y = data.data, data.target          # 569 rows, 30 numeric features
print("Shape:", X.shape)
print("Class balance:\n", y.value_counts())

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

# --- The single deep tree from Session 6 ---
tree = DecisionTreeClassifier(random_state=42).fit(X_train, y_train)
print("Deep tree  train acc:", round(tree.score(X_train, y_train), 3))
print("Deep tree  test  acc:", round(tree.score(X_test, y_test), 3))
```

Train accuracy will print as exactly `1.0`. Test accuracy will land somewhere in the low 0.90s. **Pause here.** That gap is the whole session in one line of output.

```python
# --- Demonstrate VARIANCE: same model, slightly different data ---
rng = np.random.RandomState(42)
scores = []
for seed in range(5):
    idx = rng.choice(len(X_train), size=len(X_train), replace=True)   # a bootstrap sample
    t = DecisionTreeClassifier(random_state=seed).fit(X_train.iloc[idx], y_train.iloc[idx])
    scores.append(accuracy_score(y_test, t.predict(X_test)))

print("Five deep trees, five resamples:", [round(s, 3) for s in scores])
print("Spread (max - min):", round(max(scores) - min(scores), 3))
print("Mean of the five   :", round(np.mean(scores), 3))
```

Expect five different test accuracies with a spread of roughly 5 percentage points, all from *the same algorithm on the same data*. That spread **is** variance — you are watching it happen.

```python
# --- The simplest ensemble: pool three DIFFERENT models ---
from sklearn.ensemble import VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

members = [
    ("logreg", make_pipeline(StandardScaler(), LogisticRegression(max_iter=5000, random_state=42))),
    ("knn",    make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=5))),
    ("tree",   DecisionTreeClassifier(max_depth=4, random_state=42)),
]

for name, model in members:
    model.fit(X_train, y_train)
    print(f"{name:8s} alone : {model.score(X_test, y_test):.3f}")

hard = VotingClassifier(members, voting="hard").fit(X_train, y_train)
soft = VotingClassifier(members, voting="soft").fit(X_train, y_train)
print("Hard voting     :", round(hard.score(X_test, y_test), 3))
print("Soft voting     :", round(soft.score(X_test, y_test), 3))
```

**Live walk-through — and be honest here, it is the best moment in the block.** The voting ensemble comfortably beats the *tree*, but on this particular dataset the plain logistic regression alone is likely to beat the ensemble outright. **Do not hide this. Teach it.**

Breast cancer data is very nearly linearly separable, so logistic regression is close to optimal — and pooling it with two weaker members *drags it down*. This is exactly the "What an ensemble is NOT" bullet from the opening, arriving live on screen: **an ensemble is not automatically better than its best member.** Voting helps when the members are of *comparable* strength and make *different* mistakes. It hurts when you dilute one excellent model with mediocre ones.

Point out the `make_pipeline(StandardScaler(), ...)` wrappers too: logistic regression and KNN care about scale, the tree does not, and pipelines give each member exactly what it needs. Then ask the room: *"Hard and soft voting can disagree on this dataset. What extra information does soft voting have that hard voting throws away — and why might that extra information still not save us here?"*

---

## Concept Block 2: Bagging — Bootstrap, Then Aggregate (10 min)

### The name is the algorithm

**B**ootstrap **AGG**regat**ING**. Two steps, both in the name.

```
STEP 1 — BOOTSTRAP
  From your N training rows, draw N rows WITH REPLACEMENT.
  Some rows appear twice. Some never appear at all.
  (~63% of unique rows show up; ~37% are left out — "out-of-bag")
  Do this B times → B different training sets.

STEP 2 — AGGREGATE
  Train one deep tree on each bootstrap sample → B trees.
  Classification → majority vote.
  Regression      → average.
```

### Why averaging kills variance — the board argument

Ask the room: *"If I measure your height once with a shaky tape, I might be off by 3 cm. If I measure ten times and average, how far off am I?"*

The statistical result: averaging `n` independent noisy estimates shrinks the noise by roughly `√n`.

```
variance of one tree      = V
variance of B averaged
trees, if independent     = V / B
```

Four trees, half the noise. A hundred trees, a tenth of it. **But** the trees are *not* fully independent — they all come from the same underlying dataset, so they are correlated, and the real reduction is smaller than the formula promises. Hold that thought; Concept 3 is entirely about fixing it.

### What bagging does and does not fix

| | Effect of bagging |
|---|---|
| **Variance** | Falls sharply — this is the whole point |
| **Bias** | Essentially unchanged |
| **Train accuracy** | Still near 1.00 — don't panic |
| **Test accuracy** | Rises, and *stops jumping around* |
| **Cost** | `n_estimators` times slower to train |

> **Say this out loud:** "Bagging fixes wobble, not blindness. If all your trees are wrong in the same direction, averaging them keeps them wrong."

---

## Practical Block 2: BaggingClassifier and the n_estimators Curve (15 min)

```python
from sklearn.ensemble import BaggingClassifier

bag = BaggingClassifier(
    estimator=DecisionTreeClassifier(random_state=42),  # the SAME deep tree as before
    n_estimators=100,
    bootstrap=True,          # this is the "bootstrap" in bagging
    random_state=42,
    n_jobs=-1                # trees are independent → train them in parallel
)
bag.fit(X_train, y_train)

print("Single deep tree :", round(tree.score(X_test, y_test), 3))
print("100 bagged trees :", round(bag.score(X_test, y_test), 3))
print("Bagged train acc :", round(bag.score(X_train, y_train), 3))
```

The bagged score should land a few points above the single tree. Train accuracy stays at or very near 1.00 — **call this out explicitly**, because students will read it as "still overfitting" and panic. It is not overfitting; each individual tree memorises, but the *vote* generalises.

```python
# --- How many trees do we actually need? ---
import matplotlib.pyplot as plt

sizes = [1, 2, 5, 10, 25, 50, 100, 200]
accs = []
for n in sizes:
    b = BaggingClassifier(
        estimator=DecisionTreeClassifier(random_state=42),
        n_estimators=n, random_state=42, n_jobs=-1
    ).fit(X_train, y_train)
    accs.append(b.score(X_test, y_test))

plt.figure(figsize=(7, 4))
plt.plot(sizes, accs, "o-", color="teal", lw=2)
plt.axhline(tree.score(X_test, y_test), color="crimson", ls="--",
            label="Single deep tree")
plt.xlabel("Number of trees in the bag")
plt.ylabel("Test accuracy")
plt.title("Bagging: accuracy climbs, then plateaus — it never collapses")
plt.legend()
plt.tight_layout()
plt.show()
```

**Live walk-through:** The curve rises steeply from 1 to about 25 trees, then flattens. Trace the plateau with your finger and make the point that *matters most today*: **the curve flattens, it does not turn downward.** Adding trees to a bag can never make it overfit — it can only waste your CPU. Contrast this now, verbally, with boosting, where more trees eventually *does* hurt. Then ask: *"If more trees are always safe, why not use 10,000?"* (Answer: training and prediction time, and zero accuracy gain past the plateau.)

---

## BREAK (10 min)

*Before you go: bagging gives every tree all 30 columns to choose from. If one column is far stronger than the rest, what will every single tree split on first — and what does that do to the "make different mistakes" rule?*

---

## Concept Block 3: Random Forest and Feature Importance (10 min)

### The problem the break question exposed

In plain bagging, every tree can see every column. In the breast cancer data, `worst_perimeter` is enormously predictive. So tree 1 splits on it first. And tree 2. And tree 87. The trees end up structurally near-identical, they make **the same mistakes**, and averaging them recovers far less variance than the `V/B` formula promised.

**Correlated trees are barely better than one tree.**

### The Random Forest fix — one extra line of randomness

```
Random Forest = Bagging  +  at EVERY split, each tree may only
                            consider a RANDOM SUBSET of features
```

That is the entire difference. At each node, the tree picks `max_features` columns at random (`sqrt(30) ≈ 5` by default for classification) and finds the best split *among those five only*. A different five at the next node.

The dominant column is simply *absent* from many splits. Weaker-but-useful columns finally get a turn. The trees **decorrelate** — and now averaging does its full job.

### The three knobs

| Knob | Meaning | Start with | If you increase it |
|---|---|---|---|
| `n_estimators` | Number of trees | 100–500 | Safer, slower, never overfits |
| `max_depth` | Depth cap per tree | `None` | More variance per tree; the forest absorbs it |
| `max_features` | Columns offered per split | `"sqrt"` | Trees get more correlated — less decorrelation benefit |

### Feature importance

Every split records how much it improved leaf purity. Average that gain across all trees and all splits, normalise to sum to 1.0 — that is `rf.feature_importances_`.

**Board warning, in capitals:** **IMPORTANCE IS NOT CAUSATION.** A feature can rank high because it is *correlated* with the true driver, not because it drives anything. It tells you what the model leaned on. It does not tell you what the world does. It also quietly *inflates* high-cardinality and continuous columns.

---

## Practical Block 3: Random Forest, Its Knobs, and Importance (15 min)

```python
from sklearn.ensemble import RandomForestClassifier

rf = RandomForestClassifier(
    n_estimators=300,
    max_depth=None,        # let each tree grow fully — the forest handles it
    max_features="sqrt",   # THE line that makes it a forest, not just a bag
    random_state=42,
    n_jobs=-1
)
rf.fit(X_train, y_train)

print("Single tree   :", round(tree.score(X_test, y_test), 3))
print("Bagging (100) :", round(bag.score(X_test, y_test), 3))
print("Random Forest :", round(rf.score(X_test, y_test), 3))
```

```python
# --- Does max_features actually matter? Prove it. ---
for mf in ["sqrt", "log2", 0.5, None]:      # None = use ALL features = plain bagging
    m = RandomForestClassifier(n_estimators=300, max_features=mf,
                               random_state=42, n_jobs=-1).fit(X_train, y_train)
    label = "all (= bagging)" if mf is None else str(mf)
    print(f"max_features={label:16s} test acc: {m.score(X_test, y_test):.3f}")
```

```python
# --- Ask the forest what it leaned on ---
importances = pd.Series(rf.feature_importances_, index=X.columns).sort_values()

plt.figure(figsize=(8, 7))
importances.tail(12).plot(kind="barh", color="seagreen")
plt.xlabel("Mean decrease in impurity (importances sum to 1.0)")
plt.title("Random Forest — Top 12 Features")
plt.tight_layout()
plt.show()

print(importances.tail(5).round(3))
print("Sum of all importances:", round(importances.sum(), 3))   # 1.0
```

**Live walk-through:** Three things to call out, in this order.

1. The `max_features` sweep shows `None` (plain bagging) is usually the *weakest* setting. That is the decorrelation argument, proven on screen — not on a slide.
2. The importance bars are dominated by a handful of "worst_*" columns. Note aloud that several of these are near-duplicates of each other, so the importance is being *split* between them — a column can look weak simply because its twin stole the credit.
3. Print the sum: exactly 1.0. Importances are shares of a fixed pie, not standalone scores.

*Ask the room:* "This forest says `worst_perimeter` matters most. Can I now tell an oncologist that perimeter **causes** malignancy?"

---

## Concept Block 4: Boosting — Sequential Error Correction (10 min)

### A completely different philosophy

Bagging builds trees **in parallel**, each blind to the others, and averages away their noise.
Boosting builds trees **one at a time**, each one *looking at what the previous ones got wrong* and specialising in exactly those rows.

```
Tree 1  → trained on the data.        Makes errors.
Tree 2  → trained on TREE 1's ERRORS. Fixes some. Leaves new ones.
Tree 3  → trained on the errors that remain.
...
Final prediction = Tree1 + lr·Tree2 + lr·Tree3 + ...
```

`lr` is the **learning rate**: how big a bite each new tree is allowed to take out of the remaining error. Small `learning_rate` = cautious steps = needs more trees = usually more accurate.

### Weak learners, on purpose

Boosting deliberately uses **shallow** trees — `max_depth=3` is typical. A single one is barely better than a coin flip. That is fine: it is a *specialist*, not a soloist. Its job is to fix one slice of error, not to be right on its own.

Because each tree corrects a systematic error, boosting attacks **BIAS** — the other half of the Session 2 trade-off.

### The comparison table — put this on the board and leave it there

| | **Bagging / Random Forest** | **Boosting** |
|---|---|---|
| Trees are built | In **parallel**, independently | **Sequentially**, each fixing the last |
| Primarily reduces | **Variance** | **Bias** |
| Base learner | Deep, strong trees | Shallow, weak trees |
| More trees | Never hurts — just slower | **Can overfit** |
| Tuning | Forgiving, works out of the box | Sensitive — `learning_rate` is critical |
| Parallelisable | Yes, fully | No — trees depend on each other |
| Use it when | You want a strong, safe default | You need the last 2% of accuracy |

### The names they will meet in industry

`GradientBoostingClassifier` is scikit-learn's classic implementation — correct, but slow on large data. `HistGradientBoostingClassifier` bins the features into histograms first and is dramatically faster; it is inspired by LightGBM. Outside scikit-learn, **XGBoost** and **LightGBM** are the two libraries that win most tabular Kaggle competitions and run in production at scale. The *ideas* are identical to what we just covered — the engineering is what differs.

---

## Practical Block 4: Boosting and the Final Leaderboard (10 min)

```python
from sklearn.ensemble import GradientBoostingClassifier, HistGradientBoostingClassifier

gb = GradientBoostingClassifier(
    n_estimators=100,
    learning_rate=0.1,
    max_depth=3,          # deliberately WEAK trees
    random_state=42
).fit(X_train, y_train)

hgb = HistGradientBoostingClassifier(random_state=42).fit(X_train, y_train)

print("Gradient Boosting     :", round(gb.score(X_test, y_test), 3))
print("Hist Gradient Boosting:", round(hgb.score(X_test, y_test), 3))
```

```python
# --- THE money demo: more trees. Boosting CAN overfit. A forest cannot. ---
# Use a deliberately NOISY dataset so the effect is visible.
from sklearn.datasets import make_classification

Xn, yn = make_classification(n_samples=600, n_features=10, n_informative=4,
                             n_redundant=2, flip_y=0.25,   # 25% of labels are wrong on purpose
                             random_state=42)
Xn_tr, Xn_te, yn_tr, yn_te = train_test_split(Xn, yn, test_size=0.3,
                                              random_state=42, stratify=yn)

print("BOOSTING — learning_rate=0.5, adding trees:")
for n in [10, 50, 100, 300, 600, 1000]:
    m = GradientBoostingClassifier(n_estimators=n, learning_rate=0.5,
                                   max_depth=3, random_state=42).fit(Xn_tr, yn_tr)
    print(f"  n_estimators={n:<5} train: {m.score(Xn_tr, yn_tr):.3f}"
          f"  test: {m.score(Xn_te, yn_te):.3f}")

print("\nRANDOM FOREST — same data, adding trees:")
for n in [10, 50, 100, 300, 600, 1000]:
    m = RandomForestClassifier(n_estimators=n, random_state=42,
                               n_jobs=-1).fit(Xn_tr, yn_tr)
    print(f"  n_estimators={n:<5} train: {m.score(Xn_tr, yn_tr):.3f}"
          f"  test: {m.score(Xn_te, yn_te):.3f}")
```

**This is the single most important output of the session.** The boosting test accuracy *peaks early and then falls* as trees are added — it is dutifully fitting the 25% of labels we corrupted, because corrupted labels are exactly "what the previous trees got wrong". The forest's test accuracy climbs and then holds flat, and never turns down.

Put the two columns side by side on screen: **sequential ensembles can overfit with more members; parallel ensembles cannot.** Lower `learning_rate` (try 0.05) makes boosting take smaller, more cautious steps and delays the collapse — that is what the knob is *for*.

```python
# --- The leaderboard ---
leaderboard = pd.DataFrame({
    "model": ["Single deep tree", "Soft voting (3 models)", "Bagging (100 trees)",
              "Random Forest (300)", "Gradient Boosting", "HistGradientBoosting"],
    "test_accuracy": [tree.score(X_test, y_test), soft.score(X_test, y_test),
                      bag.score(X_test, y_test), rf.score(X_test, y_test),
                      gb.score(X_test, y_test), hgb.score(X_test, y_test)],
}).sort_values("test_accuracy", ascending=False).round(3)
print(leaderboard.to_string(index=False))
```

```python
# --- One glance at WHERE the best model errs (full treatment: Session 8) ---
from sklearn.metrics import confusion_matrix

cm = confusion_matrix(y_test, rf.predict(X_test))
print("Confusion matrix (rows = true, cols = predicted):")
print(cm)
print("\nAccuracy hides something: which kind of mistake is worse here —")
print("calling a malignant tumour benign, or a benign tumour malignant?")
```

**Live walk-through:** The leaderboard should climb monotonically-ish from the single tree to the ensembles, though the exact ordering of the top three will shuffle by a row or two — say so honestly, and use it: *"The gaps at the top are one or two test rows. Do not over-read them."* Finish on the confusion matrix. Do **not** teach precision and recall — just show that the two off-diagonal cells are not equally bad, and leave the room hungry for Session 8.

---

## Summary & Wrap-Up (5 min)

**The spine of today, in five steps:**

1. **A deep decision tree is low-bias but high-variance** — it memorises, and its test score wobbles by several points depending on which rows it saw.
2. **An ensemble pools many models.** It only works if the members make *different* mistakes. A `VotingClassifier` is the simplest version: pool a logistic regression, a KNN, and a tree.
3. **Bagging = bootstrap + aggregate.** Train many deep trees on many resamples and take the majority vote. Random errors cancel. **Variance falls; bias does not.** More trees are always safe.
4. **Random Forest = bagging + random feature subsets at every split.** This *decorrelates* the trees so averaging works properly. Three knobs: `n_estimators`, `max_depth`, `max_features`. Read its `feature_importances_` — but never call it causation.
5. **Boosting = sequential weak trees, each fixing the last one's errors.** This cuts **bias**. It is more accurate and more fragile: `learning_rate` matters, and too many trees *will* overfit. `HistGradientBoosting` in sklearn; XGBoost and LightGBM in industry.

**Bridge:** *"Every model today was judged on one number: accuracy. Next session — **Classification Metrics & Threshold Analysis** — you will see why that number can be a lie. A model that predicts 'no cancer' for every single patient can score 95% accuracy on an imbalanced dataset. You will learn precision, recall, F1, ROC-AUC, and how moving one threshold changes everything."*

---

## Q&A & Doubt Solving (5 min)

**Q: My Random Forest still shows 100% training accuracy. Isn't that overfitting?**
→ No, and this trips up almost everyone. Each individual tree in the forest *does* memorise its bootstrap sample — that is by design. What matters is the *test* score and its *stability*. If train is 1.00 and test is 0.96 and stays at 0.96 across different splits, you have a healthy forest. Judge a forest by test performance, never by the train/test gap alone.

**Q: If more trees never hurt a Random Forest, why not set `n_estimators=5000`?**
→ Because the accuracy curve plateaus, usually around 100–300 trees, and everything past that plateau is pure cost. Training time and prediction time grow linearly with the number of trees. In production, prediction latency is often the binding constraint — a 5000-tree forest can be too slow to serve.

**Q: When would boosting actually lose to a Random Forest?**
→ Three common cases. On very noisy data, boosting chases the noise — it is literally trained to fit what previous models got wrong, and noise *is* what they got wrong. On small datasets, it overfits quickly. And when you have no time to tune: an untuned Random Forest is usually excellent, while an untuned boosting model can be mediocre or worse.

**Q: Can I bag models other than trees — say, logistic regressions?**
→ Yes, `BaggingClassifier(estimator=LogisticRegression())` runs fine. But it will barely help. Bagging reduces variance, and logistic regression is already a low-variance, high-bias model — there is almost no variance left to remove. Bagging pays off exactly when the base model is *unstable*, which is why deep trees are the classic pairing.

**Q: A feature scored 0.00 importance. Can I delete that column?**
→ Be careful. A zero can mean "genuinely useless" or it can mean "perfectly correlated with another column that grabbed all the credit first". Drop it, retrain, and check whether accuracy actually holds. Importance is a description of *this fitted model's behaviour*, not a verdict on the column itself.

---

## Instructor Notes

- **Zero installs, zero downloads.** Everything runs on `load_breast_cancer` from `sklearn.datasets` plus matplotlib. Nothing depends on a network. If you want a second dataset for the practice loop, `make_classification(n_samples=400, n_features=6, n_informative=3, random_state=42)` gives a clean forest-vs-tree gap in seconds.
- **Set `n_jobs=-1`** on every bagging and forest call, and say why: the trees are genuinely independent, so they train in parallel. Then point out that `GradientBoostingClassifier` has no `n_jobs` parameter *at all* — it cannot parallelise, because tree `k` needs tree `k-1` to exist first. That single missing parameter teaches the parallel-vs-sequential distinction better than any slide.
- **Do not fix the numbers to the decimal.** Accuracies on this dataset land in the 0.92–0.97 band and will shuffle slightly with the sklearn version. Say the band out loud, and treat any 0.005 difference as noise, not as a result. This is good modelling hygiene and students copy it.
- **Pacing:** Practical 2's `n_estimators` loop and Practical 3's `max_features` sweep each fit several models. On a slow laptop, cut `n_estimators` from 300 to 100 in Practical 3 — the qualitative story is unchanged. If you are behind in Practical 4, drop the leaderboard and the confusion matrix, but **never** drop the noisy-data boosting-vs-forest comparison. That is the payoff of the whole session; the 1000-tree boosting fits are the slow part, so trim that list to `[10, 100, 600]` rather than skipping it.

- **On the honest results:** two outputs will look "wrong" and both are teaching gold. (1) In Practical 1, logistic regression alone beats the voting ensemble — the data is nearly linearly separable. Use it to kill the "ensembles always win" myth on the spot. (2) In Practical 4, the *clean* breast cancer data will NOT show boosting overfitting, which is exactly why the demo switches to a noisy `make_classification` set. Say plainly that you had to add noise to expose the failure mode. Students trust a course that shows a technique failing.
- **The single most common student mistake:** treating "more trees" as a universal overfitting risk, and therefore keeping `n_estimators` tiny "to be safe". Pre-empt it in Practical 2 by physically tracing the plateau on the plot, and again in Practical 4 by showing that boosting is the *one* place where more trees genuinely can hurt. The distinction — parallel ensembles cannot overfit with more members, sequential ones can — is the sharpest idea in this session.
- **Hold the line on metrics.** Students who have read ahead will ask about precision, recall, and ROC-AUC. Acknowledge the question, write the word "Session 8" on the board, and move on. Today is about *models*; next week is about *judging* them.
