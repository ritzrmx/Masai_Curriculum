Create a Mermaid mental-model diagram for the given current session.

Goal:
The diagram should help students understand how the current live session fits into the course, what they already know, how this session helps in real life, and how it connects to future learning.

Input will be provided after this prompt as either:
1. A curriculum CSV file/content plus the current session name, or
2. A module-wise list of all sessions plus the current session name.

Instructions:
1. Identify:
   - Previous completed modules before the current session.
   - Current module content covered until the previous session.
   - The current session.
   - Upcoming modules after the current session.
   - Course-level and real-life relevance of the current session.

2. Create a Mermaid `flowchart` mental model, not a large mindmap.

3. Box structure:
   - One box per previous module, but show a maximum of 3 previous-module boxes.
   - If there are more than 3 previous modules, include only the 3 most relevant or closest previous modules and summarize their role at a bird's-eye level.
   - One box for "Current Module Until Previous Session".
   - One main highlighted box for "Current Session".
   - One or two boxes connecting the current session to course value and real-life value.
   - One box per upcoming module, but show a maximum of 3 upcoming-module boxes.
   - Upcoming boxes must strictly represent upcoming modules, not upcoming sessions.
   - If there are more than 3 upcoming modules, include only the next 3 modules and summarize them at a bird's-eye level.

4. In previous and upcoming module boxes:
   - First show whether it is a previous/upcoming module.
   - Then show the module name.
   - Below that, in brackets, mention the two major tech stacks or concepts.
   - Then show short tech learnt / tech to be used.

5. Do not use explicit session numbers in the diagram labels.
   - Use labels like "Previous Session", "Current Session", "Current Module Until Previous Session", "Upcoming Module".
   - Do not write "Session 35", "Session 36", etc.

6. Keep content bird's-eye level.
   - Avoid too many bullets.
   - Keep each box concise and readable.
   - Keep box text light: use short phrases, not paragraph-style content.
   - Do not overfill boxes with too many topics; choose only the most useful tech stacks or concepts.
   - The current session box should clearly explain the mental shift or live lecture value.

7. Make the Mermaid visually interesting:
   - **Pick shapes for text fit first**, then use color to show role.
   - Use colors via `classDef`.
   - Use only light background colors so text remains easy to read.
   - Avoid dark, saturated, or heavily filled box backgrounds.
   - Keep font contrast strong and readable against the chosen background.
   - Use thick arrows.
   - Add meaningful arrow labels wherever they improve the mental model.
   - Arrow labels must be short and polished, usually 1-3 words, such as `Foundation`, `Components`, `Blueprint`, `Course Path`, `Real-Life Use`, or `Next Module`.
   - Do not use placeholder arrow labels like `<you add proper name here>`.
   - Give arrow-label text breathing room using Mermaid-safe spacing only, for example `A ==>|&nbsp;Foundation&nbsp;| B`.
   - If an arrow label looks cramped or touches its label border, shorten the label first; do not use CSS, `padding`, `margin`, or `style` attributes.
   - Use `nodeSpacing`, `rankSpacing`, and `diagramPadding` (suggested: 55, 65, 24).
   - Avoid inline CSS because it may render as visible text.
   - Do not put styling instructions inside node labels. Text such as `padding: 8px`, `style=`, `font-size`, `margin`, or CSS snippets must never appear inside the visible box content.
   - Avoid slant-box syntax if it causes `/.../` artifacts in preview.

   **Node shapes — required mapping:**

   | Box role | Mermaid syntax | Shape | Notes |
   |---|---|---|---|
   | Course start | `START["Course Start"]` | Rectangle | One short line only |
   | Previous module | `P0["…"]` | Rectangle | Multi-line labels OK |
   | Current module until previous session | `CURMOD["…"]` | Rectangle | Split long header with `<br/>` |
   | Current session (highlight) | `CURSES["…"]` | Rectangle | Use `classDef` for emphasis — not stadium/circle |
   | Course value / Real-life value | `CVAL["…"]` / `RVAL["…"]` | Rectangle | **Never** use diamond `{…}` — text gets clipped |
   | Upcoming module | `U0["…"]` | Rectangle | Multi-line labels OK |

   **Do not use for multi-line text:**
   - Diamond / rhombus: `{label}` or `{{label}}`
   - Stadium / pill for long labels: `(["long text"])`
   - Circle / double-circle: `((label))`, `(((label)))`
   - Subroutine double-border for dense text: `[[label]]` (prefer rectangle)
   - Parallelogram / trapezoid: `[/label/]`, `[\label\]`

   **Label layout rules:**
   - Max ~5 lines per box; max ~28 characters per line where possible.
   - Break long headers across lines: `Current Module Until<br/>Previous Session`.
   - Use short phrase stacks (`Lab · Python · Git`) instead of one long sentence.
   - Put module progress on separate lines with `<br/>`, not a single overflowing row.
   - Highlight the current session with `classDef` stroke width and fill — not awkward node shapes.

8. Output only the Mermaid code block.
   - Do not add explanation before or after the Mermaid.

Expected Mermaid style:
- Use `flowchart TB`.
- Use subgraphs for foundation, value, and future sections (simple titles: `Foundation`, `Value`, `Future Path`).
- Use **rectangle nodes** `NODE["label"]` for every box except optional one-line start.
- Use `classDef` for previous/current/value/future boxes.
- Use `linkStyle default stroke-width:3px`.
- Use `<br/>`, `<b>`, `<i>`, and `&nbsp;` only for safe formatting.

Example node lines:
```
CURMOD["<b>Current Module Until<br/>Previous Session</b><br/><i>Foundations of Data</i><br/>Lab · Python · Git<br/>NumPy · Pandas"]
CURSES["<b>Current Session</b><br/><b>Data Cleaning</b><br/><i>Shift:</i> Fix messy tables first"]
CVAL["<b>Course Value</b><br/>Trustworthy tables<br/>for the full stack"]
```

Now use the curriculum details below and create the Mermaid diagram.

Curriculum Details:
[Paste CSV content or module-wise session list here]

Current Session Name:
[Paste current session name here]