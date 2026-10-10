# TA Live Demo Script — Python Fundamentals II
> Session 31 | Runtime: ~7 minutes | Delivered at session end, after Balaji's lecture

**Setup before class starts:** A Python notebook with last session's if / elif / else rating code in one cell for Pune.

---

```
STEP 1 — Show the pain (≈1 min)
  Action: Change growth to 12, rerun, then to -3, rerun. Count out loud.
  Result: Three cities means three edits and three runs
  Say out loud: "Now imagine 300 cities. There has to be a better way."
```

```
STEP 2 — Put the cities in a dictionary (≈2 min)
  Action: Type growth_by_city = {"Bengaluru": 12, "Pune": 9, "Chennai": -3} then print(growth_by_city["Pune"]).
  Result: 9
  Say out loud: "A dictionary is a contacts list: you look up a name and get a value."
```

```
STEP 3 — Loop over it (≈2 min)
  Action: Type: for city in growth_by_city: / growth = growth_by_city[city] / the same if / elif / else / print(city, rating).
  Result: Bengaluru Strong, Pune Healthy, Chennai Declining
  Say out loud: "This is last session's code inside a loop. One run, every city."
```

```
STEP 4 — Add a city and rerun (≈2 min)
  Action: Type growth_by_city["Test City"] = 5 and run the loop again. Then deliberately type growth_by_city["pune"] to show the KeyError.
  Result: Test City Healthy appears with no other change; lowercase pune gives a KeyError
  Say out loud: "We added data and changed no logic. And keys are case sensitive: pune is not Pune."
```

---

> **TA TALKING POINT:** "If you are about to copy and paste the same lines a third time, you need a loop. And always ask what makes it stop."
