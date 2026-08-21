# corpus-access-bench

**What does giving a language model access to a specialist corpus actually buy?**

Four models, five ways of reaching the same body of scholarship, one 60-question
exam in the history of economic thought, graded blind by panels of three judges
against a pre-registered decision rule.

The answer, in one line: **the stronger the model, the less access matters.**

| Access to the corpus | Claude Sonnet 5 | Claude Opus 5 | Claude Fable 5 | Qwen 3.8 27B (local) |
|---|---|---|---|---|
| **C** — cold, no tools at all | 45.3 | 56.0 | **58.5** | 24.7 |
| **D** — open web only | 45.5 | 57.4 | 56.8 | 30.0 |
| **B** — the volumes as PDF + text extracts, `grep` allowed | **49.8** | 56.6 | **58.5** | 37.6 |
| **A** — a hand-built index of the corpus, then its pages | 49.4 | **57.9** | 57.1 | 39.8 |
| **B′** — the corpus split into one file per entry | 42.6 † | **57.9** † | **58.5** | **44.9** |
| *spread, best minus worst* | *4.5* | *1.9* | *1.7* | ***20.3*** |

Marks are out of 60, each the mean of three independent judges. † measured in a
separate grading round; see [RESULTS.md](RESULTS.md) for why rounds are not
directly comparable and how an anchor copy quantifies the drift.

**Conditions.** Frontier arms and judges ran through Claude Code on a Max
subscription at reasoning effort **high**. The local model was **Qwen 3.8 27B,
Q4_K_M, llama.cpp, 131 k context, ≈31 tok/s** on one desk-side machine — an
**RTX A4000 (16 GB) plus an RTX 3060 (12 GB)**, 28 GB of VRAM between them,
Threadripper PRO 3945WX, 125 GB RAM — and has no effort control at all. Effort
is a first-order factor here, so it is declared with every number in this
repository. **One decimal is all the instrument resolves**: a difference under
about 2 points is not a difference, and the anchor copy in RESULTS.md § 0 is
what establishes that floor rather than assuming it.

A local 27-billion-parameter model gains **twenty points** from corpus access —
more than the entire distance between it and a frontier model. The frontier
models gain, within the resolution of this instrument, nothing: Fable scores
58.5 cold, 58.5 on the PDFs, and 58.5 on the file directory.

And a second result that surprised us more:

> **The hand-built index lost to `ls`.** Extracting the corpus into one file per
> entry, filename = entry title, beat the carefully constructed map of the field
> — by 4.1 points for the local model — and beat the raw PDFs by 6.1. What
> pays is not cataloguing a corpus. It is cutting it at the right granularity,
> so that the filename *is* the index and an absence is a fact about `ls`.

---

## Why this might be worth your time

Most retrieval evaluations answer "does retrieval help?" with a single model and
report yes. Running the same exam across a capability range turns that into a
more useful question — *for whom* does it help — and the answer has a shape:
the benefit is concentrated almost entirely at the low end, and it is large
there. If you are choosing where to spend engineering effort, that is the
finding: corpus plumbing is a lever for small local models and close to a dead
weight for frontier ones.

The methodology may be the more transferable part. Grading free-form scholarly
prose is where evaluations usually go soft, so the protocol is built around
three commitments, all pre-registered before any run:

- **A salted copy.** After the real copies come in, a fifth copy is written in
  the same register carrying six defects sealed in advance — a plausible false
  date, an inverted attribution, a non-existent reference, a fabricated folio, a
  reversed thesis, a forged quotation. It goes into the blinded pile with the
  others. **If the panel does not find them, the panel's verdicts on the real
  copies are discarded and the judges are replaced, not the conclusion.** An
  evaluation that cannot fail its own graders is not measuring them.
- **Frozen predictions and a written decision rule.** Each campaign commits its
  predictions and the threshold that would change our behaviour, before the
  draw. Two predictions were falsified, and are reported as falsified.
- **A control stratum, published in full.** 20 of the 60 questions are standard
  doctoral material, pre-registered as non-discriminating. Those 20 are in this
  repository — statements, answer key, every arm's answers, every judge's
  per-question line and justification. Audit the grading yourself.

---

## Conclusions

Two of these are equipment decisions for one researcher's daily work. The third
is what the study can and cannot settle. The fourth is the part that transfers.

**1. A local Qwen 3.8 27B with a knowledge base does not replace Claude Opus 5
for daily research work.** Fully equipped, the 27B scores 44.9; Opus 5 with no
tools at all scores 56.0. The corpus closes about half the gap and leaves eleven
points, six times the resolution floor.

The slowness is worth stating precisely, because the precise version is less
damning. It lives in the tool loop, not in inference: cold, the local model took
859 s against 432 s, a factor of two. With the corpus wired, 6 100–7 200 s
against 905–1 250 s. What is slow is a tool round-trip on two consumer cards, so
this verdict is dated rather than permanent — it indicts a harness and a
workstation, not a model class.

**2. Corpus access will not be optimised for the frontier models** — and the
reason is not that they are proven to know the material. It is that nothing
measurable justifies the spend, which is two to four times the tokens and the
time on every run. That decision holds under either reading of the flat frontier
columns, which is what makes it a decision rather than a guess. What would
reopen it: an exam the frontier models do not saturate.

**3. What this exam cannot settle: whether the strong models really know as much
as a scholarly reference work.** Marks near 58/60 with 1.9-point spreads are
equally consistent with "they know it" and with "these questions are too easy to
reveal what they do not know". The instrument argues for the second reading
against our own expectation: the frozen prediction that a cold model would score
at most 10/20 on the obscure stratum failed at 14.7, and Opus 5's four arms fit
inside 1.9 points on 60. A saturated instrument does not demonstrate the
examinee's knowledge; it demonstrates its own ceiling. Settling this needs harder
questions, which campaign 4 did not know how to write.

**4. Keep the corpus wired for the strong models anyway — for provenance, not
for the mark.** A mark measures whether an answer is right. It does not measure
whether a reader can check it. The corpus-armed copies cited exact folios that
the judges verified, and flagged unprompted which of their answers rested on an
opened page rather than on memory. A model that knows the material but cannot
route you to the page leaves the whole verification to you.

**And the one result that is not about anyone's equipment:** the shape of a
corpus beats the catalogue of a corpus. A directory of one file per entry beat a
hand-built index of the same material by 4.1 points, and answers a question no
search can pose — whether an entry exists at all.

---

## What is in this repository

```
README.md          this file
PROTOCOL.md        the frozen protocol, and the journal of its amendments
RESULTS.md         every table: quality, strata, costs, jury calibration
LIMITATIONS.md     what this does not establish, at some length
harness/           the code, parameterised — no path is hard-coded
  prompts/         the arm and judge prompts, verbatim, in the language served
  redactions.json  the naming policy, applied mechanically
campaigns/         one directory per campaign, immutable once run
public/            the control stratum, in full
instrument/        MANIFEST.sha256 only — see below
tests/             including a guard checked against a known positive
```

**`instrument/` holds a manifest and nothing else.** The 40 discriminating
questions, the answer key, the blinding keys and the seal files are not in this
tree and never will be. The manifest records the SHA-256 of each, so any
campaign can prove *which* version of the instrument it sat without exposing it.
The reasoning is in [PROTOCOL.md](PROTOCOL.md) § What is public and why.

**The corpus is not here either.** It is a standard multi-volume reference work
in the history of economic thought; this study makes no claim about the form in
which a researcher holds it, and redistributes none of it. Every published file
passes through a naming policy enforced by `tests/test_naming_policy.py`, which
is itself checked against a case known to leak — a guard whose all-clear is
indistinguishable from "I could not look" is not a guard.

## Replaying it

You need the sealed instrument, which is not distributed. What *is* here is
everything else: the arm prompts word for word, the grading rubric, the runner
for a local llama.cpp model, the blinding and aggregation scripts, and the cost
accounting. Someone who writes their own 60 questions on their own corpus can
run this design end to end.

```bash
python harness/runner_local_arms.py --arm B-prime --questions <sheet> --out <dir>
python harness/blind.py --answers <dir> --salted <copy> --out <blind> --key <key>
# … judges grade the blinded pile …
python harness/aggregate.py --notes <notes> --key <key> --strata <map> \
                            --salted-questions 7 17 27 34 35 53
```

## Status

Four campaigns, August 2026: a 20-question pilot, the 60-question main study on
two models, a round adding the file-directory access layer, and a round adding a
frontier model and a local 27B. Costs are recorded per arm in tokens, tool calls
and wall-clock seconds. The two time columns measure different things — local
inference on known hardware against a hosted service with queueing — and
RESULTS.md § 4 says so before comparing them.

The next campaign is the interesting one. The file-directory result says
granularity is what pays — so the question becomes how far that goes: structured
re-extraction with headings and links, resolved identifiers, generated indexes
and access instructions inside the corpus directory. If the shape of the corpus
is the lever, it should be possible to move the small models further.

## Licence

Text and data: CC BY 4.0. Code under `harness/`: MIT. Both are defaults chosen
so the repository is usable rather than after long deliberation; open an issue if
either is wrong for your purpose.

Minh Ha-Duong, CNRS (CIRED).
