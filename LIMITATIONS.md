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

## Effort is a confound, and it is not small

The frontier arms and judges ran at reasoning effort *high*. The local model has
no equivalent control; its reasoning budget came from the runner. Arm C spent
roughly 18 k of 26 k generated tokens on reasoning, and on some blocks the model
consumed the entire 24 k budget thinking and emitted nothing — repaired by a
retry with thinking suppressed, so a minority of 27B blocks ran in a different
mode from the rest.

Some unknown share of the 27B's cold-arm deficit is therefore an inference-budget
artefact. A serious follow-up holds the token budget constant across candidates
instead of holding the effort *label* constant.

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
