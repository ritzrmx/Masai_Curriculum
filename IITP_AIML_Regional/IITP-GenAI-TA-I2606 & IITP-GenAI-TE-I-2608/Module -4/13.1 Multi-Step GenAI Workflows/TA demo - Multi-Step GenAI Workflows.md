# TA Live Demo Script — Multi-Step GenAI Workflows
> Session 29 | Runtime: ~7 minutes | Delivered at session end, after Balaji's lecture

**Setup before class starts:** A whiteboard, a GenAI chat tool, the city growth table (Bengaluru 12%, Pune 9%, Chennai -3%), and a short pre-written GenAI report saved in a doc with one planted error: it says Pune trails Bengaluru by 4 points.

---

```
STEP 1 — Draw the three-step chain (≈1 min)
  Action: On the board draw: Calculate growth by city -> GenAI writes the report -> Send to leadership.
  Say out loud: "Three steps. If step one is wrong, steps two and three will make the mistake sound brilliant."
```

```
STEP 2 — Show the report and ask who can spot the problem (≈2 min)
  Action: Put the pre-written report on screen next to the table. Give the room a minute to find the mistake.
  Result: Someone notices 12 minus 9 is 3, not 4
  Say out loud: "It read perfectly well. The error was invisible until someone checked."
```

```
STEP 3 — Add the checkpoints (≈2 min)
  Action: Draw a diamond after Calculate: "recompute 12 minus 9 in the sheet". Draw another after the report: "reviewer prompt". Then type into GenAI: "List every number in this report and say whether it appears in the table below."
  Result: The reviewer flags the 4 as not in the table
  Say out loud: "GenAI can be the editor. But we still recompute one number ourselves, because the editor can be wrong too."
```

```
STEP 4 — Go back one step, not to the start (≈2 min)
  Action: Rerun only the report step with: "Use only the table. State the gap between cities exactly." Recheck the gap.
  Result: The report now says 3 points
  Say out loud: "We didn't redo the whole analysis. Small steps mean small repairs."
```

---

> **TA TALKING POINT:** "Put a checkpoint wherever a new number is created and again before anything leaves your hands. If a check fails, go back one step, not to the start."
