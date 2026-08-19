# Lecture Script: ML Workflow & Problem Framing
> **Instructor Reference** — Module 2: Classical ML | Session 1 | Duration: 2 Hours

---

## Session Overview

**Goal:** Students can frame a vague business ask as a precise ML problem, split data correctly with `train_test_split`, and use `cross_val_score` for a trustworthy performance estimate — before writing any real model code.

**Student profile at this point:** Comfortable with Python, pandas, and basic EDA from Module 1. This is their first exposure to scikit-learn's modeling workflow, and their first time hearing terms like "target variable," "stratify," and "cross-validation" used precisely.

**Key outcome:** Every student can (1) correctly label a business scenario as regression, classification, or clustering, (2) fill out a 4-question problem-framing worksheet unaided, (3) write a correct `train_test_split` call with stratification, and (4) run and interpret `cross_val_score` output, including reading the standard deviation as a stability signal — all demonstrated on `customers.csv`.

**Dataset for this session:** `customers.csv` (in this folder) — 30 rows of `customer_id`, `age`, `monthly_spend`, `support_tickets`, `tenure_months`, `churned`.

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| SEGMENT 1: Opening & Hook — Why "Just Apply ML" Fails | 10 min | 0:10 |
| SEGMENT 2: Supervised vs Unsupervised | 15 min | 0:25 |
| SEGMENT 3: Problem Framing Worksheet | 20 min | 0:45 |
| SEGMENT 4: Practical — Frame Four Business Scenarios in Pairs | 15 min | 1:00 |
| **BREAK** | 10 min | 1:10 |
| SEGMENT 5: train_test_split & Stratification | 15 min | 1:25 |
| SEGMENT 6: cross_val_score | 15 min | 1:40 |
| SEGMENT 7: Lab — End-to-End Mini-Workflow on customers.csv | 15 min | 1:55 |
| SEGMENT 8: Summary, Wrap-Up & Q&A | 5 min | 2:00 |

---

## SEGMENT 1: Opening & Hook (10 min)

**Say to the class:** *"Raise your hand if you've heard someone — a manager, a founder, a LinkedIn post — say 'let's just throw AI at it' about a business problem."*

Pause, take a show of hands. There will usually be several.

**Write on the board this brief, exactly as given to a fictional junior analyst:**

```
"Make our sales better with ML."
```

**Ask:** *"You've just been handed this exact sentence as your entire project brief. What's wrong with it? What would you need to know before writing a single line of code?"*

Let students call out answers for 2-3 minutes, writing each on the board as it comes up. Steer the discussion toward these four gaps if the class doesn't surface them naturally:

- There is no defined **target variable** — what column, exactly, are we predicting?
- There is no description of what **data** exists to support a prediction — do we even have historical sales records with the right structure?
- There is no stated **success metric** — how will we know, in a measurable way, if the model "worked"?
- There is no mention of **what decision** the prediction will actually drive — will a human read a dashboard? Will a system auto-adjust pricing?

**Say:** *"Every session from here on assumes you've cleared these four gaps before touching scikit-learn. Today is entirely about that clearing process, plus the two lines of code — `train_test_split` and `cross_val_score` — that keep you honest once you do start modeling. By the end of today, if someone hands you 'make our sales better with ML,' you'll have a repeatable process to turn that into something you could actually build."*

**Context to set — course arc:**

**Say:** *"Module 1 was about wrangling and understanding data. Module 2, which starts today, is about turning that data into predictions. Every session in this module builds on the last: today's framing skills, next session's clean pipelines, the math master class after that, and then regression, regularization, classification, and ensembles. Skipping today's foundation is the single most common reason real-world ML projects fail — not bad algorithms, bad framing."*

**Learning contract for today — write on board:**

- Tell supervised and unsupervised learning apart, instantly, for any scenario
- Fill out a 4-question problem-framing worksheet without hesitation
- Split data correctly with `train_test_split`, including when and why to use `stratify`
- Run `cross_val_score` and read BOTH the mean and the standard deviation

---

## SEGMENT 2: Supervised vs Unsupervised (15 min)

### The One Deciding Question (5 min)

**Say:** *"The single most important question in framing any ML problem is: do we have a column that records the actual, historical outcome we want to predict? If yes, we're in supervised learning territory. If no — we just have a pile of records and want to find structure in them — we're in unsupervised territory."*

Draw this on the board:

```
Do you have labelled outcomes?
        |
   ---------------
   |             |
  YES            NO
   |             |
Supervised    Unsupervised
   |             |
 number?      find groups
 or category?  (clustering)
   |    |
Regression Classification
```

**Write the comparison table on the board:**

| | Supervised | Unsupervised |
|---|---|---|
| Has labels in training data? | Yes | No |
| Example question | "Will this customer churn?" | "What customer groups exist?" |
| Typical algorithms (later sessions) | Linear/logistic regression, decision trees | K-means clustering |
| How you evaluate it | Compare prediction to known answer | Harder — needs business judgment |

**Say:** *"Notice something important: the deciding question is never 'is this hard' or 'do we have lots of data.' It is specifically: is there a known outcome column sitting in our historical data right now?"*

### Regression vs Classification vs Clustering (5 min)

**Say:** *"Within supervised learning, there's a second question: is the outcome a NUMBER or a CATEGORY? That decides regression vs classification."*

| ML task | Question it answers | Output type | Example |
|---|---|---|---|
| Regression | How much? / How many? | A number | Predict next month's revenue |
| Classification | Which category? | A label (yes/no, A/B/C) | Will this customer churn? |
| Clustering | What groups naturally exist? | Segments (no predefined labels) | Discover customer personas |

**Walk through four examples out loud, asking the class to vote before you reveal the answer. Cold-call individual students for each:**

1. *"Predicting a house's sale price from its features."* → Ask: supervised or unsupervised? (Supervised.) Number or category? (Number → regression.)
2. *"Grouping retail customers by purchasing behaviour, with no predefined segments given to us."* → Unsupervised, clustering. No "correct" segment label exists anywhere in the data.
3. *"Predicting whether a loan applicant will default."* → Supervised (past defaults are recorded), category → classification.
4. *"Finding which products are frequently bought together, with no target column at all."* → Unsupervised — closer to association/clustering territory, no explicit target.

### Common Misconception to Pre-empt (5 min)

**Say:** *"Here's a trap almost every beginner falls into: thinking 'unsupervised' means 'we have no data' or 'we don't know anything.' That's wrong. Unsupervised models still need PLENTY of good data — they just don't have an answer key column telling them what the 'right' output is for each row."*

**Live-code a tiny illustration using `customers.csv`:**

```python
import pandas as pd

df = pd.read_csv("customers.csv")
print(df.columns.tolist())
print(df[["age", "monthly_spend", "churned"]].head())
```

**Run it and point at the `churned` column specifically.** **Say:** *"This dataset has a `churned` column — 1 or 0 for every row. That's our answer key. Because it exists, predicting churn from this data is a SUPERVISED problem. If I deleted this column entirely and asked you to group these 30 customers into 'similar' clusters using only age, spend, and tickets — that would become an UNSUPERVISED problem, on the exact same rows."*

**Ask:** *"So the same raw dataset can support both a supervised AND an unsupervised project — the difference is purely about whether you're using a labelled target column. True or false?"* (True — reinforce this explicitly.)

---

## SEGMENT 3: Problem Framing Worksheet (20 min)

### Introducing the Worksheet (5 min)

**Say:** *"I'm going to give you a repeatable 4-question worksheet. Use this literally every time a stakeholder hands you a vague ask — treat it as non-negotiable, the same way you'd never skip checking a recipe's ingredient list before cooking."*

Write the four questions on the board, large:

```
1. What DECISION will this prediction drive?
2. What is the TARGET VARIABLE, exactly — name the column?
3. Is the target a NUMBER, a CATEGORY, or is there NO LABEL at all?
4. What does a WRONG prediction COST us?
```

### Worked Example — Churn (10 min)

**Say:** *"Let's fill this out together, live, on the board, for 'reduce customer churn.'"*

**Question 1 — decision:**

**Ask:** *"If we build this model, who acts on the prediction, and what do they DO differently?"* Guide toward: *"Which customers get a proactive retention call from the support team this week."*

**Question 2 — target variable:**

**Ask:** *"Look at `customers.csv` on screen. Which exact column is our target?"* Answer: `churned` — binary, 1 = churned, 0 = stayed.

**Question 3 — label type:**

Since `churned` is 0/1, this is a category → binary classification.

**Question 4 — cost of being wrong:**

**Say:** *"There are two distinct ways to be wrong here. Let's name both."*

Write on the board:

| Error type | What happened | Cost |
|---|---|---|
| False negative | Predicted "stays," but customer actually churns | We lose a customer we could have saved with a retention call |
| False positive | Predicted "churns," but customer actually stays | We waste one retention call on someone who didn't need it |

**Ask the class:** *"Which of those two errors is probably more expensive for a subscription business — losing a paying customer, or making one unnecessary phone call?"*

Guide the discussion to: missing a real churner is usually far costlier than one wasted phone call, because customer lifetime value typically dwarfs the cost of a support call. **Say:** *"Hold onto this insight — it directly previews the precision/recall tradeoff we cover properly in Session 7. For now, just notice: naming the cost of each error type is ALREADY part of problem framing, long before we pick a metric or an algorithm."*

**Say, summarizing:** *"Notice we never once mentioned an algorithm name in this entire worksheet. Algorithm choice is the LAST decision you make in a real project, not the first. Most beginners do this backwards — they pick 'random forest' before they've even named the target column."*

### A Second Worked Example — Faster Pass (5 min)

**Say:** *"Let's do one more, faster, to build the muscle memory. Business ask: 'Help us price our new product listings better.'"*

Rapid-fire with the class, filling the board:

1. *Decision:* What price to display for a new listing before it goes live.
2. *Target:* `fair_market_price` (a number we'd need in historical listing data).
3. *Label type:* Number → regression.
4. *Cost of wrong:* Pricing too high loses sales volume; pricing too low loses margin on every sale. Both costs are real but different in kind — flag this as something the business needs to weigh, not something ML decides for them.

---

## SEGMENT 4: Practical — Frame the Scenarios (15 min)

### Setup (2 min)

**Say:** *"Get into pairs. I'm handing each pair one of four scenario cards. You have 8 minutes to fill out the 4-question worksheet on paper or in a shared doc for your scenario. Then each pair reports back in one sentence."*

**The four scenario cards — write these on the board or hand out as slips:**

| # | Scenario |
|---|---|
| 1 | A hospital wants to predict which discharged patients are likely to be readmitted within 30 days. |
| 2 | A retailer wants to forecast how many units of each product will sell next month. |
| 3 | An email provider wants to automatically flag spam messages. |
| 4 | A marketing team wants to discover natural customer segments from purchase history, with no predefined groups given to them. |

### Working Time (8 min)

**Facilitation:** Walk the room during the 8 minutes. Listen for pairs who try to name an algorithm before finishing the worksheet — redirect them explicitly: *"Hold off on the algorithm name. Finish question 3 first — number, category, or no label?"*

Watch especially for scenario 4 — some pairs will try to force a "target variable" onto it out of habit. If you see this, prompt: *"Does any column in this scenario record a 'correct' segment for each customer? If not, what does that tell you about question 2?"*

### Expected Answers (Instructor Reference — Do Not Hand Out)

| # | Target | Type | Supervised? |
|---|---|---|---|
| 1 | `readmitted_30d` (yes/no) | Category | Yes — classification |
| 2 | `units_sold_next_month` | Number | Yes — regression |
| 3 | `is_spam` (yes/no) | Category | Yes — classification |
| 4 | none — no target column exists | n/a | No — clustering |

### Debrief (5 min)

Have one pair from each scenario read their answer aloud. For scenario 4, explicitly highlight that this is the odd one out — no target variable exists, so it cannot be supervised no matter how the team tries to frame the "output." **Ask the class:** *"What would have to change about the hospital's data for scenario 1 to become unsupervised instead?"* (Answer: if we removed the `readmitted_30d` column entirely and just asked "group these patients by similarity," it becomes unsupervised clustering on the same rows — echoing SEGMENT 2's point.)

---

## BREAK (10 min)

*Suggested break prompt:* Ask students to think of one prediction their own favourite app probably makes about them (a delivery ETA, a "you might also like," a fraud flag) and come back ready to say whether it's regression, classification, or clustering.

---

## SEGMENT 5: train_test_split & Stratification (15 min)

### The Exam Analogy (3 min)

**Say:** *"Imagine a student who studies using yesterday's exact exam paper, then sits the exact same paper again and scores 100%. Did they learn the subject, or did they memorize the answer key? You genuinely cannot tell — because you tested them on material they'd already seen. A model evaluated on its own training data has exactly this problem, and it's one of the most common ways beginners fool themselves."*

### Live Coding — the Split (7 min)

**Live-code this on the projector, using `customers.csv`:**

```python
import pandas as pd
from sklearn.model_selection import train_test_split

df = pd.read_csv("customers.csv")
print(df.head())
print(df["churned"].value_counts())

X = df.drop(columns=["customer_id", "churned"])
y = df["churned"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print("Train shape:", X_train.shape)
print("Test shape:", X_test.shape)
print("Train churn ratio:\n", y_train.value_counts(normalize=True))
print("Test churn ratio:\n", y_test.value_counts(normalize=True))
```

**Talk through each line as you run it:**

- `df.drop(columns=["customer_id", "churned"])` — `customer_id` is an identifier, not a feature. A model that "learns" from an ID number is memorizing rows, not learning patterns. **Say:** *"Always drop pure identifier columns before training. If you ever see `id` show up as an important feature in a model, that's a five-alarm fire — something has gone wrong."*
- `test_size=0.2` — reserve 20% of rows purely for honest evaluation; the model never sees these rows during training.
- `random_state=42` — fixes the random shuffle so the split is reproducible. **Ask:** *"Why does it matter if the split changes every time we rerun the notebook?"* Guide to: comparing two model versions becomes unreliable if they were evaluated on different random test sets.
- `stratify=y` — the critical one for THIS dataset specifically.

### Live Demo — Stratification Matters (5 min)

**Run the split WITHOUT `stratify=y` first, live, and show the ratio drift:**

```python
X_train_bad, X_test_bad, y_train_bad, y_test_bad = train_test_split(
    X, y, test_size=0.2, random_state=7
)
print("Without stratify - train churn ratio:\n", y_train_bad.value_counts(normalize=True))
print("Without stratify - test churn ratio:\n", y_test_bad.value_counts(normalize=True))
```

**Run it a couple of times with different `random_state` values (7, 13, 99) and show the class how the test set's churn ratio can drift noticeably away from the overall 50/50 split on this small 30-row dataset.**

**Say:** *"With a rare or even moderately imbalanced target, an unlucky random split can leave your test set with almost no positive examples at all — making any metric computed on it essentially meaningless. Now watch what happens when we add `stratify=y` back."*

Re-run the original stratified code and show the ratios matching closely between train and test.

**Say:** *"`stratify=y` tells `train_test_split` to preserve the target's class proportions in both the train and test sets. This matters MORE as your dataset gets smaller or your classes get more imbalanced — and we'll see genuinely imbalanced data starting Session 6."*

**Common error to demonstrate live:** Forgetting to drop `customer_id` before training — briefly show `X_train.columns` including `customer_id`, ask *"what's wrong with this feature list?"*, then fix it by re-running the drop.

---

## SEGMENT 6: cross_val_score (15 min)

### Why One Split Isn't Enough (3 min)

**Say:** *"A single train/test split gives you exactly one number. But what if that particular 20% test slice happened to be unusually easy, or unusually hard, just by chance? You'd draw the wrong conclusion about your model's real-world performance. Cross-validation runs the same evaluation multiple times on different slices of the training data and averages the result, so one lucky or unlucky split can't fool you."*

### The 5-Fold Picture (4 min)

Draw this on the board:

```
Training data split into 5 folds: [1][2][3][4][5]

Round 1: train on [2][3][4][5], validate on [1]
Round 2: train on [1][3][4][5], validate on [2]
Round 3: train on [1][2][4][5], validate on [3]
Round 4: train on [1][2][3][5], validate on [4]
Round 5: train on [1][2][3][4], validate on [5]

Final score = average of all 5 validation scores
```

**Say:** *"Notice every single row gets used for validation EXACTLY once across the five rounds, and gets used for training four times. No row is ever wasted, and every row eventually 'proves itself' on a model that never saw it during that particular round."*

### Live Coding (5 min)

**Continuing from the stratified split above:**

```python
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LogisticRegression

model = LogisticRegression(max_iter=1000)
scores = cross_val_score(model, X_train, y_train, cv=5, scoring="accuracy")
print("Fold scores:", scores)
print(f"Mean CV accuracy: {scores.mean():.3f} (+/- {scores.std():.3f})")
```

**Run it and read the printed fold scores aloud, one by one.** **Talk through:**

- `cv=5` — 5-fold cross-validation; the training data is internally split into 5 chunks.
- `scoring="accuracy"` — we're asking for accuracy specifically. scikit-learn supports many other scoring strings we'll use starting Session 7 (`"precision"`, `"recall"`, `"f1"`, `"r2"`, etc.).
- The **mean** is the headline number to report.
- The **standard deviation** tells you how STABLE that number is.

**Say, emphasizing this hard:** *"A mean of 0.90 with a std of 0.01 is a much more trustworthy result than a mean of 0.90 with a std of 0.15 — the second model's performance is swinging wildly depending on which slice of data it happens to see. Never report just the mean. Always report both."*

### Critical Rule (3 min)

**Say, writing this on the board in capital letters:** `NEVER CROSS-VALIDATE ON THE TEST SET.`

**Ask:** *"We called `cross_val_score(model, X_train, y_train, ...)`. What would go wrong if I'd written `X_test, y_test` instead, or even the full `X, y`?"*

Guide to: the test set is supposed to remain completely untouched until the very final evaluation, at the end of the whole project. If you cross-validate on it, or on the full dataset including it, you're back to the exam-with-the-answer-key problem from SEGMENT 5 — just hidden one layer deeper.

---

## SEGMENT 7: Lab — End-to-End Mini-Workflow (15 min)

### Instructions (read aloud)

*"Working individually or in pairs, complete these five steps using `customers.csv` in this folder:"*

1. Load the CSV with pandas and inspect `df["churned"].value_counts()`.
2. In one sentence, write the ML framing: *"Given ___, predict ___."*
3. Split with `train_test_split`, `test_size=0.25`, `random_state=42`, and `stratify=y` — remembering to drop `customer_id` from the features first.
4. Run `cross_val_score` with `cv=5` on a baseline `LogisticRegression(max_iter=1000)`, and print both the mean and the standard deviation.
5. Write one sentence: given the class balance you saw in step 1, would you trust plain accuracy as the metric, or would you want something else? Why?

### Starter Code (put on screen for students who want a scaffold)

```python
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LogisticRegression

df = pd.read_csv("customers.csv")
print(df["churned"].value_counts())

# TODO: write your one-sentence framing here as a comment

X = df.drop(columns=[___, ___])
y = df[___]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=___, random_state=___, stratify=___
)

model = LogisticRegression(max_iter=1000)
scores = cross_val_score(model, X_train, y_train, cv=___, scoring="accuracy")
print(f"Mean: {scores.mean():.3f}, Std: {scores.std():.3f}")

# TODO: write your one-sentence metric justification here as a comment
```

### Reference Solution

```python
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LogisticRegression

df = pd.read_csv("customers.csv")
print(df["churned"].value_counts())

# Framing: Given a customer's age, monthly spend, support tickets, and
# tenure, predict whether they will churn (churned = 1) or stay (0).

X = df.drop(columns=["customer_id", "churned"])
y = df["churned"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

model = LogisticRegression(max_iter=1000)
scores = cross_val_score(model, X_train, y_train, cv=5, scoring="accuracy")
print(f"Mean: {scores.mean():.3f}, Std: {scores.std():.3f}")

# Metric note: churned is roughly balanced in this toy dataset (about 50/50),
# so accuracy is a reasonable first metric here. In a real churn dataset,
# where churners are usually a small minority, plain accuracy would be
# misleading and we'd want precision/recall instead (Session 7).
```

**Instructor circulates** and checks that each student actually wrote the one-sentence framing in step 2 — this is the step students skip when eager to jump straight to code. Cold-call two or three students to read their framing sentence aloud in the last two minutes.

---

## SEGMENT 8: Summary, Wrap-Up & Q&A (5 min)

**What we covered today:**
- Supervised vs unsupervised — the one deciding question is whether a labelled target column exists
- Regression vs classification vs clustering — number, category, or no label
- The 4-question problem-framing worksheet: decision, target, label type, cost of error
- `train_test_split` with `stratify=y` to keep class ratios honest across train/test
- `cross_val_score` — why one split isn't enough, and why you always report mean AND std

**Bridge to next session:** *"Today you learned to ask four questions before writing any modeling code, and two lines — `train_test_split` and `cross_val_score` — that keep every number you report afterward honest. Next session, we deal with a problem every real dataset has: messy, mixed-type, incomplete features. We'll build a `Pipeline` and `ColumnTransformer` that turns raw columns into model-ready inputs — and we'll see, with our own eyes, exactly how sloppy preprocessing order silently leaks test data into training."*

**Homework / self-practice:**
1. Take one app you use daily and identify one feature that's probably a supervised ML prediction. Write its 4-question framing worksheet.
2. Re-run today's lab with `test_size=0.3` instead of `0.25` and compare the CV mean/std — did stability change?
3. Optional: try `cross_val_score` with `cv=3` instead of `cv=5` on the same lab data and compare the standard deviation. Which felt more stable, and why might fewer folds behave differently?

---

## Q&A & Doubt Solving

**Likely questions and suggested answers:**

**Q: Why 5 folds specifically? Why not 10, or 3?**
→ 5 and 10 are the most common defaults — they balance computation cost against stability. More folds means more, smaller validation sets (more stable estimate, more compute); fewer folds means larger validation sets per round but fewer of them. For small datasets like today's, 5 is a sensible default.

**Q: If cross_val_score already evaluates the model, why do we still need a separate test set?**
→ Cross-validation happens entirely on the training data and is typically used to COMPARE models or tune settings. The held-out test set is your final, one-time "real world" check, touched only once your model choice is locked in — never used to make decisions during development.

**Q: What if my dataset has no obvious target column at all?**
→ That's a strong signal you're in unsupervised territory (clustering). Go back to the 4-question worksheet — if question 2 has no answer, question 3 answers itself as "no label," and question 4 (cost of wrong) needs to be reframed around cluster usefulness rather than prediction accuracy.

**Q: Does `random_state=42` have to be 42 specifically?**
→ No — 42 is a popular convention (a nod to "Hitchhiker's Guide to the Galaxy"), but any fixed integer works. What matters is using the SAME value consistently within one experiment so results are reproducible and comparable.

**Q: My cross_val_score mean looks great (0.95) but the std is also fairly large (0.10). Is this a good model?**
→ Not necessarily trustworthy yet. A large std relative to the mean means performance varies a lot depending on which fold you look at — the model might be getting lucky on some slices of data and struggling on others. Investigate further (more data, different features, or a different validation strategy) before declaring victory.

**Q: Can I use stratify on a regression target too?**
→ Not directly — `stratify` expects discrete categories to preserve proportions of. For regression targets, you'd typically bucket the continuous target into ranges first if you wanted stratified sampling, though for most regression problems a plain random split is standard.

---

## Instructor Notes

- **Prerequisite check:** In the first five minutes, quickly confirm students remember `train_test_split` is entirely new territory today, even though `pandas` and basic Python are familiar from Module 1 — don't assume scikit-learn API familiarity.
- **Common mistake:** Students will try to name an algorithm ("let's use random forest!") before finishing the 4-question worksheet. Redirect firmly but kindly every time — this instinct needs correcting early in the module, since it recurs constantly.
- **Another common mistake:** Leaving `customer_id` in the feature matrix. Make this mistake ONCE, visibly, on your own live-coded example, so students recognize the symptom (an oddly "too good" model, or an ID column with a suspiciously high coefficient) rather than only hearing about it in the abstract.
- **Engagement tip:** The stratification demo (running the same split with different `random_state` values, watching the ratio drift) is the strongest "aha" moment of the session — don't rush it, and consider running it three or four times if the room seems unconvinced the first time.
- **Time check:** If running behind before the break, shorten the second worked example in SEGMENT 3 (the pricing scenario) to a quick verbal walkthrough instead of a full board fill-in.
- **If running long after the break:** Trim SEGMENT 6's Q&A live-coding to the single `cross_val_score` block; skip the optional `cv=3` vs `cv=5` comparison and assign it as homework instead.
- **Materials to prepare:** `customers.csv` open and ready in a notebook; four scenario cards (printed or on a shared slide); whiteboard space for the worksheet template.

---

## Common Errors — Quick Reference

| Bug / mistake | Symptom | Fix |
|---|---|---|
| Naming an algorithm before finishing the framing worksheet | Jumps straight to "let's use X" without a target variable named | Redirect to question 2: name the exact target column first |
| Leaving `customer_id` in the feature matrix | Model performance looks suspiciously perfect | `X = df.drop(columns=["customer_id", "churned"])` |
| Forgetting `stratify=y` on an imbalanced or small target | CV scores swing wildly between reruns | Add `stratify=y` to `train_test_split` |
| Calling `cross_val_score` on the full dataset or on `X_test` | Metrics look great but don't hold up in later evaluation | Only ever call it on `X_train, y_train` |
| Reporting only the mean CV score | Hides how stable (or shaky) the result really is | Always print and discuss the standard deviation too |
| Treating "unsupervised" as "no data needed" | Confusion about why clustering still needs a full dataset | Clarify: unsupervised means "no target column," not "no data" |

---

## Appendix: Scenario Classification Answer Key (Instructor Only)

| Scenario | Target | Type | Supervised? |
|---|---|---|---|
| Hospital readmission | `readmitted_30d` | Category | Yes — classification |
| Retail demand forecast | `units_sold_next_month` | Number | Yes — regression |
| Spam detection | `is_spam` | Category | Yes — classification |
| Customer segmentation | none | n/a | No — clustering |
| House price prediction | `sale_price` | Number | Yes — regression |
| Product-bundle discovery | none | n/a | No — clustering / association |
| Loan default prediction | `defaulted` | Category | Yes — classification |

---

## Appendix: Supplemental Framing Drills (Optional, If Time Allows)

### Drill 1 — Rapid classification

Read these aloud one at a time; students shout "regression," "classification," or "clustering":

1. Predicting tomorrow's temperature — Regression
2. Sorting news articles into unlabelled topic groups — Clustering
3. Flagging a credit card transaction as fraud or not — Classification
4. Estimating how many minutes a food delivery will take — Regression
5. Grouping website visitors by browsing pattern with no predefined segments — Clustering

### Drill 2 — Cost-of-error discussion

For each pair, ask which error type (false positive or false negative) is likely more expensive, and why:

| Scenario | Likely costlier error |
|---|---|
| Cancer screening test | False negative — missing a real case is far more dangerous than a false alarm |
| Spam filter | False positive — blocking a real, important email is often worse than one spam message getting through |
| Airport security scanner | False negative — missing a real threat is far more dangerous than extra screening |

**Say when debriefing:** *"This exact conversation — which error costs more — is exactly what you'll formalize with precision and recall in Session 7. Today, just get comfortable naming it in plain English."*

---

## FAQ — Additional Questions

**Q: Is `LogisticRegression` the "right" algorithm to use as a baseline for classification cross-validation, or should I pick something else?**
→ For today, `LogisticRegression` is a fast, simple, well-understood baseline — it trains in milliseconds even on larger data, which makes it perfect for iterating quickly during problem framing and validation-strategy setup. We'll cover it properly, including `predict_proba()`, in Session 6.

**Q: What happens if `stratify=y` is used but the target has a class with only 1 or 2 examples total?**
→ `train_test_split` will raise an error if a class has too few members to be represented proportionally in both splits at the chosen `test_size`. In real projects, this is itself a useful early warning that you may need more data for that rare class before modeling seriously.

**Q: Can cross-validation be used on time-series data the same way?**
→ Not with plain `cross_val_score`'s default random folding — shuffling time-ordered data for validation risks letting the model "see the future." scikit-learn provides `TimeSeriesSplit` for that case, which we mention only briefly here since this course's ML module focuses on tabular, non-time-ordered problems.

**Q: Why does the worksheet ask about "cost of a wrong prediction" before we've even trained anything?**
→ Because it shapes decisions you'll make LATER — which metric to optimize (Session 7), what threshold to use (Session 6), and even whether ML is the right tool at all. Naming the cost upfront prevents you from training a technically accurate model that's still useless for the actual business decision.

---

## SEGMENT 9: Supplemental Code Demos (Instructor Optional, If Time or Advanced Group)

### Demo A — Watching stratification fail on a smaller sample (4 min)

```python
import pandas as pd
from sklearn.model_selection import train_test_split

df = pd.read_csv("customers.csv")
small = df.sample(10, random_state=1)   # shrink to 10 rows to exaggerate the effect
X_small = small.drop(columns=["customer_id", "churned"])
y_small = small["churned"]

for seed in [1, 2, 3]:
    _, _, y_tr, y_te = train_test_split(X_small, y_small, test_size=0.3, random_state=seed)
    print(f"seed={seed} -> test churn ratio: {y_te.mean():.2f}")
```

**Break it down:**
- Shrinking to 10 rows makes the instability from Section 5 dramatically more visible
- Each `random_state` produces a noticeably different test split churn ratio without `stratify`
- This is exactly the failure mode that gets worse as real-world classes get rarer (e.g. 2% fraud rate)

**Ask:** What would you expect to see if we added `stratify=y_small` to this loop?

**Common mistake:** Assuming this instability only matters for "big" datasets — it is actually WORST on small or imbalanced ones.

**Fix:** Always default to `stratify=y` for classification problems unless you have a specific reason not to.

### Demo B — Comparing two baseline models with cross-validation (4 min)

```python
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_val_score

X = df.drop(columns=["customer_id", "churned"])
y = df["churned"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

for name, clf in [("LogisticRegression", LogisticRegression(max_iter=1000)),
                   ("DecisionTree", DecisionTreeClassifier(random_state=42))]:
    scores = cross_val_score(clf, X_train, y_train, cv=5)
    print(f"{name}: mean={scores.mean():.3f}, std={scores.std():.3f}")
```

**Break it down:**
- Same cross-validation setup, two different candidate models
- This is a very early preview of "model comparison," which becomes the full focus of Session 12
- Mean AND std both matter when comparing — a model with a slightly lower mean but much lower std may be the safer choice

**Ask:** If Model A has mean 0.91/std 0.02 and Model B has mean 0.93/std 0.12, which would you trust more for production, and why?

**Common mistake:** Picking the model with the single highest mean score without checking stability.

**Fix:** Always look at both numbers together before declaring a "winner."

### Demo C — Turning a worksheet answer directly into a code comment (3 min)

```python
# === Problem Framing Worksheet ===
# 1. Decision: which customers receive a retention call this week
# 2. Target variable: churned (0/1)
# 3. Label type: category -> binary classification
# 4. Cost of error: missing a real churner (false negative) is likely
#    costlier than one wasted retention call (false positive)

import pandas as pd
df = pd.read_csv("customers.csv")
X = df.drop(columns=["customer_id", "churned"])
y = df["churned"]
print("Framing documented. Proceeding to split and baseline model.")
```

**Break it down:**
- Writing the worksheet as a code comment keeps the framing decision attached to the code that implements it
- Future collaborators (or future-you, six months later) can see WHY the target was chosen, not just what it is
- This habit costs seconds and prevents entire days of confused re-derivation later

**Ask:** Where else in a real project might this kind of "decision log" comment be useful?

**Common mistake:** Treating problem framing as a one-time whiteboard exercise that never makes it into the codebase.

**Fix:** Copy the worksheet answers into a comment block at the top of the first modeling notebook cell, every single project.

---

## Materials Checklist

- [ ] `customers.csv` open and readable in the working notebook environment
- [ ] Four scenario cards (hospital, retail, spam, segmentation) printed or on a shared slide
- [ ] Whiteboard space reserved for the 4-question worksheet template
- [ ] Timer visible to students for the paired activity
- [ ] Optional: projector demo notebook pre-loaded with the SEGMENT 5-7 code cells

---

## Timing Contingencies

| Situation | Action |
|---|---|
| Running 10 min behind before break | Shorten the second worked example in SEGMENT 3 (pricing scenario) to a verbal walkthrough |
| Running long after break | Trim SEGMENT 6 to the single core `cross_val_score` demo; skip the `cv=3` vs `cv=5` comparison |
| Low energy after lunch/break | Use the rapid-fire Drill 1 classification quiz from the Appendix as an energizer |
| Advanced group finishes lab early | Assign Demo B (comparing two baseline models) as a stretch task |
| No shared screen / projector issue | Read code blocks aloud and have students type along from the printed lecture script |

---

## End-of-Session Quiz (5 Questions)

1. What is the one deciding question that separates supervised from unsupervised learning?
2. A target column stores "low," "medium," "high" risk tiers. Is this regression or classification?
3. Why do we call `cross_val_score` on `X_train, y_train` and never on the full dataset or `X_test`?
4. What does a large standard deviation in `cross_val_score` results tell you, even if the mean looks good?
5. Name the four questions in the problem-framing worksheet, in order.

**Answer key (instructor):**
1. Whether a labelled target/outcome column exists in the historical data.
2. Classification (category, not a number) — even though the categories have an implied order.
3. To avoid leaking test data into model selection; the test set must stay untouched until final evaluation.
4. That performance is unstable across different slices of data — the mean alone may not be trustworthy.
5. (1) What decision will this drive? (2) What is the target variable? (3) Number, category, or no label? (4) What does a wrong prediction cost?

---

## Homework Rubric

| Criterion | Excellent (4) | Good (3) | Needs Work (2) | Incomplete (1) |
|---|---|---|---|---|
| App feature framing worksheet | All 4 questions answered precisely, correct type identified | 3-4 answered, minor gaps | 2 answered, type unclear | 0-1 answered |
| Split/CV re-run comparison | Compares mean AND std with a clear explanation of any change | Compares mean and std, thin explanation | Reports numbers with no comparison | Not attempted |
| cv=3 vs cv=5 reflection | Clear, correct reasoning about fold count and stability | Reasonable but incomplete reasoning | Numbers reported, no reasoning | Not attempted |

**Total:** /12 — Pass threshold: 8/12
