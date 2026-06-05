# Coding Problem: Data Visualization & APIs
> **Session 14 — Module 1: Foundations of Data** | ⏱ 5 mins

---

## Dataset

```python
import matplotlib.pyplot as plt
import requests

months  = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
revenue = [42000, 55000, 48000, 71000, 65000, 83000]
```

---

## Tasks

**Task 1 — Basic**
Create a **bar chart** of `revenue` by `months`.
Add title `"Monthly Revenue — H1 2025"`, label the y-axis `"Revenue (₹)"`, and colour the bars `steelblue`.

**Task 2 — Basic**
On the same or a new chart, add a **horizontal dashed red line** at the average revenue. Label it `"Avg"`.

**Task 3 — Mid**
Make a GET request to the public API below and print the **name** and **capital** of the returned country.

```python
url = "https://restcountries.com/v3.1/name/india"
response = requests.get(url)
data = response.json()
# data is a list — the first item has 'name' and 'capital' keys
```

---

## Expected Output

```
[bar chart with average line displayed]

Country: India
Capital: New Delhi
```

---

<details>
<summary>Solution</summary>

```python
import matplotlib.pyplot as plt
import requests

months  = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
revenue = [42000, 55000, 48000, 71000, 65000, 83000]

# Task 1 & 2 — Bar chart with average line
avg = sum(revenue) / len(revenue)

plt.figure(figsize=(8, 4))
plt.bar(months, revenue, color="steelblue")
plt.axhline(avg, color="red", linestyle="--", label=f"Avg: ₹{avg:,.0f}")
plt.title("Monthly Revenue — H1 2025")
plt.ylabel("Revenue (₹)")
plt.legend()
plt.tight_layout()
plt.show()

# Task 3 — API call
response = requests.get("https://restcountries.com/v3.1/name/india")
data = response.json()
print("Country:", data[0]["name"]["common"])
print("Capital:", data[0]["capital"][0])
```

</details>
