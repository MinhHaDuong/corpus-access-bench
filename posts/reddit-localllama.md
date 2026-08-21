# Reddit post — r/LocalLLaMA

**Title:** Qwen 3.8 27B gains +20/60 from corpus access. Claude Opus 5 and Fable 5 gain nothing. And a plain one-file-per-entry directory beat both my hand-built index and grep-over-PDFs.

**Flair:** Resources (or Discussion — check current sub rules before posting)

---

I build research tooling for a living and wanted a number for something I kept
seeing asserted: how much does giving a model access to a specialist corpus
actually buy, and does the answer depend on the model?

Setup: 60 doctoral-level questions in one humanities field. Five arms per model,
same questions, same prompts word for word except the resources block:

- **C** — cold, no tools at all
- **D** — web search/fetch only
- **B** — the corpus as PDFs + full text extracts, grep allowed
- **A** — a hand-built index of the corpus (196 entries, cross-references), then its pages
- **B′** — the corpus split into 196 files, one per entry, filename = entry title

Graded blind, out of 60, by 3 judges from a different model family, against an
answer key built from a *second*, independent reference work.

## Results (mean of 3 judges, /60)

| Access | Claude Sonnet 5 | Claude Opus 5 | Claude Fable 5 | **Qwen 3.8 27B local** |
|---|---|---|---|---|
| C cold | 45.3 | 56.0 | **58.5** | 24.7 |
| D web | 45.5 | 57.4 | 56.8 | 30.0 |
| B PDFs+grep | **49.8** | 56.6 | **58.5** | 37.6 |
| A index | 49.4 | **57.9** | 57.1 | 39.8 |
| B′ file/entry | 42.6 | **57.9** | **58.5** | **44.9** |
| **spread** | 4.5 | 1.9 | 1.7 | **20.3** |

The instrument resolves ~2 points (same copy re-graded across three rounds:
56.0 / 57.8 / 55.3). So the frontier spreads are zero and the 20.3 is real.
Fable is dead flat — 58.5 cold, 58.5 on PDFs, 58.5 on the directory.

**Retrieval is a small-model lever.** On the two strongest models it bought
nothing measurable while costing 2–4× the tokens and time of a cold draw.

## The bit that's actionable for local setups

**B′ (one file per entry) beat A (hand-built index) by +4.1 and B (PDFs+grep) by
+6.1** on the two discriminating strata. I had spent real effort building that
index, with page addresses and 1613 cross-references. A directory listing beat
it.

Two reasons I think it wins:

1. The filename *is* the retrieval index, and it's in the model's context for
free the moment it runs `ls`. No embedding, no chunking policy, no top-k.
2. **Absence becomes a fact.** "Is there an entry on X?" gets an exact yes/no.
Grep can only fail to find something, which isn't the same claim. All four
absences the local model asserted were correct, verified against the directory.

If you're building local RAG over a bounded corpus, the cheap win may be
upstream of your retriever: cut the source at its natural unit and name the
files well.

## Hardware / conditions

- **Local:** Qwen 3.8 27B **Q4_K_M**, llama.cpp, n_ctx 131k, systemd unit.
  **RTX A4000 16GB + RTX 3060 12GB** (28GB VRAM total), Threadripper PRO
  3945WX 12-core, 125GB RAM. **~31 tok/s** sustained (30.4 measured end-to-end
  on the tool-free arm).
- **Frontier:** Claude Code on a Max sub, **reasoning effort `high`** for both
  arms and judges.

Wall clock, 60 questions: local corpus arms **6 100–7 200 s**, frontier corpus
arms 850–1 250 s. Cold, it nearly closes: 859 s local vs 379–652 s frontier.
**These two time columns are not a hardware comparison** — the frontier numbers
include queueing and agent-harness overhead on machines I can't see. What they
honestly measure is what you wait for. Twenty points for two hours of a machine
you already own is the trade.

## Method, since LLM-as-judge deserves suspicion

After the real copies came in, I wrote a **salted copy** in the same register
carrying **6 defects sealed before I drafted it** (false-but-plausible date,
inverted attribution, non-existent reference, invented page number, reversed
thesis, forged quotation) and dropped it into the blinded pile. Pre-registered
rule: **if the panel misses them, the panel's verdicts get thrown out and the
judges get replaced — not the conclusion.** Every panel passed (union ≥5/6).

One thing that did *not* work: the invented **page number** was never caught in
any round, because judges were forbidden to open the corpus. Don't seal a defect
your graders structurally cannot check.

Predictions were frozen before each run and **two were falsified**, including
"the index will win". Both are written up as failures.

## Caveats I'd want if I were reading this

- **One draw per arm.** No confidence interval. Order-of-magnitude result only.
- **Effort isn't held constant, and that one's on me.** I first wrote that the
  local model had no effort knob. It does: the template takes
  `reasoning_effort` of `none` / `low` / `medium` (raises on `high`),
  `chat_template_kwargs: {"enable_thinking": false}` kills thinking outright,
  and llama-server has `--reasoning-effort` / `--reasoning-budget`. I set none
  of them, so the local arms ran at template default against frontier arms at
  `high`. Some blocks then burned the whole 24k on reasoning with no output and
  I patched it with a `/no_think` retry — the crude version of a flag that was
  sitting right there. `--reasoning-budget` would have capped it properly.
  Some of the cold-arm deficit is an inference-budget artefact. Note the local
  ceiling is `medium`, so the labels can never match; a redo should equalise a
  **token budget** instead.
- **Q4_K_M**, not a full-precision run.
- The local model's B′ advantage is likely **understated** — on 2 of 6 blocks it
  reported consulting no file and answered from memory.
- One domain, one language (French), one rubric — and the rubric pays 0.50 for
  an honest "I don't know" vs 0.00 for a confident wrong answer. Flip that and
  the ranking moves.

## What I concluded for my own setup

**I'm not replacing Claude Opus 5 with local Qwen 3.8 27B + a knowledge base for
daily work.** Fully equipped the 27B is at 44.9; Opus 5 *with no tools at all* is
at 56.0. The corpus closes about half the gap and leaves 11 points.

But "too slow" deserves a sharper verdict: **the slowness is in the tool loop,
not inference.** Cold it's 859 s vs 432 s — 2×, totally usable. With the corpus
wired: 6 100–7 200 s vs 905–1 250 s. That's tool round-trips on 2 consumer GPUs,
which indicts my hardware and my agent loop, not the model. It'll age well.

**I'm not going to optimise corpus access for the frontier models** — but not
because they're proven to know everything. Because nothing measurable justifies
2–4× tokens and time on every run. Same decision either way.

**What I genuinely can't tell you:** whether Opus 5 / Fable 5 actually know as
much as the reference work. 58/60 with 1.9-point spreads fits both "they know
it" and "my questions are too easy", and my own falsified prediction leans
toward the second (I predicted ≤10/20 cold on the obscure stratum; got 14.7).
A saturated benchmark proves its own ceiling, not the model's knowledge. Needs
harder questions than I knew how to write — if anyone wants to write them, the
design is public.

**One thing I'll keep the corpus wired for anyway: provenance.** The score
measures whether an answer is right; it says nothing about whether you can check
it. Corpus-armed copies gave exact page refs the judges verified, and flagged
unprompted which answers came from an opened page vs. memory. For actual
research work that's most of the value, and it never shows up in the mark.

## Repo — the README is the write-up

Protocol, harness (runner, blinding, aggregation), full cost tables, and **20 of
the 60 questions published in full** — statements, answer key, every arm's
answers, every judge's per-question line, so you can audit the grading.

The other 40 stay sealed: arm C measures what the model knows *without* the
corpus, and that number dies the day the questions land in a training set.
Hashes of the sealed files are in the repo so campaigns stay verifiable.

github.com/MinhHaDuong/corpus-access-bench

Happy to answer questions on the protocol or run additional local models if
people want a specific one added — that's cheap now that the harness exists.
