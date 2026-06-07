# Coding Problem: Structured Outputs and Tool Integration

> **Session 4** | ⏱ 12–15 mins | Module 3: GenAI & Agents

---

## Scenario

You are building a job posting parser. Given a raw job description text, the LLM must extract structured data — job title, required skills, experience level, and salary range — and return it as a validated JSON object.

---

## Setup

```python
import openai, json, os
from pydantic import BaseModel, ValidationError
from typing import List, Optional

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
```

---

## Sample Job Posting

```python
job_text = """
Senior Data Engineer - FinTech Startup (Remote)
We are looking for a Senior Data Engineer with 4+ years of experience in Python, 
Apache Spark, and SQL. Familiarity with AWS (S3, Glue, Redshift) is a must.
Knowledge of dbt and Airflow is a bonus. Salary: ₹25–40 LPA.
"""
```

---

## Tasks

**Task 1 — Define the Pydantic Schema**

Define a Pydantic model that captures the structured fields from a job posting.

```python
class JobPosting(BaseModel):
    title:            str
    required_skills:  List[str]
    experience_years: int             # minimum years required
    salary_range:     Optional[str]   # e.g. "₹25–40 LPA" or None
    remote:           bool
```

---

**Task 2 — Prompt the LLM for Structured Output**

Fill in the blanks to extract structured data using `response_format`.

```python
def extract_job(text: str) -> JobPosting:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "Extract job details from the posting and return valid JSON matching the schema."
            },
            {
                "role": "user",
                "content": ___    # fill: pass the job_text
            }
        ],
        response_format={"type": "___"}   # fill: force JSON output
    )

    raw_json = response.choices[0].message.___   # fill: get content
    data     = json.loads(raw_json)
    return JobPosting(**___)                      # fill: unpack data dict
```

---

**Task 3 — Validate and Handle Errors**

Run the extractor and add a try/except block to catch `ValidationError`.

```python
try:
    job = extract_job(___)     # fill: pass job_text
    print("Title:     ", job.___)
    print("Skills:    ", job.___)
    print("Exp (yrs): ", job.___)
    print("Salary:    ", job.___)
    print("Remote:    ", job.___)
except ValidationError as e:
    print("Validation failed:", e)
except json.JSONDecodeError as e:
    print("JSON parse error:", e)
```

**Expected output (approximate):**
```
Title:      Senior Data Engineer
Skills:     ['Python', 'Apache Spark', 'SQL', 'AWS', 'S3', 'Glue', 'Redshift']
Exp (yrs):  4
Salary:     ₹25–40 LPA
Remote:     True
```

---

**Task 4 — Idempotency Check**

Run `extract_job(job_text)` three times. Do you get the same output each time? Why or why not?  
Try setting `temperature=0` and run again — does it become consistent?

---

## Key Takeaways

- `response_format={"type": "json_object"}` forces valid JSON — but you still need to validate with Pydantic
- Pydantic catches missing fields and wrong types before they cause downstream bugs
- `temperature=0` improves idempotency — critical for structured extraction pipelines
