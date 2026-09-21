# Kirana365 Dataset Package — Module 3 (Sessions 17–25)

All files simulate Kirana365, the online grocery delivery startup running
across Bengaluru, Hyderabad, Chennai, and Pune, used as the single running
example throughout Module 3. Numbers are engineered to match the specific
figures already quoted in the pre-reads and lecture scripts, so building the
actual charts in Tableau reproduces the same patterns the instructor
narrates.

## Files and which sessions use them

| File | Used in | What it's for |
|---|---|---|
| `Kirana365_Orders_Aug2026.csv` | **17, 19, 20, 21, 22, 23, 24, 25** | The core dataset. Order-level rows: Order ID, Order Date, City, Category, Quantity, Revenue (INR), Delivery Partner. This is what students load in Session 17 and keep reusing all module. |
| `Kirana365_Orders_Jul2026.csv` | **21** | Same structure as the August file, one month earlier. Needed for the "vs last month" trend calculations — Bengaluru +12%, Hyderabad +5%, Chennai −3%, Pune +9%, matching the pre-read exactly. |
| `Kirana365_ConversionChurn_Aug2026.csv` | **18** | Summary counts backing the probability worked examples: 82% festival conversion, 31% regular conversion, 6% churn, 5% CTR, 31% conversion-from-click. This is a talking-point/handout table for the stats session, not something built in Tableau. |
| `Kirana365_CustomerSegments_Aug2026.csv` | **21** | New vs Repeat customer order counts, engineered so New Customers are +25%, Repeat Customers are −5%, and the *company-wide* total is +10% — the exact "hidden problem inside a healthy KPI" exercise. |
| `Kirana365_BengaluruAdCampaign_Jun-Aug2026.csv` | **23** | Monthly ad spend, revenue from ads, and conversion rate for Bengaluru, June–August. ROI climbs 3.5 → 3.9 → 4.20 return per ₹1 spent, above the stated 2.80 company average — backs the budget-approval dashboard story. |
| `Kirana365_ChennaiDailyRevenue_Aug2026.csv` | **24** | Daily Chennai revenue for August. Includes one single-day dip (Aug 12, noise) surrounded by stable days, and a genuine monotonic decline across the final 10 days (Aug 22–31) — the trend-vs-noise teaching example. |
| `Kirana365_PuneNewSignups_Jul-Aug2026.csv` | **24** (TA demo) | Daily new customer signups in Pune across 6 weeks, climbing smoothly from 17/day to 25/day (+42%), axis-safe (starts near zero, no single-day spike) — the "real trend, not a blip" TA walkthrough. |

## Notes
- Session 22 (Dashboard Design Basics) reuses the Session 21 dashboard and data — no new file needed.
- Session 25 (Insight Writing with GenAI) reuses the Session 24 Chennai dashboard — no new file needed.
- Figures are simulated to match the narrative in the written materials, not pulled from a real MySQL instance the way Module 2's SQL data is. If exact reproducibility against a live database matters for this module too, flag it and the generation script can be adapted to write into MySQL/MariaDB instead of CSV.
