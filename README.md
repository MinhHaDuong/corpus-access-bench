# Qwen 3.8 27B gained twenty points from my reference library. Claude Opus 5 gained nothing.

I ran an exam in August.

It compared the open-book vs. closed-book performance of AI models.

Sixty questions in the history of economic thought, doctoral level. Four language
models took the exam five times each, under five different ways of reaching
knowledge: **cold** with no tools at all (a closed-book exam, a parametric test,
since the models have only their parameters); access to the **open web**; access
to the corpus as **PDFs with text search**; access to a **corpus map**, a
hand-built index of 196 entries with cross-references; and access to the **corpus
cut into 196 files**, one per entry, filename = entry title.

Every copy was graded blind, out of 60, by three judges from a different model
family, working from an answer key built from a second reference work so that no
arm could be scored for fidelity to its own source. Here is what came back.

| Access | Claude Sonnet 5 | Claude Opus 5 | Claude Fable 5 | Qwen 3.8 27B, local |
|---|---|---|---|---|
| Cold, no tools | 45.3 | 56.0 | **58.5** | 24.7 |
| Open web only | 45.5 | 57.4 | 56.8 | 30.0 |
| PDFs + text search | **49.8** | 56.6 | **58.5** | 37.6 |
| Hand-built index | 49.4 | **57.9** | 57.1 | 39.8 |
| One file per entry | 42.6 | **57.9** | **58.5** | **44.9** |
| **Best minus worst** | **4.5** | **1.9** | **1.7** | **20.3** |

The instrument resolves about two points, which I know because the same copy
carried through three grading rounds scored 56.0, 57.8 and 55.3. So read the 1.9
and the 1.7 as zero, and read the 20.3 as the finding:

A 27-billion-parameter model running on a machine under my desk gains twenty
points from corpus access. That is more than the whole distance separating it
from a frontier model in the cold column. The frontier models gain nothing I can
measure: Fable returns 58.5 cold, 58.5 on the PDFs, and 58.5 on the file
directory. Three access layers, one mark.

## Experimental conditions

An economist can be a scientist too.

The frontier models ran through Claude Code on a Max subscription at reasoning
effort *high*. The local model was Qwen 3.8 27B at Q4_K_M under llama.cpp, 131k
context, sustaining about 31 tokens/s across an RTX A4000 and an RTX 3060 —
28 GB of VRAM between two consumer-grade cards, on a Threadripper workstation. A
frontier model at low effort is a different animal.

Grading included a salted sixth copy, injected with known errors to test the
judges themselves. They were reliable. The 60 questions were organized in three
difficulty strata, from graduate school level to obscure questions in the spirit
of Humanity's Last Exam.

## What this means if you are deciding where to spend engineering effort

Corpus plumbing is a small-model lever. On a frontier model it is dead weight:
tooled access cost two to four times a cold draw in tokens and in time, every
run.

| Access | Claude Sonnet 5 | Claude Opus 5 | Claude Fable 5 | Qwen 3.8 27B, local |
|---|---|---|---|---|
| Cold, no tools | 79k / 379 s | 74k / 432 s | 74k / 652 s | 26k / 859 s |
| Open web only | 140k / 509 s | 127k / 1 143 s | 84k / 888 s | 62k / 2 361 s |
| PDFs + text search | 158k / 701 s | 241k / 1 246 s | 122k / 854 s | 166k / 6 472 s |
| Hand-built index | 253k / 985 s | 247k / 905 s | 227k / 981 s | 145k / 7 207 s |
| One file per entry | 309k / 911 s | 540k / 944 s | 277k / 1 094 s | 139k / 6 109 s |

Tokens generated / wall-clock seconds, for the same sixty questions. The two time
columns are not the same quantity: the local seconds are inference on hardware I
can see, the frontier seconds include queueing and agent-harness overhead on
machines I cannot. What they honestly measure is what I waited for.

For the local machine the price is hours. The corpus arms took 6 100 to 7 200
seconds against 850 to 1 250 for the frontier arms — five to eight times longer
for the same sixty questions. Two hours of a workstation already paid for (I have
spare electricity in the afternoon from my rooftop PV panels), against a
subscription. That is the trade, stated plainly.

## The result I did not expect

The hand-built index lost to a directory of files. Cutting the corpus into one
file per entry, so the filename is the index, beat my carefully constructed table
of contents by 4.1 points for the local model, and beat text search over the PDFs
by 6.1.

What pays is not cataloguing a corpus. It is cutting it at the right granularity,
so the structure is the index and an absence is a fact about `ls`.

That last clause deserves its own sentence. A directory answers "is there an
entry on this figure at all?" exactly, and for free. Search can only fail to find
something, which is not the same claim. All four absences the local model
asserted were correct.

## So what did I actually decide?

**I am not swapping Claude Opus 5 for a local Qwen 3.8 27B plus a knowledge base
yet.** Fully equipped, the 27B scores 44.9. Opus 5 with no tools at all scores
56.0. The corpus closes about half that gap and leaves eleven points. Plus, my
workstation is too slow.

The slowness deserves a more precise verdict. The issue lives in the tool loop,
not in inference. Cold, the local model took 859 s against 432 s — a factor of
two, hopefully less once I plug in that RTX 5060. But wire the corpus in, and the
local answer time is 6 100–7 200 s against 905–1 250 s for the datacenter-hosted
models. The tool round-trip on two old GPUs is slow. That indicts my workstation
and my harness, not the model class, and it will age.

**I am not going to optimise corpus access for the strong models.** Not because
they are proven to know everything — see below — but because nothing measurable
justifies spending two to four times the tokens and the time on every single run.

**And here is what I cannot tell you, though I would like to.** Whether Opus 5
and Fable 5 genuinely know as much as a scholarly reference work. Marks near
58/60 with 1.9-point spreads fit "they know it" and "my questions are too easy"
equally well, and my own evidence leans toward the second: I had predicted a cold
model would score at most 10/20 on the obscure stratum, and it scored 14.7. An
instrument that saturates does not prove the examinee knows the material. It
proves the instrument has a ceiling. Finding out needs harder questions.

**I will keep the corpus wired for the strong models anyway — for provenance
citations rather than for the score.** Scientific writing needs exact
bibliographies. The corpus-armed copies gave exact page references that the
judges verified, and flagged which of their answers rested on a page they had
opened rather than on memory. A model that knows the material but cannot cite to
the page leaves the whole verification to me, and in scholarly work that is most
of the work.

## What I am not claiming

One draw per arm, so no confidence interval — an order-of-magnitude result,
twenty points against two, not a ranking. The local model has no effort control
and burned part of its budget on runaway reasoning, so some of its cold deficit
is an inference-budget artefact rather than a capability gap. One domain, one
language, one rubric — and that rubric rewards honest abstention over confident
error, a value judgement about research work that would reorder the arms if
reversed.

The long version is [LIMITATIONS.md](LIMITATIONS.md), written to be the least
flattering document here.

## How the grading was kept honest

Three commitments, all fixed before any run. They are the part of this most
likely to be useful to someone measuring something else.

**A salted copy.** After the real copies came in, I wrote a further copy in the
same register carrying six defects sealed in a file before I drafted it: a
plausible false date, an inverted attribution, a reference that does not exist,
an invented page, a reversed thesis, a forged quotation. It went into the blinded
pile with the others. The rule, fixed in advance: if the panel misses them, the
panel's verdicts on the real copies are thrown out and the judges are replaced —
not the conclusion. Every panel passed. An evaluation that cannot fail its own
graders is not measuring them.

One thing that did not work: the invented page number was never caught, in any
round, because judges were forbidden to open the corpus. Do not seal a defect
your graders structurally cannot check.

**Frozen predictions.** Each campaign committed its predictions, and the
threshold that would change my behaviour, before the draw. Two were falsified,
including the one where my index wins. They are written up as falsified, because
that is what pre-registration is for.

**A control stratum, published in full.** Twenty of the sixty questions are
standard doctoral material, pre-registered as non-discriminating. Those twenty
are in this repository — statements, answer key, every arm's answers, every
judge's per-question line and justification. Audit the grading yourself rather
than take my word for it.

## What is in this repository

```
PROTOCOL.md        the frozen protocol, and the journal of its amendments
RESULTS.md         every table: quality, strata, costs, jury calibration
LIMITATIONS.md     what this does not establish, at some length
harness/           the code, parameterised — no path is hard-coded
  prompts/         the arm and judge prompts, verbatim, in the language served
  redactions.json  the naming policy, applied mechanically
campaigns/         one directory per campaign, immutable once run
public/            the control stratum, in full
instrument/        MANIFEST.sha256 only — see below
posts/             short write-ups, for which this page is the source
tests/             including a guard checked against a known positive
```

**`instrument/` holds a manifest and nothing else.** The forty discriminating
questions, the answer key, the blinding keys and the seal files are not in this
tree and never will be. What is measured is what a model knows *without* the
corpus, and that quantity dies the day the questions enter a training set. The
manifest records the SHA-256 of each sealed file, so a campaign can prove *which*
version of the instrument it sat without exposing it.

**The corpus is not here either.** It is a standard multi-volume reference work
in the history of economic thought; this study makes no claim about the form in
which a researcher holds it, and redistributes none of it. Every published file
passes through a naming policy enforced by `tests/test_naming_policy.py`, which
is itself checked against a case known to leak — a guard whose all-clear is
indistinguishable from "I could not look" is not a guard.

## Replaying it

You need the sealed instrument, which is not distributed. Everything else is
here: the arm prompts word for word, the grading rubric, the runner for a local
llama.cpp model, the blinding and aggregation scripts, and the cost accounting.
Someone who writes their own sixty questions on their own corpus can run this
design end to end.

```bash
python harness/runner_local_arms.py --arm B --questions <sheet> --out <dir>
python harness/blind.py --answers <dir> --salted <copy> --out <blind> --key <key>
# … judges grade the blinded pile …
python harness/aggregate.py --notes <notes> --key <key> --strata <map> \
                            --salted-questions 7 17 27 34 35 53
```

## What is next

If granularity is the lever, how far does it go? Structured re-extraction with
headings and links, resolved identifiers, generated indexes and access
instructions inside the corpus directory. There should be points left on the
table for the small models.

## Licence

Text and data: CC BY 4.0. Code under `harness/` and `tests/`: MIT. The corpus
studied is neither included nor redistributed, and nothing here grants rights
over it.

Minh Ha-Duong, CNRS — CIRED.
