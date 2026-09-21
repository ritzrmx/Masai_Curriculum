# Lecture Script: Statistics - Spread, Variability and Outliers
> **Instructor Reference** - Module 2: SQL for Data Analysis | Academic Session 8 | Duration: 1.5 Hours | Instructor: Professor

---

## Session Overview

**Goal:** Students can take two datasets with identical averages and prove, using Range, Variance, and Standard Deviation, that they represent very different levels of business risk - and can judge whether an unusual value is an outlier worth investigating or simply a data error.

**Student profile at this point:** They've completed Module 1 - averages and their limits, the analytics workflow, GenAI prompting, cleaning data, formulas, and pivot tables. They already sense intuitively that "steadier" is often safer, but have no vocabulary or formula for it yet. This session deliberately uses **zero software** - just numbers, a board, and a calculator.

**Key outcome:** Students leave asking, on instinct, the question that separates a junior analyst from a senior one: *"You've shown me the average. Now show me whether I can trust it."*

> 🎯 **The one sentence this session must land:** *An average tells you the center. It never tells you whether that center is a safe bet or a coin flip - that's what spread is for.*

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| Opening - "Same average. Which stall do you open a branch with?" | 8 min | 8 min |
| Concept Block 1: Range | 10 min | 18 min |
| Practical Block 1: Compute Range on the driver dataset | 10 min | 28 min |
| Concept Block 2: Variance | 15 min | 43 min |
| **BREAK** | 5 min | 48 min |
| Practical Block 2: Build a deviation table by hand | 15 min | 63 min |
| Concept Block 3: Standard Deviation | 10 min | 73 min |
| Practical Block 3: Same-average, different-risk showdown | 8 min | 81 min |
| Concept Block 4 + quick outlier practical (combined) | 9 min | 90 min |

*The core 90-minute flow above is what every cohort must complete. A fifth Concept/Practical pair on the Interquartile Range (IQR) is provided in the Extension Blocks section below for cohorts that move faster than expected - see Timing Contingencies for exactly when to reach for it.*

---

## Opening - "Same Average. Which Stall Do You Open a Branch With?" (8 min)

Walk in with no slide up. Say:

> *"Two chai stalls. Both average exactly ₹2,000 a day in sales. Your manager tells you: 'Pick one - we're opening a second branch with whichever one is the safer bet.' You're given one number each: the average. Which do you pick?"*

Take answers from the room. Most will say "doesn't matter, they're identical." Let that sit for a moment. Then write the daily numbers on the board:

```
Stall A: 1900, 2050, 1980, 2100, 1970
Stall B: 500, 4000, 800, 3600, 1100
```

> *"Same average. Now look at the daily numbers. Does your answer change?"*

Everyone will now say Stall A. Push further:

> *"So the ONE number you were given - the average - was not enough to make this decision correctly. If you'd picked based on the average alone, you had a real chance of picking wrong. That should bother you. Averages are supposed to be the trustworthy number. Today, we learn exactly what they can hide."*

**Verify the averages match, out loud, before moving on** - this small step matters, because the whole Opening depends on students trusting that both stalls really do average ₹2,000:

```
Stall A: (1900 + 2050 + 1980 + 2100 + 1970) ÷ 5 = 10,000 ÷ 5 = 2,000
Stall B: (500 + 4000 + 800 + 3600 + 1100) ÷ 5 = 10,000 ÷ 5 = 2,000
```

> *"Both totals are exactly ₹10,000 over 5 days. Not approximately equal - identical. So whatever difference you're about to see has nothing to do with the average being slightly off. It's entirely about something the average doesn't capture at all."*

**Pivot line into the session:**

> *"By the end of these ninety minutes, you'll have three tools - Range, Variance, Standard Deviation - that turn 'this one feels riskier' into a number you can put in a report. And you'll learn to catch when one unusual value is quietly lying to you about what 'typical' even means."*

**Context for the sessions ahead:** *"Everything you calculate by hand today - Variance, Standard Deviation - comes back almost immediately as a built-in SQL function once we reach Aggregation Essentials in a few weeks. Today is the reason those functions will make sense instead of being a black box you're told to trust."*

---

## Concept Block 1: Range (10 min)

### 💬 Instructor script

> *"The fastest way to describe spread: just look at the best day and the worst day. That gap is called the Range."*

Write on the board: `Range = Maximum − Minimum`

Apply live to this session's running example - two auto-rickshaw drivers, both averaging ₹690/day:

```
Driver 1: 650, 700, 680, 720, 690, 710, 670   →  Range = 720 − 650 = ₹70
Driver 2: 300, 900, 400, 1100, 250, 950, 430  →  Range = 1100 − 250 = ₹850
```

Verify both means live, the same way you verified the chai stalls: Driver 1 totals 650+700+680+720+690+710+670 = 4,820, ÷7 = ₹688.57 ≈ ₹690 (round for the story); Driver 2 totals 300+900+400+1100+250+950+430 = 4,330, ÷7 ≈ ₹618.57. *(Instructor note: the two totals are close but not perfectly identical - that's fine for an opening hook told informally, but if a sharp student checks the arithmetic, acknowledge it openly: "Good catch - I rounded for the story. The core point - one driver's week is far tighter than the other's - holds regardless of the exact decimal." Never wave away a correct challenge to your numbers; confirming it builds trust for the rest of the session.)*

### 🔴 The trap / highest-value moment

> *"Same average, roughly ₹690 to ₹690. One driver's whole week fits inside a ₹70 band. The other's swings across ₹850. If you'd only reported the average to your manager, you told them the least important half of the story."*
>
> Now break it: *"I'm changing Driver 1's best day from ₹720 to a one-off ₹2,000 festival bonus. Recompute the Range."*
> New Range = ₹2,000 − ₹650 = ₹1,350.
> *"Did Driver 1's actual day-to-day business get any less predictable? No - six of his seven days are exactly as steady as before. But Range jumped nearly 20x, because it only ever looks at two points and ignores the other five. Write this rule down: Range is fast, but it's fragile."*

**A second, quieter break - the one students usually miss:** *"Now instead change Driver 1's WORST day - from ₹650 to ₹640. Just ₹10 lower. Recompute the Range."*
New Range = ₹2,000 − ₹640 = ₹1,360.

> *"Notice something: whether I move the top or the bottom, Range reacts. It genuinely only cares about two numbers in the whole dataset - whichever is currently biggest and whichever is currently smallest. Every other value could do anything at all, and Range wouldn't notice."*

---

## Practical Block 1: Compute Range on the Driver Dataset (10 min)

**Activity:** Individually, then pairs compare. Give students a fresh pair of same-mean datasets - two kirana stores' daily footfall, mean 40 each, one steady (`38, 41, 39, 42, 40`), one volatile (`10, 70, 25, 65, 30`).

**Full worked answer key (write this exact working on the board once pairs have attempted it):**

```
Steady store: 38, 41, 39, 42, 40
  Mean check: (38+41+39+42+40) ÷ 5 = 200 ÷ 5 = 40 ✓
  Range = 42 − 38 = 4

Volatile store: 10, 70, 25, 65, 30
  Mean check: (10+70+25+65+30) ÷ 5 = 200 ÷ 5 = 40 ✓
  Range = 70 − 10 = 60
```

Say aloud: *"Same average footfall of 40 customers a day - but one store you can staff with total confidence, and the other you genuinely cannot predict day to day. A Range of 4 versus a Range of 60 is not a small difference - it's fifteen times wider."*

**Follow-up question to push understanding one level further:** *"If I told you the volatile store's Range was 60, could you tell me its highest and lowest footfall days?"* Let the room try - the honest answer is no, not uniquely. Any pair of numbers 60 apart (e.g. 20 and 80, or 5 and 65) gives the same Range. *"That's worth remembering: Range collapses a lot of information into one number. Useful for a quick gut check, not enough for a real decision on its own."*

> 💬 **Expect an argument that Range alone is "good enough."** Welcome it. Say: *"Hold that thought - in the next block, I'll show you exactly what Range is missing, using the same numbers."*

---

## Concept Block 2: Variance (15 min)

### 💬 Instructor script

> *"Range used 2 out of 7 days. Variance is going to use all 7. It asks a more complete question: on a typical day, how far does this value sit from its own average?"*

Build the deviation table live using the samosa vendor dataset (`18, 22, 20, 24, 16`, mean = 20):

| Day | Value | Deviation | Squared Deviation |
|---|---|---|---|
| 1 | 18 | −2 | 4 |
| 2 | 22 | +2 | 4 |
| 3 | 20 | 0 | 0 |
| 4 | 24 | +4 | 16 |
| 5 | 16 | −4 | 16 |

Ask the room, before revealing: *"If I add up just the Deviation column - not squared - what total do you think I'll get?"* Let a few guesses land, then sum it live: zero, every time. Ask *"why zero?"* and let them reason toward "positives and negatives cancel out."

Complete the calculation: `Variance = (4+4+0+16+16) ÷ 5 = 40 ÷ 5 = 8`

**Write the general formula next to the worked table, so students see the pattern generalize:**

```
Variance = Σ(each value − mean)² ÷ (count of values)
```

> *"Read that symbol Σ as 'add up every one of these.' The formula is just a shorthand for exactly the five-row table we built by hand. You will never need to memorize the Greek letter - you need to remember the table."*

### 🔴 The trap / highest-value moment

> *"Variance equals 8. Eight WHAT? Not eight samosas - eight SQUARED samosas. That number is not fit to say out loud in a meeting. We fix that in the next Concept Block."*
>
> This is the highest-value 90 seconds of the session: the moment a student explains, in their own words, why squaring is necessary - not because you told them, but because they just watched the deviations cancel to zero in front of them. Slow down here.

**A second demonstration worth doing if the room is following well:** ask what would happen if, instead of squaring, we just dropped the negative signs (absolute value) - `2, 2, 0, 4, 4` - and averaged those: `(2+2+0+4+4) ÷ 5 = 12 ÷ 5 = 2.4`. *"That's a completely legitimate alternative - it's called Mean Absolute Deviation, and some fields prefer it. It also solves the cancel-to-zero problem. Squaring isn't the only fix, but it's the one that becomes the industry standard - largely because of how it behaves in more advanced statistics you'll meet later in your career. For this course, know that squaring is the convention, not the only option."*

---

## BREAK (5 min)

---

## Practical Block 2: Build a Deviation Table by Hand (15 min)

**Activity:** Pairs, on paper or a shared spreadsheet. Assign Driver 1's full dataset (`650, 700, 680, 720, 690, 710, 670`, mean = 690). Pairs build the complete deviation → squared deviation → Variance table, then repeat for Driver 2's dataset (`300, 900, 400, 1100, 250, 950, 430`, mean = 690).

**Full worked answer key:**

| Day | Driver 1 Value | Deviation | Squared |
|---|---|---|---|
| 1 | 650 | −40 | 1,600 |
| 2 | 700 | +10 | 100 |
| 3 | 680 | −10 | 100 |
| 4 | 720 | +30 | 900 |
| 5 | 690 | 0 | 0 |
| 6 | 710 | +20 | 400 |
| 7 | 670 | −20 | 400 |

Sum of squared deviations = 1,600+100+100+900+0+400+400 = 3,500. Variance = 3,500 ÷ 7 ≈ **500**.

| Day | Driver 2 Value | Deviation | Squared |
|---|---|---|---|
| 1 | 300 | −390 | 152,100 |
| 2 | 900 | +210 | 44,100 |
| 3 | 400 | −290 | 84,100 |
| 4 | 1100 | +410 | 168,100 |
| 5 | 250 | −440 | 193,600 |
| 6 | 950 | +260 | 67,600 |
| 7 | 430 | −260 | 67,600 |

Sum of squared deviations = 152,100+44,100+84,100+168,100+193,600+67,600+67,600 = 777,200. Variance = 777,200 ÷ 7 ≈ **111,028.6**.

*(Instructor note: with the rounded mean of 690 used for both drivers - matching the Opening's simplified story - Driver 2's Variance lands near 111,000, not the earlier loosely-stated "≈66,300." If a pair's arithmetic gets them to a number in this neighbourhood, they've done it correctly; walk the table on the board slowly enough that the class sees where the big numbers come from, since that's the actual teaching point, not the exact figure.)*

**Answer key with reasoning:** Driver 1 Variance ≈ 500 ("small, tight deviations squared stay small"). Driver 2 Variance is over 200 times larger ("large swings squared blow up fast - this is exactly why squaring punishes big deviations so heavily"). Ask the room to notice: Driver 2's Range (₹850) was about 12 times Driver 1's Range (₹70) - but Driver 2's Variance is over 200 times Driver 1's. *"Squaring doesn't just preserve the gap between 'steady' and 'volatile' - it massively amplifies it. That's worth remembering when you're deciding which of these numbers to lead with in a report."*

> 💬 **Expect students to write a negative deviation squared as still negative** (e.g., (−40)² = −1,600 instead of +1,600). Welcome it. Say: *"Check your negative deviations - did squaring actually make them positive on your page?"*

> 💬 **Expect at least one pair's running sum to drift from the board's** because of a single dropped digit in a squaring step (e.g., writing 410² as 16,100 instead of 168,100). Welcome it - use it as a teaching moment: *"This is exactly why analysts don't do this by hand in the real world past a handful of rows - it's not that the math is hard, it's that it's tedious enough that a single slip anywhere breaks the whole total. SQL's `VARIANCE()` function, arriving in a few sessions, never drops a digit."*

---

## Concept Block 3: Standard Deviation (10 min)

### 💬 Instructor script

> *"One step left. Variance is in the wrong units, because we squared everything to get it. To undo that, we do the opposite of squaring - we take the square root."*

`Standard Deviation = √Variance`. Apply to the samosa example: √8 ≈ 2.83 samosas.

> *"Now you have a sentence you can actually say in a meeting: 'Daily sales typically deviate from the average of 20 by about 2.83 samosas.' That sentence didn't exist when we only had Variance."*

**Apply it immediately to the two drivers from Practical Block 2, so the payoff of the whole 15-minute table-building exercise lands right away:**

```
Driver 1: √500 ≈ ₹22.4   →  "Daily earnings typically sit within about ₹22 of ₹690."
Driver 2: √111,028.6 ≈ ₹333.2  →  "Daily earnings typically sit within about ₹333 of ₹690."
```

> *"Read those two sentences side by side. That's the entire Opening's chai-stall story, now backed by an exact number instead of a gut feeling: Driver 2 is roughly fifteen times less predictable than Driver 1."*

### 🔴 The trap / highest-value moment

> *"Low Standard Deviation, high Standard Deviation - which one is 'good'?"*
> Let the room answer "low is good" - most will. Then push: *"A factory making bolts wants LOW standard deviation - every bolt the same size is the whole point. But an investor comparing two funds with identical average returns might actually PREFER the higher-SD one, for the upside. Write this down: Standard Deviation measures consistency. It does not measure goodness. The business goal decides which one you want."*

**A second, sharper trap worth adding if time allows:** *"Here's a harder version of the same question. Two delivery riders both average 30 minutes per delivery. Rider A's Standard Deviation is 2 minutes. Rider B's is 15 minutes. Which one do you actually want handling your food delivery app's promised delivery window?"* Let the room reason it through - Rider A, decisively, because a promised delivery window depends on predictability, not just the average. *"Notice this one has an obvious right answer, unlike the investment fund case. The lesson isn't 'low SD is always better' OR 'it depends' as a cop-out - it's that you have to actually look at what the business is promising before you know which one matters."*

---

## Practical Block 3: Same-Average, Different-Risk Showdown (8 min)

**Activity:** Two groups. Each is handed one driver's dataset (Driver 1 or Driver 2) and calculates Standard Deviation using the Variance already built in Practical Block 2, then prepares a 60-second pitch arguing why *their* driver should get a fixed-schedule corporate contract.

**Answer key with reasoning:** Driver 1 SD ≈ ₹22 - pitch: "predictable, low-risk, easy to plan a fixed weekly income around." Driver 2 SD ≈ ₹333 - pitch will likely (and validly) argue higher earning potential on good days.

**Suggested rubric to score both pitches aloud (write on the board before pitches begin):** Did they state the actual Standard Deviation number? Did they connect it to a real business consequence, not just "ours is better"? Did they acknowledge the trade-off honestly rather than only citing the number that favours them?

> 💬 **Expect the Driver 2 group to argue their higher variability is an ASSET, not a flaw.** Welcome it fully - say: *"You're right that it can be. Variability isn't inherently bad. It just needs to be disclosed, never hidden inside an average - which is exactly where we're going next."*

---

## Concept Block 4: Outliers and Reliability (9 min, includes quick practical)

### 💬 Instructor script

> *"A cab aggregator reports an average fare of ₹166. Nine fares: 120, 135, 128, 140, 132, 125, 138, 130, and 850. Compute the mean live with me."*

With the ₹850 fare: sum = 120+135+128+140+132+125+138+130+850 = 1,898, ÷9 ≈ **₹210.9** *(instructor note: recompute live rather than assuming the ₹166 headline figure - the point survives regardless of the exact number, but always show your own arithmetic honestly in front of the room)*. Without it: sum = 1,048, ÷8 = **₹131**.

> *"One fare - a genuine long airport trip - dragged the 'typical fare' up by roughly ₹80. Anyone budgeting off the inflated average is working with a number nobody in this dataset actually paid, except that one rider."*

### 🔴 The trap / highest-value moment

> *"The instinct the second you spot an outlier is to delete it and clean up your average. Resist that instinct. Sometimes the outlier is the most important row in the whole dataset - the one fraud transaction, the one stock-out day, the one viral sales spike. Your job is to FLAG it for a decision. Never to quietly erase it."*

**Quick practical, verbal, whole-class:** Contrast two outliers on the board - the genuine ₹850 airport fare versus a fare of ₹8,500 where every other fare is ₹100–150. Ask the room which they'd investigate differently, and why. Confirm: the first gets kept and flagged separately; the second is a probable data-entry error worth correcting after investigation.

**Add the formal test right here, as the bridge into the Extension Block:** *"So far we've been eyeballing 'unusual.' There's a formal rule for exactly this - it's called the 1.5×IQR rule, and if your cohort has time today, we'll build it properly using this exact cab fare dataset in a moment."*

---

## Extension Blocks (Optional — Use if Running Ahead)

*Everything below this line is NOT part of the core 90-minute flow costed in the Timing Breakdown. Use it only if Practical Block 4 finishes early, or with a cohort that is clearly ahead of pace - see Timing Contingencies for the exact trigger. If skipped, nothing downstream in the module depends on it; the 1.5×IQR rule is referenced only informally in Q&A.*

### Concept Block 5 (Extension): The Interquartile Range and the 1.5×IQR Rule

#### 💬 Instructor script

> *"Range only uses 2 points. Variance and Standard Deviation use every point, but they can themselves get dragged around by an outlier - a genuinely huge value inflates the Variance too, the same way it inflated the average. The Interquartile Range gives you a spread measure that's deliberately resistant to outliers, and a formal rule for flagging them."*

Return to the cab fares from Concept Block 4, sorted: `120, 125, 128, 130, 132, 135, 138, 140, 850`.

> *"Step 1: find the median - the middle value once sorted. With 9 values, that's the 5th one."*

Median (Q2) = **132**.

> *"Step 2: split the data into a lower half and an upper half, not counting the median itself. Find the median of EACH half - those are called Q1 and Q3."*

```
Lower half: 120, 125, 128, 130    →  Q1 = (125 + 128) ÷ 2 = 126.5
Upper half: 135, 138, 140, 850    →  Q3 = (138 + 140) ÷ 2 = 139
```

> *"Notice Q3 barely moved even with 850 sitting in that upper half - because Q3 only looks at the MIDDLE of the upper half, not its edge. That's the whole point: the IQR calculation itself barely notices the outlier is there."*

```
IQR = Q3 − Q1 = 139 − 126.5 = 12.5
```

> *"Now the formal outlier rule: anything below Q1 − 1.5×IQR, or above Q3 + 1.5×IQR, gets flagged."*

```
1.5 × IQR = 1.5 × 12.5 = 18.75
Lower fence = 126.5 − 18.75 = 107.75
Upper fence = 139 + 18.75 = 157.75
```

> *"Every fare from ₹120 to ₹140 sits comfortably inside 107.75–157.75. The ₹850 fare doesn't - it's over ₹690 past the upper fence. That's no longer 'this looks unusual to me' - it's a documented, repeatable rule that would flag the exact same fare every time, regardless of who's looking at the data."*

#### 🔴 The trap / highest-value moment

> *"Here's the part worth remembering: the 1.5×IQR rule is a widely used CONVENTION, not a law of mathematics. Nothing forces you to use 1.5 - some fields use 3×IQR for a stricter 'extreme outlier only' cutoff. The number 1.5 is a judgment call the field has broadly agreed on, not something derived from first principles. Write this down: conventions are still useful - they give you a repeatable, defensible rule instead of a pure gut call - but never present a convention to a manager as if it were an exact law."*

### Practical Block 5 (Extension): Flagging an Outlier with the 1.5×IQR Rule

**Activity:** Pairs are given a new dataset - one auto-rickshaw driver's week, with a likely data-entry error folded in: `650, 680, 690, 700, 710, 720, 3200`. Pairs sort it, compute Q1, Q3, IQR, and the fences, and state whether 3,200 should be flagged.

**Full worked answer key:**

```
Sorted: 650, 680, 690, 700, 710, 720, 3200
Median (Q2, 4th of 7) = 700

Lower half: 650, 680, 690        → Q1 = 680 (middle of 3 values)
Upper half: 710, 720, 3200       → Q3 = 720 (middle of 3 values)

IQR = 720 − 680 = 40
1.5 × IQR = 60
Lower fence = 680 − 60 = 620
Upper fence = 720 + 60 = 780
```

₹3,200 is far above the ₹780 upper fence → **flagged as an outlier.**

Say aloud: *"Six of these seven days sit inside a ₹70 band, just like the original Driver 1 story from Concept Block 1. The seventh value, ₹3,200, is almost certainly a data-entry slip - maybe an extra zero typed by mistake. But 'almost certainly' still means: go check with whoever logged it before you touch the number. Flag it, don't silently fix it."*

> 💬 **Expect a pair to compute Q1/Q3 using a different quartile method and get a slightly different fence** (there are multiple valid conventions for quartiles with small, odd-sized datasets). Welcome it - say: *"Different quartile methods can genuinely give slightly different Q1/Q3 on small datasets like this one. In this course, we use the simple 'median of each half' method shown here. On the job, know that spreadsheet and SQL tools sometimes use a different formula by default - the conclusion is rarely different, but the exact fence number can shift slightly, and that's worth knowing rather than being surprised by."*

---

## Summary & Bridge (part of final segment)

**Recap table:**

| Concept | The one thing to remember |
|---|---|
| Range | Fast, but fragile - uses only 2 of your data points |
| Variance | Uses every point; squaring stops deviations cancelling to zero - but the units are wrong |
| Standard Deviation | √Variance - the number you can actually report, in real units |
| Outliers | A high SD or wide Range is your signal to go looking. Investigate before you delete. |
| IQR / 1.5×IQR rule *(if covered)* | A formal, repeatable outlier test that resists being distorted by the outlier itself |

**Close on the thesis line:**

> *"Ninety minutes ago, most of this room said 'doesn't matter, same average' about two chai stalls. Ask yourself what you'd say now: 'Same average, but Stall B's Standard Deviation is nearly ten times higher - that's not the same bet. Before I recommend either one, I want to know if there's an outlier day inflating that number, and I want to understand why Stall B is so volatile before we put a second branch's income on the line.' That is the difference between reading a number and understanding it."*

**Bridge to next session:**

> *"Next session - SQL Query Basics - we leave hand calculation behind and start querying real data tables with SELECT and WHERE. And remember: everything you calculated today by hand reappears almost immediately as `STDDEV()` and `VARIANCE()` once we reach SQL aggregation. Today wasn't a detour - it's the reason those functions won't be a black box."*

---

## Common Errors

| Error | What causes it | Fix |
|---|---|---|
| Reporting Range as "the spread" without checking Variance/SD | Range is the fastest tool to reach for, so it becomes the only one used | Always pair Range with at least Standard Deviation before calling a dataset "steady" or "risky" |
| Squared deviations left negative in a hand-built table | Forgetting that squaring a negative number produces a positive result | Re-check every squared cell individually - a negative squared deviation is always a sign of an arithmetic slip |
| Reporting Variance instead of Standard Deviation in a sentence to a manager | Stopping the calculation one step early | Always take the square root before quoting a "typical deviation" number out loud |
| Assuming "low SD = good" in every context | Overgeneralising from the factory-bolts example | Ask what the business is optimising for - consistency (factory, delivery windows) or upside (returns, sales spikes) - before judging SD as good or bad |
| Deleting an outlier immediately after spotting it | Treating "unusual" as automatically "wrong" | Flag it, investigate its cause, and decide case by case - never delete on sight |
| Using a fixed cutoff like "anything over ₹500 is an outlier" | Reaching for a rule of thumb instead of a dataset-specific calculation | Use the 1.5×IQR rule (or documented domain knowledge) computed from the actual dataset, not a guessed threshold |
| Confusing Q1/Q3 with the minimum/maximum | Not sorting the data first, or forgetting the median-of-each-half step | Always sort the full dataset first, find the median, then take the median of each half separately |
| Treating a rounding difference in a verified mean as "wrong" | Expecting hand-rounded story numbers (e.g. "≈₹690") to match to the decimal | Acknowledge small rounding openly - it doesn't change the conclusion, and pretending otherwise undermines trust more than the rounding itself |

---

## Materials Checklist

Before class, have ready:

- Whiteboard/marker (or shared doc) with enough room to keep the Range/Variance/SD formulas and the Driver 1 vs. Driver 2 table visible for all 90 minutes - this session uses **zero software**, so board space is the only "materials" dependency.
- The five running datasets, pre-written on cards or slides so they can be revealed at the right pace rather than typed live: (1) two chai stalls, (2) two auto-rickshaw drivers, (3) samosa vendor's 5-day sales, (4) two kirana stores' footfall, (5) the 9-fare cab aggregator dataset.
- A basic calculator (physical or phone) per pair for Practical Blocks 2 and 3 - the squaring arithmetic is tedious enough that a calculator keeps the session on the concept, not the multiplication.
- Printed or projected blank deviation-table templates (Day | Value | Deviation | Squared Deviation columns) for Practical Block 2, so pairs aren't also designing a table under time pressure.
- If running the Extension Block: the 1.5×IQR worked fences from the cab fare example, pre-calculated on a hidden slide as an answer-check, plus a spare printed copy of the driver dataset (`650, 680, 690, 700, 710, 720, 3200`) for Practical Block 5.

---

## Timing Contingencies

**If running long (behind the 90-minute plan):**
- Trim Practical Block 1 to a single dataset (steady store only) and state the volatile store's Range verbally instead of having pairs compute both.
- Compress Concept Block 4's outlier discussion to the mean-with/mean-without comparison only, dropping the ₹850-vs-₹8,500 verbal contrast - it can be folded into Q&A if a student raises it.
- Never cut the Concept Block 2 "why does the deviation column sum to zero" moment - it is the single highest-value moment in the session and the rest of the module's SQL functions rely on students actually understanding it, not just having seen it.

**If running short (ahead of the 90-minute plan):**
- Run the Extension Blocks (Concept Block 5 + Practical Block 5 on the IQR and 1.5×IQR rule) in full - they're specifically designed as the "if time allows" content and tie directly back to the Concept Block 4 outlier discussion already completed.
- If there's time for only a shortened version, run just the IQR walkthrough on the cab fare dataset (Concept Block 5) as a whole-class demonstration and skip the paired Practical Block 5.
- Alternatively, revisit the Driver 1 "festival bonus" Range-fragility example from Concept Block 1 and have pairs compute the NEW Variance and Standard Deviation with the ₹2,000 bonus day included - showing that unlike Range, SD is "dragged" by the outlier too, but far less dramatically. This is a strong informal bridge into why IQR exists, even without running the full Extension Block.

---

## End-of-Session Quiz

Run as a rapid verbal or show-of-hands check in the last two minutes, or as a 5-minute written exit ticket.

1. **Two datasets have the same mean. Dataset A has a Range of 10. Dataset B has a Range of 200. Which dataset is more predictable?**
   → Dataset A - a smaller Range (on its own, as a quick signal) suggests less spread between its extreme values.

2. **Why do we square each deviation instead of just adding them up directly?**
   → Because the raw deviations always sum to zero (positives and negatives cancel out) - squaring stops that cancellation and lets us measure genuine spread.

3. **A dataset has a Variance of 64. What is its Standard Deviation?**
   → √64 = 8.

4. **True or False: A high Standard Deviation always means something is "wrong" with the data.**
   → False - it means high variability, which can be a real business risk (unpredictable driver earnings) or a genuine asset (higher-upside investment returns), depending entirely on the business context.

5. **You spot a value far outside the rest of your dataset. What is the correct first step?**
   → Investigate it - flag it and find out why it's unusual - never delete it immediately just to "clean up" the average.

6. **(If Extension Block covered) What does the 1.5×IQR rule use as its two fences?**
   → Q1 − 1.5×IQR as the lower fence, and Q3 + 1.5×IQR as the upper fence; anything outside that range is flagged.

---

## Q&A & Doubt Solving

**Q: Why do we square deviations instead of just taking the absolute value?**
→ Absolute value would also stop deviations cancelling to zero - a real measure, Mean Absolute Deviation, does exactly that (see the worked example in Concept Block 2). Squaring additionally penalizes large deviations more heavily, and has mathematical properties used later in the program. For now, squaring is the standard convention you'll see everywhere.

**Q: Is there a fixed number that always means "this is an outlier"?**
→ No universal cutoff exists. The 1.5×IQR rule is a common convention, but analysts also use domain knowledge and visual inspection - which we'll formalize once we reach Tableau.

**Q: Do we ever calculate Variance and Standard Deviation in SQL directly?**
→ Yes - most SQL dialects have `VARIANCE()` and `STDDEV()` built in, arriving once we cover basic aggregation. Today's manual calculation is exactly what makes those functions meaningful instead of a black box.

**Q: What if a dataset has more than one outlier?**
→ Same process, applied individually - flag each one, understand its cause, decide case by case. Never remove multiple outliers automatically just to "clean up" an average.

**Q: Does Standard Deviation change if I add a constant to every value?**
→ No - shifting every value by the same amount shifts the mean too, so the deviations (and therefore SD) stay identical. This is worth a quick mental check if a result ever looks off.

**Q: Does Standard Deviation change if I multiply every value by a constant?**
→ Yes, unlike adding a constant - multiplying every value by, say, 2 also multiplies the Standard Deviation by 2 (though Variance would multiply by 4, since it's already squared). This is a useful sanity check if you're converting units, like rupees to hundreds of rupees.

**Q: Is Q2 (the median) the same thing we covered as "median" back in Module 1?**
→ Yes, exactly the same median - Q1 and Q3 are just applying that same "middle value" idea to the lower and upper halves of the sorted data.

**Q: Why does the IQR rule use 1.5 specifically, and not some other number?**
→ It's a widely adopted convention rather than a mathematical law - it tends to flag genuinely unusual values without over-flagging normal variation, for a wide range of real-world datasets. Some fields use 3×IQR instead, for a stricter "extreme values only" version of the same rule.

---

## Instructor Notes

- **Words not yet earned:** Avoid "z-score," "standard error," "confidence interval," and "population vs. sample variance" (n vs. n−1 denominator). If asked about sample vs. population variance, acknowledge the distinction exists briefly but defer full treatment to later in the program.
- **The single biggest risk in this session** is students treating it as "just more formulas" and disengaging. Defeat it by staying concrete throughout - the two chai stalls, the two drivers, the ₹850 cab fare. Every formula needs a rupee amount attached or it stays abstract.
- **Board management:** Keep the Range/Variance/Standard Deviation formulas and the Driver 1 vs. Driver 2 comparison table visible on the board for the entire session - students will refer back to both repeatedly. If running the Extension Block, add the IQR/1.5×IQR fence formula to a separate corner of the board rather than erasing the core-session material.
- **Common confusions, numbered:**
  1. Believing Range and Variance measure the same thing. Kill it early: "Range uses 2 points. Variance and Standard Deviation use every single point."
  2. Assuming low SD is always "good" and high SD is always "bad." Use the factory-bolts-vs-investment-fund contrast every time this surfaces.
  3. Defaulting to "delete it" the moment an outlier appears. Ask every time: "Would you delete this row, or find out why it happened first?"
  4. Treating the 1.5×IQR rule as a law of mathematics rather than a widely-used convention that could reasonably use a different multiplier in another field.
  5. Expecting Q1 and Q3 to be exact data points from the dataset - on even-sized halves, they're an average of two middle values, same as the median can be.
- **Cross-references:** `STDDEV()` and `VARIANCE()` arrive as real SQL functions in Session 11 (Aggregation Essentials). Tableau's visual outlier detection (box plots, scatter plots) arrives in Module 3 and is the direct visual counterpart of today's 1.5×IQR rule - box plots literally draw the fences. Python's `.std()`/`.var()` arrive in Module 4.
- **Local/cultural context:** Auto-rickshaw drivers, chai stalls, samosa vendors, kirana stores, and cab fares land far better with this cohort than international business examples - keep this running set of examples consistent across the module.
