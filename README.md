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
— so the 1.9 and the 1.7 are zero and the 20.3 is the result. A 27B model on a
desk-side machine gains more from corpus access than the entire distance
separating it from a frontier model in the cold row. Fable returns 58.5 cold,
58.5 on the PDFs, and 58.5 on the file directory.

**Second finding: the hand-built index lost to `ls`.** One file per entry,
filename as index, beat a map of 196 entries and 1613 cross-references by 4.1
points and beat text search over the PDFs by 6.1. What pays is not cataloguing a
corpus but cutting it at the right granularity — and a directory answers "is
there an entry on X at all?" exactly and for free, which no search can do. All
four absences the local model asserted were correct.

## Conditions

These are part of the measurement. A frontier model at low effort is a different
subject and nothing here transfers to one.

| | Frontier arms and judges | Local arm |
|---|---|---|
| Model | Claude Sonnet 5, Opus 5, Fable 5 | `qwen3.8-27b`, 27.3 B params, Q4_K_M |
| Reasoning effort | **high** | **left at the template default** — see below |
| Served by | Claude Code, Max subscription | llama.cpp, 131 k context, ≈31 tok/s |
| Hardware | not observable | RTX A4000 16 GB + RTX 3060 12 GB, Threadripper PRO 3945WX |

**Effort was not equalised, and the failure was avoidable.** The local model does
have an effort control — its chat template accepts `reasoning_effort` of `none`,
`low` or `medium`, and `enable_thinking: false` suppresses thinking outright —
but the campaign set none of them: the service unit carries no reasoning flag and
the runners send only `messages`, `max_tokens` and `cache_prompt`. Every local arm
therefore ran at the template's own default, thinking on and bounded only by a
24 000-token ceiling. Its top setting is `medium`; there is no `high` to place
against the frontier arms' `high`. So the comparison is frontier-at-high against
local-at-default, and part of the local model's deficit is an inference-budget
artefact rather than a capability gap. [LIMITATIONS.md](LIMITATIONS.md) states how
far that goes.

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
   for the mark.** A mark measures whether an answer is right, never whether a
   reader can check it. The corpus-armed copies cited exact pages that judges
   verified, and flagged which answers rested on an opened page rather than on
   memory.

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
