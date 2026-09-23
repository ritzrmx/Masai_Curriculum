# Lecture Script: Decision Trees
> **Instructor Reference** — Module 2: Classical ML | Session 9 | Duration: 2 Hours

---

## Session Overview

**Goal:** Students train a `DecisionTreeClassifier` in scikit-learn, visualize it with `plot_tree`, trace a single prediction's root-to-leaf path in plain language, and diagnose overfitting by comparing train vs. test accuracy across depth values.

**Student profile at this point:** Comfortable with the full supervised-learning workflow (split, fit, predict, evaluate) from Sessions 4-7, and with classification metrics (accuracy, precision, recall, F1) from Session 7. This is their first tree-based model — a different "shape" of algorithm than the linear models seen so far.

**Key outcome:** Every student trains a tree on `customer_churn.csv`, visualizes it, reads and explains at least one full root-to-leaf path in a plain-English sentence a non-technical manager could understand, and correctly diagnoses overfitting using a depth sweep.

**Dataset for this session:** `customer_churn.csv` (in this folder) — 36 rows of `age`, `monthly_spend`, `tenure_months`, `support_tickets`, `contract_type`, `used_mobile_app`, and target `churned` (0 = stayed, 1 = churned).

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| SEGMENT 1: Opening — Why a New Kind of Model | 10 min | 0:10 |
| SEGMENT 2: Fit/Predict with DecisionTreeClassifier | 20 min | 0:30 |
| SEGMENT 3: Visualizing the Tree with plot_tree | 20 min | 0:50 |
| **BREAK** | 10 min | 1:00 |
| SEGMENT 4: Reading a Root-to-Leaf Path | 20 min | 1:20 |
| SEGMENT 5: Overfitting — Depth vs. Accuracy | 20 min | 1:40 |
| SEGMENT 6: Lab — Full Workflow on customer_churn.csv | 15 min | 1:55 |
| SEGMENT 7: Summary, Wrap-Up & Q&A | 5 min | 2:00 |

---

## SEGMENT 1: Opening — Why a New Kind of Model (10 min)

### From Lines to Flowcharts (6 min)

**Say:** *"Every model we've trained so far — Linear Regression, Ridge, Lasso, Logistic Regression — has been fundamentally the same SHAPE underneath: a weighted sum of features, `w1*x1 + w2*x2 + ... + b`. Today we train something structurally completely different: a flowchart of yes/no questions. No weights, no coefficients, no straight lines at all."*

**Live-code this quick contrast on the projector:**

```python
# What every model so far has looked like, underneath:
# prediction = w1*feature1 + w2*feature2 + ... + b   (a straight line / plane)

# What a decision tree looks like, underneath:
# if feature1 <= threshold:
#     if feature2 <= another_threshold:
#         predict class A
#     else:
#         predict class B
# else:
#     predict class C
```

**Say:** *"This matters for two reasons. First, a decision tree can capture relationships a straight line simply cannot — sharp cutoffs, interactions between features, non-linear patterns — without us hand-engineering polynomial features like we did back in Session 4's overfitting demo. Second, and just as important for real projects: a tree is one of the most directly EXPLAINABLE models that exists. You can literally trace a single prediction, step by step, and hand that trace to a business stakeholder with zero statistics background."*

### Setting Expectations for Today (4 min)

**Say:** *"By the end of today you'll be able to do four things: train a `DecisionTreeClassifier`, visualize its full structure, explain any single prediction as a plain-English root-to-leaf story, and diagnose whether a given tree is overfit just by looking at how its depth was chosen. That third skill — explaining a prediction path — is one you'll use constantly in real projects, because 'the model said so' is never an acceptable answer to a stakeholder, but 'the model saw this customer is on a Monthly contract, doesn't use the app, and spends under ₹644/month, and that combination made them a high churn risk' absolutely is."*

**Learning contract for today — write on board:**

- Fit and predict with `DecisionTreeClassifier`
- Visualize a tree with `plot_tree` and `export_text`
- Trace and explain a root-to-leaf decision path
- Diagnose overfitting by comparing train vs. test accuracy across `max_depth`

---

## SEGMENT 2: Fit/Predict with DecisionTreeClassifier (20 min)

### Loading and Exploring the Data (6 min)

**Say:** *"Let's load `customer_churn.csv`, right here in this session's folder. This is a telecom-style dataset: 36 customers, a mix of numeric features and two categorical features, and a `churned` target — did this customer leave (1) or stay (0)?"*

**Live-code, step by step:**

```python
import pandas as pd

df = pd.read_csv("customer_churn.csv")
print(df.head())
print(df.shape)
print(df["churned"].value_counts())
```

**Run it.** Expected output:

```
   customer_id  age  monthly_spend  tenure_months  support_tickets contract_type used_mobile_app  churned
0         5001   36            839             41                0       Monthly             Yes        0
1         5002   24           1599             48                8       Monthly             Yes        1
2         5003   54            737             14                0       Monthly              No        1
3         5004   29           1836             38                0        Annual              No        0
4         5005   25            504             18                5       Monthly             Yes        1

(36, 8)
churned
0    18
1    18
Name: count, dtype: int64
```

**Say:** *"Notice the target is perfectly balanced — 18 churned, 18 stayed. That's convenient for today's focus on tree mechanics; real churn data is rarely this balanced, and Session 7's precision/recall/F1 toolkit is exactly what you'd reach for when it isn't."*

**Ask:** *"We have two categorical columns here — `contract_type` and `used_mobile_app`. From Session 2, what do we need to do to these before a scikit-learn model can use them?"* (Answer: encode them — e.g. one-hot encoding — since scikit-learn models require numeric input.)

### Building the Preprocessing + Tree Pipeline (8 min)

**Say:** *"Let's build this the right way, with a `ColumnTransformer` inside a `Pipeline`, exactly like Session 2's workflow — encode the two categorical columns, pass the numeric columns through unchanged, and feed everything into a `DecisionTreeClassifier`."*

**Live-code:**

```python
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

X = df[["age", "monthly_spend", "tenure_months", "support_tickets",
        "contract_type", "used_mobile_app"]]
y = df["churned"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

cat_cols = ["contract_type", "used_mobile_app"]

preprocess = ColumnTransformer([
    ("cat", OneHotEncoder(drop="if_binary"), cat_cols),
], remainder="passthrough")

tree_pipe = Pipeline(steps=[
    ("pre", preprocess),
    ("model", DecisionTreeClassifier(max_depth=3, random_state=42)),
])
tree_pipe.fit(X_train, y_train)

print("Train accuracy:", tree_pipe.score(X_train, y_train))
print("Test accuracy: ", tree_pipe.score(X_test, y_test))
```

**Run it.** Expected output:

```
Train accuracy: 0.9629629629629629
Test accuracy:  0.7777777777777778
```

**Say:** *"Two new things versus Sessions 4-7: `drop='if_binary'` on the encoder — since both categorical columns here have exactly two categories, we only need ONE column per feature to represent them fully, avoiding redundant columns. And `stratify=y` — we used this back in Session 1 for classification targets, and we're using it again here for the same reason: it keeps the churned/stayed ratio consistent between train and test."*

### Note on `max_depth=3` (2 min)

**Say:** *"I picked `max_depth=3` here somewhat arbitrarily, just to get us a first working tree. In SEGMENT 5, we'll systematically sweep through DIFFERENT depth values and let the train/test gap tell us which depth is actually justified — don't treat 3 as a magic number yet."*

### Comprehension Check (4 min)

1. *"Why did we use `stratify=y` here, given `churned` is a classification target?"* (Preserves the class balance between train and test, same reasoning as Session 1.)
2. *"What does `drop='if_binary'` do, and why is it safe here specifically?"* (Drops one of the two dummy columns for any feature with exactly two categories, since the dropped category is fully implied by the other column being 0 — safe here because both `contract_type` and `used_mobile_app` happen to have exactly two categories in this dataset.)

---

## SEGMENT 3: Visualizing the Tree with plot_tree (20 min)

### Drawing the Tree (8 min)

**Say:** *"Now the moment that makes trees special among everything we've trained this module: we can literally draw the entire decision-making process."*

**Live-code:**

```python
from sklearn.tree import plot_tree
import matplotlib.pyplot as plt

feature_names = tree_pipe.named_steps["pre"].get_feature_names_out()
tree_model = tree_pipe.named_steps["model"]

plt.figure(figsize=(16, 9))
plot_tree(
    tree_model,
    feature_names=feature_names,
    class_names=["Stay", "Churn"],
    filled=True,
    rounded=True,
)
plt.show()
```

**Run it and walk the class through the rendered figure.** **Say:** *"Every box is a node. The top box is the ROOT — the single most useful question the tree found, out of every feature and every possible threshold, for separating churners from stayers. `filled=True` colors each box by its majority class, so at a glance, orange-ish boxes lean 'Churn' and blue-ish boxes lean 'Stay' — the darker the shade, the purer that node."*

### Reading `export_text` as a Lighter-Weight Alternative (7 min)

**Say:** *"`plot_tree` is great on a screen, but you can't paste it into a Slack message or a text report easily. `export_text` gives you the exact same structure as plain text."*

**Live-code:**

```python
from sklearn.tree import export_text

tree_rules = export_text(tree_model, feature_names=list(feature_names))
print(tree_rules)
print("Tree depth:", tree_model.get_depth())
print("Number of leaves:", tree_model.get_n_leaves())
```

**Run it.** Expected output:

```
|--- cat__contract_type_Monthly <= 0.50
|   |--- class: 0
|--- cat__contract_type_Monthly >  0.50
|   |--- cat__used_mobile_app_Yes <= 0.50
|   |   |--- class: 1
|   |--- cat__used_mobile_app_Yes >  0.50
|   |   |--- remainder__monthly_spend <= 644.00
|   |   |   |--- class: 1
|   |   |--- remainder__monthly_spend >  644.00
|   |   |   |--- class: 0

Tree depth: 3
Number of leaves: 4
```

**Say:** *"Same information, zero graphics needed. Notice the feature names carry the `cat__` and `remainder__` prefixes — that's the `ColumnTransformer` labeling which branch of the preprocessing pipeline each column came from, exactly like we saw with `get_feature_names_out()` back in Session 2."*

### What Gini Impurity Is Doing, Intuitively (5 min)

**Say:** *"You'll see `gini=...` inside every box in the `plot_tree` figure. Here's the one-sentence intuition, no formula required: Gini impurity measures how 'mixed up' the classes are in a node. A node with all-churn or all-stay customers has Gini 0 — perfectly pure. A node split exactly 50/50 has the highest possible Gini for a two-class problem. At every step, the tree tries every feature and every possible threshold, and picks whichever split reduces Gini impurity the MOST — in other words, whichever question does the best job of separating churners from stayers."*

**Ask:** *"If a node has `value = [18, 0]` — 18 stayed, 0 churned — what would its Gini impurity be, roughly, without computing the formula?"* (Zero, or very close to it — the node is already pure, all one class.)

---

## BREAK (10 min)

*Suggested break prompt:* Ask students to look again at the root split (`contract_type_Monthly`) and guess, before returning, WHY a business would expect contract type to be the single most useful churn predictor out of all six features available. Come back ready to compare guesses to the real reasoning.

---

## SEGMENT 4: Reading a Root-to-Leaf Path (20 min)

### Tracing One Customer Through the Tree (8 min)

**Say:** *"Let's make this concrete with two brand-new, hand-built customers — the same 'predict on new data' pattern we used back in Session 4."*

**Live-code:**

```python
new_customers = pd.DataFrame({
    "age": [40, 40],
    "monthly_spend": [500, 2000],
    "tenure_months": [20, 20],
    "support_tickets": [2, 2],
    "contract_type": ["Monthly", "Monthly"],
    "used_mobile_app": ["Yes", "Yes"],
})

preds = tree_pipe.predict(new_customers)
print(preds)
```

**Run it.** Expected output:

```
[1 0]
```

**Say:** *"Same contract type, same app usage, same age and tenure and tickets — the ONLY difference between these two customers is monthly spend: ₹500 versus ₹2,000. And the tree's prediction flips: 1 (churn) for the low spender, 0 (stay) for the high spender. Let's trace WHY, using the `export_text` output from before."*

### Building the Plain-English Sentence Together (8 min)

**Write this template on the board:**

```
"This customer's contract is [Monthly/Annual]. [If Monthly:] They [do/don't]
use the mobile app. [If they do:] Their monthly spend is [above/below]
₹644. Following that path, the tree predicts [Churn/Stay]."
```

**Have a student narrate customer 1 (₹500/month) out loud using the template. Expect:**

*"This customer's contract is Monthly, not Annual, so we go right at the root. They DO use the mobile app, so we go right again. Their monthly spend, ₹500, is at or below ₹644, so we go left at the final split — landing on a leaf that predicts Churn."*

**Have a second student narrate customer 2 (₹2,000/month).** Expect the same path until the last split, then: *"Their monthly spend, ₹2,000, is ABOVE ₹644, so we go right at the final split — landing on a leaf that predicts Stay."*

**Say:** *"That's it. That's the entire skill. No coefficients, no 'holding other features fixed' caveat like linear regression needed — just a literal, followable sequence of yes/no questions that ends in an answer. This is why trees are prized in regulated industries like lending and healthcare, where you often have to explain EVERY individual decision, not just the model in aggregate."*

### The Limits of This Explainability (4 min)

**Say:** *"One honest caveat before we move on: this clean, simple story gets much messier as trees get DEEPER, with dozens of nodes, and messier still once we combine many trees together next session in a Random Forest. Today's 4-leaf tree is a best-case scenario for explainability — real production trees are often deeper and the full path, while still technically traceable, is less digestible for a non-technical audience without some summarization."*

**Ask:** *"If this tree had `max_depth=15` instead of 3, would tracing a root-to-leaf path still be POSSIBLE?"* (Yes, technically — every path is always traceable — but a 15-question chain is much harder for a human to hold in their head or explain simply, even though the mechanism is identical.)

---

## SEGMENT 5: Overfitting — Depth vs. Accuracy (20 min)

### The Depth Sweep, Live (8 min)

**Say:** *"Let's do exactly what we did with `PolynomialFeatures` in Session 4 — deliberately explore a range of model complexities and watch the train/test gap tell its own story."*

**Live-code:**

```python
print(f"{'depth':>6} {'train_acc':>10} {'test_acc':>10}")
for depth in [1, 2, 3, 4, 5, None]:
    d_pipe = Pipeline(steps=[
        ("pre", preprocess),
        ("model", DecisionTreeClassifier(max_depth=depth, random_state=42)),
    ])
    d_pipe.fit(X_train, y_train)
    train_acc = d_pipe.score(X_train, y_train)
    test_acc = d_pipe.score(X_test, y_test)
    print(f"{str(depth):>6} {train_acc:>10.3f} {test_acc:>10.3f}")
```

**Run it.** Expected output:

```
 depth  train_acc   test_acc
     1      0.778      0.889
     2      0.852      0.778
     3      0.963      0.778
     4      0.963      0.778
     5      1.000      0.778
  None      1.000      0.778
```

**Say, pointing at the printed table:** *"Look closely — this is a slightly different shape than Session 4's polynomial demo, and that's a great, realistic teaching moment. Train accuracy climbs steadily as depth increases, exactly as expected — a deeper tree can always fit the training data at least as well. But test accuracy actually peaks at `max_depth=1`, the SHALLOWEST tree we tried, then drops and flattens out. With only 36 rows total and 27 in the training set, a depth-1 'stump' — asking just ONE question — already captures most of the real signal, and every additional split beyond that is increasingly just fitting quirks specific to these 27 training rows."*

**Ask:** *"If your only goal were the highest possible test accuracy on THIS exact dataset, which depth would you pick?"* (`max_depth=1`, based on the printed numbers — though flag that with only 9 test rows, a single row flipping prediction changes the score by roughly 11 percentage points, so this conclusion should be held loosely.)

### Why Small Datasets Make This Especially Visible (4 min)

**Say:** *"This is worth naming explicitly: with only 36 rows, a tree doesn't need much depth to start memorizing individual customers rather than learning general patterns. On a real production dataset with tens of thousands of rows, you'd typically see train and test accuracy stay closer together for a few more levels of depth before the gap opens up — the SHAPE of this overfitting curve is universal, but exactly WHERE it starts depends heavily on how much data you have relative to how many splits the tree is allowed to make."*

### The Diagnostic Table (5 min)

**Draw this diagnostic table on the board — same structure as Session 4's, adapted for trees:**

| Pattern | Diagnosis |
|---|---|
| Train accuracy ≈ Test accuracy, both reasonably high | Good depth choice |
| Train accuracy high (near 1.0), Test accuracy much lower | Overfitting — tree is too deep for the data available |
| Train accuracy and Test accuracy both low | Underfitting — tree is too shallow, missing real signal |

**Ask:** *"Looking at our printed table, which depths show the classic overfitting SIGNATURE — train near-perfect, test clearly lower and flat?"* (`max_depth=3` onward — train accuracy keeps rising toward 1.0 while test accuracy stays flat at 0.778, a widening gap.)

### `max_depth` as One Knob Among Several (3 min)

**Say, briefly:** *"`max_depth` is the most intuitive knob for controlling tree complexity, but it's not the only one. `min_samples_leaf` (minimum rows allowed in any leaf) and `min_samples_split` (minimum rows required before a node is even allowed to split) do similar jobs — all three exist specifically to stop a tree from carving out leaves so small and specific that they're really just memorizing single rows. We'll see these tuned systematically with `GridSearchCV` in Session 11."*

---

## SEGMENT 6: Lab — Full Workflow on customer_churn.csv (15 min)

### Instructions (read aloud, step by step)

1. Load `customer_churn.csv`; build `X` with all six features (`age`, `monthly_spend`, `tenure_months`, `support_tickets`, `contract_type`, `used_mobile_app`) and `y` as `churned`.
2. Split with `train_test_split(test_size=0.25, random_state=42, stratify=y)`.
3. Build a `ColumnTransformer` that one-hot encodes `contract_type` and `used_mobile_app`, passing numeric columns through.
4. Train a `DecisionTreeClassifier(max_depth=2, random_state=42)` inside a `Pipeline`.
5. Report train and test accuracy.
6. Print the tree using `export_text`, and write one plain-English sentence explaining the root split.
7. Sweep `max_depth` over `[1, 2, 3, 4, None]` and state, in one sentence, which depth you would recommend and why.

### Starter Code

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

df = pd.read_csv("customer_churn.csv")
X = df[[___, ___, ___, ___, ___, ___]]
y = df[___]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=___, random_state=42, stratify=___
)

cat_cols = ["contract_type", "used_mobile_app"]
preprocess = ColumnTransformer([
    ("cat", ___(drop="if_binary"), cat_cols),
], remainder="passthrough")

pipe = Pipeline(steps=[
    ("pre", preprocess),
    ("model", ___(max_depth=___, random_state=42)),
])
pipe.___(X_train, y_train)

print("Train accuracy:", pipe.score(___, ___))
print("Test accuracy: ", pipe.score(___, ___))

feature_names = pipe.named_steps["pre"].get_feature_names_out()
print(export_text(pipe.named_steps["model"], feature_names=list(feature_names)))
# TODO: write your root-split interpretation sentence here as a comment

for depth in [1, 2, 3, 4, None]:
    d_pipe = Pipeline(steps=[("pre", preprocess), ("model", DecisionTreeClassifier(max_depth=depth, random_state=42))])
    d_pipe.fit(X_train, y_train)
    print(depth, d_pipe.score(X_train, y_train), d_pipe.score(X_test, y_test))
# TODO: write your recommended-depth sentence here as a comment
```

### Reference Solution

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

df = pd.read_csv("customer_churn.csv")
X = df[["age", "monthly_spend", "tenure_months", "support_tickets",
        "contract_type", "used_mobile_app"]]
y = df["churned"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

cat_cols = ["contract_type", "used_mobile_app"]
preprocess = ColumnTransformer([
    ("cat", OneHotEncoder(drop="if_binary"), cat_cols),
], remainder="passthrough")

pipe = Pipeline(steps=[
    ("pre", preprocess),
    ("model", DecisionTreeClassifier(max_depth=2, random_state=42)),
])
pipe.fit(X_train, y_train)

print("Train accuracy:", pipe.score(X_train, y_train))
print("Test accuracy: ", pipe.score(X_test, y_test))

feature_names = pipe.named_steps["pre"].get_feature_names_out()
print(export_text(pipe.named_steps["model"], feature_names=list(feature_names)))
# Root split interpretation: the tree first asks whether a customer is on a
# Monthly contract. Customers NOT on Monthly (i.e. Annual) are immediately
# predicted to stay -- contract type is the single strongest churn signal.

for depth in [1, 2, 3, 4, None]:
    d_pipe = Pipeline(steps=[("pre", preprocess), ("model", DecisionTreeClassifier(max_depth=depth, random_state=42))])
    d_pipe.fit(X_train, y_train)
    print(depth, d_pipe.score(X_train, y_train), d_pipe.score(X_test, y_test))
# Recommendation: max_depth=1 gives the best test accuracy (0.889) on this
# small dataset -- deeper trees raise train accuracy toward 1.0 without any
# further test accuracy gain, the classic overfitting signature.
```

**Instructor circulates**, checking specifically that students read the root split off the printed `export_text` output (rather than guessing from `plot_tree` colors alone), and that the "recommended depth" sentence references the actual printed train/test numbers rather than a generic statement.

---

## SEGMENT 7: Summary, Wrap-Up & Q&A (5 min)

**What we covered today:**
- Trained a `DecisionTreeClassifier` end to end inside a `Pipeline` with categorical encoding
- Visualized the tree with both `plot_tree` and `export_text`
- Traced and explained a full root-to-leaf decision path in plain business language
- Diagnosed overfitting by sweeping `max_depth` and comparing train vs. test accuracy

**Bridge to next session:** *"Today's shallow tree was refreshingly explainable — but you also saw it's a bit unstable: change the random split slightly, and the exact thresholds it picks can shift. A single tree, especially a small one, can be a bit of a 'high-variance' model — sensitive to exactly which rows it happened to train on. Next session tackles that directly: Random Forests, which train MANY trees on different random subsets of data and features, then average their votes. You'll trade away some of today's crisp explainability for real gains in accuracy and stability — and we'll find a middle ground using feature importances."*

**Homework / self-practice:**
1. Retrain with `max_depth=1` only, print the single split, and write the plain-English sentence for BOTH of its two leaves (churn leaf and stay leaf).
2. Try `min_samples_leaf=5` instead of tuning `max_depth`, and compare its train/test accuracy to the `max_depth=2` model from the lab.
3. Using the `new_customers` pattern from SEGMENT 4, hand-build a THIRD synthetic customer designed to land on a different leaf than either of the two shown in class, and confirm your prediction is correct.

---

## Q&A & Doubt Solving

**Likely questions and suggested answers:**

**Q: Why did test accuracy PEAK at `max_depth=1` instead of climbing alongside train accuracy?**
→ With only 36 rows (27 for training), the dataset is small enough that a single well-chosen split already captures most of the real signal (contract type is a strong churn predictor). Every additional split beyond that starts fitting quirks specific to the 27 training rows rather than generalizable patterns — the textbook overfitting shape, just appearing earlier than it might on a larger dataset.

**Q: Is Gini impurity the only way a tree decides where to split?**
→ No — `entropy` (information gain) is a common alternative, set via `criterion="entropy"`. Both usually produce very similar trees in practice; Gini is scikit-learn's default because it's slightly cheaper to compute (no logarithms).

**Q: Can a decision tree handle a regression target, not just classification?**
→ Yes — `DecisionTreeRegressor` works the same way structurally, but leaves predict an average numeric value instead of a class, and splits are chosen to minimize variance (similar in spirit to the MSE we minimized with Linear Regression back in Session 4) rather than Gini impurity.

**Q: Why do we still need `OneHotEncoder` for a tree, if trees just ask yes/no questions anyway? Couldn't it just split directly on the text category?**
→ scikit-learn's `DecisionTreeClassifier` implementation requires numeric input like every other scikit-learn estimator — it doesn't natively split on raw text categories the way some other tree libraries can. One-hot encoding converts each category into its own 0/1 column, which the tree can then split on exactly like any other numeric feature.

**Q: If two features are highly correlated, does that cause the same "credit splitting" issue we saw with Linear Regression's coefficients in Session 4?**
→ Less severely. A tree just picks whichever correlated feature gives the bigger Gini improvement at each split and largely ignores the other one at that node — it doesn't try to "share credit" the way a linear model's coefficients can. This is actually one of Random Forests' advantages next session: averaging many trees, each potentially favoring a different one of two correlated features, gives a fuller picture than a single tree's one-sided choice.

---

## Instructor Notes

- **Prerequisite check:** Confirm students recall `ColumnTransformer` + `OneHotEncoder` from Session 2 before SEGMENT 2 — today reuses that pattern without re-deriving it from scratch.
- **Common mistake:** Reading `plot_tree` colors as the ONLY explanation, without checking the actual split conditions and sample counts printed inside each box. Encourage students to always read the text inside the box, not just the color.
- **Another common mistake:** Assuming a deeper tree is always "more accurate." SEGMENT 5's printed table is the direct counter-example — make sure students read the ACTUAL numbers rather than assuming the intuitive-sounding answer.
- **Another common mistake:** Forgetting `stratify=y` on a classification split, especially since some earlier regression sessions (Session 4, 5) correctly did NOT use it. Reinforce that `stratify` is specific to classification targets.
- **Engagement tip:** SEGMENT 4's two-hand-built-customers demo (identical except for one number) is the strongest "aha" moment of the day — the flipped prediction from a single feature crossing a threshold makes the tree's mechanism feel completely transparent. Don't rush it.
- **Time check:** If running behind before the break, shorten SEGMENT 3's Gini impurity explanation to a single sentence and move on.
- **If running long after the break:** Compress SEGMENT 5's "why small datasets make this visible" discussion (4 min) into a single sentence and proceed straight to the diagnostic table.
- **Materials to prepare:** `customer_churn.csv` open and ready; matplotlib available for `plot_tree`; a scratch cell with SEGMENT 4's `new_customers` DataFrame pre-typed so it doesn't eat live-coding time.

---

## Common Errors — Quick Reference

| Bug / mistake | Symptom | Fix |
|---|---|---|
| Passing raw text categories directly into `DecisionTreeClassifier.fit()` | `ValueError: could not convert string to float` | Encode categorical columns first (e.g. `OneHotEncoder` inside a `ColumnTransformer`) |
| Forgetting `stratify=y` on a classification split | Unlucky splits with imbalanced train/test class ratios, especially on small datasets | Always pass `stratify=y` for classification targets |
| Assuming a deeper tree is automatically more accurate | Reports "depth=10 must be best" without checking test accuracy | Always compare train vs. test accuracy across a depth sweep before choosing |
| Reading only `plot_tree` colors, ignoring the split conditions and sample counts | Misinterprets which feature/threshold actually drove a prediction | Read the full text inside each box, or cross-check with `export_text` |
| Explaining a prediction without following the ACTUAL path for that specific row | Generic, sometimes wrong explanation not tied to the real feature values | Trace the specific row's feature values through each split condition, in order |

---

## Appendix: Root Split Interpretation Drill (Optional, If Time Allows)

For each root split below (hypothetical, for practice), have students phrase the plain-English sentence:

| Root split | Business context |
|---|---|
| `credit_score <= 650` | Loan approval |
| `tenure_months <= 6` | Subscription churn |
| `num_prior_purchases <= 1` | First-time buyer discount targeting |
| `age <= 25` | Insurance premium tier |

**Sample expected answer for row 1:** *"The tree's first and most important question is whether the applicant's credit score is 650 or below — this single cutoff does more to separate approved from rejected applicants than any other feature in the dataset."*

---

## Appendix: Depth Sweep Reference Table (Instructor Reference — Actual Run Values)

| max_depth | Train accuracy | Test accuracy |
|---|---|---|
| 1 | 0.778 | 0.889 |
| 2 | 0.852 | 0.778 |
| 3 | 0.963 | 0.778 |
| 4 | 0.963 | 0.778 |
| 5 | 1.000 | 0.778 |
| None | 1.000 | 0.778 |

*(These are the actual numbers produced by `customer_churn.csv` with `random_state=42` — use them to sanity-check your own run, though matplotlib/sklearn version differences should not change these.)*

---

## FAQ — Additional Questions

**Q: Does the order of columns in `X` matter for how the tree splits?**
→ No — the tree evaluates every feature and every threshold independently when choosing each split; column order has no effect on the resulting tree structure or predictions.

**Q: What happens if two different splits would reduce Gini impurity by the exact same amount?**
→ scikit-learn breaks ties using an internal, deterministic rule tied to feature index order — this is one of several reasons `random_state` is set, so results are reproducible even in edge cases like this.

**Q: Can a tree split on the SAME feature more than once, at different nodes?**
→ Yes, frequently — a feature like `monthly_spend` might appear at the root AND again several levels down with a different threshold, if the data supports further separation on that same feature at each stage.

**Q: Why does the class prediction shown at a non-leaf (internal) node in `plot_tree` matter, if predictions only actually happen at leaves?**
→ It doesn't affect final predictions, but it's a useful sanity-check while reading the diagram: it shows what the tree WOULD predict if you stopped early at that node, which is exactly the value a pruned (shallower) version of the tree would use there.

---

## SEGMENT 8: Supplemental Code Demos (Instructor Optional, If Time or Advanced Group)

### Demo A — Feature importance preview (5 min)

```python
importances = tree_model.feature_importances_
for name, imp in sorted(zip(feature_names, importances), key=lambda t: -t[1]):
    print(f"{name}: {imp:.4f}")
```

**Break it down:**
- `feature_importances_` scores each feature by how much it reduced Gini impurity across ALL its splits in the tree, summed and normalized
- This is a preview of Session 10's centerpiece — Random Forests extend this exact idea across many trees for a more stable importance ranking
- A single tree's importances can be unstable (sensitive to the exact random split), which is precisely the motivation for averaging across many trees next session

**Ask:** Does the feature at the ROOT split always have the highest importance score?

**Common mistake:** Assuming importance = correlation with the target; a feature can be important for splitting without having the strongest raw correlation.

**Fix:** Treat `feature_importances_` as "how useful for SPLITTING decisions," a related but distinct idea from simple correlation.

### Demo B — Comparing `criterion="gini"` vs `criterion="entropy"` (4 min)

```python
for criterion in ["gini", "entropy"]:
    c_pipe = Pipeline(steps=[("pre", preprocess), ("model", DecisionTreeClassifier(max_depth=3, criterion=criterion, random_state=42))])
    c_pipe.fit(X_train, y_train)
    print(criterion, c_pipe.score(X_train, y_train), c_pipe.score(X_test, y_test))
```

**Break it down:**
- Both criteria measure "impurity" using slightly different math (Gini uses squared class proportions, entropy uses logarithms)
- In practice, the resulting trees and accuracy are usually very close, as this demo typically shows
- Gini is scikit-learn's default mainly for computational speed, not because it's meaningfully "better"

**Ask:** If the two criteria produce nearly identical accuracy, is there ever a strong reason to prefer one over the other?

**Common mistake:** Treating `criterion` as a major hyperparameter worth extensive tuning.

**Fix:** Spend tuning effort on `max_depth`, `min_samples_leaf`, and `min_samples_split` first — `criterion` rarely moves the needle much.

### Demo C — What happens with NO `max_depth` limit at all, visually (5 min, requires matplotlib)

```python
unlimited_pipe = Pipeline(steps=[("pre", preprocess), ("model", DecisionTreeClassifier(random_state=42))])
unlimited_pipe.fit(X_train, y_train)

plt.figure(figsize=(20, 10))
plot_tree(unlimited_pipe.named_steps["model"], feature_names=feature_names, class_names=["Stay", "Churn"], filled=True)
plt.show()
print("Depth:", unlimited_pipe.named_steps["model"].get_depth())
print("Leaves:", unlimited_pipe.named_steps["model"].get_n_leaves())
```

**Break it down:**
- With no depth limit, the tree keeps splitting until every leaf is perfectly pure (or can't be split further) — visually, this produces a sprawling, hard-to-read diagram compared to SEGMENT 3's clean 4-leaf tree
- This is the "memorization" extreme made visually obvious — leaves with just 1-2 training samples each
- A great one-slide visual contrast to pin against the depth=3 tree from earlier

**Ask:** How many leaves does the unlimited tree have compared to the depth-3 tree's 4 leaves — and what does that number alone suggest?

**Common mistake:** Assuming "the tree found more patterns" rather than "the tree ran out of data to keep splitting meaningfully."

**Fix:** Pair any leaf count observation with the train/test accuracy gap — leaf count alone isn't proof of overfitting, but a large leaf count relative to dataset size is a strong warning sign.

---

## Materials Checklist

- [ ] `customer_churn.csv` open and readable in the working notebook environment
- [ ] matplotlib available for `plot_tree` (SEGMENT 3 and Demo C)
- [ ] Scratch cell with SEGMENT 4's `new_customers` DataFrame pre-typed
- [ ] Whiteboard space for the root-to-leaf sentence template
- [ ] Timer visible for the lab segment

---

## Timing Contingencies

| Situation | Action |
|---|---|
| Running 10 min behind before break | Shorten SEGMENT 3's Gini impurity explanation to one sentence |
| Running long after break | Compress SEGMENT 5's "why small datasets" discussion into one sentence |
| Low energy after lunch/break | Run the Appendix root-split interpretation drill as a quick group activity |
| Advanced group finishes lab early | Assign Demo A (feature importance preview) as a stretch task and a bridge to Session 10 |
| No shared screen / projector issue | Read `export_text` output aloud instead of relying on `plot_tree` visuals |

---

## End-of-Session Quiz (5 Questions)

1. What does the ROOT node of a decision tree represent?
2. If train accuracy is 1.0 and test accuracy is 0.70, what does that pattern indicate?
3. Why did we need `OneHotEncoder` before training the tree, even though trees only ask yes/no questions?
4. What does `feature_importances_` measure, at a high level?
5. Explain, in one plain-English sentence, what it means for a customer to "reach a leaf" during prediction.

**Answer key (instructor):**
1. The single most useful split the tree found across every feature and threshold, applied to the full training set before any splitting has happened.
2. Overfitting — the tree has essentially memorized the training rows and does not generalize to unseen data.
3. scikit-learn's `DecisionTreeClassifier` requires numeric input; one-hot encoding converts categorical columns into numeric 0/1 columns the tree can split on.
4. How much each feature contributed to reducing impurity (Gini or entropy) across all of its splits in the tree, normalized across all features.
5. It means the customer's specific feature values satisfied a unique sequence of split conditions, ending at a node with no further splits, whose majority class becomes their predicted outcome.

---

## Homework Rubric

| Criterion | Excellent (4) | Good (3) | Needs Work (2) | Incomplete (1) |
|---|---|---|---|---|
| max_depth=1 both-leaf interpretation | Both leaves correctly explained in plain English | One leaf explained clearly, other thin | Attempted, unclear or incorrect | Not attempted |
| min_samples_leaf=5 comparison | Correct run with clear train/test comparison to max_depth=2 model | Comparison present, thin interpretation | Numbers reported, no comparison | Not attempted |
| Third synthetic customer | Correct new leaf reached with clear reasoning shown | Correct leaf reached, reasoning thin | Attempted, incorrect leaf reached | Not attempted |

**Total:** /12 — Pass threshold: 8/12
