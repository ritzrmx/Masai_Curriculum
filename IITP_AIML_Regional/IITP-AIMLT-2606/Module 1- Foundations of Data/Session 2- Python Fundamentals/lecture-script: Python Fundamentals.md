# Lecture Script: Python Fundamentals
> **Instructor Reference** — Module 1: Foundations of Data | Session 2 | Duration: 2 Hours

---

## Session Overview

**Goal:** Students write and run Python in Google Colab using variables, data types, operators, input/output, and f-strings — with habits that scale to data and ML work later.

**Student profile at this point:** Attended Session 1 (AI landscape). No prior coding required; some may have tried calculators or Excel formulas. All need hands-on confidence in Colab.

**Key outcome:** Every student completes a **profile card** program (name, age, city, favourite language) and a **tip calculator** that handles user input and formatted output without type errors.

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| Opening & Colab Setup | 5 min | 0:05 |
| **Concept 1:** Variables, Types, and `type()` | 10 min | 0:15 |
| **Practical 1:** First Cells — Assign, Inspect, Print | 15 min | 0:30 |
| **Concept 2:** Operators — Arithmetic and Comparison | 10 min | 0:40 |
| **Practical 2:** Expressions Live — `/` vs `//`, PEMDAS | 15 min | 0:55 |
| **BREAK** | 10 min | 1:05 |
| **Concept 3:** input(), print(), and f-strings | 10 min | 1:15 |
| **Practical 3:** Profile Card Lab | 15 min | 1:30 |
| **Concept 4:** Type Errors and Casting | 10 min | 1:40 |
| **Practical 4:** Tip Calculator + Deliberate Error Demo | 10 min | 1:50 |
| Summary & Wrap-Up | 5 min | 1:55 |
| Q&A & Doubt Solving | 5 min | 2:00 |

---

## SEGMENT 1: Opening & Colab Setup (8 min)


**Hook:** Show a blank Colab notebook. Run:

```python
print("Hello, future AI engineer!")
```

**Ask:** *"What just happened? Where did that text come from?"* → Python executed a command; `print` sent output to the screen.

**Context to set:** Session 1 was the map. Session 2 is the first tool in your hands. Every dataset you load, every model you train, every chart you draw — it all starts with variables and expressions in Python.

**Learning contract for today:**
- Create and name variables with correct types
- Use operators to compute values
- Ask the user for input and show formatted output
- Fix the most common beginner type errors

**Say:** *"You cannot break Colab. Run cells, read errors, fix, rerun. That loop is programming."*

### Colab Setup (live — 3 min)

1. Open [colab.research.google.com](https://colab.research.google.com)
2. **File → New notebook**
3. Rename: `Session2_Python_Fundamentals_<YourName>`
4. First cell → switch to **Markdown**, title: `# Session 2 — Python Fundamentals`
5. Second cell → **Code**

**Write on board:** Shift+Enter = run cell

---

## SEGMENT 2: Variables, Types & type() (13 min)


### Variables Are Labels

| Concept | Syntax | Example |
|---|---|---|
| Assign | `name = value` | `age = 25` |
| Reassign | same name, new value | `age = 26` |
| Inspect type | `type(x)` | `type(age)` → int |

**The four types today:**

| Type | Python keyword | Example | Real use |
|---|---|---|---|
| int | `int` | `2026`, `-3` | Count, year, age |
| float | `float` | `99.5`, `3.0` | Price, temperature |
| str | `str` | `"Priya"`, `'AI'` | Names, messages |
| bool | `bool` | `True`, `False` | Flags (later with if) |

**Key teaching point:** Python **infers** type from the value you assign. You rarely write `int x = 5` like in other languages — just `x = 5`.

**Naming conventions:**
- `snake_case` for variables: `bill_amount`
- Avoid spaces and reserved words (`print`, `input`, `if` are not variable names)

**Ask:** *"Is `3.0` an int or a float?"* → float. The decimal point matters even if `.0`.

---

## SEGMENT 3: First Cells Lab (15 min)


### Live code — students type along

**Cell 1 — Basic assignments**

```python
name = "Priya"
age = 25
height_m = 1.62
is_learning_python = True

print(name)
print(age)
print(height_m)
print(is_learning_python)
```

**Expected output:**

```
Priya
25
1.62
True
```

**Ask:** *"What type is each variable?"* Students guess before you reveal:

```python
print(type(name))
print(type(age))
print(type(height_m))
print(type(is_learning_python))
```

**Expected output:**

```
<class 'str'>
<class 'int'>
<class 'float'>
<class 'bool'>
```

**Cell 2 — Reassignment**

```python
age = 25
print("Before:", age)
age = 26
print("After birthday:", age)
```

**Expected output:**

```
Before: 25
After birthday: 26
```

**Cell 3 — Strings use quotes**

```python
course = "AI & ML"
print(course)
# course = AI & ML   # Uncomment to show SyntaxError — no quotes = broken
```

**Walkthrough tip:** Run the broken line deliberately if time allows. Read the **SyntaxError** aloud — "Python expected a string."

**Say/Ask prompts:**
- *"What happens if you spell `naem` instead of `name`?"* → NameError later
- *"Can a variable name start with a number?"* → No: `2nd_place = 1` fails

---

## SEGMENT 4: Operators (13 min)


### Arithmetic

| Op | Meaning | Note |
|---|---|---|
| `+` `-` `*` | Standard math | |
| `/` | Division | Always returns **float** in Python 3 |
| `//` | Floor division | Drops decimal part |
| `%` | Remainder | Useful for even/odd |
| `**` | Power | `2 ** 3` = 8 |

### Comparison (preview for Session 3)

| Op | Result type |
|---|---|
| `==`, `!=`, `>`, `<`, `>=`, `<=` | bool (True/False) |

**Key teaching point:** `/` vs `//` trips up every cohort. Ten divided by four is **2.5** with `/` and **2** with `//`.

---

## SEGMENT 5: Expressions Lab (15 min)


```python
print("10 + 3 =", 10 + 3)
print("10 - 3 =", 10 - 3)
print("10 * 3 =", 10 * 3)
print("10 / 3 =", 10 / 3)
print("10 // 3 =", 10 // 3)
print("10 % 3 =", 10 % 3)
print("2 ** 4 =", 2 ** 4)
```

**Expected output:**

```
10 + 3 = 13
10 - 3 = 7
10 * 3 = 30
10 / 3 = 3.3333333333333335
10 // 3 = 3
10 % 3 = 1
2 ** 4 = 16
```

**Ask:** *"Why is 10 % 3 equal to 1?"* → 3 goes into 10 three times with remainder 1.

**PEMDAS demo:**

```python
print(2 + 3 * 4)       # 14, not 20
print((2 + 3) * 4)     # 20
```

**Comparison preview:**

```python
print(10 > 7)    # True
print(10 == 10)  # True  — note DOUBLE equals
print(10 = 10)   # SyntaxError — assignment, not comparison
```

**Deliberately show `10 = 10` error** — students will confuse `=` and `==` in Session 3.

**Extension (fast finishers):**

```python
# Convert Celsius to Fahrenheit
celsius = 38
fahrenheit = celsius * 9/5 + 32
print(f"{celsius}°C = {fahrenheit}°F")
```

---

## BREAK (10 min)

---


*Suggested break prompt:* Add a markdown cell listing three things you learned. After break, share one.

---

## SEGMENT 6: input, print & f-strings (13 min)


### The I/O Pattern

```
input()  →  always returns str
process  →  convert types if needed
print()  →  show result to user
```

| Function | Purpose | Returns |
|---|---|---|
| `input("prompt")` | Ask user for text | str |
| `print(x)` | Show output | None |
| f-string | Format text with variables | str |

**f-string rules:**
- Prefix with `f` or `F`
- Variables inside `{curly braces}`
- Optional format: `{value:.2f}` for two decimal places

```python
name = input("Your name: ")
print(f"Welcome, {name}!")
```

**Ask:** *"If the user types `25` for age, what type is it inside Python?"* → Still str until you cast.

---

## SEGMENT 7: Profile Card Lab (15 min)


### Requirements (display on slide)

Build a **Profile Card** program that:

1. Asks for: **name**, **age**, **city**, **favourite programming language** (or "none yet")
2. Stores each answer in a clearly named variable
3. Prints **two lines** using f-strings:
   - Line 1: greeting with name and city
   - Line 2: age now and age in 5 years
4. Bonus: third line with favourite language

### Starter scaffold (optional — or students write from scratch)

```python
# Profile Card Lab
name = input("Your name: ")
age = int(input("Your age: "))
city = input("Your city: ")
fav_lang = input("Favourite language (or 'none yet'): ")

print(f"Hello {name} from {city}! Welcome to Python.")
print(f"You are {age} today. In 5 years you will be {age + 5}.")
print(f"Language you are excited about: {fav_lang}")
```

**Sample run:**

```
Your name: Arjun
Your age: 22
Your city: Pune
Favourite language (or 'none yet'): Python

Hello Arjun from Pune! Welcome to Python.
You are 22 today. In 5 years you will be 27.
Language you are excited about: Python
```

**Facilitation (10 min coding, 5 min share):**
- Walk the room — top error: forgetting `int()` on age
- Call 2 students to screen-share output
- Praise readable variable names

**Say:** *"This is your first interactive program. Apps are just many inputs and outputs like this."*

---

## SEGMENT 8: Type Errors & Tip Calculator (15 min)


### The #1 Beginner Bug

```python
age = input("Age: ")
print(age + 1)   # TypeError!
```

**Error message:** `TypeError: can only concatenate str (not "int") to str`

**Why:** `input()` returns str. `"25" + 1` mixes text and number.

### Fixes

```python
# Fix 1: cast at input
age = int(input("Age: "))
print(age + 1)

# Fix 2: cast after input
age = input("Age: ")
age = int(age)
print(age + 1)
```

### Other common errors

| Error | Cause | Fix |
|---|---|---|
| NameError | Typo in variable name | Spell consistently |
| SyntaxError | Missing quote, bad `=` | Check punctuation |
| ValueError | `int("twenty")` | Validate input (later sessions) |
| TypeError | str + int | Cast with int() or float() |

**Teaching point:** Read the **last line** of the error first. It usually tells you exactly what went wrong.

---

### Practical — Tip Calculator (10 min)


### Tip Calculator — full solution

```python
# Tip Calculator
bill = float(input("Enter bill amount (₹): "))
tip_percent = 15
tip = bill * tip_percent / 100
total = bill + tip

print(f"Bill:        ₹{bill:.2f}")
print(f"Tip ({tip_percent}%): ₹{tip:.2f}")
print(f"Total:       ₹{total:.2f}")
```

**Sample run:**

```
Enter bill amount (₹): 1200
Bill:        ₹1200.00
Tip (15%): ₹180.00
Total:       ₹1380.00
```

**Ask:** *"Why `float()` for bill but not for tip_percent?"* → Bill may have paise; 15 is already an int.

### Deliberate error demo (2 min)

Run broken version first:

```python
bill = input("Enter bill amount (₹): ")
tip = bill * 0.15   # TypeError: str * float
```

**Say:** *"Every professional sees red errors daily. The skill is diagnosing in 30 seconds."*

Fix live with `float(input(...))`.

**Extension:** Ask for custom tip percentage with `int(input(...))`.

---

## SEGMENT 9: Summary & Wrap (8 min)


**What we covered today:**
- Variables and four core types: int, float, str, bool
- `type()` to inspect values
- Operators: especially `/` vs `//` and `%`
- `input()`, `print()`, and f-strings for user-facing programs
- Casting with `int()` and `float()` to avoid TypeError
- Colab discipline: one step per cell, run top to bottom

**Bridge to next session:** *"Next class we add **decisions** — if the score is above 60, pass; else, retake. Your tip calculator becomes smarter when it applies different rules for different inputs."*

**Homework / self-practice:**
1. Extend the profile card: ask for year of birth and compute age (assume current year 2026).
2. Build a **split-bill** calculator: bill + tip, divided by number of friends (use `/`).
3. Write one markdown cell in Colab explaining what `//` and `%` do — teach a friend.

---

## Q&A & Doubt Solving (5 min)

**Likely questions and suggested answers:**

**Q: When do I use int vs float?**
→ int for whole counts; float for money, measurements, and anything with decimals. When unsure with division, float is safer.

**Q: Can I use single quotes `'hello'` instead of double `"hello"`?**
→ Yes. Be consistent. Use one style per project.

**Q: Why does `10 / 2` give `5.0` not `5`?**
→ Python 3 `/` always returns float. Use `//` if you need integer division.

**Q: Colab says "session crashed" — what do I do?**
→ Runtime → Restart runtime. Re-run cells from top. Save important work to Drive often.

**Q: Is `input()` OK for real apps?**
→ For learning, yes. Production apps use forms, APIs, and validation. Same variables underneath.

---

## Instructor Notes

- **Environment:** Google Colab only — no local install required. Confirm all students can run `print("ok")` before Concept 1.
- **Common student mistake:** `print(f"Age: {age}")` without defining `age` first — run cells in order.
- **Another mistake:** `int(input("Age: "))` when user types `"twenty-two"` → ValueError. Acknowledge; full validation comes in Session 3+.
- **Live coding tip:** Make one intentional typo (`naem`) to normalise NameError.
- **Pacing:** If behind, give profile card starter code; if ahead, add split-bill extension.
- **Accessibility:** Read error messages aloud slowly. Beginners treat red text as failure — reframe as "Python's help note."
- **Time check:** If long after break, shorten Concept 4 to demo only and assign tip calculator as homework with solution posted.

---

## Common Errors — Quick Reference Sheet (share in chat)

| Code | Error | Fix |
|---|---|---|
| `print(naem)` | NameError | Fix spelling |
| `"5" + 1` | TypeError | `int("5") + 1` |
| `print(age + 1)` after input | TypeError | `int(input(...))` |
| `if age = 18` | SyntaxError | Use `==` in Session 3 |
| Missing `"` on string | SyntaxError | Close quote |

---

## Appendix: Complete Reference Notebook (Instructor Solution)

```python
# === Session 2 Reference Solution ===

# --- Variables & types ---
name = "Priya"
age = 25
print(type(name), type(age))

# --- Operators ---
print(10 / 4, 10 // 4, 10 % 4)

# --- Profile Card ---
name = input("Your name: ")
age = int(input("Your age: "))
city = input("Your city: ")
fav_lang = input("Favourite language: ")
print(f"Hello {name} from {city}!")
print(f"Age: {age}, in 5 years: {age + 5}")
print(f"Excited about: {fav_lang}")

# --- Tip Calculator ---
bill = float(input("Bill (₹): "))
tip = bill * 15 / 100
print(f"Total with 15% tip: ₹{bill + tip:.2f}")
```

---

## End-of-Session Quiz (5 Questions)

1. Define AI, ML, and GenAI in one sentence each.
2. Classify: UPI OTP above ₹10,000; Swiggy ETA; ChatGPT email draft.
3. What ML problem type is "predict monthly sales"?
4. Name two responsible AI habits when using GenAI for customer support.
5. Which role builds nightly data pipelines — analyst, engineer, or scientist?

**Answer key (instructor):** AI=umbrella field; ML=learns from data; GenAI=creates content. Rules/ML/GenAI respectively. Regression. Human review; verify facts. Data engineer.

---

## Homework Rubric

| Criterion | Excellent (4) | Good (3) | Needs Work (2) | Incomplete (1) |
|---|---|---|---|---|
| Core lab task | 4 clear categories with data sources | 3 mostly correct | 2 with gaps | 1 or missing |
| Lab completion | 8/8 defended | 6–7/8 | 4–5/8 | <4 |
| Written framing | 2 scenarios with I/O types | 2 partial | 1 complete | 0 |
| Reflection | Thoughtful responsible AI note | Good | Brief | Missing |

**Total:** /16 — Pass threshold: 10/16

---

## Materials Checklist

- [ ] Slide: nested AI / ML / GenAI diagram
- [ ] 8 (+1 optional) classification cards
- [ ] Course roadmap slide (Modules 1–3)
- [ ] Whiteboard markers
- [ ] Exit ticket form or sticky notes
- [ ] Timer visible to students

---

## Timing Contingencies

| Situation | Action |
|---|---|
| Running 10 min behind before break | Shorten Practical 2 walkthrough; assign e-commerce table as homework |
| Running long after break | Shorten Practical 4 to two scenarios instead of four |
| Low energy | Stand/sit vote on one headline card |
| Advanced students finish early | Stretch: Google Maps ETA — ML or rules? |
| No projector | Use chat poll for headline sort |

---

## FAQ — Q&A (8+ Questions)

**Q: Is ChatGPT "AI" or "GenAI"?** → Both. GenAI product inside AI field. Say "GenAI assistant" in interviews.

**Q: Can a rule-based system beat ML?** → Yes when rules are complete, stable, auditable.

**Q: Do I need math for ML?** → Module 1 builds Python/data first; Module 2 adds needed math.

**Q: Is Excel with formulas AI?** → Formulas are rules. Forecast on history is ML.

**Q: What's deep learning vs ML?** → Deep learning uses neural nets with many layers.

**Q: Will GenAI replace data jobs?** → No — pipelines and cleaning stay essential.

**Q: What is RAG?** → Retrieval + generation — Module 3 topic.

**Q: How pick a career path?** → Match ecosystem role to what excites you.


---

## SEGMENT 11: Supplemental Python Demos

### Demo — UPI receipt f-string

```python
upi_id = "priya@okhdfc"
amount = 250.50
print(f"Pay ₹{amount:.2f} to {upi_id}")
```

**Output:** `Pay ₹250.50 to priya@okhdfc`

**Break it down:** f-string embeds variables; `:.2f` formats two decimals.

**Ask:** Why two decimals for rupees?

**Common mistake:** Using comma as decimal separator.

**Fix:** Use dot: `250.50` not `250,50`.

### Demo — Split bill

```python
bill = 1200
friends = 5
print(f"Each pays ₹{bill / friends:.2f}")
```

**Output:** `Each pays ₹240.00`

**Break it down:** `/` returns float; f-string displays cleanly.

**Ask:** What if friends = 0?

**Common mistake:** Dividing by zero.

**Fix:** Validate `friends > 0` before dividing.

### Demo — Type error and fix

```python
# Broken: age = input("Age: "); print(age + 1)
age = int(input("Age: "))
print(age + 1)
```

**Break it down:** input returns str; int() enables math.

**Ask:** What error without int()?

**Common mistake:** Ignoring TypeError message.

**Fix:** Read last line of traceback.

### Colab discipline reference

| Rule | Why |
|---|---|
| One step per cell | Easier debug |
| Run top to bottom | Variables exist in order |
| Save to Drive | Sessions expire |

### Homework rubric detail

| Task | Excellent | Good | Needs work |
|---|---|---|---|
| Profile card | 4 inputs, f-strings, runs | 3 inputs | type errors |
| Tip calculator | float input, formatted | wrong math | missing cast |
| Split bill | correct / | wrong operator | incomplete |

### FAQ additions

**Q: int vs float?** → int for counts; float for money.

**Q: Why 10/2 is 5.0?** → Python 3 `/` always float.

**Q: Colab crashed?** → Restart runtime; rerun from top.

**Q: NameError?** → Run defining cell first.

**Q: ValueError on int()?** → User typed non-number.

**Q: Single vs double quotes?** → Both fine.

**Q: input in production?** → Forms/APIs later.

**Q: Save work?** → Copy to Drive early.


---

## SEGMENT 12: Extended Labs & Code Annotations

### Lab — Zomato-style line items

```python
item1, item2 = "Paneer Tikka", "Butter Naan"
price1, price2 = 280.0, 60.0
qty1, qty2 = 1, 2
subtotal = price1 * qty1 + price2 * qty2
gst = subtotal * 0.05
total = subtotal + gst
print(f"Subtotal: ₹{subtotal:.2f}")
print(f"GST 5%: ₹{gst:.2f}")
print(f"Total: ₹{total:.2f}")
```

**Output:**
```
Subtotal: ₹400.00
GST 5%: ₹20.00
Total: ₹420.00
```

**Break it down:**
- Multiple float variables for menu math
- Expression on one line for subtotal
- GST as percentage of subtotal

**Ask:** Where would you use int instead of float in this lab?

**Common mistake:** Forgetting GST is applied on subtotal not per item randomly.

**Fix:** Compute subtotal first, then tax once.

### Lab — compare / and //

```python
bill = 1000
people = 3
print("Exact share:", bill / people)
print("Whole rupees each:", bill // people)
print("Leftover rupees:", bill % people)
```

**Output:**
```
Exact share: 333.3333333333333
Whole rupees each: 333
Leftover rupees: 1
```

**Break it down:**
- `/` for exact split with decimals
- `//` for whole rupee buckets
- `%` for remainder — useful for paise adjustments

**Ask:** How would you express leftover as paise?

**Common mistake:** Using // when you need precise paise split.

**Fix:** Use float `/` and round with f-string `:.2f`.

### Student extension — EMI hint

```python
principal = 500000
rate_annual = 10.5
years = 5
# Simple interest estimate (not full EMI — concept only)
interest = principal * (rate_annual / 100) * years
print(f"Simple interest estimate: ₹{interest:,.2f}")
```

**Break it down:** Float division for rate; comma in format groups lakhs.

**Ask:** Why is this not bank-accurate EMI?

**Common mistake:** Claiming this is exact loan math.

**Fix:** Label as estimate; full EMI formula comes later.

### Session 2 materials timing

| Segment | Must-show code | Optional |
|---|---|---|
| 3 | assign + type | UPI f-string |
| 5 | / vs // | GST calc |
| 7 | profile card | EMI hint |
| 8 | tip calculator | custom tip % |

