# Lecture Script: Data Preparation for ML
> **Instructor Reference** — Module 2: Classical ML | Session 2 | Duration: 2 Hours

---

## Session Overview

**Goal:** Students build a full `Pipeline` + `ColumnTransformer` for a mixed numeric/categorical dataset with missing values, and can identify and prevent data leakage — including recognizing the exact line of code that would have caused it.

**Student profile at this point:** Comfortable with `train_test_split` and `cross_val_score` from Session 1; has not yet built a multi-step preprocessing pipeline in scikit-learn.

**Key outcome:** Every student builds a reusable preprocessing pipeline on `raw_customers.csv` that fits cleanly into `cross_val_score` without leakage, and can name all three leakage patterns covered today with a one-sentence fix for each.

**Dataset for this session:** `raw_customers.csv` (in this folder) — 30 rows of `customer_id`, `age`, `income` (numeric, some missing), `city` and `plan_type` (categorical, `plan_type` has some missing), `churned` (target).

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| SEGMENT 1: Opening — The Leakage Horror Story | 10 min | 0:10 |
| SEGMENT 2: Why Pipeline Over Manual Steps | 15 min | 0:25 |
| SEGMENT 3: Practical — Inspecting raw_customers.csv | 10 min | 0:35 |
| SEGMENT 4: ColumnTransformer Live Build | 25 min | 1:00 |
| **BREAK** | 10 min | 1:10 |
| SEGMENT 5: Encoding & Scaling Decision Guide | 15 min | 1:25 |
| SEGMENT 6: Data Leakage Patterns | 15 min | 1:40 |
| SEGMENT 7: Lab — Leak-Proof Pipeline on raw_customers.csv | 15 min | 1:55 |
| SEGMENT 8: Summary, Wrap-Up & Q&A | 5 min | 2:00 |

---

## SEGMENT 1: Opening — The Leakage Horror Story (10 min)

**Tell this story to the class, slowly, letting it land:**

*"A team at a fintech startup built a churn model. In testing, it scored 98% accuracy — everyone was thrilled, the model got approved for production. Three months after launch, the retention team noticed something odd: the model's real-world predictions were barely better than a coin flip. What happened?"*

Pause for guesses — let 2-3 students speculate before revealing.

**Reveal:** *"They had written `scaler.fit_transform(X)` on the ENTIRE dataset — before splitting into train and test. That means the scaler's mean and standard deviation were computed using information from rows that were LATER placed in the 'test' set. The test set was no longer truly unseen — a sliver of its statistical information had already leaked into training, through the back door. The 98% was a mirage."*

**Ask:** *"The code ran without a single error. No exception, no warning, nothing red on screen. How would you even catch a bug like this?"*

Let students discuss for a minute — the answer, which you confirm, is: you catch it by having a strict PROCESS (fit only on train, inside a `Pipeline`), not by hoping to spot it by eye. Bugs like this are invisible in the code's output; they only show up as a gap between "reported" performance and "real" performance, often months later.

**Say:** *"Today's entire session is about building the muscle memory that makes this bug structurally impossible to write, using two scikit-learn tools: `Pipeline` and `ColumnTransformer`. By the end, you'll also be able to spot two OTHER leakage patterns beyond this one, because they show up constantly in real projects and in interview questions."*

**Learning contract for today — write on board:**

- Explain why `Pipeline` prevents the exact bug in the horror story
- Build a `ColumnTransformer` that treats numeric and categorical columns differently
- Choose the right encoder/scaler for a given feature type
- Name three distinct data leakage patterns and their fixes

---

## SEGMENT 2: Why Pipeline Over Manual Steps (15 min)

### Live-Coding the Buggy Version (7 min)

**Say:** *"Let's first see the 'manual' approach that causes the horror-story bug, so you recognize it instantly if you ever see it in the wild — including in a code review you're asked to do. Then we'll see why `Pipeline` makes the bug structurally impossible."*

**Live-code the buggy version first, label it clearly as WRONG on the board:**

```python
# --- THE WRONG WAY (do not do this) ---
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

df = pd.read_csv("raw_customers.csv")
numeric_cols = ["age", "income"]

scaler = StandardScaler()
df[numeric_cols] = scaler.fit_transform(df[numeric_cols].fillna(df[numeric_cols].mean()))
# ^ fit_transform ran on the WHOLE dataframe, before any split existed

X_train, X_test, y_train, y_test = train_test_split(
    df[numeric_cols], df["churned"], test_size=0.2, random_state=42
)
```

**Run it (it works without error — that's the point) and say:** *"By the time we split, `scaler` has already 'seen' every row, including what becomes the test set. The mean and standard deviation baked into `scaler` were partly computed FROM `X_test`'s own rows. That's leakage — and notice, again, that Python gave us zero warning."*

**Ask:** *"If I asked you to prove, just by reading this code, that leakage happened here — what would you point to?"* Guide toward: the line where `fit_transform` is called BEFORE `train_test_split` even exists in the code.

### Live-Coding the Correct Version (8 min)

**Say:** *"Now the correct version, using `Pipeline`."*

```python
# --- THE RIGHT WAY ---
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import pandas as pd

df = pd.read_csv("raw_customers.csv")
X = df[["age", "income"]]
y = df["churned"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

pipe = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler()),
    ("model", LogisticRegression(max_iter=1000)),
])
pipe.fit(X_train, y_train)
print("Test accuracy:", pipe.score(X_test, y_test))
```

**Run it and talk through the ORDER of operations, pointing at each line as you speak:**

*"Notice the order: split FIRST, then `pipe.fit(X_train, y_train)`. Inside `.fit()`, the imputer and scaler compute their statistics using ONLY `X_train`. When we later call `pipe.score(X_test, ...)` or `pipe.predict(X_test)`, the pipeline internally calls `.transform()` — NOT `.fit_transform()` — on the test data, reusing the train-derived statistics. The test set's own values never get a chance to influence those statistics."*

**Say, writing this on the board in capital letters:** `FIT ON TRAIN. TRANSFORM ON TEST. NEVER THE REVERSE.`

**Ask a comprehension check:** *"If I called `pipe.fit(X_test, y_test)` by accident instead of `pipe.fit(X_train, y_train)`, what would go wrong, even though the code would still run without an error?"* Guide to: the model would be trained on the wrong (and much smaller) dataset, and "test" performance measured afterward on the true training data would be misleadingly optimistic and meaningless as an honest evaluation.

---

## SEGMENT 3: Practical — Inspecting raw_customers.csv (10 min)

**Say:** *"Before building anything, let's actually look at what we're working with. `raw_customers.csv` has two numeric columns (`age`, `income`) and two categorical columns (`city`, `plan_type`) — and BOTH `income` and `plan_type` have missing values, which is exactly what real-world data looks like."*

**Live-code, step by step, running each line and pausing to discuss:**

```python
import pandas as pd

df = pd.read_csv("raw_customers.csv")
print(df.head(10))
```

**Run it.** Point out the blank cells visible in `income` and `plan_type` for some rows.

```python
print(df.isna().sum())
```

**Run it and read the counts aloud.** **Say:** *"This single line is the fastest way to see, column by column, exactly how much cleanup work we have ahead of us."*

```python
print(df.dtypes)
```

**Run it.** **Say:** *"`age` and `income` are numeric dtypes; `city` and `plan_type` are `object` (text). This distinction is EXACTLY what will drive our `ColumnTransformer` design in a few minutes — numeric columns need imputation and scaling, text columns need imputation and encoding."*

```python
print(df["city"].value_counts())
print(df["plan_type"].value_counts(dropna=False))
```

**Run it.** **Say:** *"`city` has exactly three clean values: Pune, Delhi, Mumbai. `plan_type` has three real values plus some missing ones — `dropna=False` makes the missing count visible in the output instead of silently excluding it."*

**Ask:** *"Already, just from this exploration, can anyone guess which imputation strategy makes sense for `income` — mean, median, or most frequent? What about for `plan_type`?"* Guide to: `income` is numeric and likely to have some skew (a few high earners), so median is often safer than mean; `plan_type` is categorical, so "most frequent" is the natural choice since you can't average category labels.

---

## SEGMENT 4: ColumnTransformer Live Build (25 min)

### Numeric Sub-Pipeline (7 min)

**Say:** *"We need different treatment for numeric vs categorical columns, and we need to handle the missing values in each. `ColumnTransformer` lets us define that per-column-type recipe once, cleanly."*

```python
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler

numeric_features = ["age", "income"]
numeric_pipe = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler()),
])
```

**Talk through:** *"`SimpleImputer(strategy="median")` fills missing `income` values with the median income — computed ONLY from training rows, once we plug this into the full pipeline and call `.fit()`. Then `StandardScaler` rescales both columns to mean 0, standard deviation 1, so `age` (tens) and `income` (tens of thousands) sit on comparable scales for the model. Without this, a model could mistakenly treat `income`'s huge raw numbers as inherently 'more important' than `age`'s small ones, purely due to scale."*

### Categorical Sub-Pipeline (8 min)

```python
from sklearn.preprocessing import OneHotEncoder

categorical_features = ["city", "plan_type"]
categorical_pipe = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("onehot", OneHotEncoder(handle_unknown="ignore")),
])
```

**Talk through:** *"For categorical columns we can't take a 'median' of text, so we impute the missing `plan_type` values with the most frequent category instead. Then `OneHotEncoder` turns each category into its own 0/1 column — `city` becomes three columns: `city_Pune`, `city_Delhi`, `city_Mumbai`. A Pune customer gets a 1 in `city_Pune` and 0s everywhere else."*

**Ask:** *"Why can't we just assign city_Pune=1, city_Delhi=2, city_Mumbai=3 as a single numeric column instead of three separate 0/1 columns?"* Guide to: that would falsely imply Mumbai is somehow "three times" Pune, or that Delhi sits "between" them numerically — a fake ordering the model would try to learn from, when none actually exists.

### Combining with ColumnTransformer (5 min)

```python
from sklearn.compose import ColumnTransformer

preprocessor = ColumnTransformer(transformers=[
    ("num", numeric_pipe, numeric_features),
    ("cat", categorical_pipe, categorical_features),
])
```

**Say:** *"Each entry in `transformers` is a tuple: a name we choose, the sub-pipeline to apply, and the list of column names it applies to. `ColumnTransformer` runs each sub-pipeline on its own slice of columns, then stitches all the results back together, side by side, into one combined feature matrix."*

### Full Pipeline and Fit (5 min)

```python
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

X = df[["age", "income", "city", "plan_type"]]
y = df["churned"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

full_pipe = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("model", LogisticRegression(max_iter=1000)),
])
full_pipe.fit(X_train, y_train)
print("Test accuracy:", full_pipe.score(X_test, y_test))
print(full_pipe.named_steps.keys())
```

**Run it live**, then inspect the expanded feature names:

```python
feature_names = full_pipe.named_steps["preprocessor"].get_feature_names_out()
print(feature_names)
```

**Run it and read the printed names aloud** — point out how `age` and `income` pass through with their original names prefixed `num__`, while `city` and `plan_type` have expanded into multiple `cat__city_...` and `cat__plan_type_...` columns. **Say:** *"This one array tells you exactly what the model actually 'sees' under the hood — always worth printing when debugging a pipeline."*

---

## BREAK (10 min)

*Suggested break prompt:* Ask students to think of one column from any dataset they've worked with in Module 1 that had missing values, and come back ready to say whether they'd have used mean, median, or most-frequent imputation for it.

---

## SEGMENT 5: Encoding & Scaling Decision Guide (15 min)

### Building the Guide Together (8 min)

**Say:** *"Not every column deserves the same treatment. Let's build a decision guide together on the board — I'll ask, you propose the 'why,' and I'll fill in the table."*

| Feature type | Strategy | Why |
|---|---|---|
| Numeric, no natural order (`income`) | `StandardScaler` | Puts wildly different numeric ranges on the same footing |
| Categorical, no order (`city`) | `OneHotEncoder` | Avoids implying a fake ranking between Pune/Delhi/Mumbai |
| Categorical, ordered (e.g. `plan_type`: Basic < Standard < Premium) | `OrdinalEncoder` with explicit order | Preserves genuine rank information a model can use directly |
| Missing values | `SimpleImputer` | Fills gaps before anything downstream runs |

### The Ordinal Exception (7 min)

**Ask the class:** *"Our `plan_type` column (Basic, Standard, Premium) actually DOES have a natural order — Premium is objectively 'more' than Basic. Would `OneHotEncoder` or `OrdinalEncoder` make more sense here?"*

Guide the discussion to: either can technically work, but `OrdinalEncoder` with an explicit `categories=[["Basic", "Standard", "Premium"]]` preserves the "Premium > Standard > Basic" relationship as a single numeric column (0, 1, 2), which can help a linear model use one coefficient instead of two separate one-hot coefficients to capture the same underlying trend.

**Live-code the alternative, for contrast:**

```python
from sklearn.preprocessing import OrdinalEncoder

plan_order = OrdinalEncoder(categories=[["Basic", "Standard", "Premium"]])
sample = pd.DataFrame({"plan_type": ["Basic", "Premium", "Standard", "Basic"]})
encoded = plan_order.fit_transform(sample)
print(encoded)
```

**Run it and read the output** — `[[0.], [2.], [1.], [0.]]`. **Say:** *"Notice the encoder respects the ORDER we specified, not alphabetical order. If we'd left `categories` as default 'auto,' it would have sorted alphabetically — Basic, Premium, Standard — which would have wrongly implied Premium sits BETWEEN Basic and Standard. Always specify `categories` explicitly for ordinal data."*

**Say, closing the block:** *"For today's lab we'll keep using `OneHotEncoder` on both categorical columns for simplicity and consistency — but now you know the ordinal alternative exists, and when to reach for it in a real project."*

---

## SEGMENT 6: Data Leakage Patterns (15 min)

### Pattern 2 — Target-Derived Features Computed Globally (6 min)

**Say:** *"We've already seen leakage pattern #1 — fitting a scaler before splitting. There are two more patterns you need to recognize, because they're sneakier."*

**Say:** *"Imagine engineering a feature like 'average churn rate for this customer's city,' computed once across the WHOLE dataset before splitting."*

**Live-code the leaky version to make it concrete:**

```python
# --- LEAKY: computed on the full dataset before splitting ---
city_churn_rate = df.groupby("city")["churned"].mean()
df["city_avg_churn"] = df["city"].map(city_churn_rate)
print(df[["city", "churned", "city_avg_churn"]].head())
```

**Run it.** **Say:** *"Even though this doesn't touch `X_test`'s raw FEATURES directly, it indirectly encodes information from test rows' churn OUTCOMES into a feature the model will see during training — because every row's `city_avg_churn` was computed using the full dataset, test rows included. The fix: compute any such target-derived statistic using ONLY training rows, and ideally inside each cross-validation fold if you're doing CV."*

```python
# --- FIXED: compute the statistic from training rows only ---
X_train, X_test, y_train, y_test = train_test_split(df, df["churned"], test_size=0.2, random_state=42, stratify=df["churned"])
train_city_rate = X_train.groupby("city")["churned"].mean()
X_train = X_train.copy()
X_test = X_test.copy()
X_train["city_avg_churn"] = X_train["city"].map(train_city_rate)
X_test["city_avg_churn"] = X_test["city"].map(train_city_rate)  # reuse TRAIN-derived rates
print(X_test[["city", "city_avg_churn"]].head())
```

**Run it and point out:** *"Notice `X_test`'s new column is built by mapping through `train_city_rate` — a lookup table derived ONLY from training rows. The test set's own churn outcomes never influenced this feature."*

### Pattern 3 — Duplicate Rows Across Train and Test (5 min)

**Say:** *"If the same customer record appears twice in your raw data — maybe from two different data exports, or a scraping job that ran twice — and one copy lands in train, one in test, the model can effectively 'memorize' that exact row instead of generalizing. Its performance on that duplicated test row will look artificially perfect, inflating your overall test score."*

```python
print("Duplicate rows:", df.duplicated().sum())
df_clean = df.drop_duplicates()
print("Rows before:", len(df), "Rows after de-duplication:", len(df_clean))
```

**Run it.** **Say:** *"The fix is simple: de-duplicate BEFORE splitting, every time, as a standard first step in any data preparation workflow."*

### Summary Flow (4 min)

Draw this on the board:

```
Split first --> Fit preprocessing on train only --> Transform test with
train-fitted parameters --> No leakage
```

**Say:** *"The single sentence to internalize: `Pipeline` plus `cross_val_score` together make pattern #1 structurally impossible, because each CV fold refits the ENTIRE pipeline — including the imputer and scaler — using only that fold's training rows. That's one of the biggest reasons to always wrap preprocessing in a `Pipeline` rather than doing it by hand, and it's why we spent the first half of today building one from scratch instead of skipping straight to `fit_transform` on the whole dataframe."*

---

## SEGMENT 7: Lab — Leak-Proof Pipeline (15 min)

### Instructions (read aloud, step by step)

1. Load `raw_customers.csv` with pandas. Print `.isna().sum()` to confirm which columns have missing values.
2. Split `X` (all columns except `customer_id` and `churned`) and `y` (`churned`) with `train_test_split(test_size=0.25, random_state=42, stratify=y)`.
3. Build `numeric_pipe` (impute median, then scale) for `["age", "income"]`.
4. Build `categorical_pipe` (impute most frequent, then one-hot encode with `handle_unknown="ignore"`) for `["city", "plan_type"]`.
5. Combine both into a `ColumnTransformer`, then wrap in a full `Pipeline` with a `LogisticRegression(max_iter=1000)` as the final step.
6. Run `cross_val_score(full_pipe, X_train, y_train, cv=5)` and print the mean.
7. Finally, fit on the full training set and report `full_pipe.score(X_test, y_test)`.

### Starter Code

```python
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LogisticRegression

df = pd.read_csv("raw_customers.csv")
print(df.isna().sum())

X = df.drop(columns=[___, ___])
y = df[___]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=___, random_state=42, stratify=y)

numeric_pipe = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy=___)),
    ("scaler", ___()),
])
categorical_pipe = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy=___)),
    ("onehot", OneHotEncoder(handle_unknown=___)),
])
preprocessor = ColumnTransformer(transformers=[
    ("num", numeric_pipe, [___, ___]),
    ("cat", categorical_pipe, [___, ___]),
])
full_pipe = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("model", ___(max_iter=1000)),
])

scores = cross_val_score(full_pipe, X_train, y_train, cv=5)
print("CV mean:", scores.mean())

full_pipe.fit(X_train, y_train)
print("Test score:", full_pipe.score(X_test, y_test))
```

### Reference Solution

```python
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LogisticRegression

df = pd.read_csv("raw_customers.csv")
print(df.isna().sum())

X = df.drop(columns=["customer_id", "churned"])
y = df["churned"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)

numeric_pipe = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler()),
])
categorical_pipe = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("onehot", OneHotEncoder(handle_unknown="ignore")),
])
preprocessor = ColumnTransformer(transformers=[
    ("num", numeric_pipe, ["age", "income"]),
    ("cat", categorical_pipe, ["city", "plan_type"]),
])
full_pipe = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("model", LogisticRegression(max_iter=1000)),
])

scores = cross_val_score(full_pipe, X_train, y_train, cv=5)
print("CV mean:", scores.mean())

full_pipe.fit(X_train, y_train)
print("Test score:", full_pipe.score(X_test, y_test))
```

**Instructor circulates**, watching specifically for two mistakes: students calling `.fit_transform()` on `X_test` anywhere, and students forgetting `handle_unknown="ignore"` on the encoder (which would crash if a category appears in test but not train — unlikely with this dataset's three fixed cities, but worth calling out as a defensive habit).

---

## SEGMENT 8: Summary, Wrap-Up & Q&A (5 min)

**What we covered today:**
- The exact leakage bug that inflated a real model's reported accuracy to a meaningless 98%
- `Pipeline` structurally prevents "fit before split" leakage by fitting transformers only inside `.fit(X_train, ...)`
- `ColumnTransformer` applies different recipes to numeric vs categorical columns and stitches results together
- Decision guide: `StandardScaler` for numeric, `OneHotEncoder` for unordered categories, `OrdinalEncoder` for ordered ones
- Three leakage patterns: fit-before-split, globally-computed target-derived features, duplicate rows across train/test

**Bridge to next session:** *"You now have a preprocessing recipe you'll reuse for the rest of this module: split first, then `Pipeline` + `ColumnTransformer`, fit once, transform everywhere. Next session is a master class — we step back from code entirely and build the mathematical intuition for lines, residuals, and gradient descent, which is the engine underneath every regression model we train starting Session 4."*

**Homework / self-practice:**
1. Take `raw_customers.csv` and swap the numeric imputation strategy from `"median"` to `"mean"` — does the test score change noticeably? Why might it or might not?
2. Rewrite the categorical pipeline to use `OrdinalEncoder` for `plan_type` specifically (with an explicit category order) while keeping `OneHotEncoder` for `city`. This requires splitting the categorical `ColumnTransformer` entry into two separate entries.
3. Write, in your own words, a one-paragraph explanation of why `Pipeline` + `cross_val_score` together prevent leakage pattern #1 automatically.

---

## Q&A & Doubt Solving

**Likely questions and suggested answers:**

**Q: Do I always need a `ColumnTransformer`, even if all my features are numeric?**
→ No — if every feature is numeric, a plain `Pipeline` with just an imputer and scaler (no `ColumnTransformer`) works fine. `ColumnTransformer` earns its keep specifically when you have DIFFERENT column types needing different treatment.

**Q: What happens if I call `.transform()` on a `Pipeline` that hasn't been fit yet?**
→ scikit-learn raises a `NotFittedError`. This is a helpful guardrail — it prevents you from accidentally transforming data with statistics that don't exist yet.

**Q: Can I put feature engineering (like the `city_avg_churn` example) inside a `Pipeline` too, to avoid leakage automatically?**
→ Yes, with a custom transformer (subclassing scikit-learn's `TransformerMixin`), which is beyond today's scope but worth knowing exists — it's the professional-grade fix for pattern #2 leakage, ensuring the target-derived statistic is always recomputed per-fold automatically.

**Q: Why `handle_unknown="ignore"` specifically, instead of some other setting?**
→ Without it, `OneHotEncoder` raises an error the moment it sees a category at prediction time that it never saw during training (e.g. a new city added to the business next year). `"ignore"` instead encodes that unseen category as all-zeros across its one-hot columns, letting the pipeline keep running gracefully.

**Q: Is median imputation always better than mean imputation?**
→ Not always — median is more robust to outliers/skew (a few very high incomes won't drag it up the way they would a mean), which is why it's often a safer DEFAULT for numeric columns. But for a genuinely symmetric, outlier-free column, mean and median will barely differ.

**Q: If I have a LOT of missing data in one column — say 80% missing — should I still impute it?**
→ Worth pausing on. At that level of missingness, imputation may just be inventing most of a column's values. Consider whether to drop the column entirely, or add a separate "was this missing" indicator flag alongside the imputed value, so the model can learn from the missingness pattern itself if it's informative.

---

## Instructor Notes

- **Prerequisite check:** Confirm in the first five minutes that everyone recalls `train_test_split` and `cross_val_score` from Session 1 — today builds directly on top of both.
- **Common mistake:** Writing `fit_transform` on `X_test` "just to be safe" or "to make sure it processes correctly" — this is the single most common student error today. Catch it immediately and connect it back to the opening horror story every time you see it.
- **Another common mistake:** Forgetting `handle_unknown="ignore"`, then being confused by a `ValueError` if their lab code happens to encounter this in a stress test. Pre-empt by asking students to intentionally test their pipeline on a manufactured row with a fictional city name.
- **Engagement tip:** The two-versions-side-by-side approach (WRONG code, then RIGHT code) in SEGMENT 2 is the strongest teaching moment of the day — don't rush past the WRONG version; let students actually run it and see it "succeed" with no errors before revealing why it's dangerous.
- **Time check:** If running behind before the break, shorten SEGMENT 3's data inspection to just `.isna().sum()` and `.dtypes`, skipping the `value_counts()` walkthrough.
- **If running long after the break:** Compress SEGMENT 6's Pattern 3 (duplicates) to a 2-minute mention rather than a live-coded demo; keep Pattern 2 (target-derived features) as the priority since it's the subtler and more commonly tested concept.
- **Materials to prepare:** `raw_customers.csv` open and ready; a scratch notebook with the WRONG/RIGHT code pair from SEGMENT 2 pre-typed but not yet run, so it can be revealed live.

---

## Common Errors — Quick Reference

| Bug / mistake | Symptom | Fix |
|---|---|---|
| `fit_transform()` on the full dataset before splitting | Suspiciously high test accuracy that fails to hold in production | Split first; fit only within `Pipeline.fit(X_train, ...)` |
| `fit_transform()` called on `X_test` anywhere | Same leakage as above, just relocated | Always use `.transform()` (not `.fit_transform()`) on test/validation data |
| Missing `handle_unknown="ignore"` on `OneHotEncoder` | Crash (`ValueError`) when an unseen category appears at inference time | Add `handle_unknown="ignore"` |
| Target-derived feature computed on the full dataset | Subtle leakage; test scores look better than real-world performance | Compute the statistic from training rows only, then map it onto test rows |
| Duplicate rows split across train and test | Inflated test score from memorized duplicate rows | `df.drop_duplicates()` before splitting |
| Leaving `customer_id` in the feature matrix | Model performance looks suspiciously perfect or unstable | Drop identifier columns before building `X` |

---

## Appendix: Leakage Pattern Recognition Drill (Optional, If Time Allows)

Read each snippet aloud; students identify WHICH leakage pattern (if any) applies:

1. `scaler.fit(df); X_train, X_test = train_test_split(df)` → Pattern 1 (fit before split)
2. `df["region_avg_price"] = df.groupby("region")["price"].transform("mean")` computed on the full dataset, used as a feature → Pattern 2 (target/global statistic leak, if `price` is also the target or closely tied to it)
3. `df = df.drop_duplicates(); X_train, X_test = train_test_split(df)` → No leakage — this is the FIX being applied correctly
4. `pipe.fit(X_train, y_train); pipe.score(X_test, y_test)` → No leakage — correct usage
5. `imputer.fit(X); X_train, X_test = train_test_split(imputer.transform(X))` → Pattern 1 (fit before split, just applied to an imputer instead of a scaler)

---

## FAQ — Additional Questions

**Q: Does the ORDER of steps inside a `Pipeline` matter?**
→ Yes — each step's output feeds into the next step's input. Imputation must happen before scaling (you can't scale a `NaN`), and both must happen before the final estimator. `ColumnTransformer` entries can run in any order relative to each other since they operate on disjoint column sets, but within each sub-pipeline, order matters.

**Q: Can I inspect what a `ColumnTransformer` actually produced, as a plain array or DataFrame, for debugging?**
→ Yes: `preprocessor.fit_transform(X_train)` returns the transformed array directly, and `preprocessor.get_feature_names_out()` gives you the matching column names — extremely useful when a downstream model behaves unexpectedly and you want to inspect exactly what it's being trained on.

**Q: What if two different categorical columns need genuinely different encoders (one ordinal, one one-hot)?**
→ Give `ColumnTransformer` more than two entries — one per distinct treatment needed, each naming its own subset of columns. There's no limit to how many transformer entries you can define.

**Q: Is it ever acceptable to compute summary statistics (like a global mean for reporting/EDA) on the full dataset?**
→ Yes — for pure EXPLORATION and reporting purposes (not model training), using the full dataset is completely fine and standard. Leakage specifically refers to information flowing into your TRAINING process from data the model will later be evaluated against. Know which mode you're in.

---

## SEGMENT 9: Supplemental Code Demos (Instructor Optional, If Time or Advanced Group)

### Demo A — Inspecting imputed values directly (4 min)

```python
import pandas as pd
from sklearn.impute import SimpleImputer

df = pd.read_csv("raw_customers.csv")
imputer = SimpleImputer(strategy="median")
income_before = df[["income"]]
income_after = imputer.fit_transform(income_before)

comparison = pd.DataFrame({
    "before": income_before["income"].values,
    "after": income_after.flatten(),
})
print(comparison[df["income"].isna()])
```

**Break it down:**
- Filtering `comparison` to only the originally-missing rows shows exactly what value each `NaN` was replaced with
- Every missing row gets the SAME median value here, since we used a single imputer on one column
- This kind of before/after inspection is a great debugging habit whenever imputation results look off

**Ask:** What would change if we used `strategy="mean"` instead — would every missing row still get the same value?

**Common mistake:** Assuming imputation "guesses" a different value per row based on other columns — plain `SimpleImputer` does not do this; it always fills with one global statistic per column.

**Fix:** For row-aware imputation (using other columns to make a smarter guess), scikit-learn offers `KNNImputer` or `IterativeImputer` — worth a one-line mention as "further reading," not needed today.

### Demo B — Visualizing what OneHotEncoder actually built (4 min)

```python
from sklearn.preprocessing import OneHotEncoder
import pandas as pd

sample = pd.DataFrame({"city": ["Pune", "Delhi", "Mumbai", "Pune"]})
encoder = OneHotEncoder(sparse_output=False)
encoded = encoder.fit_transform(sample)

result = pd.DataFrame(encoded, columns=encoder.get_feature_names_out())
print(result)
```

**Break it down:**
- `sparse_output=False` forces a readable dense array instead of a memory-efficient sparse matrix, purely for this demo
- Each row gets exactly one `1` and the rest `0`s — a clean one-hot pattern
- `get_feature_names_out()` labels each column so you can see precisely which category each 1 represents

**Ask:** How many total columns would we get if `city` had 20 unique values instead of 3?

**Common mistake:** Not realizing one-hot encoding a high-cardinality column (hundreds of unique categories) can explode the feature matrix's width dramatically.

**Fix:** For high-cardinality categoricals, consider grouping rare categories into an "Other" bucket first, or using a different encoding strategy (target encoding, hashing) — flagged as advanced, not needed for this dataset.

### Demo C — Full pipeline with a different final model (3 min)

```python
from sklearn.tree import DecisionTreeClassifier

tree_pipe = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("model", DecisionTreeClassifier(random_state=42, max_depth=3)),
])
tree_pipe.fit(X_train, y_train)
print("Decision tree test score:", tree_pipe.score(X_test, y_test))
```

**Break it down:**
- The SAME `preprocessor` object is reused — only the final model step changed
- This is the real payoff of `Pipeline`: preprocessing logic is written once and works with any downstream estimator
- Session 9 covers `DecisionTreeClassifier` properly; this is just a preview using vocabulary students already have

**Ask:** Why didn't we need to rebuild `numeric_pipe` or `categorical_pipe` at all for this new model?

**Common mistake:** Rebuilding preprocessing from scratch every time a different model is tried.

**Fix:** Keep `preprocessor` as a standalone, reusable object exactly like this demo does.

---

## Materials Checklist

- [ ] `raw_customers.csv` open and readable in the working notebook environment
- [ ] Scratch notebook with the WRONG/RIGHT code pair from SEGMENT 2 pre-typed but not yet run
- [ ] Whiteboard space for the encoding/scaling decision guide table
- [ ] Timer visible to students for the lab segment
- [ ] Optional: projector demo notebook pre-loaded with the SEGMENT 4 ColumnTransformer build

---

## Timing Contingencies

| Situation | Action |
|---|---|
| Running 10 min behind before break | Shorten SEGMENT 3's data inspection to just `.isna().sum()` and `.dtypes` |
| Running long after break | Compress SEGMENT 6's Pattern 3 (duplicates) to a 2-minute mention; keep Pattern 2 as priority |
| Low energy after lunch/break | Run the Appendix leakage-pattern recognition drill as a quick energizer quiz |
| Advanced group finishes lab early | Assign Demo A or Demo B as a stretch task, or the OrdinalEncoder homework early |
| No shared screen / projector issue | Read code blocks aloud and have students type along from the printed lecture script |

---

## End-of-Session Quiz (5 Questions)

1. What line of code, and in what order relative to `train_test_split`, causes the classic "fit before split" leakage bug?
2. Why does `OneHotEncoder` need `handle_unknown="ignore"` in a production pipeline?
3. Name the three leakage patterns covered today, each in one sentence.
4. When would you prefer `OrdinalEncoder` over `OneHotEncoder`?
5. Why does using the SAME `preprocessor` object across two different final models (as in Demo C) matter?

**Answer key (instructor):**
1. Calling `.fit()` or `.fit_transform()` on a scaler/imputer using the FULL dataset, BEFORE calling `train_test_split`.
2. So the pipeline doesn't crash when it encounters a category at inference time that it never saw during training.
3. (1) Fitting preprocessing on the full dataset before splitting. (2) Computing target-derived features using the full dataset instead of training rows only. (3) Duplicate rows split across train and test, letting the model "memorize" a row it's also evaluated on.
4. When the categorical feature has a genuine, meaningful order (e.g. Basic < Standard < Premium) that a single ordered numeric column can represent faithfully.
5. It proves the preprocessing logic is decoupled from the model choice — write once, reuse with any estimator, guaranteeing consistent treatment of the data regardless of which model is being compared.

---

## Homework Rubric

| Criterion | Excellent (4) | Good (3) | Needs Work (2) | Incomplete (1) |
|---|---|---|---|---|
| Mean vs median imputation comparison | Clear numeric comparison with a correct explanation of any difference | Comparison present, thin explanation | Numbers reported, no explanation | Not attempted |
| OrdinalEncoder rewrite for plan_type | Correctly splits ColumnTransformer entries, explicit category order set | Mostly correct, minor issues (e.g. missing explicit order) | Attempted but non-functional | Not attempted |
| Leakage-prevention paragraph | Clear, correct, references Pipeline + cross_val_score refitting per fold | Mostly correct, some vagueness | Attempted, misses the core mechanism | Not attempted |

**Total:** /12 — Pass threshold: 8/12
