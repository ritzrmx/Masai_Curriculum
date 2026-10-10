# TA Live Demo Script — Statistics: Relationships in Data
> Session 26 | Runtime: ~7 minutes | Delivered at session end, after the lecture

**Setup before class starts:** Both Kirana365 CSVs open in a sheet or Python notebook (`Kirana365_Ads_Notifications_Jan-Aug2026.csv` and `Kirana365_Delay_vs_Rating_Aug2026.csv`, in the `data` folder). A whiteboard for one small sketch.

---

```
STEP 1 — Ask the leadership question (≈1 min)
  Action: Show the ads file (Jan to Aug) and ask: "Ad spend went up every month and so did revenue from ads. Did the ads work?"
  Result: Almost everyone says yes
  Say out loud: "Hold on to that answer. We are about to test how sure we really are."
```

```
STEP 2 — Put a number on it (≈2 min)
  Action: In the sheet type =CORREL(B2:B9,C2:C9). In Python the same thing is df["Ad_Spend_INR"].corr(df["Revenue_From_Ads_INR"]).
  Result: 0.989, a very strong positive correlation
  Say out loud: "Close to plus one means the two move almost in lockstep. That is the pattern. It is not yet an explanation."
```

```
STEP 3 — Compare three relationships (≈2 min)
  Action: Run the same formula on three more pairs: notifications vs revenue from ads (column D vs C), then in the delay file avg delay vs avg rating, then day number (1 to 31) vs avg rating.
  Result: +0.41, then -0.88, then about -0.01
  Say out loud: "Same formula, three very different answers. Plus 0.41 is moderate, and from only eight months. Minus 0.88 is strong, just in the opposite direction: slow days, low ratings. And minus 0.01 is what no relationship looks like."
```

```
STEP 4 — Add the hidden factor and rewrite the claim (≈2 min)
  Action: Add a month-number column 1 to 8 and correlate it with ad spend (0.975) and with revenue from ads (0.934). Sketch: Time/growth -> Ad spend up, and Time/growth -> Revenue up, with a dotted line between Ad spend and Revenue. Then cross out "Ads drove the revenue growth" and write: "Ad spend and ad-attributed revenue moved together strongly (r = 0.989). That does not show the ads caused it; a test would."
  Say out loud: "Both columns just climb with time. Revenue per rupee of ads even rose from 3.2 to 4.2, so something besides spend is helping. Same data, an honest sentence, and it tells the manager what to do next: run a test."
```

---

> **TA TALKING POINT:** "A strong correlation is where an analyst's questions begin, not where they end. Before you say 'because', name one other thing that could be driving both numbers."
