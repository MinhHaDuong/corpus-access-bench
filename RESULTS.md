# Results

Four campaigns, August 2026. Every mark is out of 60 and is the mean of three
independent judges from a model family different from the candidate's.

**Operating conditions — part of the measurement, not a footnote.**

| | Frontier arms and judges | Local arm |
|---|---|---|
| Model | Claude Sonnet 5, Claude Opus 5, Claude Fable 5 | `qwen3.8-27b`, 27.3 B parameters, Q4_K_M (17.8 GB) |
| Reasoning effort | **high**, inherited by sub-agents | no such control exists |
| Server | Claude Code on a Max subscription | llama.cpp, systemd unit, 131 k context served of 262 k trained |
| Hardware | not ours, not observable | RTX A4000 16 GB + RTX 3060 12 GB (28 GB VRAM), Threadripper PRO 3945WX 12-core, 125 GB RAM |
| Generation speed | not measurable through the harness | ≈31 tok/s sustained; 30.4 measured end to end on the tool-free arm |

A frontier model at low effort is a different subject and would not produce these
numbers; nothing here transfers to one. See § 0 for the confound this introduces,
and § 4 for why the wall-clock columns are not a hardware comparison.

## 0. Resolution — read this before the tables

Marks are reported to one decimal. That decimal is arithmetic, not measurement.
Three things bound what this instrument can actually see:

- **One draw per arm per model.** Length (60 questions, 20 per stratum, three
  judges) is the only variance reduction; there is no within-arm replication and
  therefore no confidence interval.
- **Grading drift between rounds.** The anchor copy — one cold frontier copy
  carried through three rounds — scored **56.0, 57.8, 55.3**. The same judges
  mark more severely inside a weak field.
- **Inter-judge spread** of 0.06 to 0.17 mark-units per question, which
  accumulates over 60 questions.

And one confound rather than a bound. **Effort is not held constant across the
comparison, because it cannot be.** The frontier arms think at effort high; the
local model has no such control, and its reasoning budget was set by the runner
rather than chosen — arm C spent roughly 18 k of its 26 k generated tokens on
reasoning. Worse, some blocks exhausted the whole 24 k budget in reasoning
without emitting an answer, and the fix was a retry with thinking suppressed, so
a minority of the 27B blocks ran in a different mode from the rest. Part of the
27B's deficit is therefore an inference-budget artefact and not a capability
difference. This cuts against the headline's precision, not its direction: the
gap it must explain away is twenty points.

Taken together: **a difference under about 2 points is not a difference.** Read
every comparison inside a single round, and read the small ones as ties. This is
why the study's conclusion is stated as a gradient across a capability range —
20 points against 2 — rather than as a ranking of access layers within a model.

## 1. Quality by access layer

| Access | Claude Sonnet 5 | Claude Opus 5 | Claude Fable 5 | Qwen 3.8 27B (c4) |
|---|---|---|---|---|
| C — cold | 45.3 | 56.0 | **58.5** | 24.7 |
| D — web only | 45.5 | 57.4 | 56.8 | 30.0 |
| B — PDF + text extracts | **49.8** | 56.6 | **58.5** | 37.6 |
| A — index → corpus pages | 49.4 | **57.9** | 57.1 | 39.8 |
| B′ — file per entry | 42.6 † | **57.9** † | **58.5** | **44.9** |
| *(salted copy of the round)* | 38.6 | 36.1 | 50.6 | 54.3 |
| *(anchor: cold frontier copy)* | — | 56.0 | 57.8 | 55.3 |
| **spread, best − worst** | **4.5** ‡ | **1.9** | **1.7** | **20.3** |

† Third campaign, where the B copy was re-graded in the same round and scored
51.6 (Sonnet) and 57.8 (Opus). ‡ Computed within the second campaign only.

**The gradient is the result, and only the gradient.** Corpus access moves a
local 27B by twenty points — ten times the resolution of the instrument. It
moves a mid-tier frontier model by four, which is at the edge of what can be
claimed. It moves the two strongest by 1.9 and 1.7 points, which under § 0 is
zero. Fable returns 58.5 cold, 58.5 on the PDFs and 58.5 on the file directory:
three access layers, one mark.

The right reading of the frontier columns is "no effect detectable at this
resolution", not "proven zero". A study designed to find a two-point effect in
Opus would need replication this one does not have. What it can say is that
whatever effect exists there is smaller than the effect in the 27B by an order
of magnitude.

## 2. The 27B, on the strata that carry the decision

Periphery + adjacency, out of 40. Canon is a control and is excluded.

| Qwen 3.8 27B | C cold | D web | B PDF | A index | B′ directory |
|---|---|---|---|---|---|
| P+A / 40 | 15.8 | 18.3 | 23.5 | 25.5 | **29.6** |
| gain over cold | — | +2.5 | +7.7 | +9.7 | **+13.8** |

The frozen prediction was Δ(B′ − C) ≥ +2. Measured: **+13.8**, well clear of
the resolution floor. The ordering inside it is the second finding: the plain
file-per-entry directory beats the hand-built index by 4.1 and the raw PDFs by
6.1. Both gaps clear the floor; the difference between the index and the PDFs
(2.0) sits on it and should be read as a tie.

The second frozen prediction — zero false claims of absence — also holds. All
four entries the 27B declared missing from the corpus are genuinely missing,
verified by `ls`, with a positive control confirming the probe could see a
present entry. A directory answers "is there an entry on X?" for free and
exactly; `grep` over concatenated text cannot.

## 3. What the index bought, and what it did not

The index was the original hypothesis, and it lost. Across every model it either
tied the plain corpus or trailed it, and the pre-registered rule that would have
triggered mapping a second reference work — A ≥ B + 2 on P+A for the mid-tier
model — measured **+0.1**. That work was cancelled.

Two capabilities survive the verdict, neither of them visible in a mark:

- **Provenance.** The index-armed copies cited exact folios, which the judges
  verified, and flagged unprompted which of their answers rested on an opened
  page rather than on memory.
- **Detection of absence.** An index establishes that no entry exists on a
  figure. A grep can only fail to find one. Roughly a third of the periphery
  figures in the questionnaire have no entry — their matter sits in thematic
  chapters, which only grep reaches. The index routes to titles; the content
  under the titles escapes it.

The B′ result then subsumes the second capability at lower cost: a directory
gives exact absence with no extraction work at all.

## 4. Costs

Tokens (candidate side) and wall-clock seconds. Tool calls in
`campaigns/*/costs-raw-fr.md`.

**The two time columns are not the same quantity, and the difference matters.**
The local seconds are inference on known hardware: a 27B at Q4_K_M split across
an RTX A4000 and an RTX 3060, ≈31 tok/s, every second of it accounted for. The
frontier seconds come from Claude Code on a Max subscription — a hosted service
whose latency includes queueing, rate limiting and agent-harness overhead on
machines we cannot see. Nothing here licenses a claim about relative hardware or
model speed. What the column does measure, honestly, is what a practitioner
waits: end-to-end time to get sixty graded-quality answers.

| Access | Claude Sonnet 5 | Claude Opus 5 | Claude Fable 5 | Qwen 3.8 27B (generation) |
|---|---|---|---|---|
| C | 79 k / 379 s | 74 k / 432 s | 74 k / 652 s | 26 k / 859 s |
| D | 140 k / 509 s | 127 k / 1 143 s | 84 k / 888 s | 62 k / 2 361 s |
| B | 158 k / 701 s | 241 k / 1 246 s | 122 k / 854 s | 166 k / 6 472 s |
| A | 253 k / 985 s | 247 k / 905 s | 227 k / 981 s | 145 k / 7 207 s |
| B′ | 309 k / 911 s | 540 k / 944 s | 277 k / 1 094 s | 139 k / 6 109 s |

Tooled corpus access costs two to four times a cold draw, in tokens and in time.
For the frontier models that buys nothing. For the local 27B it buys twenty
points at zero marginal cost in money.

The time it buys them with is the honest price: the local corpus arms ran
6 100 to 7 200 seconds against 850 to 1 250 for the frontier arms — five to
eight times longer for the same sixty questions, on a desk-side machine that
costs nothing per run. Cold, the gap nearly closes (859 s against 379 to 652),
because the local arm then spends its time generating rather than waiting on
tools. Two hours of a machine already paid for, against a subscription: that is
the trade this study prices.

An earlier version of the pilot reported that the index *saved* tokens against
the PDF arm (−24 %, −63 % calls). The second campaign reversed it to +60 % and
+196 %. The cause is instructive: in the pilot the PDF arm opened volumes page
by page (115 calls); by the second campaign it had learned to grep the text
extracts (25 calls). The index's apparent economy was never a property of the
index. It was a property of its opponent's clumsiness — a reason to read *how* a
baseline worked before believing a comparison against it.

## 5. Jury calibration

| Round | Union of detections | Median judge | Verdict | Inter-judge spread |
|---|---|---|---|---|
| v2 Sonnet | 6/6 | — | valid | 0.12 |
| v2 Opus | 6/6 | — | valid | 0.06 |
| Third campaign | 6/6 both sides | 3 and 5 | valid | 0.09 / 0.05 |
| Fourth, frontier round | 6/6 | ≈5 | valid | 0.11 |
| Fourth, 27B round | 5/6 | 4 | valid | 0.17 |

Every panel passed. The single defect never detected, in any round, was the
invented folio in the 27B round — the judges were forbidden to open the corpus
and so had no means of checking one. That is a fault in the seal design for that
round, recorded in PROTOCOL.md so it is not repeated.

**The salted copy outscored every real 27B copy** (54.3 against 44.9 at best).
It is written in the register of a strong copy and carries six defects; a 27B
copy is weaker throughout. The salted copy therefore calibrates *detection*, not
overall quality — a limitation of carrying one salted register across a wide
capability range.

## 6. Predictions falsified

Reporting these is the point of freezing them.

- **"A cold model scores ≤ 10/20 on periphery."** Measured 14.7. The parametric
  memory of a mid-tier model covers minor nineteenth-century figures far better
  than assumed, and the periphery stratum discriminates by only 2.1 points —
  adjacency by 1.2. The strata designed to separate the arms barely do so for
  frontier models, which is itself part of the headline.
- **"The index beats the plain corpus."** −0.3 for Sonnet, +1.3 for Opus, both
  inside the noise floor.
- **"The file directory raises the mark for every model."** It lowered Sonnet's
  by nine points. Investigation of the substrate cleared the corpus — the
  abstentions were true on the page — and located the effect in posture: a clean
  index induces abstention where the corpus is silent, while the PDF arm blended
  corpus and memory. The frontier model was indifferent to the interface.

## 7. Conclusions

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
