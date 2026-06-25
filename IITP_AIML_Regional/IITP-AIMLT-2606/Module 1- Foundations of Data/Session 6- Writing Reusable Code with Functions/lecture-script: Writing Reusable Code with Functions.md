# Lecture Script: Writing Reusable Code with Functions (2 Hours)

> **Instructor Reference** — Module 1: Foundations of Data | Session 6 | Duration: 2 Hours

---

## Session Overview

**Duration**: 2 hours (105 min teaching + 5 min break + 10 min quiz buffer)

**Goal:** Students define functions with parameters and return values, understand local vs global scope, use default arguments, preview docstrings and `*args`/`**kwargs`, and refactor a duplicated order-total script into modular functions.

**Student profile at this point:** Comfortable with variables, conditionals, and loops from Sessions 2–4. Attended the math master class (Session 5) linking domain/range to functions. May copy-paste code blocks instead of abstracting.

**Key outcome:** Every student refactors a ~40-line order-total script into `calc_subtotal`, `calc_tax`, and `calc_total` (plus optional helpers), and can explain why a variable inside a function is invisible outside it.

**Today's Promise:** "By the end, you will turn messy duplicated order code into clean, testable functions — the same pattern every data pipeline uses."

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| SEGMENT 1: Opening & Hook | 8 min | 0:08 |
| SEGMENT 2: def, Call, return | 15 min | 0:23 |
| SEGMENT 3: Parameters, Scope & print vs return | 15 min | 0:38 |
| SEGMENT 4: Default Arguments | 12 min | 0:50 |
| **BREAK** | 10 min | 1:00 |
| SEGMENT 5: Small Functions Lab | 15 min | 1:15 |
| SEGMENT 6: Modularity, Docstrings & *args/**kwargs | 12 min | 1:27 |
| SEGMENT 7: Refactor Order-Total Capstone | 20 min | 1:47 |
| SEGMENT 8: Common Mistakes & Wrap | 8 min | 1:55 |
| Quiz + Q&A buffer | 5 min | 2:00 |

---

## SEGMENT 1: Opening & Hook (8 min)

### Hook (3 min)

**Ask**: "How many of you have copy-pasted the same block of code and changed only variable names?" [Hands go up]

**Show on screen:**

```python
# Order 1
items1 = [100, 250, 80]
subtotal1 = 0
for p in items1:
    subtotal1 += p
tax1 = subtotal1 * 0.18
total1 = subtotal1 + tax1
print("Order 1 total:", total1)

# Order 2 — same logic copy-pasted
items2 = [50, 50, 200]
subtotal2 = 0
for p in items2:
    subtotal2 += p
tax2 = subtotal2 * 0.18
total2 = subtotal2 + tax2
print("Order 2 total:", total2)
```

**Ask**: "Tax rate changes to 12%. How many lines do you edit? What if you have 500 orders?"

**Reveal**: "Today you learn **functions** — name a job once, call it many times, fix bugs in one place. This is how every Pandas helper and API client is built."

### Why This Matters (5 min)

**Connect**: "Last session you traced loops and conditionals. Today we **package** that logic under names like `calc_subtotal` and `calc_tax`."

| Without functions | With functions |
|---|---|
| Same logic repeated N times | One definition, N calls |
| Fix bugs in many places | Fix once |
| Script reads like a long story | Script reads like a table of contents |

**Learning contract for today:**
- Write `def` with parameters and `return`
- Predict scope errors before they happen
- Use default arguments where sensible
- Refactor duplicated order logic into reusable functions

**Say**: "One function, one job. Name it so a teammate knows what it does without reading every line."

---

## SEGMENT 2: def, Call, return (15 min)

### What is a Function? (4 min)

**Say**: "A function is a named recipe. You **define** it once with `def`. You **call** it whenever you need that job done."

**Show**:

```python
def greet(name):
    return f"Hello, {name}"

message = greet("Anita")
print(message)
```

Output:

```
Hello, Anita
```

**Break it down**:
- `def greet(name):` — defines a function named `greet` with one parameter `name`
- `return f"Hello, {name}"` — sends the string back to the caller
- `greet("Anita")` — **call** with argument `"Anita"`
- `message = ...` — stores the returned value

**Ask**: "What are the parameter and the argument in this example?" → Parameter: `name`. Argument: `"Anita"`.

**Common mistake**: Forgetting the colon after `def greet(name)` — Python expects `:` before the indented body.

### Function with Multiple Parameters (5 min)

**Show**:

```python
def rectangle_area(width, height):
    area = width * height
    return area

print(rectangle_area(4, 7))
print(rectangle_area(10, 3))
```

Output:

```
28
30
```

**Break it down**:
- `width` and `height` are **parameters** — placeholders for values
- `4, 7` and `10, 3` are **arguments** — actual values at call time
- `area` is a **local** variable — exists only inside the function
- `return area` sends the result to whoever called the function

**Ask**: "If I call `rectangle_area(7, 4)`, do I get the same result as `rectangle_area(4, 7)`?" → Yes for multiplication; not always for subtraction — order matters for some operations.

**Common mistake**: Swapping argument order when parameters are not commutative — `subtract(a, b)` is not the same as `subtract(b, a)`.

### return Stops the Function (6 min)

**Show**:

```python
def absolute_diff(a, b):
    if a >= b:
        return a - b
    return b - a

print(absolute_diff(3, 10))
print(absolute_diff(10, 3))
```

Output:

```
7
7
```

**Break it down**:
- First `return` runs when `a >= b` — function **ends immediately**
- Second `return` runs only when the first did not — link to Session 3 branching
- Both calls return `7` — the function handles order for us

**Ask**: "After a `return` runs, does code below it in the same function still execute?" → No.

**Common mistake**: Putting code after `return` expecting it to run — dead code after return is unreachable.

### print vs return — Critical Distinction (included in segment)

**Show**:

```python
def broken_double(n):
    print(n * 2)

def good_double(n):
    return n * 2

x = broken_double(5)
print("x is:", x)

y = good_double(5)
print("y is:", y)
```

Output:

```
10
x is: None
y is: 10
```

**Break it down**:
- `print` **displays** on screen — it does not send a value to the caller
- A function with no `return` gives the caller `None`
- `good_double` returns `10`, which can be used in `total = price + good_double(fee)`

**Ask**: "Which function can you use inside `total = 100 + double(5)`?" → Only one that **returns** a number.

**Common mistake**: Using `print` inside a calculation function and wondering why the result is `None`.

**Student try**: Write `celsius_to_fahrenheit(c)` that returns `(c * 9/5) + 32`. Test with `0` and `100`. **(2 min)**

---

## SEGMENT 3: Parameters, Scope & print vs return (15 min)

### Parameters vs Arguments Vocabulary (4 min)

**Say**: "Professionals use precise words. Mixing them up is fine in conversation, but exams and docs use these terms."

| Term | Where | Example |
|---|---|---|
| Parameter | In `def` line | `price`, `pct` |
| Argument | In call | `100`, `15` |
| Return value | What caller gets | `85.0` |
| Caller | Code that invokes | `main` section |

**Show — positional and keyword arguments**:

```python
def discounted(price, pct):
    return price * (1 - pct / 100)

print(discounted(100, 10))
print(discounted(price=100, pct=10))
print(discounted(100, pct=25))
```

Output:

```
90.0
90.0
75.0
```

**Break it down**:
- Positional: first arg → first parameter
- Keyword: name the parameter at call site — order flexible
- Same math, three valid call styles

**Ask**: "When might keyword arguments help?" → Many parameters, or skipping optional ones later.

**Common mistake**: Keyword arguments before positional ones in a call — `discounted(price=100, 10)` can error; positional args must come first.

### Local Scope — Variables Inside Functions (6 min)

**Show**:

```python
def add_ten(x):
    x = x + 10
    return x

num = 5
result = add_ten(num)
print("result:", result)
print("num:", num)
```

Output:

```
result: 15
num: 5
```

**Break it down**:
- `x` is a **parameter** — local to `add_ten`
- Changing `x` inside the function does not change `num` in the caller
- `return` sends the new value back; caller must assign if it wants to keep it

**Ask**: "Did `num` change in the outer script?" → No — still `5`.

**Common mistake**: Expecting parameters to automatically update global variables with the same name.

### NameError — Using Local Names Outside (5 min)

**Show**:

```python
def calc_tax(amount):
    tax = amount * 0.18
    return tax

calc_tax(1000)
# print(tax)   # uncomment to demo NameError
```

Output (if uncommented):

```
NameError: name 'tax' is not defined
```

**Break it down**:
- `tax` exists only inside `calc_tax`
- The caller receives the **return value**, not access to internal names
- Fix: `tax_amount = calc_tax(1000)` then `print(tax_amount)`

**Ask**: "How do you get the tax value outside the function?" → Assign the return: `tax_amount = calc_tax(1000)`.

**Common mistake**: Defining a variable inside a function and using it outside without returning it.

### Reading Globals vs Passing Parameters (bonus in segment)

**Show**:

```python
TAX_RATE = 0.18

def calc_tax(amount):
    return amount * TAX_RATE

print(calc_tax(1000))
```

Output:

```
180.0
```

**Break it down**:
- `TAX_RATE` is **global** — defined at module level
- Reading a constant global is common for beginners
- Better style for larger projects: pass `tax_rate` as a parameter

**Ask**: "What happens if GST changes?" → Edit `TAX_RATE` once, or pass new rate as argument.

**Common mistake**: **Assigning** to a global name inside a function without `global` keyword — creates a new local instead. Prefer parameters.

**Write on board:** **Pass in → return out → avoid hidden globals**

---

## SEGMENT 4: Default Arguments (12 min)

### Syntax and Rules (5 min)

**Say**: "Default arguments let callers skip parameters they usually leave unchanged — like a coffee that defaults to medium size."

**Show**:

```python
def power(base, exponent=2):
    return base ** exponent

print(power(5))
print(power(5, 3))
print(power(2, 10))
```

Output:

```
25
125
1024
```

**Break it down**:
- `exponent=2` is a **default** — used when caller omits second argument
- `power(5)` → exponent becomes `2` → `25`
- `power(5, 3)` → explicit `3` overrides default

**Ask**: "What is `power(3)`?" → `9` (3 squared).

**Common mistake**: Putting default parameters **before** non-default ones — `def bad(a=1, b):` is a SyntaxError.

### greet with Default Punctuation (4 min)

**Show**:

```python
def greet(name, punct="!"):
    return f"Hello, {name}{punct}"

print(greet("Ria"))
print(greet("Ria", "?"))
```

Output:

```
Hello, Ria!
Hello, Ria?
```

**Break it down**:
- `punct="!"` — optional styling parameter
- One function handles both common and special cases
- Non-default `name` must come first

**Ask**: "Why must `name` come before `punct`?" → Parameters without defaults must precede those with defaults.

**Common mistake**: `def greet(punct="!", name)` — invalid parameter order.

### discounted with Default pct (3 min)

**Show**:

```python
def discounted(price, pct=10):
    return price * (1 - pct / 100)

print(discounted(100))
print(discounted(100, 25))
```

Output:

```
90.0
75.0
```

**Break it down**:
- Default `pct=10` matches "most items get 10% off"
- Override with second argument for sales events
- Same pattern you will use in the order capstone for `tax_rate`

**Ask**: "What does `discounted(200)` return?" → `180.0`.

**Common mistake**: Mutable default `def f(items=[])` — mention only; same list reused across calls. Use `None` and create inside for advanced work.

**Student try**: Add `currency="INR"` default to a `format_price(amount, currency="INR")` function. **(2 min)**

---

## — 10-MINUTE BREAK —

*Break prompt:* Sketch three function names for an order pipeline — no bodies required.

---

## SEGMENT 5: Small Functions Lab (15 min)

**Say**: "These three tasks match your coding problem. Work 8 minutes solo, then we review together."

### Lab Task 1 — double(n) (4 min)

**Show**:

```python
def double(n):
    return n * 2

print(double(7))
```

Output:

```
14
```

**Break it down**:
- One parameter, one return — simplest useful function
- Caller can use result in larger expressions: `double(3) + double(4)`

**Ask**: "What does `double(0)` return?" → `0`.

**Common mistake**: Using `print(n * 2)` instead of `return` — caller gets `None`.

### Lab Task 2 — discounted(price, pct=10) (5 min)

**Show**:

```python
def discounted(price, pct=10):
    return price * (1 - pct / 100)

print(discounted(100))
print(discounted(100, 25))
```

Output:

```
90.0
75.0
```

**Break it down**:
- Combines return + default argument from today
- Formula: price minus percentage off
- Second call overrides default discount

**Ask**: "What is `discounted(200, 50)`?" → `100.0` (half price).

**Common mistake**: Dividing by 100 twice — `pct` is already a percent (10 means 10%, not 0.10).

### Lab Task 3 — summary(name, scores) (6 min)

**Show**:

```python
def summary(name, scores):
    total = 0
    for s in scores:
        total += s
    average = total / len(scores)
    return average

name = "Ria"
scores = [80, 90, 70]
avg = summary(name, scores)
print(f"{name} avg: {avg}")
```

Output:

```
Ria avg: 80.0
```

**Break it down**:
- Function body uses a **loop** (Session 4) — functions can contain any logic
- `return average` sends one number back
- f-string formats output in the **caller**, not inside `summary`

**Ask**: "Could you use `sum(scores)` instead of the loop?" → Yes — `return sum(scores) / len(scores)`.

**Common mistake**: Empty `scores` list causes division by zero — mention guard `if len(scores) == 0: return 0` for robustness.

**Quick test table on board:**

| Call | Expected |
|---|---|
| `double(0)` | 0 |
| `discounted(200, 50)` | 100.0 |
| `summary("Jo", [100])` | 100.0 |

---

## SEGMENT 6: Modularity, Docstrings & *args/**kwargs (12 min)

### Refactoring Strategy (4 min)

**Say**: "Modularity means one function, one job. Refactoring improves structure without changing behaviour."

| Step | Action |
|---|---|
| 1 | Find repeated blocks |
| 2 | Name the job in plain English |
| 3 | Extract `def` with parameters |
| 4 | `return` one clear result |
| 5 | Replace old blocks with calls |
| 6 | Test with known numbers |

**Target function set for order lab:**

| Function | Parameters | Returns |
|---|---|---|
| `calc_subtotal` | `items` | float |
| `calc_tax` | `subtotal`, `tax_rate=0.18` | float |
| `calc_total` | `subtotal`, `tax` | float |
| `format_order_line` | `order_id`, `subtotal`, `tax`, `total` | str |

**Ask**: "Why separate `calc_tax` from `calc_total`?" → Each can be tested and changed independently.

**Common mistake**: One giant function that prints, computes tax, and saves to file — three jobs, should be three functions.

### Docstrings Preview (4 min)

**Show**:

```python
def calc_tax(amount, tax_rate=0.18):
    """Return tax amount for a given subtotal and rate."""
    return amount * tax_rate

help(calc_tax)
```

Output (abbreviated):

```
Help on function calc_tax in module __main__:
    calc_tax(amount, tax_rate=0.18)
    Return tax amount for a given subtotal and rate.
```

**Break it down**:
- Triple-quoted string immediately under `def` is a **docstring**
- `help()` displays it in notebooks and REPL
- One clear sentence is enough today

**Ask**: "Who reads docstrings besides you?" → Teammates, future you, `help()` users.

**Common mistake**: Docstring outside the function or after other statements — must be first statement in body.

### *args and **kwargs Preview (4 min)

**Show — *args**:

```python
def show_total(label, *amounts):
    return f"{label}: {sum(amounts)}"

print(show_total("Cart", 100, 250, 80))
```

Output:

```
Cart: 430
```

**Break it down**:
- `*amounts` collects extra positional arguments into a **tuple**
- `sum(amounts)` works on any number of prices
- You will **read** this pattern in library code more than write it today

**Show — **kwargs**:

```python
def build_profile(name, **details):
    profile = {"name": name}
    profile.update(details)
    return profile

print(build_profile("Ria", city="Pune", score=88))
```

Output:

```
{'name': 'Ria', 'city': 'Pune', 'score': 88}
```

**Break it down**:
- `**details` collects extra keyword arguments into a **dict**
- Common in APIs: `pd.read_csv(path, sep=";", encoding="utf-8")`
- Focus today on named parameters; revisit when reading docs

**Ask**: "Why do libraries need flexible parameters?" → Many optional settings — plotting, CSV parsing, model configs.

**Common mistake**: Confusing `*args` with multiplication `*` — in a parameter list, `*` means "collect extras."

---

## SEGMENT 7: Refactor Order-Total Capstone (20 min)

### Starting Script — Intentionally Messy (3 min)

**Say**: "This is ~40 lines of duplicated logic. Your job: same output, cleaner structure."

**Give students**:

```python
# --- BEFORE: messy duplicated orders ---
TAX_RATE = 0.18

# Order 101
items_101 = [120, 450, 89]
sub_101 = 0
for price in items_101:
    sub_101 += price
tax_101 = sub_101 * TAX_RATE
total_101 = sub_101 + tax_101
print(f"Order 101 | subtotal: {sub_101:.2f} | tax: {tax_101:.2f} | total: {total_101:.2f}")

# Order 102
items_102 = [310, 275]
sub_102 = 0
for price in items_102:
    sub_102 += price
tax_102 = sub_102 * TAX_RATE
total_102 = sub_102 + tax_102
print(f"Order 102 | subtotal: {sub_102:.2f} | tax: {tax_102:.2f} | total: {total_102:.2f}")

# Order 103
items_103 = [50, 50, 50, 50]
sub_103 = 0
for price in items_103:
    sub_103 += price
tax_103 = sub_103 * TAX_RATE
total_103 = sub_103 + tax_103
print(f"Order 103 | subtotal: {sub_103:.2f} | tax: {tax_103:.2f} | total: {total_103:.2f}")
```

**Ask**: "How many places do you edit if tax becomes 12%?" → Six or more — every tax line.

**Common mistake**: Refactoring everything at once without testing each function — extract and test one at a time.

### Step 1 — calc_subtotal (4 min)

**Show live refactor**:

```python
def calc_subtotal(items):
    """Return sum of all prices in items list."""
    total = 0
    for price in items:
        total += price
    return total

print(calc_subtotal([10, 20, 30]))
```

Output:

```
60
```

**Break it down**:
- Parameter `items` — list of prices changes per order
- Loop pattern from Session 4 — accumulator `total`
- `return total` — caller gets the subtotal number

**Ask**: "Test with `[120, 450, 89]` — what should you get?" → `659`.

**Common mistake**: Forgetting `return` — function prints nothing useful and returns `None`.

### Step 2 — calc_tax and calc_total (4 min)

**Show**:

```python
def calc_tax(subtotal, tax_rate=0.18):
    """Return tax amount for subtotal at given rate."""
    return subtotal * tax_rate

def calc_total(subtotal, tax):
    """Return subtotal plus tax."""
    return subtotal + tax

sub = calc_subtotal([120, 450, 89])
tax = calc_tax(sub)
total = calc_total(sub, tax)
print(f"sub={sub}, tax={tax:.2f}, total={total:.2f}")
```

Output:

```
sub=659, tax=118.62, total=777.62
```

**Break it down**:
- `calc_tax` uses default `tax_rate=0.18` — change rate in one place
- `calc_total` only adds — single responsibility
- Functions **chain**: output of one becomes input of next

**Ask**: "How do you get 12% tax on the same subtotal?" → `calc_tax(sub, tax_rate=0.12)`.

**Common mistake**: Passing `items` directly to `calc_tax` — tax applies to **subtotal**, not raw list.

### Step 3 — format_order_line and main driver (6 min)

**Show complete solution**:

```python
def format_order_line(order_id, subtotal, tax, total):
    """Return formatted one-line order summary string."""
    return f"Order {order_id} | subtotal: {subtotal:.2f} | tax: {tax:.2f} | total: {total:.2f}"

orders = {
    101: [120, 450, 89],
    102: [310, 275],
    103: [50, 50, 50, 50],
}

for order_id, items in orders.items():
    sub = calc_subtotal(items)
    tax = calc_tax(sub)
    total = calc_total(sub, tax)
    print(format_order_line(order_id, sub, tax, total))
```

Output:

```
Order 101 | subtotal: 659.00 | tax: 118.62 | total: 777.62
Order 102 | subtotal: 585.00 | tax: 105.30 | total: 690.30
Order 103 | subtotal: 200.00 | tax: 36.00 | total: 236.00
```

**Break it down**:
- `orders` dict maps order ID → item list — preview of Session 7
- Loop replaces three copy-pasted blocks
- `main` section reads top-to-bottom like a recipe

**Ask**: "Same numbers as the messy script?" → Yes — refactoring preserves behaviour.

**Common mistake**: Printing inside every helper instead of one `format_order_line` — harder to change output format.

### Extension — process_order composition (3 min)

**Show for faster students**:

```python
def process_order(order_id, items, tax_rate=0.18):
    """Return (subtotal, tax, total) tuple for one order."""
    sub = calc_subtotal(items)
    tax = calc_tax(sub, tax_rate)
    total = calc_total(sub, tax)
    return sub, tax, total

sub, tax, total = process_order(101, [120, 450, 89])
print(format_order_line(101, sub, tax, total))
```

Output:

```
Order 101 | subtotal: 659.00 | tax: 118.62 | total: 777.62
```

**Break it down**:
- Functions calling functions — **composition**
- Returns **tuple** of three values — Session 7 preview
- Higher-level `process_order` hides steps for simple callers

**Ask**: "Link to Session 5 math?" → `h(x) = f(g(x))` — compose smaller functions into bigger ones.

**Common mistake**: Returning three separate `print` statements instead of one `return` tuple — caller cannot reuse values.

---

## SEGMENT 8: Common Mistakes & Wrap (8 min)

### Common Mistakes (5 min)

**Mistake 1 — print vs return**

```python
# Wrong for calculations
def get_tax(amount):
    print(amount * 0.18)

# Right
def get_tax(amount):
    return amount * 0.18
```

**Mistake 2 — Forgetting return**

```python
def add_bonus(salary):
    bonus = salary * 0.1
    new_salary = salary + bonus
    # missing return — caller gets None
```

**Mistake 3 — Using local variable outside function**

```python
def calc(x):
    result = x * 2
    return result

calc(5)
# print(result)   # NameError
```

**Mistake 4 — Default before non-default**

```python
# def bad(price, discount=10, currency):   # SyntaxError
```

**Mistake 5 — Default parameter order in call**

```python
# discounted(pct=10, 100)   # positional after keyword — error
discounted(100, pct=10)      # correct
```

### Session Recap (3 min)

| Topic | Key Tool | Key Syntax |
|---|---|---|
| Define function | `def` | `def name(params):` |
| Return value | `return` | `return result` |
| Default arg | `=` in def | `def f(a, b=10):` |
| Local scope | indentation block | names inside `def` only |
| Refactor | extract + call | `calc_subtotal(items)` |
| Document | docstring | `"""One line."""` |
| Flexible params | preview | `*args`, `**kwargs` |

**Bridge to next session:** "Next you store **many values** in lists and dicts — then load **files and JSON**. You will write functions that take a list of records and return cleaned data."

---

## In-Class Quiz (10 Questions)

*10 min — oral, clicker, or short written. Answers in instructor key below.*

**Q1.** What keyword defines a function in Python?  
**Q2.** What is the difference between a parameter and an argument?  
**Q3.** What does a function return if there is no `return` statement?  
**Q4.** Why is `print` inside a function different from `return`?  
**Q5.** What error occurs if you use a variable created inside a function outside that function?  
**Q6.** Where must parameters with default values appear in the parameter list?  
**Q7.** What does `def power(base, exp=2)` return when called as `power(5)`?  
**Q8.** Name the three functions you extracted in the order capstone.  
**Q9.** What is a docstring and where does it go?  
**Q10.** What does `*args` collect in a function definition?

### Quiz Answer Key (Instructor Only)

1. `def`  
2. Parameter is in the definition; argument is the value passed at call time  
3. `None`  
4. `print` displays; `return` sends a value to the caller  
5. `NameError`  
6. After non-default parameters  
7. `25`  
8. `calc_subtotal`, `calc_tax`, `calc_total` (also accept `format_order_line`)  
9. Triple-quoted description under `def`, first statement in body  
10. Extra positional arguments as a tuple  

---

## Homework / Self-Practice

1. Write `celsius_to_fahrenheit(c)` with `return` and a one-line docstring. Test at `0`, `37`, and `100`.
2. Add `apply_coupon(total, pct=5)` to the order project — apply coupon **after** tax or before (document your choice in a comment).
3. Refactor a 20-line script from Session 4 (e.g. sum/average) into two functions: `compute_total(nums)` and `compute_average(nums)`.
4. Optional: Read `help(print)` and `help(len)` — notice built-in docstrings.
5. Optional: Write `process_order` that returns a tuple and unpacks it in a loop over five fake orders.

**Submission tip:** One Colab notebook — functions at top, test calls in cells below, capstone output screenshot.

---

## FAQ — Frequently Asked Questions (8+)

**Q1: Can a function return nothing?**  
Yes — implicit `None`. Fine for side effects like `print_report()`, but prefer `return` for calculations.

**Q2: Can I define a function inside a loop?**  
Python allows it, but define once at the top level for clarity unless you have a specific reason.

**Q3: Why did my function return None when I used print?**  
`print` displays; only `return` sends a value to the caller.

**Q4: How many lines should one function have?**  
No fixed rule — if it does more than one **idea**, split it. `calc_tax` should not also print receipts and save files.

**Q5: Is `TAX_RATE` as a global bad?**  
Constants at module level are common. **Changing** globals inside functions is what to avoid — prefer parameters.

**Q6: Can I return multiple values?**  
Yes — `return a, b` returns a tuple. Caller: `sub, tax = calc_parts(items)`. Full unpacking in Session 7.

**Q7: What is the difference between `return` and `break`?**  
`return` exits a **function** and optionally sends a value. `break` exits a **loop** only.

**Q8: Do I need docstrings on every function?**  
For reusable functions — yes, one sentence minimum. Throwaway scratch code in a notebook — optional.

**Q9: When should I use *args and **kwargs?**  
When building flexible library-style APIs. For learning scripts, named parameters and defaults are clearer.

**Q10: Can functions call other functions?**  
Yes — composition is the goal. `process_order` calling `calc_subtotal` and `calc_tax` is idiomatic Python.

**Q11: What if my function needs both a list and a tax rate?**  
Pass both as parameters: `def process(items, tax_rate=0.18):` — explicit beats hidden globals.

**Q12: How do functions relate to Pandas later?**  
`df.apply(lambda row: ...)` applies a function to each row — same idea, larger data.

---

## Instructor Notes

- **Live coding tip:** Introduce one function at a time with `print(calc_subtotal([10,20]))` before moving on — builds trust in refactoring.
- **Common student mistake:** Forgetting `return` and wondering why `total` is `None` downstream.
- **Common student mistake:** Using the same parameter name as a global and getting confused — rename for clarity in demos.
- **Pacing:** If short on time, provide half-refactored starter (functions defined, students write main loop only). **Protect Segment 7** — it is the capstone.
- **Assessment:** Coding problem tasks map to Segment 5; order refactor is session capstone — collect one notebook cell as exit ticket.
- **Connection to course:** Pandas `.apply()` is "call a function on each row" — preview only.
- **Pre-read alignment:** Sections A–H map to Segments 2–6; do not re-read the pre-read aloud — open with "what did you try from the pre-read?"
- **Break activity:** Function signature sketch keeps minds on modularity without heavy typing.
- **Differentiation:** Fast finishers add `apply_coupon`, `process_order` tuple return, or CSV-ready dict output for Session 7 bridge.
- **Strict 2-hour trim:** Cut Segment 6 `**kwargs` demo to verbal mention; keep docstrings one-liner; preserve Segment 7 capstone and Quiz Q1–Q8.

---

## Appendix: assert-Based Quick Tests (Optional)

```python
assert calc_subtotal([10, 20]) == 30
assert calc_tax(100, 0.18) == 18.0
assert calc_total(100, 18) == 118
assert double(7) == 14
assert discounted(100, 25) == 75.0
print("All asserts passed.")
```

Output:

```
All asserts passed.
```

**Break it down**:
- `assert` crashes if condition is False — instant feedback while refactoring
- Run after each extracted function during live coding
- Professional tests use frameworks; `assert` is enough in class today

**Ask**: "What happens if `calc_subtotal` has a bug?" → Assert fails with `AssertionError` — you know immediately.

**Common mistake**: Leaving asserts in production without tests around them — fine for learning notebooks, replace with proper tests in projects later.
