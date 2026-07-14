# Lecture Script: Analytics Workflow, Metrics & KPIs
> **Instructor Reference** — Module 1: Analytics Foundations + GenAI + Spreadsheets | Academic Session 2 | Duration: 1.5 Hours | Instructor: Industry Mentor

---

## Session Overview

**Goal:** Students can take a vague business request, run it through the four-step analytics workflow, decompose it into sharp sub-questions, and define **one KPI** with a formula, a timeframe, a target, and an owner.

**Student profile at this point:** They've had exactly one session (averages, outliers, data types). They know how to summarise a column honestly. They have **no** tools yet — no SQL, no Python, no Tableau. That is fine. **This session deliberately uses zero tools.**

**Key outcome:** Students leave able to answer the question that will be asked of them in every job interview and every Monday meeting: *"What would you actually measure, and what's your target?"*

> 🎯 **The one sentence this session must land:** *Anyone can compute a number. You are paid to know which number is worth computing — and what you'll do when it moves.*

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| Opening & Hook — "Sales are down. Fix it." | 6 min | 0:06 |
| **Concept 1:** The Analytics Workflow (4 steps) | 12 min | 0:18 |
| **Practical 1:** Map a real problem to the 4 steps | 10 min | 0:28 |
| **Concept 2:** Breaking Down a Business Problem | 10 min | 0:38 |
| **Practical 2:** Decomposition sprint (groups) | 12 min | 0:50 |
| **BREAK** | 5 min | 0:55 |
| **Concept 3:** Metrics vs KPIs — The Dashboard Test | 14 min | 1:09 |
| **Practical 3:** Promote the metric to a KPI | 10 min | 1:19 |
| **Concept 4:** Making a Question Measurable | 6 min | 1:25 |
| Summary & Bridge to Session 3 | 3 min | 1:28 |
| Q&A | 2 min | 1:30 |

---

## Opening — "Sales Are Down. Fix It." (6 min)

**Open cold. No agenda slide.** Walk in and say:

> *"You've just been hired as a data analyst. It's your first Monday. Your manager walks past your desk, doesn't sit down, and says four words:*
>
> ### **'Sales are down. Fix it.'**
>
> *…and walks away. You have a laptop, a database, and eight hours. **What do you do first?**"*

**Take answers from the room.** You will hear, roughly in order:
- *"Open the sales data"* → **the most common answer, and the wrong one**
- *"Make a chart of sales over time"*
- *"Compare this month to last month"*

Write them on the board. Don't judge yet. Then:

> *"Every one of those is an action on the DATA. Not one of you asked a question about the PROBLEM. And that is the single most expensive habit in this profession."*

**Now push:**

> *"Let me ask what your manager actually meant. 'Sales are down' — down **compared to what?** Last month? Last year? The forecast? Down in **which product**? In **every city**, or one? Down because **fewer people bought**, or because **the same people spent less**? Those are five completely different problems with five completely different fixes — and your manager gave you none of it."*

Pause.

> *"If you open the spreadsheet before you know which of those five you're solving, you will produce a beautiful, correct, utterly useless chart. Today we learn the process that stops that from ever happening to you."*

**Set the frame for the session:**

> *"Session 1 taught you to summarise a number honestly. Today is harder: **which number, and why?** By the end of these ninety minutes, you will be able to take those four words — 'sales are down' — and hand back a workflow, four sharp questions, and one KPI with a target. That is a professional's answer."*

---

## Concept Block 1: The Analytics Workflow (12 min)

### The doctor analogy — lead with this

> *"Imagine you go to a doctor with a stomach ache. She takes one look at you and immediately writes a prescription. No questions, no tests. Would you take that medicine?"*

Nobody would.

> *"So why do we accept it from analysts? A doctor follows a process: **where does it hurt** (problem) → **run tests** (data) → **read the results** (analysis) → **here's the diagnosis and what to do** (insight). Skip a step and you get malpractice. It is exactly the same for us."*

### The four steps — write these on the board and leave them up all session

```
  1. PROBLEM   →   2. DATA   →   3. ANALYSIS   →   4. INSIGHT
     |                                                   |
     └───────────────── new questions ←──────────────────┘
```

| Step | The question it answers | What you produce | The classic failure |
|---|---|---|---|
| **1. Problem** | *What are we actually trying to decide?* | A sharp, answerable question | Starting work on a vague request |
| **2. Data** | *What do we need, and do we have it?* | The right dataset, cleaned | Using whatever data is handy |
| **3. Analysis** | *What does the data say?* | Numbers, comparisons, trends | Computing things nobody asked for |
| **4. Insight** | *So what should we DO?* | A recommendation | Dumping a chart and going home |

### Two things to hammer (5 min)

**① It is a LOOP, not a line.**

> *"Step 4 almost never ends the story. You find that Bangalore is down 30% — and now you have a new question: why Bangalore? Back to Step 1. Good analysis spirals. If your work ever ends cleanly at Step 4 with no new questions, you probably didn't look hard enough."*

**② Step 1 is the whole game.**

> *"Here's the uncomfortable truth about this profession: **most failed analyses are not wrong. They're correct answers to the wrong question.** The maths was perfect. The chart was beautiful. Nobody needed it."*

> 🔴 **Say this line and let it sit:** *"An analyst who spends three days building a dashboard nobody asked for has produced nothing. An analyst who spends thirty minutes sharpening the question has already done the hardest part of the job."*

### Where students actually go wrong (2 min)

> *"Watch for this in yourself: the pull toward Step 2 is almost physical. Data is comfortable. Data is where you feel competent. Sitting with an unclear problem feels like you're not working. **That discomfort IS the work.**"*

---

## Practical Block 1: Map a Real Problem to the Four Steps (10 min)

**Format:** Whole class, on the board. You drive; they supply the content.

**The scenario — read it out:**

> *"You work at a food delivery app. The Head of Operations says: **'Customers are complaining about late deliveries. Do something.'**"*

**Now build the table live. Ask the room for each cell.**

| Step | What goes here | Answers to steer them toward |
|---|---|---|
| **1. Problem** | What are we deciding? | *"Which deliveries are late, by how much, and is it getting worse?"* — Push them: *"Is 'late' even defined? Late vs what promise?"* |
| **2. Data** | What do we need? | Order time, promised time, actual delivery time, city, restaurant, rider, order date |
| **3. Analysis** | What do we compute? | Average delay; % of orders past the promise; delay broken down by city / restaurant / hour of day |
| **4. Insight** | So what do we DO? | *"38% of late orders come from 5 restaurants that accept orders during their peak kitchen hours. Cap their order intake at peak."* |

**Three teaching beats during this block:**

1. **On Step 1 — force a definition.** When someone says "find late deliveries," ask: *"What is late?"* Let them argue. Land it: **late = actual > promised.** Without a promise time in the data, "late" is meaningless. *This is the single most important habit in the session.*

2. **On Step 3 — resist the average.** Someone will say "compute average delivery time." Callback to Session 1: *"Careful — is the mean the honest number here? If most deliveries are 20 minutes and a few are 3 hours, what does the mean tell you? What would you report instead?"* → **median, plus the % breaching the promise.**

3. **On Step 4 — demand an action.** If a student offers *"deliveries are late in Chennai,"* push back: *"That's a finding, not an insight. What should someone DO on Monday morning?"* Keep pushing until the sentence contains a verb someone can act on.

> 🎯 **Land the block:** *"Notice — we have not opened a single tool. No SQL, no Excel. And we already know exactly what to build. That's twenty minutes of thinking that just saved three days of the wrong work."*

---

## Concept Block 2: Breaking Down a Business Problem (10 min)

### The car analogy

> *"'Why is my car making a noise?' — no mechanic on earth can act on that. But: 'Is it the engine, the brakes, or the wheels? Does it happen when turning, braking, or accelerating?' — now they can work. **You are the mechanic. Vague questions must be cut into testable ones.**"*

### The technique — "which, when, who, what"

Go back to the opening hook. Put it on the board:

> 🗣️ **"Sales are down. Find out why."**

Now cut it, out loud, with the class:

| Dimension | Sharper sub-question |
|---|---|
| **Which** (product) | Are *all* products down, or only some categories? |
| **Where** (region) | Every city, or is one region dragging the total? |
| **When** (time) | A sudden drop, or a slow drift over months? |
| **Who** (customer) | Losing *new* customers, or losing *repeat* customers? |
| **What** (mechanism) | Fewer orders — or the same orders at a lower value? |

### The decomposition that does the most work (4 min)

**Stop on that last row.** Write this on the board and circle it:

```
                REVENUE  =  Number of orders  ×  Average order value
```

> *"Revenue fell. Look at that equation. There are only TWO ways that can happen: fewer orders, or smaller orders. It's arithmetic — there is no third option."*
>
> *"So before you touch any data, you already know your first move: **check which of those two fell.** If orders held steady but the average value dropped, this is a pricing or discounting story. If order count collapsed but the average held, this is a demand or marketing story. **Two completely different teams, two completely different fixes** — and you figured out which one in ten seconds, with no data at all."*

> 🔑 **The principle to write down:** *"Decompose the metric, and the data has fewer places to hide."*

### What makes a sub-question good (2 min)

> ### ✅ **A good sub-question has one property: you can imagine the answer.**
>
> *"If you can't picture what the answer looks like — a number, a comparison, a chart — the question is still too vague. Keep cutting until you can see the shape of the answer."*

**Test it live.** Ask the room: *"Which of these can you picture the answer to?"*
- *"Why are customers unhappy?"* → ❌ No shape. Still vague.
- *"What % of 1-star reviews mention delivery?"* → ✅ You can see it. It's a number.

---

## Practical Block 2: Decomposition Sprint (12 min)

**Format:** Groups of 3–4. **8 minutes to work, 4 minutes to present.**

**Give each group ONE of these vague requests:**

| # | The request |
|---|---|
| A | *"Our app has too many uninstalls."* |
| B | *"The new product launch isn't working."* |
| C | *"Marketing spend is too high."* |
| D | *"Customer support is overwhelmed."* |

**Their deliverable — put this on screen:**

```
1.  Four sharper sub-questions  (use which / where / when / who / what)
2.  ONE decomposition equation  (like revenue = orders × value)
3.  The data you would need     (name the columns)
```

**Hint to offer any group that stalls — the equations they might find:**

```
A.  Uninstalls        = installs × uninstall rate
B.  Launch revenue    = customers reached × conversion rate × price
C.  Cost per customer = total spend ÷ customers acquired
D.  Ticket load       = number of tickets × time per ticket
```

**During presentations, do exactly two things:**

1. For every sub-question, ask: **"Can you picture the answer?"** If not, make them cut it further.
2. For every decomposition, ask: **"Which half would you check FIRST, and why?"** — this forces prioritisation, which is the actual skill.

> 💬 **Expected sticking point:** Groups produce sub-questions that are still vague ("*is the app bad?*"). Don't rescue them — ask *"what number would answer that?"* and let them feel the gap. That feeling is the lesson.

---

## BREAK (5 min)

> *"Before you go: a car dashboard shows you speed, fuel, engine temperature, RPM, and outside temperature. **All five are real numbers about the car.** But only ONE of them ever makes you change what you're doing. Which one — and why does that matter to us? Five minutes."*

---

## Concept Block 3: Metrics vs KPIs — The Dashboard Test (14 min)

### Land the break question first (3 min)

> *"Which one makes you act? **The fuel light.** When it comes on, you change your behaviour — you find a petrol pump. Now: has the outside temperature reading ever once changed how you drive? Never. You've probably never looked at it."*
>
> *"Both are real. Both are measured accurately. Only one of them is a **KPI**. That's the whole distinction, and you already understood it — you just didn't have the words."*

### The definitions (3 min)

> **A METRIC is any number you can measure about the business.**
> **A KPI is a metric that is tied to a goal, has a target, and drives a decision when it moves.**

Put six metrics on the board:

```
Total revenue  ·  Number of orders  ·  Average order value
Delivery time  ·  Return rate       ·  Page views
```

> *"All six are true. All six are useful. A company might track three hundred of these. And that abundance is exactly the problem — which is why KPIs exist."*

### The three tests (4 min) — make them write this down

> ### A metric is only a KPI if it passes **all three**:
>
> | Test | Question | If it fails… |
> |---|---|---|
> | **1. GOAL** | Is it tied to something the business is trying to achieve? | It's trivia |
> | **2. TARGET** | Is there a number we're aiming for? | You can't tell good from bad |
> | **3. ACTION** | If it moves the wrong way, does someone *do* something? | Nobody will ever look at it |

### The demo that makes it click (4 min)

Write these two lines on the board, one above the other:

```
METRIC:  "Average delivery time is 4.2 days."

KPI:     "Average delivery time must stay UNDER 3 DAYS,
          because customers who wait longer than 3 days churn
          at twice the rate.
          We are at 4.2 — we are FAILING, and the logistics
          team owns the fix."
```

> *"Look carefully. **The number is identical.** 4.2 days in both. What changed?"*

Draw it out of them:
- A **target** (under 3 days)
- A **reason** — the goal it serves (churn)
- An **owner** (logistics team)
- A **verdict** (we are failing)

> 🔑 **The line to land:** *"A KPI is a promotion that a metric earns by mattering. **Every KPI is a metric. Most metrics are not KPIs.**"*

> 🔴 **And the warning:** *"If everything is a KPI, nothing is. I have seen 'KPI dashboards' with forty numbers on them. That is not a dashboard — that's a metrics dump, and nobody knows which one to act on. **Five to seven. That's your budget.** Ruthless selection IS the skill."*

---

## Practical Block 3: Promote the Metric to a KPI (10 min)

**Format:** Pairs. 5 minutes work, 5 minutes discussion.

**Put four metrics on screen. Each pair must promote TWO of them into real KPIs.**

```
1.  Number of website visitors
2.  Cart abandonment rate
3.  Number of products in the catalogue
4.  Customer churn rate
```

**The template they must fill — all five fields:**

```
KPI:        ____________________
FORMULA:    ____________________   (exactly how is it computed?)
TIMEFRAME:  ____________________   (over what period?)
TARGET:     ____________________   (what counts as success?)
OWNER:      ____________________   (who acts when it slips?)
```

**Model one on the board first, so they see the standard:**

```
KPI:        Cart abandonment rate
FORMULA:    (carts created − orders completed) ÷ carts created
TIMEFRAME:  Weekly
TARGET:     Below 60%
OWNER:      Product team — if breached, the checkout page is reviewed
```

**The trap to spring — this is the point of the block:**

Ask the room: *"Who promoted **#3, number of products in the catalogue**, to a KPI?"*

Some will have. Then ask:

> *"If that number goes down by ten, what does anyone DO on Monday morning?"*

Let the silence happen.

> *"Nothing. Nobody does anything. It's not tied to a goal, there's no sensible target, and no action follows. **It's a metric — a real, true, correctly-measured metric — and it will never be a KPI.** Recognising that is exactly the skill I'm testing."*

> 💬 **Expect pushback:** *"But you could set a target — 500 products!"* Excellent, engage it: *"You could. But WHY 500? What goal does that serve? If you can't answer that, you've set an arbitrary target, and arbitrary targets are how companies end up optimising numbers that don't matter."*

---

## Concept Block 4: Making a Question Measurable (6 min)

### The recipe (2 min)

```
1. METRIC      What exactly is being measured?
2. FORMULA     How is it computed, precisely?
3. TIMEFRAME   Over what period?
4. TARGET      What counts as success?
```

**Walk the ladder live — from vague to measurable:**

| Stage | The statement |
|---|---|
| 🗣️ **Business question** | *"Are our customers happy?"* |
| ❌ **Still vague** | *"Track customer happiness."* — Happiness is in no database. |
| ⚠️ **A metric** | *"Average star rating."* — Better. But over what period? What's good? |
| ✅ **A KPI** | *"Average star rating (sum ÷ count), measured **monthly**, must stay **at or above 4.2**. Below that, the support lead reviews every 1★ and 2★ review."* |

### The ambiguity trap (3 min) — the part they'll actually use at work

Write on the board: **"Monthly Active Users."**

> *"Sounds precise, doesn't it? Send two analysts to compute it and you will get two different numbers. Why?"*

Draw it out of the room:

- **"Active"** — logged in? Or *placed an order*? Wildly different numbers.
- **"Monthly"** — calendar month, or a rolling 30 days?
- **"User"** — one person with two accounts: one user, or two?

> 📌 **The rule:** *"A KPI whose definition lives only in your head is not a KPI. It's a number you will have to defend in every meeting for the rest of your life. **Write the definition down.** This isn't pedantry — this IS the job."*

### The test (1 min)

> ### ✅ **A KPI is measurable when someone else could compute the exact same number from the same data — without asking you a single question.**

---

## Summary & Bridge (3 min)

**What we covered:**

| Concept | The one thing to remember |
|---|---|
| **The workflow** | problem → data → analysis → insight, and it **loops**. Step 1 is the whole game. |
| **Decomposition** | Cut a vague ask with which/where/when/who/what. **Decompose the metric and the data has fewer places to hide.** |
| **Metric** | Any number you can measure. There are hundreds. |
| **KPI** | A metric with a **goal, a target, and an action**. There should be five to seven. |
| **Measurable** | Metric + formula + timeframe + target — written down, so anyone gets the same number. |

**Close by returning to the hook:**

> *"Ninety minutes ago your manager said 'sales are down, fix it,' and most of this room said 'open the data.' Ask yourselves what you'd say now."*
>
> *"You'd say: 'Down against what baseline? Let me check whether order count fell or average order value fell — that tells us if this is a marketing problem or a pricing problem. I'll come back with a KPI and a target by end of day.'"*
>
> *"**That is the difference between someone who runs numbers and someone who gets promoted.** And notice: you did it without a single tool."*

**Bridge to Session 3:**

> *"Next session: **GenAI for Analytics — Prompt, Check, Improve.** We take the exact workflow from today and put AI to work on it — drafting sub-questions, suggesting KPIs, structuring outputs. And critically, you'll learn to **catch it when it's confidently wrong**, because it will be. The workflow you learned today is what lets you tell the difference. Without it, GenAI is just a very fluent way to produce the wrong answer faster."*

---

## Q&A (2 min)

**Q: How many KPIs should a company actually have?**
→ Five to seven at the top level. Each team then has its own two or three that ladder up. If your dashboard has forty numbers, it's a metrics dump, not a KPI dashboard.

**Q: Can a metric become a KPI later?**
→ Yes, constantly — and that's healthy. During a growth push, "new signups" is a KPI. Once you pivot to retention, it demotes to a metric and "churn rate" gets promoted. **KPIs follow strategy.** If yours never change, your strategy probably isn't either.

**Q: What if my manager won't give me a target?**
→ Then you propose one and make them react. *"I suggest under 3 days — is that right?"* People who can't invent a target from scratch can almost always correct one. **A proposed number beats a blank field, every time.**

**Q: Isn't this all just common sense?**
→ Yes. And it's the most commonly skipped step in the entire profession. Common sense that nobody practises is called a competitive advantage.

---

## Instructor Notes

- **This session has no tools and no code. Do not apologise for that.** Frame it as the session that makes every later tool worth using. If students grumble, tell them: the SQL query they write in Session 9 will be a *waste of time* if the question behind it was never sharpened.
- **The biggest risk is abstraction.** "Workflow" and "KPI" are the kind of words that slide past students without landing. Defeat this by staying concrete: the **manager who says four words and walks away**, the **fuel light**, the **doctor**. Every abstract idea in this session needs a physical object attached to it.
- **The `revenue = orders × value` moment is the highest-value 90 seconds of the session.** Slow down there. Students consistently report this as the thing that changed how they think.
- **Common confusion #1:** *"Metric vs KPI is just semantics."* Kill it with the catalogue-size example in Practical 3 — a metric nobody will ever act on. The silence in the room does the teaching.
- **Common confusion #2:** Students give *findings* ("Chennai is down") instead of *insights* ("cap peak-hour intake at these 5 restaurants"). Every single time, ask: **"What should someone DO on Monday morning?"** Make it your catchphrase for the session.
- **Common confusion #3:** They'll set targets arbitrarily. Always ask *"why that number?"* An arbitrary target is worse than no target — it creates false confidence.
- **Callback to Session 1 in Practical 1** (average vs median delivery time) — it takes ten seconds and it shows students the course is a thread, not a list of topics.
- **No coding question for this session** — it is a conceptual/business session, per course design. The five pre-read exercises are the homework; the decomposition sprint is the in-class assessment.
- **Local context:** Swiggy/Zomato-style delivery, Indian retail chains, and ₹ figures land far better than US e-commerce examples with this cohort.
