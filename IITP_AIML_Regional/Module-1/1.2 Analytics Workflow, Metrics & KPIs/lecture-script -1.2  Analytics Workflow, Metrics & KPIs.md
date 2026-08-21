# Lecture Script: Analytics — Analytics Workflow, Metrics & KPIs
> **Instructor Reference** — Module 1: Analytics Foundations + GenAI + Spreadsheets | Academic Session 2 | Duration: 1 Hour | Instructor: [Name/Placeholder]

---

## Session Overview
**Goal:** By the end, students can walk any vague business problem through the problem → data → analysis → insight workflow, break a big problem into smaller data-answerable questions, distinguish a metric from a KPI, and convert a fuzzy business question into a measurable KPI.

**Student profile at this point:** Students arrive knowing mean/median/mode/range/outliers from Session 1 — comfortable computing numbers, but not yet trained to ask *what number should I even compute, and why?* Boredom risk: this session is more conceptual/verbal than numerical, so some students may feel it's "less real" than Session 1's formulas — counter this by keeping every abstraction tied immediately to a Zappy Mart decision.

**Key outcome:** Every student should leave able to take a vague complaint like "our numbers look bad" and instinctively ask "sharper problem statement, then which metric becomes the KPI?"

> 🎯 **The one sentence this session must land:** *Good analysis doesn't start with data — it starts with a sharp question, and ends with one number you're willing to be judged by.*

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| Opening — "Our Numbers Look Bad" | 6 min | 6 min |
| Concept Block 1: The Analytics Workflow + Practical | 11 min | 17 min |
| Concept Block 2: Breaking Down a Big Problem + Practical | 11 min | 28 min |
| **BREAK** | 3 min | 31 min |
| Concept Block 3: Metrics vs KPIs + Practical | 12 min | 43 min |
| Concept Block 4: Question to KPI + Practical | 11 min | 54 min |
| Summary & Bridge | 3 min | 57 min |
| Q&A & Doubt Solving | 3 min | 60 min |

---

## Opening — "Our Numbers Look Bad" (6 min)

Write this exact sentence on the board, nothing else:

> **"Zappy Mart's regional head says: 'Our numbers look bad this quarter. Fix it.'"**

> "You're the analyst who gets this message. Raise your hand if you'd know exactly what to open in Excel right now."

[Pause — very few hands, if any.]

> "Right. 'Numbers look bad' isn't actually a question yet — it's a feeling. And yet this is exactly how real business problems arrive on an analyst's desk: vague, urgent, and undefined. If you start pulling random reports right now, what's likely to happen?"

[Let students suggest: wasted time, wrong analysis, still no clear answer.]

**Pivot line:**
> "Today is about the discipline that turns 'numbers look bad, fix it' into something you can actually act on — a repeatable workflow, and a way to land on the *one number* that tells you whether you actually fixed it. Everything you learned last session — mean, median, range — those are tools. Today you learn *when and why* to reach for them."

> "This workflow is also the skeleton for the entire rest of this course — SQL, Tableau, Python — every tool ahead is just a faster way to execute one of today's four steps."

---

## Concept Block 1: The Analytics Workflow (11 min)

> "Let's fix the regional head's vague complaint together. Step 1 is always: define the actual problem. What questions would you ask the regional head before doing anything else?"

[Draw out: bad compared to what — last quarter? target? which branches? all products or some?]

Write the four-step workflow on the board:

**Problem → Data → Analysis → Insight**

> "Walk with me. Suppose after questioning, we land on: 'Udaipur branch sales dropped 15% last month.' That's Step 1 — sharp and specific. Step 2 — what data do we now need?"

[Draw out: daily sales, footfall, promotions run, stock levels.]

> "Step 3 — analysis — we compare week by week, check for stock-out days, look at footfall trend. Step 4 — insight — say we find sales dropped mainly on 4 days when the top SKU was out of stock. That's a real, evidence-backed insight — not a guess."

### 🔴 The trap / highest-value moment
> "The single biggest mistake new analysts make — someone guess what it is, based on today's opening."

[Draw out: skipping straight to analysis without a sharp problem statement.]

**One-line rule to write down:**
> *"If you can't state the problem in one precise sentence, you're not ready to open the data yet."*

## Practical Block 1: Fix the Vague Problem (part of the 11 min)

> "In pairs, 60 seconds — the regional head says 'customer complaints are increasing, do something.' Rewrite this as a Step 1 problem statement that's specific enough to analyze."

**Answer key (with reasoning aloud):**
> Sample fix: "Have complaint volumes increased month-over-month across all branches, or is the increase concentrated in specific branches or complaint categories (e.g., delivery delays vs product quality)?" — reasoning: this is now specific enough that Step 2 (data) is obvious — pull complaint logs by branch and category.

💬 Expect an argument that this takes too long when "the boss wants an answer now." Welcome it. Say: *"Ten minutes spent sharpening the problem saves hours of analyzing the wrong thing — speed without direction isn't actually fast."*

---

## Concept Block 2: Breaking Down a Big Problem (11 min)

> "Some problems are sharp but still too big to attack in one move. 'Zappy Mart's overall revenue is flat this quarter' is specific — but where do you even start?"

Write it on the board, then break it live with the class into sub-questions:

> "Shout out smaller questions hiding inside this one."

[Guide toward: is it flat across all branches, or some up/some down; flat across all product categories or specific ones; is footfall flat too, or is spend-per-customer the issue; did anything change — pricing, promotions, competitors.]

> "Each of these smaller questions now maps to one specific slice of data you can actually pull and compare. That's the whole trick — a big problem is just several small, answerable ones stacked together."

### 🔴 The trap / highest-value moment
> "Watch what happens if you skip this and try to answer the big question directly."

[Write a weak answer on the board: "Market conditions probably." Let students react to how unconvincing this sounds.]

**One-line rule:**
> *"If your answer to a business problem is vague, it's usually because you never broke the problem down before analyzing."*

## Practical Block 2: Break It Down (part of the 11 min)

> "In pairs, 90 seconds — break down: 'Should Zappy Mart open a new branch in Indore?' into at least three smaller, data-answerable questions."

**Answer key (sample, with reasoning aloud):**
- What's the estimated footfall/customer base in the target Indore location? (demand signal)
- How do nearby competitor stores perform? (competitive pressure)
- What's the cost of setting up and running the branch vs projected revenue? (financial viability)

> "Notice each of these can now be handed to someone to go pull actual numbers — that's the whole point of breaking a problem down."

---

## ☕ BREAK (3 min)

[Keep the Indore breakdown visible on the board — return to it briefly in Concept Block 4.]

---

## Concept Block 3: Metrics vs KPIs (12 min)

> "Zappy Mart tracks a lot of numbers daily — footfall, units sold, average basket size, complaints, staff hours, delivery time, return rate. Are all of these equally important to report to leadership every single week?"

[Let students say no / it depends.]

> "Right — and this is the difference between a metric and a KPI. Someone define metric for me. Now KPI."

Write the definitions:
- **Metric** — any number you can measure
- **KPI** — a metric specifically chosen to track progress toward a goal

> "Same data, different role. If Zappy Mart's stated goal this quarter is 'grow revenue per branch by 10%,' which single metric from that long list becomes the KPI?"

[Draw out: revenue growth % per branch — the others stay as background metrics.]

### 🔴 The trap / highest-value moment
> "What happens to a team that tracks 30 metrics with no clear KPI?"

[Draw out: nobody can say clearly whether the business is winning or losing — too much noise, no signal.]

**One-line rule:**
> *"A metric describes activity. A KPI is the one number you're willing to be judged by."*

## Practical Block 3: Pick the KPI (part of the 12 min)

> "This quarter's stated goal: 'reduce customer complaints.' From the list on the board — footfall, units sold, average basket size, complaints, staff hours, delivery time, return rate — which becomes the KPI, and which stay as background metrics?"

**Answer key (with reasoning aloud):**
> KPI: number/rate of customer complaints (month-over-month) — directly tied to the stated goal. The rest (footfall, units sold, basket size, staff hours, delivery time, return rate) remain useful background metrics — some may even be *drivers* of complaints (e.g., delivery time), worth watching, but they're not what leadership is judged on this quarter.

💬 Expect an argument that "return rate" should also be a KPI since it's related to complaints. Welcome it. Say: *"Good instinct — related metrics can absolutely become secondary KPIs, but the discipline is: don't dilute focus by calling everything a KPI. Pick the one(s) tightly tied to the stated goal."*

---

## Concept Block 4: Converting a Question Into a KPI (11 min)

> "Let's go back to the Indore branch questions from before the break. Take just one: 'What's the estimated demand in the target location?' How do we turn that into an actual trackable KPI?"

Write the conversion checklist on the board:
1. What exact number captures this?
2. Over what time period?
3. Is higher or lower better?
4. Can we actually get this data?

> "Walk it through with me: exact number — maybe average weekly footfall of nearby competing stores. Time period — over the last 3 months. Direction — higher footfall nearby = better demand signal. Can we get it — yes, through store visits or public foot-traffic estimates."

> "Compare that to just saying 'check if Indore has demand' — vague, not trackable. The checklist forces specificity."

### 🔴 The trap / highest-value moment
> "Here's the mistake even experienced analysts make — someone guess it, based on the checklist's 4th question."

[Draw out: picking a KPI just because the data is easy to get, not because it actually answers the business question.]

**One-line rule:**
> *"Easy-to-measure and actually-meaningful are not the same thing — check both."*

## Practical Block 4: Convert It (part of the 11 min)

> "In pairs, 60 seconds — convert this vague goal into a proper KPI using the checklist: 'We want our loyalty program to work better.'"

**Answer key (sample, with reasoning aloud):**
> "Average monthly spend per loyalty-member customer vs non-members, tracked monthly" — satisfies all four checklist questions: exact number (average spend comparison), time period (monthly), direction (higher gap = program working), and it's realistically measurable from existing transaction data.

---

## Summary & Bridge (3 min)

| Concept | The one thing to remember |
|---|---|
| Analytics workflow | Problem → Data → Analysis → Insight — always start with a sharp problem |
| Breaking down problems | A big vague problem is several small, data-answerable ones stacked together |
| Metrics vs KPIs | Metrics describe activity; a KPI is the one number you're judged by |
| Question to KPI | Use the checklist: exact number, time period, direction, measurability |

> "Remember the opening: 'our numbers look bad, fix it.' You now have a repeatable way to turn that into a sharp problem, smaller questions, and one KPI worth reporting."

**Bridge:** "Next session, we bring in **GenAI for Analytics: Prompt, Check, Improve** — you'll use GenAI tools to speed through parts of this exact workflow, like drafting sub-questions or summarizing data, while learning the same discipline from Session 1: never trust an 'average' — or a GenAI output — without checking it first."

---

## Q&A & Doubt Solving (3 min)

**Q: Can a business have more than one KPI at a time?**
→ Yes, but usually a small, deliberately chosen set (often 1-5 for a given goal) — not dozens. Too many "KPIs" defeats the purpose of having a clear focus.

**Q: What if we can't get the data for the ideal KPI?**
→ Use the closest measurable proxy, but be explicit that it's a proxy — e.g., if you can't measure "customer happiness" directly, you might use "repeat purchase rate" as a proxy and say so clearly in your report.

**Q: Isn't breaking down a problem just... asking more questions? What's the actual skill?**
→ The skill is that each sub-question must map to something you can pull from data — not just any question. "Why don't people love us?" isn't data-answerable; "Has our average rating changed month-over-month?" is.

**Q: How is a KPI different from a target/goal?**
→ A KPI is the number you track; a target is the specific value you're aiming for on that KPI (e.g., KPI = revenue growth %, target = 10% this quarter). We'll keep this distinction in mind as we build dashboards in Module 3.

---

## Instructor Notes
- **Words not yet earned — avoid:** OKRs, North Star metric, leading/lagging indicators, dashboard, cohort analysis. These add unnecessary layers this early — keep vocabulary to problem/data/analysis/insight and metric/KPI only.
- **Biggest risk this session:** feels abstract/verbal after Session 1's numeric comfort. Counter by never leaving an abstract idea (workflow step, metric vs KPI) undemonstrated with a concrete Zappy Mart number or decision within 2 minutes of introducing it.
- **Board management:** keep the four-step workflow (Problem → Data → Analysis → Insight) visible on the board for the entire session — refer back to it explicitly in Concept Blocks 2, 3, and 4 so students see it's one continuous framework, not four separate ideas.
- **Common confusions (numbered):**
  1. Treating "numbers look bad" as already a usable problem statement.
  2. Trying to answer a big problem directly instead of breaking it into sub-questions.
  3. Calling every tracked number a "KPI" rather than reserving that term for goal-tied metrics.
  4. Picking a KPI because it's easy to measure rather than because it answers the real question.
- **Cross-references forward:** Session 1.3 (GenAI can help draft sub-questions and summarize workflow steps, but outputs must be checked); Module 2 (SQL `GROUP BY`/aggregation computes the metrics behind KPIs); Module 3 (Tableau dashboards visualize KPIs for stakeholders); Module 4 (full end-to-end workflow automation).
- **Local/cultural context notes:** The "college fest planning" and "Indore new branch" examples landed well — both involve breaking a big ambition into ownable pieces, which resonates with this cohort's own project/event planning experience. Continue using Zappy Mart across Jaipur/Udaipur/Kanpur/Lucknow/Indore for continuity.
