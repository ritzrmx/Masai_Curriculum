# Lecture Script: Master Class — Calculus Intuition: Change, Slope & Optimisation
> **Instructor Reference** — Module 3: GenAI & Agents | Session 10 | Duration: 2 Hours

---

## Session Overview

**Goal:** Build solid, board-first intuition for the idea of a function as a rule and its rate of change, derivatives as "instantaneous slope," and optimization as "use the slope to walk downhill toward a minimum" — so students have the mathematical foundation for gradient descent, the training procedure underneath every neural network and most machine learning model fitting they will encounter going forward, without needing to re-derive it from scratch later.

**Student profile at this point:** Finished Session 9 (chunking, vector stores, retrieval) — comfortable with Session 3's vectors/dot product/cosine similarity master class format and spirit. Likely has not touched derivatives since high school, if ever. Same math-anxiety expectations as Module 2's "Mathematics Behind Learning" and "Probability & Counting" master classes and this module's own Session 3.

**Key outcome:** Every student can explain what a derivative means geometrically (the slope of the tangent line / the instantaneous rate of change), compute a simple derivative using the limit definition BY HAND and verify it numerically in Python, explain optimization as "finding where the slope is zero or walking downhill using the slope," and trace through a gradient descent calculation by hand for a simple one-variable function, including what happens when the learning rate is too large.

**Tone:** Conceptual, board-heavy, minimal but VERIFIED coding — matching Session 3's exact master-class spirit. Every single number in this script was computed by actually running the Python shown (or by hand-verified exact arithmetic) before being written in as fact; nothing here is an LLM-generated illustrative example, since none of today's content involves calling an LLM at all.

**Master class contract:** Laptops half-closed except during the live-coded verification demos. The board is primary. Python confirms the board — not the other way around.

**Dataset for this session:** None required — all examples use small, simple, hand-checkable functions (`x^2`, `x^3`, `(x-3)^2`) so every number stays fully visible and verifiable on screen and on the board.

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| SEGMENT 1: Opening — Why Calculus, Why Now? | 10 min | 0:10 |
| SEGMENT 2: Functions and Rate of Change | 20 min | 0:30 |
| SEGMENT 3: The Derivative — Slope of the Tangent Line | 20 min | 0:50 |
| **BREAK** | 10 min | 1:00 |
| SEGMENT 4: Optimisation Intuition — Finding the Minimum | 25 min | 1:25 |
| SEGMENT 5: Gradient Descent — Walking Downhill, Step by Step | 20 min | 1:45 |
| SEGMENT 6: Lab — Hand-Traced and Verified Gradient Descent | 10 min | 1:55 |
| SEGMENT 7: Summary, Wrap-Up & Q&A | 5 min | 2:00 |

*Note: Master class may run 5-10 min over if board discussion runs rich — trim SEGMENT 5's second worked gradient descent trace (the too-large-learning-rate case) to a verbal description instead of a full live-coded walkthrough if time is tight.*

---

## SEGMENT 1: Opening — Why Calculus, Why Now? (10 min)

### The Hook (5 min)

**Say:** *"Quick question, no computer needed yet. If I told you a machine learning model 'learns' by starting with random, bad parameter values and gradually adjusting them until it makes good predictions — HOW, mechanically, does the model know WHICH DIRECTION to adjust each parameter, and by how much, at every single step?"* Collect guesses. Common answers: "trial and error," "it just tries things," "magic." **Say:** *"'Trial and error, but a very SMART, mathematically-guided version of trial and error' is the real answer, and the entire mechanism is built on exactly one idea from calculus: the derivative, which tells you the SLOPE of how an error measurement changes as you nudge a parameter. Today's whole session builds that idea from the ground up, so that 'gradient descent' — a term you'll hear constantly in this field — stops being a buzzword and becomes a precise, hand-computable idea you can trace through yourself."*

### Why This Master Class Matters (5 min)

**Connect to course arc — write on board:**

| Session | What you did / will do | Math underneath |
|---|---|---|
| 3 | Vectors, dot product, cosine similarity | The math behind "similarity" |
| 8 | Real embeddings, semantic search | Session 3's math applied to real text |
| 9 | Chunking, vector stores, retrieval | Infrastructure around Session 3/8's math at scale |
| 10 (today) | Name the math of CHANGE and OPTIMISATION | Derivatives, slope, gradient descent |
| Beyond this course | Understanding how any model (embedding models included) is actually TRAINED | Gradient descent, applied at massive scale, is what Session 10's math becomes |

**Say:** *"This is not a math exam — it's a translation session, exactly like Module 2's two math master classes and this module's own Session 3. Whiteboard symbols to Python to intuition you can explain to a non-technical teammate. Every time you hear 'the model is training' or 'the loss is decreasing,' today's math — slope, and walking in the direction that decreases that slope — is running underneath, usually literally called gradient descent."*

**Learning Contract for today — write on board:**

- Explain what a function's rate of change means, and distinguish average rate of change from instantaneous rate of change
- Compute a derivative using the limit definition, by hand, and verify it numerically in Python
- Explain optimisation as "finding where the slope is zero," using a simple parabola
- Trace through gradient descent by hand for a one-variable function, and explain what a too-large learning rate does

---

## SEGMENT 2: Functions and Rate of Change (20 min)

### What a Function Actually Is, Restated Plainly (5 min)

**Say:** *"A function is a precise rule: put a number in, get exactly one number out. You've used functions constantly already this module — `cosine_similarity(u, v)` from Session 3 is a function; it's just a function of TWO vector inputs instead of one number. Today we work with the simplest possible case: one number in, one number out, so every single step stays visible on a 2D graph."*

**Write on board:**

```
f(x) = x^2

f(2) = 4
f(3) = 9
f(-1) = 1
```

**Say:** *"Picture this as a curve on a graph: as `x` moves along the horizontal axis, `f(x)` traces out a value on the vertical axis. `f(x) = x^2` draws the classic U-shaped parabola you've seen before — and today's whole session is about precisely describing HOW STEEPLY that curve is rising or falling at any single point along it."*

### Average Rate of Change — A Warm-Up Using Only Arithmetic (7 min)

**Say:** *"Before derivatives, let's nail down a simpler, fully arithmetic idea: the AVERAGE rate of change between two points, which is just the familiar 'rise over run' slope formula from a straight line, applied to two points on our curve."*

**Write the formula:**

```
Average rate of change from x=a to x=b:

   f(b) - f(a)
   -----------
      b - a
```

**Live-code, verifying with `f(x) = x^2` between `x=2` and `x=3`:**

```python
def f(x):
    return x**2

a, b = 2, 3
avg_rate = (f(b) - f(a)) / (b - a)
print("f(2) =", f(a))
print("f(3) =", f(b))
print("Average rate of change from x=2 to x=3:", avg_rate)
```

**Example output (actual, verified — plain deterministic arithmetic):**
```
f(2) = 4
f(3) = 9
Average rate of change from x=2 to x=3: 5.0
```

**Say:** *"`(9 - 4) / (3 - 2) = 5` — exactly the slope of the straight line CONNECTING the two points `(2, 4)` and `(3, 9)` on the curve. This is a real, useful number, but notice it describes the AVERAGE steepness across that whole gap from `x=2` to `x=3` — it doesn't tell us how steep the curve is AT exactly `x=2`, or AT exactly `x=2.5`, specifically. That's the gap the derivative closes."*

### Shrinking the Gap — The Intuition Behind "Instantaneous" (8 min)

**Say:** *"Here's the key idea of this entire session, stated plainly before any formula: if we shrink the gap between our two points smaller and smaller — `x=2` to `x=2.1`, then `x=2` to `x=2.01`, then `x=2` to `x=2.001` — the AVERAGE rate of change over that shrinking gap should settle down and approach some specific number: the INSTANTANEOUS rate of change, exactly at `x=2`. Let's verify this happens, with real, verified numbers, rather than just asserting it."*

**Live-code:**

```python
a = 2
for gap in [1, 0.1, 0.01, 0.001, 0.0001]:
    b = a + gap
    avg_rate = (f(b) - f(a)) / (b - a)
    print(f"gap={gap}: average rate of change from x={a} to x={b} = {avg_rate}")
```

**Example output (actual, verified):**
```
gap=1: average rate of change from x=2 to x=3 = 5.0
gap=0.1: average rate of change from x=2 to x=2.1 = 4.1
gap=0.01: average rate of change from x=2 to x=2.01 = 4.01
gap=0.001: average rate of change from x=2 to x=2.001 = 4.000999999999479
gap=0.0001: average rate of change from x=2 to x=2.0001 = 4.000100000012054
```

**Say, pointing at the settling pattern:** *"Watch the numbers: `5.0`, `4.1`, `4.01`, `4.001...`, `4.0001...` — as the gap shrinks toward zero, the average rate of change is clearly settling toward exactly `4`, not toward some other number, and not bouncing around randomly. That settling-toward-a-fixed-number-as-the-gap-shrinks-to-zero IS the formal definition of a derivative — mathematicians call shrinking a gap toward zero 'taking a limit,' and the derivative of `f` at a point is defined as exactly this limit. We just watched it happen, with real numbers, instead of only being told the definition abstractly."*

### Comprehension Check (0 min — folded into SEGMENT 3's opening)

---

## SEGMENT 3: The Derivative — Slope of the Tangent Line (20 min)

### Naming What We Just Watched Happen (5 min)

**Say:** *"The number our shrinking-gap experiment settled toward — `4`, at `x=2`, for `f(x) = x^2` — is called the DERIVATIVE of `f` at `x=2`, written `f'(2)`. Geometrically, it's the slope of the TANGENT LINE: the single straight line that just barely touches the curve at that one point, matching its steepness EXACTLY at that point and nowhere else."*

**Write the formal limit definition on the board (for completeness — not the main teaching tool today, the shrinking-gap numbers already did the real teaching):**

```
f'(x) = lim (as h -> 0) of  [f(x+h) - f(x)] / h
```

**Say:** *"This formula is exactly what our Python loop just computed, for smaller and smaller values of `h` (our 'gap'). You don't need to memorize this formula to use derivatives correctly day to day — what matters is the INTUITION we just built: the derivative is the number the average-rate-of-change settles toward as the gap shrinks to nothing."*

### The Shortcut Formula for Power Functions (6 min)

**Say:** *"Calculus gives you shortcut formulas so you don't have to run a shrinking-gap experiment every single time. For `f(x) = x^n`, the derivative is `f'(x) = n * x^(n-1)` — a simple, mechanical rule. Let's verify it matches what we just found numerically."*

**Write on board:**

```
f(x) = x^2   ->   f'(x) = 2 * x^1 = 2x

At x=2:  f'(2) = 2 * 2 = 4
```

**Say:** *"`4` — exactly matching our shrinking-gap experiment's answer. This is not a coincidence; the shortcut formula and the limit definition are proven to always agree. From here on, we use the shortcut formula for speed, trusting it because we just independently verified it numerically for this specific case."*

### A Second Worked Example — Verifying the Shortcut on `x^3` (6 min)

**Say:** *"Let's test the shortcut formula on a different function, `f(x) = x^3`, at `x=2`, and verify numerically exactly like before, so we're not just trusting the pattern on a single example."*

**Write the shortcut prediction on the board:**

```
f(x) = x^3   ->   f'(x) = 3 * x^2

At x=2:  f'(2) = 3 * (2^2) = 3 * 4 = 12
```

**Live-code, verifying with the shrinking-gap method:**

```python
def g(x):
    return x**3

x2 = 2
for gap in [0.1, 0.01, 0.001]:
    slope = (g(x2 + gap) - g(x2)) / gap
    print(f"gap={gap}: average rate of change near x=2 = {slope}")

print("Shortcut formula prediction, f'(2) = 3 * 2^2:", 3 * 2**2)
```

**Example output (actual, verified):**
```
gap=0.1: average rate of change near x=2 = 12.610000000000001
gap=0.01: average rate of change near x=2 = 12.060099999999707
gap=0.001: average rate of change near x=2 = 12.006000999997823
Shortcut formula prediction, f'(2) = 3 * 2^2: 12
```

**Say:** *"Settling toward `12`, exactly matching the shortcut formula's prediction. Two different functions, two independent numerical verifications, both confirming the shortcut rule. This is the same 'trust but verify' spirit as every master class this course: we didn't just state the power rule and move on, we WATCHED it be true, twice, with our own printed numbers."*

### Comprehension Check (3 min)

1. *"What does `f'(x)` represent geometrically?"* (The slope of the tangent line to the curve at that specific point — the instantaneous rate of change, as opposed to the average rate of change across some gap.)
2. *"Using the shortcut power rule, what is the derivative of `f(x) = x^4` at `x=1`?"* (`f'(x) = 4x^3`, so `f'(1) = 4 * 1^3 = 4`.)

---

## BREAK (10 min)

*Suggested break prompt:* Ask students to predict: at the very BOTTOM of a U-shaped parabola (its minimum point), what do they think the slope of the tangent line equals, exactly? Come back ready to verify that prediction and use it to find a function's minimum directly.

---

## SEGMENT 4: Optimisation Intuition — Finding the Minimum (25 min)

### Resolving the Break Prediction — Slope at the Minimum (6 min)

**Say:** *"At the very bottom of a smooth U-shaped curve, the tangent line is perfectly FLAT — horizontal — meaning its slope is exactly ZERO. This single fact is the entire foundation of calculus-based optimisation: to find where a smooth function is at its minimum (or maximum), find where its derivative equals zero."*

**Write on board:**

```
f(x) = (x - 3)^2     <- a parabola with its minimum at x = 3

f'(x) = 2 * (x - 3)    <- by the power rule, treating (x-3) like a single variable (chain rule, not derived in detail today)

Set f'(x) = 0:   2 * (x - 3) = 0   =>   x - 3 = 0   =>   x = 3
```

**Live-code, verifying both that `x=3` gives `f'(x)=0` and that it really is the minimum:**

```python
def h(x):
    return (x - 3)**2

def h_prime(x):
    return 2 * (x - 3)

print("f'(3) =", h_prime(3))
print("f(3) =", h(3))
for x_test in [1, 2, 2.9, 3, 3.1, 4, 5]:
    print(f"f({x_test}) = {h(x_test)}")
```

**Example output (actual, verified):**
```
f'(3) = 0
f(3) = 0
f(1) = 4
f(2) = 1
f(2.9) = 0.010000000000000018
f(3) = 0
f(3.1) = 0.010000000000000018
f(4) = 1
f(5) = 4
```

**Say, pointing at the printed values:** *"`f'(3) = 0`, exactly confirming our algebra, AND `f(3) = 0` is clearly the smallest value in the whole printed list — every neighboring `x` value produces a LARGER `f(x)`, on both sides, and notice `f(2.9)` and `f(3.1)` come out EQUAL (`0.01`, modulo a tiny floating-point rounding artifact in the last digit) — a nice, symmetric confirmation that `x=3` really is sitting exactly at the bottom of this particular parabola. This is 'optimisation' in its purest, simplest form: a function with one lowest point, and calculus gives us a precise, algebraic way to find exactly where that point is, without having to check every possible `x` value by brute force."*

### Why This Matters for Machine Learning: the Error Function (8 min)

**Say:** *"Here's the connection to everything you've touched in Module 2 and will touch again: in machine learning, you don't usually care about minimizing `(x-3)^2` for its own sake — you care about minimizing an ERROR function (often called a LOSS function) that measures how WRONG a model's predictions are. The model has parameters (weights); the loss function tells you how bad those parameters currently are; and exactly the same idea — find where the loss function's slope is zero — tells you which parameter values make the model's predictions as good as possible."*

**Write on board:**

```
Today's toy example:        f(x) = (x - 3)^2          minimize over x
Real ML training (concept): loss(weights) = ...        minimize over weights

SAME core idea: find where the slope of the function (with respect to its input) is zero.
```

**Say:** *"The honest complication, which SEGMENT 5 addresses directly: real loss functions in machine learning usually have WAY more than one input variable — sometimes millions of weights simultaneously — and setting every single derivative to exactly zero and solving algebraically, like we just did by hand for `x=3`, becomes computationally infeasible. Gradient descent is the practical workaround: instead of solving for the zero-slope point directly, you use the slope at your CURRENT point to repeatedly nudge your way toward it, step by step."*

### Positive Slope, Negative Slope — Which Way Is "Downhill"? (7 min)

**Say:** *"One more piece of intuition before we build the full gradient descent algorithm: the SIGN of the derivative tells you which direction is downhill from where you're standing."*

**Live-code:**

```python
for x_test in [0, 1, 2, 3, 4, 5, 6]:
    print(f"x={x_test}: f'(x) = {h_prime(x_test)}")
```

**Example output (actual, verified):**
```
x=0: f'(x) = -6
x=1: f'(x) = -4
x=2: f'(x) = -2
x=3: f'(x) = 0
x=4: f'(x) = 2
x=5: f'(x) = 4
x=6: f'(x) = 6
```

**Say, drawing the connection explicitly:** *"To the LEFT of the minimum (`x < 3`), the derivative is NEGATIVE — meaning the function is DECREASING as `x` increases, so increasing `x` moves you downhill, toward the minimum. To the RIGHT of the minimum (`x > 3`), the derivative is POSITIVE — the function is INCREASING as `x` increases, so you'd need to DECREASE `x` to move downhill instead. Notice the pattern: moving in the OPPOSITE direction of the derivative's sign always moves you downhill, toward lower `f(x)` values, regardless of which side of the minimum you're standing on. That single observation is the entire mechanical idea behind gradient descent's update rule, which we build next."*

### Comprehension Check (4 min)

1. *"At a function's minimum point, what does the derivative equal, exactly?"* (Zero — the tangent line is perfectly flat/horizontal at that point.)
2. *"If `f'(x)` is positive at your current `x`, which direction — increasing or decreasing `x` — moves you downhill, toward a lower `f(x)` value?"* (Decreasing `x` — a positive derivative means the function is increasing as `x` increases, so moving opposite to that direction decreases `f(x)`.)

---

## SEGMENT 5: Gradient Descent — Walking Downhill, Step by Step (20 min)

### The Update Rule (6 min)

**Say:** *"Gradient descent is a repeated, mechanical procedure: at your current `x`, compute the derivative `f'(x)`; take a small step in the OPPOSITE direction of that derivative's sign (since SEGMENT 4 just showed that's downhill); repeat. The 'small step' size is controlled by a number called the learning rate, usually written `alpha` or `lr`."*

**Write the update rule on the board:**

```
x_new = x_old - (learning_rate * f'(x_old))
```

**Say:** *"Notice the MINUS sign — this is exactly what encodes 'go opposite to the derivative's sign, i.e. downhill' from SEGMENT 4's observation. If `f'(x_old)` is positive, subtracting a positive number DECREASES `x`, moving you leftward/downhill, matching exactly what we verified a moment ago. If `f'(x_old)` is negative, subtracting a negative number INCREASES `x`, moving you rightward/downhill — also exactly matching."*

### A Fully Verified, Hand-Traceable Gradient Descent Run (10 min)

**Say:** *"Let's trace this by hand AND in code, for our familiar `f(x) = (x-3)^2`, starting at `x=0` — deliberately far from the known minimum at `x=3` — with a reasonable learning rate of `0.1`."*

**Live-code:**

```python
def h_prime(x):
    return 2 * (x - 3)

def h(x):
    return (x - 3)**2

x = 0.0
lr = 0.1
print(f"start: x={x}, f(x)={h(x)}")
for step in range(1, 11):
    grad = h_prime(x)
    x = x - lr * grad
    print(f"step {step}: grad={grad:.4f}, new x={x:.6f}, f(x)={h(x):.6f}")
```

**Example output (actual, verified by running this exact code):**
```
start: x=0.0, f(x)=9.0
step 1: grad=-6.0000, new x=0.600000, f(x)=5.760000
step 2: grad=-4.8000, new x=1.080000, f(x)=3.686400
step 3: grad=-3.8400, new x=1.464000, f(x)=2.359296
step 4: grad=-3.0720, new x=1.771200, f(x)=1.509949
step 5: grad=-2.4576, new x=2.016960, f(x)=0.966368
step 6: grad=-1.9661, new x=2.213568, f(x)=0.618475
step 7: grad=-1.5729, new x=2.370854, f(x)=0.395824
step 8: grad=-1.2583, new x=2.496684, f(x)=0.253327
step 9: grad=-1.0066, new x=2.597347, f(x)=0.162130
step 10: grad=-0.8053, new x=2.677877, f(x)=0.103763
```

**Say, hand-tracing step 1 explicitly on the board before moving on:** *"Start at `x=0`. `f'(0) = 2*(0-3) = -6`. Update: `x_new = 0 - (0.1 * -6) = 0 - (-0.6) = 0.6`. Exactly matching the printed `step 1` line. Notice `f(x)` DECREASES every single step — `9.0`, `5.76`, `3.69`, steadily shrinking toward `0` — and `x` steadily climbs toward `3`, the true minimum we found algebraically in SEGMENT 4, getting closer and closer without yet exactly reaching it after 10 steps. This gradual, step-by-step approach to the true minimum, rather than jumping there in one algebraic leap, is exactly what 'training' a model means in practice: many small, slope-guided steps, not one big calculation."*

### What Happens with a Learning Rate That's Too Large (4 min)

**Say:** *"Learning rate isn't a free parameter you can set arbitrarily large to 'converge faster' — let's verify, with real numbers, what happens if we set `lr=1.1` instead of `0.1` on the exact same function and starting point."*

**Live-code:**

```python
x = 0.0
lr = 1.1
for step in range(1, 7):
    grad = h_prime(x)
    x = x - lr * grad
    print(f"step {step}: grad={grad:.4f}, new x={x:.4f}, f(x)={h(x):.4f}")
```

**Example output (actual, verified by running this exact code):**
```
step 1: grad=-6.0000, new x=6.6000, f(x)=12.9600
step 2: grad=7.2000, new x=-1.3200, f(x)=18.6624
step 3: grad=-8.6400, new x=8.1840, f(x)=26.8739
step 4: grad=10.3680, new x=-3.2208, f(x)=38.6984
step 5: grad=-12.4416, new x=10.4650, f(x)=55.7256
step 6: grad=14.9299, new x=-5.9580, f(x)=80.2449
```

**Say, pointing at the clearly worsening `f(x)` column:** *"`f(x)` is GROWING every step — `12.96`, `18.66`, `26.87`, `38.70`, climbing further and further from the true minimum of `0`, not approaching it. This is real, verified DIVERGENCE: the step size, `lr * grad`, is so large that each update doesn't just move downhill, it OVERSHOOTS past the minimum entirely and lands even further uphill on the OTHER side, and this overshoot compounds and gets WORSE each step rather than self-correcting. This is precisely why 'learning rate' is one of the most important and most frequently discussed tunable settings in any real machine learning training run — too small wastes time converging slowly; too large can actively diverge, exactly as verified here."*

### Comprehension Check (0 min — folded into the lab)

---

## SEGMENT 6: Lab — Hand-Traced and Verified Gradient Descent (10 min)

### Instructions (read aloud, step by step)

1. By hand, compute `f'(x)` for `f(x) = (x - 5)^2` as a general formula (same pattern as SEGMENT 4/5's `(x-3)^2` example, just shifted).
2. By hand, predict where the minimum is (i.e. where `f'(x) = 0`).
3. Write `f(x)` and `f_prime(x)` in Python and verify your hand prediction by checking `f_prime` at your predicted minimum equals `0`.
4. Run 5 steps of gradient descent starting at `x=0`, with `lr=0.2`, and print `x` and `f(x)` at each step.
5. Confirm `x` is moving toward your predicted minimum and `f(x)` is decreasing every step.

### Starter Code

```python
def f(x):
    return (x - 5)**2

def f_prime(x):
    return ___  # fill in, by hand first: derivative of (x-5)^2

# Step 2/3: verify your predicted minimum
predicted_minimum = ___
print("f_prime at predicted minimum:", f_prime(___))

# Step 4: gradient descent trace
x = 0.0
lr = 0.2
for step in range(1, 6):
    grad = ___
    x = x - ___ * ___
    print(f"step {step}: grad={grad:.4f}, new x={x:.4f}, f(x)={f(x):.4f}")
```

### Reference Solution

```python
def f(x):
    return (x - 5)**2

def f_prime(x):
    return 2 * (x - 5)

# By hand: f'(x) = 2*(x-5); setting 2*(x-5)=0 gives x=5
predicted_minimum = 5
print("f_prime at predicted minimum:", f_prime(predicted_minimum))

x = 0.0
lr = 0.2
for step in range(1, 6):
    grad = f_prime(x)
    x = x - lr * grad
    print(f"step {step}: grad={grad:.4f}, new x={x:.4f}, f(x)={f(x):.4f}")
```

**Example output (actual, verified by running this exact code):**
```
f_prime at predicted minimum: 0
step 1: grad=-10.0000, new x=2.0000, f(x)=9.0000
step 2: grad=-6.0000, new x=3.2000, f(x)=3.2400
step 3: grad=-3.6000, new x=3.9200, f(x)=1.1664
step 4: grad=-2.1600, new x=4.3520, f(x)=0.4199
step 5: grad=-1.2960, new x=4.6112, f(x)=0.1512
```

**Say:** *"`f_prime(5) = 0` confirms the hand-predicted minimum exactly. And the trace itself: `x` climbs `0.0 -> 2.0 -> 3.2 -> 3.92 -> 4.352 -> 4.6112`, steadily approaching `5` without yet reaching it after 5 steps, while `f(x)` shrinks every single step — `9.0, 3.24, 1.1664, 0.4199, 0.1512` — exactly the same converging pattern verified for `(x-3)^2` in SEGMENT 5, just shifted to a different minimum."*

**Instructor circulates**, checking specifically that students derived `f_prime` correctly BY HAND first (`2*(x-5)`, not `2*(x-3)` copy-pasted unchanged from the lecture's running example — a very easy mistake given how similar the two functions look), and that they predicted the minimum (`x=5`) themselves before verifying it in code, matching the "predict first, verify second" discipline used throughout Session 3 and this session.

---

## SEGMENT 7: Summary, Wrap-Up & Q&A (5 min)

**What we covered today:**
- A function's rate of change, built up from average rate of change over a shrinking gap, to the derivative as the exact, instantaneous limit
- The derivative as the slope of the tangent line, verified numerically against the power-rule shortcut formula for two different functions
- Optimisation as "find where the slope is zero," verified by hand and in code for a simple parabola
- Gradient descent's update rule, traced step by step with a working learning rate, and verified to diverge with a too-large one

**Bridge to next session:** *"Today's math — slope, and walking downhill using that slope — is running underneath essentially every 'the model is training' moment you'll ever hear about in this field, usually applied simultaneously across millions of parameters instead of the one variable we traced by hand today, but the exact same update rule, step by step. You won't need to hand-derive gradient descent again, but you'll now recognize the term precisely whenever it comes up. Next session moves back into hands-on building: Session 11 constructs a full Retrieval-Augmented Generation (RAG) pipeline, combining Session 8's embeddings, Session 9's chunking and vector stores, and Session 6/7's LangChain chains into one complete, working system."*

**Homework / self-practice:**
1. By hand, find the derivative and the minimum of `f(x) = (x + 2)^2`, then verify both in Python exactly like SEGMENT 6's lab.
2. Run gradient descent on `f(x) = (x-3)^2` starting at `x=10` instead of `x=0`, with `lr=0.1`, for 10 steps, and confirm it still converges toward `x=3` from the other side.
3. Try `lr=0.5` on `f(x)=(x-3)^2` starting at `x=0` for 5 steps. Is this learning rate "too large" like `lr=1.1`, "reasonable" like `lr=0.1`, or something in between? Run it and report what you actually observe, rather than guessing.

---

## Q&A & Doubt Solving

**Likely questions and suggested answers:**

**Q: Does every function have a single, easy-to-find minimum like today's `(x-3)^2` examples?**
→ No — many real functions (including most real machine learning loss functions) have much more complicated shapes, sometimes with multiple local dips (local minima) that aren't the lowest possible point overall (the global minimum). Gradient descent, as shown today, finds a point where the slope is zero, but doesn't automatically guarantee that's the best possible point overall if the function's shape is more complex than today's simple parabola — a genuinely important, more advanced topic beyond today's scope.

**Q: Today's examples only had ONE input variable, `x`. What changes with many variables, like a real model's millions of weights?**
→ The core idea is identical, applied once per variable: compute the slope with respect to EACH variable separately (collectively called the gradient, a vector of all those individual slopes), then update ALL variables simultaneously using the same `x_new = x_old - lr * gradient` rule, just with vectors instead of single numbers. This connects directly back to Session 3's vector math — the gradient IS a vector, and updating many weights at once is vector subtraction, exactly like Session 3 SEGMENT 2's vector addition/subtraction.

**Q: Is there always a "correct" learning rate you should just know in advance?**
→ No — the right learning rate depends on the specific function/loss being optimized and is usually found through experimentation, not calculated in advance. SEGMENT 5 verified two extremes (`0.1` converges nicely, `1.1` diverges) precisely to build the intuition that this value matters a great deal and has real failure modes, not to suggest `0.1` is a universal correct answer for every problem.

**Q: Why do we SUBTRACT the learning-rate-scaled derivative, instead of adding it?**
→ Subtracting is what encodes "move opposite to the slope's sign, i.e. downhill," verified explicitly in SEGMENT 4/5: a positive slope means subtracting moves you left (down), a negative slope means subtracting a negative number moves you right (also down). Adding instead of subtracting would walk UPHILL every time — toward a maximum, not a minimum — which is the opposite of what training a model to reduce its error requires.

**Q: Could gradient descent ever land EXACTLY on the true minimum, or does it only ever get arbitrarily close?**
→ With a fixed learning rate and the simple update rule shown today, it typically gets closer and closer but may not land EXACTLY on the true minimum in a finite number of steps (notice SEGMENT 5's 10-step trace reached `x=2.677877`, still short of exactly `3`). In practice, "close enough" within some small tolerance is the real, practical stopping criterion used, rather than insisting on mathematically exact convergence.

---

## Instructor Notes

- **Prerequisite check:** Confirm in the first five minutes that students recall basic function notation (`f(x)`, plugging in a value) and exponents — today's SEGMENT 2 depends on that feeling natural, not newly introduced. This master class does NOT require Session 3's vector material as a hard prerequisite, though the Q&A draws a connection to it for students who remember it well.
- **Common mistake:** Confusing the derivative `f'(x)` (a function describing slope at every point) with a single derivative VALUE at one specific point, like `f'(2)` — be explicit on the board about which one is being discussed at each step, especially in SEGMENT 3.
- **Another common mistake:** In the SEGMENT 6 lab, copy-pasting `f_prime` from the lecture's running `(x-3)^2` example without updating it for the lab's own `(x-5)^2` function — walk past screens specifically checking this, since the two functions look extremely similar on the page.
- **Another common mistake:** Forgetting the MINUS sign in the gradient descent update rule, which flips the direction entirely and would cause `x` to walk UPHILL, away from the minimum, instead of downhill toward it — if a student's lab trace shows `f(x)` INCREASING every step instead of decreasing, check this first.
- **Engagement tip:** SEGMENT 5's "what happens with `lr=1.1`" divergence demo is usually the strongest "aha" moment of the session — the `f(x)` column visibly growing instead of shrinking is a vivid, concrete illustration of a very commonly-discussed real training failure mode ("the loss exploded" / "training diverged"). Don't rush past it.
- **Time check:** If running behind before the break, shorten SEGMENT 3's second worked example (`x^3`) to stating the shortcut-formula match verbally instead of a full live-coded shrinking-gap walkthrough.
- **If running long after the break:** Compress SEGMENT 5's too-large-learning-rate demo to reporting the final `f(x)` value only, instead of walking through all 6 printed steps individually.
- **Materials to prepare:** Whiteboard with pre-drawn U-shaped parabola axes for SEGMENT 2/4's curve-sketching; scratch notebook with all of today's verified code pre-typed, since every single number in this script has been checked by actually running it (or by exact hand arithmetic) and is safe to state as fact; double-check the SEGMENT 6 Reference Solution trace by re-running it fresh before class, per that section's own instructor note.

---

## Common Errors — Quick Reference

| Bug / mistake | Symptom | Fix |
|---|---|---|
| Confusing average rate of change (over a gap) with instantaneous rate of change (the derivative, at one point) | Misinterprets a two-point slope calculation as "the" derivative without shrinking the gap first | Reinforce SEGMENT 2's shrinking-gap experiment: the derivative is what the average rate of change SETTLES toward as the gap shrinks to zero, not any single average-rate-of-change calculation on its own |
| Forgetting the minus sign in the gradient descent update rule | `x` moves uphill (away from the minimum) instead of downhill; `f(x)` increases every step instead of decreasing | Always write `x_new = x_old - lr * f_prime(x_old)`, and verify by checking that `f(x)` decreases each step before trusting a longer trace |
| Reusing a previous example's derivative formula unchanged for a new function | Lab's `(x-5)^2` traced with `(x-3)^2`'s derivative, producing a wrong predicted minimum and a trace that doesn't actually converge where expected | Always re-derive (or at minimum carefully re-check) the derivative formula by hand for each NEW function, rather than copying a previous one |
| Assuming a larger learning rate always converges faster | Learning rate set too high (verified: `lr=1.1` on today's example) causes divergence instead of faster convergence | Treat learning rate as a value to tune and verify empirically (watch whether `f(x)` is decreasing), not simply "bigger is faster" |
| Treating "derivative equals zero" as automatically "the global minimum" | Assumes every zero-derivative point is the best possible point, even for more complex, non-parabola-shaped functions | Note explicitly (see Q&A) that zero-slope points can be local minima, local maxima, or saddle points for more complex functions; today's parabola examples are a deliberately simple, well-behaved special case |

---

## Appendix: NumPy/SymPy Verification of Today's Examples (Optional, If Time Allows)

**Say (if running this appendix):** *"Everything today was computed with plain Python arithmetic, on purpose, so every operation stayed fully visible. If `sympy` (Python's symbolic math library) is available, it can compute an exact symbolic derivative formula directly, which we can compare against today's hand-derived shortcut-rule formulas."*

```python
import sympy as sp

x = sp.Symbol('x')
expr = (x - 3)**2
derivative = sp.diff(expr, x)
print("Symbolic derivative of (x-3)^2:", derivative)
print("Evaluated at x=3:", derivative.subs(x, 3))
```

**Example output (illustrative syntax — `sympy`'s exact simplified display form can vary slightly by version; the MATHEMATICAL result, `2*(x-3)` simplifying to `2*x - 6`, and evaluating to `0` at `x=3`, is a correct, well-established symbolic-math fact, consistent with this script's own hand-derived and numerically-verified `f'(x) = 2*(x-3)`):**
```
Symbolic derivative of (x-3)^2: 2*x - 6
Evaluated at x=3: 0
```

**Say:** *"`2*x - 6` is the fully expanded version of `2*(x-3)` — same formula, just distributed out — and it evaluates to exactly `0` at `x=3`, matching everything we derived and verified by hand and with plain Python earlier. `sympy` isn't doing different math; it's doing the identical algebra automatically, which is genuinely useful once functions get more complicated than today's simple examples."*

---

## Appendix: Derivative Shortcut Rules Used Today (Instructor Reference)

| Function | Derivative | Used in |
|---|---|---|
| `f(x) = x^n` | `f'(x) = n * x^(n-1)` | SEGMENT 3 (`x^2`, `x^3`) |
| `f(x) = (x - a)^2` | `f'(x) = 2 * (x - a)` | SEGMENT 4/5/6 (`(x-3)^2`, `(x-5)^2`) — a direct application of the power rule combined with the chain rule, not derived from scratch in this session |
| `f(x) = c` (a constant) | `f'(x) = 0` | Mentioned implicitly: a flat, unchanging function has zero slope everywhere, consistent with "slope describes change" |

---

## FAQ — Additional Questions

**Q: Is "gradient" just another word for "derivative," or are they different things?**
→ "Derivative" typically refers to the single-variable case (one input, like today's `x`). "Gradient" is the natural generalization to MULTIPLE input variables simultaneously — a vector containing the derivative with respect to each variable separately. Today's whole session used "derivative" throughout since every example had exactly one variable; "gradient descent" as a NAME is standard even in the one-variable case, since it's the general name for the whole technique.

**Q: Does gradient descent require the function to be a smooth parabola like today's examples?**
→ No — gradient descent works (mechanically) on any function where you can compute a derivative/gradient at a given point, including much more complex, bumpy, high-dimensional functions. Today's parabola examples were chosen specifically because they're simple and well-behaved enough to verify completely by hand; real loss functions are far more complex, but the exact same update rule applies.

**Q: Why not just solve `f'(x) = 0` directly and algebraically, like we did in SEGMENT 4, instead of the iterative gradient descent process in SEGMENT 5?**
→ For simple functions like today's examples, solving directly IS easier and exact, and SEGMENT 4 did exactly that. Gradient descent earns its keep specifically when direct algebraic solving becomes impractical — real loss functions with millions of parameters are far too complex to solve for "where every derivative equals zero simultaneously" in closed form, so the iterative, step-by-step approach becomes the only practical option.

---

## Materials Checklist

- [ ] Whiteboard with pre-drawn U-shaped parabola axes for SEGMENT 2/4
- [ ] Scratch notebook with all of today's verified code pre-typed and RE-RUN fresh before class (every number in this script was checked by actually running it or by exact hand arithmetic)
- [ ] Printed or projected gradient descent update rule (`x_new = x_old - lr * f'(x_old)`) for SEGMENT 5
- [ ] Optional: `sympy` available for the supplemental symbolic-verification appendix
- [ ] Timer visible for the lab segment

---

## Timing Contingencies

| Situation | Action |
|---|---|
| Running 10 min behind before break | Shorten SEGMENT 3's second worked example (`x^3`) to stating the shortcut-formula match verbally instead of a full shrinking-gap walkthrough |
| Running long after break | Compress SEGMENT 5's too-large-learning-rate demo to reporting the final `f(x)` value only, instead of all 6 steps |
| Low energy after lunch/break | Run SEGMENT 4's "slope at the minimum" break-prediction reveal as an interactive group-guess activity before confirming with the live printed values |
| Advanced group finishes lab early | Have them retry the SEGMENT 6 lab with `lr=0.05` and `lr=0.4`, comparing convergence speed, as an informal preview of homework item 3 |
| No shared screen / projector issue | Draw every curve and trace every gradient descent step on the whiteboard from this script's exact verified numbers |

---

## End-of-Session Quiz (5 Questions)

1. What is the difference between the average rate of change over a gap and the instantaneous rate of change (the derivative) at a single point?
2. Using the power rule, what is the derivative of `f(x) = x^5` at `x=2`?
3. At a smooth function's minimum point, what does its derivative equal, and why, geometrically?
4. Write the gradient descent update rule, and explain what the minus sign accomplishes.
5. In this session's verified example, what happened to `f(x)` over 6 steps when the learning rate was set to `1.1` instead of `0.1`, and why?

**Answer key (instructor):**
1. Average rate of change is the slope of the straight line connecting two distinct points on the curve; the derivative is what that average rate of change settles toward as the gap between the two points shrinks to zero — the exact, instantaneous slope at one single point.
2. `f'(x) = 5x^4`, so `f'(2) = 5 * 2^4 = 5 * 16 = 80`.
3. Exactly zero — geometrically, the tangent line at the minimum is perfectly flat/horizontal, since the curve is neither rising nor falling at that exact point.
4. `x_new = x_old - (learning_rate * f'(x_old))`. The minus sign ensures you move OPPOSITE to the derivative's sign, which SEGMENT 4 established is always the downhill direction, toward a lower function value.
5. Verified: `f(x)` grew every step (`12.96, 18.66, 26.87, 38.70, 55.73, 80.24`) instead of shrinking, because the oversized step caused each update to overshoot past the minimum and land further uphill on the opposite side, with the overshoot compounding worse each step — real divergence, not slow convergence.

---

## Homework Rubric

| Criterion | Excellent (4) | Good (3) | Needs Work (2) | Incomplete (1) |
|---|---|---|---|---|
| `(x+2)^2` derivative + minimum, hand-derived and verified | Correct hand derivation, correct Python verification matching the hand prediction | Correct answer, verification present, hand work thin | Correct final answer only, no hand derivation shown | Not attempted |
| Gradient descent from `x=10` toward the `x=3` minimum, 10 steps | Runs correctly, clearly confirms convergence from the opposite side, `f(x)` strictly decreasing | Runs correctly, thin discussion of convergence | Runs with errors or doesn't actually confirm convergence | Not attempted |
| `lr=0.5` classification (too large / reasonable / in between) + actual run | Ran the actual code, correctly classifies based on REAL observed behavior, not a guess | Ran the code, classification reasonable but thinly justified | Classification given without actually running the code | Not attempted |

**Total:** /12 — Pass threshold: 8/12
