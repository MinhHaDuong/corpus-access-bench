# corpus-access-bench

Open-book versus closed-book performance of language models, measured across a
capability range. Sixty doctoral questions in the history of economic thought,
four models, five ways of reaching the same corpus, every copy graded blind by
three judges from another model family, against decision rules frozen before each
run.

**Finding: the stronger the model, the less corpus access matters.**

| Access | Claude Sonnet 5 | Claude Opus 5 | Claude Fable 5 | Qwen 3.8 27B, local |
|---|---|---|---|---|
| Cold — no tools at all | 45.3 | 56.0 | **58.5** | 24.7 |
| Open web only | 45.5 | 57.4 | 56.8 | 30.0 |
| PDFs + text search | **49.8** | 56.6 | **58.5** | 37.6 |
| Hand-built index of the corpus | 49.4 | **57.9** | 57.1 | 39.8 |
| One file per entry | 42.6 | **57.9** | **58.5** | **44.9** |
| **Best − worst** | **4.5** | **1.9** | **1.7** | **20.3** |

Marks out of 60, each the mean of three judges. **The instrument resolves about
2 points** — the same copy re-graded across three rounds scored 56.0, 57.8, 55.3
— so read any gap under 2 as a tie. Three results survive that rule.

### 1. The stronger the model, the less corpus access matters

Best minus worst access: 20.3 for the local 27B, 4.5, 1.9, 1.7 for the others.
Fable returns 58.5 cold, 58.5 on the PDFs and 58.5 on the file directory. Read
the 1.9 and the 1.7 as zero; the 20.3 is ten times the floor. Corpus plumbing is
a small-model lever, and it costs two to four times a cold draw in tokens and
time whether or not it buys anything.

### 2. The local 27B is not ready to replace Claude Opus 5 for this task

Fully equipped it scores 44.9. Opus 5 **with no tools at all** scores 56.0. The
corpus closes about half the gap and leaves eleven points, five times the floor,
and it costs 6 100–7 200 s against 905–1 250 s for the same sixty questions.
Corpus access does not turn a 27B into a frontier model on this task; it turns it
into a usefully better 27B.

### 3. The hand-built index never paid — and the directory is the only layer that moved anything

The index was the original hypothesis. Against plain PDFs with `grep`, within
each round:

| A (index) − B (PDFs + grep) | Sonnet 5 | Opus 5 | Fable 5 | Qwen 27B |
|---|---|---|---|---|
| | −0.3 | +1.3 | −1.4 | +2.2 |

Four models, four results at or barely over the floor. Real construction work —
196 entries, folios, 1613 cross-references — bought no marks anywhere. The
pre-registered rule that would have triggered mapping a second reference work
measured **+0.08**, and that work was cancelled.

The file-per-entry directory is a different matter, and **not simply better**:

| B′ (one file per entry) − B (PDFs + grep) | Sonnet 5 | Opus 5 | Fable 5 | Qwen 27B |
|---|---|---|---|---|
| | **−9.0** | +0.1 | 0.0 | **+7.3** |

It is the only access layer in the study that produced a large effect, and its
sign flips by model. For the 27B it is the best access there is, beating the
index by 5.2 and the PDFs by 7.3, and its four claims of "no entry exists on X"
were all correct — a question a directory answers exactly and free, and search
cannot pose. For Sonnet it cost nine points.

An earlier version of this page said the index "lost to `ls`". That
overgeneralises from one column: the directory beat the index measurably for the
27B alone. What holds across all four models is the weaker and more useful
claim — cataloguing a corpus bought nothing, while cutting it at the right
granularity changed a great deal, in whichever direction the model's own memory
dictated. [RESULTS.md § 3](RESULTS.md) takes the sign flip apart.

## Conditions

These are part of the measurement. A frontier model at low effort is a different
subject and nothing here transfers to one.

| | Frontier arms and judges | Local arm |
|---|---|---|
| Model | Claude Sonnet 5, Opus 5, Fable 5 | `qwen3.8-27b`, 27.3 B params, Q4_K_M |
| Reasoning effort | **high** | **`xhigh`** — the template maximum, and its default |
| Served by | Claude Code, Max subscription | llama.cpp, 131 k context, ≈31 tok/s |
| Hardware | not observable | RTX A4000 16 GB + RTX 3060 12 GB, Threadripper PRO 3945WX |

**Effort, and what the local control actually is.** The campaign passed no
reasoning parameter to the local model — and that turns out to mean it ran at
**`xhigh`, the template's maximum**, whose rendered prompt is byte-identical to
passing `xhigh` explicitly. The local arms were not handicapped; they were told,
in the system message, to "think carefully through the task, validate key
assumptions, consider plausible alternatives".

The control is three prompt strings, not a budget. `xhigh` encourages, `low`
discourages, and `medium` injects *nothing at all* — so the scale is
encourage / silence / discourage, with no measurable midpoint. Nothing enforces
any of it, which is why some blocks spent their entire 24 000-token ceiling
thinking without emitting an answer. The only hard controls sit outside the
template: `enable_thinking: false` (llama.cpp pre-closes the `<think>` block, so
the model cannot think) and `--reasoning-budget N`. There is no `high` because
the top level is named `xhigh`.

What remains a genuine inconsistency: three blocks exhausted the 24 000-token
ceiling reasoning and emitted nothing, and were re-run with thinking disabled —
the bottom of the scale, while every other block sat at the top. Twenty
questions of the local model's three hundred. Measured per block, those repairs
cost nothing: the repaired block is the *best* block of arm B′, and arm B's
matches the rest of its arm. The one real scar is five questions where arm B
answered from memory with no source consulted, and there it performs like the
cold arm — which subtracts from the corpus arms rather than flattering them.
Dropping the affected block from the decisive comparison leaves **+11.9/40**
against a pre-registered threshold of +2. Worked through in
[RESULTS.md § 4bis](RESULTS.md).

Costs ran two to four times a cold draw in tokens and in wall-clock time, on
every arm and every model — 6 100–7 200 s locally against 850–1 250 s for the
hosted models. Full cost tables: [RESULTS.md § 4](RESULTS.md), which also
explains why those two time columns are not a hardware comparison.

## How to read this repository

| Start here | To answer |
|---|---|
| [RESULTS.md](RESULTS.md) | Every table — marks, strata, costs, jury calibration, falsified predictions. § 0 derives the resolution floor before any number is quoted. |
| [PROTOCOL.md](PROTOCOL.md) | What was frozen, when, and the journal of amendments across four campaigns. |
| [LIMITATIONS.md](LIMITATIONS.md) | What this does not establish. Written to be the least flattering document here. |
| [`public/`](public/) | The control stratum in full: 20 statements, the answer key, every arm's answers, every judge's per-question line. Audit the grading rather than take our word for it. |
| [`harness/`](harness/) | The code. Parameterised; no path hard-coded. |
| [`campaigns/`](campaigns/) | One directory per campaign, immutable once run, each with its preregistration. |
| [`posts/`](posts/) | The same material written as an article, for readers who arrive from a feed. |

## What is sealed, and why

`instrument/` holds `MANIFEST.sha256` and nothing else. The forty discriminating
questions, the answer key, the blinding keys and the seal files are not in this
tree and never will be.

The reason is narrow. The cold arm measures what a model knows *without* the
corpus — and that quantity dies the day the questions enter a training set.
Publishing the instrument would buy one round of auditability at the cost of
every round after it. The manifest records the digest of each sealed file, so a
campaign can prove which version it sat without exposing it; seal files are
burned after use and their hashes outlive them.

The published control stratum is the compensation, and it is a real one: twenty
questions, pre-registered as non-discriminating, with the full grading trail.
The cost is equally real and unmitigated — nobody can audit the forty questions
that carry the result. [PROTOCOL.md](PROTOCOL.md) § What is public and why argues
the trade.

**The corpus is not here either.** It is a standard multi-volume reference work
in the history of economic thought; this study makes no claim about the form in
which a researcher holds it, and redistributes none of it. Published files pass
through a naming policy (`harness/redactions.json`) enforced by
`tests/test_naming_policy.py` — itself checked against a case known to leak,
because a guard whose all-clear is indistinguishable from "I could not look" is
not a guard.

## Replaying it

The sealed instrument is not distributed, so a full replication needs sixty
questions of your own. Everything else is here: arm prompts word for word, the
grading rubric, a runner for a local llama.cpp model, blinding, aggregation, and
the cost accounting.

```bash
python harness/runner_local_arms.py --arm B --questions <sheet> --out <dir>
python harness/blind.py --answers <dir> --salted <copy> --out <blind> --key <key>
# … judges grade the blinded pile …
python harness/aggregate.py --notes <notes> --key <key> --strata <map> \
                            --salted-questions 7 17 27 34 35 53
```

Three parts of the design travel better than the finding, and are the reason the
harness is public:

- **A salted copy.** A further copy in the same register carries six defects
  sealed before it is drafted, and goes into the blinded pile. If the panel
  misses them, the panel's verdicts are discarded and the judges replaced — not
  the conclusion. An evaluation that cannot fail its own graders is not
  measuring them.
- **Frozen predictions with a written decision threshold**, committed before the
  draw. Two were falsified, including the one where the index wins, and are
  reported as falsified.
- **A control stratum**, pre-registered as carrying no decision, published whole.

## What the author concluded

Stated as decisions, since that is what the campaigns were run to settle. The
reasoning is in [RESULTS.md § 7](RESULTS.md).

1. **A local 27B plus a knowledge base does not replace Claude Opus 5 for daily
   research work.** Fully equipped the 27B scores 44.9; Opus 5 with no tools
   scores 56.0. The slowness is in the tool loop rather than in inference — cold,
   859 s against 432 s — so that verdict indicts a workstation and a harness, and
   will age.
2. **Corpus access will not be optimised for the frontier models.** Not because
   they are proven to know the material, but because nothing measurable justifies
   the spend. The decision is the same under either reading.
3. **Whether the strong models really know as much as a scholarly reference work
   is unsettled here**, and the instrument argues against its own optimism: the
   frozen prediction that a cold model would score ≤ 10/20 on the obscure stratum
   failed at 14.7. A saturated instrument demonstrates its own ceiling, not the
   examinee's knowledge. Settling this needs harder questions.
4. **The corpus stays wired for the strong models anyway — for provenance, not
   for the mark.** This one rests on a working practice rather than on a number,
   so it needs stating plainly.

   A researcher keeps a fulltext copy of every work they cite. Not a
   bibliographic entry, not a DOI, not a search result: the document itself, on
   disk, openable. The rule exists because a bibliographic database is reliable
   for whether a reference *exists* and unreliable for what it *says* — this
   study met both failures while building its own answer key, where a fraction
   quoted in a well-known paper came back wrong from two independent OCRs, and a
   review circulates under the wrong journal title. A page number is read on the
   page it prints on, never interpolated from a text extraction.

   That practice is what an agent inherits, or does not. An agent working inside
   a corpus held as fulltext can cite *sur pièce* — from the piece — and its
   citation is checkable by whoever reads next. An agent that merely knows the
   material can only recall it, and every locator it produces has to be
   re-verified by hand before the work can be published. In scholarly writing
   that verification is most of the labour, so the choice is not between a good
   answer and a slightly better one. It is between a citation and a claim.

   The measured behaviours are the evidence that the wiring delivers it: the
   corpus-armed copies gave exact folios the judges opened and checked, flagged
   unprompted which of their answers rested on a page they had opened rather
   than on memory, and — for the directory arm — established four times that no
   entry existed at all, which is a statement no search can make.

   None of that appears in a mark. It is why decision 2 is about optimisation
   effort and not about disconnecting the corpus.

## Status

Four campaigns, August 2026: a 20-question pilot, the 60-question main study on
two models, a round adding the file-directory access layer, and a round adding a
frontier model and a local 27B.

Next: if granularity is the lever, how far does it go? Structured re-extraction
with headings and links, resolved identifiers, generated indexes and access
instructions inside the corpus directory.

## Licence

Text and data CC BY 4.0; code under `harness/` and `tests/` MIT. The corpus
studied is neither included nor redistributed, and nothing here grants rights
over it.

Minh Ha-Duong, CNRS — CIRED.
