# Lecture Script: Statistics — Statistics: Probability and Uncertainty
> **Instructor Reference** — Module 3: Tableau Dashboards + Storytelling | Academic Session 18 | Duration: 1.5 Hours | Instructor: Abhinandhan

---

## Session Overview
**Goal:** Students can calculate a business probability (like conversion rate, click-through rate, or churn rate) from raw counts, and can correctly explain to a non-technical stakeholder why a high probability is not a guarantee.

**Student profile at this point:** They've just spent a full session building their first Tableau charts, and before that, nine sessions deep in SQL. They are comfortable with exact answers — a query returns exact rows, a chart shows an exact bar height. Expect resistance to the idea that a "correct" answer can still be wrong 1 time in 10. This is also their first statistics session since Session 9 (Spread, Variability and Outliers), so expect some rust on basic quantitative reasoning — rebuild gently before assuming fluency.

**Key outcome:** Students should leave with the instinct to ask "how many times out of how many?" any time someone states a probability or likelihood in a business meeting.

> 🎯 **The one sentence this session must land:** *A probability describes a pattern across many cases — it never promises what happens in any single case.*

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| Opening Hook | 6 min | 6 min |
| Concept + Practical Block 1: The Probability Scale | 15 min | 21 min |
| Concept + Practical Block 2: Likelihood of Business Events | 15 min | 36 min |
| **BREAK** | 8 min | 44 min |
| Concept + Practical Block 3: Conversion Rate & CTR | 18 min | 62 min |
| Concept + Practical Block 4: Probability vs Certainty | 18 min | 80 min |
| Summary & Bridge | 5 min | 85 min |
| Q&A & Doubt Solving | 5 min | 90 min |

---

## Opening — "The Weather Forecast Trap" (6 min)

> "Yesterday's forecast said 80% chance of rain in Hyderabad. It didn't rain. Was the forecaster wrong?"

Take two or three hands. Most will initially say yes.

> "The forecaster was right. Out of every ten days that looked exactly like yesterday, historically, it rained on about eight of them. Yesterday just happened to be one of the other two. The forecast wasn't a promise — it was a pattern."

**Pivot line:** "Every time you calculate a conversion rate, a churn rate, or a click-through rate for Kirana365, you are making exactly this kind of weather forecast about your customers. Today you learn to calculate these numbers correctly — and, just as importantly, to talk about them honestly."

**Context for the sessions ahead:** "This is the third statistics session in the course — after averages, and after spread and variability. Probability is the natural next step: once you know how spread out your data is, the next question is always 'how likely is this specific thing to happen again?'"

---

## Concept Block 1: The Probability Scale (8 min)

> "Think of probability like a volume knob, not a light switch. It doesn't jump from silent to full blast — it slides from 0, completely off, to 1, completely on."

Draw the scale on the board: 0 — 0.5 — 1, labelling "impossible," "coin-flip," "certain."

> "82 out of 100 Kirana365 app-openers during the festival sale placed an order. That's 82 divided by 100 — 0.82, or 82%. Everything sits somewhere on this line."

### 🔴 The trap / highest-value moment
> "Write this rule down, because it's the one mistake I see in every single cohort: a high probability is not certainty. 0.9 still means 1 time in 10, it does not happen. If a number isn't exactly 1, something else is still possible."

## Practical Block 1: Placing Numbers on the Scale (7 min)

Give students five scenarios and ask them to place a rough probability estimate (as a fraction and a %) on the board's scale, then explain their reasoning:
1. A customer who has ordered every week for 6 months orders again this week
2. A brand-new app user who never opened the app again completes a purchase
3. A coin-flip style A/B test shows no clear winner

**Answer key with reasoning:** (1) high, close to 0.9–0.95 — strong established pattern; (2) very low, close to 0–0.05 — no engagement signal at all; (3) close to 0.5 — genuinely uncertain, that's what "no clear winner" means numerically.

💬 **Expect an argument about "why isn't #1 exactly 1.0 if they order every week?"** Welcome it. Say: "Because 'every week for 6 months' is still a pattern, not a law of physics. Something could always break the streak — that's exactly why we never round a strong pattern up to certainty."

---

## Concept Block 2: Likelihood of Business Events (8 min)

> "Picture every customer as a coin — but not a fair one. A loyal customer's coin is weighted toward 'buys again.' A frustrated customer's coin is weighted toward 'leaves.' Probability is how we put a number on that weighting instead of relying on a gut feeling."

Work the churn example on the board: 240 silent customers out of 4,000 active Bengaluru customers → `240/4000 = 0.06` = 6% churn probability.

> "Six out of every hundred customers, roughly, going quiet next month if nothing changes. That's not a guess anymore — it's a number you can act on."

### 🔴 The trap / highest-value moment
> "Now here's the trap: what if I calculated that 6% from just 8 customers instead of 4,000? Small samples swing wildly — one or two people leaving in a tiny group can look like a huge probability that isn't real. Always ask: how many was that number based on?"

## Practical Block 2: Sample Size Sanity Check (7 min)

Present two churn numbers: "Store A: 6% churn, based on 4,000 customers" vs "Store B: 25% churn, based on 8 customers." Ask students which number they'd trust to act on, and why.

**Answer key with reasoning:** Store A's number is trustworthy — a large, stable base. Store B's 25% is just 2 out of 8 people — a tiny shift (one more or one fewer customer leaving) would swing that percentage dramatically. The correct instinct is to treat Store B's number as unreliable until more data comes in, not to panic and launch a retention campaign based on 8 customers.

💬 **Expect pushback**: "But 25% sounds worse — shouldn't we act on the scarier number first?" Welcome it. Say: "The scariest-looking number and the most trustworthy number are not always the same number. That instinct — check the sample size before you react — will save you from chasing noise more times than you'll ever be thanked for."

---

## BREAK (8 min)

---

## Concept Block 3: Conversion Rate and Click-Through Rate (9 min)

> "These are the two probabilities you will calculate more than any other in your career, so let's nail the formulas and, more importantly, when to use each."

Write both formulas on the board and walk the Diwali banner example: 9,000 views → 450 clicks (CTR = 5%) → 140 orders from those clicks (conversion-from-click = 31%).

> "Notice CTR and conversion answer two completely different questions. CTR asks: did anyone even engage? Conversion asks: did engagement turn into money?"

### 🔴 The trap / highest-value moment
> "The trap is reporting only one of these two numbers and letting someone draw the wrong conclusion. A campaign can have a fantastic CTR and a terrible conversion rate — great at grabbing attention, useless at generating sales. You almost always need both numbers side by side."

## Practical Block 3: Diagnose the Campaign (9 min)

Give two campaign scenarios: Campaign X (CTR 8%, conversion-from-click 5%) and Campaign Y (CTR 2%, conversion-from-click 40%). Ask: which campaign would you recommend scaling up, and why?

**Answer key with reasoning:** Campaign Y — despite the low CTR, the people who do click are far more likely to buy, suggesting better audience targeting. Campaign X attracts a lot of low-intent clicks. The right move might be to combine Y's targeting with X's reach, not to simply scale the one with the bigger raw click number.

💬 **Expect an argument that "more clicks is always better."** Welcome it. Say: "More clicks that don't convert just cost you money on ad spend. This is exactly why we never celebrate a single metric in isolation."

---

## Concept Block 4: Probability Is Not Certainty (9 min)

> "Back to the weather forecast. A founder hears '75% of customers who add 3+ items to cart complete checkout' and mentally rounds it up to 'they will buy.' Your job is to gently stop that rounding, every time."

Roleplay the founder conversation on the board, showing the honest reframing: "3 out of 4 such customers typically complete checkout — this particular customer was one of the other one in four, and that's expected, not a system failure."

### 🔴 The trap / highest-value moment
> "The highest-value moment in this entire session: when a stakeholder hears a probability and treats it as a promise, you correct it kindly but immediately. Left uncorrected, that misunderstanding leads to bad decisions — panicking over normal variation, or over-trusting a number that was never a guarantee."

## Practical Block 4: Reframe the Stakeholder Line (9 min)

Give students three stakeholder statements that wrongly treat probability as certainty, and ask them to write a one-sentence honest reframing for each:
1. "Our model says 90% of these leads will convert, so let's not follow up with the other 10%."
2. "We had an 80% chance of rain and it didn't rain, so the forecast was wrong."
3. "6% churn means exactly 6 people out of every 100 will leave, no more, no less."

**Answer key with reasoning:** (1) "90% is still 9 out of 10 — the other 10% still deserve follow-up, they're not a lost cause, just less likely." (2) "The forecast describes a pattern across many similar days, not a guarantee for this one day." (3) "6% is an average pattern — some months it might be 4, other months 9, but around 6 is the expected typical value."

💬 **Expect a question about whether probabilities are ever "wrong."** Welcome it. Say: "A probability is wrong if the underlying pattern was miscalculated — not simply because one outcome went the other way. That distinction is the whole point of today's session."

---

## Summary & Bridge (5 min)

| Concept | The one thing to remember |
|---|---|
| Probability scale | 0 = impossible, 1 = certain, everything real sits in between |
| Likelihood of business events | A probability needs a large enough sample to be trustworthy |
| Conversion rate & CTR | They measure different steps of the same journey — report both |
| Probability vs certainty | A high probability is a pattern, never a promise |

Close on the thesis: "A probability describes a pattern across many cases — it never promises what happens in any single case. Every number you report from here on should carry that honesty with it."

**Bridge to Session 19:** "Next session we're back in Tableau, learning to choose the right chart for the story your data tells — including how to visually communicate a probability like the 31% conversion rate you calculated today, instead of just stating it as a number."

---

## Q&A & Doubt Solving (5 min)

**Q: Is probability the same thing as percentage?**
→ Almost — probability is usually written as a decimal between 0 and 1, and percentage is just that decimal multiplied by 100. They describe the same idea in different units.

**Q: How large does a sample need to be before I trust a probability?**
→ There's no single magic number, but as a working rule for this course: be cautious of any probability calculated from fewer than 30-50 cases, and always state the sample size alongside the number.

**Q: What's the difference between churn rate and churn probability?**
→ In practice, none — churn rate calculated from historical data is exactly how we estimate churn probability going forward, assuming similar conditions continue.

**Q: Can a probability be calculated for something that's never happened before, like a totally new product launch?**
→ Not reliably from data alone — that requires expert judgment or comparison to similar past launches, which is a softer, less precise version of the same idea.

**Q: Why does this matter for Tableau, which is a visual tool, not a statistics tool?**
→ Because every KPI tile you'll build starting Session 21 is a probability or a rate — and how you visually frame it affects whether your audience reads it honestly or over-trusts it.

---

## Instructor Notes
- **Words not yet earned:** "confidence interval," "statistical significance," "Bayesian" — these belong to more advanced statistics; today stays at the level of simple ratios and honest communication.
- **Biggest risk in this session:** Students treating probability as purely a math exercise and missing the communication half of the session — the stakeholder reframing exercises are just as important as the formulas and should not be rushed to save time.
- **Board management:** Keep the probability scale (0 — 0.5 — 1) and the thesis line visible throughout; also keep the CTR and conversion formulas up during Practical Block 3.
- **Common confusions:**
  1. Rounding any high probability up to "will definitely happen."
  2. Trusting a probability without checking the sample size behind it.
  3. Conflating click-through rate and conversion rate as the same metric.
- **Cross-references:** This session's honesty-about-uncertainty theme returns explicitly in Module 4's Statistics: Distributions, Insights and Drawing Conclusions session, and probability-as-a-KPI resurfaces directly in Session 21 (KPIs and Trends on One View).
- **Local/cultural context notes:** The Hyderabad weather-forecast opening and Diwali banner campaign example both land naturally with this cohort; keep the churn/conversion numbers framed around Kirana365's Bengaluru/Hyderabad/Chennai stores for continuity with the Tableau sessions around this one.
