# Lecture Script: Foundations of Data — Python Fundamentals
> **Instructor Reference** — Module 1: Foundations of Data | Academic Session 2 | Duration: 2 Hours | Instructor: [Industry Mentor / Name Placeholder]

---

## Session Overview
**Goal:** By the end, students can declare correctly-typed variables, build expressions using arithmetic and comparison operators, and write a complete input-to-output Python program using f-strings — with disciplined, top-to-bottom notebook habits.

**Student profile at this point:** Has a working VS Code + Colab + Git setup from Session 1, and can distinguish AI/ML/GenAI. No prior programming experience assumed. Likely wrong assumption: that Python "just knows" what type of value they meant (e.g., expecting `input()` to return a number automatically). Boredom risk is low, but frustration risk is high the first time a type error appears.

**Key outcome:** Students should leave with the instinct to ask, before writing any line: *"What type of value is this, and what am I allowed to do with it?"*

> 🎯 **The one sentence this session must land:** *Every value in Python has a type, and that type decides what you're allowed to do with it — get the type wrong, and the operation breaks.*

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| Opening — "The ₹5 That Wasn't a Number" | 8 min | 8 min |
| Concept + Practical Block 1: Variables & Data Types | 25 min | 33 min |
| Concept + Practical Block 2: Operators | 22 min | 55 min |
| ☕ BREAK | 5 min | 60 min |
| Concept + Practical Block 3: Input, Output & f-strings | 25 min | 85 min |
| Concept + Practical Block 4: Notebook Discipline in Colab | 15 min | 100 min |
| Summary & Bridge | 5 min | 105 min |
| Q&A & Doubt Solving | 15 min | 120 min |

---

## Opening — "The ₹5 That Wasn't a Number" (8 min)

Type this live in Colab, in front of the room:
```python
price = input("Enter the price: ")
total = price + 5
```
Type `5` when prompted. Let it crash with a `TypeError`.

> "I typed the number 5. Python is telling me I can't add 5 to it. Why? Because as far as Python is concerned, I didn't type the *number* 5 — I typed the *text* '5'. And you can't do arithmetic on text. This one distinction — what TYPE of value you're holding — is going to explain almost every confusing error you hit for the next few weeks."

[Pause — let them sit with the error message on screen.]

> "Everything in Python has a type. Today you'll learn the four basic types, how to combine values with operators, how to talk to your program with input and output, and the habits that keep your code working reliably every single time you run it — not just the first time."

Pivot line: "Let's fix that error properly — starting with what a variable and a type actually are."

---

## Concept + Practical Block 1: Variables & Data Types (25 min)

### "Every kirana shop shelf holds one kind of thing"
> "Picture your local kirana shop. The rice shelf holds rice. The oil shelf holds oil. You wouldn't put loose rice on the oil shelf. A variable in Python works the same way — it's a labeled shelf, and the type of value tells you what belongs on it."

Build this table live, one row at a time, asking students to guess the type before you reveal it:

| Type | Example | Looks like |
|---|---|---|
| `int` | Number of items in a cart | `5` |
| `float` | Price with paise | `49.50` |
| `str` | A name or message | `"Priya"` |
| `bool` | Is the order paid? | `True` |

**Hands-on (live-coded together):**
```python
item_count = 3
price_per_item = 49.5
customer_name = "Priya"
is_paid = True
print(type(item_count), type(price_per_item), type(customer_name), type(is_paid))
```

**Answer key / reasoning to say aloud:** Walk through why `type()` printed `<class 'int'>` etc. — connect the printed class name back to the table on the board.

### 🔴 The trap / highest-value moment
Write on the board: **"`"5"` is not the same as `5`. Quotes mean text, no quotes means number."**

> "This single distinction is behind the crash we saw in the opening. Write it down."

💬 **Expect an argument about:** "Why does Python care so much — other languages/Excel just figure it out?" Welcome it. Say: *"Python is being strict on purpose — it's catching a mistake for you before it becomes a much harder bug to find later, in a 500-line program instead of a 5-line one."*

---

## Concept + Practical Block 2: Operators (22 min)

### "The scoreboard doesn't just add — sometimes it compares"
> "A cricket scoreboard does two different jobs. Adding runs after every ball — that's arithmetic. Checking 'is Team A ahead of Team B' — that's comparison. It gives you True or False, not a new number."

Build table live:

| Category | Operator | Meaning | Example | Result |
|---|---|---|---|---|
| Arithmetic | `+ - * /` | Basic maths | `10 + 3` | `13` |
| Arithmetic | `//` | Floor division | `10 // 3` | `3` |
| Arithmetic | `%` | Remainder | `10 % 3` | `1` |
| Comparison | `==` | Equal to | `5 == 5` | `True` |
| Comparison | `> <` | Greater/less than | `7 > 4` | `True` |

**Hands-on:**
```python
home_score = 184
away_score = 179
run_difference = home_score - away_score
home_won = home_score > away_score
print(run_difference, home_won)
```

**Answer key / reasoning to say aloud:** `run_difference` is `5` — a new int produced by subtraction. `home_won` is `True` — not a new number, but a judgment about the two numbers.

### 🔴 The trap / highest-value moment
Write on the board: **"`=` puts a value in a box. `==` asks if two values are equal. Never confuse them."**

💬 **Expect an argument about:** "Why does `10 / 3` give a decimal but `10 // 3` doesn't?" Welcome it. Say: *"`/` always gives you the precise decimal answer. `//` throws away the decimal part on purpose — useful when you want, say, 'how many full teams of 3 fit into 10 people,' where a fractional team doesn't make sense."*

---

## ☕ BREAK (5 min)

---

## Concept + Practical Block 3: Input, Output & f-strings (25 min)

### "Taking the order, handing back the receipt"
> "At a café counter, you ask the customer what they want — that's `input()`. Then you hand back a receipt with their order woven into it — that's a `print()` with an f-string."

**Hands-on, built live, line by line:**
```python
name = input("What's your name? ")
item_count = int(input("How many items? "))
price = 49.5
total = item_count * price
print(f"Hi {name}, your total for {item_count} items is ₹{total}")
```

Pause after the second line specifically:
> "Why did I wrap `input()` in `int()` this time, but not for the name? Because `input()` ALWAYS gives you text back — even if the user types a number. If I want to do maths with it, I have to convert it myself."

**Answer key / reasoning to say aloud:** Walk through what happens if a student forgets the `int()` conversion — recreate the opening's crash deliberately here so the fix "clicks" as the direct solution to the problem posed at the start of class.

### 🔴 The trap / highest-value moment
Write on the board: **"Forgetting the `f` before the quotes means Python prints `{name}` literally, not the value inside it."**

Demonstrate live: remove the `f` from the print statement and show the broken output.

💬 **Expect an argument about:** "Why not just use `+` to join strings together instead of f-strings?" Welcome it. Say: *"You can — but the moment you're mixing numbers and text, like our ₹ total, `+` forces you to convert every single value to text manually. f-strings do that for you automatically and read more like a normal sentence."*

---

## Concept + Practical Block 4: Notebook Discipline in Colab (15 min)

### "Following the recipe book in order"
> "A recipe only works if you follow the steps in order. Run step 5 before step 3, and dinner goes wrong — even though every step was written correctly. Colab cells work the same way."

**Live demonstration (deliberately break it to make the point):**
1. Define `price = 49.5` in a later cell.
2. Go back and re-run an earlier cell that uses `price`, without re-running the later cell first.
3. Show that Colab still remembers the *old* value — a classic "it worked a second ago" bug.

> "This is exactly why, before you submit or share any notebook, you do one thing: Runtime → Restart runtime and run all. If it still works top to bottom with a clean slate, you know it's actually correct — not just correct by accident of click order."

### 🔴 The trap / highest-value moment
Write on the board: **"Before submitting: Restart runtime and run all. Every time."**

💬 **Expect an argument about:** "This seems like an extra step for nothing — my code already ran fine." Welcome it. Say: *"It ran fine in the order YOU happened to click it. Your instructor, and later your teammates, will run it fresh from the top — and that's the only order that has to work."*

---

## Summary & Bridge (5 min)

| Concept | The one thing to remember |
|---|---|
| Variables & data types | Every value has a type, and the type decides what you can do with it |
| Operators | Arithmetic makes new values; comparison makes True/False judgments |
| Input, output, f-strings | `input()` always returns text; f-strings weave variables into readable output |
| Notebook discipline | Restart runtime and run all before you trust or submit any notebook |

Close on the thesis: *"Every value in Python has a type, and that type decides what you're allowed to do with it — get the type wrong, and the operation breaks."*

Bridge: "So far your programs only calculate. Next session, you'll teach them to make decisions — choosing what to do based on a condition — in **Control Flow & Decision Making**."

---

## Q&A & Doubt Solving (15 min)

**Q: Why does `input()` always return text, even for numbers?**
→ Python has no way to know in advance whether you'll type a number, a name, or a sentence — so it plays it safe and gives you text every time, letting you convert it explicitly when you need to.

**Q: What's the difference between `float` and `int` if both can technically store numbers?**
→ `int` stores whole numbers only; `float` stores numbers with decimal points — trying to store `49.5` as an `int` would either error or lose the decimal, depending on how you convert it.

**Q: Can I use f-strings with numbers, not just text?**
→ Yes — f-strings can embed any variable, regardless of type, directly inside `{}`, and Python converts it to readable text automatically.

**Q: Why did my code work the first time I ran it, but break the second time?**
→ Almost always a notebook-order issue — a variable was defined in a cell you didn't re-run, so Colab used a stale value; "Restart runtime and run all" catches this every time.

**Q: Is `==` the same as `=` in maths class where we use one `=` sign for everything?**
→ No — this is a common source of bugs precisely because maths class trains you to see one symbol for both ideas; in Python, `=` assigns and `==` compares, and mixing them causes real errors.

**Q: Do I need to memorize all the operators today?**
→ No — focus on recognizing the difference between arithmetic (produces a new value) and comparison (produces True/False); the exact symbols become second nature through repetition over the next few sessions.

---

## Instructor Notes
- **Words not yet earned — avoid using without defining:** "type casting," "type coercion," "mutable," "immutable." These get formalized properly in Session 3.3 (Python Data Structures).
- **Biggest risk this session:** frustration at the first `TypeError` — normalize it explicitly by naming it in the opening hook as the exact thing they'll learn to prevent, not an embarrassing mistake.
- **Board management:** Keep the four-type table (`int`, `float`, `str`, `bool`) visible on the board or a pinned slide for the entire session — nearly every later block refers back to it.
- **Common confusions, numbered:**
  1. Believing `input()` returns a number when the user types digits.
  2. Confusing `=` (assignment) with `==` (comparison).
  3. Forgetting the `f` before an f-string's quotes and not understanding why `{name}` printed literally.
- **Cross-references to later sessions:** Type discipline here directly sets up Control Flow (2.1), where comparison operators become the backbone of every `if` statement; f-string formatting resurfaces constantly in Pandas output (Sessions 5.1–5.2) and Data Visualization (6.2) labels.
- **Local/cultural context notes:** Kirana shop shelves, cricket scoreboards, café ordering, and ₹ totals continue as running analogies from Session 1 — keep them consistent so students recognize the pattern rather than learning a new metaphor every session.
