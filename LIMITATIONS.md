# Limitations

Written to be read before the results are cited, not after they are disputed.

## The design cannot produce a confidence interval

One draw per arm per model. Sixty questions and three judges reduce variance;
they do not replicate. Nothing here supports a significance claim, and the word
does not appear in RESULTS.md. What the study establishes is an order of
magnitude: twenty points against two.

The practical rule, derived from the anchor copy in RESULTS.md § 0 rather than
assumed: **differences below about 2 points are not differences.** Applied
honestly, this dissolves most of the within-model rankings. It leaves the
between-model gradient standing, because that gap is ten times the floor.

## Effort is a confound, it is not small, and it was avoidable

The frontier arms and judges ran at reasoning effort *high*. The local arms ran
at whatever their chat template does by default.

An earlier version of this file said the local model had no equivalent control.
That was wrong, and checking took ten minutes. The template accepts a
`reasoning_effort` of `none`, `low` or `medium` — measured on a trivial prompt:
2, 22 and 29 completion tokens — and `chat_template_kwargs:
{"enable_thinking": false}` drops a 92-token answer to 6 with no reasoning at
all. `llama-server` exposes `--reasoning`, `--reasoning-effort` and
`--reasoning-budget` besides. The campaign set none of them: the service unit
carries no reasoning flag, and the runners send `messages`, `max_tokens` and
`cache_prompt` and nothing else.

Two things follow. Arm C spent roughly 18 k of 26 k generated tokens on
reasoning, and some blocks consumed the entire 24 k ceiling thinking without
emitting an answer — repaired by putting `/no_think` in the prompt, the crude
form of a control the server offered properly, so a minority of 27B blocks ran
in a different mode from the rest. `--reasoning-budget` would have capped those
blocks by construction.

Some unknown share of the 27B's deficit is therefore an inference-budget
artefact rather than a capability gap.

Note what a redo can and cannot fix. It cannot equalise the effort *label*: the
local ceiling is `medium` and the frontier arms ran at `high`, so no setting
makes those two the same word. It can hold a **token budget** constant across
candidates, which is the better-posed comparison in any case — and which this
campaign, having left the control untouched, did not attempt.

## The 27B's advantage is probably understated

For two of six blocks the 27B's directory arm reported consulting no entry at
all and answered from memory. The measured gain rests on the four blocks where
the tool actually served. The effect is a lower bound.

## One salted register across a wide capability range

The salted copy is written in the register of a strong copy and carries six
sealed defects. In the 27B round it outscored every genuine 27B copy (54.3
against 44.9). That validates the panel's *detection* — the point of the device
— but the salted copy does not double as a quality floor, and no reader should
take it as one.

In the same round the invented-folio defect went undetected by all three judges,
because judges are forbidden to open the corpus. That is a fault in the seal
design, not in the panel.

## Rounds are not comparable without the anchor

Three grading rounds gave the same cold-frontier copy 56.0, 57.8, 55.3 — a
spread of 2.4 points on an identical text. Judges mark more severely inside a
weak field. Comparisons across rounds are read through the anchor or not at all;
the Sonnet and Opus B′ figures come from a different round than their A, B, C, D
figures, which is why RESULTS.md flags them and computes the Sonnet spread
within one round.

## Contamination is unmeasured, not absent

Arm C measures parametric memory. If a candidate's training data contains this
corpus or material derived from it, arm C is inflated and the measured benefit
of access shrinks. We cannot inspect any candidate's training data. The control
stratum was chosen precisely as material assumed present in every training
corpus; the discriminating strata were chosen as material assumed thin there,
and one frozen prediction about that — cold ≤ 10/20 on periphery — was falsified
at 14.7, which suggests the assumption was optimistic.

## Web arms are not comparable to each other

Two campaigns exhausted their web-search budget mid-run and fell back to fetching
pages named from memory. Coverage and cost for those arms are not comparable to
a full search, and are flagged in the campaign cost files. Arm D is the weakest
column of the study.

## One domain, one language, one exam

History of economic thought, in French, 150 words per answer, graded by a rubric
that rewards lucid abstention over confident error. That rubric is a value
judgement about research work, and a different one would reorder the arms —
notably any rubric that rewarded coverage over caution, which would punish the
directory arm's honest silences.

Nothing here has been shown to transfer to another domain, another language,
another answer length, or another model at another effort setting.

## The instrument is not distributed

Forty of the sixty questions are sealed, for the reason in PROTOCOL.md § What is
public and why. A reader can audit the grading on the control stratum and cannot
audit it on the strata that carry the result. This is a real cost of the design
and it is not mitigated by anything in this repository.
