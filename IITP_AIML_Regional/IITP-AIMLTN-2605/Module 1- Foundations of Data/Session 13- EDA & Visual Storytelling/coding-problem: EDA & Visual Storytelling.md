# Coding Problem: EDA & Visual Storytelling
> **Session 13 — Module 1: Foundations of Data** | ⏱ 5 mins

---

## Dataset

```python
import pandas as pd
import matplotlib.pyplot as plt

data = {
    "region":  ["North", "South", "North", "East", "West", "South", "East", "North"],
    "product": ["Laptop", "Chair", "Laptop", "Notebook", "Laptop", "Chair", "Notebook", "Laptop"],
    "sales":   [65000, 12000, 58000, 800, 72000, 15000, 900, 61000],
    "profit":  [15000, 4000, 12000, 200, 18000, 5500, 150, 14000]
}
df = pd.DataFrame(data)
```

---

## Tasks

**Task 1 — Basic**
Print `df.describe()` for the `sales` and `profit` columns (round to 0 decimals in your reading).

**Task 2 — Basic**
Create a **bar chart** of **total sales by region**.
Title: `"Total Sales by Region"`, y-axis: `"Sales (₹)"`, bars coloured `steelblue`.

**Task 3 — Mid**
Print the **Pearson correlation** between `sales` and `profit` (round to 2 decimals).
Then print the **region with the highest total profit**.

---

## Expected Output

```
         sales   profit
count      8.0      8.0
mean   35588.0   8606.0
std    31013.0   6998.0
min      800.0    150.0
25%     9225.0   3050.0
50%    36500.0   8750.0
75%    62000.0  14250.0
max    72000.0  18000.0

[bar chart displayed]

Correlation (sales, profit): 0.99
Highest-profit region: North
```

---

<details>
<summary>Solution</summary>

```python
import pandas as pd
import matplotlib.pyplot as plt

data = {
    "region":  ["North", "South", "North", "East", "West", "South", "East", "North"],
    "product": ["Laptop", "Chair", "Laptop", "Notebook", "Laptop", "Chair", "Notebook", "Laptop"],
    "sales":   [65000, 12000, 58000, 800, 72000, 15000, 900, 61000],
    "profit":  [15000, 4000, 12000, 200, 18000, 5500, 150, 14000]
}
df = pd.DataFrame(data)

# Task 1
print(df[["sales", "profit"]].describe().round(0))

# Task 2
region_sales = df.groupby("region")["sales"].sum()
plt.figure(figsize=(7, 4))
plt.bar(region_sales.index, region_sales.values, color="steelblue")
plt.title("Total Sales by Region")
plt.ylabel("Sales (₹)")
plt.tight_layout()
plt.show()

# Task 3
corr = df["sales"].corr(df["profit"])
print(f"Correlation (sales, profit): {corr:.2f}")
top_region = df.groupby("region")["profit"].sum().idxmax()
print(f"Highest-profit region: {top_region}")
```

</details>
