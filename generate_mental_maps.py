#!/usr/bin/env python3
"""Generate mental Map MD files from curriculum CSVs for each batch."""

from __future__ import annotations

import csv
import os
import re
from dataclasses import dataclass
from difflib import SequenceMatcher
from pathlib import Path

CONTENT_ROOT = Path(__file__).resolve().parent

MODULE_META = {
    "foundations": {
        "short": "Foundations of Data",
        "concepts": "Python · Data Stack",
        "learnt": "Python, Git, NumPy, Pandas, SQL, viz, APIs",
        "upcoming_use": "Feeds clean data into ML and GenAI builds",
    },
    "classical": {
        "short": "Classical ML",
        "concepts": "scikit-learn · Statistics",
        "learnt": "Prep, regression, classification, ensembles, clustering",
        "upcoming_use": "Predictive models before LLM grounding",
    },
    "genai": {
        "short": "GenAI & Agents",
        "concepts": "LLMs · Agents",
        "learnt": "Prompts, tools, embeddings, RAG, APIs, orchestration",
        "upcoming_use": "Ship grounded AI products and agent workflows",
    },
}


def norm(s: str) -> str:
    s = s.lower()
    s = re.sub(r"[^\w\s]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def module_key(module: str) -> str:
    m = module.lower()
    if "module 1" in m or "foundation" in m:
        return "foundations"
    if "module 2" in m or "classical" in m:
        return "classical"
    if "module 3" in m or "genai" in m or "agent" in m:
        return "genai"
    return "foundations"


def clean_module_label(module: str) -> str:
    return re.sub(r"^Module \d+:\s*", "", module).strip()


def escape_mermaid(text: str) -> str:
    return text.replace('"', "'")


def rect_node(node_id: str, label: str) -> str:
    """Rectangle node — best fit for multi-line labels."""
    return f'    {node_id}["{label}"]'


def two_line_value(text: str, max_len: int = 30) -> str:
    """Split long value text into at most two short lines."""
    text = escape_mermaid(text.strip())
    if len(text) <= max_len:
        return text
    words = text.split()
    line1: list[str] = []
    i = 0
    while i < len(words) and len(" ".join(line1 + [words[i]])) <= max_len:
        line1.append(words[i])
        i += 1
    if i >= len(words):
        return text
    line2 = " ".join(words[i:])
    if len(line2) > max_len:
        line2 = line2[: max_len - 1].rstrip() + "…"
    return "<br/>".join([" ".join(line1), line2])


def top_phrases(subtopics: str, n: int = 3, max_len: int = 48) -> list[str]:
    if not subtopics:
        return []
    parts = re.split(r"[;\n]+", subtopics)
    out = []
    for p in parts:
        p = p.strip()
        if not p:
            continue
        if ":" in p and len(p) > max_len:
            p = p.split(":", 1)[0].strip()
        if len(p) > max_len:
            p = p[: max_len - 1].rstrip() + "…"
        if p and p not in out:
            out.append(p)
        if len(out) >= n:
            break
    return out


def _hits(pattern: str, *texts: str) -> bool:
    return any(re.search(pattern, txt, re.I) for txt in texts if txt)


def mental_shift(title: str, subtopics: str, module_k: str) -> str:
    t = title.lower()
    s = subtopics.lower()
    phrases = top_phrases(subtopics, 2)
    hint = phrases[0] if phrases else title

    patterns = [
        (r"\b(?:ai\s+vs|landscape|beginner)\b", "See AI as a career map—not hype"),
        (r"\b(?:lab|setup|install|colab|vscode|secrets)\b", "Move from watching to a working dev lab"),
        (r"\b(?:developer workflow|git\b|terminal|cli\b)\b", "Think like a developer: versioned, repeatable work"),
        (r"\b(?:variables|data types?|language of ai)\b", "Code becomes your daily thinking language"),
        (r"\b(?:if-else|conditional|boolean logic|decision making)\b", "Turn business rules into executable logic"),
        (r"\b(?:for loop|while loop|automation)\b", "Replace manual repetition with loops"),
        (r"\b(?:defining functions|functions? &|modularity|organizing with functions)\b", "Design reusable building blocks, not one-off scripts"),
        (r"\b(?:data collections?|lists? and slicing|tuples?|dictionaries)\b", "Pick the right in-memory data shape"),
        (r"\b(?:file handling|reading files|json structure)\b", "Bridge programs to real files and APIs"),
        (r"\b(?:numpy|numerical foundations|multidimensional arrays)\b", "Think in vectors—speed for AI math"),
        (r"\b(?:pandas|dataframe|data table)\b", "Treat data as tables you can query and clean"),
        (r"\b(?:data cleaning|cleaning & preparation|messy data)\b", "Fix messy tables before analysis"),
        (r"\b(?:sql\b|joins?|querying)\b", "Query data like an analyst—tables and joins"),
        (r"\b(?:matplotlib|plotly|visual storytelling|eda checklist|plotting)\b", "Turn numbers into decisions via visuals"),
        (r"\b(?:requests library|api security|streamlit|agent's hands)\b", "Connect code to live services and demos"),
        (r"\b(?:ethics?|terms of service|privacy|module review)\b", "Build responsibly before scaling impact"),
        (r"\b(?:masterclass|master class)\b", "Connect math intuition to how models learn"),
        (r"\b(?:sneaker|scraping|beautifulsoup)\b", "Ship a mini end-to-end data project"),
        (r"\b(?:ml workflow|problem framing|train(?:ing)?/.?validation)\b", "Frame ML problems before picking models"),
        (r"\b(?:imputing|encoding|scaling|messy data|feature engineering)\b", "Trustworthy features beat fancy algorithms"),
        (r"\b(?:data leakage|class imbalance|cross-validation)\b", "Evaluate models that generalize"),
        (r"\b(?:linear regression|ordinary least squares|predicting numbers|predicting values)\b", "Predict numbers with interpretable lines"),
        (r"\b(?:lasso|ridge|regularization|bias-variance)\b", "Control complexity—not just fit harder"),
        (r"\b(?:mae|rmse|r-squared|regression metrics)\b", "Measure error the way stakeholders understand"),
        (r"\b(?:logistic regression|decision tree|random forest|classification)\b", "Learn patterns that separate classes"),
        (r"\b(?:roc curve|auc|threshold)\b", "Tune decisions for business trade-offs"),
        (r"\b(?:k-means|clustering|unsupervised|pca|dimensionality)\b", "Find structure without labels"),
        (r"\b(?:grid search|model selection|end-to-end pipeline)\b", "Compare models with a disciplined pipeline"),
        (r"\b(?:tokens?|context window|temperature|llm foundations)\b", "Treat LLMs as probabilistic engines"),
        (r"\b(?:prompt engineering|few-shot|chain-of-thought|zero-shot)\b", "Steer models with deliberate prompting"),
        (r"\b(?:ai agents?|tool usage|react framework|reasoning loops)\b", "Design agents that act, not only chat"),
        (r"\b(?:embeddings?|vector stores?|semantic search|semantic retrieval)\b", "Search meaning—not just keywords"),
        (r"\b(?:rag\b|retrieval-augmented|context retrieval)\b", "Ground answers in your own documents"),
        (r"\b(?:fastapi|productionizing|deployment|render)\b", "Wrap intelligence in reliable APIs"),
        (r"\b(?:langgraph|orchestration|workflow design)\b", "Orchestrate multi-step agent flows"),
        (r"\b(?:structured outputs?|json schema|output validation)\b", "Make model outputs machine-safe"),
        (r"\b(?:guardrails?|human oversight|safety)\b", "Ship AI with human-safe guardrails"),
        (r"\bmultimodal\b", "Combine text, audio, and vision pipelines"),
    ]
    for pat, msg in patterns:
        if _hits(pat, t, s):
            return msg
    if module_k == "foundations":
        return f"Strengthen data foundations around {hint}"
    if module_k == "classical":
        return f"Connect modeling choices to {hint}"
    return f"Apply GenAI ideas through {hint}"


def course_value(title: str, subtopics: str, module_k: str) -> str:
    title_l = title.lower()
    t = (title + " " + subtopics).lower()
    if _hits(r"\b(?:landscape|beginner|career|ai vs)\b", title_l):
        return "Orient to the full AI learning path ahead"
    if _hits(r"\b(?:lab setup|setting up|computing foundations?|programming foundations?)\b", title_l):
        return "Stand up the toolkit every later session assumes"
    if _hits(r"\bmaster\s*class\b", title_l):
        return "Math intuition behind algorithms you will run"
    if module_k == "foundations":
        if _hits(r"\b(?:sql|pandas|join|query)\b", t):
            return "Analyst-ready data skills across the stack"
        if _hits(r"\b(?:streamlit|requests library|eda workshop)\b", t):
            return "Prototype data products teammates can try"
        if _hits(r"\bapi\b", t) and _hits(r"\b(?:get|post|requests|streamlit|workshop)\b", t):
            return "Prototype data products teammates can try"
        return "Core stack every AI engineer repeats daily"
    if module_k == "classical":
        return "Predictive literacy for product and business KPIs"
    if "rag" in t or "embedding" in t:
        return "Grounded GenAI apps—not generic chatbots"
    if "agent" in t or "tool" in t:
        return "Automate multi-step work with agent design"
    return "Production-minded AI from prompts to deploy"


def real_life_value(title: str, subtopics: str, module_k: str) -> str:
    title_l = title.lower()
    t = (title + " " + subtopics).lower()
    if _hits(r"\b(?:landscape|beginner|career)\b", title_l):
        return "Choose roles and projects with clear AI context"
    if _hits(r"\b(?:lab setup|setting up|computing foundations?)\b", title_l):
        return "Match how professionals set up machines and repos"
    if _hits(r"\bmaster\s*class\b", title_l):
        return "Read formulas and charts without fear in interviews"
    if _hits(r"\b(?:git|terminal|developer workflow|version control)\b", t):
        return "Same habits used on real engineering teams"
    if _hits(r"\b(?:data cleaning|cleaning & preparation)\b", title_l, t):
        return "Clean messy exports before decisions"
    if "pandas" in t or "sql" in t or "eda" in t:
        return "Answer business questions from messy exports"
    if "regression" in t or "classification" in t or "cluster" in t:
        return "Forecast, segment, and score like industry ML"
    if "api" in t or "fastapi" in t or "deploy" in t:
        return "Ship features users can call from apps"
    if "prompt" in t or "llm" in t:
        return "Copilots and assistants you can control"
    if "rag" in t or "embedding" in t:
        return "Q&A on company docs and support knowledge"
    if module_k == "genai":
        return "Build assistants that act inside your tools"
    if module_k == "classical":
        return "Turn historical data into actionable scores"
    return "Skills reused in internships and AI roles"


def _session_theme(sess: SessionRow, max_len: int = 40) -> str:
    sub = sess.subtopics.strip()
    short_title = re.sub(r"^(Master [Cc]lass:?|Masterclass:?)\s*", "", sess.title).strip()
    if not sub or re.match(
        r"^(Understand|Learn|Master|Build|Enable|Design|Discover|Explore|Consolidate)\b",
        sub,
        re.I,
    ):
        text = short_title
    else:
        phrases = top_phrases(sub, 1, max_len=max_len)
        text = phrases[0] if phrases else short_title
    if len(text) > max_len:
        return text[: max_len - 1].rstrip() + "…"
    return text


def module_until_prev(sessions: list[SessionRow], idx: int) -> str:
    cur = sessions[idx]
    same = [s for s in sessions[:idx] if s.module_key == cur.module_key]
    if not same:
        return "Starting this module today"
    if len(same) <= 3:
        themes = [_session_theme(s) for s in same]
        return "<br/>".join(themes) if themes else "Earlier sessions in this module"
    if len(same) <= 6:
        themes = [_session_theme(s, 28) for s in same]
        lines: list[str] = []
        chunk = 2
        for i in range(0, len(themes), chunk):
            part = " · ".join(themes[i : i + chunk])
            if len(part) > 44:
                part = part[:43].rstrip() + "…"
            lines.append(part)
        return "<br/>".join(lines[:4])
    # Many prior sessions: show start, middle, and latest themes on separate lines
    picks = [same[0], same[len(same) // 2], same[-1]]
    lines = [_session_theme(picks[0], 28)]
    lines.append("…")
    lines.append(_session_theme(picks[2], 28))
    return "<br/>".join(lines)


def prev_module_boxes(sessions: list[SessionRow], idx: int) -> list[tuple[str, str, str, str]]:
    cur_key = sessions[idx].module_key
    order = ["foundations", "classical", "genai"]
    pos = order.index(cur_key)
    boxes = []
    for k in order[:pos][-3:]:
        meta = MODULE_META[k]
        boxes.append(
            (
                "Previous Module",
                meta["short"],
                meta["concepts"],
                f"<i>Learnt:</i> {meta['learnt']}",
            )
        )
    return boxes[-3:]


def upcoming_module_boxes(sessions: list[SessionRow], idx: int) -> list[tuple[str, str, str, str]]:
    cur_key = sessions[idx].module_key
    order = ["foundations", "classical", "genai"]
    pos = order.index(cur_key)
    boxes = []
    for k in order[pos + 1 : pos + 4]:
        meta = MODULE_META[k]
        boxes.append(
            (
                "Upcoming Module",
                meta["short"],
                meta["concepts"],
                f"<i>Uses:</i> {meta['upcoming_use']}",
            )
        )
    return boxes[:3]


@dataclass
class SessionRow:
    module: str
    title: str
    subtopics: str
    module_key: str
    module_label: str


def find_session_folder(batch_dir: Path, title: str, folders: list[str]) -> str | None:
    n = norm(title)
    best = None
    best_ratio = 0.0
    for f in folders:
        ft = norm(re.sub(r"^Session \d+- ", "", f))
        ratio = SequenceMatcher(None, n, ft).ratio()
        if ratio > best_ratio:
            best_ratio = ratio
            best = f
    return best if best_ratio >= 0.72 else None


def build_diagram(sessions: list[SessionRow], idx: int) -> str:
    cur = sessions[idx]
    prev_mods = prev_module_boxes(sessions, idx)
    up_mods = upcoming_module_boxes(sessions, idx)
    until_prev = module_until_prev(sessions, idx)
    focus = top_phrases(cur.subtopics, 3)
    shift = mental_shift(cur.title, cur.subtopics, cur.module_key)
    cv = course_value(cur.title, cur.subtopics, cur.module_key)
    rv = real_life_value(cur.title, cur.subtopics, cur.module_key)
    mod_name = cur.module_label

    lines = [
        "```mermaid",
        "%%{init: {'flowchart': {'nodeSpacing': 55, 'rankSpacing': 65, 'diagramPadding': 24}}}%%",
        "flowchart TB",
        "linkStyle default stroke-width:3px",
        "",
        'subgraph foundation[" Foundation "]',
        "direction TB",
    ]

    prev_ids = []
    for i, (kind, name, concepts, learnt) in enumerate(prev_mods):
        nid = f"P{i}"
        prev_ids.append(nid)
        label = (
            f"<b>{kind}</b><br/>{escape_mermaid(name)}<br/>"
            f"<i>[{escape_mermaid(concepts)}]</i><br/>{learnt}"
        )
        lines.append(rect_node(nid, label))

    mid = "CURMOD"
    until_lbl = (
        f"<b>Current Module Until<br/>Previous Session</b><br/>"
        f"<i>{escape_mermaid(mod_name)}</i><br/>{until_prev}"
    )
    lines.append(rect_node(mid, until_lbl))

    cur_id = "CURSES"
    title_short = escape_mermaid(cur.title)
    if len(title_short) > 32:
        title_short = title_short[:31].rstrip() + "…"
    focus_lines = focus[:2] if focus else []
    focus_txt = "<br/>".join(escape_mermaid(p) for p in focus_lines)
    shift_short = escape_mermaid(shift)
    if len(shift_short) > 40:
        shift_short = shift_short[:39].rstrip() + "…"
    cur_parts = [
        "<b>Current Session</b>",
        f"<b>{title_short}</b>",
        f"<i>Shift:</i> {shift_short}",
    ]
    if focus_txt:
        cur_parts.append(focus_txt)
    cur_lbl = "<br/>".join(cur_parts)
    lines.append(rect_node(cur_id, cur_lbl))
    lines.append("end")
    lines.append("")

    lines.append('subgraph value[" Value "]')
    lines.append("direction LR")
    cv_id, rv_id = "CVAL", "RVAL"
    lines.append(
        rect_node(cv_id, f"<b>Course Value</b><br/>{two_line_value(cv)}")
    )
    lines.append(
        rect_node(rv_id, f"<b>Real-Life Value</b><br/>{two_line_value(rv)}")
    )
    lines.append("end")
    lines.append("")

    if up_mods:
        lines.append('subgraph future[" Future Path "]')
        lines.append("direction TB")
        up_ids = []
        for i, (kind, name, concepts, uses) in enumerate(up_mods):
            uid = f"U{i}"
            up_ids.append(uid)
            uses_short = escape_mermaid(re.sub(r"^<i>Uses:</i>\s*", "", uses, flags=re.I))
            if len(uses_short) > 36:
                uses_short = uses_short[:35].rstrip() + "…"
            label = (
                f"<b>{kind}</b><br/>{escape_mermaid(name)}<br/>"
                f"<i>[{escape_mermaid(concepts)}]</i><br/>{uses_short}"
            )
            lines.append(rect_node(uid, label))
        lines.append("end")
        lines.append("")

    # edges
    if prev_ids:
        lines.append(f"{prev_ids[-1]} ==>|&nbsp;Foundation&nbsp;| {mid}")
        for a, b in zip(prev_ids, prev_ids[1:]):
            lines.append(f"{a} -.->|&nbsp;Builds&nbsp;| {b}")
    else:
        lines.append('START["Course Start"] ==>|&nbsp;Begin&nbsp;| CURMOD')

    lines.append(f"{mid} ==>|&nbsp;Progress&nbsp;| {cur_id}")
    lines.append(f"{cur_id} ==>|&nbsp;Course Path&nbsp;| {cv_id}")
    lines.append(f"{cur_id} ==>|&nbsp;Real-Life&nbsp;| {rv_id}")
    if up_mods:
        lines.append(f"{cur_id} ==>|&nbsp;Next Module&nbsp;| {up_ids[0]}")
        for a, b in zip(up_ids, up_ids[1:]):
            lines.append(f"{a} -.->|&nbsp;Ahead&nbsp;| {b}")

    lines.extend(
        [
            "",
            "classDef prevBox fill:#E8F4FC,stroke:#2B6CB0,stroke-width:2px,color:#1A202C",
            "classDef curModBox fill:#FFF8E6,stroke:#B7791F,stroke-width:2px,color:#1A202C",
            "classDef curSessBox fill:#E6FFFA,stroke:#0D9488,stroke-width:3px,color:#1A202C",
            "classDef valueBox fill:#F3E8FF,stroke:#7C3AED,stroke-width:2px,color:#1A202C",
            "classDef futureBox fill:#ECFDF5,stroke:#047857,stroke-width:2px,color:#1A202C",
            "classDef startBox fill:#F7FAFC,stroke:#4A5568,stroke-width:2px,color:#1A202C",
        ]
    )

    prev_class = ",".join(prev_ids) if prev_ids else ""
    if prev_class:
        lines.append(f"class {prev_class} prevBox")
    if not prev_ids:
        lines.append("class START startBox")
    lines.append(f"class {mid} curModBox")
    lines.append(f"class {cur_id} curSessBox")
    lines.append(f"class {cv_id},{rv_id} valueBox")
    if up_mods:
        lines.append(f"class {','.join(up_ids)} futureBox")

    lines.append("```")
    return "\n".join(lines)


def load_curriculum(csv_path: Path) -> list[SessionRow]:
    rows: list[SessionRow] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            module = row.get("Module", "").strip()
            title = row.get("Session Name", "").strip()
            subtopics = row.get("Sub Topics / Learning Objectives", "").strip()
            if not title:
                continue
            mk = module_key(module)
            rows.append(
                SessionRow(
                    module=module,
                    title=title,
                    subtopics=subtopics,
                    module_key=mk,
                    module_label=clean_module_label(module),
                )
            )
    return rows


def collect_folders(batch_dir: Path) -> dict[str, str]:
    mapping = {}
    for root, dirs, _ in os.walk(batch_dir):
        for d in dirs:
            if d.startswith("Session "):
                full = os.path.join(root, d)
                mapping[d] = full
    return mapping


def main() -> None:
    stats = {"written": 0, "missing_folder": [], "skipped_exists": 0}

    for batch_dir in sorted(CONTENT_ROOT.glob("IITP-*")):
        if not batch_dir.is_dir():
            continue
        csv_files = list(batch_dir.glob("Curriculum*.csv"))
        if not csv_files:
            print(f"No CSV for {batch_dir.name}")
            continue
        sessions = load_curriculum(csv_files[0])
        folder_names = list(collect_folders(batch_dir).keys())

        for idx, sess in enumerate(sessions):
            folder = find_session_folder(batch_dir, sess.title, folder_names)
            if not folder:
                stats["missing_folder"].append((batch_dir.name, sess.title))
                continue
            folder_path = None
            for root, dirs, _ in os.walk(batch_dir):
                if folder in dirs:
                    folder_path = Path(root) / folder
                    break
            if not folder_path:
                stats["missing_folder"].append((batch_dir.name, sess.title))
                continue

            out_name = f"mental Map: {sess.title}.md"
            out_path = folder_path / out_name
            content = build_diagram(sessions, idx) + "\n"
            out_path.write_text(content, encoding="utf-8")
            stats["written"] += 1

        print(f"{batch_dir.name}: {len(sessions)} sessions processed")

    print(f"\nTotal written: {stats['written']}")
    if stats["missing_folder"]:
        print(f"Missing folders: {len(stats['missing_folder'])}")
        for b, t in stats["missing_folder"][:15]:
            print(f"  {b}: {t}")


if __name__ == "__main__":
    main()
