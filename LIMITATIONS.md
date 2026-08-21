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

## Effort: what the local control is, and what it is not

The frontier arms and judges ran at reasoning effort *high*. The local arms
passed no reasoning parameter, which renders a prompt byte-identical to
`reasoning_effort: xhigh` — **the template's maximum**. They were not
handicapped. They were instructed to "think carefully through the task, validate
key assumptions, consider plausible alternatives", and arm C spent roughly 18 k
of its 26 k generated tokens doing so before scoring 24.7.

Two earlier versions of this file were wrong about this, in opposite directions:
the first said no control existed, the second said the model ran at some
unspecified default. Both were settled in minutes by rendering the template.

**The control is three prompt strings, not a budget.** `xhigh` encourages, `low`
discourages, and `medium` injects nothing at all — the scale is
encourage / silence / discourage, with no midpoint that means anything. Nothing
enforces any level. The only mechanisms that bound anything sit outside the
template: `enable_thinking: false`, where llama.cpp pre-closes the `<think>`
block so the model structurally cannot think, and `--reasoning-budget N`, which
injects the end-of-thinking tag after N tokens. There is no `high`; the top
level is named `xhigh`, which is why a request for `high` raises.

**What is still wrong with the campaign.** Some blocks exhausted the entire
24 000-token ceiling in reasoning and emitted no answer. The repair put
`/no_think` in the prompt, which places those blocks at the *bottom* of the
scale while every other block sat at the top. A minority of the 27B's answers
were therefore produced with thinking disabled and the rest with thinking
maximally encouraged. That is a real inconsistency in the local column, and
`--reasoning-budget` is the control that would have removed it.

**What a redo can and cannot equalise.** Not the effort *label*: the two scales
share no level name, so no setting makes "high" and "xhigh" the same condition.
A **token budget** held constant across candidates is the better-posed
comparison, and this campaign did not attempt it.

## The saturated blocks, and what re-running them cost

Three of the local model's thirty blocks exhausted the 24 000-token ceiling in
reasoning and emitted nothing; they were re-run with thinking disabled. Ten
questions of sixty in arm B, ten in arm B′.

Measured per block (RESULTS.md § 4bis), the repaired blocks were not depressed —
B′'s is the best block of its arm, B's matches the rest of its arm exactly — and
the headline comparison holds at +11.92/40 when the affected block is dropped,
against a pre-registered threshold of +2. What the repair did cost is narrower:
on five questions arm B answered from memory with no source consulted, and on
those five it performs like the cold arm. That subtracts from arm B rather than
adding to it.

The residual objection this cannot answer: block assignment was not random, so
"the blocks that saturated" is not a random sample of questions, and a
ten-question block on one draw is a noisy unit. The exclusion test is the
defence, not the per-block comparison.

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

## No semantic retrieval was tested

Every access layer here is lexical, and in every one of them the candidate model
chooses what it reads: `grep` over text extracts plus `pdftotext` on a named page
(arm B), the same with a hand-built map (arm A), a directory listing and a file
opened by name (arm B′). No embedding index was built, no vector store was
queried, and at no point did a chunk-and-rank retriever select a passage on the
candidate's behalf.

**So "retrieval", in the write-ups, means agentic lexical access.** Where
`posts/` calls retrieval a small-model lever, the claim covers the layers
measured here and stops there. Embedding RAG, which is what most readers mean by
the word, is untested in either direction: nothing in these results argues that
it would behave like `grep`, and nothing argues that it would not.

**One structural difference deserves naming, as a conjecture and not a result.**
A top-k retriever returns k passages for every query, including queries about
material the corpus does not cover. The directory arm's four correct claims that
no entry existed (RESULTS.md § 2) have no obvious analogue in that regime, and
that behaviour is what decision 4 rests on. Whether a semantic layer recovers it,
loses it, or replaces it with false claims of absence is the kind of question
this study was built to settle and did not.

The cost tables inherit the same scope. Two to four times a cold draw prices an
agentic tool loop paid per query; an embedding index is paid once at build time
and amortised over the run. Neither figure transfers to the other.

A packaged RAG system — paperqa and its kind — sits a further step away, because
such a system supplies its own model for evidence summarisation and answer
drafting. Measuring one would characterise the product, not the access layer, and
its column would not be comparable with those here, where the candidate is the
only model that reads the corpus.

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
