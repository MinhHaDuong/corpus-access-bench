# LinkedIn feed post — announces the article

The article is the long form. This is the post that carries it into the feed.
First two lines have to earn the "see more" tap: on mobile that is roughly all a
reader gets for free.

---

## Primary draft

A 27-billion-parameter model running under my desk gained twenty points out of
sixty from access to my reference library.

Claude Opus 5, given the same library, gained nothing.

I spent August measuring this properly. Sixty doctoral questions in the history
of economic thought. Four models, five ways of reaching the answers — closed
book, open web, the PDFs, a hand-built index I was rather proud of, and the same
corpus cut into one file per entry. Every copy graded blind, out of 60, by three
judges from a different model family.

Qwen 3.8 27B, local: +20.3
Claude Sonnet 5: +4.5
Claude Opus 5: +1.9
Claude Fable 5: +1.7

My instrument only resolves about two points, so the bottom two lines are zero.
The stronger the model, the less access to a corpus matters. Retrieval is a
small-model subsidy, and on a frontier model it is dead weight that still costs
two to four times the tokens and the time, every single run.

Then the result I did not see coming.

My hand-built index — 196 entries, 1613 cross-references, real work — lost to a
folder of files. One file per entry, filename as index, beat it by four points
and beat text search over the PDFs by six. What pays is not cataloguing a
corpus. It is cutting it at the right granularity, so the structure is the index
and an absence becomes a fact about `ls`.

I froze my predictions before each run. Two were falsified, including the one
where my index wins. They are written up as falsified, because that is what
pre-registration is for.

Protocol, harness, cost tables and a third of the questions are public —
including every model's answers and every judge's line, so you can audit the
grading rather than take my word for it.

Full write-up in the article below. Code and data:
github.com/MinhHaDuong/corpus-access-bench

#LLM #RAG #LocalLLM #OpenScience

---

## Short variant

If the long one feels heavy for a feed, this keeps the hook and drops the
apparatus.

A 27B model running under my desk gained twenty points out of sixty from reading
my reference library.

Claude Opus 5, given the same library, gained nothing.

Four models, sixty doctoral questions in the history of economic thought, five
ways of reaching the answers, every copy graded blind by three judges from
another model family. The gain from corpus access was 20.3 points for the local
model and 1.9 for Opus 5 — and my instrument only resolves about two points, so
call that zero.

The stronger the model, the less access matters. Retrieval is a small-model
subsidy.

One thing I did not expect: my hand-built index of 196 entries lost to a folder
of files, filename as index. What pays is not cataloguing a corpus but cutting
it at the right granularity.

Predictions frozen before each run; two falsified, and reported as falsified.
Protocol, harness and a third of the questions public.

Article below. Repo: github.com/MinhHaDuong/corpus-access-bench

#LLM #RAG #LocalLLM #OpenScience

---

## Posting notes

- **The tables are already flattened, deliberately.** LinkedIn renders neither
  Markdown pipes nor a monospace font, so a grid cannot hold its columns. The
  article uses dot leaders and a stated reading order instead — a form that
  survives a proportional face, because each line carries its own label. Do not
  re-pipe them on the way in. The feed post sidesteps the question by listing
  only the four gains.
- **A comment beats a second link.** LinkedIn suppresses reach on posts with
  outbound links. Common workaround: put the repo URL in the first comment and
  leave the post itself linking only to the article.
- **First comment is also where the caveats fit** — one draw per arm, Q4_K_M, no
  effort control on the local model. Anyone who would object already knows to
  ask, and answering before they do reads as confidence.
