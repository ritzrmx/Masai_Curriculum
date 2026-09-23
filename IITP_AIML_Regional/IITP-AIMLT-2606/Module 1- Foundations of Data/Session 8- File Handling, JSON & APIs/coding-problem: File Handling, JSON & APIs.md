# Coding Problem: File Handling, JSON & APIs
> **Session 8 — Module 1: Foundations of Data** | ⏱ 5 mins

---

## Tasks

**Task 1 — Basic**

Parse JSON string and print city:

```python
import json
raw = '{"user": "Maya", "city": "Pune", "score": 88}'
data = json.loads(raw)
print(data["city"])
```

**Task 2 — Basic**

Write dict to JSON string with `ensure_ascii=False`:

```python
record = {"product": "Notebook", "qty": 2}
# json.dumps → print
```

**Task 3 — Mid**

Simulate API response — print status and title:

```python
response = {"status_code": 200, "body": {"title": "Intro to ML"}}
# Print: OK: Intro to ML if status 200 else Error
```

---

## Expected Output

```
Pune
{"product": "Notebook", "qty": 2}
OK: Intro to ML
```

---

<details>
<summary>Solution</summary>

```python
import json
raw = '{"user": "Maya", "city": "Pune", "score": 88}'
data = json.loads(raw)
print(data["city"])

record = {"product": "Notebook", "qty": 2}
print(json.dumps(record))

response = {"status_code": 200, "body": {"title": "Intro to ML"}}
if response["status_code"] == 200:
    print("OK:", response["body"]["title"])
else:
    print("Error")
```
</details>
