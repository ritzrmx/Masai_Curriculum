# TA Live Demo Script — Python Fundamentals I
> Session 30 | Runtime: ~7 minutes | Delivered at session end, after Balaji's lecture

**Setup before class starts:** A Python notebook (Colab or Jupyter) open with empty cells and the font size turned up.

---

```
STEP 1 — Store values in variables (≈1 min)
  Action: Type and run: city = "Pune" then growth = 9 then print(city, growth).
  Result: Pune 9
  Say out loud: "The equals sign here does not mean 'equals'. It means: store the value on the right into the name on the left."
```

```
STEP 2 — Show the text trap (≈2 min)
  Action: Type growth_text = "9" then print(growth_text + 1). Then run print(int(growth_text) + 1).
  Result: A TypeError first, then 10
  Say out loud: "Read the last line of the error aloud. Python is telling us exactly what is wrong. Numbers that come from files often arrive as text."
```

```
STEP 3 — Let the code decide (≈2 min)
  Action: Type: if growth >= 10: rating = "Strong" / elif growth >= 5: rating = "Healthy" / elif growth >= 0: rating = "Slow" / else: rating = "Declining", then print(city, rating). Mind the colons and indentation.
  Result: Pune Healthy
  Say out loud: "This is the rule we would have applied by eye. Now it is applied the same way every time."
```

```
STEP 4 — Predict before you run (≈2 min)
  Action: Ask the room: what does it print if growth = 12? And if growth = -3? Take answers, then change the value and run.
  Result: Strong, then Declining
  Say out loud: "Predicting first is how you learn. And remember: one equals stores, two equals compares."
```

---

> **TA TALKING POINT:** "A variable stores a value and a condition lets your code decide. Predict the output before you press run: that habit teaches more than copying code ever will."
