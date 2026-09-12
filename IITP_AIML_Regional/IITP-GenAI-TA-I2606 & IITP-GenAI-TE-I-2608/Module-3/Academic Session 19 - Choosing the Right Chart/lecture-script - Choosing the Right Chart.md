# Lecture Script: Tableau — Choosing the Right Chart
> **Instructor Reference** — Module 3: Tableau Dashboards + Storytelling | Academic Session 19 | Duration: 2 Hours | Instructor: Balaji

---

## Session Overview
**Goal:** Students can look at a real business question and select the chart type that answers it clearly, then format that chart for fast readability using sorting, labels, and purposeful colour.

**Student profile at this point:** They can build a bar chart and a line chart, and they just spent a stats session learning to state probabilities honestly. Expect overreliance on bar charts as a "safe default" for everything, and a habit — likely carried over from Excel — of reaching for pie charts whenever "parts of a whole" comes up. Boredom risk is low here since this session is visually rich, but there's a risk of students treating chart choice as purely aesthetic rather than a judgement call tied to the question being asked.

**Key outcome:** Students should leave with the habit of writing down their question in one sentence before opening Tableau, and letting that sentence dictate the chart type.

> 🎯 **The one sentence this session must land:** *The chart type follows from the question you're asking — not from which chart you happen to know best.*

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| Opening Hook | 8 min | 8 min |
| Concept + Practical Block 1: Beyond Bar and Line | 25 min | 33 min |
| Concept + Practical Block 2: Matching Chart to Question | 20 min | 53 min |
| **BREAK** | 10 min | 63 min |
| Concept + Practical Block 3: Comparing Chart Types on the Same Data | 25 min | 88 min |
| Concept + Practical Block 4: Making Charts Readable | 22 min | 110 min |
| Summary & Bridge | 5 min | 115 min |
| Q&A & Doubt Solving | 5 min | 120 min |

---

## Opening — "The Pie Chart Crime Scene" (8 min)

Project a genuinely unreadable pie chart — 9 thin slices of Kirana365's product categories, several barely distinguishable in colour, no labels.

> "Quick — without squinting — which category is Kirana365's third-biggest? You have five seconds."

Let them struggle audibly.

> "Nobody got it. Not because you're bad at reading charts — because this chart was the wrong tool for this job from the start."

Switch to the same data as a sorted, labelled bar chart. The third-biggest category is instantly obvious.

> "Same data. Same nine categories. One chart works, one doesn't. That's today's entire session in one comparison."

**Pivot line:** "Last session you learned two chart types — bar and line. Today you learn that Tableau gives you a whole toolbox, and picking the wrong tool from that box actively hides your insight instead of revealing it."

**Context for the sessions ahead:** "Every dashboard for the rest of this module is built from charts you choose today. Choose badly here, and every future dashboard inherits that weakness."

---

## Concept Block 1: Beyond Bar and Line (13 min)

> "Think of chart types like kitchen tools. Bar charts are your knife — you reach for it constantly. But sometimes you need a ladle, not a knife."

Introduce stacked bar, scatter plot, treemap, and highlight table on the board with one-line jobs each, then live-build a stacked bar of Revenue by City, coloured by Category, on the Kirana365 data.

> "Watch — this single chart now answers two questions at once: which city is biggest, AND what's driving that city's number."

### 🔴 The trap / highest-value moment
> "The trap: reaching for a pie chart 'because it's the classic parts-of-a-whole chart.' Write this down: **past 4-5 slices, a pie chart becomes unreadable. Real business data almost always has more categories than that — use a stacked bar or treemap instead.**"

## Practical Block 1: Rebuild the Crime Scene (12 min)

Give students the same 9-category product data from the opening. Task: rebuild it as a stacked bar chart (by City, coloured by Category) instead of a pie chart, and identify the third-biggest category correctly this time.

**Answer key with reasoning:** Once rebuilt as a sorted, coloured stacked or simple bar, the third-biggest category becomes visible within seconds — proving the earlier failure was the chart type, not the data or the reader.

💬 **Expect a question about when pie charts are ever acceptable.** Welcome it. Say: "With 2-3 slices, rarely more, a pie chart can work — think 'percentage of orders that were on-time vs late.' The moment you're tempted to add a fourth or fifth slice, switch tools."

---

## Concept Block 2: Matching Chart to Question (10 min)

> "Before you open Tableau at all, write your question in one plain sentence. The chart type falls out of that sentence — it shouldn't be a separate decision."

Walk the decision table on the board: "which is bigger" → bar; "how did it change" → line; "what's it made of" → stacked bar/treemap; "is there a relationship" → scatter; "where are the patterns across many rows" → highlight table.

> "Today's example: 'Is there a relationship between how many items a customer orders and how much they spend?' That's two numbers, and a relationship question — that phrase alone tells you it's a scatter plot, before you've touched Tableau."

### 🔴 The trap / highest-value moment
> "The highest-value habit in this entire session: picking the chart type BEFORE opening Tableau, from the question, not from familiarity. Bar charts feel 'safe' — that safety is exactly what leads to weak, generic dashboards."

## Practical Block 2: Question to Chart Type (10 min)

Give five one-sentence business questions and ask students to name the chart type for each, with a reason:
1. "Which delivery partner has the most late deliveries?"
2. "How has Kirana365's daily order volume changed since June?"
3. "Do customers who order more items also spend proportionally more?"
4. "What does Chennai's revenue breakdown by category look like?"

**Answer key with reasoning:** 1-Bar (comparing categories); 2-Line (time sequence); 3-Scatter (relationship between two numbers); 4-Stacked bar or treemap (part-to-whole within one city).

💬 **Expect an argument that question 3 "could just be a bar chart of average spend per quantity bucket."** Welcome it. Say: "That's a valid alternative — but it hides individual orders and can flatten out real variation. A scatter plot shows every single order, which is often more honest for a relationship question."

---

## BREAK (10 min)

---

## Concept Block 3: Comparing Chart Types on the Same Data (13 min)

> "Same data, different chart, different story. This is why good analysts sketch two or three chart options before committing to one."

Live-build three views of the same August data: plain bar (City totals), stacked bar (City + Category), and a scatter (Quantity vs Revenue per order). Narrate what each one reveals that the others hide.

> "The bar chart tells you Bengaluru wins. The stacked bar tells you Bengaluru wins *because of Snacks*, while Chennai's smaller total is almost entirely Groceries. The scatter tells you a handful of huge bulk orders are quietly pulling the whole average up. Three charts, three different true stories, same underlying rows."

### 🔴 The trap / highest-value moment
> "The trap: assuming there's always one single correct chart. Often two or three are all valid — the real skill is picking the one that best matches what you're about to say next in your presentation."

## Practical Block 3: Three Views, Three Insights (12 min)

Students build all three chart types (bar, stacked bar, scatter) on the Kirana365 data themselves and write one sentence per chart describing what unique insight it reveals that the others don't.

**Answer key with reasoning:** Expect answers similar to the instructor's narration above — the key grading criterion is that each of the three sentences names something genuinely different, proving the student understands each chart type serves a distinct purpose rather than being interchangeable.

💬 **Expect pushback**: "Isn't this a lot of extra work — building three charts to answer one question?" Welcome it. Say: "In practice you'll often sketch mentally, not fully build, all three — but doing it fully once, today, is exactly how that instinct gets built."

---

## Concept Block 4: Making Charts Readable (12 min)

> "An unlabelled, unsorted chart is a shop shelf with no price tags, items in random order. All the information is technically there — the customer just has to work far too hard for it."

Live demonstrate: take the plain City bar chart, sort it high-to-low, add data labels on each bar, and colour only the lowest bar red to flag underperformance.

> "Same chart type, same data — but now readable in under three seconds instead of ten to fifteen."

### 🔴 The trap / highest-value moment
> "The opposite trap is just as real: over-formatting. Labels on every single bar, five decorative colours with no meaning, 3D effects. That creates just as much visual noise as no formatting at all. Format only what helps the one point you're making."

## Practical Block 4: Format for Speed (10 min)

Give students an unsorted, unlabelled, default-coloured bar chart and ask them to apply exactly three fixes: sort by value, label the top and bottom bar only, and colour the lowest bar to flag it — nothing more.

**Answer key with reasoning:** The finished chart should be readable in under 3 seconds by a classmate who hasn't seen the data before — this is the actual test of success, not a checklist of features applied.

💬 **Expect a question about "why only label the top and bottom bar, not all of them?"** Welcome it. Say: "Because labelling everything defeats the purpose — the whole point of a chart over a table is that most values don't need to be read exactly. Label only what the story requires."

---

## Summary & Bridge (5 min)

| Concept | The one thing to remember |
|---|---|
| Beyond bar and line | Different chart types answer different kinds of questions — pick by purpose, not habit |
| Matching chart to question | Write your question in one sentence before opening Tableau |
| Comparing chart types | The same data can tell different true stories depending on the chart chosen |
| Readability | Sort, label sparingly, and use colour only with a purpose |

Close on the thesis: "The chart type follows from the question you're asking — not from which chart you happen to know best. Every chart in your future dashboards should be able to answer 'what question is this answering?' in one sentence."

**Bridge to Session 20:** "Next session we take these well-chosen, well-formatted charts and combine several of them, for the first time, into a single connected dashboard — Building a Dashboard."

---

## Q&A & Doubt Solving (5 min)

**Q: Is there ever a wrong chart type for a given dataset, or just weaker choices?**
→ Usually it's about weaker vs stronger choices, but some are genuinely wrong — like a line chart connecting non-sequential categories, which implies a trend that doesn't exist.

**Q: How many chart types does Tableau actually offer?**
→ Many more than the five-plus-bar-and-line covered today — but these cover roughly 80% of real business questions; the rest you'll pick up as specific needs arise.

**Q: Can I combine two chart types, like bars and a line, on the same chart?**
→ Yes — a "dual axis" chart does exactly this, and it's a common technique we'll touch on again once we start building full dashboards.

**Q: What if my question could genuinely be answered by two different chart types equally well?**
→ Then pick based on your audience — a quick glance for a busy store manager might favour a bar chart, while a detailed relationship story for an analyst peer might favour a scatter plot.

**Q: Should I always sort my bar charts, no exceptions?**
→ Almost always yes for comparison charts — the only common exception is when the order itself is meaningful, like days of the week in their natural sequence.

---

## Instructor Notes
- **Words not yet earned:** "dual axis," "dashboard actions," "parameters" — these belong to later sessions; keep today's vocabulary to chart type names and formatting terms only.
- **Biggest risk in this session:** Students treating chart selection as a purely aesthetic choice rather than a judgement tied to a specific question — counter this by insisting every practical exercise starts with writing the one-sentence question first.
- **Board management:** Keep the "question → chart type" decision table visible for the entire session; also keep the thesis line up throughout.
- **Common confusions:**
  1. Defaulting to pie charts for anything "parts of a whole," regardless of slice count.
  2. Treating bar charts as a universal safe choice for every kind of question.
  3. Over-formatting a chart until the extra decoration becomes its own source of confusion.
- **Cross-references:** This session's chart choices become the literal building blocks of Session 20 (Building a Dashboard), and the "audience matters" idea returns fully in Session 23 (Dashboards That Support Decisions).
- **Local/cultural context notes:** The kitchen-tools and shop-shelf analogies land well with this cohort; keep using Kirana365's real city and category data so every chart-type decision is grounded in a business the students already know, not an abstract example.
