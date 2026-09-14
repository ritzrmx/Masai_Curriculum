# Lecture Script: Mathematics of Machine Learning — Probability & Counting
> **Instructor Reference** — Module 2: Classical ML | Academic Session 24 (Master Class) | Duration: 1.5 Hours | Instructor: Abhinandhan

---

## Session Overview
**Goal:** By the end of this session, students can define a sample space and event, compute probabilities as ratios, calculate P(A∪B) and P(A|B), derive Bayes' Theorem from conditional probability, and explain numerically why rare events make accurate-sounding tests deceptive.

**Student profile at this point:** Just finished Session 23, which left them with unresolved discomfort about how a "90%+ accurate" DummyClassifier could still be useless. They have strong practical intuition about precision/recall but no formal probability foundation underneath it yet. Likely wrong assumption: most will guess that a "90% accurate" disease test means "90% chance you have it if you test positive" — this session exists specifically to dismantle that assumption with real numbers. Boredom/anxiety risk: math anxiety is a real concern here; counter with analogy-first delivery, and by explicitly linking every formula back to Session 23's already-familiar precision/recall discomfort.

**Key outcome:** Students should leave able to work through a full Bayes' Theorem calculation by hand and correctly explain, in plain language, why the answer is so much lower than gut instinct suggests.

> 🎯 **The one sentence this session must land:** *When the thing you're testing for is rare, even a highly accurate test produces mostly false alarms — and Bayes' Theorem is the precise tool that proves exactly how much.*

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| Opening — "The Surprising Test Result" | 6 min | 6 min |
| Concept Block 1: Sample Space and Events | 10 min | 16 min |
| Practical Block 1: List the Sample Space | 6 min | 22 min |
| Concept Block 2: Probability as a Ratio | 8 min | 30 min |
| Concept Block 3: P(A∪B) — Union | 10 min | 40 min |
| Practical Block 2: Union Venn Diagram Exercise | 6 min | 46 min |
| **BREAK** | 8 min | 54 min |
| Concept Block 4: P(A\|B) — Conditional Probability | 10 min | 64 min |
| Concept Block 5: Deriving Bayes' Theorem | 10 min | 74 min |
| Practical Block 3: Live Coding Demo (TA Code) | 8 min | 82 min |
| Concept Block 6: Conditional ≠ Joint — Closing the Loop to Session 23 | 4 min | 86 min |
| Summary & Bridge | 3 min | 89 min |
| Q&A & Doubt Solving | 1 min | 90 min |

---

## Opening — "The Surprising Test Result" (6 min)

Open with this, verbatim-ish:

> "Suppose 1% of a population has a certain disease, and a test is 90% accurate — it correctly catches 90% of people who truly have the disease, and correctly clears 90% of people who don't. You test positive. What's the chance you actually have the disease?"

Pause. Ask for a quick show of hands: "who thinks the answer is close to 90%?" (Most will raise their hands.)

> "The real answer is about 8%. Not a typo — eight percent. By the end of this session, you'll be able to derive that number yourselves, from scratch, and explain exactly why gut instinct gets it so wrong."

**Pivot line:** "This is the exact mathematical machinery underneath Session 23's discomfort with the DummyClassifier's accuracy. Today we go one level deeper than precision and recall — into the probability theory that explains *why* those metrics behave the way they do."

**Context for sessions ahead:** "Everything from here forward — decision trees, random forests, even how you'd judge a GenAI system's confidence later in this course — rests on this same rare-event intuition."

---

## Concept Block 1: Sample Space and Events (10 min)

> "Think of every possible result of a T20 match: Team A wins, Team B wins, tied or abandoned. That full list is the **sample space**. 'Team A wins' is one specific **event** — a subset of that space we care about."

Write on the board:

> Sample space = every possible outcome
> Event = any subset of outcomes we're interested in

> "Rolling a standard die: sample space is {1,2,3,4,5,6}. The event 'even number' is {2,4,6} — a subset."

### 🔴 The trap / highest-value moment
> "An event doesn't have to be a single outcome — it can be any collection, including the whole space or none of it. Write this down: *an event is a subset, not necessarily a single result.*"

---

## Practical Block 1: List the Sample Space (6 min)

Ask students, individually, to write the sample space for "the number of heads in two coin flips" and identify the event "at least one head." 2 minutes, then cold-call.

**Answer key reasoning to say aloud:** Sample space (treating each flip as distinguishable) is {HH, HT, TH, TT}. "At least one head" is {HH, HT, TH} — 3 out of 4 outcomes.

---

## Concept Block 2: Probability as a Ratio (8 min)

> "A kirana shop owner notices sales exceeded ₹10,000 on 12 of the last 30 days. The simplest estimate of 'probability of a big sales day' is exactly that ratio: 12 out of 30."

Write the formula:

$$P(\text{event}) = \frac{\text{outcomes in the event}}{\text{outcomes in the sample space}}$$

> "For our die, P(even) = 3/6 = 0.5."

💬 Expect a question: "does this only work when outcomes are equally likely?" Welcome it. Say: "Exactly right — this clean ratio assumes equally likely outcomes. Real-world probabilities like churn rate are usually estimated from historical data instead, but the same ratio intuition still applies underneath."

---

## Concept Block 3: P(A∪B) — Union (10 min)

> "Picture Swiggy Instamart customers: some bought snacks, some bought a cold drink, some bought both. If you want 'snacks OR cold drink,' you can't just add the two probabilities separately — anyone who bought both gets counted twice."

Write and derive live:

$$P(A \cup B) = P(A) + P(B) - P(A \cap B)$$

$$P(\text{snacks or drink}) = 0.4 + 0.3 - 0.1 = 0.6$$

Draw the Venn diagram on the board with the overlap region explicitly labeled 0.1.

### 🔴 The trap / highest-value moment
> "Forgetting to subtract the overlap is the single most common union mistake — it silently double-counts anyone in both groups. Write this down: *union means subtract the overlap once, always.*"

---

## Practical Block 2: Union Venn Diagram Exercise (6 min)

Give a new pair of overlapping probabilities (e.g., P(cricket fan)=0.5, P(football fan)=0.35, P(both)=0.15). Have students compute P(cricket OR football) individually, 2 minutes, then cold-call to confirm on the board.

---

## BREAK (8 min)

---

## Concept Block 4: P(A|B) — Conditional Probability (10 min)

> "'What fraction of cold-drink buyers also bought snacks?' is a completely different question from 'what fraction of all customers bought both?' The first question shrinks the entire sample space down to just cold-drink buyers first, then asks about snacks only within that smaller group."

Write and compute live:

$$P(A|B) = \frac{P(A \cap B)}{P(B)}$$

$$P(\text{snacks}|\text{cold drink}) = \frac{0.1}{0.3} \approx 0.33$$

> "Even though only 10% of *all* customers bought both, a full 33% of cold-drink buyers also bought snacks — because we narrowed our lens to just that group."

### 🔴 The trap / highest-value moment
> "P(A|B) and P(A∩B) are not the same number, and confusing them is one of the most common reasoning errors in all of statistics. Write this down: *P(A∩B) is a slice of everything; P(A|B) is a slice of just B's portion.* This distinction is the entire key to today's disease example."

---

## Concept Block 5: Deriving Bayes' Theorem (10 min)

> "Let's derive the tool that answers our opening question, using only what we just defined — no shortcuts."

Write the derivation live, step by step:

$$P(A|B) = \frac{P(A \cap B)}{P(B)} \quad \text{and} \quad P(B|A) = \frac{P(A \cap B)}{P(A)}$$

> "From the second equation: $P(A \cap B) = P(B|A) \times P(A)$. Substitute that into the first equation..."

$$P(A|B) = \frac{P(B|A) \times P(A)}{P(B)}$$

> "That's Bayes' Theorem. Now let's plug in the disease numbers from the opening."

Work through live on the board:

- P(Disease) = 0.01, P(Positive|Disease) = 0.90, P(Positive|No Disease) = 0.10

$$P(\text{Positive}) = (0.90)(0.01) + (0.10)(0.99) = 0.009 + 0.099 = 0.108$$

$$P(\text{Disease}|\text{Positive}) = \frac{0.90 \times 0.01}{0.108} = \frac{0.009}{0.108} \approx 0.083$$

> "8.3%. Because the disease is so rare, the enormous healthy population — even with just a 10% false-positive rate — generates more false positives in raw numbers than the small sick population generates true positives."

### 🔴 The trap / highest-value moment
> "This is precisely Session 23's DummyClassifier discomfort, from the opposite direction. When the positive class is rare, even a fairly accurate test produces a flood of false positives relative to true positives. Write this down: *rare positive class + imperfect test = mostly false alarms among the positives, no matter how 'accurate' the test sounds.*"

---

## Practical Block 3: Live Coding Demo (TA Code) (8 min)

**Handoff line (must match TA code file's opening comment):** "Let's actually compute this Bayes' Theorem calculation in code, step by step, and then see the same effect show up in a churn-flagging scenario."

Hand off to `ta-code - Session 24 - Master Class - Probability & Counting.py`, narrating each `# --- EXPLAIN ---` block aloud:

1. Define the disease example's known probabilities as plain variables
2. Compute P(Positive) by combining both groups
3. Apply Bayes' Theorem and print the final ~8.3% result, matching the board derivation exactly
4. A short closing illustration applying the same reasoning to a hypothetical rare-event churn-flagging scenario, connecting directly back to Session 23's precision discussion

---

## Concept Block 6: Conditional ≠ Joint — Closing the Loop to Session 23 (4 min)

> "Quick close: precision, from Session 23, was TP / (TP + FP) — which is really just P(actually churned | flagged as churn), a conditional probability. Recall was TP / (TP + FN) — P(flagged | actually churned), the conditional probability in the *other* direction. These are different numbers for exactly the reason we spent all session on: conditioning on different things gives genuinely different answers."

Ask quickly: "so which of precision and recall corresponds to which side of Bayes' Theorem — the P(B|A) or the P(A|B)?" Let one or two students attempt an answer; the exact mapping isn't critical, the goal is just making the connection explicit before moving on.

---

## Summary & Bridge (3 min)

| Concept | The one thing to remember |
|---|---|
| Sample space & event | Every possible outcome, and any subset of interest |
| Probability as a ratio | Favorable outcomes over total outcomes |
| P(A∪B) | Add both, subtract the overlap once |
| P(A\|B) | Restricts the sample space to B first — not the same as P(A∩B) |
| Bayes' Theorem | Rare events + imperfect tests = mostly false alarms among the positives |

Close on the thesis line: "When the thing you're testing for is rare, even a highly accurate test produces mostly false alarms — and Bayes' Theorem is the precise tool that proves exactly how much."

**Bridge to next session:** "We've now fully explained the probability theory behind everything since Session 17's DummyClassifier. Session 25 shifts back to a hands-on classifier — Decision Trees — where we'll train a model and literally visualize its decision-making process with `plot_tree`, no probability formulas required."

---

## Q&A & Doubt Solving (1 min)

Given the tight 90-minute window, take one live question if time allows; otherwise direct remaining questions to the tutorial session.

**Q: Does Bayes' Theorem only apply to disease testing?**
→ Not at all — it applies anywhere you're updating a belief based on new evidence, including fraud detection, spam filtering, and churn flagging, as today's closing demo showed.

---

## Instructor Notes
- **Words not yet earned:** DecisionTreeClassifier, plot_tree, entropy/Gini impurity — all Session 25 onward. Keep today's language in pure probability terms.
- **Biggest risk in this session:** math anxiety compounded by the tight 90-minute window and genuinely counter-intuitive result. Counter by repeating the plain-language explanation of the 8.3% result at least twice, in different words each time.
- **Pacing note:** this is a 90-minute session — do not let the Bayes' derivation run long; the numerical plug-in matters more than dwelling on the algebra.
- **Board management:** keep the Bayes' Theorem formula and the final disease-example numbers visible from Concept Block 5 through the end of the session — Concept Block 6's closing connection depends on students seeing these numbers again.
- **Common confusions, numbered:**
  1. Assuming a "90% accurate" test means "90% chance of having the condition if positive"
  2. Confusing P(A|B) with P(A∩B)
  3. Forgetting to subtract the overlap when computing P(A∪B)
  4. Not immediately seeing the connection between today's math and Session 23's precision/recall
- **Cross-references:** Session 23 (Classification Metrics) is the practical precursor this session formalizes; Session 32 (Master Class: Vectors & Linear Algebra) continues the "pure math, hand-derived" master class format later in the course.
- **Local/cultural context notes:** the CSV-specified disease-testing example is kept verbatim since it's a widely recognized teaching example, with the Swiggy Instamart and churn-flagging examples layered around it for cohort consistency.
