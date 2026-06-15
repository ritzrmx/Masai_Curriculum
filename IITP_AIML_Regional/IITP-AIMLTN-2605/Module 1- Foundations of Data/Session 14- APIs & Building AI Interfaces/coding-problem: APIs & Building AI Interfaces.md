# Coding Problem: APIs & Building AI Interfaces
> **Session 14 — Module 1: Foundations of Data** | ⏱ 5 mins

---

## Dataset

A simulated API response (no live key required for Tasks 1–2):

```python
import json
import pandas as pd

response_text = """
{
  "city": "Mumbai",
  "temp_celsius": 32,
  "humidity": 78,
  "condition": "Partly Cloudy",
  "forecast": [
    {"day": "Mon", "high": 33, "low": 27},
    {"day": "Tue", "high": 34, "low": 28},
    {"day": "Wed", "high": 32, "low": 26}
  ]
}
"""
```

---

## Tasks

**Task 1 — Basic**
Parse `response_text` with `json.loads()` and print the **city**, **temp_celsius**, and **wind speed** from `wind.speed_kmh` if the nested key existed — otherwise print `humidity` instead.

**Task 2 — Basic**
Convert the `forecast` list into a **Pandas DataFrame** and print it. Then print the **average high temperature** (round to 1 decimal).

**Task 3 — Mid**
Make a GET request to the public API below and print the **country name** and **capital**.

```python
import requests
url = "https://restcountries.com/v3.1/name/india"
```

---

## Expected Output

```
City: Mumbai
Temperature: 32°C
Humidity: 78%

   day  high  low
0  Mon    33   27
1  Tue    34   28
2  Wed    32   26

Average high: 33.0°C

Country: India
Capital: New Delhi
```

---

<details>
<summary>Solution</summary>

```python
import json
import pandas as pd
import requests

response_text = """
{
  "city": "Mumbai",
  "temp_celsius": 32,
  "humidity": 78,
  "condition": "Partly Cloudy",
  "forecast": [
    {"day": "Mon", "high": 33, "low": 27},
    {"day": "Tue", "high": 34, "low": 28},
    {"day": "Wed", "high": 32, "low": 26}
  ]
}
"""

# Task 1
data = json.loads(response_text)
print(f"City: {data['city']}")
print(f"Temperature: {data['temp_celsius']}°C")
if "wind" in data:
    print(f"Wind speed: {data['wind']['speed_kmh']} km/h")
else:
    print(f"Humidity: {data['humidity']}%")

# Task 2
forecast_df = pd.DataFrame(data["forecast"])
print(forecast_df)
avg_high = forecast_df["high"].mean()
print(f"\nAverage high: {avg_high:.1f}°C")

# Task 3
response = requests.get("https://restcountries.com/v3.1/name/india")
country_data = response.json()
print(f"\nCountry: {country_data[0]['name']['common']}")
print(f"Capital: {country_data[0]['capital'][0]}")
```

</details>
