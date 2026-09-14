# Lecture Script: Machine Learning — ML Workflow & Problem Framing
> **Instructor Reference** — Module 2: Classical ML | Academic Session 17 | Duration: 2 Hours | Instructor: Aswath Rao

---

## Session Overview
**Goal:** By the end of this session, students can translate any business question into the correct ML problem type, explain supervised vs. unsupervised learning, use `train_test_split` and `cross_val_score` correctly, and justify a metric choice based on business cost — all before writing any modeling code.

**Student profile at this point:** They are strong with Pandas, EDA, SQL, and spreadsheets (Sessions 9–16) and comfortable framing business questions from data (Session 14). They have **never** built or evaluated a predictive model. Likely wrong assumption: several will think "ML" starts with `.fit()` and skip the framing step entirely. Boredom risk: this session has almost no new syntax, so energy must come from the storytelling and cold-calling, not the code.

**Key outcome:** Students should leave asking themselves, unprompted, "wait — what kind of ML problem is this, and what would it cost us to get it wrong?" before touching any dataset.

> 🎯 **The one sentence this session must land:** *You don't start a machine learning project by picking a model — you start by correctly translating a business question into a problem type, and by deciding in advance how you'll prove your answer is actually trustworthy.*

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| Opening — "The Manager's Question" | 8 min | 8 min |
| Concept Block 1: Problem Framing | 12 min | 20 min |
| Practical Block 1: Classify These Business Questions | 10 min | 30 min |
| Concept Block 2: Supervised vs. Unsupervised | 12 min | 42 min |
| Practical Block 2: Supervised or Unsupervised? Rapid Fire | 8 min | 50 min |
| **BREAK** | 10 min | 60 min |
| Concept Block 3: Train/Test Split | 10 min | 70 min |
| Concept Block 4: Cross-Validation | 10 min | 80 min |
| Practical Block 3: Live Coding Demo (TA Code) | 10 min | 90 min |
| Concept Block 5: Metric Selection as Business Decision | 10 min | 100 min |
| Practical Block 4: Cost of Mistakes Debate | 8 min | 108 min |
| Summary & Bridge | 6 min | 114 min |
| Q&A & Doubt Solving | 6 min | 120 min |

---

## Opening — "The Manager's Question" (8 min)

Walk in and open with this, verbatim-ish:

> "You're on the ops analytics team at Swiggy. Every single month, some delivery partners just... stop taking orders. They leave the platform. Replacing one isn't free — recruiting, onboarding, and a gap in delivery capacity in that neighborhood for weeks. One day your manager walks up to your desk and says: 'Can we figure out who's going to leave — *before* they leave?'"

Pause. Ask the room:

> "Raise your hand if your first instinct is to open a notebook and import `sklearn`."

(Several hands will go up — that's the point.)

> "Here's the uncomfortable truth: if you do that right now, you will almost certainly build the wrong thing. Because that sentence your manager said isn't code yet. It's not even a well-formed question yet. Today, before we touch a single model, we learn how to translate it correctly — and how to prove, honestly, whether our answer is any good."

**Pivot line:** "Everything you've learned for 16 sessions — Pandas, EDA, SQL — was about understanding what already happened. Starting today, we ask the computer to predict what *hasn't* happened yet. That's a fundamentally different kind of thinking, and it starts with framing, not code."

**Context for sessions ahead:** "This exact workflow — frame the problem, split the data, evaluate honestly, choose the right metric — is the skeleton every single session for the next two weeks hangs on. Sessions 20, 22, 25, and 26 will each plug a different model into this same skeleton."

---

## Concept Block 1: Problem Framing (12 min)

> "So — 'can we predict who's going to churn.' Let's actually break that down. Every business question you'll ever be handed maps onto exactly one of three boxes."

Write on the board:

| Business question | ML problem type |
|---|---|
| "Will X churn?" | Classification |
| "How many orders will X place?" | Regression |
| "Are there natural groups in our partners?" | Clustering |

> "Classification: the answer is a category. Regression: the answer is a number. Clustering: there's no known answer at all — we're hunting for structure. Our churn question — will this partner leave, yes or no — that's a category. So this is classification."

### 🔴 The trap / highest-value moment
> "Here's the single highest-value habit I want you to build today: **before you write any code, say out loud which of these three boxes your problem belongs in.** Students who skip this step build regressions when they needed classifiers, or try to force a label onto a problem that has none. Write this rule down: *the box comes before the code, always.*"

---

## Practical Block 1: Classify These Business Questions (10 min)

Put 4 scenarios on screen, have students work in pairs for 3 minutes, then cold-call:

1. "Predict monthly revenue for each Zomato restaurant partner next quarter." → **Regression** (numeric outcome)
2. "Will this HDFC credit card applicant default?" → **Classification** (categorical outcome, historical defaults known)
3. "Group Ola drivers into behavioral segments with no predefined categories." → **Clustering** (no known label)
4. "Predict which delivery zone will see the most order volume during IPL final week." → **Regression** (numeric outcome, though some students may say classification if they misread "which zone" as a category — see below)

**Answer key reasoning to say aloud:** For #4, explicitly address the trap: "which zone" *sounds* categorical, but if we're predicting an actual order-volume number per zone and picking the max, it's really regression underneath. If instead we just wanted to label each zone as "high" or "low" volume, that reframes it as classification. **Say aloud:** "Notice how the same real-world scenario can become two different ML problem types depending on exactly how you phrase the target — that's exactly why this framing step matters so much."

💬 Expect an argument about #4. Welcome it. Say: "You're both right — it depends on how precisely we define the target. That ambiguity is normal in real projects, and resolving it is your job as the analyst, not something the data tells you automatically."

---

## Concept Block 2: Supervised vs. Unsupervised Learning (12 min)

> "Let's go one level deeper. Picture a kirana shop owner with three years of credit-ledger history. She already knows exactly which customers eventually stopped paying on time. That history is a **label** — a known outcome sitting right there in her records. Training a model on labeled history like this is called **supervised learning**."

> "Now imagine she instead wants to group her regular customers into natural 'types' — without deciding in advance what the groups even are. There's no known correct answer in her ledger for that. That's **unsupervised learning**."

Write the two-line definitions on the board:
- **Supervised:** learning from historical data where the outcome is already known
- **Unsupervised:** finding structure with no known outcome to check against

> "Quick gut check — our Swiggy churn problem: do we have a label? Yes — we know, historically, which partners actually left. So it's supervised. Combined with what we said earlier, churn prediction is specifically **supervised classification**."

### 🔴 The trap / highest-value moment
> "Students often assume 'grouping' automatically means clustering. It doesn't. Grouping customers into *known* categories — like 'will renew' vs. 'won't renew,' based on actual past renewal records — is still supervised, because the label already exists. Clustering is only for when no such label exists at all. Write this down: *if a known outcome exists in your historical data, it's supervised — no matter how 'grouped' the output feels.*"

---

## Practical Block 2: Supervised or Unsupervised? Rapid Fire (8 min)

Go around the room fast, one scenario per student, answer must come in under 5 seconds:

- Predicting HDFC loan default → **Supervised** (past defaults are known)
- Grouping Zomato restaurants by cuisine + review patterns, no predefined categories → **Unsupervised**
- Forecasting next month's Ola ride demand → **Supervised** (past demand numbers are the label)
- Flagging unusual transactions with no prior fraud labels → **Unsupervised**
- Predicting exam scores from study hours → **Supervised**
- Segmenting website visitors into behavior clusters with no predefined groups → **Unsupervised**

💬 Expect pushback on the "unusual transactions" one — some students will argue fraud detection is always supervised because "fraud" feels like an obvious label. Say: "It's supervised *if* you already have confirmed fraud cases labeled in your history. The moment you have zero confirmed labels and are just hunting for outliers, it becomes unsupervised. The technique depends entirely on what data you actually have — not on the topic."

---

## BREAK (10 min)

---

## Concept Block 3: Train/Test Split (10 min)

> "Here's a trap that catches almost every beginner. Imagine a student who memorizes the *exact* answer key from last year's exam instead of understanding the subject. Give them that same exam again — perfect score. Give them a new exam on the same topics — they struggle. Memorization looks exactly like learning, until the questions change."

> "A model evaluated only on the data it trained on has the exact same problem. It can memorize quirks specific to that data rather than learning something that generalizes to new partners it's never seen."

Write the fix on the board:

```python
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
```

> "`test_size=0.2` locks away 20% of our data purely for honest evaluation — the model never sees it during training. `random_state=42` just makes the split reproducible, so rerunning the code gives the same split every time."

### 🔴 The trap / highest-value moment
> "There is no single correct split ratio — 80/20 is common, but it's a trade-off, not a law. More training data usually means a better-learned model; more test data means a more trustworthy evaluation. You cannot maximize both at once. Write this down: *the split ratio is a judgment call, not a formula.*"

---

## Concept Block 4: Cross-Validation (10 min)

> "One more problem with a single split: what if, by pure chance, your 20% test set happened to be unusually easy, or unusually hard? Your performance number could be lying to you just from bad luck in the split."

> "Think about how a cricket selector judges a batter's true form. Nobody judges form off a single innings — a great or terrible score that day could just be the pitch, or the bowling attack, or luck. Judging across five different innings in different conditions gives a far more trustworthy read."

Write:

```python
from sklearn.model_selection import cross_val_score

scores = cross_val_score(model, X, y, cv=5)
```

> "With `cv=5`, the data is split into 5 chunks. The model trains on 4 and tests on the 1 held-out chunk — five times, rotating which chunk is held out — and we average the five scores into one far more reliable number."

**Say explicitly:** "We are not going deep into stratified folds, leakage-safe CV, or nested CV today — that's Session 27's job. Today, just internalize: repeating the experiment gives you a number you can actually trust."

---

## Practical Block 3: Live Coding Demo (TA Code) (10 min)

**Handoff line (must match TA code file's opening comment):** "Let's actually see this in code — same Swiggy churn scenario, same numbers we've been talking about all session."

Hand off to the accompanying `ta-code - Session 17 - ML Workflow & Problem Framing.py` file. Walk through, narrating each `# --- EXPLAIN ---` comment aloud as written in the code file:

1. Build the small synthetic 200-partner dataset (reusing Pandas from Module 1)
2. Confirm this is supervised classification (label = `churned`)
3. Run `train_test_split` — point out the resulting 160/40 split on screen
4. Run `cross_val_score` with `cv=5` — point out the five scores and their average on screen
5. Land the punchline together with the class: the baseline "model" (`DummyClassifier`) gets ~91% accuracy just by always guessing "no churn" — because almost nobody in the sample churns. **Do not resolve this yet** — just let it sit as an unsettling number.

💬 Expect a question here: "wait, 91% sounds great — why are we unhappy?" Welcome it. Say: "Hold that feeling. That exact discomfort is the seed of Session 23. For today, just notice: a number can look great and still be almost useless."

---

## Concept Block 5: Metric Selection as Business Decision (10 min)

> "Back to the churn problem. If we wrongly say a partner *won't* churn but they do — a **false negative** — we lose them with zero chance to intervene. If we wrongly say a partner *will* churn but they stay — a **false positive** — we waste a retention incentive on someone who was never leaving."

Ask the room directly:

> "Which mistake costs Swiggy more — missing a real churner, or wasting an incentive on someone who'd have stayed anyway?"

Let them debate — there is genuinely no single correct answer here.

### 🔴 The trap / highest-value moment
> "The trap is defaulting to 'accuracy' for every problem because it's the most familiar word. You just watched a baseline hit 91% accuracy by doing nothing intelligent at all. Write this down: *metric choice follows business cost, not habit — and we prove exactly why accuracy fails in Session 23.*"

---

## Practical Block 4: Cost of Mistakes Debate (8 min)

Split the room into two sides: "false negatives are worse" vs. "false positives are worse," for the Swiggy churn scenario specifically. Give 3 minutes to prepare an argument, then 30 seconds each side.

**Model reasoning to surface regardless of which side wins:** Losing an experienced delivery partner (false negative) usually costs more than one wasted retention incentive (false positive), because replacement costs (recruiting, onboarding, lost capacity) tend to be larger than one incentive payout — but this is a business assumption that should be validated with real numbers, not assumed.

💬 Expect someone to ask "so what's the actual right answer?" Welcome it. Say: "There isn't one without real cost numbers from the business. That's exactly the point — you now know the *right question to ask* before touching a metric, even if you don't yet have the number."

---

## Summary & Bridge (6 min)

| Concept | The one thing to remember |
|---|---|
| Problem framing | Every business question maps to classification, regression, or clustering — decide the box before writing code |
| Supervised vs. unsupervised | Supervised means a known label exists in history; unsupervised means it doesn't |
| Train/test split | Never evaluate a model on the data it trained on |
| Cross-validation | One split can be lucky or unlucky; averaging several is more trustworthy |
| Metric selection | The "right" metric depends on which mistake costs the business more |

Close on the thesis line: "You don't start a machine learning project by picking a model — you start by correctly translating a business question into a problem type, and by deciding in advance how you'll prove your answer is trustworthy."

**Bridge to next session:** "Today we decided *what kind* of problem we're solving and *how* we'll prove our answer is honest. Session 18 — Data Preparation for ML — is about getting the data itself into a shape a model can actually consume: encoding categories, scaling numbers, and avoiding a sneaky trap called data leakage that can quietly ruin an otherwise good model."

---

## Q&A & Doubt Solving (6 min)

**Q: Why did we use `DummyClassifier` instead of a real model today?**
→ We haven't learned any real models yet — that starts with Linear Regression in Session 20. `DummyClassifier` lets us practice the *workflow* (splitting, cross-validating) without pretending we've already taught modeling.

**Q: Is `test_size=0.2` always correct?**
→ No — it's a common default, but the right ratio depends on how much data you have and how much you value training size versus evaluation reliability. There's no universal rule.

**Q: What's the difference between `train_test_split` and `cross_val_score` — don't they do the same thing?**
→ `train_test_split` gives you one split, evaluated once. `cross_val_score` repeats that process across multiple rotating splits and averages the result, which is more reliable but takes more computation.

**Q: If accuracy can be misleading, why did we even compute it today?**
→ To make you feel the problem firsthand before we hand you the fix. Session 23 gives you the actual tools (precision, recall, confusion matrices) to diagnose exactly what a misleading accuracy number is hiding.

**Q: Can a problem be both classification and clustering?**
→ Not at the same time for the same target — but a project can use both: clustering to explore unlabeled structure first, then classification once you've defined labels from what you found. That's an advanced pattern, not required today.

**Q: How do we know if our historical churn labels are even trustworthy?**
→ Great instinct — that's exactly the kind of data-quality question EDA (Session 14) trained you to ask, and it's just as relevant here. We'll formalize this concern further when we cover data leakage in Session 27.

---

## Instructor Notes
- **Words not yet earned:** precision, recall, F1, confusion matrix, ROC-AUC, stratified k-fold, hyperparameter, regularization, gradient descent — all explicitly future sessions. If a student uses one of these terms from prior exposure, acknowledge it but redirect: "hold that thought for Session 23/27."
- **Biggest risk in this session:** boredom, since there's almost no new syntax. Counter this by keeping the Swiggy story alive constantly and by using cold-calls and rapid-fire drills rather than long stretches of lecture.
- **Board management:** keep the three-box table (Classification/Regression/Clustering) and the supervised/unsupervised two-liner visible on the board for the entire session — students will refer back to both repeatedly.
- **Common confusions, numbered:**
  1. Confusing "grouping" with clustering even when a known label exists (it's still supervised)
  2. Assuming higher accuracy always means a better model
  3. Treating the train/test split ratio as a fixed rule rather than a trade-off
  4. Expecting a single "correct" metric to exist independent of business context
- **Cross-references:** Session 23 (Classification Metrics) resolves today's accuracy discomfort; Session 27 (Model Validation & Leakage) formalizes cross-validation rigor and data trustworthiness questions raised today; Session 20 (Linear Regression) is where a real model finally replaces today's `DummyClassifier` placeholder.
- **Local/cultural context notes:** Swiggy churn lands consistently well with this cohort as the central scenario — keep reusing it verbatim through Sessions 18 and 20 rather than switching examples, since the mental map's "shift" framing depends on this continuity.
