# Lecture Script: Master Class — Numbers, Logic & Structure
> **Instructor Reference** — Module 1: Foundations of Data | Session 5 | Duration: 2 Hours

---

## Session Overview

**Goal:** Students build intuition for binary/boolean logic, truth tables, De Morgan's laws, sets/Venn diagrams, mathematical functions, number systems, and filter logic — and connect each idea to Python they already use.

**Student profile at this point:** Comfortable with `if`/`elif`/`else`, loops, and basic types from Sessions 2–4. Some anxiety about "math" — this session reframes math as the language already running inside their code.

**Key outcome:** Every student can complete a truth table by hand, simplify one negated condition with De Morgan's laws, explain union/intersection with a Venn sketch, state domain/range for a score→grade mapping, and describe how the same AND/OR/NOT logic appears in data filters — with optional Python demos confirming the board work.

**Tone:** Conceptual, board-heavy, minimal coding. Draw truth tables and Venn diagrams. Use Python only to *verify* logic, not to introduce new syntax.

**Master class contract:** Laptops half-closed. Whiteboard is primary. Python proves the board — not the other way around.

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| SEGMENT 1: Opening & Hook — Why Math Is Already in Your Code | 10 min | 0:10 |
| SEGMENT 2: Binary, Boolean & Truth Tables | 25 min | 0:35 |
| SEGMENT 3: Practical — Build Tables on Board + Python Check | 15 min | 0:50 |
| SEGMENT 4: De Morgan's Laws & Negated Conditions | 15 min | 1:05 |
| **BREAK** | 10 min | 1:15 |
| SEGMENT 5: Sets, Venn Diagrams & Python Collections | 25 min | 1:40 |
| SEGMENT 6: Practical — Venn Activity & Filter Logic Preview | 15 min | 1:55 |
| SEGMENT 7: Math Functions, Number Systems & Python `def` Preview | 20 min | 2:15 |
| SEGMENT 8: Quiz, Homework, FAQ & Wrap | 15 min | 2:30 |

*Note: Master class may run 10–15 min over if discussion is rich — trim SEGMENT 7 number-systems digression or shorten quiz discussion if needed to end by 2:30.*

---

## SEGMENT 1: Opening & Hook (10 min)

### Hook (4 min)

**Write on board:**

```
IF age >= 18 AND has_valid_id:
    allow_entry = True
```

**Ask:** *"You wrote this in Session 3. Where is the math?"*

Wait for answers. Students may say comparisons, numbers, or "no math — it's Python."

**Reveal:** Every `and` / `or` / `not` is **Boolean algebra** — invented long before Python. Computers store True/False as 1/0 (**binary**). Data filters, SQL `WHERE` clauses, and ML feature flags all use the same logic.

**Second hook — local context:**

**Ask:** *"When you order on Swiggy or Zomato, what yes/no checks happen before you see restaurants?"*

Collect: logged in, location serviceable, restaurant open, maybe membership offer.

**Say:** *"That's a chain of AND conditions. You already think in math — you just called it 'code.'"*

### Why This Master Class Matters (4 min)

**Connect to course arc:**

| Session | What you did | Math underneath |
|---|---|---|
| 3 | `if` / `elif` / `else` | Boolean logic, comparisons |
| 4 | `for` loops | Repeated steps, finite sets |
| 5 (today) | Name the math | Truth tables, sets, functions |
| 6 (next) | `def` functions | Domain → range mappings |
| 10+ | Pandas filters | Same AND/OR on every row |

**Say:** *"This is not a math exam. It is a **translation session**: whiteboard symbols ↔ Python ↔ business rules. Students who master this read specs, debug conditions, and interview with confidence."*

### Learning Contract (2 min)

**Today's checklist — write on board:**

- Fill truth tables for AND, OR, NOT
- Rewrite negated conditions with De Morgan's laws
- Use Venn diagrams for union, intersection, difference
- State domain and range for a simple mapping
- Preview how filter logic becomes SQL/Pandas later

**Say:** *"Keep your laptop half-closed. The board is primary today. We will run small Python checks to prove the board — not the other way around."*

---

## SEGMENT 2: Binary, Boolean & Truth Tables (25 min)

### From Switches to True/False (5 min)

Draw a simple switch on the board: OFF = 0, ON = 1.

**Key teaching point:** One bit is tiny. Billions of bits form numbers, text, and images. At the **decision layer**, we collapse to **True** or **False**.

| Human | Python | Binary idea |
|---|---|---|
| Yes | `True` | 1 |
| No | `False` | 0 |

**Ask:** *"Is `score >= 60` a number or a boolean?"*

Wait. Answer: It **compares** numbers but **produces** True/False — so the result is boolean.

**Say:** *"The score is a number. The pass check is yes/no. Data columns like `is_active` store that yes/no directly."*

### Python Boolean Demo (3 min)

```python
age = 22
is_adult = age >= 18
print(is_adult)
print(type(is_adult))
```

**Output:**
```
True
<class 'bool'>
```

**Break it down:**
- `age >= 18` compares two numbers and returns `True` or `False`
- `is_adult` stores that boolean in a variable
- `type()` confirms the value is `bool`, not `int`

**Ask:** *"What prints if age is 15?"* → `False`

**Common mistake:** Confusing `=` (assign) with `==` (compare). `age = 18` stores; `age == 18` asks a yes/no question.

### Truth Table for NOT (3 min)

Build on board:

| A | NOT A |
|---|---|
| T | F |
| F | T |

**Class chant:** *"NOT flips the row."*

```python
is_raining = True
print(not is_raining)
```

**Output:**
```
False
```

**Break it down:**
- `not` is the Python word for NOT
- True becomes False; False becomes True

**Ask:** *"If `is_member` is False, what is `not is_member`?"* → True

### Truth Table for AND (5 min)

Build slowly — four rows only:

| A | B | A AND B |
|---|---|---|
| T | T | T |
| T | F | F |
| F | T | F |
| F | F | F |

**Memory hook:** AND is picky — **both** must be True.

```python
has_ticket = True
age_ok = True
print(has_ticket and age_ok)

has_ticket = True
age_ok = False
print(has_ticket and age_ok)
```

**Output:**
```
True
False
```

**Break it down:**
- `and` needs both sides True
- First pair: True and True → True (entry allowed)
- Second pair: True and False → False (denied)

**Ask:** *"For a Mumbai metro token machine: needs valid ticket AND balance — which row matters?"* → Only both True

**Common mistake:** Using `and` when you mean `or`. "Accept cash or UPI" needs OR, not AND.

### Truth Table for OR (4 min)

| A | B | A OR B |
|---|---|---|
| T | T | T |
| T | F | T |
| F | T | T |
| F | F | F |

**Memory hook:** OR is generous — **at least one** True.

```python
is_weekend = False
is_holiday = True
print(is_weekend or is_holiday)
```

**Output:**
```
True
```

**Break it down:**
- Only one side needs to be True
- Weekend OR holiday → day off school/work

**Ask:** *"Give a real rule that should use OR, not AND."* → e.g. "Notify if SMS fails OR email bounces"

### Compound Conditions (5 min)

**Example on board:** `(A or B) and not C`

**Say:** *"Solve inside-out: NOT first, then AND/OR — unless parentheses say otherwise."*

Give students: `A=True`, `B=False`, `C=True`. Work on paper for 2 minutes.

**Reveal step by step:**
- `A or B` → True
- `not C` → False
- `True and False` → **False**

```python
A, B, C = True, False, True
result = (A or B) and not C
print(result)
```

**Output:**
```
False
```

**Break it down:**
- Parentheses force `A or B` first
- `not C` flips True to False
- Final `and` needs both sides True — fails

**Write on board:** **Truth table = exhaust all combinations — no guessing**

**Ask:** *"How many rows for three variables A, B, C?"* → 8 rows (2³)

---

## SEGMENT 3: Practical — Build Tables on Board + Python Check (15 min)

### Activity — Hand Truth Table (7 min)

**Problem (on slide or board):**

> Let `P = age >= 18`, `Q = has_membership`. Fill the table for `P and Q`.

Use concrete rows — Indian gym membership example:

| age | membership | P | Q | P and Q | Discount? |
|---|---|---|---|---|---|
| 20 | True | T | T | T | Yes |
| 16 | True | F | T | F | No |
| 25 | False | T | F | F | No |
| 15 | False | F | F | F | No |

**Ask pairs:** *"Which rows get the discount?"* — Only row 1.

**Ask:** *"A 25-year-old without membership — which column fails?"* → Q is False, so AND fails.

### Python Verification (5 min)

```python
def show_and(age, member):
    p = age >= 18
    q = member
    result = p and q
    print(f"age={age}, member={member} -> P={p}, Q={q}, P and Q={result}")

show_and(20, True)
show_and(16, True)
show_and(25, False)
```

**Output:**
```
age=20, member=True -> P=True, Q=True, P and Q=True
age=16, member=True -> P=False, Q=True, P and Q=False
age=25, member=False -> P=True, Q=False, P and Q=False
```

**Break it down:**
- Function mirrors the board columns P, Q, and result
- Python prints `True`/`False` — same as your table
- The board is not "theory"; it is the spec the machine follows

**Ask:** *"If we changed `and` to `or`, which rows would give discount?"* → Rows 1, 2, and 3 (anyone 18+ OR anyone with membership)

**Common mistake:** Testing only one row. Always check boundaries: exactly 18, exactly at threshold.

### Optional Stretch — Truth Table Loop (3 min)

```python
def truth_and(a, b):
    return a and b

for a in (True, False):
    for b in (True, False):
        print(a, b, "->", truth_and(a, b))
```

**Output:**
```
True True -> True
True False -> False
False True -> False
False False -> False
```

**Break it down:**
- Nested loops visit every combination — exactly what a truth table lists
- Outer loop: A; inner loop: B
- Four rows, no missing cases

**Say:** *"When you write `for` loops in Session 4, you were already walking combinations. Today we name that pattern."*

---

## SEGMENT 4: De Morgan's Laws & Negated Conditions (15 min)

### The Two Laws (5 min)

**Write large on board:**

```
NOT (A AND B)  ≡  (NOT A) OR (NOT B)
NOT (A OR B)   ≡  (NOT A) AND (NOT B)
```

Use ≡ meaning "always the same result."

**Intuition for first law:** Negating "both required" becomes "fail if **either** fails."

**Business example — e-commerce:**

```
NOT (paid AND shipped)
≡ (NOT paid) OR (NOT shipped)
```

**Ask:** *"An order paid but not shipped — in the filter or not?"*

Wait. → NOT paid is False, NOT shipped is True → OR → **True** (shows in "not fully complete" list).

**Ask:** *"An order paid AND shipped — in the filter?"* → Both NOTs False → OR → False → excluded. Good.

### Python Link from Session 3 (5 min)

```python
paid = True
shipped = False

print(not (paid and shipped))
print((not paid) or (not shipped))
```

**Output:**
```
True
True
```

**Break it down:**
- `paid and shipped` → False (not both true)
- `not False` → True
- `(not paid) or (not shipped)` → False or True → True — same answer

**Ask:** *"Why would we rewrite the second form?"* → Easier to read in dashboards; matches how business teams describe exceptions

**Common mistake:** Writing `not paid and shipped` without parentheses — operator precedence makes it `(not paid) and shipped`, which is **not** De Morgan.

**Write on board:** **When negating a group — parentheses first, then De Morgan**

### Board Drill (5 min)

**Prompt:** Simplify `NOT (A OR B)` using De Morgan.

**Reveal:** `(NOT A) AND (NOT B)`

**Quick verify** with `A=True`, `B=False`:
- `NOT (True OR False)` → NOT True → **False**
- `(NOT True) AND (NOT False)` → False AND True → **False** ✓

```python
A, B = True, False
print(not (A or B))
print((not A) and (not B))
```

**Output:**
```
False
False
```

**Break it down:**
- `A or B` is True (first True wins)
- Negated → False
- De Morgan form also False — laws hold

**Say:** *"When a Pandas filter looks wrong, try De Morgan on paper before changing code."*

---

## — 10-MINUTE BREAK —

*Break prompt on slide:* Sketch two overlapping circles on paper. Label left "Product A buyers", right "Product B buyers". Shade union and intersection. Be ready to compute counts after break.

---

## SEGMENT 5: Sets, Venn Diagrams & Python Collections (25 min)

### Set Definition (4 min)

**One-line for students:** A **set** holds **unique** items; order does not matter for membership.

On the board, draw Venn diagram with circles A and B.

| Region | Name | Symbol | Python |
|---|---|---|---|
| A only | A minus B | A − B | `A - B` |
| B only | B minus A | B − A | `B - A` |
| Overlap | Intersection | A ∩ B | `A & B` |
| Either or both | Union | A ∪ B | `A \| B` |

**Ask:** *"Can a set contain duplicate user IDs?"* → No — second duplicate is ignored or rejected

### Worked Example — Streaming Genres (6 min)

```
A = users who watched Action
B = users who watched Comedy

A & B  → watched both (overlap)
A | B  → watched at least one
A - B  → Action only, never Comedy
```

**Ask:** *"If |A| = 100, |B| = 80, |A ∩ B| = 30, how many in A ∪ B?"*

Pairs compute 2 min. → 100 + 80 − 30 = **150** (include overlap once).

**Write formula on board:** `|A ∪ B| = |A| + |B| − |A ∩ B|`

**Say:** *"This is the same counting you do for festival crowds — don't double-count people in both circles."*

### Python Set Demo (5 min)

```python
action = {"u1", "u2", "u3", "u4"}
comedy = {"u3", "u4", "u5"}

print("Both:", action & comedy)
print("Either:", action | comedy)
print("Action only:", action - comedy)
```

**Output:**
```
Both: {'u3', 'u4'}
Either: {'u1', 'u2', 'u3', 'u4', 'u5'}
Action only: {'u1', 'u2'}
```

**Break it down:**
- `&` intersection — users in both sets
- `|` union — all unique users from either set
- `-` difference — in first set but not second

**Ask:** *"How many in union?"* → 5 users

**Common mistake:** Using `+` on sets — sets use `|` for union, not `+`

### Lists, Dicts, JSON — Structure Map (5 min)

| Structure | Math view | Python | Duplicate allowed? |
|---|---|---|---|
| Sequence | Ordered list | `list` | Yes |
| Set | Unordered unique | `set` | No |
| Map | Function keys→values | `dict` | Keys unique |
| Wire text | JSON object/array | `json.loads` | JSON object keys unique |

**Teaching point:** When you need "unique user IDs", a **set** (or `drop_duplicates` in Pandas later) matches the math. When you need "user_id → email", a **dict** is a map.

```python
cities = ["Mumbai", "Pune", "Mumbai"]
unique_cities = set(cities)
print(unique_cities)
```

**Output:**
```
{'Mumbai', 'Pune'}
```

**Break it down:**
- List allows duplicate "Mumbai"
- Set keeps one copy — uniqueness enforced

**Ask:** *"When would a list be better than a set?"* → When order matters or duplicates matter (transaction log)

**Link to data cleaning (future):** Duplicate rows = set violation at the row level. You will fix that in Session 10+.

### Venn Picture → Business Language (5 min)

**Draw on board** while narrating Flipkart-style campaigns:

- Circle A: bought electronics in sale
- Circle B: bought fashion in sale
- Overlap: bought both
- A only: electronics-only buyers

**Ask:** *"Marketing wants 'anyone who bought either category' — which operation?"* → Union

**Ask:** *"Cross-sell to people who bought electronics but not fashion — which region?"* → A − B

---

## SEGMENT 6: Practical — Venn Activity & Filter Logic Preview (15 min)

### Venn Activity — Customers A & B (8 min)

**Scenario:** Kirana chain runs two campaigns in March.

- **A:** Bought snacks  
- **B:** Bought beverages  

Give counts (on slide):

- |A only| = 40  
- |B only| = 35  
- |A ∩ B| = 25  

**Tasks for pairs (4 min):**
1. Shade A ∪ B on Venn sketch  
2. Compute |A ∪ B|  
3. How many bought **only** beverages?  
4. Campaign reach for "snack OR beverage buyers"?

**Reveal:**
- |A ∪ B| = 40 + 35 + 25 = **100**  
- B only = **35**  
- Campaign reach = **100**

**Ask:** *"Why subtract 25?"* → Counted twice in 40+35 — they are the overlap

### Filter Logic Preview — Same Math, Different Syntax (7 min)

**Say:** *"You have not written SQL or Pandas yet. But the logic is Session 3 again — applied to every row in a table."*

**Tiny table on board:**

| order_id | city | amount_inr |
|---|---|---|
| 101 | Mumbai | 1200 |
| 102 | Pune | 800 |
| 103 | Mumbai | 450 |

**Condition:** `city == "Mumbai" and amount_inr >= 500`

Build boolean mask on board:

| row | city==Mumbai | amt>=500 | AND | Keep? |
|---|---|---|---|---|
| 101 | T | T | T | Yes |
| 102 | F | T | F | No |
| 103 | T | F | F | No |

```python
# Preview only — full Pandas comes in Session 10
orders = [
    {"order_id": 101, "city": "Mumbai", "amount_inr": 1200},
    {"order_id": 102, "city": "Pune", "amount_inr": 800},
    {"order_id": 103, "city": "Mumbai", "amount_inr": 450},
]

for row in orders:
    keep = row["city"] == "Mumbai" and row["amount_inr"] >= 500
    print(row["order_id"], "->", keep)
```

**Output:**
```
101 -> True
102 -> False
103 -> False
```

**Break it down:**
- Each row evaluates the same condition — like a truth table row
- `and` requires both city match and amount threshold
- Only order 101 passes

**Ask:** *"How is this different from one `if` in Session 3?"* → Same condition, many rows — data scale

**Common mistake:** Using `or` when business meant `and` — "Mumbai OR amount>=500" would keep rows 101, 102, and 103

**SQL preview on board (no execution):**

```sql
SELECT * FROM orders
WHERE city = 'Mumbai' AND amount_inr >= 500;
```

**Say:** *"AND is AND. The notation changed; the truth table did not."*

---

## SEGMENT 7: Math Functions, Number Systems & Python `def` Preview (20 min)

### Mathematical Function Definition (5 min)

**Write on board:**

```
f: Domain → Range
Each input x maps to exactly one output f(x)
```

**Examples table:**

| Function | Domain | Range | Rule |
|---|---|---|---|
| Celsius → Fahrenheit | temperatures in °C | temperatures in °F | F = 9C/5 + 32 |
| Score → Grade | 0–100 | {A,B,C,F} | bands |
| user_id → email | valid user IDs | email strings | lookup table |
| Pincode → city | 6-digit pincodes | city names | lookup (ideal) |

**Ask:** *"Can one score map to both B and A?"* → Not a function — ambiguous

**Say:** *"Python might not stop you from bad logic — but specs and tests should enforce one output per input."*

### Python Function Preview (5 min)

```python
def celsius_to_fahrenheit(c):
    return c * 9 / 5 + 32

print(celsius_to_fahrenheit(0))
print(celsius_to_fahrenheit(38))
```

**Output:**
```
32.0
100.4
```

**Break it down:**
- `c` is input from domain (a Celsius value)
- `return` sends one output to range (Fahrenheit)
- 0°C → water freeze point 32°F; 38°C → body temp ~100.4°F

**Ask:** *"What is the domain if we only accept non-negative temps?"* → c >= 0 — validation can enforce domain

**Common mistake:** Function prints sometimes A, sometimes B for same input — breaks math function rule and makes testing hard

### Grade Function — Domain, Range, Boundaries (5 min)

```python
def grade(score):
    if score >= 90:
        return "A"
    elif score >= 75:
        return "B"
    elif score >= 60:
        return "C"
    else:
        return "F"

for s in [59, 60, 74, 75, 89, 90, 100]:
    print(s, "->", grade(s))
```

**Output:**
```
59 -> F
60 -> C
74 -> C
75 -> B
89 -> B
90 -> A
100 -> A
```

**Break it down:**
- Domain: scores 0–100 (inputs)
- Range: {A, B, C, F} (outputs)
- `elif` chain picks exactly one grade per score

**Ask:** *"Where is the boundary risk?"* → Scores exactly at 60, 75, 90 — tie to careful `>=` from Session 3

**Common mistake:** Using `>` instead of `>=` at boundary — score 60 might fall through wrong

**Say:** *"Session 6 is coding-heavy again. You will name machines, pass parameters, and return — today you understand **why** one input should give one clear output."*

### Number Systems — Brief Board Tour (5 min)

**Three systems:**

| System | Base | Digits | Typical use |
|---|---|---|---|
| Decimal | 10 | 0–9 | Prices in INR, ages |
| Binary | 2 | 0, 1 | Memory, True/False as 1/0 |
| Hexadecimal | 16 | 0–9, A–F | Colour codes, memory dumps |

**Quick conversion on board:** binary `101` = 1×4 + 0×2 + 1×1 = **5** decimal

```python
# Python can convert bases — verification only
print(int("101", 2))
print(hex(255))
```

**Output:**
```
5
0xff
```

**Break it down:**
- `int("101", 2)` reads 101 as binary → 5 decimal
- `hex(255)` shows hex form of 255 → useful for colours like `#FF0000`

**Ask:** *"Do data analysts convert binary daily?"* → Rarely; know that data is bits underneath

**Say:** *"Floats can surprise you: `0.1 + 0.2` may not equal `0.3` exactly. For money, teams often store paise as integers."*

```python
print(0.1 + 0.2)
print(0.1 + 0.2 == 0.3)
```

**Output:**
```
0.30000000000000004
False
```

**Break it down:**
- Binary fractions cannot represent all decimals exactly
- Comparison fails — use rounding or integer paise for INR

**Common mistake:** Using `==` on floats for money — compare with tolerance or use integers

### Composition Preview (optional if time)

```python
def add_gst(price_inr):
    return price_inr * 1.18

def format_bill(price_inr):
    total = add_gst(price_inr)
    return f"Total: ₹{total:.2f}"

print(format_bill(1000))
```

**Output:**
```
Total: ₹1180.00
```

**Break it down:**
- `format_bill` calls `add_gst` — output of one feeds input of next
- Math composition: h(x) = f(g(x))

**Ask:** *"What is the domain of `add_gst`?"* → Sensible prices (positive numbers)

---

## SEGMENT 8: Quiz, Homework, FAQ & Wrap (15 min)

### Session Recap Table (3 min)

| Topic | Key idea | Python / tool link |
|---|---|---|
| Binary / Boolean | Two states 0/1, True/False | `bool`, comparisons |
| Truth tables | All combinations, no guess | `and`, `or`, `not` |
| De Morgan | Flip negated AND/OR groups | Parentheses + rewrite |
| Sets / Venn | Union, intersection, difference | `set`, `|`, `&`, `-` |
| Functions | Domain → one output in range | `def`, `return` (Session 6) |
| Number systems | Decimal, binary, hex | `int(x, 2)`, float caveats |
| Filter logic | Row-wise boolean mask | SQL `WHERE`, Pandas later |

**Bridge to next session:** *"Session 6 is coding-heavy. You will write **functions** — recipe cards that implement the mappings we drew today. Bring your grade function sketch; we refactor messy scripts into clean, reusable pieces."*

### Quiz — 10 Questions (7 min)

*Instructor: read aloud or show slide; students answer on paper. Review answers aloud.*

**Q1.** How many rows in a truth table with two variables A and B?  
**Answer:** 4

**Q2.** `A=True`, `B=False`. What is `A and B`?  
**Answer:** False

**Q3.** `A=True`, `B=False`. What is `A or B`?  
**Answer:** True

**Q4.** Simplify `NOT (A AND B)` using De Morgan.  
**Answer:** `(NOT A) OR (NOT B)`

**Q5.** `NOT (A OR B)` equals what De Morgan form?  
**Answer:** `(NOT A) AND (NOT B)`

**Q6.** Set A = {1,2,3}, B = {3,4}. What is A ∩ B?  
**Answer:** {3}

**Q7.** Same sets — what is A ∪ B?  
**Answer:** {1, 2, 3, 4}

**Q8.** In math, a function must give how many outputs per valid input?  
**Answer:** Exactly one

**Q9.** Binary `101` equals what decimal number?  
**Answer:** 5

**Q10.** SQL `WHERE city = 'Mumbai' AND amount >= 500` keeps a row only when —?  
**Answer:** Both conditions are True (city is Mumbai and amount is at least 500)

**Ask:** *"Which question was hardest — truth tables, De Morgan, or sets?"* — adjust review accordingly.

### Homework (2 min)

**Assign on slide — no laptop required unless students want to verify:**

1. **Truth table:** Complete all 8 rows for `(P or Q) and not R` with columns P, Q, R, P or Q, not R, final result.

2. **De Morgan:** Rewrite `NOT (paid OR refunded)` in equivalent form. Give one example transaction that matches the filter.

3. **Venn:** |A only| = 50, |B only| = 30, |A ∩ B| = 20. Find |A ∪ B|. Draw and label regions.

4. **Functions:** For `discount_eligible(age, is_member)` where rule is age >= 18 AND member, write domain, range, and a 4-row truth table (use age buckets `<18` and `>=18`).

5. **Reflection (one paragraph):** How is a Python dict like a function from keys to values? Use an example with Indian pincode → city.

**Optional Python verify:** Implement `grade(score)` from today's demo and test boundaries 59, 60, 89, 90.

### FAQ — Instructor Reference (use during Q&A)

**Q1: Do I need to memorize truth tables?**  
→ Memorize rules for AND/OR/NOT; derive tables when unsure. Four rows for two variables is quick.

**Q2: When do I use a set vs a list?**  
→ List when order and duplicates matter. Set when you only care about unique membership or fast `in` checks.

**Q3: Is every Python function a math function?**  
→ Mathematically, only if each input maps to one well-defined output. Good functions behave that way even when Python allows side effects.

**Q4: How does this connect to ML?**  
→ Features are numbers; labels are categories; decision trees split on boolean conditions (`feature <= 5`). Same logic, larger scale.

**Q5: Why learn De Morgan if Python runs both forms?**  
→ Readable specs, fewer bugs in negated dashboard filters, and common interview question.

**Q6: Do I need binary conversion for data jobs?**  
→ Rarely day to day. Know True/False as 1/0 and that floats are approximate — especially for money.

**Q7: How is SQL related if we learn Python?**  
→ SQL filters rows with AND/OR/NOT — same truth tables. Pandas `.loc` and SQL `WHERE` are parallel skills.

**Q8: What if I still fear math?**  
→ You already used this math in Session 3. Today we label it. Naming fear reduces it.

**Q9: Can a dict have duplicate keys?**  
→ No — later key overwrites earlier. That enforces one value per key, like a function.

**Q10: What's the difference between `==` and `=`?**  
→ `=` assigns a value; `==` compares and gives True/False.

### Closing (3 min)

**Say:** *"You did not learn a new programming language today. You learned the language your programs already speak — yes/no, sets, mappings. Session 6 turns grade rules and GST helpers into reusable functions. Sessions 10+ apply the same AND/OR to thousands of rows. One story, new notation each time."*

**Final board line:**

```
Math = naming what your Python already does
```

---

## Instructor Notes

### Room Setup
- Whiteboard markers in **three colours** for Venn regions (A only, B only, overlap)
- True/False cards optional for AND vs OR kinesthetic demo (reuse from Session 3)
- Print **blank 4-row truth table template** for each student
- Slide with Mental Map from pre-read for optional 1-min recap

### Pacing Guidance
- **Core — do not rush:** Truth tables (SEGMENT 2) and De Morgan (SEGMENT 4). These unlock filters and interviews.
- **Trim if behind:** Number systems demo in SEGMENT 7 (keep decimal/binary `101` example only); optional composition GST example
- **Extend if ahead:** Eight-row truth table for three variables; extra Venn numeric problem from homework

### Pedagogy
- **Minimal coding:** If students open laptops too early, redirect: *"Board first, verify in Python second."*
- **Sensitivity:** Avoid *"you must love math"* framing — use *"you already used this in Python."*
- **Participation:** Pair work for truth tables and Venn counts; cold-call one row per table to keep attention
- **Indian context:** Swiggy/Zomato filters, Mumbai metro, IPL fan sets, INR/GST, pincode lookups — rotate examples to match class region

### Common Student Struggles
| Struggle | Response |
|---|---|
| AND vs OR confusion | Use picky vs generous hooks; one concrete food-order example each |
| Forgetting parentheses with NOT | Write `not (a and b)` vs `not a and b` side by side with truth values |
| Venn double-counting | Always write formula `|A|+|B|−|∩|` on board |
| Domain vs range swapped | Domain = inputs you allow in; range = outputs that can come out |
| "When will I use sets?" | Unique users, tags, duplicate removal — name Pandas `drop_duplicates` |

### Materials Checklist
- [ ] Truth table handout (4-row and 8-row blank)
- [ ] Venn activity slide with |A only|, |B only|, |∩| counts
- [ ] Quiz answer key for instructor
- [ ] Homework slide or LMS post
- [ ] Pre-read link: Numbers, Logic & Structure

### Connections Forward (name-drop only — no depth today)
- **Session 6:** `def`, `return`, scope — implement today's mappings
- **Session 8:** JSON dicts as maps on the wire
- **Session 10–11:** Pandas boolean indexing, `df[condition]`
- **SQL modules:** `WHERE`, `JOIN` as set operations
- **Classical ML:** decision tree splits as boolean tests on features

### Assessment Signals
- Student can fill 4-row AND table without help → ready for filters
- Student simplifies one De Morgan expression → ready for dashboard specs
- Student computes |A ∪ B| from three region counts → ready for SQL joins intuition
- Student states domain and range for grade function → ready for Session 6 functions

---

## Q&A & Doubt Solving (overflow from SEGMENT 8)

*Use if class needs extra time after quiz or homework review.*

**Likely live-coding doubt — operator precedence:**

```python
# What prints?
print(not False and True)
print(not (False and True))
```

**Output:**
```
True
True
```

**Break it down:**
- First: `not False` → True; `True and True` → True
- Second: `False and True` → False; `not False` → True
- Same result here — but parentheses matter in other cases

**Common mistake:** Assuming `not` binds the whole expression without parentheses

**Likely doubt — empty set edge case:**

```python
A = {1, 2, 3}
B = set()
print(A & B)
print(A | B)
```

**Output:**
```
set()
{1, 2, 3}
```

**Break it down:**
- Intersection with empty set is empty
- Union with empty set leaves A unchanged

**Ask:** *"If no one is in both campaigns, what is |A ∩ B|?"* → 0 — formula still works

---

*End of Lecture Script — Session 5: Master Class — Numbers, Logic & Structure*
