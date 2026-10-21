# Multimodal AI Pipelines

## 1. What You'll Learn in This Section

In this lesson, you'll learn to:

- Chain speech-to-text, summarization/extraction and text-to-speech stages into one pipeline.
- Understand why an error in an early stage (a misheard word) quietly corrupts every stage after it.
- Put a quality gate between stages, and route doubtful inputs to a human instead of guessing.
- Apply the same thinking to images: check that an image is usable before any model reads it.

## 2. Detailed Explanation

### From one modality to several

Until now the module worked with text. Real inputs arrive as audio (a recorded voice note), images (a
photographed receipt) and text, and real outputs are sometimes spoken. A **multimodal pipeline** is a
chain of stages, each converting one form of data into another.

The core analogy is a relay race. Each runner hands a baton to the next; one dropped baton ends the
race no matter how fast the others are. The skill here is not the individual stages — each is a library
call — but what happens **between** them.

```text
VOICE NOTE (audio)
   -> SPEECH-TO-TEXT      audio  -> transcript
   -> CLEAN / EXTRACT     text   -> structured fields (city, order, intent)
   -> DECIDE / ROUTE      fields -> action or human review
   -> TEXT-TO-SPEECH      text   -> spoken reply (audio)
```

This lesson uses a small dataset: three recorded customer voice notes (`voice_note_1..3.wav`), one
silent clip, their reference transcripts, and three images (a receipt, a too-dark copy, and a blank page).
The voice notes were synthesised from known sentences, so we can measure transcription errors exactly.

### Stage 1 — Speech-to-text

```python
from transformers import pipeline
asr = pipeline("automatic-speech-recognition", model="openai/whisper-tiny.en")
print(asr("voice_note_1.wav")["text"])
```

`whisper-tiny.en` is a small open-source model: fast, free and local, but it makes mistakes.

```text
SPOKEN:       "Delivery in Gurugram was late by forty minutes."
TRANSCRIBED:  " delivery and guregram was late by 40 minutes."
```

Two errors: "in" became "and", and **"Gurugram" became "guregram"**. We can measure this with **word error
rate (WER)**: the number of word edits (substitutions, insertions, deletions) divided by the number of
reference words. Lower is better; 0 is perfect.

**Watch out for:** a transcript is a *guess*, not a fact. Whisper returns text without a trustworthy
confidence score, so we must verify it ourselves.

### The quiet danger — errors compound

```text
"guregram" is not a known city
   -> city extraction finds nothing
   -> the ticket has no city
   -> it cannot be routed to the Gurugram team
```

No stage crashed. Every stage did its job. The failure only shows up at the end, far from its cause.
That is why multimodal pipelines need **checks between stages**.

### Quality gate 1 — is the transcript usable at all?

Feed Whisper silence and it does not return an empty string. It returns a long run of dots.

```python
def transcript_usable(text, min_words=3):
    letters = sum(c.isalpha() for c in text)
    if letters < 0.5 * max(len(text.strip()), 1):   # mostly punctuation = degenerate output
        return False, "mostly non-letter characters"
    if len(text.split()) < min_words:
        return False, "too few words"
    return True, "ok"
```

A gate like this turns a silent clip into "cannot process — ask for a re-record" instead of a ticket full
of dots.

### Repairing known domain terms

We know the legal values for `city`: Gurugram, Mumbai, Delhi, Noida, Chennai. Fuzzy matching can repair
near-misses:

```python
import difflib
CITIES = ["gurugram", "mumbai", "delhi", "noida", "chennai"]
difflib.get_close_matches("guregram", CITIES, n=1, cutoff=0.75)   # ['gurugram']
```

The **cutoff matters**. Too low and ordinary words get "corrected" into cities (a harmful silent edit);
too high and real errors slip through. Record every correction so a human can audit it.

### Stage 2 — extract fields and decide

```python
def extract_fields(text):
    t = text.lower()
    city = next((c for c in CITIES if c in t), None)
    order = re.search(r"order\s*#?\s*(\d{3,6})", t)
    intent = ("refund" if "refund" in t else "replacement" if "replacement" in t
              else "address_change" if "address" in t else "unknown")
    return {"city": city, "order_id": order.group(1) if order else None, "intent": intent}
```

Routing rule: a **refund** touches money, so it is a *gated* action (recall the Safety session) — the
pipeline drafts it and a person approves. Missing city or unknown intent also goes to human review.

### Stage 3 — Text-to-speech, and checking it

```bash
say -v Samantha -o reply.aiff "Thanks, we have logged your request."
```

Never assume the audio says what you meant. A **round-trip check** transcribes the generated audio and
compares it to the intended text; a large WER means the spoken reply is not trustworthy.

### Images: check usability before any model reads them

A vision model fed a black or blank image will still produce *something*. Cheap checks catch this first:

```python
from PIL import Image
import numpy as np
arr = np.asarray(Image.open("receipt.png").convert("L"), dtype=float)
brightness, contrast = arr.mean(), arr.std()
```

```text
mean brightness very low  -> too dark
standard deviation tiny   -> blank or washed out (no content to read)
```

A real receipt shows a healthy brightness and clear contrast; the dark copy and the blank page fail the
gate. Only images that pass should go on to a vision model or OCR step.

### Orchestration — one function, explicit statuses

```python
def process_voice_note(path):
    raw = transcribe(path)
    ok, why = transcript_usable(raw)
    if not ok:
        return {"status": "rejected", "reason": why}
    fixed, corrections = repair_cities(raw)
    fields = extract_fields(fixed)
    if fields["city"] is None or fields["intent"] == "unknown":
        return {"status": "human_review", "fields": fields, "corrections": corrections}
    ...
```

Every outcome is an explicit status — `processed`, `needs_approval`, `human_review`, `rejected` — never a
silent default.

### The mental model to carry in

```text
RAW INPUT (audio / image)
      |
      v
STAGE -> CHECK -> STAGE -> CHECK -> STAGE       a gate after every stage
      |
      v
REPAIR WHAT YOU SAFELY CAN                      fuzzy match against known values, log it
      |
      v
ROUTE WHAT YOU CANNOT                           to a human, with the reason
      |
      v
VERIFY THE OUTPUT TOO                           round-trip the spoken reply
```

## 3. Key Takeaways

- A multimodal pipeline is a chain of stages; the difficulty lies in the handoffs between them.
- Transcripts and model outputs are guesses. Measure them (WER) and gate them (e.g. silence became dots).
- Errors compound silently: a misheard city name produced no crash, just an unroutable ticket.
- Repair only what you can verify against known values, with a sensible cutoff, and log each correction.
- Check images for brightness and contrast before a vision model sees them.
- Give every outcome an explicit status and send doubtful cases to a human with the reason.

**Mental model:** Think of the pipeline as a relay race — the baton passes (the checks between stages)
decide whether the team finishes, not how fast each runner is.
