# Lecture Script: Master Class — The Mathematics Behind Learning: Lines, Curves & Errors
> **Instructor Reference** — Module 2: Classical ML | Session 5 | Duration: 2 Hours

---

## Session Overview

**Goal:** Students open up the black box they have been calling `.fit()`. By the end they can, on paper, write a line's equation, compute every residual, square them into a single error number, sketch that error as a bowl-shaped curve, and take a gradient-descent step by hand — then reproduce all of it in twenty lines of NumPy.

**Student profile at this point:** They have already trained Linear Regression, Ridge and Lasso (Session 3) and evaluated them with MSE, RMSE and R² (Session 4). They have used `.fit()` many times and it has always worked. **They have never once been told what it does.** From Module 1 they know slope, scatter plots, mean and standard deviation. They have never met a derivative in this course.

**Key outcome:** A hand-written gradient descent loop that finds the same slope `np.polyfit` finds.

**Tone for this session:** A **master class**, not a library tutorial. Chalk before code — every idea is worked by hand first and only then verified in NumPy. scikit-learn is deliberately almost absent today. Slow down; let silences happen while people compute.

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| Opening — What Does `.fit()` Actually Do? | 5 min | 0:05 |
| **Concept 1:** y = mx + c — Reading a Line in Real Units | 10 min | 0:15 |
| **Practical 1:** Two points, one line — by hand, then NumPy | 15 min | 0:30 |
| **Concept 2:** Residuals, and Why We Square Them | 10 min | 0:40 |
| **Practical 2:** Residual table and SSE by hand, then vectorised | 15 min | 0:55 |
| **BREAK** | 10 min | 1:05 |
| **Concept 3:** The Error Bowl and the Meaning of a Derivative | 10 min | 1:15 |
| **Practical 3:** Plot the bowl; watch a secant become a tangent | 15 min | 1:30 |
| **Concept 4:** Gradient Descent — Walking Downhill in Fog | 10 min | 1:40 |
| **Practical 4:** A hand-written gradient descent loop | 10 min | 1:50 |
| Summary & Wrap-Up | 5 min | 1:55 |
| Q&A & Doubt Solving | 5 min | 2:00 |

---

## Opening (5 min)

**Do this, live, in front of them.** Type these three lines and run them:

```python
from sklearn.linear_model import LinearRegression
model = LinearRegression().fit(X, y)
print(model.coef_, model.intercept_)
```

Let it print. Then ask:

*"You have all run this. It took forty milliseconds. Now tell me — in the forty milliseconds between the dot and the fit, what did the machine actually DO? Not 'it learnt.' Not 'it found the best line.' What arithmetic did it perform?"*

Let the room go quiet. That silence is the whole reason today's session exists.

**What today is NOT:**
- It is **not** a scikit-learn session. We will barely import it.
- It is **not** a proof-heavy calculus lecture. No limits notation, no chain rule.
- It is **not** about memorising formulas. If you memorise, you have missed it.

**What today IS:**
- It **is** the four-step engine that sits inside every model you will ever train: *guess a line → measure the gaps → square them into one number → walk that number downhill.*
- It **is** the one session where you will do the machine's job with a pen, so the machine stops being magic.
- It **is** the foundation for neural networks in Module 3 — they use this exact same loop, just with millions of `m` values instead of one.

**Write the spine of the session on the board and leave it there all class:**

```
       y = mx + c   →   residual   →   MSE   →   the bowl   →   downhill
        (the line)     (the gaps)   (one number)  (a curve)   (the learning)
```

---

## Concept Block 1: y = mx + c — Reading a Line in Real Units (10 min)

### The equation, anchored in something they paid for this week

**Board it as an autorickshaw meter, not as algebra:**

```
fare = 15 × km + 25          y = m·x + c
       │         └── c: flag-down charge, the value of y when x = 0
       └──────────── m: the rate, how much y moves for +1 of x
```

Every kilometre adds ₹15. Ask: *"What is the fare for a zero-kilometre ride?"* — ₹25. **That is the intercept.** It is what the line reports when the input is nothing at all.

### Slope is rise over run — and it has units

**Board this triangle:**

```
        rent
         │                          ● (900, 50000)
   50000 │                        ╱ │
         │                      ╱   │  rise = 18000
         │                    ╱     │
   32000 │          ● ──────╱───────┘
         │       (500, 32000)  run = 400
         └──────────────────────────────── size (sq ft)
```

```
m = rise / run = (50000 - 32000) / (900 - 500) = 18000 / 400 = 45
```

**Now the sentence that matters — say it slowly:**

*"m = 45 does not mean 'forty-five'. It means* **forty-five rupees per square foot per month.** *Every single extra square foot you rent costs you ₹45 more. That is not a number. That is a finding. That is the entire output of a regression model, in one English sentence."*

| Slope | Reads as | Sanity check |
|---|---|---|
| `m = 45` on rent vs sq ft | ₹45 more rent per extra sq ft | Plausible for a metro |
| `m = 7.1` on marks vs hours | 7.1 more marks per extra study hour | Plausible |
| `m = -0.8` on score vs hours of TV | 0.8 marks *lost* per TV hour | Negative slope = downhill line |
| `m = 0` | x tells you nothing about y | The flat line — the null model |

**Drive the point home:** always read `m` back in the units of your columns. A model that says `m = 45` and a model that says `m = 45,000` are telling wildly different stories, and only the units reveal which one is nonsense.

---

## Practical Block 1: Two Points, One Line (15 min)

### By hand first — 6 minutes, pens down on keyboards

Put this on the board. It is our dataset for the whole session: six flats in a Pune suburb.

```
size (100s of sq ft) |  4    5    6    7    8    9
monthly rent (₹ 000) | 17   21   22   27   29   33
```

Ask everyone to compute the slope through **only the first and the last points**, `(4, 17)` and `(9, 33)`, then through `(4, 17)` and `(8, 29)`.

- Through (4,17) and (8,29): `m = (29 - 17) / (8 - 4) = 12 / 4 = 3`
- Intercept from (4,17): `c = y - m·x = 17 - 3(4) = 17 - 12 = 5`
- **Our candidate line: `rent = 3 × size + 5`**

*"Translate that for me."* → **₹3,000 more rent per extra 100 sq ft — that is ₹30 per square foot — on top of a ₹5,000 base.**

### Then verify it in code — 9 minutes

```python
import numpy as np
import matplotlib.pyplot as plt

# Six flats. size in hundreds of sq ft, rent in thousands of rupees.
size = np.array([4., 5., 6., 7., 8., 9.])
rent = np.array([17., 21., 22., 27., 29., 33.])

# The line we built by hand from two points
m, c = 3.0, 5.0
pred = m * size + c
print("Our line: rent =", m, "x size +", c)
print("Predictions:", pred)          # -> [17. 20. 23. 26. 29. 32.]

# Three candidate lines, same intercept, different slopes
plt.figure(figsize=(9, 5))
plt.scatter(size, rent, s=110, color='steelblue', zorder=5, label='Actual flats')
grid = np.linspace(3.5, 9.5, 50)
for guess, style in [(2.5, 'r--'), (3.0, 'g-'), (3.5, 'm--')]:
    plt.plot(grid, guess * grid + 5, style, lw=2, label=f'm = {guess}')
plt.xlabel('Size (hundreds of sq ft)')
plt.ylabel('Monthly rent (₹ thousands)')
plt.title('Which slope fits best?')
plt.legend(); plt.grid(alpha=0.3); plt.show()
```

**Live walk-through:** Point at the red line (`m = 2.5`) — *"too flat, it sails under the big flats."* Point at the magenta (`m = 3.5`) — *"too steep, it flies over them."* Then ask the room the question that sets up the rest of the class: **"You can all SEE that green is best. But how would a computer, which cannot see, know that? It needs a number. What number?"**

That number is coming in the next block. Do not answer it yet.

---

## Concept Block 2: Residuals, and Why We Square Them (10 min)

### The residual

**Board:**

```
residual = actual − predicted
```

Positive residual → the dot is **above** the line → we under-predicted.
Negative residual → the dot is **below** the line → we over-predicted.

Take one flat from the table: size = 6 (i.e. 600 sq ft). Our line says `3(6) + 5 = 23`. Reality says `22`.

```
residual = 22 − 23 = −1     (we asked for ₹1,000 too much rent)
```

*"Every dot has its own residual. Six dots, six residuals. Now I need to squash six numbers into one score, so I can compare lines."*

### Attempt 1: just add them up. It fails.

Do this on the board with the real numbers — it lands harder when they see it collapse.

| size | actual | predicted (3x+5) | residual |
|---|---|---|---|
| 4 | 17 | 17 | 0 |
| 5 | 21 | 20 | +1 |
| 6 | 22 | 23 | −1 |
| 7 | 27 | 26 | +1 |
| 8 | 29 | 29 | 0 |
| 9 | 33 | 32 | +1 |

Sum of residuals = `0 + 1 − 1 + 1 + 0 + 1 = +2`. Nearly zero. *"So this line is nearly perfect? Careful — a line that is ₹10,000 too high on one flat and ₹10,000 too low on the next also sums to zero. Adding raw residuals lets mistakes cancel. A dart 10 cm left and a dart 10 cm right is not a bullseye."*

### Attempt 2: square them. It works.

```
SSE = Σ (actual − predicted)²          Sum of Squared Errors
MSE = SSE / n                          Mean Squared Error  (Session 4 — now you know why)
```

```
SSE = 0² + 1² + (−1)² + 1² + 0² + 1² = 0 + 1 + 1 + 1 + 0 + 1 = 4
MSE = 4 / 6 = 0.667
```

**Squaring buys you two things, and you must say both out loud:**

1. **Negatives cannot cancel.** `(−1)² = (+1)² = 1`. Error only ever accumulates.
2. **Big misses are punished disproportionately.** Ten residuals of 1 contribute `10`. One residual of 10 contributes `100`. The model will *bend itself* to fix the single worst point. (This is exactly why one outlier can wreck a regression — and why the squaring choice has consequences you feel in real projects.)

**Then say the sentence that unlocks the second half of the session:**

*"MSE = 0.667 is not just a report card. It is a score attached to the slope m = 3. Change m, and you get a different score. So MSE is a **function of m**. And functions of one variable can be plotted. What do you think that plot looks like?"*

---

## Practical Block 2: Residuals and SSE — By Hand, Then Vectorised (15 min)

### Their turn — 5 minutes, on paper

Give them `m = 2.5, c = 5` and the same six flats. Ask for the residual table and the SSE. Walk around; let people struggle. The answer (`SSE = 86.75`) should feel *shockingly* worse than 4 — that is the point.

### Now the code — 10 minutes

```python
# NOTE: `size` and `rent` are already defined from Practical 1.
import numpy as np
import pandas as pd

size = np.array([4., 5., 6., 7., 8., 9.])
rent = np.array([17., 21., 22., 27., 29., 33.])

def error_report(m, c=5.0):
    """Residuals, SSE and MSE for the line rent = m*size + c."""
    pred = m * size + c
    resid = rent - pred                      # actual - predicted
    sse = np.sum(resid ** 2)                 # squares, so nothing cancels
    mse = np.mean(resid ** 2)                # = sse / n
    return pred, resid, sse, mse

pred, resid, sse, mse = error_report(3.0)
print(pd.DataFrame({
    'size': size, 'actual': rent, 'predicted': pred,
    'residual': resid, 'squared': resid ** 2
}))
print(f"\nSum of raw residuals : {resid.sum():.2f}   <- misleadingly small!")
print(f"SSE : {sse:.2f}")
print(f"MSE : {mse:.3f}")

# Now score three different slopes with the SAME function
print("\n--- One number per slope ---")
for guess in [2.5, 3.0, 3.5]:
    _, _, s, mm = error_report(guess)
    print(f"m = {guess}  ->  SSE = {s:7.2f}   MSE = {mm:6.3f}")
```

The three SSE values print as roughly `86.75`, `4.00`, `56.75`. Ask: *"Read those three numbers left to right. High, low, high. What shape is that?"* — Someone will say "a U". **Write "U" on the board and circle it.** That is the error bowl, and they discovered it themselves.

**Live walk-through:** Highlight that `error_report` never looks at the data plot — it only ever returns *one number* for *one slope*. That is the interface the machine works through. It cannot see the scatter; it can only ask "how bad is m = 3?" and get back `0.667`.

---

## BREAK (10 min)

*Something to chew on: you just scored three slopes and got a U-shape. You could score a thousand slopes and find the bottom. But a neural network has 175 billion slopes to choose. You cannot try them all — not in the lifetime of the universe. So how does it find the bottom? Come back and we will steal the trick.*

---

## Concept Block 3: The Error Bowl and the Meaning of a Derivative (10 min)

### Two plots, and students must not confuse them

Draw both, side by side, and label them in enormous letters. **This is the single most common point of confusion in the session.**

```
   PLOT 1 — THE DATA                  PLOT 2 — THE ERROR BOWL
   (what the flats look like)         (what the SLOPES score)

   rent │      ● ●                    MSE  │ \                    /
        │    ●                             │  \                  /
        │  ● ●                             │   \              /
        │●                                 │     \_______ /
        └──────────── size                 └────────────────────── m
                                                       ↑
        x-axis = a flat                        x-axis = a GUESS at m
                                               bottom = the best guess
```

*"In Plot 2, every single point on that curve is an entire line from Plot 1, boiled down to one score. Plot 2 is a plot of possible models."*

Give the curve its proper name: the **cost function**, `J(m)`. And note its shape is not an accident — because MSE is built out of *squares*, and `x²` is a parabola, the cost curve for a linear model is always a clean, single-bottomed bowl. There are no fake valleys to get trapped in. (Mention that in Module 3 this stops being true — neural network landscapes are lumpy — and that is why deep learning is harder.)

### The derivative, in three chalk strokes

**Stroke 1 — the secant.** Pick two points on the curve, join them. That straight line is a **secant**. Its slope is just rise ÷ run. Nothing new.

**Stroke 2 — slide it in.** Move the second point closer to the first. The secant tilts. Closer still. Tilts more.

**Stroke 3 — the tangent.** When the two points are *almost* the same point, the secant stops being a chord and becomes a **tangent** — a line that just kisses the curve at one spot. **The slope of that tangent is the derivative.**

```
derivative at a point = the steepness of the curve, right there
```

The only rule you need all session — write it and box it:

```
if  y = x²   then   slope at x = 2x
```

Sanity-test it live: at `x = 3` slope is `6` (steeply uphill). At `x = −3` slope is `−6` (steeply downhill). At `x = 0` slope is **`0`** — perfectly flat.

### The punchline

*"Where is x = 0 on the parabola? The very bottom. So the bottom of a curve is exactly the place where its slope is zero. **Minimising an error is the same task as hunting for zero slope.** And the derivative is the tool that tells you, from wherever you happen to be standing, how far you are from that flat spot and in which direction."*

---

## Practical Block 3: Plot the Bowl, Watch a Secant Become a Tangent (15 min)

```python
import numpy as np
import matplotlib.pyplot as plt

size = np.array([4., 5., 6., 7., 8., 9.])
rent = np.array([17., 21., 22., 27., 29., 33.])
C = 5.0                                    # intercept held fixed today

def mse_for(m):
    return np.mean((rent - (m * size + C)) ** 2)

# --- 1. Draw the error bowl by brute force ---
slopes = np.linspace(1.0, 5.0, 200)
costs  = np.array([mse_for(m) for m in slopes])

best_m = slopes[np.argmin(costs)]
print(f"Lowest MSE on this grid is at m ≈ {best_m:.3f}")   # lands near 3.05

plt.figure(figsize=(9, 5))
plt.plot(slopes, costs, lw=2.5, color='darkorange')
plt.scatter([best_m], [costs.min()], s=150, color='green', zorder=5,
            label=f'bottom of the bowl: m ≈ {best_m:.2f}')
plt.axvline(best_m, ls=':', color='green')
plt.xlabel('slope m  (the parameter we are choosing)')
plt.ylabel('MSE  (how wrong that choice is)')
plt.title('The Error Bowl — cost as a function of the slope')
plt.legend(); plt.grid(alpha=0.3); plt.show()
```

### Secant → tangent, numerically

```python
# The one rule: for f(x) = x**2, the true slope at x is 2x.
# At x = 3, the true slope should be 6. Let's SNEAK UP on it.
f = lambda x: x ** 2
x0 = 3.0

print("  h        secant slope (f(x+h) - f(x)) / h")
for h in [1.0, 0.5, 0.1, 0.01, 0.001, 0.0001]:
    secant = (f(x0 + h) - f(x0)) / h
    print(f"{h:>7}      {secant:.5f}")
# The column marches 7.0 -> 6.5 -> 6.1 -> 6.01 -> 6.001 -> 6.0001
# It is closing in on exactly 2 * 3 = 6. That limit IS the derivative.

# And the flat spot:
for x in [-3, -1, 0, 1, 3]:
    print(f"x = {x:>3}   slope 2x = {2*x:>3}   {'<-- FLAT. this is the minimum' if x == 0 else ''}")
```

**Live walk-through:** Run the secant loop and *read the column out loud, top to bottom*: "seven… six point five… six point one… six point zero one…". Then ask: **"What number is this column trying to reach?"** They will say six. *"Six is 2 × 3. You just computed a derivative from first principles, with no calculus at all. That is all a derivative ever was — the number the secant is running towards."*

Then tie the two halves together: *"Our error bowl is a parabola too. So somewhere on it there is a point where the tangent is dead flat. That point is the best model. Now — how do we get there without checking 200 slopes on a grid like we just cheated with?"*

---

## Concept Block 4: Gradient Descent — Walking Downhill in Fog (10 min)

### The picture (do this one entirely without code)

*"You are on a hillside. Fog everywhere — you cannot see the valley floor, and you cannot see where you started. You have exactly one instrument: you can feel the slope of the ground under your feet. What do you do?"*

They will say it: **feel which way is downhill, take a step, feel again.** That is gradient descent. There is nothing more to it.

### The rule, written once, on the board

```
new_m  =  old_m  −  learning_rate × (slope of the error curve at old_m)
```

**Read it aloud as a sentence:** *"Move against the slope."*

Why the minus sign is doing all the work — make them see it both ways:

| Where you stand | Slope there | `− rate × slope` gives | m moves | Correct? |
|---|---|---|---|---|
| Left wall (m too small) | negative (curve falls to the right) | a **positive** nudge | m goes **up** | ✅ towards the bottom |
| Right wall (m too big) | positive (curve rises to the right) | a **negative** nudge | m goes **down** | ✅ towards the bottom |
| At the bottom | zero | zero | m **stops** | ✅ it has arrived |

*"Notice the algorithm never needs to be told which side of the bowl it is on. The sign of the slope tells it. And when it reaches the flat spot, the update becomes zero and it parks itself. It stops automatically."*

### The gradient for our MSE

State it plainly and do not derive it — one line, then move on:

```
MSE(m)  = average of (rent − (m·size + c))²
slope   = −(2/n) × Σ [ size × residual ]
```

*"It is the `2x` rule from the parabola, wearing a coat. That is the only calculus in this room."*

**Do one step, by hand, right now.** At `m = 3`, our residuals were `0, +1, −1, +1, 0, +1`:

```
Σ (size × residual) = 4(0) + 5(1) + 6(−1) + 7(1) + 8(0) + 9(1)
                    = 0 + 5 − 6 + 7 + 0 + 9  =  15

slope = −(2/6) × 15 = −5

new_m = 3 − (0.01 × −5) = 3 + 0.05 = 3.05
```

*"The slope came out negative — meaning the bowl still falls away to the right — so the rule pushed m upward, from 3.00 to 3.05. It moved us towards the better slope, and we never once looked at the plot."*

### The learning rate — the one dial you tune

| Learning rate | Behaviour | The fog analogy |
|---|---|---|
| Far too small | Crawls; still nowhere near the bottom after hundreds of steps | Shuffling forward one centimetre at a time |
| Just right | Descends fast, settles cleanly | A confident walking stride |
| Too big | Overshoots the valley, lands higher up the far wall, then higher still — **explodes to infinity** | Leaping clean across the valley, harder each time |

*"The 'too big' case is not a slow failure. It is a catastrophic one — your loss becomes `nan` in about ten steps. When your training blows up in Module 3, this table is the first place to look."*

---

## Practical Block 4: A Hand-Written Gradient Descent Loop (10 min)

```python
import numpy as np

size = np.array([4., 5., 6., 7., 8., 9.])
rent = np.array([17., 21., 22., 27., 29., 33.])
C = 5.0

def mse_and_slope(m):
    resid = rent - (m * size + C)          # actual - predicted
    mse   = np.mean(resid ** 2)
    slope = -2 * np.mean(size * resid)     # the derivative of MSE w.r.t. m
    return mse, slope

def descend(learning_rate, steps=20, m=1.0, show=False):
    """Start at a deliberately bad slope and walk downhill."""
    for i in range(steps):
        mse, slope = mse_and_slope(m)
        if show and i < 5:
            print(f"  step {i}:  m = {m:8.4f}   MSE = {mse:10.4f}   slope = {slope:9.4f}")
        m = m - learning_rate * slope      # <-- THE ENTIRE ALGORITHM
    return m, mse_and_slope(m)[0]

print("Walking downhill with learning_rate = 0.01, starting from m = 1.0")
final_m, final_mse = descend(0.01, steps=20, show=True)
print(f"\nAfter 20 steps:  m = {final_m:.4f}   MSE = {final_mse:.4f}")

# Was it right? Ask NumPy for the exact answer (intercept fixed at 5):
exact = np.sum(size * (rent - C)) / np.sum(size ** 2)
print(f"Exact best slope (algebra):  m = {exact:.4f}")
```

The trace shows `m` leaping from `1.0` to roughly `2.86` on the first step (the slope there is huge and steep), then easing in: `3.04`, `3.05`, `3.055`… and the algebraic answer is about `3.0554`. **They match.** Let that land.

### The learning rate, felt rather than described

```python
print("\n--- Same hill, three different step sizes (20 steps each) ---")
for lr in [0.0002, 0.01, 0.025]:
    m, e = descend(lr, steps=20)
    verdict = "too small — barely moved" if lr == 0.0002 else \
              "just right — found it"    if lr == 0.01   else \
              "TOO BIG — diverged!"
    print(f"lr = {lr:<8}  m = {m:>14.4f}   MSE = {e:>12.4g}   ({verdict})")
```

- `lr = 0.0002` limps to roughly `m = 1.6` — nowhere near `3.06`. It would get there eventually. You do not have eventually.
- `lr = 0.01` nails it.
- `lr = 0.025` **explodes** — `m` runs off to a large negative number and MSE goes astronomical. Show the ugly number on screen. Let them enjoy it.

**Live walk-through:** After the divergence prints, ask: *"Nothing about the data changed. Nothing about the bowl changed. The only thing I altered was a number I invented. What does that tell you about hyperparameters?"* — That the model can be perfect and your *configuration* can still destroy it. This is the emotional groundwork for every hyperparameter conversation for the rest of the course.

---

## Summary & Wrap-Up (5 min)

**Point at the spine you wrote on the board in minute one, and walk it, left to right:**

1. **`y = mx + c`** — a line is a rate (`m`) plus a starting point (`c`), and both are read back in real units. `m = 45` means *₹45 more rent per extra square foot*.
2. **Residual = actual − predicted** — one gap per data point, measured in the target's own units.
3. **We square them** — because negatives would cancel (darts left and right are not a bullseye), and because big misses deserve to hurt. Sum them → **SSE**. Average them → **MSE**.
4. **MSE is a function of `m`** — so plot it against `m` and you get the **error bowl**. Every point on that bowl is one entire candidate model, scored.
5. **The bottom of a curve is where its slope is zero** — and the **derivative** is what tells you the slope at the spot you are standing on. Secant, slid in, becomes tangent. `d/dx of x² is 2x`. That is all.
6. **Gradient descent** — `new_m = old_m − learning_rate × slope`. Move against the slope. Repeat. The minus sign makes it self-correcting; the learning rate decides whether you stroll, crawl, or fly off the map.

*"You did not learn six things today. You learnt one thing six times: **make the error a number, then make the number smaller.** Everything else in machine learning is a variation on that sentence."*

**Bridge:** *"Next session — **Classification Foundations** — the target stops being a number and becomes a category: spam or not, churn or stay. You cannot square 'spam'. So we will need a new way to measure wrongness. But the moment we have one, we will do exactly what we did today: turn it into a curve, find the slope, and walk downhill. The engine does not change. Only the fuel."*

---

## Q&A & Doubt Solving (5 min)

**Q: Why bother with gradient descent at all? You showed us an exact algebra formula for the best slope at the end.**
→ Excellent catch, and it is the right question. For a straight line with one feature, the exact formula wins — it is instant and perfect. But that formula requires inverting a matrix, and its cost blows up roughly with the cube of the number of features. At a few hundred features it is slow; at a million (a neural network) it is impossible, and for most models no exact formula exists at all. Gradient descent does not care how many parameters there are — it just keeps stepping. It is the only method that scales, which is why it, not algebra, powers all of deep learning.

**Q: Why do we square the residuals instead of taking absolute values? Absolute values also stop the cancelling.**
→ True, and absolute error (MAE) is a perfectly real metric you have already met. Two reasons we default to squares. First, squaring punishes one big miss far more than many small ones — often what you want, since a ₹50,000 error on one flat is worse than ₹5,000 errors on ten flats. Second, `x²` is smooth everywhere, so it has a clean derivative at every point; `|x|` has a sharp corner at zero where the slope is undefined, which makes the downhill walk misbehave right where you want it to settle.

**Q: How do I actually pick the learning rate? Is there a formula?**
→ No formula — it is a hyperparameter, meaning *you* choose it and the data judges you. The practical recipe: start around `0.01`, plot MSE against step number, and read the shape. Falling steadily to a flat line means it is fine. Falling painfully slowly means increase it, usually by 10×. Jumping around or shooting to `nan` means decrease it, usually by 10×. You are looking for the largest step size that still descends smoothly.

**Q: We held the intercept `c` fixed at 5 the whole session. Isn't that cheating?**
→ It is a teaching simplification, and a deliberate one — with one parameter the error surface is a 2-D bowl you can draw on a board. Let `c` move too and it becomes a 3-D valley, and the algorithm computes *two* slopes each step (one for `m`, one for `c`) and steps in both directions at once. That is genuinely all that changes. Real models do this for thousands of parameters simultaneously; the loop body is identical, just longer.

---

## Instructor Notes

- **Chalk-first is not optional here.** If you open the notebook before the board is full, students will copy code and learn nothing. The rule for this session: every number must appear in someone's handwriting before it appears on a screen. Budget the hand-worked minutes and protect them.
- **The number-one confusion is the two plots.** Students conflate the data scatter (x = flat size) with the error bowl (x = the slope `m`). Draw them side by side, label the x-axes in capital letters, and go back and point at the pair every single time you say the word "bowl". If you fix only one misconception today, fix this one.
- **Setup:** `numpy`, `pandas`, `matplotlib` only. `pip install numpy pandas matplotlib`. Nothing downloads, nothing is fetched, the dataset is six numbers typed inline. This session should run on a laptop with no internet.
- **Pacing:** Practical 3 (the secant loop) is the block to cut if you are running late — the printed column is beautiful but the idea survives on the board alone. Never cut Practical 4; the hand-written descent loop *is* the session's artifact. If you overrun, take the time from Q&A and answer the rest on the forum.
- **Let the divergence be ugly.** When `lr = 0.025` blows up, do not tidy the output or apologise for it. Let the `1.8e+06` sit on the projector. Students remember catastrophes; they forget clean runs. This is the moment "hyperparameter" stops being a vocabulary word.
- **For students who are ahead:** ask them to make `c` learnable too — add a second gradient, `slope_c = -2 * np.mean(resid)`, and update both parameters inside the same loop. They should recover roughly `m ≈ 3.11, c ≈ 4.59`, which is exactly what `np.polyfit(size, rent, 1)` returns. Watching a hand-written loop reproduce a library function is the best possible ending to this class.
