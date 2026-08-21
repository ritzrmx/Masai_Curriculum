# Lecture Script: Foundations of Data — Loops, Iteration & Repetitive Logic
> **Instructor Reference** — Module 1: Foundations of Data | Academic Session 4 | Duration: 2 Hours | Instructor: [Industry Mentor / Name Placeholder]

---

## Session Overview
**Goal:** By the end, students can write for and while loops with correct termination conditions, control loop flow using break and continue, and iterate over lists and strings by index.

**Student profile at this point:** Comfortable with variables, operators, and if/elif/else from Sessions 1.2 and 2.1. Likely wrong assumption: that `range(5)` includes 5, or that a `while` loop will "figure out" when to stop on its own. Boredom risk is low; frustration risk is high the first time a student accidentally writes an infinite loop and the notebook appears to freeze.

**Key outcome:** Students should leave with the instinct to ask, before writing any loop: *"Do I know exactly how many times this repeats? Or does it depend on a condition that changes?"* — that question decides `for` vs `while`.

> 🎯 **The one sentence this session must land:** *A for loop repeats a known number of times; a while loop repeats until a condition you control becomes False — and if nothing inside it ever changes that condition, it never stops.*

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| Opening — "The Notebook That Wouldn't Stop" | 8 min | 8 min |
| Concept + Practical Block 1: for Loops & range() | 25 min | 33 min |
| Concept + Practical Block 2: while Loops & Termination | 22 min | 55 min |
| ☕ BREAK | 5 min | 60 min |
| Concept + Practical Block 3: break & continue | 20 min | 80 min |
| Concept + Practical Block 4: Iterating Lists & Strings | 20 min | 100 min |
| Summary & Bridge | 5 min | 105 min |
| Q&A & Doubt Solving | 15 min | 120 min |

---

## Opening — "The Notebook That Wouldn't Stop" (8 min)

Type this live in Colab, but DON'T run it yet:
```python
count = 0
while count < 5:
    print(count)
```

> "Before I run this — who can tell me what's missing?"
[Pause for guesses.]

> "There's no line inside this loop that changes `count`. If I run this, it will print `0` forever, and I'll have to manually stop it. This is called an infinite loop, and almost everyone in this room will write one by accident in the next hour. That's fine — today you'll learn exactly why it happens and how to prevent it."

Run it briefly, show the endless `0`s, then interrupt/stop the cell.

> "Loops are how your program repeats work automatically instead of you copy-pasting the same line 20 times. But repetition without a clear stopping point is dangerous — today's session is really about controlling exactly when and how repetition ends."

Pivot line: "Let's start with the loop that always knows when to stop — the `for` loop."

---

## Concept + Practical Block 1: for Loops & range() (25 min)

### "Serving prasad to everyone in a known queue"
> "At a temple, if you know there are exactly 5 people in line, you serve prasad 5 times, one per person, then you're done. A `for` loop works the same way — it runs once per item in a known sequence."

**Hands-on:**
```python
for person_number in range(1, 6):
    print(f"Serving prasad to person {person_number}")
```

Ask before running: "How many times will this print?" Let the room guess, then run and confirm: exactly 5 times, `1` through `5`.

### 🔴 The trap / highest-value moment
Write on the board: **"`range(5)` gives 0,1,2,3,4 — it stops ONE SHORT of 5."**

Demonstrate live: `for i in range(5): print(i)` — count the outputs together as a room.

💬 **Expect an argument about:** "Why does range start at 0 and stop early — isn't that confusing?" Welcome it. Say: *"It lines up with how indexing works in Python — the first item in a list is also at position 0, not 1. Once that clicks, `range()` behaving the same way actually makes things more consistent, not less."*

---

## Concept + Practical Block 2: while Loops & Termination Conditions (22 min)

### "Waiting at the bus stop — you don't know exactly how long"
> "You don't wait a fixed number of minutes at a bus stop — you wait WHILE the bus hasn't come. The moment it arrives, you stop. That's a `while` loop: repeat as long as a condition holds."

**Hands-on, built live:**
```python
bus_arrived = False
minutes_waited = 0

while not bus_arrived:
    minutes_waited += 1
    print(f"Waited {minutes_waited} minute(s)...")
    if minutes_waited == 7:
        bus_arrived = True

print("Bus arrived!")
```

Ask the room: "What's the ONE line that guarantees this loop eventually stops?" — point to `minutes_waited == 7` setting `bus_arrived = True`.

**Answer key / reasoning to say aloud:** Connect directly back to the opening hook — the earlier broken example was missing exactly this kind of line, which is why it never stopped.

### 🔴 The trap / highest-value moment
Write on the board: **"Something inside a while loop MUST eventually make its condition False — or it never stops."**

💬 **Expect an argument about:** "Why not just always use `for` loops and avoid this risk entirely?" Welcome it. Say: *"`for` loops need you to already know the sequence or count in advance. Real situations — like 'keep asking the user for input until they type quit' — don't have a fixed count. That's exactly when `while` earns its place."*

---

## ☕ BREAK (5 min)

---

## Concept + Practical Block 3: break & continue (20 min)

### "Pulled aside vs. waved through"
> "At airport security — if the metal detector seriously alarms, you're pulled out of line entirely. That's `break`. If someone just forgot to remove their belt, they step aside, fix it, and rejoin the process at the next check — that's `continue`. Both interrupt the normal flow, but very differently."

**Hands-on:**
```python
for item_price in [200, 150, 0, 300, 450]:
    if item_price == 0:
        continue
    if item_price > 400:
        break
    print(f"Item within budget: ₹{item_price}")
```

Trace it together as a room, item by item, predicting what prints before running.

**Answer key / reasoning to say aloud:** `200` and `150` print normally. `0` is skipped via `continue` — the loop moves on without printing. `300` prints. `450` triggers `break` — the loop stops entirely, so nothing after it (even if there were more items) would run.

### 🔴 The trap / highest-value moment
Write on the board: **"`continue` skips ONE iteration and keeps going. `break` stops the WHOLE loop, right there."**

💬 **Expect an argument about:** "Can't I just use an if/else instead of `continue`?" Welcome it. Say: *"Often yes, for simple cases — but `continue` becomes essential once you have several checks in a row and just want to skip the rest of THIS iteration's checks without deeply nesting everything in an else block."*

---

## Concept + Practical Block 4: Iterating Over Lists & Strings (20 min)

### "The attendance register — read in order, or jump to a row"
> "A teacher can read an attendance register top to bottom, name by name — or jump straight to row number 5. Lists and strings support both approaches in Python."

**Hands-on:**
```python
roll_call = ["Aditi", "Rohan", "Meera"]

for i, student in enumerate(roll_call):
    print(f"Row {i}: {student}")
```

Then show direct indexing: `print(roll_call[0])`.

**Answer key / reasoning to say aloud:** Walk through why `roll_call[0]` gives `"Aditi"`, not `"Rohan"` — reinforce the zero-indexing rule from Block 1's `range()` discussion, tying the two together explicitly.

### 🔴 The trap / highest-value moment
Write on the board: **"Indexing starts at 0. The first item is `[0]`, not `[1]`."**

💬 **Expect an argument about:** "Why does `enumerate()` matter if I could just track a counter myself with `i = i + 1`?" Welcome it. Say: *"You could — but `enumerate()` does it correctly and cleanly in one line, and it's the convention every experienced Python programmer reaches for, so you'll recognize it everywhere in real code."*

---

## Summary & Bridge (5 min)

| Concept | The one thing to remember |
|---|---|
| for loops & range() | Repeats a known number of times; `range(n)` stops one short of `n` |
| while loops | Repeats until a condition becomes False — something inside must change it |
| break & continue | `break` exits the whole loop; `continue` skips just this iteration |
| Iterating sequences | Indexing starts at 0; `enumerate()` gives you index and value together |

Close on the thesis: *"A for loop repeats a known number of times; a while loop repeats until a condition you control becomes False — and if nothing inside it ever changes that condition, it never stops."*

Bridge: "Everything you've coded so far — conditions, loops, operators — actually rests on some deeper mathematics. Next session is a Master class where we step back and look at the number systems, logic, and structures underneath all of it."

---

## Q&A & Doubt Solving (15 min)

**Q: What happens if I accidentally write an infinite while loop in Colab?**
→ Click the stop/interrupt button on the running cell — it forcibly halts execution; the fix is always to check that something inside the loop changes the condition being tested.

**Q: Can I use break and continue inside a while loop too, not just for loops?**
→ Yes — both keywords work identically inside while loops; they control the flow of any loop type the same way.

**Q: Is there a limit to how many times a for loop can run?**
→ Only practical limits — it runs exactly as many times as there are items in the sequence, whether that's 5 or 5 million; very large sequences just take longer.

**Q: Why did my nested for loop inside an if statement not print anything?**
→ Almost always an indentation issue — check that the loop and its body are indented consistently and correctly nested inside the if block, not accidentally outside it.

**Q: Can I loop over a string the same way I loop over a list?**
→ Yes — a string is a sequence of characters, so `for letter in "Python":` visits each character one at a time, just like looping over a list of items.

**Q: When would I actually need `enumerate()` instead of just looping normally?**
→ Anytime you need to know WHERE an item is, not just what it is — like printing row numbers, or comparing an item to its neighbor by position.

---

## Instructor Notes
- **Words not yet earned — avoid using without defining:** "list comprehension," "iterator," "generator." These are worth flagging as "a faster way to write this, coming later" but not formally taught today.
- **Biggest risk this session:** a student's Colab cell appearing to freeze from an infinite while loop — walk the room proactively during Block 2's hands-on to catch this before panic sets in, and normalize it in the opening hook.
- **Board management:** Keep the for-loop flowchart from the pre-read visible during Block 1, and write the "while loop must eventually go False" rule somewhere it stays visible through Block 2 and the break/continue block that follows.
- **Common confusions, numbered:**
  1. Expecting `range(n)` to include `n` itself.
  2. Writing a `while` loop with no line that changes the condition.
  3. Mixing up `break` (stops everything) with `continue` (skips just one iteration).
- **Cross-references to later sessions:** Today's iteration logic becomes the mental model for looping through DataFrame rows conceptually in Pandas (Sessions 5.1–5.2), and `range()`/indexing habits carry directly into NumPy array indexing (Session 4.2).
- **Local/cultural context notes:** Temple prasad queues, bus stop waiting, and airport security lines continue as familiar Indian-context analogies — keep leaning on physical, queue-based scenarios since they map unusually well onto loop behavior.
