# Lecture Script: NumPy — Numerical Foundation
> **Instructor Reference** — Module 1: Foundations of Data | Session 9 | Duration: 2 Hours

---

## Session Overview

**Goal:** Students create and manipulate NumPy arrays with indexing, slicing, broadcasting, reshape, and flatten — without Python loops.

**Key outcome:** Vectorized temperature and sales calculations on 1D and 2D arrays.

---

## Timing Breakdown

| Segment | Duration |
|---|---|
| Why NumPy after lists | 10 min |
| Create arrays, dtype, shape | 20 min |
| Indexing & slicing | 20 min |
| BREAK | 10 min |
| Element-wise ops & broadcasting | 25 min |
| reshape, flatten, 2D arrays | 20 min |
| Lab: array stats challenge | 10 min |
| Wrap | 5 min |

---

## Live Demo Sequence

```python
import numpy as np
a = np.array([1, 2, 3, 4])
print(a * 2, a.mean())

m = np.array([[1, 2], [3, 4]])
print(m.shape, m.flatten())
```

Emphasise: same operation on whole array — no for-loop.
