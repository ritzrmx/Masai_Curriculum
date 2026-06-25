# Lecture Script: Pandas — Loading, Inspection & Filtering
> **Instructor Reference** — Module 1: Foundations of Data | Session 10 | Duration: 2 Hours

---

## Session Overview

**Goal:** Load CSVs, inspect with head/info/describe, filter with boolean indexing and loc/iloc.

**Key outcome:** Clean exploration report on a messy employee or sales CSV.

---

## Timing Breakdown

| Segment | Duration |
|---|---|
| Series vs DataFrame | 15 min |
| read_csv + inspection trio | 25 min |
| Boolean filtering | 20 min |
| BREAK | 10 min |
| loc vs iloc | 25 min |
| Sorting & column selection | 15 min |
| Lab: find data quality issues | 15 min |
| Wrap | 5 min |

---

## Inspection checklist (teach as ritual)

```python
import pandas as pd
df = pd.read_csv("data.csv")
df.head()
df.info()
df.describe()
df.shape
```
