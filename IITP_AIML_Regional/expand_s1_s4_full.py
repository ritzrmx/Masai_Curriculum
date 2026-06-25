#!/usr/bin/env python3
"""Expand IITP-AIMLT-2606 Module 1 Sessions 1-4 pre-reads (450+) and lectures (750+).

Run: python3 expand_s1_s4_full.py
Overwrites 8 markdown files under Module 1- Foundations of Data (Sessions 1-4).
"""

from pathlib import Path

MODULE = Path(__file__).resolve().parent / "IITP-AIMLT-2606/Module 1- Foundations of Data"


def extract_mental_map(pre_read_path: Path) -> str:
    text = pre_read_path.read_text(encoding="utf-8")
    start = text.index("## Mental Map")
    end = text.index("## What You'll Learn")
    return text[start:end].rstrip()


def code_block(code: str, output: str, breakdown: list[str], ask: str, mistake: tuple[str, str]) -> str:
    bullets = "\n".join(f"- {b}" for b in breakdown)
    return f"""```python
{code.rstrip()}
```

**Output:**
```
{output.rstrip()}
```

**Break it down:**
{bullets}

**Ask:** {ask}

**Common mistake:** {mistake[0]}

**Fix:** {mistake[1]}
"""


def segment_header(n: int, title: str, minutes: int) -> str:
    return f"\n## SEGMENT {n}: {title} ({minutes} min)\n"


def sub_timing(label: str, minutes: int) -> str:
    return f"\n### {label} ({minutes} min)\n"


def lecture_footer(
    quiz: str,
    quiz_answers: str,
    homework_rows: str,
    materials: str,
    contingencies: str,
    instructor_notes: str,
    faqs: str,
) -> str:
    return f"""
---

## End-of-Session Quiz (5 Questions)

{quiz}

**Answer key (instructor):** {quiz_answers}

---

## Homework Rubric

| Criterion | Excellent (4) | Good (3) | Needs Work (2) | Incomplete (1) |
|---|---|---|---|---|
{homework_rows}

**Total:** /16 — Pass threshold: 10/16

---

## Materials Checklist

{materials}

---

## Timing Contingencies

{contingencies}

---

## Instructor Notes

{instructor_notes}

---

## FAQ — Q&A

{faqs}
"""


def write_outputs() -> list[tuple[str, int]]:
    """Generate and write all 8 files; return (path, line_count) pairs."""
    outputs: list[tuple[Path, str]] = []

    s1_dir = MODULE / "Session 1- AI, ML & GenAI Landscape"
    s2_dir = MODULE / "Session 2- Python Fundamentals"
    s3_dir = MODULE / "Session 3- Control Flow & Decision Making"
    s4_dir = MODULE / "Session 4- Loops, Iteration & Repetitive Logic"

    mm1 = extract_mental_map(s1_dir / "pre-read: AI, ML & GenAI Landscape.md")
    mm2 = extract_mental_map(s2_dir / "pre-read: Python Fundamentals.md")
    mm3 = extract_mental_map(s3_dir / "pre-read: Control Flow & Decision Making.md")
    mm4 = extract_mental_map(s4_dir / "pre-read: Loops, Iteration & Repetitive Logic.md")

    outputs.extend([
        (s1_dir / "pre-read: AI, ML & GenAI Landscape.md", session1_preread(mm1)),
        (s1_dir / "lecture-script: AI, ML & GenAI Landscape.md", session1_lecture()),
        (s2_dir / "pre-read: Python Fundamentals.md", session2_preread(mm2)),
        (s2_dir / "lecture-script: Python Fundamentals.md", session2_lecture()),
        (s3_dir / "pre-read: Control Flow & Decision Making.md", session3_preread(mm3)),
        (s3_dir / "lecture-script: Control Flow & Decision Making.md", session3_lecture()),
        (s4_dir / "pre-read: Loops, Iteration & Repetitive Logic.md", session4_preread(mm4)),
        (s4_dir / "lecture-script: Loops, Iteration & Repetitive Logic.md", session4_lecture()),
    ])

    results = []
    for path, content in outputs:
        path.write_text(content, encoding="utf-8")
        lines = content.count("\n") + (1 if content and not content.endswith("\n") else 0)
        results.append((str(path.relative_to(MODULE.parent.parent)), lines))
    return results


# ---------------------------------------------------------------------------
# SESSION 1 PRE-READ
# ---------------------------------------------------------------------------

def session1_preread(mental_map: str) -> str:
    return f"""# AI, ML & GenAI Landscape
---

{mental_map}

## What You'll Learn

In this pre-read, you'll discover:

- What **AI**, **ML**, and **GenAI** mean — in plain language, not buzzwords
- Real **industry examples** that show where each term applies in India and globally
- The main **types of ML problems** (prediction, grouping, generation) and when each fits
- How the **AI/ML ecosystem** fits together — data, models, apps, and people
- How to **map a business use case** to the right category before writing code
- Where **deep learning** and **GenAI** sit inside the bigger picture
- Why **responsible AI** matters even when you are just starting out

---

## A. Artificial Intelligence — The Big Umbrella

> 💡 **Analogy:** AI is like the entire **transport industry** — cars, buses, trains, and planes all move people, but they work in different ways. ML and GenAI are specific vehicles inside that industry.

**One-line definition:** **Artificial Intelligence (AI)** is any computer system designed to perform tasks that normally require human intelligence — like understanding language, recognising images, or making decisions.

When someone says "we use AI," they might mean anything from a simple rule ("if balance is low, send alert") to a deep learning model that reads X-rays. The word **AI** is broad. Your job as a learner is to ask: *What kind of AI? What does it actually do?*

```mermaid
flowchart TD
    AI["Artificial Intelligence<br/>Broad field"]
    ML["Machine Learning<br/>Learns from data"]
    GenAI["Generative AI<br/>Creates new content"]
    Rules["Rule-based systems<br/>If-then logic"]
    AI --> ML
    AI --> Rules
    ML --> GenAI
```

| Term | What it does | Example in daily life |
|---|---|---|
| AI | Mimics intelligent behaviour | Voice assistant, chess engine |
| ML | Learns patterns from data | Spam filter, price prediction |
| GenAI | Generates text, images, code | ChatGPT, image generators |
| Rules | Follows fixed instructions | OTP alert above ₹10,000 |

**Rule-based AI** uses hand-written logic. A thermostat that turns on AC when temperature exceeds 25°C is AI — but nobody trained it on data. It follows fixed instructions.

**Data-driven AI** (ML and GenAI) improves by learning from examples. That is the path this course emphasises because real-world problems rarely fit neat if-then rules.

**Worked example — UPI payment alert:**

| Step | System type | Why |
|---|---|---|
| Transaction amount > ₹10,000 | Rule-based | Fixed threshold, no training |
| "Is this transaction unusual for this user?" | ML (anomaly) | Learns normal spending patterns |
| Chatbot explains why payment failed | GenAI | Generates natural-language reply |

**Key idea:** Not every "smart" product uses ML. Knowing the difference stops you from over-engineering simple problems or under-investing in complex ones.

---

## B. Machine Learning — Learning From Data

> 💡 **Analogy:** Teaching a child to recognise fruits by showing hundreds of photos works better than listing rules like "if red and round, it's an apple." **ML** learns from examples instead of hand-written rules.

**One-line definition:** **Machine Learning (ML)** is a branch of AI where systems improve at a task by finding patterns in data — without being explicitly programmed for every case.

The ML loop is always the same at a high level: collect historical data, train a model to find patterns, then use that model on new inputs.

```mermaid
flowchart LR
    D[Historical data] --> T[Train model]
    T --> M[Trained model]
    N[New input] --> M
    M --> P[Prediction or insight]
```

| ML type | Has labels? | Goal | Example |
|---|---|---|---|
| Supervised | Yes | Predict known outcomes | Will customer churn? |
| Unsupervised | No | Find hidden structure | Customer segments |
| Reinforcement | Rewards | Learn best actions | Game-playing bots |

**Supervised learning** is the most common in business. You have past examples with known answers: "this customer left," "this transaction was fraud," "this house sold for ₹50 lakh." The model learns to predict the answer for new cases.

**Unsupervised learning** finds groups or patterns when nobody labelled the data. Marketing teams use it to discover customer segments they did not know existed.

**Reinforcement learning** learns by trial and error with rewards — common in robotics and game AI, less common in day-one data jobs.

| Problem shape | ML task type | Output |
|---|---|---|
| How much will sales be next month? | Regression | A number |
| Is this email spam? | Classification | A category (yes/no) |
| Which customers behave similarly? | Clustering | Groups |
| Which product should we recommend? | Recommendation | Ranked list |

**Worked example — Flipkart delivery ETA:**

1. **Input data:** past orders, distance, traffic, weather, time of day
2. **Training:** model learns which factors predict late vs on-time delivery
3. **Output:** "Arrives by 6 PM" shown in the app — a predicted number or time window
4. **Category:** supervised regression or classification depending on design

**Key idea:** ML needs data — usually lots of it — and a clear question. "Use ML" without defining the question leads to confusion.

---

## C. Generative AI — Creating New Content

> 💡 **Analogy:** A **photocopier** copies what exists. A **GenAI** tool is more like a skilled writer who has read millions of books and can draft a new paragraph in your style — original output, trained on existing data.

**One-line definition:** **Generative AI (GenAI)** uses large models trained on vast text or media to **create** new content — answers, summaries, code, images — from a prompt.

GenAI burst into public view with tools like ChatGPT, but the idea builds on years of **deep learning** — neural networks with many layers that learn rich representations from data.

| Traditional ML | GenAI |
|---|---|
| Predicts a number or category | Generates open-ended text or media |
| Needs structured training data | Trained on language or multimodal data |
| Output is fixed (0/1, price) | Output is flexible (paragraphs, code) |
| Easier to measure accuracy | Harder to judge "correctness" |

```mermaid
flowchart LR
    P[Your prompt] --> L[Large language model]
    L --> O[Generated text or code]
    C[Optional context docs] --> L
```

**What GenAI is good at:**
- Drafting emails, summaries, and documentation
- Explaining code or generating boilerplate
- Brainstorming ideas and rephrasing content
- Answering questions when paired with search (RAG — covered later in the course)

**What GenAI struggles with:**
- **Hallucination** — confident-sounding answers that are factually wrong
- Precise numeric prediction without proper data pipelines
- Decisions that require strict audit trails without guardrails
- Tasks where a small, cheap ML model would be faster and more reliable

**Worked example — support email draft vs fraud score:**

| Task | Right tool | Wrong tool | Why |
|---|---|---|---|
| Draft reply to angry customer | GenAI | Rule-only | Language is open-ended |
| Score transaction fraud 0–1 | ML classifier | GenAI alone | Needs auditable numeric score |
| Summarise 50-page policy PDF | GenAI + RAG | Manual copy-paste | Generation + retrieval |

**Key idea:** GenAI *composes*; traditional ML *scores* or *labels*. A fraud system needs a classifier trained on labelled transactions. A support agent might use GenAI to draft replies — but a human or rule should approve them.

---

## D. Mapping Use Cases to the Right Category

> 💡 **Analogy:** Before ordering food, you decide: dine-in, takeaway, or cook at home. Picking **AI vs ML vs GenAI** is the same — match the tool to the job.

**One-line definition:** **Problem framing** means naming what you want the system to do so you choose the right approach — rules, ML model, or GenAI assistant.

Before any project, ask three questions:

1. **What is the output?** A number, a label, or new text/media?
2. **Do we have historical examples?** ML needs data; rules need known logic.
3. **How wrong can we afford to be?** High-stakes decisions need validation, not just a chatbot.

| Use case | Best fit | Why |
|---|---|---|
| Sort emails into folders with fixed rules | Rules / classic AI | Logic is known upfront |
| Predict next month's sales | ML (regression) | Pattern in historical numbers |
| Draft a customer support reply | GenAI | Open-ended language generation |
| Group shoppers by behaviour | ML (clustering) | No pre-defined labels |
| Detect credit card fraud | ML (classification) | Learns subtle patterns from past fraud |
| Answer questions about company policy | GenAI + search (RAG) | Needs flexible language, grounded in docs |

```mermaid
flowchart TD
    Q{{What is the output?}}
    Q -->|Fixed rules| R[Rule-based system]
    Q -->|Number or category| M[Machine Learning]
    Q -->|New text or content| G[Generative AI]
```

**Step-by-step framing exercise:**

1. Write: *"Given ___, the system should output ___."*
2. Circle the output type: number, label, or text/media
3. Pick rules, ML, or GenAI from the table above
4. List one data source you would need

**Example:** *"Given past sales and festival dates, the system should output next month's revenue in rupees."* → Output is a number → ML regression → needs historical sales CSV.

**Common mistake:** Using GenAI for everything because it is trendy. Predicting loan default from structured financial data is an ML classification problem — not a prompt to ChatGPT.

**Key idea:** One clear sentence about input and output usually reveals the right category before anyone opens an IDE.

---

## E. The AI/ML Ecosystem — People, Data, and Products

> 💡 **Analogy:** Making a movie needs writers, actors, cameras, and editors — not just one star. **AI products** need data engineers, scientists, developers, and domain experts working together.

**One-line definition:** The **AI ecosystem** is the network of roles, tools, and data flows that turn raw information into intelligent applications.

```mermaid
flowchart TD
    D[Data sources] --> DE[Data engineer]
    DE --> DS[Data scientist / analyst]
    DS --> M[ML model or GenAI app]
    M --> DEV[Software developer]
    DEV --> U[End user]
    PM[Product / domain expert] --> DS
    PM --> DEV
```

| Role | Main focus | Example task |
|---|---|---|
| Data analyst | Explore and report on data | Build sales dashboard in Excel or Python |
| Data engineer | Move and store data reliably | Build nightly pipeline from app to warehouse |
| Data scientist | Train and evaluate models | Build churn prediction model |
| ML engineer | Deploy models to production | Serve fraud model with low latency |
| AI/GenAI engineer | Integrate LLMs and agents | Build RAG chatbot over company docs |
| Product manager | Define problem and success metrics | Decide what "good recommendation" means |

**Data** sits at the centre of everything in this course. Module 1 teaches you to wrangle data with Python, Pandas, and SQL. Module 2 teaches classical ML. Module 3 teaches GenAI and agents. You cannot skip the foundation.

| Course module | You learn | Typical job tasks |
|---|---|---|
| Module 1 — Foundations of Data | Python, Pandas, SQL, EDA | Clean data, query tables, visualise trends |
| Module 2 — Classical ML | scikit-learn, validation, metrics | Train predictors, compare models |
| Module 3 — GenAI & Agents | LLMs, RAG, tools, guardrails | Build assistants and agent workflows |

**Worked example — who touches a churn model?**

| Role | Contribution |
|---|---|
| Product manager | Defines "churn" (no purchase in 90 days?) |
| Data engineer | Builds nightly feature table from app logs |
| Data analyst | Explores which features correlate with churn |
| Data scientist | Trains and evaluates the model |
| ML engineer | Deploys API that returns churn score |
| Developer | Shows "at risk" badge in the app UI |

**Key idea:** You do not need to be all roles on day one. But knowing who does what helps you pick a career path and speak clearly in interviews.

---

## F. Deep Learning and the Path to GenAI

> 💡 **Analogy:** If ML is learning to ride a bicycle, **deep learning** is learning on a multi-gear racing bike with many moving parts — more power, but you need more practice and better roads (data).

**One-line definition:** **Deep learning** is machine learning that uses **neural networks** with many layers to learn complex patterns — especially in images, audio, and language.

```mermaid
flowchart TD
    ML[Machine Learning] --> DL[Deep Learning]
    DL --> CV[Computer vision]
    DL --> NLP[Language models]
    NLP --> LLM[Large language models]
    LLM --> GenAI[Generative AI products]
```

| Layer | What it learns | Example product |
|---|---|---|
| Shallow ML | Simple patterns in tables | Logistic regression for spam |
| Deep learning | Rich patterns in images/text | Face unlock, speech recognition |
| Large language models | Language from huge text corpora | ChatGPT, Gemini, Claude |
| Multimodal models | Text + images + audio | Image captioning, voice assistants |

**You do not need to build neural networks on day one.** This course gives you the data and Python foundation first. Module 2 introduces classical ML. Module 3 connects to LLMs and agents.

| Question | Classical ML | Deep learning / GenAI |
|---|---|---|
| Data size | Often works with thousands of rows | Often needs millions of examples |
| Interpretability | Often easier to explain | Often harder ("black box") |
| Cost to run | Cheap on a laptop | LLM API calls cost money per request |
| Best for tabular business data | Often yes | Sometimes overkill |

**Key idea:** GenAI is the **product layer** many users see. Underneath it is deep learning. Underneath that is still the same data discipline you start building in Module 1.

---

## G. A Short Timeline — How We Got Here

> 💡 **Analogy:** Smartphones did not appear overnight — landlines, flip phones, and touch screens each built on the last. **AI history** is the same: decades of progress, then a visible burst.

**One-line definition:** **AI history** helps you see that today's GenAI tools stand on decades of research — not magic — and that hype cycles come and go while useful techniques remain.

| Era | Highlight | Why it matters to you |
|---|---|---|
| 1950s–60s | "AI" coined; early chess programs | Shows rules-based AI is old, not new |
| 1990s–2000s | Spam filters, search ranking | ML in products you already use |
| 2012+ | Deep learning wins image contests | Neural nets become practical |
| 2017+ | Transformer architecture | Foundation for modern LLMs |
| 2022+ | ChatGPT public launch | GenAI enters mainstream workflows |

```mermaid
flowchart LR
    R[Rules and logic] --> M[Classic ML]
    M --> D[Deep learning]
    D --> L[LLMs]
    L --> G[GenAI apps]
```

**Hype vs substance checklist:**

| Signal | Hype | Substance |
|---|---|---|
| Claim | "AI will replace all jobs tomorrow" | "AI automates specific repetitive tasks" |
| Proof | Buzzwords only | Demo with real data and metrics |
| Plan | "Use ChatGPT for everything" | Problem framed with clear output type |

**Key idea:** When you read AI news, ask: *Is this rules, ML, or GenAI — and what data made it possible?* That question keeps you grounded.

---

## H. Responsible AI — Start With Good Habits

> 💡 **Analogy:** Learning to drive includes seatbelts and speed limits before highway merges. **Responsible AI** means building safety and fairness habits before you ship anything to real users.

**One-line definition:** **Responsible AI** means designing and using AI systems fairly, transparently, and safely — especially when decisions affect people.

| Principle | Plain English | Example |
|---|---|---|
| Fairness | System should not discriminate by group | Loan model checked across regions |
| Transparency | Users know when AI is involved | "Drafted by AI — please review" |
| Privacy | Personal data protected | No customer PII in public prompts |
| Accuracy | Verify before acting | Human approves medical or legal drafts |
| Safety | Block harmful outputs | Filters on user-generated content |

```mermaid
flowchart TD
    P[Problem] --> D[Data check]
    D --> M[Model or GenAI]
    M --> V[Validate output]
    V --> H[Human review if high stakes]
    H --> S[Ship to user]
```

**GenAI-specific risks:**

| Risk | What goes wrong | Starter habit |
|---|---|---|
| Hallucination | False facts stated confidently | Always verify critical claims |
| Bias | Unfair stereotypes in text | Review outputs; diversify test prompts |
| Data leakage | Secrets pasted into public chat | Never put passwords or keys in prompts |
| Over-reliance | Skipping human judgment | Keep human in the loop for decisions |

**Worked example — HR resume screening:**

| Approach | Risk | Better practice |
|---|---|---|
| GenAI alone ranks candidates | Opaque, may bias | ML on labelled hires + audit metrics |
| GenAI drafts interview questions | Lower risk | Human recruiter reviews before sending |
| Rules-only keyword match | Misses good candidates | Hybrid: rules + human review |

**Key idea:** Responsibility is not a Module 3-only topic. The framing choices you make in Session 1 — rules vs ML vs GenAI — are already ethical engineering decisions.

---


## I. Quick Reference — Decision Cheat Sheet

| If the output is… | And data looks like… | Start with… |
|---|---|---|
| Fixed yes/no from known rules | Thresholds, law, policy | Rules |
| A number or category from history | Labelled tables, logs | ML |
| New sentences or images | Language/media prompt | GenAI |

```mermaid
flowchart TD
    Start[New project idea] --> Q1{{Output type?}}
    Q1 -->|Number or label| ML[Consider ML]
    Q1 -->|Fixed logic| R[Consider rules]
    Q1 -->|New text or media| G[Consider GenAI]
    ML --> D[Do we have data?]
    D -->|No| R
    D -->|Yes| OK[Prototype ML path]
```

**Worked example — PhonePe support triage:**

| Step | Tool | Why |
|---|---|---|
| Block txn over daily limit | Rules | Statutory / product cap |
| Flag unusual merchant category | ML | Learns user history |
| Draft SMS explaining decline | GenAI | Natural language |
| Human approves SMS | Process | Responsible AI gate |

**Key idea:** Most Indian fintech products you use daily combine all three layers — not just "AI."

---

## Practice Exercises

**1. Pattern Recognition** — For each item, label it AI, ML, or GenAI (some may fit more than one — explain why): (a) Netflix recommending shows, (b) a chatbot writing an email draft, (c) a thermostat following "if temp > 25, turn on AC," (d) Google Photos grouping faces, (e) a bank rules engine blocking transactions over ₹10 lakh without OTP, (f) Swiggy predicting delivery time, (g) DALL·E creating a logo from a text prompt.

**2. Concept Detective** — A startup wants to "use AI" to detect fraudulent credit card transactions. Which category fits best? What kind of ML problem is it (regression, classification, or clustering)? What data would they need? Name one responsible AI check they should plan for.

**3. Real-Life Application** — List three jobs in your city that touch AI, ML, or GenAI. For each, name the role (analyst, engineer, etc.), which term applies, and one task they might do in a typical week.

**4. Spot the Error** — Someone says: "We don't need ML — we'll just use ChatGPT to predict whether a loan should be approved." What is wrong with this plan? Name at least three risks (accuracy, audit, data type, cost, or fairness).

**5. Planning Ahead** — Pick one app you use daily (food delivery, banking, social media). Sketch whether it likely uses rules, ML, GenAI, or a mix. For each feature, note what data the app might collect to power that feature and one responsible AI question you would ask as a product owner.

---

> ✅ **You're done!** You can now tell AI, ML, and GenAI apart, spot real industry examples, map use cases to the right approach, and name starter responsible AI habits before anyone writes code. Next session you will open Google Colab and write your first Python programs — the language everything else in this course builds on.
"""


# ---------------------------------------------------------------------------
# SESSION 2 PRE-READ
# ---------------------------------------------------------------------------

def session2_preread(mental_map: str) -> str:
    return f"""# Python Fundamentals
---

{mental_map}

## What You'll Learn

In this pre-read, you'll discover:

- How to **declare variables** and pick the right **data types** for your data
- How **operators** let you compute, compare, and combine values
- How **input and output** connect your program to the person using it
- How **f-strings** format readable messages with variables inside
- Good **Colab notebook habits** so your work stays organised and reproducible
- How Python shows up inside **Indian apps** you already use every day

---

## A. Variables — Named Storage Boxes

> 💡 **Analogy:** A **variable** is like a labelled lunch box. You put food in, close the lid, and next time you open "Monday lunch," the same contents are there — unless you swap them for something else.

**One-line definition:** A **variable** is a name that points to a value stored in memory so you can reuse and update it later.

```python
age = 25          # int — whole number
price = 19.99     # float — decimal number
name = "Priya"    # str — text (string)
is_student = True # bool — True or False
```

| Type | Example | Use when |
|---|---|---|
| int | 42, -7, 0 | Whole counts — age, quantity, year |
| float | 3.14, 99.5 | Decimals — price, temperature, score |
| str | "hello", 'Python' | Text — names, messages, IDs as text |
| bool | True, False | Yes/no flags — is_active, passed |

```mermaid
flowchart LR
    N[name = Priya] --> M[Memory holds value]
    M --> R[Reuse name anywhere]
```

**Worked example — Swiggy order receipt:**

| Variable | Type | Sample value |
|---|---|---|
| `restaurant` | str | "Biryani House" |
| `item_count` | int | 3 |
| `subtotal` | float | 450.00 |
| `is_premium` | bool | False |

**Key idea:** The **type** tells Python how to treat the value. `"5"` (text) and `5` (number) look similar but behave very differently in math.

---

## B. Data Types — Why `"5"` and `5` Are Not the Same

> 💡 **Analogy:** A phone contact labelled "Home" with the number 555-0100 is not the same as typing the word "five-five-five" into the dialer.

**One-line definition:** A **data type** is the category of a value that controls what operations Python allows on it.

```python
print(type(42))        # <class 'int'>
print(type(3.14))      # <class 'float'>
print(type("hello"))   # <class 'str'>
print(type(True))      # <class 'bool'>
```

| Value | Type | What happens with `+ 1` |
|---|---|---|
| `5` | int | `6` — math works |
| `5.0` | float | `6.0` — math works |
| `"5"` | str | Error — cannot add text and number |
| `True` | bool | `2` — True acts like 1 in math (avoid this habit) |

**Type conversion** (casting):

```python
age_text = "25"
age_number = int(age_text)
print(age_number + 1)        # 26

upi_amount = "1500"
amount = float(upi_amount)
print(f"Paid ₹{{amount:.2f}}")
```

```mermaid
flowchart TD
    I[input always str] --> C{{Need math?}}
    C -->|Yes| T[int or float]
    C -->|No| S[Keep as str]
```

**Key idea:** `input()` always returns a **string**. If you ask for age or bill amount and want math, you must convert.

---

## C. Operators — Doing Math and Comparisons

> 💡 **Analogy:** Operators are kitchen tools: **+** is a mixer, **==** is a taste test, and **>** asks "is this portion bigger?"

**One-line definition:** **Operators** are symbols that perform calculations or comparisons on values and return a result.

| Operator | Name | Example | Result |
|---|---|---|---|
| + | Addition | `10 + 3` | 13 |
| - | Subtraction | `10 - 3` | 7 |
| * | Multiplication | `10 * 3` | 30 |
| / | Division | `10 / 3` | 3.333… |
| // | Floor division | `10 // 3` | 3 |
| % | Modulo | `10 % 3` | 1 |
| ** | Exponent | `2 ** 3` | 8 |

| Operator | Meaning | Example |
|---|---|---|
| == | Equal to | `5 == 5` → True |
| != | Not equal | `5 != 3` → True |
| >, <, >=, <= | Greater / less | `10 > 7` → True |

```mermaid
flowchart LR
    A["10 / 3"] --> R1["3.333 float"]
    B["10 // 3"] --> R2["3 int"]
    C["10 > 7"] --> R3["True bool"]
```

**Worked example — splitting a ₹1,200 dinner bill among 5 friends:**

```python
bill = 1200
people = 5
each_pays = bill / people      # 240.0 float
whole_groups = bill // people  # 240 int
leftover = bill % people       # 0
```

**Key idea:** `/` always gives a float in Python 3, even when the answer is whole: `10 / 2` is `5.0`, not `5`.

---

## D. Input, Output, and f-strings

> 💡 **Analogy:** **print()** announces your order number. **input()** asks your name. **f-strings** are name tags that auto-fill your details.

**One-line definition:** **Input/output (I/O)** lets programs talk to users; **f-strings** embed variables inside text cleanly.

```python
name = input("Your name: ")
print("Hello,", name)

name = "Priya"
score = 87
print(f"Hello {{name}}, you scored {{score}}%")

bill = 1200.50
tip_pct = 15
tip = bill * tip_pct / 100
print(f"Bill: ₹{{bill:.2f}}, Tip: ₹{{tip:.2f}}, Total: ₹{{bill + tip:.2f}}")
```

| Format style | Example | When to use |
|---|---|---|
| f-string | `f"Hi {{name}}"` | Best default — readable |
| comma in print | `print("Hi", name)` | Quick debug |
| str + str | `"Hi " + name` | Works but clumsy for many values |

**Key idea:** f-strings make your output readable. You will use them in every lab and project in this course.

---

## E. Comments and Readable Code

> 💡 **Analogy:** Comments are sticky notes on a recipe — they explain *why* you preheat the oven.

**One-line definition:** A **comment** is a note Python ignores, written for humans reading your code.

```python
# Ask for the user's name
name = input("Name: ")
bill = 500  # bill amount in rupees
```

| Good habit | Bad habit |
|---|---|
| `monthly_salary = 45000` | `ms = 45000` |
| Explain business rule in comment | Comment every obvious line |
| One idea per line when learning | Five statements crammed on one line |

**Key idea:** Clear names beat clever shortcuts. Your future self (and your teammate) reads this code in six months.

---

## F. Colab Notebook Discipline

> 💡 **Analogy:** A notebook is a lab journal — one experiment per cell, run in order.

**One-line definition:** **Colab discipline** means organising notebook cells so your code runs predictably top to bottom.

```mermaid
flowchart TD
    A[Open Colab] --> B[Add markdown title cell]
    B --> C[Code cell: one step]
    C --> D[Run cell Shift+Enter]
    D --> E{{Error?}}
    E -->|Yes| F[Read message fix rerun]
    E -->|No| G[Next cell]
    G --> C
```

| Rule | Why it matters |
|---|---|
| One logical step per cell | Easier to debug |
| Run cells top to bottom | Variables exist in order |
| Add markdown headers | You find sections later |
| Restart runtime if variables act odd | Clears stale state |
| Save a copy to Drive | Colab sessions expire |

| Action | Shortcut |
|---|---|
| Run cell | Shift + Enter |
| Add code cell | Ctrl + M, then B |
| Add markdown cell | Ctrl + M, then M |

**Key idea:** Professional data work lives in notebooks. Building good habits now saves hours when datasets get large.

---

## G. Python Behind Apps You Use in India

> 💡 **Analogy:** You do not see the kitchen when you order biryani on Swiggy — but variables and math still run behind the app.

**One-line definition:** Every feature you tap — UPI pay, delivery ETA, coupon codes — is built from the same primitives you learn today: store values, compute, show text.

| App feature | Variables involved | Type mix |
|---|---|---|
| UPI amount entry | `amount`, `upi_id`, `verified` | float, str, bool |
| Swiggy delivery fee | `distance_km`, `base_fee`, `surge` | float, float, float |
| IRCTC passenger count | `adults`, `children`, `quota` | int, int, str |
| PhonePe cashback | `cashback_pct`, `order_total` | float, float |

```mermaid
flowchart LR
    U[User input] --> V[Variables in memory]
    V --> O[Operators compute]
    O --> P[print / f-string output]
```

**Worked example — UPI receipt message (pseudocode):**

```
store payer_name as string
store amount as float after converting input
store txn_id as string
print f-string with rupee symbol and two decimals
```

**Key idea:** Session 2 feels small, but it is the same language powering payment apps, recommendation engines, and GenAI tools later in the course.

---

## H. Debugging TypeErrors — Read the Error Message

> 💡 **Analogy:** A TypeError is the fire alarm telling you two things do not fit together — like pouring milk into a petrol tank.

**One-line definition:** A **TypeError** happens when you use an operator or function on the wrong data type.

| Error snippet | Likely cause | Fix |
|---|---|---|
| `can only concatenate str (not "int") to str` | Added string + number | Convert with `str()` or `int()` |
| `unsupported operand type(s) for +: 'int' and 'str'` | Mixed types in math | Cast input before `+` |
| `invalid literal for int()` | User typed "twenty" | Validate input or use try/except later |

```python
# Broken
age = input("Age: ")
print(age + 1)

# Fixed
age = int(input("Age: "))
print(age + 1)
```

```mermaid
flowchart TD
    E[Error message] --> R[Read last line]
    R --> T[Find type words]
    T --> F[Fix cast or operator]
    F --> X[Re-run cell]
```

**Key idea:** Errors are teachers, not enemies. Read the last line of the traceback — it usually names the types that clashed.

---


## I. Running Your First Cells — Step by Step

| Step | Action | What you should see |
|---|---|---|
| 1 | New Colab notebook | Empty code cell |
| 2 | `print("Hello")` + Shift+Enter | `Hello` below cell |
| 3 | `name = "Asha"` then `print(name)` | `Asha` |
| 4 | `type(name)` | `<class 'str'>` |
| 5 | Restart runtime + rerun from top | Same results if order preserved |

```mermaid
flowchart LR
    C[Code cell] --> R[Shift+Enter]
    R --> O[Output below]
    O --> N[Next cell]
```

**Worked example — chai shop receipt variables:**

```python
shop = "Corner Chai"
cups = 2
price_per_cup = 15.0
total = cups * price_per_cup
print(f"{{cups}} cups from {{shop}}: ₹{{total:.2f}}")
```

| Variable | Type | Role |
|---|---|---|
| shop | str | Shop name on receipt |
| cups | int | Count of items |
| price_per_cup | float | Rupees with paise |
| total | float | Computed line amount |

**Common beginner questions:**

| Question | Short answer |
|---|---|
| Why `3.0` not int? | Decimal point makes it float |
| Can I change a variable? | Yes — reassignment replaces value |
| What if cell order wrong? | NameError — rerun from top |

**Key idea:** Treat the notebook like a recipe — ingredients (variables) must exist before you cook (compute).

---

## J. Variable Naming — Do's and Don'ts

| Do | Don't | Why |
|---|---|---|
| `monthly_salary` | `ms` | Readable in six months |
| `item_count` | `item count` | Spaces invalid |
| `total_gst` | `Total_GST` mixed | Pick one case style |
| `is_active` | `active` alone | bool names read as questions |

```mermaid
flowchart LR
    N[Clear name] --> R[Readable code]
    R --> M[Easier debugging]
    M --> T[Team collaboration]
```

**Worked example — renaming unclear code:**

| Before | After | Improvement |
|---|---|---|
| `x = 45000` | `monthly_salary = 45000` | Meaning clear |
| `t = 18` | `gst_percent = 18` | Unit obvious |
| `f = True` | `is_gst_inclusive = True` | bool reads as yes/no |

**Key idea:** You spend more time reading code than writing it — names are documentation.

---

## K. Print Debugging — Your First Superpower

Before fancy debuggers, use **print** to see variable values:

```python
bill = 800
tip_pct = 15
tip = bill * tip_pct / 100
print("DEBUG bill:", bill, "tip:", tip)
```

| When stuck | Print this |
|---|---|
| Wrong total | intermediate variables |
| Unexpected type | `type(x)` |
| Which branch ran | message inside each if branch |

**Key idea:** `print("DEBUG:", variable)` is professional habit — not just for beginners.

---

## Practice Exercises

**1. Pattern Recognition** — For each value, name the type: (a) `3.0`, (b) `"3.0"`, (c) `3`, (d) `True`, (e) `"True"`. Which pairs look alike but behave differently?

**2. Concept Detective** — A student runs `print(10 / 4)` and gets `2.5`, then `print(10 // 4)` and gets `2`. Explain why both are correct but different.

**3. Real-Life Application** — You are building a Zomato-style receipt. List five values as variables with types (include int, float, str). Name each variable clearly.

**4. Spot the Error** — This code crashes: `age = input("Age: "); print(age + 1)`. What error type appears? What two-line fix would you apply?

**5. Planning Ahead** — Write pseudocode for a tip calculator: ask bill amount in rupees, compute 15% tip, print bill + tip + total with an f-string. Mention where you convert types.

---

> ✅ **You're done!** Variables, types, operators, and I/O are the atoms of every Python program in this course — from data cleaning to machine learning to GenAI agents. Next session you will add **decisions** with if/elif/else so your programs branch like real apps do.
"""


# ---------------------------------------------------------------------------
# SESSION 3 PRE-READ
# ---------------------------------------------------------------------------

def session3_preread(mental_map: str) -> str:
    return f"""# Control Flow & Decision Making
---

{mental_map}

## What You'll Learn

In this pre-read, you'll discover:

- How **if / elif / else** run different code paths based on conditions
- How **boolean logic** (and, or, not) combines multiple tests
- How **comparison operators** produce True or False values
- How to **trace nested conditions** step by step and predict output
- How real apps — UPI limits, Swiggy surge, loan checks — use decisions every second

---

## A. The if Statement — One Fork in the Road

> 💡 **Analogy:** At a traffic junction, if the light is green you go; otherwise you stop.

**One-line definition:** An **if statement** runs a block of code only when a **condition** evaluates to **True**.

```python
score = 72
if score >= 60:
    print("Pass")
else:
    print("Retake")
```

```mermaid
flowchart TD
    C{{score >= 60?}}
    C -->|True| P[Print Pass]
    C -->|False| F[Print Retake]
```

| Part | Role |
|---|---|
| `if` | Start the decision |
| condition | Expression that is True or False |
| `:` | Starts the block |
| indented body | Code that runs when True |
| `else` | Optional — runs when False |

**Key idea:** Python checks the condition once. If True, it runs the `if` block and **skips** the `else`.

---

## B. elif and else — Multiple Branches

> 💡 **Analogy:** A restaurant menu with Veg / Non-veg / Dessert — you pick **one** path.

**One-line definition:** **elif** adds extra conditions between `if` and `else` so your program can choose among three or more outcomes.

```python
temp = 38
if temp > 40:
    print("Heatwave alert")
elif temp > 30:
    print("Hot day")
else:
    print("Comfortable")
```

| temp value | Branch that runs |
|---|---|
| 45 | First `if` — Heatwave |
| 38 | First `elif` — Hot day |
| 22 | `else` — Comfortable |

```mermaid
flowchart TD
    T{{temp > 40?}}
    T -->|Yes| H[Heatwave]
    T -->|No| T2{{temp > 30?}}
    T2 -->|Yes| HOT[Hot day]
    T2 -->|No| OK[Comfortable]
```

**Key idea:** Order matters. Put the strictest or highest threshold first when ranges overlap.

---

## C. Boolean Logic — AND, OR, NOT

> 💡 **Analogy:** Entering a concert needs a **ticket and** valid ID. A sale applies if you are a **member or** have a coupon.

**One-line definition:** **Boolean logic** combines True/False conditions using `and`, `or`, and `not`.

| Operator | True when | Everyday read |
|---|---|---|
| A and B | Both True | "Both must hold" |
| A or B | At least one True | "Either is enough" |
| not A | A is False | "Opposite of A" |

**AND truth table:**

| A | B | A and B |
|---|---|---|
| True | True | True |
| True | False | False |
| False | True | False |
| False | False | False |

**OR truth table:**

| A | B | A or B |
|---|---|---|
| True | True | True |
| True | False | True |
| False | True | True |
| False | False | False |

```mermaid
flowchart LR
    A1[Age >= 18] --> C1{{and}}
    A2[Has ID] --> C1
    C1 --> OUT1[Allow entry]
```

**Key idea:** `and` is stricter. `or` is looser. Use `()` when mixing them.

---

## D. Comparison Operators — Building Conditions

> 💡 **Analogy:** A luggage scale compares your bag's weight to the limit.

**One-line definition:** **Comparison operators** test how two values relate and always return a **bool**.

| Operator | Meaning | Example |
|---|---|---|
| == | equal to | `score == 100` |
| != | not equal | `status != "banned"` |
| >, <, >=, <= | greater / less | `age > 18` |

| Symbol | Meaning |
|---|---|
| `=` | Assign a value to a variable |
| `==` | Compare two values for equality |

```python
x = 5      # assignment
x == 5     # comparison — True

score = 82
if 75 <= score < 90:
    print("Grade B")
```

**Key idea:** Conditions inside `if` must evaluate to True or False — not assignment statements.

---

## E. Nested Conditions — Decisions Inside Decisions

> 💡 **Analogy:** An outer gate checks your ticket. An inner gate checks your seat section.

**One-line definition:** A **nested condition** is an if statement inside another if block.

```python
country = "IN"
amount = 1500

if country == "IN":
    if amount > 1000:
        print("GST applies")
    else:
        print("Below GST threshold")
else:
    print("International order")
```

| country | amount | Output |
|---|---|---|
| IN | 1500 | GST applies |
| IN | 500 | Below GST threshold |
| US | 1500 | International order |

```mermaid
flowchart TD
    O{{country == IN?}}
    O -->|No| INT[International rules]
    O -->|Yes| I{{amount > 1000?}}
    I -->|Yes| GST[GST applies]
    I -->|No| LOW[Below threshold]
```

**Key idea:** Deep nesting (4+ levels) gets hard to read. Often `and` / `or` or early `elif` chains are clearer.

---

## F. Tracing Execution — Predict Before You Run

> 💡 **Analogy:** Following a board game rulebook move by move before rolling dice.

**One-line definition:** **Tracing** is following each condition in order to determine which lines execute.

```python
x = 15
if x > 20:
    print("A")
elif x > 10:
    print("B")
else:
    print("C")
# Output: B
```

| Step | Check | Result |
|---|---|---|
| 1 | `x > 20` | False — skip |
| 2 | `x > 10` | True — print B |
| 3 | `else` | Skipped |

**Key idea:** Tracing is a core interview and debugging skill.

---

## G. Decisions in Indian Apps — UPI, Swiggy, IRCTC

> 💡 **Analogy:** Every "Proceed to pay" button hides dozens of if-statements checking balance, limits, and fraud flags.

**One-line definition:** Production apps encode **business rules** as conditions — the same if/elif/else you write in Colab.

| App | Condition (plain English) | Python-style sketch |
|---|---|---|
| PhonePe | If amount > ₹1,00,000 require extra OTP | `if amount > 100000 and not otp_verified:` |
| Swiggy | If rain alert and peak hour, add surge fee | `if is_raining and is_peak:` |
| IRCTC | If waitlist number <= 10 show high chance | `if waitlist <= 10:` |
| Paytm | If KYC incomplete block wallet send | `if not kyc_complete:` |

```mermaid
flowchart TD
    U[User action] --> C{{Rule checks}}
    C -->|Pass| OK[Allow feature]
    C -->|Fail| MSG[Show error message]
```

**Worked example — UPI daily limit:**

| Variable | Value | Rule |
|---|---|---|
| `daily_spent` | 45000 | Max ₹1,00,000 per day |
| `this_txn` | 60000 | Would exceed limit |
| Result | Block | `if daily_spent + this_txn > 100000:` |

**Key idea:** Session 1 taught you that banks mix **rules** and **ML**. Session 3 teaches you to write the rule half yourself.

---

## H. Validation Before You Decide

> 💡 **Analogy:** A bouncer checks ID format before checking age — garbage input gets rejected early.

**One-line definition:** **Input validation** uses if-statements to reject bad data before main logic runs.

```python
score = int(input("Score (0-100): "))
if score < 0 or score > 100:
    print("Invalid score")
else:
    if score >= 60:
        print("Pass")
    else:
        print("Retake")
```

| Check | Why |
|---|---|
| Range 0–100 | Prevents nonsense grades |
| Non-empty string | Prevents blank usernames |
| Positive amount | Prevents negative UPI transfers |

```mermaid
flowchart TD
    I[Input] --> V{{Valid?}}
    V -->|No| E[Error message]
    V -->|Yes| L[Main business logic]
```

**Key idea:** Validate first, decide second. Real apps never trust raw input.

---


## I. Combining Decisions — Real Rule Chains

> 💡 **Analogy:** Airport security: domestic vs international (outer), then baggage weight (inner), then random screening (extra check).

**One-line definition:** **Rule chains** stack conditions the way apps stack checks before showing a feature.

```python
logged_in = True
is_premium = False
cart_total = 1200

if logged_in:
    if cart_total >= 999:
        discount = 100
    elif is_premium:
        discount = 50
    else:
        discount = 0
    print(f"Discount: ₹{{discount}}")
else:
    print("Please log in")
```

| logged_in | cart_total | is_premium | discount |
|---|---|---|---|
| True | 1200 | False | 100 |
| True | 500 | True | 50 |
| True | 500 | False | 0 |
| False | any | any | login message |

```mermaid
flowchart TD
    L{{Logged in?}}
    L -->|No| LOGIN[Show login]
    L -->|Yes| C{{cart >= 999?}}
    C -->|Yes| D100[₹100 off]
    C -->|No| P{{Premium?}}
    P -->|Yes| D50[₹50 off]
    P -->|No| D0[No discount]
```

**Swiggy-style surge (sketch):**

| Condition | Message |
|---|---|
| rain and peak | "+₹30 surge fee" |
| rain only | "+₹15 surge fee" |
| else | standard fee |

**Key idea:** Apps feel "smart" because many small if-checks run in sequence — you are learning to write that logic.

---

## J. Truth Table Practice — AND / OR / NOT

Fill before class (answers below for instructor):

| A | B | A and B | A or B |
|---|---|---|---|
| True | True | ? | ? |
| True | False | ? | ? |
| False | True | ? | ? |
| False | False | ? | ? |

| A | not A |
|---|---|
| True | ? |
| False | ? |

```mermaid
flowchart TD
    T[Truth tables] --> A[AND stricter]
    T --> O[OR looser]
    T --> N[NOT flip]
```

**PhonePe example:** `pin_ok and balance_ok and not blocked` — all must pass for send money.

**Key idea:** When in doubt, draw a two-row truth table on paper before coding compound conditions.

---

## K. Comparison Pitfalls — = vs ==

| Code | Valid? | Meaning |
|---|---|---|
| `x = 5` | Yes | assign 5 to x |
| `x == 5` | Yes | compare x to 5 |
| `if x = 5:` | **No** | SyntaxError |
| `if x == 5:` | Yes | branch when equal |

```python
status = "gold"
if status == "gold":
    print("15% loyalty discount")
```

**IRCTC sketch:** `if quota == "TATKAL" and age >= 12` — two comparisons with and.

**Key idea:** One equals assigns; two equals compares — the most common beginner syntax error in Session 3.

**Quick check:** Before Session 3 class, rewrite `if age = 18` correctly on paper.

---

## Practice Exercises

**1. Pattern Recognition** — Without running code, what prints when `x = 5` then when `x = 2` in an if/else that prints "A" when `x > 3` else "B"?

**2. Concept Detective** — Login needs valid email **and** password length >= 8. Write the condition using `and`.

**3. Real-Life Application** — List three apps that use if/else today. Describe one condition each checks.

**4. Spot the Error** — Why does `if age = 18:` fail? What single character fixes it?

**5. Planning Ahead** — Design grade bands A ≥ 90, B ≥ 75, C ≥ 60, else F with if/elif/else pseudocode. Explain why order matters.

---

> ✅ **You're done!** You can now branch code like real products — pass/fail, eligibility, discounts, and tax rules all start with if/elif/else. Next session you will add **loops** so programs repeat without copy-pasting.
"""


# ---------------------------------------------------------------------------
# SESSION 4 PRE-READ
# ---------------------------------------------------------------------------

def session4_preread(mental_map: str) -> str:
    return f"""# Loops, Iteration & Repetitive Logic
---

{mental_map}

## What You'll Learn

In this pre-read, you'll discover:

- Why **loops** replace copy-paste code when the same action must run many times
- How **for loops** walk through lists, strings, and number ranges
- How **while loops** repeat until a condition becomes False
- How **range()**, **break**, and **continue** give you fine control over repetition
- How to **iterate lists and strings** to compute sums, averages, and patterns
- When to pick **for** vs **while** in real Indian app scenarios

---

## A. Why Loops Beat Copy-Paste

> 💡 **Analogy:** Washing ten plates means repeating scrub–rinse–dry. You do not write a new card for each plate.

**One-line definition:** A **loop** is a block of code that repeats until a condition or collection is finished.

```mermaid
flowchart LR
    S[Same task\nmany times] --> L[Write loop\nonce]
    L --> R[Run on\neach item]
    R --> D[Done]
```

| Situation | Without a loop | With a loop |
|---|---|---|
| Sum 5 test scores | Five `+` lines | One `for` over the list |
| Print "Hello" 100 times | 100 print lines | `for i in range(100)` |
| Retry UPI until success | Hard to manage | `while` with counter |

**Key idea:** Loops handle **collections** — prices, rows, characters. Every data workflow later relies on iteration.

---

## B. for Loops — Repeat for Each Item

> 💡 **Analogy:** A baggage carousel — each bag passes once; you inspect **each bag** without knowing the count in advance.

**One-line definition:** A **for loop** runs its block once for every item in a sequence.

```python
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(fruit)
```

```mermaid
flowchart TD
    Start[Start for loop] --> Next{{More items?}}
    Next -->|Yes| Body[Run loop body]
    Body --> Next
    Next -->|No| End[Continue after loop]
```

| Goal | Pattern |
|---|---|
| Print every item | `for x in my_list: print(x)` |
| Build a total | `total = 0` then `for n in nums: total += n` |
| Count matches | `count = 0` then `if` inside loop |

**Key idea:** Read aloud: *"For each item in the collection, do the body."*

---

## C. range() — Counting Without a List

> 💡 **Analogy:** Elevator floor buttons — **range()** generates the numbers for you.

**One-line definition:** **range()** produces integers you can loop over without building a full list.

```python
for i in range(5):
    print(i)   # 0, 1, 2, 3, 4
```

| Call | Numbers produced | Common use |
|---|---|---|
| `range(5)` | 0–4 | Repeat 5 times from zero |
| `range(1, 6)` | 1–5 | Count from 1 to 5 inclusive |
| `range(0, 10, 2)` | 0, 2, 4, 6, 8 | Step by 2 |
| `range(10, 0, -1)` | 10 down to 1 | Countdown |

```mermaid
flowchart LR
    R[range start stop step] --> N[Integer sequence]
    N --> F[for i in range]
    F --> B[Loop body]
```

**Key idea:** `range(5)` stops **before** 5 — zero-based, like list indexes.

---

## D. while Loops — Repeat Until a Condition Fails

> 💡 **Analogy:** Filling bottles **while** the tap runs. When the tap stops, you stop.

**One-line definition:** A **while loop** repeats as long as a condition stays **True**.

```python
count = 3
while count > 0:
    print(count)
    count -= 1
print("Done")
```

```mermaid
flowchart TD
    C{{Condition True?}}
    C -->|Yes| B[Run body]
    B --> U[Update something]
    U --> C
    C -->|No| E[Exit loop]
```

| Loop type | Best when | Risk |
|---|---|---|
| `for` | Known collection or count | Editing list while looping |
| `while` | Repeat until event (login OK) | **Infinite loop** if never False |

**Key idea:** Every `while` must move toward False — update a counter or read new input inside the body.

---

## E. break and continue — Steering Inside a Loop

> 💡 **Analogy:** **continue** skips one obstacle; **break** exits the entire level early.

**One-line definition:** **break** stops the whole loop; **continue** skips to the next item.

```python
for i in range(10):
    if i == 3:
        continue
    if i == 7:
        break
    print(i)
# prints 0, 1, 2, 4, 5, 6
```

| Keyword | Effect | Typical use |
|---|---|---|
| `break` | Exit loop now | Found answer; stop searching |
| `continue` | Skip to next iteration | Ignore invalid items |

```mermaid
flowchart TD
    L[Loop iteration] --> Q{{continue?}}
    Q -->|Yes| N[Next item]
    Q -->|No| W[Do work]
    W --> B{{break?}}
    B -->|Yes| X[Leave loop]
    B -->|No| N
```

**Key idea:** Order of `if` checks inside the loop matters — test special cases first.

---

## F. Iterating Lists and Strings

> 💡 **Analogy:** Reading a message word by word or letter by letter — same text, two walks.

**One-line definition:** **Iteration** visits each element of a sequence one at a time.

```python
scores = [88, 92, 75]
total = 0
for score in scores:
    total += score
average = total / len(scores)
```

| Sequence | `for item in seq` | `for i in range(len(seq))` |
|---|---|---|
| List of numbers | Sum, average, max | Every 2nd item by index |
| String | Count vowels | Replace at position |
| Order IDs | Filter with `if` | Pair with parallel list |

**Worked example — Swiggy order totals:**

| Order ID | Amount (₹) |
|---|---|
| SW001 | 320 |
| SW002 | 450 |
| SW003 | 275 |

```python
amounts = [320, 450, 275]
total = 0
for amt in amounts:
    total += amt
print(f"Total sales: ₹{{total}}")  # ₹1045
```

**Key idea:** Pandas and SQL hide loops in fast library code — but the mental model is identical: visit each row, apply a rule.

---

## G. Nested Loops — Tables and Grids

> 💡 **Analogy:** Checking every seat in every row of a cinema — outer loop = row, inner loop = seat.

**One-line definition:** A **nested loop** is a loop inside another loop, used for grids, tables, and combinations.

```python
for row in range(3):
    for col in range(2):
        print(f"Row {{row}}, Col {{col}}")
```

```mermaid
flowchart TD
    O[Outer loop] --> I[Inner loop]
    I --> W[Work on pair]
    W --> I
    I --> O
```

| Use case | Outer | Inner |
|---|---|---|
| Multiplication table | Row number 1–10 | Column 1–10 |
| Seat map | Row letter | Seat number |
| Batch UPI export | Day | Transaction in day |

**Key idea:** Nested loops multiply work — 10 × 10 = 100 iterations. Use only when you need every pair.

---

## H. Choosing for vs while — Decision Guide

> 💡 **Analogy:** **for** is a fixed school timetable; **while** is "study until you understand the chapter."

**One-line definition:** Pick **for** when you know how many times or which items; pick **while** when you stop on an event.

| Scenario | Best loop | Why |
|---|---|---|
| Sum all items in a list | `for` | Collection is known |
| Print numbers 1 to N | `for` with `range` | Fixed count |
| ATM PIN retry (3 tries) | `for` or `while` | Both work; counter clear |
| Wait for valid UPI PIN | `while` | Unknown attempts until correct |
| Read file until empty | `while` | Stop on end condition |

```mermaid
flowchart TD
    Q{{Know items or count?}}
    Q -->|Yes| F[Use for]
    Q -->|No| W[Use while]
    W --> U{{Update toward False?}}
    U -->|No| D[Danger infinite loop]
    U -->|Yes| OK[Safe while]
```

**Worked example — FizzBuzz 1 to 15 (outline):**

```
for each number n from 1 to 15:
    if n divisible by 3 and 5: print FizzBuzz
    elif n divisible by 3: print Fizz
    elif n divisible by 5: print Buzz
    else: print n
```

**Key idea:** If you cannot name what makes the loop stop, pause and redesign before coding.

---


## I. Accumulator Patterns — Building Results in a Loop

> 💡 **Analogy:** A piggy bank — each coin loop adds to the total without separate jars for coin 1, coin 2, coin 3.

**One-line definition:** An **accumulator** is a variable (often `total`, `count`, or `max_so_far`) updated inside a loop.

```python
amounts = [320, 450, 275, 510]
total = 0
count_over_400 = 0
for amt in amounts:
    total += amt
    if amt > 400:
        count_over_400 += 1
print(f"Total ₹{{total}}, orders over ₹400: {{count_over_400}}")
```

| Pattern | Starter value | Update inside loop |
|---|---|---|
| Sum | `total = 0` | `total += value` |
| Count | `count = 0` | `count += 1` when condition |
| Max | `best = values[0]` or `-inf` | `if v > best: best = v` |
| Join text | `parts = []` | `parts.append(s)` then `" ".join(parts)` |

```mermaid
flowchart LR
    I[Init accumulator] --> L[Loop each item]
    L --> U[Update accumulator]
    U --> L
    L --> F[Use final value]
```

**Worked example — daily UPI summary:**

| txn | Amount |
|---|---|
| 1 | 250 |
| 2 | 1200 |
| 3 | 89 |

Loop computes total ₹1,539 and count of txns over ₹1000 (1).

**Key idea:** Accumulators turn loops into summaries — the same pattern behind sales dashboards and ML feature counts later.

---

## J. Common Loop Bugs — Spot Before You Run

| Bug | Symptom | Fix |
|---|---|---|
| Infinite while | Notebook hangs | Update variable toward False |
| Wrong range stop | Missing last number | Remember stop is exclusive |
| Wrong indent | IndentationError | Align body with 4 spaces |
| Sum without init | Wrong total | Set `total = 0` before loop |
| break vs continue swap | Skips wrong items | Trace on paper first |

```mermaid
flowchart TD
    W[while loop] --> U{{Update var?}}
    U -->|No| BAD[Infinite risk]
    U -->|Yes| OK[Safe loop]
```

**Trace challenge — predict output:**

```python
total = 0
for n in [2, 4, 6]:
    total += n
print(total)
```

Answer: 12 — one pass, three additions.

**Key idea:** Loops fail in predictable ways; a 30-second trace prevents a 30-minute debug session.

---

## K. From Loops to Real Data — Preview

| Today (Python list) | Later (Pandas) | Same idea |
|---|---|---|
| `for x in amounts:` | `df['amount'].apply(...)` | visit each value |
| sum in loop | `df['amount'].sum()` | aggregate |
| filter with if | boolean mask | keep subset |

```mermaid
flowchart LR
    L[for loop] --> P[Pandas vectorize]
    P --> M[ML on columns]
```

**Swiggy orders → tomorrow's DataFrame** — loop today; one Pandas line next month. Same mental model.

**Key idea:** You are learning the pattern every data and ML job uses — not just toy lists.

| Preview | Session 4 today | Session 10+ later |
|---|---|---|
| Sum a list | for loop | `df['amount'].sum()` |
| Filter rows | if inside for | boolean mask |
| Repeat N times | range(N) | vectorised ops |

**Stretch question:** If you have 10,000 UPI transactions in a list, why is a loop still the right *mental model* even when Pandas hides the loop?

**Key idea:** Performance changes; the pattern does not.

| Loop type | Stop condition | Example |
|---|---|---|
| for over list | list exhausted | print each order ID |
| for over range | counter reaches stop | Attempt 1..3 |
| while | condition False | PIN until correct |

---

## Practice Exercises

**1. Pattern Recognition** — `range(4)` vs `range(1, 5)`: what numbers print? Which prints "Attempt 1" through "Attempt 4"?

**2. Concept Detective** — Three password tries: compare `for` over `range(3)` with `while attempts < 3`. One advantage of each?

**3. Real-Life Application** — Name three tasks that repeat until a condition is met. For each, pick `for` or `while` and why.

**4. Spot the Error** — A loop should print evens and stop when sum > 20 but stops early. Explain why updating `total` before the even check changed behaviour.

**5. Planning Ahead** — FizzBuzz 1–20 pseudocode with if/elif. Note where `break` or `continue` are **not** needed.

---

> ✅ **You're done!** Loops let one short program handle ten items or ten thousand. Next is a **master class** on math and logic — then **functions** for reusable code.
"""

# ---------------------------------------------------------------------------
# LECTURE GENERATORS
# ---------------------------------------------------------------------------

def session1_lecture() -> str:
    return """# Lecture Script: AI, ML & GenAI Landscape
> **Instructor Reference** — Module 1: Foundations of Data | Session 1 | Duration: 2 Hours

---

## Session Overview

**Goal:** Students leave with a clear mental map of AI, ML, and GenAI — and can classify real use cases without jargon or hype.

**Student profile at this point:** Complete beginners. Many have used ChatGPT or seen AI headlines but have no formal computer science or data background. Some may conflate all "smart" software with ML.

**Key outcome:** Every student can explain AI, ML, and GenAI in one sentence each, classify at least six real products into the right category, and map two business scenarios to the correct approach (rules, ML, or GenAI).

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| Opening & Icebreaker | 5 min | 0:05 |
| **Concept 1:** AI as the Umbrella — Rules vs Learning | 10 min | 0:15 |
| **Practical 1:** Sort the Headlines — Classification Activity | 15 min | 0:30 |
| **Concept 2:** ML Problem Types & the Data Loop | 10 min | 0:40 |
| **Practical 2:** E-commerce Scenario Cards — Supervised or Not? | 15 min | 0:55 |
| **BREAK** | 10 min | 1:05 |
| **Concept 3:** GenAI vs Traditional ML — Compose vs Score | 10 min | 1:15 |
| **Practical 3:** When NOT to Use GenAI — Spot the Wrong Tool | 15 min | 1:30 |
| **Concept 4:** The AI Ecosystem — Roles, Data, and Course Roadmap | 10 min | 1:40 |
| **Practical 4:** Map Use Cases in Pairs — Full Problem Framing | 10 min | 1:50 |
| Summary & Wrap-Up | 5 min | 1:55 |
| Q&A & Doubt Solving | 5 min | 2:00 |

---

## SEGMENT 1: Opening & Hook (8 min)


**Hook:** Display three headlines on screen (or read aloud):

1. *"Netflix's recommendation engine drives 80% of what people watch."*
2. *"ChatGPT helps students draft essay outlines in seconds."*
3. *"Smart traffic lights adjust timing based on fixed rush-hour schedules."*

**Ask the class:** *"Which of these is AI? Which is ML? Which is GenAI? Are they all three?"*

Let students call out answers — do not correct yet. Write their guesses on the board.

**Context to set:** This course takes you from Python basics → data wrangling → classical ML → GenAI agents. Today is the map of the territory. If you leave knowing *which tool fits which problem*, every future session will feel connected — not like random topics.

**Learning contract for today:**
- Define AI, ML, and GenAI in plain language
- Classify real products and headlines into the right bucket
- Frame a business problem before anyone says "let's use ChatGPT"

**Say:** *"You do not need to memorise buzzwords. You need a decision instinct: given this problem, what kind of system fits?"*

---

## SEGMENT 2: AI Umbrella — Rules vs Learning (13 min)


### The Nested Picture

Draw three nested circles on the board (or show slide):

```
        ┌─────────────────────────────┐
        │  Artificial Intelligence    │
        │   ┌─────────────────────┐   │
        │   │  Machine Learning   │   │
        │   │   ┌─────────────┐   │   │
        │   │   │ Deep Learn  │   │   │
        │   │   │  / GenAI    │   │   │
        │   │   └─────────────┘   │   │
        │   └─────────────────────┘   │
        └─────────────────────────────┘
```

**Key teaching point:** **AI is not one product.** It is a field — like "medicine" covers surgery, pharmacy, and physiotherapy.

| Category | How it works | When it fits |
|---|---|---|
| Rule-based AI | Hand-written if-then logic | Rules are known and stable |
| Machine Learning | Learns patterns from data | Patterns exist but rules are too complex |
| Generative AI | Creates new text/media from prompts | Output is open-ended language or content |

**Examples on the board:**

| Product | Category | Why |
|---|---|---|
| Thermostat: if temp > 25°C → AC on | Rule-based AI | Fixed threshold, no training |
| Spam filter | ML (classification) | Learns from millions of labelled emails |
| ChatGPT | GenAI | Generates novel text from prompts |
| Face unlock on phone | ML (classification) | Learns your face from photos |

**Ask:** *"Is a calculator AI?"* → Discuss: it computes but does not mimic human judgment. Not everything automated is AI.

**Ask:** *"Is Excel with formulas AI?"* → Formulas are rules. A pivot table summarising data is analytics, not ML — unless you add a forecast function trained on history.

**Write on board:** **AI = umbrella | ML = learns from data | GenAI = creates content**

---

## SEGMENT 3: Sort the Headlines Lab (15 min)


### Setup (2 min)

**Say:** *"You are now product analysts. Your job is to sort real features into the right bucket — and defend your choice."*

Form pairs. Give each pair a handout (physical cards or shared doc) with **8 items** below. They have **8 minutes** to sort. Each item goes in exactly one primary bucket: **Rules**, **ML**, or **GenAI**.

### The 8 Cards

| # | Feature / Headline | Correct bucket | Reasoning |
|---|---|---|---|
| 1 | Face unlock on smartphone | ML | Trained on face images; classification |
| 2 | Bank SMS: "Transaction over ₹10,000 — reply YES to confirm" | Rules | Fixed threshold trigger |
| 3 | DALL·E generating an image from a text prompt | GenAI | Creates new visual content |
| 4 | Excel formula: `=IF(A1>100,"High","Low")` | Rules | Hand-written logic |
| 5 | Spotify Discover Weekly playlist | ML | Recommendation from listening history |
| 6 | Siri reading today's weather from a database | Rules + lookup | Fetches data; no learning in the query step |
| 7 | K-means customer segmentation for marketing | ML (unsupervised) | Finds groups without pre-set labels |
| 8 | GitHub Copilot suggesting the next line of code | GenAI | Generates code from context |

**Optional stretch card (if fast pairs finish early):**

| # | Feature | Tricky answer |
|---|---|---|
| 9 | Google Maps ETA prediction | ML | Uses traffic patterns from historical data |

### Facilitation Script

**Minute 0–8:** Pairs sort silently. Walk the room. Listen for debates — "Is Siri AI or not?" is a good sign.

**Minute 8–12:** Call on 3 pairs to defend one card each. Ask dissenters: *"What would change your mind?"*

**Minute 12–15:** Reveal answer key. Highlight the tricky ones:

- **Siri weather** — mostly rules + data lookup. The *voice recognition* part is ML; reading weather is not.
- **Excel IF** — not ML. If someone says "AI" because Excel is smart, clarify: *automation ≠ learning*.
- **K-means** — ML but **unsupervised**. No "correct answer" in training data.

**Debrief question:** *"Which cards could fit two buckets depending on how the product is built?"* → Face unlock could use rules in very old phones; modern ones use ML.

**Write on board:** When sorting, ask: **Does it learn from data, follow fixed rules, or generate new content?**

---

## SEGMENT 4: ML Problem Types & Data Loop (13 min)


### The Four Question Shapes

| ML task | Question it answers | Output type | Business example |
|---|---|---|---|
| Regression | How much? | Number | Next month's revenue |
| Classification | Which category? | Label (yes/no, A/B/C) | Will customer churn? |
| Clustering | What groups exist? | Segments | Shopper personas |
| Recommendation | What should we suggest next? | Ranked list | "Customers also bought…" |

**The ML loop — draw on board:**

```
Historical data → Train model → Trained model
                                      ↓
New input ─────────────────────→ Prediction
```

**Teaching point:** ML always needs **data** and a **clear question**. "Use ML" without both is a recipe for failure.

### Supervised vs Unsupervised — Quick Table

| | Supervised | Unsupervised |
|---|---|---|
| Has labels in training? | Yes | No |
| Example question | "Will this loan default?" | "What customer groups exist?" |
| Common algorithms | Logistic regression, random forest | K-means, PCA |
| Evaluation | Compare prediction to known answer | Harder — use business judgment |

**Ask:** *"HR wants to predict who will quit in the next 90 days. Supervised or unsupervised?"* → Supervised (past quitters are labelled).

**Ask:** *"Marketing wants to discover new audience segments. Supervised or unsupervised?"* → Unsupervised (no pre-defined segment labels).

---

## SEGMENT 5: E-commerce Scenario Cards (15 min)


### Setup

**Say:** *"Same company, four problems. For each: name the ML task type and whether it is supervised."*

Display or hand out:

| # | Scenario | Task type | Supervised? |
|---|---|---|---|
| 1 | Predict December sales in rupees | Regression | Yes |
| 2 | Flag fraudulent orders before shipping | Classification | Yes |
| 3 | Group customers by purchase behaviour for campaigns | Clustering | No |
| 4 | Recommend products on the homepage | Recommendation | Usually yes (implicit feedback) |

**Activity (10 min):** Pairs fill a table with four columns: **Scenario | AI/ML/GenAI | Task type | What data is needed**

Example row for scenario 2:

| Scenario | Category | Task | Data needed |
|---|---|---|---|
| Fraud flag | ML | Classification | Past orders labelled fraud/not fraud |

**Walkthrough (5 min):** Review answers on board. Stress data requirements:

- Regression needs historical sales numbers
- Classification needs labelled fraud examples (often imbalanced — few frauds, many legit)
- Clustering needs behavioural features (RFM: recency, frequency, monetary)
- GenAI is **not** the first choice for fraud — you need auditable scores

**Ask:** *"What happens if you have no labelled fraud data?"* → You cannot train a supervised classifier yet. Options: rule-based starter, partner with bank, or manual review queue.

---

## BREAK (10 min)

---


*Suggested break prompt:* Ask students to open one app on their phone and identify one feature that is probably ML and one that is probably rules. They will share one finding after the break.

---

## SEGMENT 6: GenAI vs ML — Compose vs Score (13 min)


### The One-Line Distinction

**Write on board:** **ML scores or labels. GenAI composes.**

| | Traditional ML | Generative AI |
|---|---|---|
| Typical output | Number, category, score | Paragraph, code, image |
| Training data | Structured tables, labels | Massive text/media corpora |
| Evaluation | Accuracy, precision, RMSE | Harder — human review, rubrics |
| Best for | Prediction, ranking, detection | Drafting, explaining, brainstorming |
| Risk profile | Wrong number | Confident wrong answer (hallucination) |

### What GenAI Is Good At (in 2025)

- Drafting emails, summaries, meeting notes
- Explaining code or generating boilerplate
- Answering natural-language questions *when grounded in documents* (RAG — Module 3)
- Brainstorming marketing copy or interview prep

### What GenAI Is NOT a Substitute For

- Loan approval from structured financial features → **ML classifier**
- Inventory forecast from sales history → **ML regression**
- Guaranteed-correct legal or medical advice → **needs human expert + guardrails**
- Real-time fraud scoring at millisecond latency → **trained ML model in production**

**Ask:** *"Why would a bank not rely on ChatGPT alone for fraud detection?"*

Expected answers: latency, cost, hallucination, audit trail, no access to private transaction data in a public model.

**Key message:** GenAI is a powerful **interface layer**. Classical ML is often the **decision engine** underneath. This course teaches both — in the right order.

---

## SEGMENT 7: When NOT to Use GenAI (15 min)


### The "AI Solution" Pitch Game

Read four startup pitches aloud. Students vote: **Good fit**, **Wrong tool**, or **Needs hybrid**.

| # | Pitch | Verdict | Why |
|---|---|---|---|
| 1 | "We'll use ChatGPT to predict employee attrition from HR spreadsheets." | Wrong tool | Structured prediction → ML classification |
| 2 | "We'll use a fine-tuned LLM to draft personalised onboarding emails from employee profiles." | Good fit / hybrid | Generation task; may combine with templates |
| 3 | "We'll use GenAI to cluster customers by purchase history." | Wrong tool | Clustering is unsupervised ML on numeric features |
| 4 | "We'll use RAG so support agents query our policy PDFs in plain English." | Good fit | GenAI + retrieval — Module 3 topic |

**Activity (8 min):** Pairs rewrite pitch #1 correctly. One sentence: *"Given employee history, the system should output leave probability."* Then name the right approach.

**Share (5 min):** 2–3 pairs read their rewrite. Class votes.

**Minimal code optional (2 min):** If room has laptops, show that "classification" is a one-liner conceptually — no full training today:

```python
# Conceptual only — not training a real model today
# ML classification OUTPUT: a label and often a probability
example_output = {"employee_id": 1042, "churn_risk": "high", "probability": 0.87}
print(example_output)

# GenAI OUTPUT: open-ended text
genai_output = "Based on the profile, this employee may be disengaged because..."
print(genai_output)
```

**Say:** *"See the shape difference? One is a score you can threshold. One is prose you must interpret."*

**Expected output:**

```
{'employee_id': 1042, 'churn_risk': 'high', 'probability': 0.87}
Based on the profile, this employee may be disengaged because...
```

---

## SEGMENT 8: Ecosystem & Roadmap (12 min)


### Who Does What

| Role | Primary focus | Example deliverable |
|---|---|---|
| Data analyst | Explore and report | Weekly sales dashboard |
| Data engineer | Pipelines and storage | Nightly sync from app to data warehouse |
| Data scientist | Model training and evaluation | Churn model with 0.85 AUC |
| ML engineer | Production deployment | Fraud API serving 1000 req/sec |
| GenAI / AI engineer | LLM integration, agents | Policy Q&A bot with citations |
| Product manager | Problem definition, metrics | PRD: "Reduce support tickets 20%" |

**Ask:** *"Who owns the question 'Is this model fair to all customer segments?'"* → Data scientist + product + domain expert. Not the model alone.

### The Data Foundation

**Say:** *"Every role above depends on clean, accessible data. That is Module 1."*

Show course roadmap slide:

| Module | Topics | You will be able to… |
|---|---|---|
| Module 1 — Foundations of Data | Python, Pandas, SQL, EDA, APIs | Load, clean, query, and visualise data |
| Module 2 — Classical ML | scikit-learn, validation, metrics | Train and compare predictive models |
| Module 3 — GenAI & Agents | LLMs, RAG, tools, guardrails | Build grounded AI products |

```mermaid
flowchart LR
    M1[Module 1<br/>Data foundations] --> M2[Module 2<br/>Classical ML]
    M2 --> M3[Module 3<br/>GenAI and agents]
```

**Career paths — quick mention:**

- Love spreadsheets and charts → analyst track
- Love coding and pipelines → engineer track
- Love models and experiments → scientist track
- Love products and users → PM with AI literacy

No single path is "best." Today's session helps you see where *you* might fit.

---

## SEGMENT 9: Problem Framing Lab (10 min)


### Four Business Scenarios

Pairs complete a worksheet with columns: **Problem | Output type | Rules / ML / GenAI | Supervised? | Data needed**

| # | Scenario | Expected framing |
|---|---|---|
| 1 | HR: screen 500 resumes for "Python" skill | Hybrid: keyword rules or ML ranking; GenAI for summary drafts only |
| 2 | Retail: forecast inventory for monsoon season | ML regression; historical sales + weather features |
| 3 | Support: answer FAQs from a fixed policy doc | GenAI + RAG (Module 3); not pure prompt-only |
| 4 | Fintech: detect anomalous login locations | ML classification or anomaly detection; labelled past fraud helps |

**Timing:** 6 min work, 4 min debrief — one scenario from two pairs.

**Instructor Say for scenario 1:** *"Is 'contains the word Python' ML?"* → Rule. *"Is 'rank best fit candidates' ML?"* → Often yes, if trained on past hire outcomes.

**Exit ticket (last 2 min):** On a sticky note or chat, one sentence each:
- AI is…
- ML is…
- GenAI is…

Collect or read a sample aloud.

---

## SEGMENT 10: Summary & Wrap (8 min)


**What we covered today:**
- AI as the umbrella — rules, ML, and GenAI inside it
- ML task types: regression, classification, clustering, recommendation
- Supervised vs unsupervised — labels matter
- GenAI composes; ML scores — do not swap them blindly
- Ecosystem roles and the Module 1 → 2 → 3 path

**Bridge to next session:** *"Next class you open Google Colab and write real Python — variables, types, and your first interactive programs. Every model and dashboard later is built from those bricks."*

**Homework / self-practice:**
1. Pick three apps you use daily. For each feature, label it Rules, ML, or GenAI and write one sentence why.
2. Read the pre-read section E again. Which role sounds most interesting to you? Write two sentences on why.
3. Optional: find one news headline about "AI" this week and rewrite it with the correct term (ML, GenAI, or rules).

---

## Q&A & Doubt Solving (5 min)

**Likely questions and suggested answers:**

**Q: Is deep learning the same as ML?**
→ Deep learning is a *subset* of ML using neural networks with many layers. All deep learning is ML; not all ML is deep learning. Logistic regression is ML but not deep learning.

**Q: Do I need to learn classical ML if GenAI can do everything?**
→ Yes. Production systems combine both. GenAI is expensive and non-deterministic for many tasks. A ₹0.001 fraud score from a small ML model beats a ₹0.50 LLM call.

**Q: What's the difference between data analyst and data scientist?**
→ Analysts focus on exploration, reporting, and insights. Scientists focus on building and evaluating predictive models. Overlap exists — titles vary by company.

**Q: Is ChatGPT "AI" or "GenAI"?**
→ Both. It is a GenAI product (generates text). GenAI is a type of AI. In interviews, be specific: "GenAI assistant" is clearer than "AI."

**Q: Can a rule-based system ever be better than ML?**
→ Yes. When rules are complete, stable, and auditable — tax brackets, OTP thresholds, eligibility cutoffs. ML adds value when rules cannot capture the pattern.

---

## Instructor Notes

- **No laptop required** for most of this session — cards and board work well. Optional Python snippet in Practical 3 if time and devices allow.
- **Common student mistake:** Calling everything "AI" because it is automated. Push back gently: *"Does it learn from data?"*
- **Another mistake:** Assuming GenAI replaces data cleaning. Emphasise Module 1 data skills as non-negotiable foundation.
- **Engagement tip:** The Sort the Headlines activity is the energy peak — debrief thoroughly; do not rush.
- **Time check:** If running long before break, shorten Practical 2 walkthrough and assign e-commerce table as homework.
- **If running long after break:** Shorten Practical 4 to two scenarios instead of four.
- **Materials to prepare:** 8 (+1 optional) printed or digital cards; course roadmap slide; exit ticket sticky notes or chat form.
- **Diversity note:** Use Indian context examples (UPI fraud alerts, monsoon inventory, ₹ thresholds) — students relate faster than US-only examples.

---

## Common Errors (Student Mental Models to Correct)

| Misconception | Correction |
|---|---|
| "AI = ChatGPT" | AI is a field; ChatGPT is one GenAI product |
| "More AI is always better" | Match tool to problem; rules are often enough |
| "ML works with no data" | ML needs examples; quality and quantity matter |
| "GenAI always tells the truth" | Hallucination is a core risk; verify outputs |
| "I can skip Python and jump to LLMs" | Data and code skills underpin every AI role |

---

## Appendix: Full Classification Answer Key (Instructor Only)

| Item | Bucket | One-line defence |
|---|---|---|
| Face unlock | ML | Learns face patterns from images |
| Bank OTP threshold | Rules | Fixed amount trigger |
| DALL·E | GenAI | Creates images from text |
| Excel IF | Rules | User-written logic |
| Discover Weekly | ML | Learns taste from history |
| Siri weather | Rules + lookup | Retrieves API data |
| K-means segments | ML (unsupervised) | Finds clusters in data |
| Copilot | GenAI | Generates code suggestions |
| Maps ETA | ML | Predicts from traffic patterns |


---

## SEGMENT 11: Supplemental Code Demos (Instructor Optional)

### Demo A — Rule threshold vs ML score (3 min)

```python
amount = 15000
if amount > 10000:
    print("RULE: OTP required for ₹", amount)
fraud_score = 0.82
if fraud_score > 0.7:
    print("ML: Review transaction — score", fraud_score)
```

**Output:**
```
RULE: OTP required for ₹ 15000
ML: Review transaction — score 0.82
```

**Break it down:**
- First block is rule-based — same threshold for everyone
- fraud_score simulates a trained model output
- Production UPI uses both rules and ML

**Ask:** Where would you draw the line between rule and ML for a ₹50,000 transfer?

**Common mistake:** Putting every check in ML.

**Fix:** Keep hard regulatory limits as auditable rules; use ML for pattern anomalies.

### Demo B — Churn risk toy loop (3 min)

```python
customers = [
    {"name": "Asha", "days_idle": 120, "churned": 1},
    {"name": "Ravi", "days_idle": 5, "churned": 0},
    {"name": "Meera", "days_idle": 95, "churned": 1},
]
for c in customers:
    risk = "high" if c["days_idle"] > 90 else "low"
    print(c["name"], "→", risk, "| actual:", c["churned"])
```

**Output:**
```
Asha → high | actual: 1
Ravi → low | actual: 0
Meera → high | actual: 1
```

**Break it down:**
- List of dicts represents a customer table
- Simple rule mimics what ML learns automatically
- Labels in churned column — supervised learning target

**Ask:** What features would Flipkart use to predict delivery delay?

**Common mistake:** Saying ML needs no data.

**Fix:** List features: distance, prep time, rain, traffic, time of day.

### Demo C — Compose vs score (3 min)

```python
customer, issue = "Priya", "late delivery"
draft = f"Dear {customer}, we apologise for the {issue}. ₹100 credit applied."
print("GENAI DRAFT:", draft)
score = 0.91
print("ML FRAUD SCORE:", score)
```

**Output:**
```
GENAI DRAFT: Dear Priya, we apologise for the late delivery. ₹100 credit applied.
ML FRAUD SCORE: 0.91
```

**Break it down:**
- f-string draft simulates GenAI-style composition
- Single numeric score suits audit and thresholds
- Same company may use both in one workflow

**Ask:** Why should fraud score not be a free-form GenAI paragraph?

**Common mistake:** Using GenAI for numeric decisions without validation.

**Fix:** Use ML classifier with logged features and reproducible scores.

### Indian context scenario bank (reference)

| # | Scenario | Expected category | Notes |
|---|---|---|---|
| 1 | BHIM UPI daily limit check | Rules | Fixed ₹1,00,000/day |
| 2 | Zomato restaurant ranking | ML | Learning from ratings and orders |
| 3 | Bank chatbot draft for failed txn | GenAI | Open-ended language |
| 4 | IRCTC tatkal queue position display | Rules + lookup | Not predictive ML |
| 5 | Paytm fraud anomaly flag | ML | Learns unusual patterns |
| 6 | Canva text-to-image banner | GenAI | Creates new media |
| 7 | GST slab calculation | Rules | Statutory brackets |
| 8 | Swiggy rain surge multiplier | Rules or ML hybrid | Business chooses design |

### Facilitation timing cheat sheet

| Minute | Activity | Instructor move |
|---|---|---|
| 0–5 | Headline hook | Write guesses, no corrections |
| 5–15 | AI umbrella | Draw nested circles |
| 15–30 | Sort headlines | Walk room during pair work |
| 30–40 | ML problem types | Draw data loop |
| 40–55 | E-commerce cards | Stress data requirements |
| 55–65 | Break | Prompt: one ML + one rule feature on phone |
| 65–75 | GenAI vs ML | Emphasise compose vs score |
| 75–90 | Wrong tool pitches | Pairs rewrite pitch #1 |
| 90–100 | Ecosystem | Show Module 1→3 roadmap |
| 100–110 | Problem framing | Exit ticket three definitions |
| 110–120 | Q&A + quiz | Collect exit tickets |

### Exit ticket rubric

| Response quality | AI definition | ML definition | GenAI definition |
|---|---|---|---|
| Strong | Field / umbrella | Learns from data | Creates content |
| Acceptable | Smart computers | Prediction from data | ChatGPT-like |
| Needs follow-up | "ChatGPT" only | "Advanced AI" vague | Same as AI |

### Pre-read alignment notes

| Pre-read section | Live session segment | Do not repeat |
|---|---|---|
| A — AI umbrella | Segment 2 | Full history timeline |
| B — ML types | Segment 4 | Every algorithm name |
| C — GenAI | Segment 6 | Transformer architecture depth |
| D — Framing | Segment 9 | Full responsible AI policy |
| E — Ecosystem | Segment 8 | Salary discussions |

### Student worksheet — Problem framing template

```
Scenario name: _______________________
Given (inputs): _______________________
The system should output: _______________________
Output type (circle): number | label | text/media
Best approach (circle): Rules | ML | GenAI
Supervised? yes / no / n/a
One data source needed: _______________________
One responsible AI question: _______________________
```

### Stretch activities for fast pairs

1. Debate: Should Swiggy ETA be rules or ML? Defend with data needs.
2. Rewrite a news headline that says "AI" with the precise term.
3. Sketch a hybrid flow: UPI txn → rule limit → ML anomaly → GenAI customer SMS draft → human approve.

### Glossary wall (post on LMS)

| Term | One-line student definition |
|---|---|
| AI | Computers doing tasks that seem intelligent |
| ML | Systems that improve by learning patterns in data |
| GenAI | AI that creates new text, code, or images |
| Supervised | Learning from examples with known answers |
| Unsupervised | Finding structure without labels |
| Hallucination | GenAI stating false facts confidently |
| RAG | Search docs first, then generate answer |
| Regression | Predicting a number |
| Classification | Predicting a category |

---

## End-of-Session Quiz (5 Questions)

1. Define AI, ML, and GenAI in one sentence each.
2. Classify: UPI OTP above ₹10,000; Swiggy ETA; ChatGPT email draft.
3. What ML problem type is "predict monthly sales"?
4. Name two responsible AI habits when using GenAI for customer support.
5. Which role builds nightly data pipelines — analyst, engineer, or scientist?

**Answer key (instructor):** AI=umbrella field; ML=learns from data; GenAI=creates content. Rules/ML/GenAI respectively. Regression. Human review; verify facts. Data engineer.

---

## Homework Rubric

| Criterion | Excellent (4) | Good (3) | Needs Work (2) | Incomplete (1) |
|---|---|---|---|---|
| Use-case mapping | 4 clear categories with data sources | 3 mostly correct | 2 with gaps | 1 or missing |
| Headline sort | 8/8 defended | 6–7/8 | 4–5/8 | <4 |
| Written framing | 2 scenarios with I/O types | 2 partial | 1 complete | 0 |
| Reflection | Thoughtful responsible AI note | Good | Brief | Missing |

**Total:** /16 — Pass threshold: 10/16

---

## Materials Checklist

- [ ] Slide: nested AI / ML / GenAI diagram
- [ ] 8 (+1 optional) classification cards
- [ ] Course roadmap slide (Modules 1–3)
- [ ] Whiteboard markers
- [ ] Exit ticket form or sticky notes
- [ ] Timer visible to students

---

## Timing Contingencies

| Situation | Action |
|---|---|
| Running 10 min behind before break | Shorten Practical 2 walkthrough; assign e-commerce table as homework |
| Running long after break | Shorten Practical 4 to two scenarios instead of four |
| Low energy | Stand/sit vote on one headline card |
| Advanced students finish early | Stretch: Google Maps ETA — ML or rules? |
| No projector | Use chat poll for headline sort |

---

## FAQ — Q&A (8+ Questions)

**Q: Is ChatGPT "AI" or "GenAI"?** → Both. GenAI product inside AI field. Say "GenAI assistant" in interviews.

**Q: Can a rule-based system beat ML?** → Yes when rules are complete, stable, auditable.

**Q: Do I need math for ML?** → Module 1 builds Python/data first; Module 2 adds needed math.

**Q: Is Excel with formulas AI?** → Formulas are rules. Forecast on history is ML.

**Q: What's deep learning vs ML?** → Deep learning uses neural nets with many layers.

**Q: Will GenAI replace data jobs?** → No — pipelines and cleaning stay essential.

**Q: What is RAG?** → Retrieval + generation — Module 3 topic.

**Q: How pick a career path?** → Match ecosystem role to what excites you.


---

## SEGMENT 12: Instructor Deep-Dive — Indian Market Examples

### Case study table — classify together

| Product feature | Rules | ML | GenAI | Notes |
|---|---|---|---|---|
| NPCI UPI txn limit | ✓ | | | Regulatory cap |
| Paytm fraud alert | | ✓ | | Scores from history |
| Swiggy menu description AI | | | ✓ | Draft text |
| IRCTC waitlist number | ✓ | | | Deterministic queue |
| Amazon "customers also bought" | | ✓ | | Recommendation |
| Bank GenAI email draft | | | ✓ | Human review required |

### Code block — framing helper

```python
def frame_problem(given: str, output: str) -> dict:
    kind = "unknown"
    if output in ("number", "label"):
        kind = "ML"
    elif output == "text":
        kind = "GenAI"
    elif output == "rule":
        kind = "Rules"
    return {"given": given, "output": output, "suggested": kind}

print(frame_problem("past sales", "number"))
print(frame_problem("policy PDF question", "text"))
```

**Output:**
```
{'given': 'past sales', 'output': 'number', 'suggested': 'ML'}
{'given': 'policy PDF question', 'output': 'text', 'suggested': 'GenAI'}
```

**Break it down:**
- Function returns a dict summary — preview of structured thinking
- Output type drives suggested category
- Real projects start with this conversation before coding

**Ask:** What output type for "is this email spam?"

**Common mistake:** Skipping the output-type question and jumping to tools.

**Fix:** Write one sentence: *Given ___, output ___.*

### Interview prep — one-liners

| Term | One-liner for interviews |
|---|---|
| AI | Field of systems mimicking intelligent tasks |
| ML | Subset that learns patterns from data |
| GenAI | Creates new content from prompts |
| Supervised | Learning with labelled examples |
| Hallucination | Confident but wrong GenAI output |

### Session 1 exit checklist

- [ ] Student can define AI, ML, GenAI
- [ ] Student sorted 6+ headline cards correctly
- [ ] Student completed one framing worksheet row
- [ ] Student named one responsible AI habit
- [ ] Student knows Module 1→3 roadmap

"""


def session2_lecture() -> str:
    return """# Lecture Script: Python Fundamentals
> **Instructor Reference** — Module 1: Foundations of Data | Session 2 | Duration: 2 Hours

---

## Session Overview

**Goal:** Students write and run Python in Google Colab using variables, data types, operators, input/output, and f-strings — with habits that scale to data and ML work later.

**Student profile at this point:** Attended Session 1 (AI landscape). No prior coding required; some may have tried calculators or Excel formulas. All need hands-on confidence in Colab.

**Key outcome:** Every student completes a **profile card** program (name, age, city, favourite language) and a **tip calculator** that handles user input and formatted output without type errors.

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| Opening & Colab Setup | 5 min | 0:05 |
| **Concept 1:** Variables, Types, and `type()` | 10 min | 0:15 |
| **Practical 1:** First Cells — Assign, Inspect, Print | 15 min | 0:30 |
| **Concept 2:** Operators — Arithmetic and Comparison | 10 min | 0:40 |
| **Practical 2:** Expressions Live — `/` vs `//`, PEMDAS | 15 min | 0:55 |
| **BREAK** | 10 min | 1:05 |
| **Concept 3:** input(), print(), and f-strings | 10 min | 1:15 |
| **Practical 3:** Profile Card Lab | 15 min | 1:30 |
| **Concept 4:** Type Errors and Casting | 10 min | 1:40 |
| **Practical 4:** Tip Calculator + Deliberate Error Demo | 10 min | 1:50 |
| Summary & Wrap-Up | 5 min | 1:55 |
| Q&A & Doubt Solving | 5 min | 2:00 |

---

## SEGMENT 1: Opening & Colab Setup (8 min)


**Hook:** Show a blank Colab notebook. Run:

```python
print("Hello, future AI engineer!")
```

**Ask:** *"What just happened? Where did that text come from?"* → Python executed a command; `print` sent output to the screen.

**Context to set:** Session 1 was the map. Session 2 is the first tool in your hands. Every dataset you load, every model you train, every chart you draw — it all starts with variables and expressions in Python.

**Learning contract for today:**
- Create and name variables with correct types
- Use operators to compute values
- Ask the user for input and show formatted output
- Fix the most common beginner type errors

**Say:** *"You cannot break Colab. Run cells, read errors, fix, rerun. That loop is programming."*

### Colab Setup (live — 3 min)

1. Open [colab.research.google.com](https://colab.research.google.com)
2. **File → New notebook**
3. Rename: `Session2_Python_Fundamentals_<YourName>`
4. First cell → switch to **Markdown**, title: `# Session 2 — Python Fundamentals`
5. Second cell → **Code**

**Write on board:** Shift+Enter = run cell

---

## SEGMENT 2: Variables, Types & type() (13 min)


### Variables Are Labels

| Concept | Syntax | Example |
|---|---|---|
| Assign | `name = value` | `age = 25` |
| Reassign | same name, new value | `age = 26` |
| Inspect type | `type(x)` | `type(age)` → int |

**The four types today:**

| Type | Python keyword | Example | Real use |
|---|---|---|---|
| int | `int` | `2026`, `-3` | Count, year, age |
| float | `float` | `99.5`, `3.0` | Price, temperature |
| str | `str` | `"Priya"`, `'AI'` | Names, messages |
| bool | `bool` | `True`, `False` | Flags (later with if) |

**Key teaching point:** Python **infers** type from the value you assign. You rarely write `int x = 5` like in other languages — just `x = 5`.

**Naming conventions:**
- `snake_case` for variables: `bill_amount`
- Avoid spaces and reserved words (`print`, `input`, `if` are not variable names)

**Ask:** *"Is `3.0` an int or a float?"* → float. The decimal point matters even if `.0`.

---

## SEGMENT 3: First Cells Lab (15 min)


### Live code — students type along

**Cell 1 — Basic assignments**

```python
name = "Priya"
age = 25
height_m = 1.62
is_learning_python = True

print(name)
print(age)
print(height_m)
print(is_learning_python)
```

**Expected output:**

```
Priya
25
1.62
True
```

**Ask:** *"What type is each variable?"* Students guess before you reveal:

```python
print(type(name))
print(type(age))
print(type(height_m))
print(type(is_learning_python))
```

**Expected output:**

```
<class 'str'>
<class 'int'>
<class 'float'>
<class 'bool'>
```

**Cell 2 — Reassignment**

```python
age = 25
print("Before:", age)
age = 26
print("After birthday:", age)
```

**Expected output:**

```
Before: 25
After birthday: 26
```

**Cell 3 — Strings use quotes**

```python
course = "AI & ML"
print(course)
# course = AI & ML   # Uncomment to show SyntaxError — no quotes = broken
```

**Walkthrough tip:** Run the broken line deliberately if time allows. Read the **SyntaxError** aloud — "Python expected a string."

**Say/Ask prompts:**
- *"What happens if you spell `naem` instead of `name`?"* → NameError later
- *"Can a variable name start with a number?"* → No: `2nd_place = 1` fails

---

## SEGMENT 4: Operators (13 min)


### Arithmetic

| Op | Meaning | Note |
|---|---|---|
| `+` `-` `*` | Standard math | |
| `/` | Division | Always returns **float** in Python 3 |
| `//` | Floor division | Drops decimal part |
| `%` | Remainder | Useful for even/odd |
| `**` | Power | `2 ** 3` = 8 |

### Comparison (preview for Session 3)

| Op | Result type |
|---|---|
| `==`, `!=`, `>`, `<`, `>=`, `<=` | bool (True/False) |

**Key teaching point:** `/` vs `//` trips up every cohort. Ten divided by four is **2.5** with `/` and **2** with `//`.

---

## SEGMENT 5: Expressions Lab (15 min)


```python
print("10 + 3 =", 10 + 3)
print("10 - 3 =", 10 - 3)
print("10 * 3 =", 10 * 3)
print("10 / 3 =", 10 / 3)
print("10 // 3 =", 10 // 3)
print("10 % 3 =", 10 % 3)
print("2 ** 4 =", 2 ** 4)
```

**Expected output:**

```
10 + 3 = 13
10 - 3 = 7
10 * 3 = 30
10 / 3 = 3.3333333333333335
10 // 3 = 3
10 % 3 = 1
2 ** 4 = 16
```

**Ask:** *"Why is 10 % 3 equal to 1?"* → 3 goes into 10 three times with remainder 1.

**PEMDAS demo:**

```python
print(2 + 3 * 4)       # 14, not 20
print((2 + 3) * 4)     # 20
```

**Comparison preview:**

```python
print(10 > 7)    # True
print(10 == 10)  # True  — note DOUBLE equals
print(10 = 10)   # SyntaxError — assignment, not comparison
```

**Deliberately show `10 = 10` error** — students will confuse `=` and `==` in Session 3.

**Extension (fast finishers):**

```python
# Convert Celsius to Fahrenheit
celsius = 38
fahrenheit = celsius * 9/5 + 32
print(f"{celsius}°C = {fahrenheit}°F")
```

---

## BREAK (10 min)

---


*Suggested break prompt:* Add a markdown cell listing three things you learned. After break, share one.

---

## SEGMENT 6: input, print & f-strings (13 min)


### The I/O Pattern

```
input()  →  always returns str
process  →  convert types if needed
print()  →  show result to user
```

| Function | Purpose | Returns |
|---|---|---|
| `input("prompt")` | Ask user for text | str |
| `print(x)` | Show output | None |
| f-string | Format text with variables | str |

**f-string rules:**
- Prefix with `f` or `F`
- Variables inside `{curly braces}`
- Optional format: `{value:.2f}` for two decimal places

```python
name = input("Your name: ")
print(f"Welcome, {name}!")
```

**Ask:** *"If the user types `25` for age, what type is it inside Python?"* → Still str until you cast.

---

## SEGMENT 7: Profile Card Lab (15 min)


### Requirements (display on slide)

Build a **Profile Card** program that:

1. Asks for: **name**, **age**, **city**, **favourite programming language** (or "none yet")
2. Stores each answer in a clearly named variable
3. Prints **two lines** using f-strings:
   - Line 1: greeting with name and city
   - Line 2: age now and age in 5 years
4. Bonus: third line with favourite language

### Starter scaffold (optional — or students write from scratch)

```python
# Profile Card Lab
name = input("Your name: ")
age = int(input("Your age: "))
city = input("Your city: ")
fav_lang = input("Favourite language (or 'none yet'): ")

print(f"Hello {name} from {city}! Welcome to Python.")
print(f"You are {age} today. In 5 years you will be {age + 5}.")
print(f"Language you are excited about: {fav_lang}")
```

**Sample run:**

```
Your name: Arjun
Your age: 22
Your city: Pune
Favourite language (or 'none yet'): Python

Hello Arjun from Pune! Welcome to Python.
You are 22 today. In 5 years you will be 27.
Language you are excited about: Python
```

**Facilitation (10 min coding, 5 min share):**
- Walk the room — top error: forgetting `int()` on age
- Call 2 students to screen-share output
- Praise readable variable names

**Say:** *"This is your first interactive program. Apps are just many inputs and outputs like this."*

---

## SEGMENT 8: Type Errors & Tip Calculator (15 min)


### The #1 Beginner Bug

```python
age = input("Age: ")
print(age + 1)   # TypeError!
```

**Error message:** `TypeError: can only concatenate str (not "int") to str`

**Why:** `input()` returns str. `"25" + 1` mixes text and number.

### Fixes

```python
# Fix 1: cast at input
age = int(input("Age: "))
print(age + 1)

# Fix 2: cast after input
age = input("Age: ")
age = int(age)
print(age + 1)
```

### Other common errors

| Error | Cause | Fix |
|---|---|---|
| NameError | Typo in variable name | Spell consistently |
| SyntaxError | Missing quote, bad `=` | Check punctuation |
| ValueError | `int("twenty")` | Validate input (later sessions) |
| TypeError | str + int | Cast with int() or float() |

**Teaching point:** Read the **last line** of the error first. It usually tells you exactly what went wrong.

---

### Practical — Tip Calculator (10 min)


### Tip Calculator — full solution

```python
# Tip Calculator
bill = float(input("Enter bill amount (₹): "))
tip_percent = 15
tip = bill * tip_percent / 100
total = bill + tip

print(f"Bill:        ₹{bill:.2f}")
print(f"Tip ({tip_percent}%): ₹{tip:.2f}")
print(f"Total:       ₹{total:.2f}")
```

**Sample run:**

```
Enter bill amount (₹): 1200
Bill:        ₹1200.00
Tip (15%): ₹180.00
Total:       ₹1380.00
```

**Ask:** *"Why `float()` for bill but not for tip_percent?"* → Bill may have paise; 15 is already an int.

### Deliberate error demo (2 min)

Run broken version first:

```python
bill = input("Enter bill amount (₹): ")
tip = bill * 0.15   # TypeError: str * float
```

**Say:** *"Every professional sees red errors daily. The skill is diagnosing in 30 seconds."*

Fix live with `float(input(...))`.

**Extension:** Ask for custom tip percentage with `int(input(...))`.

---

## SEGMENT 9: Summary & Wrap (8 min)


**What we covered today:**
- Variables and four core types: int, float, str, bool
- `type()` to inspect values
- Operators: especially `/` vs `//` and `%`
- `input()`, `print()`, and f-strings for user-facing programs
- Casting with `int()` and `float()` to avoid TypeError
- Colab discipline: one step per cell, run top to bottom

**Bridge to next session:** *"Next class we add **decisions** — if the score is above 60, pass; else, retake. Your tip calculator becomes smarter when it applies different rules for different inputs."*

**Homework / self-practice:**
1. Extend the profile card: ask for year of birth and compute age (assume current year 2026).
2. Build a **split-bill** calculator: bill + tip, divided by number of friends (use `/`).
3. Write one markdown cell in Colab explaining what `//` and `%` do — teach a friend.

---

## Q&A & Doubt Solving (5 min)

**Likely questions and suggested answers:**

**Q: When do I use int vs float?**
→ int for whole counts; float for money, measurements, and anything with decimals. When unsure with division, float is safer.

**Q: Can I use single quotes `'hello'` instead of double `"hello"`?**
→ Yes. Be consistent. Use one style per project.

**Q: Why does `10 / 2` give `5.0` not `5`?**
→ Python 3 `/` always returns float. Use `//` if you need integer division.

**Q: Colab says "session crashed" — what do I do?**
→ Runtime → Restart runtime. Re-run cells from top. Save important work to Drive often.

**Q: Is `input()` OK for real apps?**
→ For learning, yes. Production apps use forms, APIs, and validation. Same variables underneath.

---

## Instructor Notes

- **Environment:** Google Colab only — no local install required. Confirm all students can run `print("ok")` before Concept 1.
- **Common student mistake:** `print(f"Age: {age}")` without defining `age` first — run cells in order.
- **Another mistake:** `int(input("Age: "))` when user types `"twenty-two"` → ValueError. Acknowledge; full validation comes in Session 3+.
- **Live coding tip:** Make one intentional typo (`naem`) to normalise NameError.
- **Pacing:** If behind, give profile card starter code; if ahead, add split-bill extension.
- **Accessibility:** Read error messages aloud slowly. Beginners treat red text as failure — reframe as "Python's help note."
- **Time check:** If long after break, shorten Concept 4 to demo only and assign tip calculator as homework with solution posted.

---

## Common Errors — Quick Reference Sheet (share in chat)

| Code | Error | Fix |
|---|---|---|
| `print(naem)` | NameError | Fix spelling |
| `"5" + 1` | TypeError | `int("5") + 1` |
| `print(age + 1)` after input | TypeError | `int(input(...))` |
| `if age = 18` | SyntaxError | Use `==` in Session 3 |
| Missing `"` on string | SyntaxError | Close quote |

---

## Appendix: Complete Reference Notebook (Instructor Solution)

```python
# === Session 2 Reference Solution ===

# --- Variables & types ---
name = "Priya"
age = 25
print(type(name), type(age))

# --- Operators ---
print(10 / 4, 10 // 4, 10 % 4)

# --- Profile Card ---
name = input("Your name: ")
age = int(input("Your age: "))
city = input("Your city: ")
fav_lang = input("Favourite language: ")
print(f"Hello {name} from {city}!")
print(f"Age: {age}, in 5 years: {age + 5}")
print(f"Excited about: {fav_lang}")

# --- Tip Calculator ---
bill = float(input("Bill (₹): "))
tip = bill * 15 / 100
print(f"Total with 15% tip: ₹{bill + tip:.2f}")
```

---

## End-of-Session Quiz (5 Questions)

1. Define AI, ML, and GenAI in one sentence each.
2. Classify: UPI OTP above ₹10,000; Swiggy ETA; ChatGPT email draft.
3. What ML problem type is "predict monthly sales"?
4. Name two responsible AI habits when using GenAI for customer support.
5. Which role builds nightly data pipelines — analyst, engineer, or scientist?

**Answer key (instructor):** AI=umbrella field; ML=learns from data; GenAI=creates content. Rules/ML/GenAI respectively. Regression. Human review; verify facts. Data engineer.

---

## Homework Rubric

| Criterion | Excellent (4) | Good (3) | Needs Work (2) | Incomplete (1) |
|---|---|---|---|---|
| Core lab task | 4 clear categories with data sources | 3 mostly correct | 2 with gaps | 1 or missing |
| Lab completion | 8/8 defended | 6–7/8 | 4–5/8 | <4 |
| Written framing | 2 scenarios with I/O types | 2 partial | 1 complete | 0 |
| Reflection | Thoughtful responsible AI note | Good | Brief | Missing |

**Total:** /16 — Pass threshold: 10/16

---

## Materials Checklist

- [ ] Slide: nested AI / ML / GenAI diagram
- [ ] 8 (+1 optional) classification cards
- [ ] Course roadmap slide (Modules 1–3)
- [ ] Whiteboard markers
- [ ] Exit ticket form or sticky notes
- [ ] Timer visible to students

---

## Timing Contingencies

| Situation | Action |
|---|---|
| Running 10 min behind before break | Shorten Practical 2 walkthrough; assign e-commerce table as homework |
| Running long after break | Shorten Practical 4 to two scenarios instead of four |
| Low energy | Stand/sit vote on one headline card |
| Advanced students finish early | Stretch: Google Maps ETA — ML or rules? |
| No projector | Use chat poll for headline sort |

---

## FAQ — Q&A (8+ Questions)

**Q: Is ChatGPT "AI" or "GenAI"?** → Both. GenAI product inside AI field. Say "GenAI assistant" in interviews.

**Q: Can a rule-based system beat ML?** → Yes when rules are complete, stable, auditable.

**Q: Do I need math for ML?** → Module 1 builds Python/data first; Module 2 adds needed math.

**Q: Is Excel with formulas AI?** → Formulas are rules. Forecast on history is ML.

**Q: What's deep learning vs ML?** → Deep learning uses neural nets with many layers.

**Q: Will GenAI replace data jobs?** → No — pipelines and cleaning stay essential.

**Q: What is RAG?** → Retrieval + generation — Module 3 topic.

**Q: How pick a career path?** → Match ecosystem role to what excites you.


---

## SEGMENT 11: Supplemental Python Demos

### Demo — UPI receipt f-string

```python
upi_id = "priya@okhdfc"
amount = 250.50
print(f"Pay ₹{amount:.2f} to {upi_id}")
```

**Output:** `Pay ₹250.50 to priya@okhdfc`

**Break it down:** f-string embeds variables; `:.2f` formats two decimals.

**Ask:** Why two decimals for rupees?

**Common mistake:** Using comma as decimal separator.

**Fix:** Use dot: `250.50` not `250,50`.

### Demo — Split bill

```python
bill = 1200
friends = 5
print(f"Each pays ₹{bill / friends:.2f}")
```

**Output:** `Each pays ₹240.00`

**Break it down:** `/` returns float; f-string displays cleanly.

**Ask:** What if friends = 0?

**Common mistake:** Dividing by zero.

**Fix:** Validate `friends > 0` before dividing.

### Demo — Type error and fix

```python
# Broken: age = input("Age: "); print(age + 1)
age = int(input("Age: "))
print(age + 1)
```

**Break it down:** input returns str; int() enables math.

**Ask:** What error without int()?

**Common mistake:** Ignoring TypeError message.

**Fix:** Read last line of traceback.

### Colab discipline reference

| Rule | Why |
|---|---|
| One step per cell | Easier debug |
| Run top to bottom | Variables exist in order |
| Save to Drive | Sessions expire |

### Homework rubric detail

| Task | Excellent | Good | Needs work |
|---|---|---|---|
| Profile card | 4 inputs, f-strings, runs | 3 inputs | type errors |
| Tip calculator | float input, formatted | wrong math | missing cast |
| Split bill | correct / | wrong operator | incomplete |

### FAQ additions

**Q: int vs float?** → int for counts; float for money.

**Q: Why 10/2 is 5.0?** → Python 3 `/` always float.

**Q: Colab crashed?** → Restart runtime; rerun from top.

**Q: NameError?** → Run defining cell first.

**Q: ValueError on int()?** → User typed non-number.

**Q: Single vs double quotes?** → Both fine.

**Q: input in production?** → Forms/APIs later.

**Q: Save work?** → Copy to Drive early.


---

## SEGMENT 12: Extended Labs & Code Annotations

### Lab — Zomato-style line items

```python
item1, item2 = "Paneer Tikka", "Butter Naan"
price1, price2 = 280.0, 60.0
qty1, qty2 = 1, 2
subtotal = price1 * qty1 + price2 * qty2
gst = subtotal * 0.05
total = subtotal + gst
print(f"Subtotal: ₹{subtotal:.2f}")
print(f"GST 5%: ₹{gst:.2f}")
print(f"Total: ₹{total:.2f}")
```

**Output:**
```
Subtotal: ₹400.00
GST 5%: ₹20.00
Total: ₹420.00
```

**Break it down:**
- Multiple float variables for menu math
- Expression on one line for subtotal
- GST as percentage of subtotal

**Ask:** Where would you use int instead of float in this lab?

**Common mistake:** Forgetting GST is applied on subtotal not per item randomly.

**Fix:** Compute subtotal first, then tax once.

### Lab — compare / and //

```python
bill = 1000
people = 3
print("Exact share:", bill / people)
print("Whole rupees each:", bill // people)
print("Leftover rupees:", bill % people)
```

**Output:**
```
Exact share: 333.3333333333333
Whole rupees each: 333
Leftover rupees: 1
```

**Break it down:**
- `/` for exact split with decimals
- `//` for whole rupee buckets
- `%` for remainder — useful for paise adjustments

**Ask:** How would you express leftover as paise?

**Common mistake:** Using // when you need precise paise split.

**Fix:** Use float `/` and round with f-string `:.2f`.

### Student extension — EMI hint

```python
principal = 500000
rate_annual = 10.5
years = 5
# Simple interest estimate (not full EMI — concept only)
interest = principal * (rate_annual / 100) * years
print(f"Simple interest estimate: ₹{interest:,.2f}")
```

**Break it down:** Float division for rate; comma in format groups lakhs.

**Ask:** Why is this not bank-accurate EMI?

**Common mistake:** Claiming this is exact loan math.

**Fix:** Label as estimate; full EMI formula comes later.

### Session 2 materials timing

| Segment | Must-show code | Optional |
|---|---|---|
| 3 | assign + type | UPI f-string |
| 5 | / vs // | GST calc |
| 7 | profile card | EMI hint |
| 8 | tip calculator | custom tip % |



---

## SEGMENT 12: Extended Labs & Code Annotations

### Lab — Zomato-style line items

```python
item1, item2 = "Paneer Tikka", "Butter Naan"
price1, price2 = 280.0, 60.0
qty1, qty2 = 1, 2
subtotal = price1 * qty1 + price2 * qty2
gst = subtotal * 0.05
total = subtotal + gst
print(f"Subtotal: ₹{subtotal:.2f}")
print(f"GST 5%: ₹{gst:.2f}")
print(f"Total: ₹{total:.2f}")
```

**Output:**
```
Subtotal: ₹400.00
GST 5%: ₹20.00
Total: ₹420.00
```

**Break it down:**
- Multiple float variables for menu math
- Expression on one line for subtotal
- GST as percentage of subtotal

**Ask:** Where would you use int instead of float in this lab?

**Common mistake:** Forgetting GST is applied on subtotal not per item randomly.

**Fix:** Compute subtotal first, then tax once.

### Lab — compare / and //

```python
bill = 1000
people = 3
print("Exact share:", bill / people)
print("Whole rupees each:", bill // people)
print("Leftover rupees:", bill % people)
```

**Output:**
```
Exact share: 333.3333333333333
Whole rupees each: 333
Leftover rupees: 1
```

**Break it down:**
- `/` for exact split with decimals
- `//` for whole rupee buckets
- `%` for remainder — useful for paise adjustments

**Ask:** How would you express leftover as paise?

**Common mistake:** Using // when you need precise paise split.

**Fix:** Use float `/` and round with f-string `:.2f`.

### Student extension — EMI hint

```python
principal = 500000
rate_annual = 10.5
years = 5
# Simple interest estimate (not full EMI — concept only)
interest = principal * (rate_annual / 100) * years
print(f"Simple interest estimate: ₹{interest:,.2f}")
```

**Break it down:** Float division for rate; comma in format groups lakhs.

**Ask:** Why is this not bank-accurate EMI?

**Common mistake:** Claiming this is exact loan math.

**Fix:** Label as estimate; full EMI formula comes later.

### Session 2 materials timing

| Segment | Must-show code | Optional |
|---|---|---|
| 3 | assign + type | UPI f-string |
| 5 | / vs // | GST calc |
| 7 | profile card | EMI hint |
| 8 | tip calculator | custom tip % |

"""


def session3_lecture() -> str:
    return """# Lecture Script: Control Flow & Decision Making
> **Instructor Reference** — Module 1: Foundations of Data | Session 3 | Duration: 2 Hours

---

## Session Overview

**Goal:** Students write if/elif/else blocks with combined boolean conditions, trace nested logic on paper, and build two working programs: a **grade calculator** and an **eligibility checker**.

**Student profile at this point:** Comfortable with Colab, variables, types, operators, input/output, and f-strings from Session 2. Ready to turn business rules into executable code.

**Key outcome:** Every student completes a grade band program (elif chain), an eligibility checker (and/or/not), and correctly traces at least three multi-branch examples before running them.

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| Opening & Hook — Why Decisions Matter | 5 min | 0:05 |
| **Concept 1:** if / else — One Branch | 10 min | 0:15 |
| **Practical 1:** Pass/Fail Live Coding | 15 min | 0:30 |
| **Concept 2:** elif Chains & Order of Checks | 10 min | 0:40 |
| **Practical 2:** Grade Calculator Lab | 15 min | 0:55 |
| **BREAK** | 10 min | 1:05 |
| **Concept 3:** Boolean Logic & Truth Tables | 10 min | 1:15 |
| **Practical 3:** Truth Table Activity + and/or/not Live | 15 min | 1:30 |
| **Concept 4:** Nested Conditions & Tracing | 10 min | 1:40 |
| **Practical 4:** Eligibility Checker Lab | 10 min | 1:50 |
| Summary & Wrap-Up | 5 min | 1:55 |
| Q&A & Doubt Solving | 5 min | 2:00 |

---

## SEGMENT 1: Opening & Hook (8 min)


**Hook:** Ask the class: *"What happens on Swiggy when you open the app — before you see restaurants?"*

Collect answers: login check, location, serviceability, offers for members.

**Say:** *"Every one of those is an if statement. Today we write the same kind of logic in Python."*

**Context to set:** Session 2 stored data and did math. Real apps also **choose** — pass or fail, eligible or not, discount or full price. That is **control flow**.

**Learning contract for today:**
- Write if / elif / else with correct indentation
- Combine conditions with and, or, not
- Trace code on paper before running
- Build grade and eligibility programs end to end

**Write on board:** `if condition:` → True runs indented block | False skips to else/elif

---

## Concept Block 1: if / else — One Branch (10 min)

### Anatomy of a Decision

```python
score = 72

if score >= 60:
    print("Pass — well done!")
else:
    print("Retake required.")
```

| Line | Purpose |
|---|---|
| `if score >= 60:` | Condition — must be True or False |
| Indented print | Body — runs only if True |
| `else:` | Catch-all when condition is False |
| Colon `:` | Required after if/elif/else |

**Indentation rule:** Python uses whitespace (4 spaces) to know what belongs inside the branch. No curly braces `{}` like other languages.

**Comparison operators review:**

| Operator | Meaning |
|---|---|
| `==` | Equal |
| `!=` | Not equal |
| `>`, `<`, `>=`, `<=` | Greater / less |

**Critical mistake preview:**

```python
if age = 18:   # SyntaxError — assignment, not comparison
```

**Write on board:** **`=` assigns | `==` compares**

**Ask:** *"Can the condition be a variable that is already True or False?"* → Yes:

```python
is_member = True
if is_member:
    print("Member discount")
```

---

## Practical Block 1: Pass/Fail Live Coding (15 min)

### Cell 1 — Basic pass/fail

Students type along:

```python
score = int(input("Enter your score (0-100): "))

if score >= 60:
    print("Result: PASS")
else:
    print("Result: FAIL")
```

**Sample run:**

```
Enter your score (0-100): 72
Result: PASS
```

**Ask:** *"What if they type 59?"* → FAIL branch.

### Cell 2 — Boundary test

```python
score = 60
if score >= 60:
    print("Pass")
else:
    print("Fail")
# Exactly 60 passes — >= means "60 or more"
```

**Expected output:** `Pass`

**Say/Ask prompts:**
- *"What happens with score = 59?"*
- *"Do we need else? What if we only want to print on pass?"* → else is optional

### Cell 3 — Trace without running

Put on board:

```python
temperature = 45
if temperature > 40:
    print("Heatwave")
else:
    print("Normal")
```

**Activity (2 min):** Students write predicted output on paper. Then run to verify.

**Expected output:** `Heatwave`

**Debrief:** Tracing before running catches logic bugs early.

---

## Concept Block 2: elif Chains & Order of Checks (10 min)

### Why elif Exists

When you have **more than two outcomes**, use `elif`:

```python
temp = 38

if temp > 40:
    print("Heatwave alert")
elif temp > 30:
    print("Hot day")
elif temp > 20:
    print("Warm")
else:
    print("Cool")
```

**Teaching point:** Python checks **top to bottom**. First True branch wins. Rest are **skipped**.

### Order trap — demonstrate wrong order

```python
score = 95

# WRONG ORDER — everything becomes "F" tier wrongly
if score >= 60:
    print("C or above")      # 95 matches here first!
elif score >= 90:
    print("A")               # Never reached

# CORRECT ORDER — highest threshold first
if score >= 90:
    print("A")
elif score >= 75:
    print("B")
elif score >= 60:
    print("C")
else:
    print("F")
```

| score | Wrong chain prints | Correct chain prints |
|---|---|---|
| 95 | C or above | A |
| 82 | C or above | B |
| 55 | (first elif 60 fails…) | F |

**Grade band reference table:**

| Grade | Condition |
|---|---|
| A | score >= 90 |
| B | score >= 75 |
| C | score >= 60 |
| F | else |

**Key message:** Put **strictest / highest** checks first when using overlapping thresholds.

---

## SEGMENT 5: Grade Calculator Lab (15 min)


### Requirements (display on slide)

Build a **Grade Calculator** that:

1. Asks for a score (0–100) as integer
2. Prints letter grade: A ≥ 90, B ≥ 75, C ≥ 60, else F
3. Uses **elif chain** (not separate unrelated ifs)
4. Bonus: print a one-line message per grade ("Excellent!", etc.)

### Reference solution

```python
# Grade Calculator Lab
score = int(input("Enter score (0-100): "))

if score >= 90:
    grade = "A"
    message = "Excellent work!"
elif score >= 75:
    grade = "B"
    message = "Good job!"
elif score >= 60:
    grade = "C"
    message = "Passed — keep improving."
else:
    grade = "F"
    message = "Retake recommended."

print(f"Score: {score} → Grade: {grade}")
print(message)
```

**Sample runs:**

```
Enter score (0-100): 94
Score: 94 → Grade: A
Excellent work!

Enter score (0-100): 58
Score: 58 → Grade: F
Retake recommended.
```

**Facilitation (10 min code, 5 min share):**
- Walk room — common bug: wrong elif order
- Ask one student: *"Trace score=75 — which branch?"* → B
- Ask: *"Trace score=90 — A or B?"* → A (>= 90 checked first)

**Extension for fast finishers:**

```python
if score < 0 or score > 100:
    print("Invalid score — enter 0 to 100")
else:
    # elif chain here
```

Preview validation — full input checking later in course.

---

## BREAK (10 min)

---


*Suggested break prompt:* Write one real-life rule as if/else in plain English (e.g. "if rain, take umbrella"). Share after break.

---

## SEGMENT 6: Boolean Logic (13 min)


### Three operators

| Operator | English | True when |
|---|---|---|
| `and` | both must hold | all parts True |
| `or` | at least one | any part True |
| `not` | opposite | flips True↔False |

```python
age = 20
has_id = True

if age >= 18 and has_id:
    print("Entry allowed")
```

### Truth tables — draw on board

**AND**

| A | B | A and B |
|---|---|---|
| T | T | T |
| T | F | F |
| F | T | F |
| F | F | F |

**OR**

| A | B | A or B |
|---|---|---|
| T | T | T |
| T | F | T |
| F | T | T |
| F | F | F |

**NOT**

| A | not A |
|---|---|
| T | F |
| F | T |

**Physical activity tip:** Give students two True/False cards. Call out `A and B` — they stand only if BOTH true. Then `A or B` — stand if EITHER true. Muscle memory helps.

**Ask:** *"Login needs email valid AND password length >= 8. Write it."*

```python
if email_valid and password_length >= 8:
    print("Login OK")
```

**Ask:** *"Discount if member OR has coupon?"*

```python
if is_member or has_coupon:
    print("Discount applied")
```

**Precedence note:** `not` > `and` > `or`. Use parentheses when mixing: `(a or b) and c`.

---

## SEGMENT 7: Discount Rules Lab (15 min)


### Part A — Truth table fill (5 min)

Handout or slide — students fill **A and B** and **A or B** for all four rows (use T/F). Check against board tables above.

### Part B — Live coding discount rules (10 min)

```python
is_member = input("Are you a member? (yes/no): ").lower() == "yes"
has_coupon = input("Do you have a coupon? (yes/no): ").lower() == "yes"

if is_member or has_coupon:
    discount = 15
    print(f"You get {discount}% off!")
else:
    discount = 0
    print("No discount today.")

bill = float(input("Bill amount (₹): "))
final = bill * (1 - discount / 100)
print(f"Final amount: ₹{final:.2f}")
```

**Sample run (member):**

```
Are you a member? (yes/no): yes
Do you have a coupon? (yes/no): no
You get 15% off!
Bill amount (₹): 1000
Final amount: ₹850.00
```

**Discussion:** *"Should member AND coupon stack to 30%?"* → Business rule, not Python rule. Code what product asks for:

```python
if is_member and has_coupon:
    discount = 25
elif is_member or has_coupon:
    discount = 15
else:
    discount = 0
```

**Say:** *"Same syntax, different business decision. Always clarify rules before coding."*

---

## Concept Block 4: Nested Conditions & Tracing (10 min)

### When to nest

```python
country = "IN"
amount = 1500

if country == "IN":
    if amount > 1000:
        print("GST applies — include 18% in invoice")
    else:
        print("Below GST registration threshold")
else:
    print("International — apply export rules")
```

**vs flat and:**

```python
if country == "IN" and amount > 1000:
    print("GST applies")
```

| Style | Use when |
|---|---|
| Nested | Different inner logic per outer branch |
| `and` | Single combined test, same action |

### Trace-the-output — board exercise

```python
x = 15
if x > 20:
    print("A")
elif x > 10:
    print("B")
else:
    print("C")
```

**Trace table on board:**

| Step | Condition | True? | Action |
|---|---|---|---|
| 1 | x > 20 → 15 > 20 | No | skip |
| 2 | x > 10 → 15 > 10 | Yes | print B |
| 3 | else | — | skipped |

**Expected output:** `B`

**Second trace (harder):**

```python
logged_in = True
is_admin = False

if logged_in:
    if is_admin:
        print("Admin panel")
    else:
        print("User dashboard")
else:
    print("Please log in")
```

**Expected output:** `User dashboard`

---

## Practical Block 4: Eligibility Checker Lab (10 min)

### Scenario

A simplified **loan eligibility** check (educational — not financial advice):

| Rule | Requirement |
|---|---|
| Age | 21 to 60 inclusive |
| Income | ≥ ₹25,000 per month |
| Documents | PAN submitted |
| Credit | Not blacklisted |

### Reference solution

```python
# Eligibility Checker Lab
print("=== Loan Eligibility Check ===")

age = int(input("Age: "))
income = float(input("Monthly income (₹): "))
has_pan = input("PAN submitted? (yes/no): ").lower() == "yes"
blacklisted = input("Credit blacklisted? (yes/no): ").lower() == "yes"

# Combined conditions
age_ok = age >= 21 and age <= 60
income_ok = income >= 25000
docs_ok = has_pan
credit_ok = not blacklisted

if age_ok and income_ok and docs_ok and credit_ok:
    print("✅ ELIGIBLE — proceed to application.")
elif not age_ok:
    print("❌ Ineligible: age must be 21–60.")
elif not income_ok:
    print(f"❌ Ineligible: income ₹{income:.0f} below ₹25,000 minimum.")
elif not docs_ok:
    print("❌ Ineligible: PAN document required.")
elif not credit_ok:
    print("❌ Ineligible: credit blacklist flag.")
else:
    print("❌ Ineligible: review required.")
```

**Sample run (eligible):**

```
=== Loan Eligibility Check ===
Age: 28
Monthly income (₹): 45000
PAN submitted? (yes/no): yes
Credit blacklisted? (yes/no): no
✅ ELIGIBLE — proceed to application.
```

**Sample run (income fail):**

```
Age: 30
Monthly income (₹): 18000
PAN submitted? (yes/no): yes
Credit blacklisted? (yes/no): no
❌ Ineligible: income ₹18000 below ₹25,000 minimum.
```

**Facilitation (7 min code, 3 min debrief):**
- Highlight `not blacklisted` as readable credit check
- Ask: *"Why store age_ok instead of one giant if?"* → Readable, debuggable
- Connect to Session 1: banks use **ML** for fraud; **rules** for hard cutoffs like age

**Trace quiz (if time):** age=19, income=50000, pan=yes, blacklisted=no → which message?

**Answer:** Ineligible age (first failing elif in simplified version — discuss order if using combined if).

---

## SEGMENT 10: Summary & Wrap (8 min)


**What we covered today:**
- if / else and elif chains — order of checks matters
- Grade calculator pattern — overlapping thresholds top-down
- Boolean logic: and, or, not — truth tables
- Nested conditions vs combined and
- Tracing execution before running
- Eligibility checker — real-world rule encoding

**Bridge to next session:** *"Next class: **loops** — repeat without copy-paste. Grade every student in a list. Process every row in a table. Same Colab, new superpower."*

**Homework / self-practice:**
1. Add input validation to grade calculator: reject scores below 0 or above 100.
2. Build a **movie ticket** pricer: child (<12) ₹100, student (12–18) ₹150, adult ₹200.
3. Write three trace questions (if/elif) and swap with a partner — predict output before running.

---

## Q&A & Doubt Solving (5 min)

**Likely questions and suggested answers:**

**Q: elif vs separate if statements?**
→ elif is mutually exclusive — only one runs. Separate ifs can each fire independently. Use elif for grade bands; separate ifs when checking unrelated flags.

**Q: Can I use if inside if? How deep?**
→ Yes. Keep nesting shallow (2–3 levels). Refactor with and/or or functions if deeper.

**Q: Why `==` for strings but `is` sometimes online?**
→ For learning, always use `==` for value comparison. `is` checks identity — advanced topic; avoid for now.

**Q: My code does nothing when I run it — no error.**
→ Condition was False and you had no else. Add print debug: `print("debug:", score)` before if.

**Q: How does this connect to ML?**
→ Model outputs (score > 0.5) become conditions. if/else wraps model decisions in apps.

---

## Instructor Notes

- **Prerequisite check:** First 5 min — confirm all can run Session 2 profile card. Pair struggling students.
- **Common mistake:** `if age = 18` — stop and fix immediately; whole cohort will hit this.
- **Another mistake:** Forgetting colon after if/elif/else — SyntaxError on next line.
- **Indentation:** Mixed tabs/spaces cause IndentationError. Colab defaults to spaces — good.
- **Truth table activity:** Physical stand/sit version takes 3 min but fixes and/or confusion for visual learners.
- **Eligibility lab:** Keep disclaimers light — "simplified teaching example."
- **Time check:** If behind, give grade calculator starter with elif skeleton empty.
- **If ahead:** Add nested GST example from pre-read section E.

---

## Common Errors — Quick Reference

| Bug | Symptom | Fix |
|---|---|---|
| `=` in if | SyntaxError | Use `==` |
| Wrong elif order | 95 gets C not A | Highest threshold first |
| Missing colon | SyntaxError next line | Add `:` after condition |
| Bad indent | IndentationError | Align with 4 spaces |
| String vs int compare | Unexpected branch | Cast input with int() |

---

## Appendix: Trace-the-Output Answer Key (Instructor)

| # | Code snippet | Output |
|---|---|---|
| 1 | x=5, if x>3 print A else B | A |
| 2 | x=2, same | B |
| 3 | x=15, elif chain to 20/10 | B |
| 4 | logged_in T, is_admin F nested | User dashboard |
| 5 | score=75, grade bands 90/75/60 | B |

---

## Appendix: Full In-Class Trace Quiz (Optional — 5 min if ahead)

Students predict output — then run:

```python
# Quiz 1
a, b = True, False
print(a and b)
print(a or b)
print(not a)

# Quiz 2
n = 8
if n > 10:
    print("X")
elif n > 5:
    print("Y")
else:
    print("Z")
```

**Answers:**

```
False
True
False

Y
```

---

## End-of-Session Quiz (5 Questions)

1. Define AI, ML, and GenAI in one sentence each.
2. Classify: UPI OTP above ₹10,000; Swiggy ETA; ChatGPT email draft.
3. What ML problem type is "predict monthly sales"?
4. Name two responsible AI habits when using GenAI for customer support.
5. Which role builds nightly data pipelines — analyst, engineer, or scientist?

**Answer key (instructor):** AI=umbrella field; ML=learns from data; GenAI=creates content. Rules/ML/GenAI respectively. Regression. Human review; verify facts. Data engineer.

---

## Homework Rubric

| Criterion | Excellent (4) | Good (3) | Needs Work (2) | Incomplete (1) |
|---|---|---|---|---|
| Core lab task | 4 clear categories with data sources | 3 mostly correct | 2 with gaps | 1 or missing |
| Lab completion | 8/8 defended | 6–7/8 | 4–5/8 | <4 |
| Written framing | 2 scenarios with I/O types | 2 partial | 1 complete | 0 |
| Reflection | Thoughtful responsible AI note | Good | Brief | Missing |

**Total:** /16 — Pass threshold: 10/16

---

## Materials Checklist

- [ ] Slide: nested AI / ML / GenAI diagram
- [ ] 8 (+1 optional) classification cards
- [ ] Course roadmap slide (Modules 1–3)
- [ ] Whiteboard markers
- [ ] Exit ticket form or sticky notes
- [ ] Timer visible to students

---

## Timing Contingencies

| Situation | Action |
|---|---|
| Running 10 min behind before break | Shorten Practical 2 walkthrough; assign e-commerce table as homework |
| Running long after break | Shorten Practical 4 to two scenarios instead of four |
| Low energy | Stand/sit vote on one headline card |
| Advanced students finish early | Stretch: Google Maps ETA — ML or rules? |
| No projector | Use chat poll for headline sort |

---

## FAQ — Q&A (8+ Questions)

**Q: Is ChatGPT "AI" or "GenAI"?** → Both. GenAI product inside AI field. Say "GenAI assistant" in interviews.

**Q: Can a rule-based system beat ML?** → Yes when rules are complete, stable, auditable.

**Q: Do I need math for ML?** → Module 1 builds Python/data first; Module 2 adds needed math.

**Q: Is Excel with formulas AI?** → Formulas are rules. Forecast on history is ML.

**Q: What's deep learning vs ML?** → Deep learning uses neural nets with many layers.

**Q: Will GenAI replace data jobs?** → No — pipelines and cleaning stay essential.

**Q: What is RAG?** → Retrieval + generation — Module 3 topic.

**Q: How pick a career path?** → Match ecosystem role to what excites you.


---

## SEGMENT 11: Supplemental Control Flow Demos

### Demo — Grade bands

```python
score = int(input("Score: "))
if score >= 90:
    print("A")
elif score >= 75:
    print("B")
elif score >= 60:
    print("C")
else:
    print("F")
```

**Break it down:** elif chain; highest threshold first.

**Ask:** Grade for score=75?

**Common mistake:** elif 60 before elif 90.

**Fix:** Order thresholds descending.

### Demo — Member OR coupon

```python
is_member = input("Member? ").lower() == "yes"
has_coupon = input("Coupon? ").lower() == "yes"
if is_member or has_coupon:
    print("15% off")
```

**Ask:** Stack to 30% if both?

**Common mistake:** Ambiguous business rule without spec.

**Fix:** Ask product owner; code explicit policy.

### Demo — GST nested

```python
country, amount = "IN", 1500
if country == "IN":
    if amount > 1000:
        print("GST applies")
```

**Ask:** Rewrite with `and`.

**Common mistake:** 4+ nesting levels.

**Fix:** Flatten with and/or.

### Trace practice bank

| x | Code | Output |
|---|---|---|
| 5 | if x>3: A else B | A |
| 2 | same | B |
| 15 | elif 20/10 | B |

### FAQ additions

**Q: elif vs if?** → elif exclusive.

**Q: == vs is?** → Use == now.

**Q: Silent code?** → False condition, no else.

**Q: ML connection?** → score > 0.5 in if.

**Q: not keyword?** → Python uses not not !

**Q: Chained comparison?** → 75 <= x < 90 valid.

**Q: Input validation?** → Check range before logic.

**Q: Blacklisted flag?** → Use not blacklisted for readability.
"""


def session4_lecture() -> str:
    return """# Lecture Script: Loops, Iteration & Repetitive Logic
> **Instructor Reference** — Module 1: Foundations of Data | Session 4 | Duration: 2 Hours

---

## Session Overview

**Goal:** Students write `for` and `while` loops with correct termination, use `range()`, `break`, and `continue`, and iterate lists and strings to solve practical problems.

**Student profile at this point:** Comfortable with variables, basic types, and `if`/`elif`/`else` from Session 3. May have seen loops in passing but confuse `range()` bounds or create infinite `while` loops.

**Key outcome:** Every student completes three labs: sum/average of a list, a FizzBuzz-style pattern, and a password retry loop with `while` + `break` — and can explain when to choose `for` vs `while`.

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| Opening & Hook | 5 min | 0:05 |
| **Concept 1:** Why Loops + for Loop Mental Model | 10 min | 0:15 |
| **Practical 1:** for Loops, range(), and List Iteration | 15 min | 0:30 |
| **Concept 2:** while Loops + Avoiding Infinite Loops | 10 min | 0:40 |
| **Practical 2:** while, break, continue Live Demos | 15 min | 0:55 |
| **BREAK** | 10 min | 1:05 |
| **Concept 3:** Index vs Value + String Iteration | 10 min | 1:15 |
| **Practical 3:** Sum, Average, and FizzBuzz-Style Lab | 20 min | 1:35 |
| **Concept 4:** Choosing for vs while + Common Pitfalls | 10 min | 1:45 |
| **Practical 4:** Password Retry with while + break | 10 min | 1:55 |
| Summary & Wrap-Up | 3 min | 1:58 |
| Q&A & Doubt Solving | 2 min | 2:00 |

---

## SEGMENT 1: Opening & Hook (8 min)


**Hook:** Show this on screen (or paste into the notebook):

```python
prices = [120, 450, 89, 310, 275]
# Someone wrote:
print(prices[0] + prices[1] + prices[2] + prices[3] + prices[4])
```

**Ask the class:** *"What happens tomorrow when the shop adds 50 more products? Do we add 50 more lines?"*

Let them answer. Then show:

```python
total = 0
for price in prices:
    total += price
print("Total:", total)
```

**Context to set:** Real data work — sales rows, sensor readings, survey answers — means repeating the same logic thousands of times. Loops are not a syntax trick. They are how programs scale.

**Learning contract for today:**
- Write `for` loops over lists and `range()`
- Write safe `while` loops that always move toward stopping
- Use `break` and `continue` on purpose, not by accident
- Build sum/average, FizzBuzz-style output, and a password retry script

**Say:** *"If you can explain when the loop stops, you understand the loop."*

---

## Concept Block 1: Why Loops + for Loop Mental Model (10 min)

### Copy-Paste vs One Pattern

Draw on the board:

```
WITHOUT LOOP          WITH for LOOP
─────────────         ─────────────
do task on item 1     for each item:
do task on item 2         do task
do task on item 3     (automatic)
... forever ...
```

**Key teaching point:** A **loop** is one recipe applied to each item in a sequence. The sequence can be a list, a string, or numbers from `range()`.

### Reading a for Loop Aloud

```python
for score in [90, 85, 72]:
    print(score)
```

Practice with the class: *"For each score in the list, print the score."* Three iterations, then done.

| Part | Name | Role |
|---|---|---|
| `for` | Keyword | Starts the loop |
| `score` | Loop variable | Holds current item |
| `in [90, 85, 72]` | Sequence | What to walk through |
| Indented block | Body | Runs once per item |

**Ask:** *"After the loop finishes, what is the last value of `score`?"* → `72` (the final item). Useful to know; do not rely on it unless intentional.

**Write on board:** **for = known collection or count → visit each**

---

## Practical Block 1: for Loops, range(), and List Iteration (15 min)

### Demo 1 — Print Each Item

```python
names = ["Ria", "Sam", "Jo"]
for name in names:
    print(f"Hello, {name}")
```

**Walk through output line by line.** Ask: *"How many times did the body run?"*

### Demo 2 — range() Variants

```python
# Zero to four
for i in range(5):
    print(i, end=" ")
print()  # 0 1 2 3 4

# One to five
for i in range(1, 6):
    print(i, end=" ")
print()  # 1 2 3 4 5

# Evens below 10
for i in range(0, 10, 2):
    print(i, end=" ")
print()  # 0 2 4 6 8
```

**Teaching moment:** `range(5)` means "start at 0, stop before 5." Same idea as list indices starting at 0.

**Ask the class before running:** *"What will `range(2, 7)` print?"* — Let them predict, then run.

### Demo 3 — Accumulator Pattern (Sum)

```python
nums = [4, 7, 2, 9, 1]
total = 0
for n in nums:
    total += n
print("Sum:", total)
```

**Explain the pattern:** Initialise before the loop (`total = 0`), update inside (`total += n`), use after (`print`).

```python
# Average — same loop, one more step
count = len(nums)
average = total / count
print("Average:", average)
```

**Live demonstration tip:** Change `nums` to a longer list live. Show that the loop body did not change — only the data did.

**Extension for faster students:**

```python
# Multiplication table for 7
n = 7
for i in range(1, 11):
    print(f"{n} x {i} = {n * i}")
```

---

## Concept Block 2: while Loops + Avoiding Infinite Loops (10 min)

### The while Mental Model

```mermaid
flowchart TD
    C{Condition True?}
    C -->|Yes| B[Body]
    B --> C
    C -->|No| E[Done]
```

**One-line definition for students:** **while** repeats *as long as* the condition is True — check first, then run, then check again.

```python
countdown = 3
while countdown > 0:
    print(countdown)
    countdown -= 1
print("Lift off!")
```

**Key teaching point:** Something inside the body must **move the condition toward False**. If you forget `countdown -= 1`, you get an infinite loop.

### for vs while — Decision Guide

| Use | Loop | Example |
|---|---|---|
| Fixed list or known count | `for` | Sum all scores in a list |
| Repeat until event | `while` | Login until correct or 3 fails |
| Process until empty | `while` | Read lines until end of file |

**Danger sign:** `while True:` without a `break` path → runs forever.

**Ask:** *"You need to retry an API call until it succeeds or you hit 5 failures. for or while?"* → Either works; `while attempts < 5` is often clearest.

---

## Practical Block 2: while, break, continue Live Demos (15 min)

### Demo 1 — Menu Loop with break

```python
while True:
    choice = input("Enter q to quit: ")
    if choice == "q":
        break
    print(f"You typed: {choice}")
print("Goodbye")
```

**Say:** *"`while True` looks scary — but `break` is the planned exit. This pattern is common in menus and games."*

### Demo 2 — continue Skips One Round

```python
for i in range(1, 8):
    if i == 4:
        continue
    print(i, end=" ")
print()
# prints 1 2 3 5 6 7 — skips 4
```

**Ask:** *"What is the difference between `continue` and `break` here?"* → `continue` skips printing 4 only; `break` would stop the whole loop at 4.

### Demo 3 — Filter While Summing (from coding problem)

```python
nums = [4, 7, 2, 9, 1]
running = 0
for n in nums:
    if n > 5:
        print(n)
    running += n
    if running > 15:
        print("Stopping early — running sum exceeded 15")
        break
```

**Discussion:** Order matters. We add every `n` to `running`, even small ones. That is why we break after 7 and 9, not only after printing large values.

---

## BREAK (10 min)

---


*Suggested break prompt:* Ask students to write on paper: one problem for `for`, one for `while`. Share one example each when class resumes.

---

## Concept Block 3: Index vs Value + String Iteration (10 min)

### Two Ways Through a List

| Style | Code | When to use |
|---|---|---|
| By value | `for x in items:` | Sum, filter, print values |
| By index | `for i in range(len(items)):` | Need position (rank, pair with another list) |

```python
items = ["pen", "book", "bag"]
for i in range(len(items)):
    print(i, items[i])
```

**Teaching point:** Prefer **by value** when you do not need the index — it is clearer.

### Strings Are Sequences

```python
word = "loop"
for ch in word:
    print(ch)
```

**Ask:** *"How many iterations for `'hello'`?"* → 5 (one per character).

**Link to data:** CSV columns, JSON strings, and user input are all text you will walk character by character or line by line later.

---

## Practical Block 3: Sum, Average, and FizzBuzz-Style Lab (20 min)

### Lab Part A — Sum and Average (8 min)

**Give students this starter:**

```python
test_scores = [78, 85, 92, 88, 74, 91, 83]

# TODO: use a loop to compute total and average
# Print: "Total: ..." and "Average: ..."
```

**Walk through solution together after 5 minutes solo work:**

```python
test_scores = [78, 85, 92, 88, 74, 91, 83]

total = 0
for score in test_scores:
    total += score

average = total / len(test_scores)
print(f"Total: {total}")
print(f"Average: {average:.1f}")
```

**Check:** Ask a student to explain why `len(test_scores)` is safe outside the loop but the `+=` must be inside.

### Lab Part B — FizzBuzz-Style (12 min)

**Rules (write on board):**

- For numbers 1 to 20:
  - Divisible by 3 and 5 → print `FizzBuzz`
  - Divisible by 3 only → print `Fizz`
  - Divisible by 5 only → print `Buzz`
  - Otherwise → print the number

**Starter:**

```python
for n in range(1, 21):
    # your if/elif chain here
    pass
```

**Solution to reveal step-by-step:**

```python
for n in range(1, 21):
    if n % 3 == 0 and n % 5 == 0:
        print("FizzBuzz")
    elif n % 3 == 0:
        print("Fizz")
    elif n % 5 == 0:
        print("Buzz")
    else:
        print(n)
```

**Common mistake to demonstrate:** Checking `% 3` before the combined `% 3 and % 5` case — show wrong output for 15 if order is wrong.

**Ask:** *"Why do we test 3 and 5 together first?"* → Otherwise 15 prints `Fizz` only.

---

## Concept Block 4: Choosing for vs while + Common Pitfalls (10 min)

### Pitfall Checklist

| Mistake | Symptom | Fix |
|---|---|---|
| Infinite while | Program never ends | Update condition variable; add break |
| Off-by-one range | Missing first or last item | Trace `range(start, stop)` — stop is exclusive |
| Modifying list while looping | Skipped items | Loop over a copy or use index carefully |
| Forgetting initialiser | Wrong sum (`total` undefined) | Set `total = 0` before loop |

**Write on board:** **INIT → LOOP → UPDATE → USE RESULT**

### Nested Loops (Brief Intro)

```python
for row in range(1, 4):
    for col in range(1, 4):
        print(f"({row},{col})", end=" ")
    print()
```

**Say:** *"Outer loop = rows. Inner loop = columns. You will see this again with tables and grids — not exam depth today, just know the pattern exists."*

---

## Practical Block 4: Password Retry with while + break (10 min)

### Lab Setup

**Scenario:** Correct PIN is `"1234"`. User gets **3 attempts**. After success, welcome message. After 3 failures, lock message.

**Starter:**

```python
CORRECT_PIN = "1234"
MAX_TRIES = 3
attempts = 0

# TODO: while loop — ask for PIN, compare, break on success
# increment attempts; if attempts == MAX_TRIES and still wrong, print locked
```

**Solution:**

```python
CORRECT_PIN = "1234"
MAX_TRIES = 3
attempts = 0

while attempts < MAX_TRIES:
    pin = input("Enter PIN: ")
    if pin == CORRECT_PIN:
        print("Access granted. Welcome!")
        break
    else:
        attempts += 1
        remaining = MAX_TRIES - attempts
        if remaining > 0:
            print(f"Wrong PIN. {remaining} attempt(s) left.")
        else:
            print("Account locked. Too many failed attempts.")
```

**Alternative with for:**

```python
CORRECT_PIN = "1234"
for attempt in range(1, 4):
    pin = input(f"Attempt {attempt}/3 — Enter PIN: ")
    if pin == CORRECT_PIN:
        print("Access granted!")
        break
else:
    # runs only if loop did NOT break
    print("Account locked.")
```

**Teaching moment:** Python's `for`/`else` is optional — mention it for advanced students; `while` version is enough for core outcome.

**Discussion:** *"Why not store the real PIN in plain text in production?"* — Brief security note: real systems hash passwords; this is a learning exercise only.

---

## Summary & Wrap-Up (3 min)

**What we covered today:**
- **for** loops over lists, strings, and `range()`
- **while** loops with a clear path to stopping
- **break** (exit early) and **continue** (skip one round)
- Accumulator pattern for **sum** and **average**
- FizzBuzz-style multi-branch logic inside a loop
- Password retry with attempt counting

**Bridge to next session:** *"Tomorrow is a master class — no heavy coding. We zoom out to the math behind True/False, sets, and functions. That math is the same engine running inside every `if` and `while` you wrote today."*

**Homework / self-practice:**
- Print squares of 1–10 using `for` and `range`
- Write a loop that counts vowels in a string
- Optional: guess-the-number game with `while` and `break`

---

## Q&A & Doubt Solving (2 min)

**Likely questions and suggested answers:**

**Q: When should I use `range(len(list))` instead of `for x in list`?**
→ Use index when you need the position or two lists aligned by index. Otherwise prefer `for x in list`.

**Q: My while loop never stops — what do I check first?**
→ Print the condition variable inside the loop. Is it changing? Is the condition ever False?

**Q: Can I use `break` in a for loop?**
→ Yes. `break` exits whichever loop it is inside — for or while.

**Q: Does `range(10)` include 10?**
→ No. It stops before 10, so you get 0 through 9.

---

## Instructor Notes

- **Live coding tip:** Deliberately create an infinite loop once (remove `countdown -= 1`), show Ctrl+C or kernel interrupt, then fix it — students remember the scare.
- **Common student mistake:** Using `for i in range(len(nums))` when `for n in nums` is enough — praise simpler code when it works.
- **Pacing:** If running long before break, shorten nested loop intro. If ahead, add guess-the-number as a 5-minute bonus.
- **Connection to course:** Mention that Pandas `.apply()` and row iteration inherit this mental model — loops become hidden inside libraries later.
- **Assessment alignment:** Coding problem tasks (squares, sum with break) map directly to Practical Blocks 1–2; assign as exit ticket if time is tight.

---

## End-of-Session Quiz (5 Questions)

1. Define AI, ML, and GenAI in one sentence each.
2. Classify: UPI OTP above ₹10,000; Swiggy ETA; ChatGPT email draft.
3. What ML problem type is "predict monthly sales"?
4. Name two responsible AI habits when using GenAI for customer support.
5. Which role builds nightly data pipelines — analyst, engineer, or scientist?

**Answer key (instructor):** AI=umbrella field; ML=learns from data; GenAI=creates content. Rules/ML/GenAI respectively. Regression. Human review; verify facts. Data engineer.

---

## Homework Rubric

| Criterion | Excellent (4) | Good (3) | Needs Work (2) | Incomplete (1) |
|---|---|---|---|---|
| Core lab task | 4 clear categories with data sources | 3 mostly correct | 2 with gaps | 1 or missing |
| Lab completion | 8/8 defended | 6–7/8 | 4–5/8 | <4 |
| Written framing | 2 scenarios with I/O types | 2 partial | 1 complete | 0 |
| Reflection | Thoughtful responsible AI note | Good | Brief | Missing |

**Total:** /16 — Pass threshold: 10/16

---

## Materials Checklist

- [ ] Slide: nested AI / ML / GenAI diagram
- [ ] 8 (+1 optional) classification cards
- [ ] Course roadmap slide (Modules 1–3)
- [ ] Whiteboard markers
- [ ] Exit ticket form or sticky notes
- [ ] Timer visible to students

---

## Timing Contingencies

| Situation | Action |
|---|---|
| Running 10 min behind before break | Shorten Practical 2 walkthrough; assign e-commerce table as homework |
| Running long after break | Shorten Practical 4 to two scenarios instead of four |
| Low energy | Stand/sit vote on one headline card |
| Advanced students finish early | Stretch: Google Maps ETA — ML or rules? |
| No projector | Use chat poll for headline sort |

---

## FAQ — Q&A (8+ Questions)

**Q: Is ChatGPT "AI" or "GenAI"?** → Both. GenAI product inside AI field. Say "GenAI assistant" in interviews.

**Q: Can a rule-based system beat ML?** → Yes when rules are complete, stable, auditable.

**Q: Do I need math for ML?** → Module 1 builds Python/data first; Module 2 adds needed math.

**Q: Is Excel with formulas AI?** → Formulas are rules. Forecast on history is ML.

**Q: What's deep learning vs ML?** → Deep learning uses neural nets with many layers.

**Q: Will GenAI replace data jobs?** → No — pipelines and cleaning stay essential.

**Q: What is RAG?** → Retrieval + generation — Module 3 topic.

**Q: How pick a career path?** → Match ecosystem role to what excites you.


---

## SEGMENT 11: Supplemental Loop Demos

### Demo — Sum and average

```python
scores = [88, 92, 75]
total = 0
for s in scores:
    total += s
print(total / len(scores))
```

**Break it down:** accumulator pattern.

**Ask:** Empty list problem?

**Common mistake:** Divide by zero on [].

**Fix:** Check len > 0.

### Demo — FizzBuzz core

```python
for n in range(1, 21):
    if n % 15 == 0:
        print("FizzBuzz")
    elif n % 3 == 0:
        print("Fizz")
    elif n % 5 == 0:
        print("Buzz")
    else:
        print(n)
```

**Ask:** Why 15 first?

**Common mistake:** Check 3 before 15.

**Fix:** Most specific condition first.

### Demo — while retry

```python
attempts = 0
pin = ""
while pin != "1234" and attempts < 3:
    pin = input("PIN: ")
    attempts += 1
```

**Break it down:** while until correct or max tries.

**Common mistake:** Infinite loop without update.

**Fix:** Increment attempts each round.

### Loop choice reference

| Pattern | Loop |
|---|---|
| Known list | for |
| Fixed count | for range |
| Until event | while |

### FAQ additions

**Q: range include stop?** → Stops before stop value.

**Q: for vs while?** → for known; while until event.

**Q: break vs continue?** → break exits; continue skips iteration.

**Q: Loop variable after?** → May hold last value.

**Q: Nested loops?** → Outer row inner col.

**Q: Pandas loops?** → Vectorised later; same idea now.

**Q: Modify list while looping?** → Avoid; copy or iterate copy.

**Q: while True?** → Only with break inside.


---

## SEGMENT 12: Extended Loop Labs

### Lab — Swiggy order IDs above threshold

```python
order_ids = ["SW100", "SW101", "SW102", "SW103"]
amounts = [320, 550, 275, 890]
THRESHOLD = 500
for i in range(len(order_ids)):
    if amounts[i] > THRESHOLD:
        print(order_ids[i], amounts[i])
```

**Output:**
```
SW101 550
SW103 890
```

**Break it down:**
- Parallel lists same length
- Index loop when both ID and amount needed
- if inside for filters rows

**Ask:** How rewrite with zip(order_ids, amounts)?

**Common mistake:** IndexError when lists different lengths.

**Fix:** Confirm len match or use zip.

### Lab — vowel counter

```python
word = "bangalore"
vowels = "aeiou"
count = 0
for ch in word:
    if ch in vowels:
        count += 1
print("Vowels:", count)
```

**Output:** `Vowels: 4`

**Break it down:** Loop over string characters; membership test with `in`.

**Ask:** Case-insensitive version?

**Common mistake:** Forgetting strings iterate by character.

**Fix:** `for ch in word.lower():`

### Lab — nested multiplication table snippet

```python
for row in range(1, 4):
    line = []
    for col in range(1, 4):
        line.append(str(row * col))
    print(" ".join(line))
```

**Output:**
```
1 2 3
2 4 6
3 6 9
```

**Break it down:** Outer row, inner col — classic nested pattern.

**Ask:** How many total iterations?

**Common mistake:** Infinite nested loop without increment.

**Fix:** for loops manage increment automatically.

### while vs for decision card

| Situation | Choose |
|---|---|
| Print 1..N | for + range |
| Sum a list | for over list |
| PIN until correct | while |
| Retry max 3 times | for range(3) or while |

### Session 4 exit checklist

- [ ] Student wrote a for loop over a list
- [ ] Student used range with correct start/stop
- [ ] Student explained break vs continue
- [ ] Student computed sum or average in a loop
- [ ] Student attempted FizzBuzz or similar

### Homework rubric (loops)

| Criterion | Excellent (4) | Good (3) | Needs Work (2) | Incomplete (1) |
|---|---|---|---|---|
| Sum/average lab | Correct logic + output | minor off-by-one | wrong accumulator | missing |
| FizzBuzz 1–20 | Correct elif order | minor branch bug | wrong range | missing |
| Password retry | 3 tries + message | no counter | infinite loop | missing |

"""


if __name__ == "__main__":
    results = write_outputs()
    print("Generated files:")
    for path, lines in results:
        ok_pre = "pre-read" in path and lines >= 450
        ok_lec = "lecture-script" in path and lines >= 750
        status = "OK" if (ok_pre or ok_lec) else "CHECK"
        print(f"  [{status}] {lines:4d} lines  {path}")
    prereads = [l for p, l in results if "pre-read" in p]
    lectures = [l for p, l in results if "lecture-script" in p]
    print(f"\nPre-reads: min={min(prereads)}, max={max(prereads)} (target 450+)")
    print(f"Lectures:  min={min(lectures)}, max={max(lectures)} (target 750+)")
