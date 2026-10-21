# TA Live Demo Script — Summarise, Compare and Report with GenAI
> Session 27 | Runtime: ~7 minutes | Delivered at session end, after Balaji's lecture

**Setup before class starts:** A GenAI chat tool open, and this month's Kirana365 revenue growth by city saved in a note ready to paste: Bengaluru +12%, Pune +9%, Chennai -3%.

---

```
STEP 1 — Run the weak prompt (≈1 min)
  Action: Paste the table and type: "Summarise this data."
  Result: A generic paragraph that repeats the three numbers and makes no point
  Say out loud: "It is not wrong. It is just not useful. That is what a one-line brief gets you."
```

```
STEP 2 — Rewrite it with four parts (≈2 min)
  Action: Type: "You are a business analyst. Below is this month's revenue growth by city. Compare the three cities in three bullets under 20 words each, and say which city needs attention. Use only this data."
  Result: Three sharp bullets that single out Chennai
  Say out loud: "Same data, same tool. Only the brief changed: role, task, data, format."
```

```
STEP 3 — Check one number (≈2 min)
  Action: Pick one claim from the output, for example the gap between Bengaluru and Pune, and check it against the table: 12 minus 9 is 3 points. Scan for any word like 'caused'.
  Result: The gap matches; no causal claim
  Say out loud: "It reads smoothly. Smooth does not mean verified. One number checked is the minimum before it leaves your hands."
```

```
STEP 4 — Refine with one instruction (≈2 min)
  Action: Add: "Return a table with columns City, Growth, Gap to best city, then one recommended next step. Use only the data given."
  Result: A table: Bengaluru 12 and gap 0, Pune 9 and gap 3, Chennai -3 and gap 15, then one next step
  Say out loud: "One instruction changed and the output became a reusable shape for next month's report."
```

---

> **TA TALKING POINT:** "Treat the first answer as a draft: say what is missing, add one instruction, and check one number before it goes anywhere."
