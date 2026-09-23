# Lecture Script: Clustering, Model Selection & Explainability
> **Instructor Reference** — Module 2: Classical ML | Session 12 | Duration: 2 Hours

---

## Session Overview

**Goal:** Students run `KMeans` clustering and determine an optimal `k` using the elbow method and silhouette score, compare multiple trained models from across this module using a structured metric table, and explain model predictions and feature importance in plain business language. This session also CLOSES Module 2 — Classical ML, so it includes a module-review thread woven through the wrap-up.

**Student profile at this point:** Has trained linear models (Sessions 4-6), evaluated classification metrics (Session 7), and trained tree-based models (Sessions 9-10), all SUPERVISED — every model so far had a target column to learn from. Today introduces their first UNSUPERVISED technique, with no target at all, before pulling the whole module together.

**Key outcome:** Every student runs KMeans on `customer_segments.csv`, produces an elbow plot and silhouette scores to justify a choice of `k`, names each resulting cluster in plain business language, builds a structured comparison table across three trained models on `customer_churn.csv`, and writes at least one feature-importance explanation a non-technical stakeholder could act on.

**Datasets for this session:** `customer_segments.csv` (in this folder) — 36 rows of `annual_spend_k`, `purchase_frequency_per_month`, `avg_basket_value`, `loyalty_years`, no target column, for the clustering segment. `customer_churn.csv` from Session 9/10 (referenced via relative path) for the model comparison segment.

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| SEGMENT 1: Opening — Learning Without an Answer Key | 10 min | 0:10 |
| SEGMENT 2: Fit/Predict with KMeans | 20 min | 0:30 |
| SEGMENT 3: Choosing k — Elbow Method and Silhouette Score | 25 min | 0:55 |
| **BREAK** | 10 min | 1:05 |
| SEGMENT 4: Comparing Multiple Models Side by Side | 20 min | 1:25 |
| SEGMENT 5: Explainability in Plain Business Language | 15 min | 1:40 |
| SEGMENT 6: Lab — Full Workflow (Clustering + Comparison) | 15 min | 1:55 |
| SEGMENT 7: Module 2 Wrap-Up, Review & Q&A | 5 min | 2:00 |

---

## SEGMENT 1: Opening — Learning Without an Answer Key (10 min)

### Naming the Shift (6 min)

**Say:** *"Stop and notice something about every single dataset we've used since Session 4: `housing_sample.csv` had `price_lakhs`. `loan_applications.csv` had `approved`. `customer_churn.csv` had `churned`. `patient_readmission.csv` had `readmitted_30d`. Every model we've trained has had an answer key — a target column telling it exactly what the 'right' output was for every row. Today, for the first time in this entire module, we work with a dataset that has NO target column at all."*

**Live-code this quick reveal:**

```python
import pandas as pd

df = pd.read_csv("customer_segments.csv")
print(df.head())
print(df.columns.tolist())
```

**Run it.** **Say:** *"Look at that column list — `customer_id`, `annual_spend_k`, `purchase_frequency_per_month`, `avg_basket_value`, `loyalty_years`. Nothing to predict. No `y`. This is UNSUPERVISED learning: instead of learning a mapping from features to a known label, the algorithm finds STRUCTURE in the data on its own — in today's case, natural groupings of similar customers."*

### Setting Expectations for Today (4 min)

**Say:** *"By the end of today you'll be able to do four things: run KMeans clustering on unlabeled data, defend your choice of the number of clusters using two complementary techniques, build a fair side-by-side comparison of several trained models, and — the skill that ties this entire module together — explain what any of these models actually found, in plain English, to someone who has never seen a line of Python. This last skill is genuinely the most valuable one in the whole module, because a brilliant model that nobody can explain to a business stakeholder is a model that never gets deployed."*

**Learning contract for today — write on board:**

- Run `KMeans` clustering and interpret cluster assignments
- Choose `k` using the elbow method and silhouette score together
- Build a structured multi-model comparison table
- Explain predictions and feature importance in plain business language

---

## SEGMENT 2: Fit/Predict with KMeans (20 min)

### Why Scaling Matters Here, More Than Ever (6 min)

**Say:** *"Before we fit anything, one non-negotiable step. KMeans works purely by measuring DISTANCE between points — and distance calculations get completely dominated by whichever feature happens to have the largest raw numeric range, unless we scale first."*

**Live-code the problem, briefly:**

```python
print(df[["annual_spend_k", "purchase_frequency_per_month", "avg_basket_value", "loyalty_years"]].describe())
```

**Run it and point at the ranges.** **Say:** *"`avg_basket_value` ranges into the THOUSANDS, while `loyalty_years` ranges from under 1 to maybe 8. Without scaling, KMeans would essentially only 'see' `avg_basket_value` and largely ignore `loyalty_years` when computing distances — not because loyalty doesn't matter, but purely because of the units it happens to be measured in. This is the exact same 'features on different scales' problem Session 5 flagged for Ridge/Lasso regularization — same root cause, different algorithm."*

### Fitting KMeans (8 min)

**Live-code:**

```python
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

X = df[["annual_spend_k", "purchase_frequency_per_month", "avg_basket_value", "loyalty_years"]]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
df["cluster"] = kmeans.fit_predict(X_scaled)

print(df["cluster"].value_counts())
```

**Run it.** Expected output:

```
cluster
0    13
2    12
1    11
Name: count, dtype: int64
```

**Say:** *"`n_init=10` tells KMeans to try 10 different random starting positions for the cluster centers and keep the best result — KMeans can get stuck in a mediocre local solution depending on where it starts, so trying multiple starts and keeping the best is standard practice, not optional polish. `random_state=42` then makes THAT search reproducible, same role it's played all module."*

**Say:** *"Notice `fit_predict` — a new method name, but it's doing something structurally familiar: `fit` learns the 3 cluster centers from the data, and `predict` (fused into one call here) assigns every row to its nearest center. No separate train/test split this time either — with no target to guard against overfitting to, that specific concern from every prior session doesn't apply the same way here."*

### Profiling the Clusters (6 min)

**Live-code:**

```python
cluster_profile = df.groupby("cluster")[["annual_spend_k", "purchase_frequency_per_month",
                                          "avg_basket_value", "loyalty_years"]].mean().round(2)
print(cluster_profile)
```

**Run it.** Expected output:

```
         annual_spend_k  purchase_frequency_per_month  avg_basket_value  loyalty_years
cluster
0                  26.40                          4.XX            1082.XX            2.92
1                  49.94                          1.XX            3966.XX            5.42
2                  15.18                          8.XX             613.XX            1.58
```

**Say:** *"This is the moment raw numbers turn into a business story. Cluster 1: high annual spend, LOW purchase frequency, huge average basket size, highest loyalty — these are your premium, occasional big-ticket shoppers. Cluster 2: lowest spend, HIGHEST frequency, small basket size, lowest loyalty — frequent, budget-conscious shoppers. Cluster 0 sits in between on almost every dimension — your balanced, mid-tier segment. None of this required a target column; the structure was already there in how these customers naturally behave."*

**Ask:** *"If a marketing team wanted to run a loyalty-rewards campaign specifically targeting customers at risk of leaving due to low engagement, which cluster would you point them to first, and why?"* (Cluster 2 — lowest loyalty years and lowest average spend, despite frequent purchases; likely the most price-sensitive, least "locked in" segment.)

---

## SEGMENT 3: Choosing k — Elbow Method and Silhouette Score (25 min)

### Why We Can't Just Guess k=3 (5 min)

**Say:** *"We used `n_clusters=3` a moment ago — but be honest, that number came from me, not from any principled process. Let's fix that properly, the way you'd need to for a real, unlabeled dataset where you don't already know there are 'obviously' 3 groups."*

### The Elbow Method, Live (8 min)

**Live-code:**

```python
inertias = []
for k in range(2, 8):
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    km.fit(X_scaled)
    inertias.append(km.inertia_)
    print(k, round(km.inertia_, 2))
```

**Run it.** Expected output:

```
2 40.94
3 20.81
4 17.49
5 14.96
6 12.89
7 11.11
```

**Say:** *"`inertia_` is the sum of squared distances from every point to its assigned cluster center — lower means tighter, more compact clusters. Notice the pattern: from `k=2` to `k=3`, inertia drops by a huge amount, 40.94 down to 20.81. From `k=3` to `k=4`, the drop is much smaller, 20.81 to 17.49. From there on, each additional cluster buys less and less improvement. That bend — where the curve stops dropping sharply and starts to flatten — is the 'elbow,' and it's visually around `k=3` here."*

**Live-code the plot:**

```python
import matplotlib.pyplot as plt

plt.plot(range(2, 8), inertias, marker="o")
plt.xlabel("k")
plt.ylabel("Inertia")
plt.title("Elbow Method")
plt.show()
```

**Run it and point at the visible bend around k=3.**

### The Silhouette Score, Live (8 min)

**Say:** *"The elbow method is useful but a bit subjective — 'where does it bend' can be a judgment call. Silhouette score gives us a second, more precise opinion."*

**Live-code:**

```python
from sklearn.metrics import silhouette_score

sil_scores = []
for k in range(2, 8):
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = km.fit_predict(X_scaled)
    sil = silhouette_score(X_scaled, labels)
    sil_scores.append(sil)
    print(k, round(sil, 3))
```

**Run it.** Expected output:

```
2 0.608
3 0.539
4 0.456
5 0.352
6 0.287
7 0.317
```

**Say:** *"Silhouette score ranges from -1 to 1: for each point, it compares how close that point is to others in ITS OWN cluster versus the NEAREST different cluster. Higher means better-separated, more confidently-assigned clusters. Here's an interesting wrinkle worth sitting with: the HIGHEST silhouette score is actually at `k=2`, not `k=3` — but it's only a modest amount higher than `k=3`'s score (0.608 vs 0.539), and `k=2` would merge our clearly-distinct 'premium occasional' and 'budget frequent' groups into one, losing real business nuance."*

### Reconciling the Two Signals with Business Context (4 min)

**Say:** *"This is a genuinely important, slightly uncomfortable lesson: elbow method and silhouette score are DECISION SUPPORT tools, not decision-MAKING tools. Neither one hands you a single unambiguous right answer automatically. Here, `k=2` scores marginally higher on silhouette, and `k=3` sits at the elbow's bend with a silhouette score that's still solidly good (0.539, well above 0) — and critically, `k=3` maps onto THREE segments a marketing team can actually act on differently: premium occasional shoppers, budget frequent shoppers, and a balanced middle segment. We choose `k=3`, and we write down WHY: the statistical signals support it reasonably well, AND it aligns with a business-actionable segmentation."*

**Ask:** *"If silhouette score had shown `k=2` dramatically higher — say 0.85 versus `k=3`'s 0.30 — would you still recommend `k=3` for business reasons alone?"* (Generally no — a very large statistical gap is a stronger signal that the data genuinely doesn't support that many distinct groups; business context should inform a CLOSE call, not override a clear one.)

### The Decision Table (0 min — folded into discussion above; keep note for instructor)

**Draw this table on the board:**

| Signal | What it favors here | Weight in final decision |
|---|---|---|
| Elbow method | Bend visible around k=3 | Supporting evidence |
| Silhouette score | Highest at k=2, close second at k=3 | Supporting evidence, not decisive alone |
| Business actionability | 3 segments are each independently useful to marketing | Tie-breaker for this close call |

---

## BREAK (10 min)

*Suggested break prompt:* Ask students to think back across the whole module — Linear Regression, Ridge/Lasso, Logistic Regression, Decision Trees, Random Forests — and pick which ONE model they'd nominate as "most explainable to a non-technical stakeholder" and which they'd nominate as "most likely to have the best raw accuracy." Come back ready to defend both picks.

---

## SEGMENT 4: Comparing Multiple Models Side by Side (20 min)

### Building the Comparison Table, Live (10 min)

**Say:** *"Let's switch datasets back to `customer_churn.csv` from Sessions 9 and 10, and do something we've never done in one place before: train THREE different model types on the exact same split and put their metrics in one table, side by side."*

**Live-code:**

```python
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

churn_df = pd.read_csv("../Session 9- Decision Trees/customer_churn.csv")
X_churn = churn_df[["age", "monthly_spend", "tenure_months", "support_tickets",
                     "contract_type", "used_mobile_app"]]
y_churn = churn_df["churned"]

X_train, X_test, y_train, y_test = train_test_split(
    X_churn, y_churn, test_size=0.25, random_state=42, stratify=y_churn
)

cat_cols = ["contract_type", "used_mobile_app"]
num_cols = ["age", "monthly_spend", "tenure_months", "support_tickets"]

pre_scaled = ColumnTransformer([
    ("cat", OneHotEncoder(drop="if_binary"), cat_cols),
    ("num", StandardScaler(), num_cols),
])
pre_plain = ColumnTransformer([("cat", OneHotEncoder(drop="if_binary"), cat_cols)], remainder="passthrough")

models = {
    "Logistic Regression": Pipeline([("pre", pre_scaled), ("model", LogisticRegression(max_iter=1000))]),
    "Decision Tree": Pipeline([("pre", pre_plain), ("model", DecisionTreeClassifier(max_depth=3, random_state=42))]),
    "Random Forest": Pipeline([("pre", pre_plain), ("model", RandomForestClassifier(n_estimators=200, max_depth=4, random_state=42))]),
}

results = []
for name, pipe in models.items():
    pipe.fit(X_train, y_train)
    preds = pipe.predict(X_test)
    results.append({
        "Model": name,
        "Accuracy": round(accuracy_score(y_test, preds), 3),
        "Precision": round(precision_score(y_test, preds), 3),
        "Recall": round(recall_score(y_test, preds), 3),
        "F1": round(f1_score(y_test, preds), 3),
    })

results_df = pd.DataFrame(results)
print(results_df.to_string(index=False))
```

**Run it.** Expected output:

```
              Model  Accuracy  Precision  Recall    F1
Logistic Regression     0.889       0.80    1.00 0.889
      Decision Tree     0.778       0.75    0.75 0.750
      Random Forest     0.889       0.80    1.00 0.889
```

**Say:** *"Here's a genuinely honest, slightly humbling result: Logistic Regression — the very FIRST classification model we trained back in Session 6 — ties with Random Forest for the best accuracy AND F1 here, and both beat the single Decision Tree. This is a real, common finding in practice, not a scripted lesson: more complex models don't automatically win. Session 4's opening lesson — 'always start simple and give yourself a real number to beat' — pays off directly here."*

### Choosing a Winner Isn't Just "Highest Number" (6 min)

**Ask:** *"Given this exact tie between Logistic Regression and Random Forest, what ELSE — beyond these four metrics — might tip your recommendation one way or the other?"* Guide toward:

- **Explainability:** Logistic Regression's coefficients (Session 6) are simpler to explain than Random Forest's feature importances, though both are reasonably interpretable compared to a black box.
- **Stability across splits:** Session 10's SEGMENT 4 showed Random Forest is typically more STABLE across different random splits than a single tree — worth re-checking whether that stability edge holds against Logistic Regression too, not just against a single tree.
- **Training/inference cost:** Logistic Regression trains and predicts essentially instantly; Random Forest with 200 trees is still fast at this data scale but meaningfully more expensive at larger scale.
- **Deployment simplicity:** A simpler model is often easier to monitor, debug, and explain to auditors or regulators over time.

**Say:** *"There is no universally 'correct' winner from a table alone — the table narrows the field to real contenders, and the FINAL choice depends on which of these secondary factors matters most for the specific business context. This is the single biggest maturity jump in this whole module: moving from 'which model has the highest number' to 'which model is the right FIT for this specific deployment situation.'"*

### The General Comparison-Table Template (4 min)

**Write this reusable pattern on the board:**

```
1. Train every candidate model on the IDENTICAL train/test split
2. Score every candidate with the SAME set of metrics
3. Put results in one table, sorted by the primary business metric
4. Before declaring a winner, explicitly discuss: explainability, stability,
   cost, and deployment constraints -- not just the top number
```

---

## SEGMENT 5: Explainability in Plain Business Language (15 min)

### The Skill That Ties Everything Together (5 min)

**Say:** *"Every session this module has ended with some version of 'translate this into plain English' — Session 4's coefficient sentences, Session 9's root-to-leaf paths, Session 10's feature importance framing. Today we practice it one more time, deliberately, as a closing, standalone skill, because in a real job this is often the ONLY part of your work a non-technical stakeholder ever actually reads."*

### Extracting and Translating, Live (6 min)

**Live-code:**

```python
rf_model = models["Random Forest"]
feature_names = rf_model.named_steps["pre"].get_feature_names_out()
importances = rf_model.named_steps["model"].feature_importances_

ranked = sorted(zip(feature_names, importances), key=lambda t: -t[1])
for name, score in ranked:
    print(f"{name}: {score:.4f}")

top_feature, top_score = ranked[0]
print(f"\nTop driver: {top_feature} ({top_score:.1%} of splitting usefulness)")
```

**Run it.** Expected output:

```
remainder__support_tickets: 0.2260
remainder__tenure_months: 0.1882
cat__contract_type_Monthly: 0.1836
remainder__monthly_spend: 0.1467
cat__used_mobile_app_Yes: 0.1329
remainder__age: 0.1226

Top driver: remainder__support_tickets (22.6% of splitting usefulness)
```

**Have the class collectively draft the final business sentence out loud, using the module-wide template:**

```
"[Model type] predicts [target] mainly based on [top feature]. In practice,
this means [plain business consequence] -- so [recommended action]."
```

**Model answer:** *"Our churn model predicts customer churn mainly based on how many support tickets a customer has filed. In practice, this means customers with repeated unresolved issues are our highest churn risk — so the retention team should prioritize proactive outreach to any customer with 4 or more open or recent tickets, rather than waiting for a cancellation request."*

### Why "It Depends" Is Sometimes the Most Honest Explanation (4 min)

**Say:** *"One last, important honesty check. Sometimes the truthful explanation ISN'T a single clean sentence — SEGMENT 4's near-tie between Logistic Regression and Random Forest is a perfect example. The most defensible stakeholder-facing answer there might genuinely be: 'Two of our three candidate models perform about equally well; we recommend the simpler one for easier long-term maintenance, but both are solid choices.' Resist the urge to manufacture false confidence or false precision just to sound decisive — a clear, honest 'it's close, and here's how we're breaking the tie' is far more valuable, and far more trustworthy, than an overconfident single answer."*

---

## SEGMENT 6: Lab — Full Workflow (Clustering + Comparison) (15 min)

### Instructions (read aloud, step by step)

1. Load `customer_segments.csv`, scale the four numeric features, and run KMeans for `k` in `range(2, 8)`, printing inertia and silhouette score for each.
2. Choose a final `k`, justify it in one sentence combining at least one statistical signal AND business reasoning, then fit final clusters and print the per-cluster mean profile.
3. Load `../Session 9- Decision Trees/customer_churn.csv`, train Logistic Regression, Decision Tree, and Random Forest on an identical split, and build a comparison table with Accuracy, Precision, Recall, F1.
4. Extract the Random Forest's top feature by importance and write one plain-English business sentence using the module template.
5. Write one final sentence naming which model you'd recommend deploying and why, referencing at least one factor BEYOND raw accuracy.

### Starter Code

```python
import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# --- Part 1: Clustering ---
df = pd.read_csv("customer_segments.csv")
X = df[[___, ___, ___, ___]]
X_scaled = ___().fit_transform(X)

for k in range(2, 8):
    km = ___(n_clusters=k, random_state=42, n_init=10)
    labels = km.fit_predict(X_scaled)
    print(k, km.inertia_, silhouette_score(___, ___))

final_k = ___
kmeans = KMeans(n_clusters=final_k, random_state=42, n_init=10)
df["cluster"] = kmeans.fit_predict(X_scaled)
print(df.groupby("cluster")[[___, ___, ___, ___]].mean())
# TODO: write your k-choice justification sentence here as a comment

# --- Part 2: Model comparison ---
churn_df = pd.read_csv("../Session 9- Decision Trees/customer_churn.csv")
X_churn = churn_df[["age", "monthly_spend", "tenure_months", "support_tickets", "contract_type", "used_mobile_app"]]
y_churn = churn_df["churned"]
X_train, X_test, y_train, y_test = train_test_split(X_churn, y_churn, test_size=0.25, random_state=42, stratify=y_churn)

cat_cols = ["contract_type", "used_mobile_app"]
num_cols = ["age", "monthly_spend", "tenure_months", "support_tickets"]
pre_scaled = ColumnTransformer([("cat", OneHotEncoder(drop="if_binary"), cat_cols), ("num", StandardScaler(), num_cols)])
pre_plain = ColumnTransformer([("cat", OneHotEncoder(drop="if_binary"), cat_cols)], remainder="passthrough")

models = {
    "Logistic Regression": Pipeline([("pre", pre_scaled), ("model", ___(max_iter=1000))]),
    "Decision Tree": Pipeline([("pre", pre_plain), ("model", ___(max_depth=3, random_state=42))]),
    "Random Forest": Pipeline([("pre", pre_plain), ("model", ___(n_estimators=200, max_depth=4, random_state=42))]),
}

results = []
for name, pipe in models.items():
    pipe.___(X_train, y_train)
    preds = pipe.predict(X_test)
    results.append({"Model": name, "Accuracy": round(accuracy_score(y_test, preds), 3),
                     "Precision": round(precision_score(y_test, preds), 3),
                     "Recall": round(recall_score(y_test, preds), 3),
                     "F1": round(f1_score(y_test, preds), 3)})
print(pd.DataFrame(results))

rf_model = models["Random Forest"]
feat_names = rf_model.named_steps["pre"].get_feature_names_out()
importances = rf_model.named_steps["model"].___
top_feature, top_score = sorted(zip(feat_names, importances), key=lambda t: -t[1])[0]
# TODO: write your business-language sentence and final recommendation here as comments
```

### Reference Solution

```python
import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# --- Part 1: Clustering ---
df = pd.read_csv("customer_segments.csv")
X = df[["annual_spend_k", "purchase_frequency_per_month", "avg_basket_value", "loyalty_years"]]
X_scaled = StandardScaler().fit_transform(X)

for k in range(2, 8):
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = km.fit_predict(X_scaled)
    print(k, km.inertia_, silhouette_score(X_scaled, labels))

final_k = 3
kmeans = KMeans(n_clusters=final_k, random_state=42, n_init=10)
df["cluster"] = kmeans.fit_predict(X_scaled)
print(df.groupby("cluster")[["annual_spend_k", "purchase_frequency_per_month", "avg_basket_value", "loyalty_years"]].mean())
# k=3 justification: the elbow bends around k=3, silhouette score at k=3
# (0.539) is close to the k=2 maximum (0.608) and still solidly positive,
# and k=3 maps onto three genuinely distinct, actionable customer segments
# for marketing (premium occasional, budget frequent, balanced mid-tier).

# --- Part 2: Model comparison ---
churn_df = pd.read_csv("../Session 9- Decision Trees/customer_churn.csv")
X_churn = churn_df[["age", "monthly_spend", "tenure_months", "support_tickets", "contract_type", "used_mobile_app"]]
y_churn = churn_df["churned"]
X_train, X_test, y_train, y_test = train_test_split(X_churn, y_churn, test_size=0.25, random_state=42, stratify=y_churn)

cat_cols = ["contract_type", "used_mobile_app"]
num_cols = ["age", "monthly_spend", "tenure_months", "support_tickets"]
pre_scaled = ColumnTransformer([("cat", OneHotEncoder(drop="if_binary"), cat_cols), ("num", StandardScaler(), num_cols)])
pre_plain = ColumnTransformer([("cat", OneHotEncoder(drop="if_binary"), cat_cols)], remainder="passthrough")

models = {
    "Logistic Regression": Pipeline([("pre", pre_scaled), ("model", LogisticRegression(max_iter=1000))]),
    "Decision Tree": Pipeline([("pre", pre_plain), ("model", DecisionTreeClassifier(max_depth=3, random_state=42))]),
    "Random Forest": Pipeline([("pre", pre_plain), ("model", RandomForestClassifier(n_estimators=200, max_depth=4, random_state=42))]),
}

results = []
for name, pipe in models.items():
    pipe.fit(X_train, y_train)
    preds = pipe.predict(X_test)
    results.append({"Model": name, "Accuracy": round(accuracy_score(y_test, preds), 3),
                     "Precision": round(precision_score(y_test, preds), 3),
                     "Recall": round(recall_score(y_test, preds), 3),
                     "F1": round(f1_score(y_test, preds), 3)})
print(pd.DataFrame(results))

rf_model = models["Random Forest"]
feat_names = rf_model.named_steps["pre"].get_feature_names_out()
importances = rf_model.named_steps["model"].feature_importances_
top_feature, top_score = sorted(zip(feat_names, importances), key=lambda t: -t[1])[0]
# Business sentence: our churn model predicts churn mainly based on
# support ticket volume -- customers with more open/recent tickets are
# our highest churn risk, so retention should prioritize proactive
# outreach to high-ticket customers rather than waiting for cancellation.
# Recommendation: Logistic Regression ties Random Forest on every metric
# here, and is simpler to explain and cheaper to maintain long-term, so
# it is the recommended deployment choice unless future data shows the
# Random Forest pulling ahead on a larger, more complex dataset.
```

**Instructor circulates**, checking specifically that the `k` justification sentence references BOTH a statistical signal and a business reason (not just one), and that the final model recommendation names a factor beyond the raw metric numbers.

---

## SEGMENT 7: Module 2 Wrap-Up, Review & Q&A (5 min)

**Full Module 2 review — walk through this list on the board, one line per session:**

- **Session 1-2:** Framed ML problems correctly and built leakage-aware preprocessing pipelines with `ColumnTransformer`
- **Session 3 (Master Class):** Built the mathematical foundation — lines, residuals, gradient descent — that every model since has rested on
- **Session 4:** Trained `LinearRegression`, evaluated with MAE/RMSE/R², interpreted coefficients, diagnosed overfitting
- **Session 5:** Controlled overfitting directly with Ridge and Lasso, and named the bias-variance tradeoff
- **Session 6-7:** Trained `LogisticRegression`, worked with `predict_proba` and thresholds, and mastered the full classification metrics toolkit
- **Session 8 (Master Class):** Built the probability foundation behind every classification metric
- **Session 9-10:** Moved to tree-based models — fully explainable single trees, then more accurate, more stable Random Forests
- **Session 11:** Learned to actually TRUST your reported numbers — cross-validation, `GridSearchCV`, and catching data leakage before it costs you
- **Session 12 (today):** Stepped into unsupervised learning with KMeans, and closed the loop by comparing every model type side by side and explaining results in business language

**Say:** *"Every single model in this module, from Session 4's simplest `LinearRegression` to today's Random Forest and KMeans, follows the exact same skeleton you now know cold: prepare the data honestly, split or fold it properly, fit, evaluate with the RIGHT metric for the problem, and — always — explain the result to someone who wasn't in this room. That skeleton is Module 2's real takeaway, far more than any single algorithm's name."*

**Homework / self-practice:**
1. Re-run the clustering lab with `k=4` and `k=5` and write one sentence each on whether the resulting clusters still feel business-meaningful, or start to feel arbitrarily split.
2. Extend the model comparison table to include a fourth model of your choice from the module (e.g., a Ridge- or Lasso-based classifier, or a different `max_depth` Random Forest), and update your final recommendation.
3. Write a 4-6 sentence "executive summary" of your `customer_churn.csv` findings, as if presenting to a non-technical VP: name the winning model, the top churn driver in business language, and one concrete recommended action.

---

## Q&A & Doubt Solving

**Likely questions and suggested answers:**

**Q: Could we have used a supervised model instead of KMeans if we secretly HAD a target column, just to double-check the clusters make sense?**
→ You could compare clusters against a KNOWN label after the fact (if one existed) as a sanity check, but that's different from KMeans itself, which never uses labels at all — the entire point of clustering is finding structure without supervision. If you already have reliable labels for the exact business question you care about, a supervised classifier is usually more directly useful than clustering.

**Q: Why did silhouette score DECREASE from k=2 to k=3 but the elbow method still favored k=3?**
→ These two techniques measure genuinely different things — inertia (elbow) only cares about how tight each cluster is internally, while silhouette also weighs how well-SEPARATED clusters are from their nearest neighbor cluster. It's completely normal for them to disagree at the margins; that's exactly why SEGMENT 3 taught you to weigh both alongside business context rather than trusting either alone.

**Q: In the model comparison table, is it fair that Random Forest used `max_depth=4` and 200 trees while Decision Tree used `max_depth=3`? Shouldn't they match?**
→ Good catch, and worth naming explicitly: for a scientifically "cleanest" comparison, you'd often hold hyperparameters like `max_depth` constant across model types, as we deliberately did in Session 10's head-to-head. Here, each model used a REASONABLE setting for its type, which is closer to how you'd actually compare production-ready candidates — each tuned reasonably for itself — rather than an artificially constrained apples-to-apples test. Both approaches are valid depending on whether your goal is isolating one specific effect (match hyperparameters) or comparing realistic best-effort candidates (tune each independently).

**Q: Does `feature_importances_` still work the same way for the Random Forest model used in the comparison table?**
→ Yes — identical mechanism to Session 10, since it's the exact same `RandomForestClassifier` class and the same fitted `Pipeline` structure.

**Q: What's the actual difference between "explainability" and "interpretability" — are they the same thing?**
→ In casual industry usage they're often used interchangeably, as we have today. Some practitioners draw a finer distinction: "interpretable" models (like a shallow decision tree or linear regression) are simple enough to understand directly from their structure; "explainable" can also refer to post-hoc techniques (like SHAP, mentioned briefly in Session 10's FAQ) that explain a more complex, less inherently transparent model after the fact. Not a distinction you need to stress over for this course, but good to have heard the terms.

---

## Instructor Notes

- **Prerequisite check:** Confirm students recall `StandardScaler` (Sessions 5/6/11) before SEGMENT 2 — today's KMeans scaling discussion assumes that concept is already fluent, just applied to a new algorithm.
- **Common mistake:** Running KMeans on unscaled features. Catch this explicitly in the lab if you see it — the resulting clusters will look strange and hard to interpret, and it's a very easy step to forget since KMeans itself doesn't error out or warn you.
- **Another common mistake:** Treating the elbow "bend" or the highest silhouette score as an automatic, unquestionable final answer rather than supporting evidence. Reinforce SEGMENT 3's framing explicitly.
- **Another common mistake:** In the model comparison table, declaring a "winner" using accuracy alone without discussing explainability/stability/cost as SEGMENT 4 modeled. Push students in the lab to name a non-accuracy factor explicitly.
- **Engagement tip:** SEGMENT 4's near-tie between Logistic Regression and Random Forest is a genuinely useful "humility" moment for the whole module — let it land, and connect it back to Session 4's "always start simple" opening lesson for a satisfying full-circle callback.
- **Time check:** If running behind before the break, shorten SEGMENT 3's "reconciling the two signals" discussion to a single instructor-stated conclusion rather than an open class discussion.
- **If running long after the break:** Compress SEGMENT 5 to just the live business-sentence drafting, skipping the standalone "it depends" honesty discussion (assign it as a reading).
- **Materials to prepare:** `customer_segments.csv` open and ready; confirm the relative path `../Session 9- Decision Trees/customer_churn.csv` resolves correctly in your teaching environment (or copy `customer_churn.csv` directly into this session's folder as a fallback); matplotlib available for the elbow plot; whiteboard space for the Module 2 review list in SEGMENT 7.

---

## Common Errors — Quick Reference

| Bug / mistake | Symptom | Fix |
|---|---|---|
| Running KMeans on unscaled features | Clusters dominated by whichever feature has the largest raw range, hard to interpret | Always `StandardScaler` (or similar) before KMeans |
| Treating elbow/silhouette as fully automatic, no business judgment | Chooses a `k` that's statistically defensible but not actionable | Combine both statistical signals with business context, as in SEGMENT 3 |
| Comparing models trained on DIFFERENT splits | Invalid, apples-to-oranges comparison table | Always use the identical train/test split across all candidate models |
| Declaring a "winner" from accuracy alone | Misses real deployment considerations (explainability, cost, stability) | Explicitly discuss at least one factor beyond the top metric number |
| Explaining feature importance with false precision or overconfidence | Misleads stakeholders into thinking the model is more certain than it is | Use honest, appropriately-hedged business language, as modeled in SEGMENT 5 |

---

## Appendix: Cluster Naming Drill (Optional, If Time Allows)

For each hypothetical cluster profile below, have students propose a plain-English segment NAME and one marketing action:

| Cluster | Spend | Frequency | Loyalty |
|---|---|---|---|
| A | High | Low | High |
| B | Low | High | Low |
| C | Medium | Medium | Medium |
| D | High | High | High |

**Sample expected answer for row A:** *"Name: 'Premium Occasional Shoppers.' Action: target with exclusive, high-value offers timed around their infrequent but large purchases, rather than high-frequency discount campaigns that don't match their behavior."*

---

## Appendix: Elbow & Silhouette Reference Table (Instructor Reference — Actual Run Values)

| k | Inertia | Silhouette score |
|---|---|---|
| 2 | 40.94 | 0.608 |
| 3 | 20.81 | 0.539 |
| 4 | 17.49 | 0.456 |
| 5 | 14.96 | 0.352 |
| 6 | 12.89 | 0.287 |
| 7 | 11.11 | 0.317 |

*(These are the actual numbers produced by `customer_segments.csv` with `random_state=42`, `n_init=10` — use them to sanity-check your own run.)*

---

## FAQ — Additional Questions

**Q: Can KMeans handle categorical features directly, the way we one-hot encoded them for trees?**
→ Not natively in a fully principled way — KMeans' distance calculation assumes numeric, continuous-ish features. One-hot encoding categorical columns before KMeans is common practice, though the resulting 0/1 distances behave a bit differently than genuinely continuous ones; specialized variants like K-Modes or K-Prototypes exist for heavily categorical data, outside today's scope.

**Q: Does `KMeans.predict()` work on brand-new data after fitting, like our supervised models' `.predict()` did?**
→ Yes — once fit, `kmeans.predict(new_scaled_data)` assigns new points to whichever existing cluster center is nearest, without recomputing the centers. Note the new data must be scaled using the SAME fitted scaler as the training data, exactly parallel to how we've handled preprocessing all module.

**Q: In the final model comparison, could we have also included KMeans somehow?**
→ Not directly in the same table — KMeans solves a fundamentally different kind of problem (grouping, no target) from the four classification metrics used for the churn comparison. You could, however, use cluster membership itself AS a new engineered FEATURE for a supervised churn model — a common real-world pattern that combines both techniques.

**Q: Is there a version of `GridSearchCV` for tuning `k` in KMeans automatically?**
→ Not directly via `GridSearchCV` with a standard accuracy-style score, since KMeans has no target to score against in the usual sense. Silhouette score CAN be used as a custom scoring function with tools like `GridSearchCV` for more automated k-selection, but the elbow-plus-silhouette-plus-business-judgment approach from today remains the most common, most defensible practice.

---

## SEGMENT 8: Supplemental Code Demos (Instructor Optional, If Time or Advanced Group)

### Demo A — Visualizing clusters in 2D with PCA (6 min, requires matplotlib)

```python
from sklearn.decomposition import PCA

pca = PCA(n_components=2)
X_2d = pca.fit_transform(X_scaled)

plt.scatter(X_2d[:, 0], X_2d[:, 1], c=df["cluster"], cmap="viridis")
plt.xlabel("PCA component 1")
plt.ylabel("PCA component 2")
plt.title("Customer segments (2D projection)")
plt.show()
```

**Break it down:**
- Our data has 4 dimensions, too many to plot directly — PCA compresses it down to the 2 most informative combined dimensions for visualization purposes only (the actual clustering above used all 4 original scaled features, not this 2D projection)
- A visibly well-separated, colorful blob structure in this plot is a nice additional, intuitive confirmation of the silhouette score's numeric story
- A great "wow" visual to include in a real stakeholder-facing report

**Ask:** If the colored groups in this plot overlapped heavily rather than forming distinct blobs, what would that suggest about our chosen `k`?

**Common mistake:** Assuming this 2D plot IS the clustering itself, rather than a visualization of clustering that happened in the original 4D scaled space.

**Fix:** Always clarify that PCA here is for visualization only — the actual `KMeans.fit_predict()` call used the full original feature set.

### Demo B — ROC-AUC as a fourth model comparison metric (5 min)

```python
from sklearn.metrics import roc_auc_score

for name, pipe in models.items():
    probs = pipe.predict_proba(X_test)[:, 1]
    auc = roc_auc_score(y_test, probs)
    print(f"{name}: ROC-AUC = {auc:.3f}")
```

**Break it down:**
- Extends Session 7's ROC-AUC concept directly into today's comparison table, since all three of today's models support `predict_proba`
- ROC-AUC measures ranking quality across ALL possible thresholds at once, complementing the single-threshold Accuracy/Precision/Recall/F1 numbers already in the table
- A natural stretch addition to the SEGMENT 4 comparison table for advanced groups

**Ask:** Could two models have very similar Accuracy/F1 but noticeably different ROC-AUC? What would that suggest?

**Common mistake:** Treating ROC-AUC as strictly superior to the other metrics rather than complementary.

**Fix:** Use ROC-AUC alongside threshold-specific metrics, not as a full replacement — different business questions call for different metrics, as Session 7 established.

### Demo C — A tiny "explainability memo" template (4 min)

```python
memo = f"""
CHURN MODEL SUMMARY (for non-technical stakeholders)
-----------------------------------------------------
Recommended model: Logistic Regression (tied best performance, simplest to maintain)
Top churn driver: {top_feature} ({top_score:.1%} of model's decision-making weight)
Plain-English takeaway: Customers with more support tickets are our highest
churn risk. Proactive outreach to high-ticket customers is the top
recommended action.
"""
print(memo)
```

**Break it down:**
- A tiny, reusable template for turning a session's findings into something immediately shareable
- Deliberately short — a stakeholder memo that requires the reader to already understand ML terminology has failed at its one job
- A nice closing artifact students can reuse for their own future projects, including any capstone work

**Ask:** What's the ONE sentence in this memo doing the most "explainability" work, and why?

**Common mistake:** Burying the plain-English takeaway underneath too much technical detail (metric tables, hyperparameters) at the TOP of the memo.

**Fix:** Lead with the plain-English takeaway and recommended action; technical detail (if needed at all for this audience) belongs further down or in an appendix.

---

## Materials Checklist

- [ ] `customer_segments.csv` open and readable in the working notebook environment
- [ ] Access to `../Session 9- Decision Trees/customer_churn.csv` confirmed (or a local copy as fallback)
- [ ] matplotlib available for the elbow plot and Demo A's PCA visualization
- [ ] Whiteboard space for the Module 2 review list (SEGMENT 7)
- [ ] Timer visible for the lab segment

---

## Timing Contingencies

| Situation | Action |
|---|---|
| Running 10 min behind before break | Shorten SEGMENT 3's "reconciling the two signals" discussion to one instructor-stated conclusion |
| Running long after break | Compress SEGMENT 5 to the live business-sentence drafting only, skip the standalone "it depends" discussion |
| Low energy after lunch/break | Run the Appendix cluster-naming drill as a quick group activity |
| Advanced group finishes lab early | Assign Demo A (PCA visualization) or Demo B (ROC-AUC) as a stretch task |
| No shared screen / projector issue | Read the printed inertia/silhouette tables aloud and have students type along |

---

## End-of-Session Quiz (5 Questions)

1. What is the key structural difference between KMeans and every other model trained this module?
2. Why must features be scaled before running KMeans?
3. If the elbow method and silhouette score disagree on the best `k`, what should you do?
4. In a structured model comparison table, name two factors — beyond the top metric number — that should influence a final deployment choice.
5. Why is a well-hedged "it's close, here's how we're breaking the tie" often a more honest stakeholder explanation than a confident single answer?

**Answer key (instructor):**
1. KMeans is unsupervised — it has no target column at all and finds structure purely from feature similarity, unlike every supervised model trained in prior sessions.
2. KMeans measures pure distance between points; unscaled features with larger numeric ranges would dominate the distance calculation regardless of their true importance.
3. Weigh both alongside business context and actionability — neither method alone is fully decisive, especially in close calls.
4. Any two of: explainability, stability across different data splits, training/inference cost, deployment/monitoring simplicity.
5. Because it accurately reflects genuine uncertainty in the underlying data/metrics rather than manufacturing false confidence, which builds more durable trust with stakeholders over time.

---

## Homework Rubric

| Criterion | Excellent (4) | Good (3) | Needs Work (2) | Incomplete (1) |
|---|---|---|---|---|
| k=4 and k=5 re-clustering | Both runs completed with clear, reasoned business-meaningfulness judgment | Runs completed, thin judgment | Attempted, unclear conclusions | Not attempted |
| Fourth model comparison | Correctly added with updated table and recommendation | Added, thin recommendation update | Attempted, errors present | Not attempted |
| Executive summary | Clear, correctly targeted at non-technical audience, names model/driver/action | Present, technical language leaks in | Vague or incomplete | Not attempted |

**Total:** /12 — Pass threshold: 8/12

---

*This session closes Module 2 — Classical ML. Module 3 begins next with a new set of techniques building on this foundation.*
