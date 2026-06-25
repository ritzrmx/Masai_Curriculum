# Coding Problem: NumPy - Numerical Foundation
> **Session 9 — Module 1: Foundations of Data** | ⏱ 5 mins

---

## Dataset

Daily temperatures (°C) recorded over 10 days:

```python
import numpy as np

temps = np.array([28, 31, 35, 29, 40, 22, 38, 33, 27, 41])
```

---

## Tasks

**Task 1 — Basic**
Add `3` to every value in `temps` (heat index) and print the result.

**Task 2 — Basic**
Print the first 5 temperatures and the last 3 temperatures using slicing.

**Task 3 — Mid**
Print only temperatures **above 35°C** and how many there are.

---

## Expected Output

```
Heat index: [31 34 38 32 43 25 41 36 30 44]

First 5: [28 31 35 29 40]
Last 3:  [33 27 41]

Above 35°C: [40 38 41]
Count: 3
```

---

<details>
<summary>Solution</summary>

```python
import numpy as np

temps = np.array([28, 31, 35, 29, 40, 22, 38, 33, 27, 41])

print("Heat index:", temps + 3)
print("First 5:", temps[:5])
print("Last 3: ", temps[-3:])
hot = temps[temps > 35]
print("Above 35°C:", hot)
print("Count:", len(hot))
```

</details>
