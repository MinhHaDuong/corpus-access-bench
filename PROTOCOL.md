# Protocol

Frozen before each campaign's first draw, then amended only by adding a dated
entry to the journal at the end of this file. The French originals as committed
are preserved verbatim under `campaigns/*/PREREGISTRATION-fr.md` and
`harness/prompts/`; this document is the English account of them.

## The question

Does access to a specialist corpus raise the quality of a model's answers in a
scholarly domain, by how much, at what cost — and does the answer depend on the
model?

## The corpus

A standard multi-volume reference work in the history of economic thought, 196
signed entries with cross-references, the kind of source a specialist would
consult first. It is not distributed here and this study makes no claim about
the form in which it is held. What matters for the measurement is its structure:
196 entries, each on a bounded range of pages, cross-referring to one another.

A second reference work of the same kind, independent of the first, built the
answer key. That separation is load-bearing: an answer key drawn from the corpus
the arms are reading would score fidelity to a source rather than correctness,
and every arm without that source would be penalised for a difference of
edition.

## The five access layers

Each arm is a fresh agent, one draw, given the same answer sheet and prompts
identical word for word except for the resources block. The verbatim prompts are
in `harness/prompts/arms-fr-verbatim.md`.

| Arm | Resources |
|---|---|
| **A** | a hand-built index of the corpus (196 entries, folios, 1613 cross-references), then the pages it routes to. No web. |
| **B** | the volumes as PDF plus complete text extracts; `grep` permitted. No web, no index. |
| **B′** | the corpus split into 196 files, one per entry, filename = entry title. Nothing else. |
| **C** | reads the answer sheet, then uses no tool of any kind. |
| **D** | web search and fetch only; no local file but the sheet. |

Prohibitions are declared before the run and verified after it by grepping each
arm's own tool-call log (`harness/contamination.py`) — never by asking the model
what it used. The arms' self-reported `TOOL CALLS:` line undercounts, which is
why the harness counter is what the cost tables record. Ceiling: 200 tool calls.

## The exam

60 questions, doctoral level, three strata of 20, interleaved on the served
sheet as C1, P1, A1, C2, … and **unlabelled**: the stratum map lives in a file
the arms cannot reach.

- **Canon (C)** — control. Standard doctoral material; a cold model should do
  well, and if it does not, the apparatus is broken rather than the model
  ignorant. Pre-registered as non-discriminating.
- **Periphery (P)** — minor figures, untranslated texts, local quarrels: well
  covered in reference works, thin in textbooks and in training data.
- **Adjacency (A)** — filiations, fronts, intermediaries: where things sit with
  respect to one another. The stratum where a cross-reference apparatus ought to
  pay.

The decision rules are stated on P+A, never on the total: canon is a control and
including it would dilute exactly the signal being tested.

Answers are capped at 150 words, in French, with honest abstention explicitly
invited. Before any draw, an independent validator with web access checked every
factual presupposition in the P and A statements; 37 of 40 passed and 3 were
replaced for excess canonicity. Repeat that validation on any modification.

## Grading

Three judges per round, always a **different model family from the candidates**,
with web access, working blind, on three declared angles: the bare rubric;
fabrication and rhetorical confidence; historiographical substance. The rubric
(`harness/prompts/rubric-fr-verbatim.md`) scores 0 to 1 in steps of 0.25.

Two features of the rubric do the real work. A lucid abstention is worth 0.50,
and 0.75 if it says *why* — while a confident wrong answer is worth 0.00. The
gap is deliberate: on a research question a confidently asserted false lead
costs more than a blank. And the judges are told that blinding is partial —
copies differ visibly in what they can cite — and instructed to grade the copy,
not the method: a precise folio is not a guarantee but a claim to verify, and an
uncited true statement is not a fault.

The judges' own verifications override the answer key. One judge corrected the
key on Otto Bauer; that is the intended behaviour, not an incident.

## Jury calibration: the salted copy

After the real copies arrive, a fifth copy is written in the same register
carrying **six defects sealed in a file before it is drafted**: a plausible false
date, an inverted attribution, a non-existent reference, an invented entry or
folio, a reversed thesis, a forged quotation, spread across the three strata. It
is blinded into the pile with the others.

**The panel is valid if the union of its detections reaches 5 of 6 and the median
judge reaches 3 of 6.** Below that, the panel's verdicts on the real copies are
declared uninformative and the round is graded again by other judges. The
conclusion does not change; the jury does.

Defects are burned after use. Each round seals new ones.

One design lesson, paid for in the fourth campaign: **do not seal a folio defect
in a round where the judges are forbidden to open the corpus.** An invented
folio is then structurally undetectable, and it was the single defect no judge
ever caught.

## Blinding and aggregation

`harness/blind.py` cuts the provenance trailer, orders the copies by the SHA-256
of their own blinded text, and writes a key that stays away from the judges.
Completeness is asserted on the *blinded* file, not on the source — in the
fourth campaign a repaired block had been appended after the trailer, was
silently cut, and a judge noticed before the harness did.

`harness/aggregate.py` produces per-arm totals, the decomposition by stratum,
the panel's marks on the seeded questions, and inter-judge agreement.

## What is public and why

The **control stratum is published in full** — the 20 statements, the answer key
entries, every arm's 20 answers, every judge's per-question line — under
`public/`. It is standard doctoral material, already in every training corpus by
construction, and pre-registered as carrying no decision. Publishing it costs
the instrument nothing and lets a reader audit the grading end to end.

The **40 discriminating questions stay sealed**, with their answer key, keys and
seal files, recorded in `instrument/MANIFEST.sha256` by hash alone. The reason
is narrow and, we think, decisive: arm C measures what a model knows *without*
the corpus. If the questions enter a training corpus, arm C rises for reasons
that have nothing to do with the corpus, and the quantity the study is built to
measure is destroyed. Publishing the instrument would make the fifth campaign
uninterpretable while adding, to the fourth, only what the control stratum
already shows.

This is the dev/test split of any benchmark meant to survive its own
publication. The cost is real and stated: a reader cannot check the questions
that carry the result. Anyone who wants that check can write 60 of their own —
the design is here, and the instrument is the cheapest part of it.

## Amendment journal

| Date | Amendment | Where |
|---|---|---|
| 2026-08 | v1 pilot, 20 canonical questions only. Falsified by its own control: the same cold model scored 2.5/20 on an apparatus questionnaire and 16.92/20 on the canonical one — fourteen points carried by the choice of questions. Stratification introduced in response. | `campaigns/2026-07-v1-pilot/` |
| 2026-08-20 | v2 frozen: 60 questions, three strata, four arms, two models, salted copy, decision rule at A ≥ B + 2 on P+A. | `campaigns/2026-08-v2-sonnet-opus/PREREGISTRATION-fr.md` |
| 2026-08-20 | Arm B′ (file-per-entry directory) added and pre-registered, with the B copy re-graded in the same round so the comparison stays within a round. | `campaigns/2026-08-eval3-md-directory/` |
| 2026-08-21 | Frontier and local-27B columns pre-registered, with an anchor copy carried across rounds to measure grading drift. Prediction: Δ(B′ − C) ≥ +2 on P+A for the 27B. | `campaigns/2026-08-eval4-fable-qwen/` |
| 2026-08-21 | Naming policy adopted: published files describe the reference works by role and never name them. Applied by `harness/redactions.json`, enforced by `tests/test_naming_policy.py`. | this repository |
| 2026-08-21 | **Correction, not an amendment.** The claim that the local model had no reasoning-effort control was checked against the running server and found false: the template accepts `none`/`low`/`medium`, `enable_thinking: false` suppresses thinking, and `llama-server` exposes `--reasoning-effort` and `--reasoning-budget`. Campaign 4 set none of them. The measurements stand; their description was wrong and is corrected in README, RESULTS § 0 and LIMITATIONS. Campaign 5 must declare and set the local effort control. | this repository |
