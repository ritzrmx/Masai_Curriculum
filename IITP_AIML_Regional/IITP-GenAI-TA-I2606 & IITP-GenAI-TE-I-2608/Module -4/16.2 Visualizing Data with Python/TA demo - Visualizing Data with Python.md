# TA Live Demo Script — Visualizing Data with Python
> Session 36 | Runtime: ~7 minutes | Delivered at session end, after Balaji's lecture

**Setup before class starts:** A notebook with pandas and matplotlib, and this month's revenue growth by city: Bengaluru 12, Pune 9, Chennai -3. A pre-made Tableau view of the same three numbers open in another tab.

---

```
STEP 1 — Show a bare chart (≈1 min)
  Action: Run plt.bar(["Bengaluru", "Pune", "Chennai"], [12, 9, -3]) then plt.show() with no title or labels. Ask: what is this chart saying?
  Result: Three bars and no context
  Say out loud: "A road sign with no words. Nobody can tell what the numbers are or what they measure."
```

```
STEP 2 — Make it readable (≈2 min)
  Action: Add plt.title("Revenue growth by city, this month"), plt.ylabel("Growth (%)") and a colour, then rerun.
  Result: The same bars, now with a title, a unit and a colour
  Say out loud: "Could a stranger read it without me? Title, axis labels with units, every time. The zero baseline is what shows Chennai going the wrong way."
```

```
STEP 3 — Plot straight from pandas (≈2 min)
  Action: Build df = pd.DataFrame({"city": [...], "growth": [...]}) and run df.plot(kind="bar", x="city", y="growth", legend=False, title="..."). Call plt.savefig("growth.png") before plt.show().
  Result: The same chart from a table, and a saved image file
  Say out loud: "No pulling columns out into lists. Save before you show, or you may save a blank image."
```

```
STEP 4 — Python or Tableau? (≈2 min)
  Action: Switch to the Tableau tab and hover and filter on the same three numbers. Ask the room: a dashboard for managers today, or a chart that refreshes itself every Monday?
  Result: Tableau for the first, Python for the second
  Say out loud: "Neither is better. Interactive and fast: Tableau. Repeatable and automated: Python."
```

---

> **TA TALKING POINT:** "Pick the chart by the question and label it so it can be read without you in the room."
