# Lecture Script: Tableau + GenAI — Insight Writing with GenAI
> **Instructor Reference** — Module 3: Tableau Dashboards + Storytelling | Academic Session 25 | Duration: 2 Hours | Instructor: Balaji

---

## Session Overview
**Goal:** Students can prompt a GenAI tool with their own confirmed dashboard reading to draft a genuine insight (not a description), refine that draft for clarity and audience-appropriate tone, and pair it with the right chart into a complete data story.

**Student profile at this point:** They can now build clean, decision-focused dashboards and read unfamiliar ones for genuine insight. They've used GenAI conversationally in Module 1, but never specifically to draft business insight writing from their own dashboard reading. Expect the risk of over-trusting fluent-sounding GenAI output without checking it against their own verified reading — this is the central danger to correct today.

**Key outcome:** Students should leave able to explain, unprompted, why a smooth-reading GenAI insight can still be wrong, and how to guard against that.

> 🎯 **The one sentence this session must land:** *GenAI is excellent at turning your correct reading into clear prose fast — it is not a substitute for having read the dashboard correctly yourself first.*

---

## Timing Breakdown

| Segment | Duration | Cumulative |
|---|---|---|
| Opening Hook | 8 min | 8 min |
| Concept + Practical Block 1: GenAI as a Drafting Partner | 18 min | 26 min |
| Concept + Practical Block 2: Prompting for Insight, Not Description | 22 min | 48 min |
| **BREAK** | 10 min | 58 min |
| Concept + Practical Block 3: Refining for Clarity and Tone | 25 min | 83 min |
| Concept + Practical Block 4: Structuring a Complete Data Story | 27 min | 110 min |
| Summary & Bridge | 5 min | 115 min |
| Q&A & Doubt Solving | 5 min | 120 min |

---

## Opening — "The Confident, Wrong Paragraph" (8 min)

> "I asked GenAI to write an insight from a chart, but I only gave it the raw numbers, no context. Here's what it wrote."

Read aloud a smooth, confident-sounding but subtly wrong GenAI-drafted paragraph (e.g., claiming a revenue dip was caused by a specific campaign change that, in the real scenario, hadn't actually happened yet at that point in time).

> "Notice — that paragraph reads beautifully. Clear sentences, confident tone, sounds exactly like something you'd send a founder. It's also wrong, because I gave it incomplete information and it filled the gap with a guess dressed up as fact."

**Pivot line:** "Today's whole session is about using GenAI as a genuinely powerful drafting partner, without falling for writing that just *sounds* right."

**Context for the sessions ahead:** "This closes the loop on all of Module 3 — every chart, every dashboard, every reading skill you've built ends here, in a real message someone can act on. It also carries straight into Module 4, where GenAI becomes part of your everyday analytics workflow."

---

## Concept Block 1: GenAI as a Drafting Partner, Not a Replacement (9 min)

> "Using GenAI to write an insight is like asking a skilled assistant to type up your handwritten notes into a clean paragraph. Genuinely useful — but if your notes said the wrong thing, they'll type up a clean, confident version of the wrong thing."

Live demo: feed GenAI a correct, specific observation from last session's Chennai reading ("Chennai revenue -3%, all other cities positive, decline specifically in Groceries") and show the clear, accurate draft that comes back.

> "The quality of what comes out is entirely dependent on the quality and completeness of what I put in."

### 🔴 The trap / highest-value moment
> "The trap from this morning's opening: trusting GenAI output because it reads smoothly. Write this down: **fluent writing and accurate analysis are two different things. GenAI is strong at the first, and only as good as your input at the second.**"

## Practical Block 1: Spot the Confident Guess (9 min)

Give students three GenAI-drafted insight paragraphs, all fluent and confident, but only some grounded in complete, accurate information. Task: identify which ones are trustworthy and which are likely filling gaps with confident-sounding guesses, and explain how they can tell.

**Answer key with reasoning:** Trustworthy drafts cite specific, verifiable numbers and comparisons consistent with the actual dashboard; suspect drafts make causal claims ("caused by") without any comparison or timing evidence provided in the prompt — the tell is unsupported causal language appearing where the prompt never supplied causal evidence.

💬 **Expect a question about "how would I even know if I wasn't there for the original prompt?"** Welcome it. Say: "Good instinct — that's exactly why, in real work, you always check a GenAI insight draft against the actual dashboard yourself before sending it, every single time, no exceptions."

---

## Concept Block 2: Prompting for Insight, Not Description (13 min)

> "A vague prompt produces a vague draft. A specific prompt — one that includes your own actual reading — produces a genuine insight."

Live demo: run the weak prompt "write something about this Chennai chart" and show the generic output; then run the strong prompt including the specific reading (city comparison, category breakdown, direction) and show the dramatically better, specific output.

> "Same GenAI tool. Same chart. Completely different quality of output — because I changed what I gave it, not which tool I used."

### 🔴 The trap / highest-value moment
> "The trap: handing GenAI just the raw chart or numbers and expecting it to independently notice the same pattern you spotted through careful reading last session. Write this down: **always include your own confirmed reading — the trend you checked, the comparison you made — directly in the prompt.**"

## Practical Block 2: Weak Prompt, Strong Prompt (13 min)

Give students a Kirana365 scenario (Bengaluru conversion rate rising from 28% to 31% alongside a banner campaign launch) and ask them to write both a weak prompt and a strong prompt for GenAI, then run both and compare the outputs.

**Answer key with reasoning:** The weak prompt ("summarize this dashboard") typically returns a generic restatement; the strong prompt (including the specific numbers, timeframe, and the explicit instruction to note correlation vs causation) returns a specific, appropriately cautious insight — the comparison itself is the teaching moment, proving prompt quality drives output quality.

💬 **Expect pushback**: "Isn't it more work to write a detailed prompt every time?" Welcome it. Say: "It's more upfront work and far less rework — a vague prompt you have to heavily rewrite afterward usually costs more total time than a specific one written well the first time."

---

## BREAK (10 min)

---

## Concept Block 3: Refining for Clarity and Tone (13 min)

> "A GenAI draft is a starting point, not a finished product. The same true insight needs different tone depending on who's reading it."

Live demo: take the Chennai insight and produce two tone variants — the blunt, headline-first founder version, and the collaborative, non-accusatory Chennai-team version — showing how the underlying facts stay identical while word choice shifts.

> "Same numbers. Same conclusion. Completely different first sentence, because the audience is different."

### 🔴 The trap / highest-value moment
> "The trap: sending the wrong tone to the wrong audience — the blunt founder version to the local team, say. Write this down: **a technically accurate insight can still land badly if the tone doesn't match who's reading it.** Refining tone is still your judgment call, not GenAI's."

## Practical Block 3: Two Tones, One Insight (12 min)

Students take one insight they've already confirmed (from a provided Kirana365 scenario) and produce two GenAI-assisted drafts: one for a founder (headline-first, brief), one for the relevant frontline store team (collaborative, exploratory).

**Answer key with reasoning:** Both drafts should state the same underlying fact and recommendation, but differ meaningfully in opening line, directness, and framing — grading focuses on whether the two versions would genuinely land differently with their intended readers, not just superficial word swaps.

💬 **Expect a question about "how do I know which tone is right without knowing the reader personally?"** Welcome it. Say: "General patterns hold reasonably well — senior leadership usually wants the headline first; frontline teams closer to the issue usually want context and collaboration first. When in doubt, err toward respectful and specific over blunt."

---

## Concept Block 4: Structuring a Complete Data Story (13 min)

> "A complete data story pairs the right chart with the written insight — visual proof and plain-language meaning together, in one place."

Live demo: assemble the full Kirana365 package — the small Chennai-outlier bar chart from Session 23, the refined founder-tone insight text, and a clear one-line next step ("pull Chennai's Groceries pricing and stock data before Friday's ops review").

> "This mirrors the trend-evidence-ask structure from a few sessions ago — now finished with actual words instead of relying on the chart alone."

### 🔴 The trap / highest-value moment
> "The trap: sending a chart with no text, or text with no chart. Write this down: **the strongest data stories always pair visual proof and written meaning — neither one alone does the whole job.**"

## Practical Block 4: Assemble the Full Data Story (14 min)

Students take their refined Chennai insight from Practical Block 3, pair it with an appropriate chart (reused from earlier sessions or newly built), and add one clear next-step line, producing a complete send-ready package.

**Answer key with reasoning:** A complete package includes a specific chart directly supporting the claim, 2-3 sentences of insight text in appropriate tone, and one concrete, actionable next step — missing any of the three pieces should be flagged as incomplete during peer review.

💬 **Expect a question about length — "how long should the written insight be?"** Welcome it. Say: "Short — 2 to 4 sentences for most business audiences. If it's longer than that, it's probably explaining instead of concluding; save the deep detail for someone who explicitly asks for it."

---

## Summary & Bridge (5 min)

| Concept | The one thing to remember |
|---|---|
| GenAI as a drafting partner | Fluent writing doesn't guarantee accurate analysis — check the reading yourself first |
| Prompting for insight | Include your own confirmed reading directly in the prompt |
| Refining tone | Same facts, different audiences need different tone — that judgment stays yours |
| Complete data story | Pair chart and text together — visual proof and written meaning, always both |

Close on the thesis: "GenAI is excellent at turning your correct reading into clear prose fast — it is not a substitute for having read the dashboard correctly yourself first. Today you used it exactly the way it should be used: as a fast, powerful drafting partner for your own good judgment."

**Bridge to the Module 3 Evaluation:** "That's everything — from your very first bar chart through today's complete data story. The Module 3 Evaluation checks all of it. After that, Module 4 begins, and GenAI becomes part of your everyday analytics workflow, alongside your first steps into Python."

---

## Q&A & Doubt Solving (5 min)

**Q: Can I just ask GenAI to "check if my insight is correct" instead of verifying it myself?**
→ Not reliably — GenAI can catch some obvious logical gaps, but it doesn't have independent access to your actual dashboard data, so it can't truly verify your reading; that check still needs to be yours.

**Q: Is it okay to use GenAI to help me choose which chart to pair with an insight?**
→ Yes, as a suggestion — but the final choice should reflect what you learned in Session 19 about matching chart type to the actual question, since GenAI won't have seen your full dashboard context.

**Q: How much should I edit a GenAI draft before sending it?**
→ Enough that it sounds like you and matches your specific reading exactly — treat the first draft as a strong starting point, not a final answer, every time.

**Q: What if GenAI's tone suggestion feels off for my specific audience?**
→ Trust your own read of the audience over GenAI's guess — you know your specific founder, colleague, or team better than any general-purpose tone suggestion can.

**Q: Should every dashboard finding get a full written insight, or just the important ones?**
→ Just the important ones — writing a full insight for every minor fluctuation creates noise; reserve this effort for findings that genuinely warrant someone's attention or action.

---

## Instructor Notes
- **Words not yet earned:** "hallucination mitigation," "retrieval-augmented generation," "prompt chaining" — these are real GenAI concepts but beyond today's practical scope; keep vocabulary to prompting, drafting, refining, and tone.
- **Biggest risk in this session:** Students trusting a fluent GenAI draft without independently verifying it against their own dashboard reading — this is the exact failure mode from the opening hook and should be revisited explicitly during every practical exercise's debrief.
- **Board management:** Keep "fluent writing ≠ accurate analysis" and the weak-prompt/strong-prompt comparison visible for the entire session.
- **Common confusions:**
  1. Assuming a well-written GenAI draft must be factually correct.
  2. Giving GenAI raw numbers with no context and expecting it to independently spot the same pattern a human reader would.
  3. Sending the same tone to every audience regardless of who's actually reading it.
- **Cross-references:** This session closes the loop on the full Module 3 arc — chart choice (Session 19), dashboard assembly (Session 20), decision focus (Session 23), and reading discipline (Session 24) all feed directly into today's writing process; it also directly previews the GenAI-assisted workflows that open Module 4.
- **Local/cultural context notes:** The "skilled assistant typing up handwritten notes" analogy lands well with this cohort; keep the Chennai insight as the throughline example across both tone variants, since a specific, familiar business scenario makes the tone-shifting exercise concrete rather than abstract.
