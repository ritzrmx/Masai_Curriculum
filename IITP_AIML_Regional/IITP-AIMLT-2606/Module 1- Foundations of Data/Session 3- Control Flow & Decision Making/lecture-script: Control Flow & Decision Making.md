# Lecture Script: Control Flow & Decision Making
> **Instructor Reference** — Module 1: Foundations of Data | Session 3 | Duration: 2 Hours

---

## Session Overview

**Goal:** Students write if/elif/else blocks with combined boolean conditions, trace nested logic on paper, and build two working programs: a **grade calculator** and an **eligibility checker**.

**Student profile at this point:** Comfortable with Colab, variables, types, operators, input/output, and f-strings from Session 2. Ready to turn business rules into executable code.

**Key outcome:** Every student completes a grade band program (elif chain), an eligibility checker (and/or/not), and correctly traces at least three multi-branch examples before running them.

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| Opening & Hook — Why Decisions Matter | 5 min | 0:05 |
| **Concept 1:** if / else — One Branch | 10 min | 0:15 |
| **Practical 1:** Pass/Fail Live Coding | 15 min | 0:30 |
| **Concept 2:** elif Chains & Order of Checks | 10 min | 0:40 |
| **Practical 2:** Grade Calculator Lab | 15 min | 0:55 |
| **BREAK** | 10 min | 1:05 |
| **Concept 3:** Boolean Logic & Truth Tables | 10 min | 1:15 |
| **Practical 3:** Truth Table Activity + and/or/not Live | 15 min | 1:30 |
| **Concept 4:** Nested Conditions & Tracing | 10 min | 1:40 |
| **Practical 4:** Eligibility Checker Lab | 10 min | 1:50 |
| Summary & Wrap-Up | 5 min | 1:55 |
| Q&A & Doubt Solving | 5 min | 2:00 |

---

## SEGMENT 1: Opening & Hook (8 min)


**Hook:** Ask the class: *"What happens on Swiggy when you open the app — before you see restaurants?"*

Collect answers: login check, location, serviceability, offers for members.

**Say:** *"Every one of those is an if statement. Today we write the same kind of logic in Python."*

**Context to set:** Session 2 stored data and did math. Real apps also **choose** — pass or fail, eligible or not, discount or full price. That is **control flow**.

**Learning contract for today:**
- Write if / elif / else with correct indentation
- Combine conditions with and, or, not
- Trace code on paper before running
- Build grade and eligibility programs end to end

**Write on board:** `if condition:` → True runs indented block | False skips to else/elif

---

## Concept Block 1: if / else — One Branch (10 min)

### Anatomy of a Decision

```python
score = 72

if score >= 60:
    print("Pass — well done!")
else:
    print("Retake required.")
```

| Line | Purpose |
|---|---|
| `if score >= 60:` | Condition — must be True or False |
| Indented print | Body — runs only if True |
| `else:` | Catch-all when condition is False |
| Colon `:` | Required after if/elif/else |

**Indentation rule:** Python uses whitespace (4 spaces) to know what belongs inside the branch. No curly braces `{}` like other languages.

**Comparison operators review:**

| Operator | Meaning |
|---|---|
| `==` | Equal |
| `!=` | Not equal |
| `>`, `<`, `>=`, `<=` | Greater / less |

**Critical mistake preview:**

```python
if age = 18:   # SyntaxError — assignment, not comparison
```

**Write on board:** **`=` assigns | `==` compares**

**Ask:** *"Can the condition be a variable that is already True or False?"* → Yes:

```python
is_member = True
if is_member:
    print("Member discount")
```

---

## Practical Block 1: Pass/Fail Live Coding (15 min)

### Cell 1 — Basic pass/fail

Students type along:

```python
score = int(input("Enter your score (0-100): "))

if score >= 60:
    print("Result: PASS")
else:
    print("Result: FAIL")
```

**Sample run:**

```
Enter your score (0-100): 72
Result: PASS
```

**Ask:** *"What if they type 59?"* → FAIL branch.

### Cell 2 — Boundary test

```python
score = 60
if score >= 60:
    print("Pass")
else:
    print("Fail")
# Exactly 60 passes — >= means "60 or more"
```

**Expected output:** `Pass`

**Say/Ask prompts:**
- *"What happens with score = 59?"*
- *"Do we need else? What if we only want to print on pass?"* → else is optional

### Cell 3 — Trace without running

Put on board:

```python
temperature = 45
if temperature > 40:
    print("Heatwave")
else:
    print("Normal")
```

**Activity (2 min):** Students write predicted output on paper. Then run to verify.

**Expected output:** `Heatwave`

**Debrief:** Tracing before running catches logic bugs early.

---

## Concept Block 2: elif Chains & Order of Checks (10 min)

### Why elif Exists

When you have **more than two outcomes**, use `elif`:

```python
temp = 38

if temp > 40:
    print("Heatwave alert")
elif temp > 30:
    print("Hot day")
elif temp > 20:
    print("Warm")
else:
    print("Cool")
```

**Teaching point:** Python checks **top to bottom**. First True branch wins. Rest are **skipped**.

### Order trap — demonstrate wrong order

```python
score = 95

# WRONG ORDER — everything becomes "F" tier wrongly
if score >= 60:
    print("C or above")      # 95 matches here first!
elif score >= 90:
    print("A")               # Never reached

# CORRECT ORDER — highest threshold first
if score >= 90:
    print("A")
elif score >= 75:
    print("B")
elif score >= 60:
    print("C")
else:
    print("F")
```

| score | Wrong chain prints | Correct chain prints |
|---|---|---|
| 95 | C or above | A |
| 82 | C or above | B |
| 55 | (first elif 60 fails…) | F |

**Grade band reference table:**

| Grade | Condition |
|---|---|
| A | score >= 90 |
| B | score >= 75 |
| C | score >= 60 |
| F | else |

**Key message:** Put **strictest / highest** checks first when using overlapping thresholds.

---

## SEGMENT 5: Grade Calculator Lab (15 min)


### Requirements (display on slide)

Build a **Grade Calculator** that:

1. Asks for a score (0–100) as integer
2. Prints letter grade: A ≥ 90, B ≥ 75, C ≥ 60, else F
3. Uses **elif chain** (not separate unrelated ifs)
4. Bonus: print a one-line message per grade ("Excellent!", etc.)

### Reference solution

```python
# Grade Calculator Lab
score = int(input("Enter score (0-100): "))

if score >= 90:
    grade = "A"
    message = "Excellent work!"
elif score >= 75:
    grade = "B"
    message = "Good job!"
elif score >= 60:
    grade = "C"
    message = "Passed — keep improving."
else:
    grade = "F"
    message = "Retake recommended."

print(f"Score: {score} → Grade: {grade}")
print(message)
```

**Sample runs:**

```
Enter score (0-100): 94
Score: 94 → Grade: A
Excellent work!

Enter score (0-100): 58
Score: 58 → Grade: F
Retake recommended.
```

**Facilitation (10 min code, 5 min share):**
- Walk room — common bug: wrong elif order
- Ask one student: *"Trace score=75 — which branch?"* → B
- Ask: *"Trace score=90 — A or B?"* → A (>= 90 checked first)

**Extension for fast finishers:**

```python
if score < 0 or score > 100:
    print("Invalid score — enter 0 to 100")
else:
    # elif chain here
```

Preview validation — full input checking later in course.

---

## BREAK (10 min)

---


*Suggested break prompt:* Write one real-life rule as if/else in plain English (e.g. "if rain, take umbrella"). Share after break.

---

## SEGMENT 6: Boolean Logic (13 min)


### Three operators

| Operator | English | True when |
|---|---|---|
| `and` | both must hold | all parts True |
| `or` | at least one | any part True |
| `not` | opposite | flips True↔False |

```python
age = 20
has_id = True

if age >= 18 and has_id:
    print("Entry allowed")
```

### Truth tables — draw on board

**AND**

| A | B | A and B |
|---|---|---|
| T | T | T |
| T | F | F |
| F | T | F |
| F | F | F |

**OR**

| A | B | A or B |
|---|---|---|
| T | T | T |
| T | F | T |
| F | T | T |
| F | F | F |

**NOT**

| A | not A |
|---|---|
| T | F |
| F | T |

**Physical activity tip:** Give students two True/False cards. Call out `A and B` — they stand only if BOTH true. Then `A or B` — stand if EITHER true. Muscle memory helps.

**Ask:** *"Login needs email valid AND password length >= 8. Write it."*

```python
if email_valid and password_length >= 8:
    print("Login OK")
```

**Ask:** *"Discount if member OR has coupon?"*

```python
if is_member or has_coupon:
    print("Discount applied")
```

**Precedence note:** `not` > `and` > `or`. Use parentheses when mixing: `(a or b) and c`.

---

## SEGMENT 7: Discount Rules Lab (15 min)


### Part A — Truth table fill (5 min)

Handout or slide — students fill **A and B** and **A or B** for all four rows (use T/F). Check against board tables above.

### Part B — Live coding discount rules (10 min)

```python
is_member = input("Are you a member? (yes/no): ").lower() == "yes"
has_coupon = input("Do you have a coupon? (yes/no): ").lower() == "yes"

if is_member or has_coupon:
    discount = 15
    print(f"You get {discount}% off!")
else:
    discount = 0
    print("No discount today.")

bill = float(input("Bill amount (₹): "))
final = bill * (1 - discount / 100)
print(f"Final amount: ₹{final:.2f}")
```

**Sample run (member):**

```
Are you a member? (yes/no): yes
Do you have a coupon? (yes/no): no
You get 15% off!
Bill amount (₹): 1000
Final amount: ₹850.00
```

**Discussion:** *"Should member AND coupon stack to 30%?"* → Business rule, not Python rule. Code what product asks for:

```python
if is_member and has_coupon:
    discount = 25
elif is_member or has_coupon:
    discount = 15
else:
    discount = 0
```

**Say:** *"Same syntax, different business decision. Always clarify rules before coding."*

---

## Concept Block 4: Nested Conditions & Tracing (10 min)

### When to nest

```python
country = "IN"
amount = 1500

if country == "IN":
    if amount > 1000:
        print("GST applies — include 18% in invoice")
    else:
        print("Below GST registration threshold")
else:
    print("International — apply export rules")
```

**vs flat and:**

```python
if country == "IN" and amount > 1000:
    print("GST applies")
```

| Style | Use when |
|---|---|
| Nested | Different inner logic per outer branch |
| `and` | Single combined test, same action |

### Trace-the-output — board exercise

```python
x = 15
if x > 20:
    print("A")
elif x > 10:
    print("B")
else:
    print("C")
```

**Trace table on board:**

| Step | Condition | True? | Action |
|---|---|---|---|
| 1 | x > 20 → 15 > 20 | No | skip |
| 2 | x > 10 → 15 > 10 | Yes | print B |
| 3 | else | — | skipped |

**Expected output:** `B`

**Second trace (harder):**

```python
logged_in = True
is_admin = False

if logged_in:
    if is_admin:
        print("Admin panel")
    else:
        print("User dashboard")
else:
    print("Please log in")
```

**Expected output:** `User dashboard`

---

## Practical Block 4: Eligibility Checker Lab (10 min)

### Scenario

A simplified **loan eligibility** check (educational — not financial advice):

| Rule | Requirement |
|---|---|
| Age | 21 to 60 inclusive |
| Income | ≥ ₹25,000 per month |
| Documents | PAN submitted |
| Credit | Not blacklisted |

### Reference solution

```python
# Eligibility Checker Lab
print("=== Loan Eligibility Check ===")

age = int(input("Age: "))
income = float(input("Monthly income (₹): "))
has_pan = input("PAN submitted? (yes/no): ").lower() == "yes"
blacklisted = input("Credit blacklisted? (yes/no): ").lower() == "yes"

# Combined conditions
age_ok = age >= 21 and age <= 60
income_ok = income >= 25000
docs_ok = has_pan
credit_ok = not blacklisted

if age_ok and income_ok and docs_ok and credit_ok:
    print("✅ ELIGIBLE — proceed to application.")
elif not age_ok:
    print("❌ Ineligible: age must be 21–60.")
elif not income_ok:
    print(f"❌ Ineligible: income ₹{income:.0f} below ₹25,000 minimum.")
elif not docs_ok:
    print("❌ Ineligible: PAN document required.")
elif not credit_ok:
    print("❌ Ineligible: credit blacklist flag.")
else:
    print("❌ Ineligible: review required.")
```

**Sample run (eligible):**

```
=== Loan Eligibility Check ===
Age: 28
Monthly income (₹): 45000
PAN submitted? (yes/no): yes
Credit blacklisted? (yes/no): no
✅ ELIGIBLE — proceed to application.
```

**Sample run (income fail):**

```
Age: 30
Monthly income (₹): 18000
PAN submitted? (yes/no): yes
Credit blacklisted? (yes/no): no
❌ Ineligible: income ₹18000 below ₹25,000 minimum.
```

**Facilitation (7 min code, 3 min debrief):**
- Highlight `not blacklisted` as readable credit check
- Ask: *"Why store age_ok instead of one giant if?"* → Readable, debuggable
- Connect to Session 1: banks use **ML** for fraud; **rules** for hard cutoffs like age

**Trace quiz (if time):** age=19, income=50000, pan=yes, blacklisted=no → which message?

**Answer:** Ineligible age (first failing elif in simplified version — discuss order if using combined if).

---

## SEGMENT 10: Summary & Wrap (8 min)


**What we covered today:**
- if / else and elif chains — order of checks matters
- Grade calculator pattern — overlapping thresholds top-down
- Boolean logic: and, or, not — truth tables
- Nested conditions vs combined and
- Tracing execution before running
- Eligibility checker — real-world rule encoding

**Bridge to next session:** *"Next class: **loops** — repeat without copy-paste. Grade every student in a list. Process every row in a table. Same Colab, new superpower."*

**Homework / self-practice:**
1. Add input validation to grade calculator: reject scores below 0 or above 100.
2. Build a **movie ticket** pricer: child (<12) ₹100, student (12–18) ₹150, adult ₹200.
3. Write three trace questions (if/elif) and swap with a partner — predict output before running.

---

## Q&A & Doubt Solving (5 min)

**Likely questions and suggested answers:**

**Q: elif vs separate if statements?**
→ elif is mutually exclusive — only one runs. Separate ifs can each fire independently. Use elif for grade bands; separate ifs when checking unrelated flags.

**Q: Can I use if inside if? How deep?**
→ Yes. Keep nesting shallow (2–3 levels). Refactor with and/or or functions if deeper.

**Q: Why `==` for strings but `is` sometimes online?**
→ For learning, always use `==` for value comparison. `is` checks identity — advanced topic; avoid for now.

**Q: My code does nothing when I run it — no error.**
→ Condition was False and you had no else. Add print debug: `print("debug:", score)` before if.

**Q: How does this connect to ML?**
→ Model outputs (score > 0.5) become conditions. if/else wraps model decisions in apps.

---

## Instructor Notes

- **Prerequisite check:** First 5 min — confirm all can run Session 2 profile card. Pair struggling students.
- **Common mistake:** `if age = 18` — stop and fix immediately; whole cohort will hit this.
- **Another mistake:** Forgetting colon after if/elif/else — SyntaxError on next line.
- **Indentation:** Mixed tabs/spaces cause IndentationError. Colab defaults to spaces — good.
- **Truth table activity:** Physical stand/sit version takes 3 min but fixes and/or confusion for visual learners.
- **Eligibility lab:** Keep disclaimers light — "simplified teaching example."
- **Time check:** If behind, give grade calculator starter with elif skeleton empty.
- **If ahead:** Add nested GST example from pre-read section E.

---

## Common Errors — Quick Reference

| Bug | Symptom | Fix |
|---|---|---|
| `=` in if | SyntaxError | Use `==` |
| Wrong elif order | 95 gets C not A | Highest threshold first |
| Missing colon | SyntaxError next line | Add `:` after condition |
| Bad indent | IndentationError | Align with 4 spaces |
| String vs int compare | Unexpected branch | Cast input with int() |

---

## Appendix: Trace-the-Output Answer Key (Instructor)

| # | Code snippet | Output |
|---|---|---|
| 1 | x=5, if x>3 print A else B | A |
| 2 | x=2, same | B |
| 3 | x=15, elif chain to 20/10 | B |
| 4 | logged_in T, is_admin F nested | User dashboard |
| 5 | score=75, grade bands 90/75/60 | B |

---

## Appendix: Full In-Class Trace Quiz (Optional — 5 min if ahead)

Students predict output — then run:

```python
# Quiz 1
a, b = True, False
print(a and b)
print(a or b)
print(not a)

# Quiz 2
n = 8
if n > 10:
    print("X")
elif n > 5:
    print("Y")
else:
    print("Z")
```

**Answers:**

```
False
True
False

Y
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

## SEGMENT 11: Supplemental Control Flow Demos

### Demo — Grade bands

```python
score = int(input("Score: "))
if score >= 90:
    print("A")
elif score >= 75:
    print("B")
elif score >= 60:
    print("C")
else:
    print("F")
```

**Break it down:** elif chain; highest threshold first.

**Ask:** Grade for score=75?

**Common mistake:** elif 60 before elif 90.

**Fix:** Order thresholds descending.

### Demo — Member OR coupon

```python
is_member = input("Member? ").lower() == "yes"
has_coupon = input("Coupon? ").lower() == "yes"
if is_member or has_coupon:
    print("15% off")
```

**Ask:** Stack to 30% if both?

**Common mistake:** Ambiguous business rule without spec.

**Fix:** Ask product owner; code explicit policy.

### Demo — GST nested

```python
country, amount = "IN", 1500
if country == "IN":
    if amount > 1000:
        print("GST applies")
```

**Ask:** Rewrite with `and`.

**Common mistake:** 4+ nesting levels.

**Fix:** Flatten with and/or.

### Trace practice bank

| x | Code | Output |
|---|---|---|
| 5 | if x>3: A else B | A |
| 2 | same | B |
| 15 | elif 20/10 | B |

### FAQ additions

**Q: elif vs if?** → elif exclusive.

**Q: == vs is?** → Use == now.

**Q: Silent code?** → False condition, no else.

**Q: ML connection?** → score > 0.5 in if.

**Q: not keyword?** → Python uses not not !

**Q: Chained comparison?** → 75 <= x < 90 valid.

**Q: Input validation?** → Check range before logic.

**Q: Blacklisted flag?** → Use not blacklisted for readability.
