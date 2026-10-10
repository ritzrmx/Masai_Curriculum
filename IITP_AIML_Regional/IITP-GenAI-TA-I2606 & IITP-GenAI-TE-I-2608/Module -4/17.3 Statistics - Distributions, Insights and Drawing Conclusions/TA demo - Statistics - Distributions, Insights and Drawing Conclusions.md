# TA Live Demo Script — Statistics: Distributions; Insights and Drawing Conclusions
> Session 39 | Runtime: ~7 minutes | Delivered at session end, after the lecture

**Setup before class starts:** A notebook with the statistics and matplotlib libraries and eleven Kirana365 order values in ₹ on screen: 400, 450, 500, 500, 550, 600, 650, 700, 800, 850, 9000.

---

```
STEP 1 — Quote the average (≈1 min)
  Action: Run st.mean(values) and say the number aloud. Ask the room: would you put this in a leadership report?
  Result: About 1,364
  Say out loud: "That sounds like a typical order. Let's see if it is."
```

```
STEP 2 — Look at the shape (≈2 min)
  Action: Run plt.hist(values, bins=range(0, 11000, 1000)) with a title and axis labels.
  Result: One tall bar on the left with ten orders under ₹1,000 and one lonely bar far to the right
  Say out loud: "Ten of eleven orders are under a thousand rupees. The average describes one customer, not the typical one."
```

```
STEP 3 — Use the median (≈2 min)
  Action: Run st.median(values), then the mean and median again with the 9000 order removed.
  Result: Median 600; without the big order the mean is 600 as well
  Say out loud: "One order moved the mean from 600 to 1,364 and barely touched the median. When the mean is far above the median, suspect skew."
```

```
STEP 4 — Word it fairly (≈2 min)
  Action: Put two sentences on screen. Weak: "Average order value is ₹1,364." Better: "The median order was ₹600; one ₹9,000 order lifted the mean to ₹1,364. Based on 11 orders, so a hint rather than proof."
  Say out loud: "The fair version is not weaker. It is more useful because it tells the reader what to do next."
```

---

> **TA TALKING POINT:** "One number can describe nobody. Look at the shape first, then claim only what the evidence supports."
