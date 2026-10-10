# TA Live Demo Script — End-to-End Analytics Workflow
> Session 38 | Runtime: ~7 minutes | Delivered at session end, after Balaji's lecture

**Setup before class starts:** A notebook with the cleaning-and-merge code from 17.1 in a single cell, the raw files ready (the messy orders export and the ad spend sheet), and a GenAI chat tool open.

---

```
STEP 1 — Make the question measurable (≈1 min)
  Action: Write on the board: "Where is ad spend working hardest?" Then rewrite it as: "Units sold per ₹ lakh of ad spend, by city."
  Say out loud: "Vague question in, vague answer out. We decide what we are measuring before we touch the data."
```

```
STEP 2 — Run the pipeline and validate (≈2 min)
  Action: Run the cell and read out the row counts at each step, then the table. Recompute one number by hand.
  Result: Rows 7, 6, 5; Bengaluru 3.0, Pune 2.5, Chennai 1.5 units per lakh; total 20 matches the source; 9 divided by 3 is 3.0
  Say out loud: "It ran. That does not mean it is right. We check the counts and recompute one number."
```

```
STEP 3 — Document it with GenAI (≈2 min)
  Action: Paste the code, the row counts and the decisions into GenAI with: "Document this analysis for a colleague: Purpose, Data sources, Steps, Decisions, Limits, How to rerun. Use ONLY what is in the material below. If something is unclear, list it as a question." Then read the output against the code line by line.
  Result: Clear documentation; any step or check we did not actually do gets struck out
  Say out loud: "GenAI writes this well, but only if we hand it the facts. If it claims a check we never ran, we edit that out."
```

```
STEP 4 — Write the message, answer first (≈2 min)
  Action: Ask GenAI for a four-part manager message (headline, evidence, limits, next step) from the table only, then check it: Bengaluru and Pune turn ad spend into more units than Chennai; 3.0, 2.5 and 1.5; based on five orders and units, not revenue; test moving a small budget from Chennai to Bengaluru for a month.
  Result: A message under 120 words with the answer in the first line
  Say out loud: "If the manager only reads two lines, they must still get the answer. And no 'caused': the limits stay in."
```

---

> **TA TALKING POINT:** "Finish the job: run it end to end, write down what you did, and put the answer in the first line."
