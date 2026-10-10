# TA Live Demo Script — Python Fundamentals III
> Session 32 | Runtime: ~7 minutes | Delivered at session end, after Balaji's lecture

**Setup before class starts:** A Python notebook with a file cities.csv in the same folder containing three lines after the header: city,growth then Bengaluru,12 then Pune,9 then Chennai,-3.

---

```
STEP 1 — Write a function (≈1 min)
  Action: Type def rate_city(growth): with the if / elif / else returning "Strong", "Healthy", "Slow" or "Declining", then call print(rate_city(9)).
  Result: Healthy
  Say out loud: "It is a recipe card: write the steps once, fill in the blanks each time. And defining it does nothing until you call it."
```

```
STEP 2 — Read the file (≈2 min)
  Action: Type with open("cities.csv", "r") as f: lines = f.read().strip().split("\n") then print(lines).
  Result: A list of text lines including the header
  Say out loud: "Everything that comes out of a file is text, including the numbers."
```

```
STEP 3 — Loop, convert, call (≈2 min)
  Action: Type for line in lines[1:]: city, growth = line.split(",") then print(city, rate_city(int(growth))). First run it without int() to show the error.
  Result: A TypeError comparing str and int, then Bengaluru Strong, Pune Healthy, Chennai Declining
  Say out loud: "lines[1:] skips the header. int() turns the text into a number. Read the error's last line every time."
```

```
STEP 4 — Write the results out (≈2 min)
  Action: Open ratings.txt with mode "w" and write one line per city inside the loop. Open the file to show it. Run the cell again to show it is overwritten.
  Result: A file ratings.txt with one rating line per city
  Say out loud: "Read, process, write. And write mode wipes what was there, so keep your original data safe."
```

---

> **TA TALKING POINT:** "Read, process, write. If you can say those three words about your task, you can script it, and a function is how you keep the middle step reusable."
