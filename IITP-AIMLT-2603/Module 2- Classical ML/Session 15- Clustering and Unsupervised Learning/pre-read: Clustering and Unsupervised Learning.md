# Clustering and Unsupervised Learning
---

## Mental Map

```mermaid
%%{init: {'flowchart': {'nodeSpacing': 55, 'rankSpacing': 65, 'diagramPadding': 24}}}%%
flowchart TB
linkStyle default stroke-width:3px

subgraph foundation[" Foundation "]
direction TB
    P0["<b>Previous Module</b><br/>Foundations of Data<br/><i>[Python · Data Stack]</i><br/><i>Learnt:</i> Python, Pandas, SQL, cleaning, viz, APIs"]
    CURMOD["<b>Current Module Until<br/>Previous Session</b><br/><i>Classical ML</i><br/>Regression · classification<br/>Trees · Random Forest<br/>ROC · AUC · validation"]
    CURSES["<b>Current Session</b><br/><b>Clustering & Unsupervised ML</b><br/><i>Shift:</i> Find structure without labels<br/>K-Means · distance · elbow<br/>Interpret & use clusters"]
end

subgraph value[" Value "]
direction LR
    CVAL["<b>Course Value</b><br/>Learn from unlabelled<br/>data — most of the world"]
    RVAL["<b>Real-Life Value</b><br/>Customer segments,<br/>anomaly detection, EDA"]
end

subgraph future[" Future Path "]
direction TB
    U0["<b>Upcoming Module</b><br/>GenAI & Agents<br/><i>[LLMs · Agents]</i><br/>RAG & agent apps"]
end

P0 ==>|&nbsp;Foundation&nbsp;| CURMOD
CURMOD ==>|&nbsp;Progress&nbsp;| CURSES
CURSES ==>|&nbsp;Course Path&nbsp;| CVAL
CURSES ==>|&nbsp;Real-Life&nbsp;| RVAL
CURSES ==>|&nbsp;Next Module&nbsp;| U0

classDef prevBox fill:#E8F4FC,stroke:#2B6CB0,stroke-width:2px,color:#1A202C
classDef curModBox fill:#FFF8E6,stroke:#B7791F,stroke-width:2px,color:#1A202C
classDef curSessBox fill:#E6FFFA,stroke:#0D9488,stroke-width:3px,color:#1A202C
classDef valueBox fill:#F3E8FF,stroke:#7C3AED,stroke-width:2px,color:#1A202C
classDef futureBox fill:#ECFDF5,stroke:#047857,stroke-width:2px,color:#1A202C
classDef startBox fill:#F7FAFC,stroke:#4A5568,stroke-width:2px,color:#1A202C
class P0 prevBox
class CURMOD curModBox
class CURSES curSessBox
class CVAL,RVAL valueBox
class U0 futureBox
```

## What You'll Learn

In this pre-read, you'll discover:

- What **unsupervised learning** is and how it differs from supervised learning
- How **K-Means clustering** finds natural groups in unlabelled data
- What **distance metrics** measure and how they drive cluster formation
- How the **elbow method** helps you choose the right number of clusters (K)
- How to **interpret and label clusters** to turn them into business insights

---

## A. Unsupervised Learning — No Labels, No Problem

> 💡 **Analogy:** A librarian receiving thousands of new books with no subject labels does not give up — they read the books, notice themes and similarities, and organise shelves by inferred categories. **Unsupervised learning** is that process: finding structure in data without being told what to look for.

**One-line definition:** **Unsupervised learning** is a category of ML where the model learns patterns, structure, or groupings from data without any labelled target variable — the algorithm finds order on its own.

```mermaid
flowchart LR
    subgraph supervised["Supervised Learning"]
        S["Input features + labels\n(pre-labelled data)\n→ Learns to predict labels"]
    end
    subgraph unsupervised["Unsupervised Learning"]
        U["Input features only\n(no labels)\n→ Discovers structure"]
    end
```

**Where unsupervised learning is used:**

| Task | Application | No labels because |
|---|---|---|
| Clustering | Customer segmentation | Nobody labelled customers in advance |
| Anomaly detection | Fraud, defects | Rare events are hard to label exhaustively |
| Dimensionality reduction | Compressing features | No target — just explore the data |
| Topic modelling | Grouping news articles | Articles are not pre-categorised |

**Why most data is unlabelled:**

Labelling requires human effort — expert annotators, time, and cost. Most real-world data (web logs, sensor readings, transaction records) is never labelled. Unsupervised learning lets you extract value from it anyway.

---

## B. K-Means Clustering — Grouping by Similarity

> 💡 **Analogy:** Party organisers grouping attendees into tables use a simple rule: "people who know each other stay together." K-Means uses a mathematical version of that rule: "data points closer together belong to the same group." It starts with K guesses and iteratively refines the groupings until they stabilise.

**One-line definition:** **K-Means clustering** partitions n data points into K groups (clusters) by iteratively assigning each point to its nearest cluster centre (centroid) and then updating each centroid to be the mean of its assigned points.

**The algorithm in 4 steps:**

```mermaid
flowchart TD
    I["1. Choose K\nPlace K centroids randomly"] --> A["2. Assign each point\nto the nearest centroid"]
    A --> U["3. Update centroids\nMove each to mean of its assigned points"]
    U --> C{4. Did centroids\nmove significantly?}
    C -->|Yes| A
    C -->|No| D["Converged\nFinal cluster assignments"]
```

**What "nearest" means:**

By default, K-Means uses **Euclidean distance** — the straight-line distance between two points. For two features (x₁, x₂):

```
distance = √((x₁_a − x₁_b)² + (x₂_a − x₂_b)²)
```

**Important preprocessing requirement:** Always **scale features** before running K-Means. If one feature is in ₹ lakhs (range 0–100) and another is age (range 18–60), the income feature will dominate all distance calculations. Standardise all features to zero mean and unit variance first.

---

## C. Distance Metrics — Measuring Similarity

> 💡 **Analogy:** Two cities can be compared by: straight-line distance on a map (Euclidean), road distance through the city grid (Manhattan), or how different their names sound (cosine similarity for text). **Distance metrics** are the mathematical version of this choice — different metrics reveal different types of similarity.

**One-line definition:** A **distance metric** is a function that quantifies how different or similar two data points are — the choice of metric fundamentally shapes what "nearby" means and therefore which clusters form.

| Metric | Formula (simplified) | Best for |
|---|---|---|
| **Euclidean** | √(sum of squared differences) | Numeric data, similar scales |
| **Manhattan** | Sum of absolute differences | When large differences are less important |
| **Cosine** | Angle between feature vectors | Text, high-dimensional data |

```mermaid
flowchart LR
    A["Point A\n(age=25, income=30)"] --> E["Euclidean distance\n= √((25−45)² + (30−80)²)\n≈ 53.9"]
    B["Point B\n(age=45, income=80)"] --> E
    A --> M["Manhattan distance\n= |25−45| + |30−80|\n= 70"]
    B --> M
```

**Effect of feature scale on distance:**

| Features | No scaling | With scaling |
|---|---|---|
| Income (0–200k) and Age (18–65) | Income dominates distance | Both contribute equally |
| Cluster result | Clusters based mostly on income | Balanced clustering across features |

Scaling is not optional for K-Means — it is mandatory for meaningful clusters.

---

## D. The Elbow Method — Choosing K

> 💡 **Analogy:** When organising a bookshelf, too few categories (2: fiction/non-fiction) is too broad. Too many (200 micro-categories) is impractical. There is a sweet spot where adding another category stops meaningfully improving organisation. The **elbow method** finds that sweet spot for clusters.

**One-line definition:** The **elbow method** plots the total within-cluster sum of squared distances (inertia) for different values of K and identifies the "elbow" — the point where adding more clusters stops producing meaningful improvement.

```mermaid
flowchart LR
    K2["K=2\nInertia: 5000\n(too few clusters,\neach large)"] --> K3
    K3["K=3\nInertia: 3000"] --> K4
    K4["K=4\nInertia: 1800\n← Elbow here"] --> K5
    K5["K=5\nInertia: 1700\n(minimal gain)"] --> K10
    K10["K=10\nInertia: 1500\n(many clusters,\nnot useful)"]
```

**How to use it:**

1. Train K-Means for K = 2, 3, 4, … 10 (or more)
2. Record inertia for each K
3. Plot K (x-axis) vs inertia (y-axis)
4. Find the "elbow" — the bend where the curve flattens
5. Choose K at the elbow

**When there is no clear elbow:**

If the curve decreases smoothly without a clear bend, it means the data has no strong natural cluster structure. In this case, choose K based on **business constraints** (e.g. "we can run 4 marketing campaigns, so K=4").

---

## E. Cluster Interpretation and Business Use Cases

> 💡 **Analogy:** A geographer who draws regional boundaries on a map has done the clustering. The real work is then naming each region — "industrial belt," "agricultural zone," "coastal tourism" — and deciding what policies to apply to each. **Cluster interpretation** is that naming and analysis step.

**One-line definition:** **Cluster interpretation** means analysing the statistical profile of each cluster (mean feature values, size, distribution) to assign a human-readable label and derive business actions from it.

**How to interpret clusters:**

After running K-Means, compute the mean of each feature per cluster:

| Cluster | Avg age | Avg income (₹k) | Avg tenure (yrs) | Label |
|---|---|---|---|---|
| 0 | 28 | 35 | 1.2 | Young, entry-level |
| 1 | 45 | 120 | 8.5 | Senior, high-value |
| 2 | 35 | 60 | 3.4 | Mid-career, growing |

Now each cluster has a name and a business action:

| Cluster | Label | Business action |
|---|---|---|
| 0 | Young, entry-level | Retention incentives, career path messaging |
| 1 | Senior, high-value | Premium loyalty programme, personalised offers |
| 2 | Mid-career, growing | Skills development, cross-sell products |

**Real-world business use cases:**

| Industry | Clustering application |
|---|---|
| Retail | Customer segmentation for personalised campaigns |
| Banking | Risk segment identification for product offers |
| Healthcare | Patient grouping for care pathway design |
| E-commerce | Product grouping for recommendation engines |
| Operations | Machine fault type categorisation for maintenance |

**K-Means limitations to know:**

- Assumes spherical, equally-sized clusters (not always true in practice)
- Sensitive to outliers — one extreme point can pull a centroid significantly
- Must choose K in advance — not always obvious
- Not suitable for categorical features directly — use numeric representations or a different algorithm

---

## Practice Exercises

**1. Pattern Recognition**  
A K-Means model with K=3 is trained on customer data (age, monthly spend). After convergence, the centroids are at: (25, 500), (45, 3000), (60, 800). Describe what each cluster likely represents in business terms. What would happen to the clusters if monthly spend was not scaled and ranged from 0 to 50,000 while age ranged from 18 to 70?

**2. Concept Detective**  
An analyst runs K-Means for K=2 to 10 and plots inertia. The inertia drops sharply from K=2 to K=4, then decreases very slowly from K=4 to K=10. Using section D, identify the optimal K, explain what the flat region means about the data, and describe what you would do if the business team insists on K=6 for operational reasons.

**3. Real-Life Application**  
Describe how you would use K-Means clustering in three of the following contexts: (a) grouping e-commerce customers for a marketing campaign, (b) grouping hospital patients by health indicators, (c) identifying fault patterns in manufacturing sensors, (d) grouping news articles by topic. For each: name the features you would use, how many clusters you might start with, and what you would do after clustering to extract actionable insights.

**4. Spot the Error**  
A data scientist runs K-Means on a customer dataset with three features: `age (18–75)`, `annual_salary_INR (0 to 15,00,000)`, and `num_purchases (1–200)`. They do not scale the data first. The resulting clusters look suspiciously income-based, ignoring age and purchase frequency almost entirely. Using section C, explain why this happened and what they should do to fix it.

**5. Planning Ahead**  
You are segmenting 100,000 mobile app users into groups to personalise push notifications. Available features: `session_length`, `sessions_per_week`, `features_used_count`, `days_since_last_session`, `in_app_purchase_amount`. Describe the full clustering pipeline: preprocessing steps, how you would use the elbow method, what K you would start with, how you would name and describe the clusters, and what the product team would do differently for each cluster.

---

> ✅ **You're done!** You now understand how K-Means finds hidden groups in unlabelled data, how distance and scaling shape the results, and how to interpret clusters into actionable business segments. Next (and final session of the module): **Model Selection and End-to-End Pipeline**, where you will learn how to compare all the algorithms you have studied and build a complete, reproducible ML workflow from raw data to deployed model.
