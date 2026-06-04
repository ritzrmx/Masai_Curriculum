# Lecture Script: APIs & Building AI Interfaces
> **Instructor Reference** — Module 1: Foundations of Data | Session 14 | Duration: 2 Hours

---

## Session Overview

**Goal:** Students can make authenticated API calls, parse JSON responses into Pandas DataFrames, handle errors, and build a minimal Gradio demo that calls a live API and shows the result — bridging data analysis with AI application building.

**Student profile at this point:** Have completed all data analysis tools (Pandas, SQL, EDA). This is the session that pivots from "analysing data" to "building things with data and AI."

**Key outcome:** Students build a working Gradio app that accepts a user question, calls the OpenAI API (or a mock), and displays the response — demonstrating the foundation of every AI product they will build in Modules 2 and 3.

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| Opening — What Is an API and Why Do We Need It? | 5 min | 0:05 |
| **Concept 1:** HTTP, JSON, and the Request-Response Model | 10 min | 0:15 |
| **Practical 1:** Call a live public API, parse JSON → DataFrame | 15 min | 0:30 |
| **Concept 2:** Authentication — API Keys and Headers | 10 min | 0:40 |
| **Practical 2:** Call the OpenAI API (or a weather API) with auth | 15 min | 0:55 |
| **BREAK** | 10 min | 1:05 |
| **Concept 3:** Error Handling and Rate Limits | 10 min | 1:15 |
| **Practical 3:** Robust API calls with retry logic | 15 min | 1:30 |
| **Concept 4:** Building an AI Interface with Gradio | 10 min | 1:40 |
| **Practical 4:** Build and demo the Gradio app | 10 min | 1:50 |
| Summary & Wrap-Up | 5 min | 1:55 |
| Q&A & Doubt Solving | 5 min | 2:00 |

---

## Opening (5 min)

**Hook:** Show students the Spotify home page → *"How does this page know what songs you like? How does WhatsApp deliver your message in < 1 second across the world? How does a weather widget know the temperature in your city right now?"*

The answer is all the same: **API calls**. Every modern application is a network of APIs exchanging structured data.

**Closer to home:** *"How does ChatGPT work when you embed it in a website? Your application calls the OpenAI API, sends your message as JSON, and receives the response as JSON. That is all. No magic — just HTTP requests. By the end of today, you will have built that yourself."*

---

## Concept Block 1: HTTP, JSON, and the Request-Response Model (10 min)

### The Request-Response Model

```
Your Python code             Server
     │                          │
     │── HTTP Request ─────────►│
     │   (GET /weather?city=Mumbai)
     │                          │ (server looks up Mumbai weather)
     │◄── HTTP Response ────────│
         (200 OK, JSON body)
```

**Key HTTP concepts:**

| Concept | Meaning | Example |
|---|---|---|
| URL / Endpoint | The address of the resource | `https://api.openweathermap.org/data/2.5/weather` |
| Method | What to do | `GET` (read), `POST` (send data), `DELETE` |
| Status code | Did it work? | `200` OK, `401` Unauthorised, `429` Rate limited, `500` Server error |
| Headers | Metadata about the request | `Authorization: Bearer <api_key>` |
| Body | Data sent (POST) or received (GET) | JSON string |

### JSON — The Universal Data Format

JSON = JavaScript Object Notation — the lingua franca of APIs. It maps directly to Python dicts and lists.

```python
# JSON from a weather API (raw string)
response_text = '''
{
  "city": "Mumbai",
  "temp_celsius": 32,
  "humidity": 78,
  "condition": "Partly Cloudy",
  "wind": {"speed_kmh": 18, "direction": "SW"}
}
'''

import json
data = json.loads(response_text)
print(data['city'])           # "Mumbai"
print(data['wind']['speed_kmh'])  # 18 — nested access
```

**DataFrame from JSON array:**
```python
# Many API responses return a list of objects
records = [
    {"city": "Mumbai", "temp": 32},
    {"city": "Delhi", "temp": 38},
    {"city": "Bangalore", "temp": 26}
]
import pandas as pd
df = pd.DataFrame(records)
print(df)
```

---

## Practical Block 1: Call a Live Public API (15 min)

### Use a Public API — No Key Required

Use the **Open-Meteo** weather API (completely free, no authentication):

```python
import requests
import pandas as pd

# Open-Meteo — free weather API, no key needed
# Mumbai: lat=19.076, lon=72.877
lat, lon = 19.076, 72.877
url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": lat,
    "longitude": lon,
    "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
    "timezone": "Asia/Kolkata",
    "forecast_days": 7
}

response = requests.get(url, params=params)
print("Status code:", response.status_code)
print("Response type:", type(response.json()))
```

```python
# Parse the response
data = response.json()
print("Top-level keys:", list(data.keys()))

# Extract daily forecast into DataFrame
daily = data['daily']
df_weather = pd.DataFrame({
    'date': daily['time'],
    'max_temp_c': daily['temperature_2m_max'],
    'min_temp_c': daily['temperature_2m_min'],
    'precipitation_mm': daily['precipitation_sum']
})

df_weather['date'] = pd.to_datetime(df_weather['date'])
print("\n7-day forecast for Mumbai:")
print(df_weather)

# Visualise
import matplotlib.pyplot as plt
plt.figure(figsize=(9, 4))
plt.plot(df_weather['date'], df_weather['max_temp_c'], 'o-r', label='Max Temp')
plt.plot(df_weather['date'], df_weather['min_temp_c'], 'o-b', label='Min Temp')
plt.fill_between(df_weather['date'],
                 df_weather['min_temp_c'],
                 df_weather['max_temp_c'],
                 alpha=0.2, color='orange')
plt.xlabel('Date')
plt.ylabel('Temperature (°C)')
plt.title('Mumbai 7-Day Temperature Forecast')
plt.xticks(rotation=30)
plt.legend()
plt.tight_layout()
plt.show()
```

**Walk through each step:** URL construction, `params` dictionary, status check, JSON parsing, DataFrame creation. Ask: *"What would happen if we changed the city to Delhi? What two parameters change?"*

---

## Concept Block 2: Authentication — API Keys and Headers (10 min)

### Why APIs Require Authentication

Most useful APIs are paid or rate-limited. Authentication:
1. Identifies who is making the call (billing)
2. Limits usage to prevent abuse (rate limits)
3. Restricts access to data that is not public

### API Key Storage Rules

**Rule 1: Never hardcode API keys in your code.**

```python
# WRONG — this key will be in your git history forever
api_key = "sk-1234abc..."   

# RIGHT — load from environment variable
import os
api_key = os.environ.get("OPENAI_API_KEY")

# Or from .env file using python-dotenv
from dotenv import load_dotenv
load_dotenv()
api_key = os.environ["OPENAI_API_KEY"]
```

**Rule 2: Add `.env` to `.gitignore` immediately after creating it.**

### How Keys Are Passed to APIs

| Method | Code pattern | Used by |
|---|---|---|
| Header | `headers={"Authorization": f"Bearer {key}"}` | OpenAI, most REST APIs |
| Query param | `params={"api_key": key}` | Older APIs |
| SDK (handles it) | `OpenAI(api_key=key)` | OpenAI SDK, most modern |

### OpenAI API Structure

```python
from openai import OpenAI
import os

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful data analyst."},
        {"role": "user",   "content": "In one sentence, what is a DataFrame?"}
    ],
    temperature=0.7,
    max_tokens=100
)

reply = response.choices[0].message.content
print(reply)
```

---

## Practical Block 2: Call an API with Authentication (15 min)

### Option A — If students have OpenAI keys

```python
from openai import OpenAI
import os

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "YOUR_KEY_HERE"))

def ask_analyst(question, data_context=""):
    """Ask a data analysis question with optional context."""
    messages = [
        {
            "role": "system",
            "content": (
                "You are a data analyst assistant. "
                "Provide concise, accurate answers to data-related questions. "
                "If given data context, use it in your answer."
            )
        }
    ]
    if data_context:
        messages.append({
            "role": "user",
            "content": f"Data context:\n{data_context}\n\nQuestion: {question}"
        })
    else:
        messages.append({"role": "user", "content": question})

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.5,
        max_tokens=200
    )
    return response.choices[0].message.content

# Test it
print(ask_analyst("What is the difference between mean and median?"))

# With data context
sample_data = "Sales: [5000, 8000, 6000, 55000, 7000]. One outlier present."
print(ask_analyst("Should I report the mean or median for this sales data?", sample_data))
```

### Option B — Mock API (if no keys available)

```python
# Mock that mimics the OpenAI structure for demo purposes
def ask_analyst_mock(question, data_context=""):
    """Mock API response for demo purposes."""
    responses = {
        "mean": "Mean is the arithmetic average; median is the middle value. Use median when data has outliers.",
        "outlier": "With an outlier (55,000 vs others ~6,500), report the median (7,000) as the typical value.",
    }
    for key, response in responses.items():
        if key in question.lower() or key in data_context.lower():
            return response
    return "Great question! In data analysis, always verify your assumptions with the data."

print(ask_analyst_mock("mean vs median"))
```

---

## BREAK (10 min)

*Ask students to think about what "user interface" they would build around the weather API or the analyst function. They will implement one after the break.*

---

## Concept Block 3: Error Handling and Rate Limits (10 min)

### What Can Go Wrong with API Calls

| Error | HTTP Status | Cause | What to do |
|---|---|---|---|
| Unauthorised | 401 | Wrong or expired API key | Check the key; re-generate |
| Not found | 404 | Wrong endpoint URL | Check documentation |
| Rate limited | 429 | Too many requests | Wait and retry with backoff |
| Server error | 500 | API is broken | Retry; contact support |
| Timeout | (ConnectionError) | Network or server slow | Retry with timeout parameter |

### The Right Way to Call an API

```python
import requests
import time

def safe_api_call(url, params=None, headers=None, retries=3):
    """Call an API with retry logic and error handling."""
    for attempt in range(retries):
        try:
            response = requests.get(url, params=params, headers=headers, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 429:
                wait = 2 ** attempt  # 1, 2, 4 seconds
                print(f"Rate limited. Waiting {wait}s before retry {attempt+1}...")
                time.sleep(wait)
            elif response.status_code == 401:
                print("Authentication failed. Check your API key.")
                return None
            else:
                print(f"HTTP {response.status_code}: {response.text[:200]}")
                return None
        except requests.exceptions.Timeout:
            print(f"Timeout on attempt {attempt+1}")
            time.sleep(2 ** attempt)
        except requests.exceptions.ConnectionError:
            print(f"Connection error on attempt {attempt+1}")
            time.sleep(2)
    
    print(f"Failed after {retries} attempts.")
    return None
```

**Key teaching points:**
- Always set a `timeout` — never let a hanging request block your program forever
- Exponential backoff (2^n seconds) is the standard approach for rate limits
- Log meaningful errors — `print(f"HTTP {response.status_code}")` helps debugging enormously

---

## Practical Block 3: Robust API Calls with Retry Logic (15 min)

```python
# Demonstrate error handling with the weather API
# Good call
result = safe_api_call(
    "https://api.open-meteo.com/v1/forecast",
    params={"latitude": 19.076, "longitude": 72.877,
            "daily": "temperature_2m_max", "forecast_days": 3,
            "timezone": "Asia/Kolkata"}
)
if result:
    print("Success! Max temps:", result['daily']['temperature_2m_max'])

# Bad call (wrong endpoint)
result_bad = safe_api_call("https://api.open-meteo.com/v1/WRONG_ENDPOINT",
                            params={"latitude": 19.076, "longitude": 72.877})
print("Bad call result:", result_bad)

# Timeout simulation
result_timeout = safe_api_call("https://httpbin.org/delay/15",  # 15s delay server
                                retries=2)
print("Timeout result:", result_timeout)
```

**Live demo value:** Students see the retry logic actually run when you hit the timeout test. The print statements show exactly what's happening.

---

## Concept Block 4: Building an AI Interface with Gradio (10 min)

### What Is Gradio?

Gradio is a Python library that creates instant web UIs for Python functions — no HTML or JavaScript needed. Used extensively in the ML/AI community for demos (many Hugging Face models have Gradio interfaces).

```python
# pip install gradio
import gradio as gr

# Any Python function → Gradio demo
def greet(name):
    return f"Hello, {name}!"

demo = gr.Interface(fn=greet, inputs="text", outputs="text")
demo.launch()
```

### Gradio Component Types

| Input component | When to use |
|---|---|
| `gr.Textbox()` | Free text entry |
| `gr.Slider()` | Numeric range (temperature, limits) |
| `gr.Dropdown()` | Choose from a fixed list |
| `gr.File()` | Upload a CSV |

| Output component | When to use |
|---|---|
| `gr.Textbox()` | Text response |
| `gr.Dataframe()` | Show a table |
| `gr.Plot()` | Matplotlib/Plotly figure |

---

## Practical Block 4: Build the Gradio App (10 min)

**Goal:** A Gradio demo that takes a city name, calls the weather API, and shows a 7-day forecast table + chart.

```python
import gradio as gr
import requests
import pandas as pd
import matplotlib.pyplot as plt

CITY_COORDS = {
    "Mumbai":    (19.076, 72.877),
    "Delhi":     (28.704, 77.102),
    "Bangalore": (12.972, 77.594),
    "Chennai":   (13.083, 80.270),
    "Kolkata":   (22.573, 88.364)
}

def get_forecast(city):
    """Fetch 7-day weather forecast and return table + chart."""
    if city not in CITY_COORDS:
        return f"City '{city}' not found. Try: {', '.join(CITY_COORDS.keys())}", None
    
    lat, lon = CITY_COORDS[city]
    result = safe_api_call(
        "https://api.open-meteo.com/v1/forecast",
        params={"latitude": lat, "longitude": lon,
                "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
                "timezone": "Asia/Kolkata", "forecast_days": 7}
    )
    
    if not result:
        return "Failed to fetch weather data.", None
    
    daily = result['daily']
    df = pd.DataFrame({
        'Date': daily['time'],
        'Max Temp (°C)': daily['temperature_2m_max'],
        'Min Temp (°C)': daily['temperature_2m_min'],
        'Rain (mm)':     daily['precipitation_sum']
    })
    
    # Build chart
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(df['Date'], df['Max Temp (°C)'], 'o-r', label='Max', lw=2)
    ax.plot(df['Date'], df['Min Temp (°C)'], 'o-b', label='Min', lw=2)
    ax.fill_between(df['Date'], df['Min Temp (°C)'], df['Max Temp (°C)'],
                    alpha=0.15, color='orange')
    ax.set_title(f'{city} — 7-Day Forecast')
    ax.set_ylabel('Temperature (°C)')
    plt.xticks(rotation=30, fontsize=8)
    plt.legend()
    plt.tight_layout()
    
    return df, fig

# Launch Gradio
demo = gr.Interface(
    fn=get_forecast,
    inputs=gr.Dropdown(choices=list(CITY_COORDS.keys()), label="Select City"),
    outputs=[
        gr.Dataframe(label="7-Day Forecast"),
        gr.Plot(label="Temperature Chart")
    ],
    title="Indian City Weather Forecast",
    description="Powered by Open-Meteo (free, no key required)"
)

demo.launch(share=False)
# Navigate to: http://127.0.0.1:7860
```

**Let students interact with the running app.** Have 2–3 students call it with different cities. This is the most engaging moment of the session.

**Extension (if there is time):** Add a second tab that lets students type a free-text question and calls the LLM analyst function.

---

## Summary & Wrap-Up (5 min)

**What we built today:**
- Called a live REST API and parsed JSON → DataFrame → chart
- Applied API key security (environment variables, never in code)
- Built robust error handling with retry and exponential backoff
- Created a working Gradio app — a real user interface with no HTML

**The bridge to GenAI:** *"Everything you've seen today is what every LLM API call looks like under the hood. When you call the OpenAI API in Module 3, you're doing exactly what we did today — a POST request with a JSON body, an API key in the header, and JSON in the response. You already know how it works."*

**Homework:** Using the `safe_api_call` function, call the [exchangerate.host](https://exchangerate.host) API to get today's INR → USD → EUR rates and display them in a DataFrame. Add a Gradio interface with a currency dropdown.

---

## Q&A & Doubt Solving (5 min)

**Q: What's the difference between GET and POST?**
→ GET retrieves data, parameters are in the URL. POST sends data (in the body) and creates or processes something. OpenAI's chat endpoint is POST because you're sending your messages as a JSON body.

**Q: Can I use `requests` for the OpenAI API directly instead of the SDK?**
→ Yes — the SDK is a convenience wrapper around `requests`. At its core: `requests.post("https://api.openai.com/v1/chat/completions", headers={"Authorization": f"Bearer {key}"}, json={...})`. The SDK handles parsing and type hints.

**Q: Is Gradio only for demos or can I deploy it?**
→ `demo.launch(share=True)` creates a public URL (72-hour temporary link). For permanent deployment, use Hugging Face Spaces (free) or any Python hosting service.

**Q: What happens to my API key if I accidentally commit it to GitHub?**
→ Revoke it immediately — GitHub scans for known API key patterns and alerts you, but attackers can also scan public repos in seconds. The key is compromised the moment it is in version control.

---

## Instructor Notes

- **API keys:** If students don't have OpenAI keys, use the mock function or have a shared class key for demo purposes. Do NOT share your personal key — create a separate limited-budget key.
- **Open-Meteo:** This is a free, open-source API with no registration required — ideal for in-class demos where student key setup would take too long.
- **Gradio install:** `pip install gradio`. Verify before the session. Gradio v4+ is recommended.
- **Network issues:** If the classroom network blocks external APIs, pre-cache the responses in pickle files and load from cache. Show the API call in code and play the cached response.
- **The session's emotional high point** is when the Gradio app runs and students can interact with it. Protect the last 10 minutes of class for this demo, even if it means cutting something earlier.
