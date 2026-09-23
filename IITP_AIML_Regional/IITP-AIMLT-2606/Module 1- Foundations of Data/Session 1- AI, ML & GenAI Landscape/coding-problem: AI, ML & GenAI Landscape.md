# Coding Problem: AI, ML & GenAI Landscape
> **Session 1 — Module 1: Foundations of Data** | ⏱ 5 mins

---

## Scenario

You are onboarding as a junior analyst. Classify each project and ML problem type before any code is written.

---

## Tasks

**Task 1 — Basic**

Fill in the category for each (`AI`, `ML`, or `GenAI`):

```python
projects = {
    "Email spam filter trained on labelled emails": "___",
    "Chatbot that drafts support replies from a prompt": "___",
    "Thermostat: if temp > 30, turn on AC": "___",
    "Recommend products based on purchase history": "___",
}
for name, cat in projects.items():
    print(f"{name}: {cat}")
```

**Task 2 — Basic**

Mark each as `regression`, `classification`, or `unsupervised`:

```python
problems = {
    "Predict house price": "___",
    "Detect fraud (yes/no)": "___",
    "Group customers by behaviour": "___",
    "Forecast daily sales": "___",
}
for task, ptype in problems.items():
    print(f"{task}: {ptype}")
```

**Task 3 — Mid**

Write comments explaining your choice:

```python
# Scenario: A bank wants to predict loan default (yes/no) from applicant data.
# Best approach: ___ (ML / GenAI / Rules)
# ML problem type: ___
# Why not GenAI for the final decision? ___
```

---

## Expected Output

```
Email spam filter trained on labelled emails: ML
Chatbot that drafts support replies from a prompt: GenAI
Thermostat: if temp > 30, turn on AC: AI
Recommend products based on purchase history: ML

Predict house price: regression
Detect fraud (yes/no): classification
Group customers by behaviour: unsupervised
Forecast daily sales: regression
```

---

<details>
<summary>Solution</summary>

```python
projects = {
    "Email spam filter trained on labelled emails": "ML",
    "Chatbot that drafts support replies from a prompt": "GenAI",
    "Thermostat: if temp > 30, turn on AC": "AI",
    "Recommend products based on purchase history": "ML",
}
for name, cat in projects.items():
    print(f"{name}: {cat}")

problems = {
    "Predict house price": "regression",
    "Detect fraud (yes/no)": "classification",
    "Group customers by behaviour": "unsupervised",
    "Forecast daily sales": "regression",
}
for task, ptype in problems.items():
    print(f"{task}: {ptype}")

# Scenario: loan default prediction
# Best approach: ML
# ML problem type: classification
# Why not GenAI: need consistent, auditable yes/no from structured features;
# GenAI is not trained for regulated scoring on tabular applicant data.
```
</details>
