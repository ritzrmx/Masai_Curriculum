# TA Live Demo Script — Breaking Down the Workflow
> Session 28 | Runtime: ~7 minutes | Delivered at session end, after Balaji's lecture

**Setup before class starts:** A whiteboard or shared doc ready to sketch a workflow diagram live, plus a GenAI chat tool open for the "fix it" demo.

---

```
STEP 1 — Replay the failed prompt (≈1 min)
  Action: Type into GenAI: "Our Pune numbers look off, please fix it."
  Result: a generic, hedging response that can't commit to anything useful
  Say out loud: "Watch — it's not refusing, it's guessing. That's the cost of skipping straight to a prompt."
```

```
STEP 2 — Clarify the real question out loud (≈1 min)
  Say out loud: "Let's actually do step one. 'Off' compared to what — last month? Off on revenue, or on delivery ratings? Let's say we mean: Pune's revenue growth has slowed compared to the other three cities."
```

```
STEP 3 — Sketch the full workflow live (≈3 min)
  Action: Draw five boxes on the board: Clarify -> Pull Pune revenue data by month -> Analyse trend vs other cities -> GenAI summarises the finding -> Human decides the action
  Action: Label each box with its tool: Human / SQL-Tableau / Mix / GenAI / Human
  Say out loud: "Five boxes. Five tools. Notice GenAI owns exactly one of them — the summarise step. That's not a weakness, that's an honest map."
```

```
STEP 4 — Run only the one GenAI-suited step (≈2 min)
  Action: Type into GenAI: "Summarise in 3 sentences: Pune's revenue grew 9% this month, slower than Bengaluru's 12%, but still positive and ahead of Chennai's -3%. Focus on whether this is a real concern or normal variation."
  Result: a focused, accurate 3-sentence summary
  Say out loud: "This worked well specifically because I only asked GenAI to do the one step it's actually built for — summarising real numbers I'd already gathered myself."
```

---

> **TA TALKING POINT:** "Before you type a single prompt on a real problem, sketch the boxes first — like I just did on the board. If you can't name a specific tool for every box, the workflow isn't ready yet, and neither is the prompt."
