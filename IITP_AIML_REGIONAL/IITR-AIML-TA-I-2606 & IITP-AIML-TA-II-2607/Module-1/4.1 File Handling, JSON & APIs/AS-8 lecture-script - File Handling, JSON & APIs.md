# Lecture Script: Foundations of Data — File Handling, JSON & APIs
> **Instructor Reference** — Module 1: Foundations of Data | Academic Session 8 | Duration: 2 Hours | Instructor: [Industry Mentor / Name Placeholder]

---

## Session Overview
**Goal:** By the end, students can read and write files safely using context managers, parse and generate JSON, make GET/POST API calls with the `requests` library, and apply ethical API key and rate-limit practices.

**Student profile at this point:** Comfortable with functions and all four core Python data structures from Sessions 3.2–3.3. Already has API key hygiene from Session 1.1. Likely wrong assumption: that an API call always succeeds and returns exactly the expected data. Boredom risk is low — this session feels like "real-world programming" to most students; frustration risk is moderate the first time a live API call fails due to network issues or rate limits during class.

**Key outcome:** Students should leave able to fetch real data from the internet, safely save it, and handle the case where something goes wrong — not just the happy path.

> 🎯 **The one sentence this session must land:** *Files and APIs are just Session 3.3's data structures arriving from the outside world — the skill is reading them in safely and never trusting a request has succeeded until you've checked.*

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| Opening — "Where Does Real Data Actually Come From?" | 8 min | 8 min |
| Concept + Practical Block 1: File I/O & Context Managers | 22 min | 30 min |
| Concept + Practical Block 2: JSON Structure | 20 min | 50 min |
| ☕ BREAK | 5 min | 55 min |
| Concept + Practical Block 3: APIs & the requests Library | 30 min | 85 min |
| Concept + Practical Block 4: Ethical API Usage | 15 min | 100 min |
| Summary & Bridge | 5 min | 105 min |
| Q&A & Doubt Solving | 15 min | 120 min |

---

## Opening — "Where Does Real Data Actually Come From?" (8 min)

> "Every list and dictionary you've built so far, you typed by hand. But real projects don't work that way — data arrives from files on disk, or from the internet, in real time. Today changes that entirely."

Ask the room: "When you open Swiggy and see restaurant listings, where does that data actually come from, technically?" Let a few students guess.

> "It's an API call happening the instant you open the app — a request goes out, a response comes back, usually shaped exactly like the dictionaries and lists you built last session. Today you'll learn to do that yourself: read and write files, and fetch real data from the internet."

Pivot line: "Let's start with the simpler case — your own files on disk."

---

## Concept + Practical Block 1: File I/O & Context Managers (22 min)

### "The library book you must remember to return"
> "Borrowing a library book means checking it out, using it, and returning it — if you forget to return it, the library can't lend it to the next person. Files work the same way in code: open, use, close."

**Hands-on, built live:**
```python
with open("orders.txt", "w") as f:
    f.write("Order 1: Chai, ₹20\n")
    f.write("Order 2: Samosa, ₹15\n")

with open("orders.txt", "r") as f:
    print(f.read())
```

> "Notice I never wrote `f.close()` anywhere. The `with` block does that automatically the moment we leave it — even if something crashes in between."

**Answer key / reasoning to say aloud:** Contrast with the manual version — `f = open(...)`, do stuff, `f.close()` — and point out that if an error happens between opening and closing, the manual version can leave the file open or the write incomplete; `with` guarantees proper cleanup regardless.

### 🔴 The trap / highest-value moment
Write on the board: **"`with` guarantees the file closes properly, even if your code crashes partway through. Manual open()/close() does not."**

💬 **Expect an argument about:** "Why not just always remember to call `.close()` myself?" Welcome it. Say: *"You'd have to remember it every single time, including inside error-handling code — one missed case, and you've got a corrupted or locked file. `with` removes that risk entirely, for free."*

---

## Concept + Practical Block 2: JSON Structure (20 min)

### "The filled-out application form"
> "A filled-out form has labeled fields — name, phone, a list of previous addresses. JSON is exactly this: structured, labeled data written as text, and it looks almost identical to the dictionaries and lists you built last session."

**Hands-on, live-coded:**
```python
import json

json_text = '{"name": "Priya", "orders": ["Chai", "Samosa"]}'
data = json.loads(json_text)
print(data["orders"][0])

python_dict = {"city": "Hyderabad", "pincode": 500081}
print(json.dumps(python_dict))
```

> "`json.loads` — 'load string' — turns JSON text into a real Python dictionary you can index into. `json.dumps` — 'dump string' — does the reverse."

### 🔴 The trap / highest-value moment
Write on the board: **"Raw JSON is just TEXT until you `json.loads()` it — you can't use dictionary methods on it directly before that."**

Demonstrate live: try `json_text["name"]` directly on the raw string and show the `TypeError`.

💬 **Expect an argument about:** "Why does JSON exist at all if it's basically the same as a Python dict?" Welcome it. Say: *"Because not every programming language has a 'Python dictionary' — JSON is a universal, language-independent format. A JavaScript app, a Python script, and a mobile app can all read the exact same JSON, even though each language represents it slightly differently internally."*

---

## ☕ BREAK (5 min)

---

## Concept + Practical Block 3: APIs & the requests Library (30 min)

### "Checking the menu vs. placing the order"
> "On a food delivery app, checking the menu doesn't change anything — that's a GET request, just asking for information. Placing an order sends new data to be processed — that's a POST request."

**Hands-on, live-coded (use a real, free public API if internet access is available in class):**
```python
import requests

response = requests.get("https://api.example.com/weather?city=Hyderabad")
print(response.status_code)
data = response.json()
print(data)
```

Build the status code table live, framing each as a delivery-app notification:

| Code | Meaning | Delivery-app equivalent |
|---|---|---|
| 200 | Success | "Order confirmed" |
| 404 | Not found | "This restaurant doesn't exist" |
| 429 | Too many requests | "You're calling too often, slow down" |
| 500 | Server error | "Kitchen's systems are down" |

**Answer key / reasoning to say aloud:** Deliberately call an endpoint that returns a 404 (a slightly wrong URL) to show what a failed response actually looks like, and point out that `response.json()` on a failed request may error or return an unhelpful error payload — reinforcing why you always check `status_code` first.

### 🔴 The trap / highest-value moment
Write on the board: **"Never trust a response until you've checked its status code. A failed request doesn't always look obviously broken."**

💬 **Expect an argument about:** "Why bother checking manually — shouldn't the code just fail loudly if something's wrong?" Welcome it. Say: *"Sometimes it does, but often an API returns a 200-looking response with an error message buried INSIDE the JSON body instead. Checking explicitly is the only way to catch both kinds of failure reliably."*

---

## Concept + Practical Block 4: Ethical API Usage — Keys & Rate Limits (15 min)

### "The shopkeeper who doesn't want 100 calls a minute"
> "Recall your ATM PIN from Session 1.1 — that's your API key, never shared publicly. Now add a new idea: a rate limit is like a shopkeeper politely saying 'please don't call me every 5 seconds asking for updates.' Push past that, and the service can block you entirely."

**Hands-on:**
```python
import time
import requests

for city in ["Hyderabad", "Mumbai", "Delhi"]:
    response = requests.get(f"https://api.example.com/weather?city={city}")
    print(response.json())
    time.sleep(1)
```

**Answer key / reasoning to say aloud:** Point out `time.sleep(1)` explicitly — this single line is the difference between a respectful, sustainable API usage pattern and one that risks triggering a `429` or a permanent ban.

### 🔴 The trap / highest-value moment
Write on the board: **"Looping through hundreds of API calls with no delay is the fastest way to get your key suspended — check documented rate limits before you build any loop around an API."**

💬 **Expect an argument about:** "Isn't checking the ToS overkill for a student project?" Welcome it. Say: *"It matters more than people expect — some APIs explicitly forbid redistributing their data, or using it commercially, even in student projects. A quick read of the ToS before you build something takes minutes and avoids real problems later."*

---

## Summary & Bridge (5 min)

| Concept | The one thing to remember |
|---|---|
| File I/O & context managers | `with` guarantees safe, automatic file closing |
| JSON | Structured text, converted to/from Python with `loads`/`dumps` |
| requests & APIs | GET retrieves, POST sends; always check the status code |
| Ethical API usage | Keys stay secret, respect rate limits, read the ToS |

Close on the thesis: *"Files and APIs are just Session 3.3's data structures arriving from the outside world — the skill is reading them in safely and never trusting a request has succeeded until you've checked."*

Bridge: "Real datasets are often huge and numerical — thousands of prices, scores, measurements. Next session, you'll learn NumPy, which handles large numerical data efficiently, without slow loops."

---

## Q&A & Doubt Solving (15 min)

**Q: What happens if the file I try to open with `"r"` mode doesn't exist?**
→ Python raises a `FileNotFoundError` — reading requires the file to already exist, unlike `"w"` mode, which creates a new file if one doesn't exist.

**Q: Can I use `json.loads()` on data that isn't valid JSON?**
→ No — it raises a `JSONDecodeError` if the text isn't properly formatted JSON, which is a useful signal that either the API changed its format or something went wrong upstream.

**Q: Do all APIs require an API key?**
→ No — some public APIs are open with no key required, while others require registration and a key for authentication, tracking usage, or billing purposes.

**Q: What's the difference between a 404 and a 500 error?**
→ A 404 means the specific thing you asked for doesn't exist (a wrong URL or missing resource); a 500 means something broke on the server's own side, unrelated to what you asked for.

**Q: How do I know what rate limit an API actually has?**
→ It's documented in the API's official documentation — always check there rather than guessing, since limits vary widely from provider to provider.

**Q: Can I write JSON directly to a file instead of a plain text string?**
→ Yes — `json.dump(data, f)` writes a Python object directly to an open file as JSON, and `json.load(f)` reads it back, combining today's two concepts in one step.

---

## Instructor Notes
- **Words not yet earned — avoid using without defining:** "authentication tokens," "OAuth," "webhooks," "pagination." These are more advanced API concepts that surface only if a later project specifically requires them — not today.
- **Biggest risk this session:** live API calls failing unpredictably due to classroom network issues or a demo endpoint being temporarily down — have a pre-saved example JSON response ready as a fallback so the lesson doesn't stall if live internet access misbehaves.
- **Board management:** Keep the status code table from Block 3 visible through Block 4, since ethical API usage directly builds on recognizing a `429` (rate limit) response.
- **Common confusions, numbered:**
  1. Forgetting that raw JSON text isn't yet a usable Python dictionary until parsed.
  2. Assuming an API response always succeeds without checking `status_code`.
  3. Looping through API calls with no delay, risking rate limits or bans.
- **Cross-references to later sessions:** File reading here directly sets up `pd.read_csv()` in Session 5.1; JSON structure resurfaces whenever nested API or scraped data needs to become a DataFrame; ethical data-usage habits echo forward into the EDA & Business Thinking session (6.3), where data provenance matters for trustworthy analysis.
- **Local/cultural context notes:** Library book borrowing, Swiggy's menu-browsing-vs-ordering flow, and the shopkeeper rate-limit analogy continue the running Indian-context thread — the ATM PIN callback to Session 1.1 is deliberate and should be spoken aloud to reinforce continuity across the module.
