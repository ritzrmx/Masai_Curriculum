# Lecture Script: Machine Learning — Classification Metrics
> **Instructor Reference** — Module 2: Classical ML | Academic Session 23 | Duration: 2 Hours | Instructor: Aswath Rao

---

## Session Overview
**Goal:** By the end of this session, students can build and interpret a confusion matrix, explain precisely why accuracy misleads on imbalanced data, compute precision and recall, combine them into F1, and select the right metric for a specific business scenario.

**Student profile at this point:** Just learned to adjust classification thresholds qualitatively in Session 22, and has been carrying an unresolved "accuracy can be misleading" discomfort since Session 17's `DummyClassifier` demo. Likely wrong assumption: several will still instinctively reach for accuracy as the default "how good is my model" number. Boredom risk: very low — this session pays off two lingering open threads from earlier sessions, which creates strong narrative momentum.

**Key outcome:** Students should leave able to look at any classification report and immediately identify which metric matters most for the business scenario described, without defaulting to accuracy out of habit.

> 🎯 **The one sentence this session must land:** *Accuracy answers "how often is the model right overall," but precision and recall answer the two questions that actually matter in an imbalanced, high-stakes decision: can I trust my flags, and am I missing real cases?*

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| Opening — "The Accuracy Con" | 8 min | 8 min |
| Concept Block 1: The Confusion Matrix | 12 min | 20 min |
| Practical Block 1: Fill In the Confusion Matrix | 8 min | 28 min |
| Concept Block 2: Accuracy's Blind Spot, Finally Proven | 10 min | 38 min |
| Practical Block 2: The Dummy Baseline Reveal | 8 min | 46 min |
| **BREAK** | 10 min | 56 min |
| Concept Block 3: Precision | 10 min | 66 min |
| Concept Block 4: Recall | 10 min | 76 min |
| Practical Block 3: Compute Precision and Recall By Hand | 8 min | 84 min |
| Concept Block 5: F1 and the Precision-Recall Tradeoff | 12 min | 96 min |
| Practical Block 4: Live Coding Demo (TA Code) | 14 min | 110 min |
| Summary & Bridge | 5 min | 115 min |
| Q&A & Doubt Solving | 5 min | 120 min |

---

## Opening — "The Accuracy Con" (8 min)

Open with this, verbatim-ish:

> "Way back in Session 17, our very first baseline model — one that did nothing intelligent at all, just always guessed 'no churn' — scored around 91% accuracy. It felt like a great number. I told you to hold that discomfort. Today, we finally resolve it, with real math."

Pause. Ask the room:

> "If a model that does literally nothing intelligent can still score 91% accuracy, what does that tell you about accuracy as a metric, at least for this kind of problem?"

(Let a few answers land — someone will likely say "it's not a good metric here.")

> "Exactly. Today you get the precise vocabulary — and the proof — for why, and what to use instead."

**Pivot line:** "Session 22 taught you that moving the classification threshold trades one kind of mistake against another. Today we finally get the numbers to measure that trade properly, instead of just reasoning about it qualitatively."

**Context for sessions ahead:** "Every classifier for the rest of this course — trees, forests, and beyond — gets judged using exactly today's vocabulary, not accuracy alone."

---

## Concept Block 1: The Confusion Matrix (12 min)

> "Recall Session 22's airport security analogy. Every bag falls into exactly one of four outcomes: a real threat correctly caught, an innocent bag wrongly flagged, a real threat missed, or an innocent bag correctly cleared. A confusion matrix is this exact four-way breakdown, applied to any classifier."

Draw the 2x2 table on the board:

| | Predicted: No Churn | Predicted: Churn |
|---|---|---|
| **Actual: No Churn** | True Negative (TN) | False Positive (FP) |
| **Actual: Churn** | False Negative (FN) | True Positive (TP) |

> "Every single prediction lands in exactly one of these four boxes. No exceptions, no ambiguity."

### 🔴 The trap / highest-value moment
> "Which class counts as 'positive' is a choice, not a fact of nature. Here, churn is positive because it's the outcome we care about detecting. Write this down: *always confirm which class is 'positive' before reading any confusion matrix* — flipping this assumption flips the entire interpretation."

---

## Practical Block 1: Fill In the Confusion Matrix (8 min)

Give students a list of 10 actual/predicted label pairs. Have them individually tally TP, TN, FP, FN counts, 4 minutes, then cold-call to build the matrix together on the board.

---

## Concept Block 2: Accuracy's Blind Spot, Finally Proven (10 min)

> "Let's bring back Session 17's `DummyClassifier`. On a test set where about 20% of partners actually churn, a model that always predicts 'no churn' scores roughly 80% accuracy — while catching exactly zero real churners."

Draw this confusion matrix explicitly on the board:

| | Predicted: No Churn | Predicted: Churn |
|---|---|---|
| **Actual: No Churn** | 48 (TN) | 0 (FP) |
| **Actual: Churn** | 12 (FN) | 0 (TP) |

> "Zero True Positives. Every single actual churner became a False Negative. And yet accuracy — (TN+TP)/total — still comes out to 80%, because non-churners dominate the dataset."

### 🔴 The trap / highest-value moment
> "A high accuracy number, alone, tells you almost nothing about whether a model is useful when outcomes are imbalanced. Write this down: *always check the confusion matrix before trusting an accuracy figure, especially for rare-event problems.*"

---

## Practical Block 2: The Dummy Baseline Reveal (8 min)

Show the actual Session 17 `DummyClassifier` numbers side by side with a real trained model's confusion matrix (both on today's dataset). Ask the room: "which model would you actually want in production, and does accuracy alone tell you that?" Let this land as a genuine "aha" moment — most students will immediately see the real model's non-zero True Positives as the deciding factor, not the accuracy numbers.

💬 Expect someone to ask "so is accuracy ever useful?" Welcome it. Say: "Yes — when classes are roughly balanced and mistakes cost about the same in both directions. It's not a bad metric everywhere, just a dangerous default here."

---

## BREAK (10 min)

---

## Concept Block 3: Precision (10 min)

> "Imagine a security team that flags 20 bags as suspicious in a day, but only 5 actually contain anything concerning. That's a lot of wasted investigation time on false alarms. Precision measures exactly this: of everything flagged as positive, what fraction was actually correct?"

Write the formula and compute live:

$$\text{Precision} = \frac{TP}{TP + FP}$$

> "Our churn model at threshold 0.5 flags 15 partners. 12 actually churn, 3 don't. Precision = 12 / (12+3) = 0.80 — 80% of our flags were genuinely at risk."

### 🔴 The trap / highest-value moment
> "High precision doesn't guarantee you're catching most real cases. A model that only flags the single most obvious churner and is right could have 100% precision while missing almost everyone else. Write this down: *precision says nothing about what you missed — that's recall's job.*"

---

## Concept Block 4: Recall (10 min)

> "Back to airport security — if 10 real threats passed through screening, and flags caught only 6, recall measures that: of everything that should have been flagged, how much actually was?"

$$\text{Recall} = \frac{TP}{TP + FN}$$

> "In our test set, 12 partners actually churned, and our model caught all 12 — 0 False Negatives. Recall = 12/(12+0) = 1.00. We caught every real churner in this particular test set."

### 🔴 The trap / highest-value moment
> "High recall doesn't guarantee your flags are trustworthy. A model that flags *everyone* as 'will churn' gets perfect recall automatically — it never misses a real case — but its precision would likely be terrible. Write this down: *precision and recall each tell only half the story; you need both.*"

---

## Practical Block 3: Compute Precision and Recall By Hand (8 min)

Using Practical Block 1's hand-built confusion matrix, have students compute precision and recall themselves, 4 minutes, then cold-call to confirm and discuss which number is more "worrying" for that specific matrix.

---

## Concept Block 5: F1 and the Precision-Recall Tradeoff (12 min)

> "Imagine grading a student who scored perfectly on one exam but skipped every other one entirely. A simple average might look fine, hiding how lopsided their real performance was. F1 score combines precision and recall in a way that specifically punishes this imbalance."

$$F1 = 2 \times \frac{\text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}}$$

> "With precision=0.80 and recall=1.00, F1 comes out around 0.89 — a strong, balanced score. Drop recall to 0.10 while keeping precision at 0.80, and F1 collapses, correctly reflecting that catching only 10% of real churners is a serious problem."

Now revisit Session 22's threshold sweep explicitly, with real precision/recall numbers on the board:

| Threshold | Precision | Recall |
|---|---|---|
| 0.3 | 0.75 | 1.00 |
| 0.5 | 0.80 | 1.00 |
| 0.7 | 1.00 | 0.83 |

> "Notice: pushing the threshold up to 0.7 buys perfect precision but costs recall — some real churners now slip through. This is the exact tradeoff Session 22 discussed qualitatively, now sitting in front of you as real numbers."

### 🔴 The trap / highest-value moment
> "There is no universally 'best' metric. The right one depends entirely on the business scenario's cost structure — exactly what Sessions 17 and 22 both argued without the numbers to prove it. Write this down: *choose the metric based on the cost of being wrong, then optimize for that metric specifically.*"

---

## Practical Block 4: Live Coding Demo (TA Code) (14 min)

**Handoff line (must match TA code file's opening comment):** "Let's actually compute all of this in code — same Swiggy churn pipeline from Session 22, and finally, the DummyClassifier reveal from Session 17."

Hand off to `ta-code - Session 23 - Classification Metrics.py`, narrating each `# --- EXPLAIN ---` block aloud:

1. Rebuild the Session 22 pipeline (preprocessing + LogisticRegression) and fit it
2. Print the confusion matrix, precision, recall, F1, and accuracy at the default threshold — point out these match the board numbers from Concept Blocks 3-5
3. Rebuild Session 17's `DummyClassifier` baseline on this same test set, and print its confusion matrix and metrics side by side — the big reveal: high accuracy, precision and recall both at zero
4. Loop through the same three thresholds (0.3, 0.5, 0.7) and print precision/recall for each, confirming the tradeoff table from Concept Block 5 with live numbers

💬 Expect genuine reaction here — this is designed to land as a payoff moment. Let it breathe for a few seconds before moving to summary.

---

## Summary & Bridge (5 min)

| Concept | The one thing to remember |
|---|---|
| Confusion matrix | Every prediction falls into exactly one of TP, TN, FP, FN |
| Accuracy | Can look great while a model does nothing useful, especially with imbalanced data |
| Precision | Of what was flagged, how much was right |
| Recall | Of what should've been flagged, how much was caught |
| F1 / tradeoff | No metric is universally best — choose based on which mistake costs more |

Close on the thesis line: "Accuracy answers 'how often is the model right overall,' but precision and recall answer the two questions that actually matter in an imbalanced, high-stakes decision: can I trust my flags, and am I missing real cases?"

**Bridge to next session:** "Today's metrics all rest on probability reasoning — what does a '73% chance of churn' really mean, mathematically? Session 24's Master Class derives Bayes' Theorem from first principles, which is exactly the tool used to reason correctly about rare events like churn, fraud, and disease."

---

## Q&A & Doubt Solving (5 min)

**Q: Is there a single metric that's always the safest default?**
→ Not universally, but F1 is a reasonable default when you don't yet know the business cost structure, since it penalizes ignoring either precision or recall entirely.

**Q: Can precision and recall both be low at the same time?**
→ Yes — that indicates a genuinely weak model, not just a threshold tuning issue. If both are low even after trying several thresholds, the model itself likely needs improvement.

**Q: What's a "good" F1 score?**
→ It depends entirely on the problem and dataset — there's no universal cutoff. Compare against a sensible baseline (like the `DummyClassifier`) rather than an arbitrary number.

**Q: Does sklearn compute all of this in one function?**
→ Yes — `classification_report` from `sklearn.metrics` prints precision, recall, F1, and support for each class in one call, which we'll use more going forward.

**Q: How does this change for multiclass problems from Session 22?**
→ Precision and recall get computed per class, then usually averaged (macro or weighted average) — the core ideas are identical, just applied class by class.

---

## Instructor Notes
- **Words not yet earned:** ROC-AUC, GridSearchCV, k-fold, stratified sampling as a formal technique — Session 27 and beyond.
- **Biggest risk in this session:** none really — this is a high-payoff session. The only risk is rushing the Practical Block 2 "reveal" moment; let it land before moving on.
- **Board management:** keep the confusion matrix template and the precision/recall formulas visible for the entire session — nearly every block refers back to them.
- **Common confusions, numbered:**
  1. Forgetting which class is "positive" before interpreting a confusion matrix
  2. Treating high precision as proof of high recall, or vice versa
  3. Assuming F1 is always the right choice regardless of business context
  4. Continuing to default to accuracy out of habit even after today's session
- **Cross-references:** Session 24 (Master Class: Probability & Counting) formalizes the probability reasoning underneath today's metrics; Session 27 (Model Validation & Leakage) will pair these metrics with `GridSearchCV` for systematic model comparison.
- **Local/cultural context notes:** the direct callback to Session 17's `DummyClassifier` is the emotional core of this session — don't skip re-showing those original numbers, since the payoff depends on students recognizing them.
