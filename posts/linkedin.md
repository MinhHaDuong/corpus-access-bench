# LinkedIn article — ready to paste

**Title:** Qwen 3.8 27B gained twenty points from my reference library. Claude Opus 5 gained nothing.

---

I spent August running an exam.

Sixty questions in the history of economic thought, doctoral level. Four
language models sat it, each five times over, under five different ways of
reaching the same body of scholarship: cold with no tools at all; the open web;
the corpus as PDFs with text search; a hand-built index of the corpus, 196
entries with cross-references, that I had spent real effort constructing; and
the corpus cut into 196 files, one per entry, filename = entry title.

Every copy was graded blind, out of 60, by three judges from a different model
family, working from an answer key built from a second reference work so that no
arm could be scored for fidelity to its own source.

Here is what came back.

| Access | Claude Sonnet 5 | Claude Opus 5 | Claude Fable 5 | Qwen 3.8 27B, local |
|---|---|---|---|---|
| Cold, no tools | 45.3 | 56.0 | **58.5** | 24.7 |
| Web only | 45.5 | 57.4 | 56.8 | 30.0 |
| PDFs + text search | **49.8** | 56.6 | **58.5** | 37.6 |
| Hand-built index | 49.4 | **57.9** | 57.1 | 39.8 |
| One file per entry | 42.6 | **57.9** | **58.5** | **44.9** |
| **Best minus worst** | **4.5** | **1.9** | **1.7** | **20.3** |

A 27-billion-parameter model running on a machine under my desk gains twenty
points from corpus access. That is more than the whole distance separating it
from a frontier model in the cold column. The frontier models gain nothing I can
measure: Fable returns 58.5 cold, 58.5 on the PDFs, and 58.5 on the file
directory. Three access layers, one mark.

The instrument resolves about two points, which I know because the same copy
carried through three grading rounds scored 56.0, 57.8 and 55.3. So read the
1.9 and the 1.7 as zero, and read the 20.3 as the finding.

**Conditions, because they are part of the result.** The frontier models ran
through Claude Code on a Max subscription at reasoning effort *high*. The local
model was Qwen 3.8 27B at Q4_K_M under llama.cpp, 131k context, sustaining about
31 tokens/s across an RTX A4000 and an RTX 3060 — 28 GB of VRAM between two
consumer-grade cards, on a Threadripper workstation. A frontier model at low
effort is a different subject and none of this transfers to one.

**What this means if you are deciding where to spend engineering effort.**
Corpus plumbing is a small-model lever. On a frontier model it is close to dead
weight, and not free weight: tooled access cost two to four times a cold draw in
tokens and in time, every run.

For the local machine the price is hours. The corpus arms took 6 100 to 7 200
seconds against 850 to 1 250 for the frontier arms — five to eight times longer
for the same sixty questions. Two hours of a workstation already paid for,
against a subscription. That is the trade, stated plainly. (The two time columns
are not a hardware comparison: the frontier seconds include queueing and harness
overhead on machines I cannot see. What they honestly measure is what a user
waits.)

**The result I did not expect.** The hand-built index lost. It lost to a
directory of files. Cutting the corpus into one file per entry, so the filename
is the index, beat my carefully constructed map by 4.1 points for the local
model and beat text search over the PDFs by 6.1. It also answers a question no
search can: *is there an entry on this figure at all?* A directory says yes or
no exactly, for free. Search can only fail to find something, which is not the
same statement.

What pays is not cataloguing a corpus. It is cutting it at the right
granularity, so the structure is the index and an absence is a fact about `ls`.

**On method, because grading prose is where evaluations go soft.** After the
real copies came in I wrote a fifth copy in the same register carrying six
defects sealed in a file before I drafted it: a plausible false date, an
inverted attribution, a reference that does not exist, an invented page, a
reversed thesis, a forged quotation. It went into the blinded pile with the
others. The rule, fixed in advance: if the panel misses them, the panel's
verdicts on the real copies are thrown out and the judges are replaced — not the
conclusion. Every panel passed. An evaluation that cannot fail its own graders
is not measuring them.

Predictions were frozen before each run, and two were falsified. I had predicted
a cold model would score at most 10 out of 20 on the obscure stratum; it scored
14.7. I had predicted the index would win. Both are written up as failures,
because that is what pre-registration is for.

**So what did I actually decide?**

*I am not swapping Claude Opus 5 for a local Qwen 3.8 27B plus a knowledge
base.* Fully equipped, the 27B scores 44.9. Opus 5 with no tools at all scores
56.0. The corpus closes about half that gap and leaves eleven points.

The slowness deserves a more precise verdict than "too slow", because the
precise one is less damning: it lives in the tool loop, not in inference. Cold,
the local model took 859 s against 432 s — a factor of two, perfectly usable.
Wire the corpus in and it is 6 100–7 200 s against 905–1 250 s. What is slow is
a tool round-trip on two consumer GPUs. That indicts my workstation and my
harness, not the model class, and it will age.

*I am not going to optimise corpus access for the strong models.* Not because
they are proven to know everything — see below — but because nothing measurable
justifies spending two to four times the tokens and the time on every single
run. That decision is the same whichever explanation is true, which is what
makes it a decision rather than a guess.

**And here is what I cannot tell you**, though I would like to. Whether Opus 5
and Fable 5 genuinely know as much as a scholarly reference work. Marks near
58/60 with 1.9-point spreads fit "they know it" and "my questions are too easy"
equally well, and my own evidence leans toward the second: I had predicted a
cold model would score at most 10/20 on the obscure stratum, and it scored 14.7.
An instrument that saturates does not prove the examinee knows the material. It
proves the instrument has a ceiling. Finding out needs harder questions than
I knew how to write.

One consequence of that uncertainty is practical, and it cuts against my own
second decision. **I will keep the corpus wired for the strong models anyway —
for provenance rather than for the score.** A mark says whether an answer is
right. It says nothing about whether a reader can check it. The corpus-armed
copies gave exact page references that the judges verified, and flagged
unprompted which of their answers rested on a page they had opened rather than
on memory. A model that knows the material but cannot route you to the page
leaves the whole verification to you, and in scholarly work that is most of the
work.

**What I am not claiming.** One draw per arm, so no confidence interval — an
order-of-magnitude result, twenty points against two, not a ranking. The local
model has no effort control and burned part of its budget on runaway reasoning,
so some of its cold deficit is an inference-budget artefact rather than a
capability gap. One domain, one language, one rubric — and that rubric rewards
honest abstention over confident error, a value judgement about research work
that would reorder the arms if reversed.

The protocol, the harness, the cost tables and twenty of the sixty questions —
with every model's answers and every judge's line — are public. The other forty
stay sealed, because the thing being measured is what a model knows *without*
the corpus, and that quantity dies the day the questions enter a training set.

👉 github.com/MinhHaDuong/corpus-access-bench

Next: if granularity is the lever, how far does it go? Structured re-extraction
with headings and links, resolved identifiers, generated indexes and access
instructions inside the corpus directory. There should be points left on the
table for the small models.

*Minh Ha-Duong, CNRS — CIRED.*
