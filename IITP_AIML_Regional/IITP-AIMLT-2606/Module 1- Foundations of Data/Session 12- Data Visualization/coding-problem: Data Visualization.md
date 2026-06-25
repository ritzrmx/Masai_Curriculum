# Coding Problem: Data Visualization
> **Session 12 — Module 1: Foundations of Data** | ⏱ 5 mins

---

## Dataset

```python
import matplotlib.pyplot as plt

days = ["Mon", "Tue", "Wed", "Thu", "Fri"]
visits = [120, 135, 128, 150, 142]
```

---

## Tasks

**Task 1 — Basic**

Create a bar chart of visits by day with title "Daily Visits".

**Task 2 — Basic**

On same data, print max visits and which day (no plot).

**Task 3 — Mid**

Add `plt.ylabel("Visits")` and save figure as `visits.png` (use `plt.savefig` before show/close).

---

## Expected Output

```
150 Thu
Saved visits.png
```

*(Plus bar chart displayed or saved.)*

---

<details>
<summary>Solution</summary>

```python
import matplotlib.pyplot as plt

days = ["Mon", "Tue", "Wed", "Thu", "Fri"]
visits = [120, 135, 128, 150, 142]

plt.bar(days, visits)
plt.title("Daily Visits")
plt.ylabel("Visits")
plt.savefig("visits.png")
plt.close()

print(max(visits), days[visits.index(max(visits))])
print("Saved visits.png")
```
</details>
