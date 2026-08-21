# LinkedIn article

**Title:** Qwen 3.8 27B gained twenty points from my reference library. Claude Opus 5 gained nothing.

> The repository page is the canonical text — this is that article, flattened for
> a venue that renders neither Markdown tables nor a monospace font. Edit
> `README.md` first and carry changes here, not the other way round. The tables
> below use dot leaders on purpose: do not re-pipe them on the way in.

---
I ran an exam in August.

It compared the open-book vs. closed-book performance of AI models.

Sixty questions in the history of economic thought, doctoral level. Four language models took the exam five times each, under five different ways of reaching knowledge: A/ Cold with no tools at all (aka a closed books exam, aka a parametric test since models have only their parameters); B/ Access the open web; C/ Access the corpus as PDFs with text search; D/ Access to a corpus map, a hand-built index of 196 entries with cross-references; and E/ Access to the corpus cut into 196 files, one per entry, filename = entry title.

Every copy was graded blind, out of 60, by three judges from a different model family, working from an answer key built from a second reference work so that no arm could be scored for fidelity to its own source. Here is what came back.

Marks out of 60. Reading order in every line: Claude Sonnet 5 · Claude Opus 5 · Claude Fable 5 · Qwen 3.8 27B running locally.

Cold, no tools ......... 45.3 · 56.0 · 58.5 · 24.7
Open web only .......... 45.5 · 57.4 · 56.8 · 30.0
PDFs + text search ..... 49.8 · 56.6 · 58.5 · 37.6
Hand-built index ....... 49.4 · 57.9 · 57.1 · 39.8
One file per entry ..... 42.6 · 57.9 · 58.5 · 44.9

Best minus worst ........ 4.5 ·  1.9 ·  1.7 · 20.3

The instrument resolves about two points, which I know because the same copy carried through three grading rounds scored 56.0, 57.8 and 55.3. So read the 1.9 and the 1.7 as zero, and read the 20.3 as the finding:

A 27-billion-parameter model running on a machine under my desk gains twenty points from corpus access. That is more than the whole distance separating it from a frontier model in the cold column. The frontier models gain nothing I can measure: Fable returns 58.5 cold, 58.5 on the PDFs, and 58.5 on the file directory. Three access layers, one mark.

Experimental conditions (an economist can be a scientist too!) The frontier models ran through Claude Code on a Max subscription at reasoning effort high. The local model was Qwen 3.8 27B at Q4_K_M under llama.cpp, 131k context, sustaining about 31 tokens/s across an RTX A4000 and an RTX 3060 — 28 GB of VRAM between two consumer-grade cards, on a Threadripper workstation. A frontier model at low effort is a different animal.

A word on the local model's reasoning effort, because I got it wrong twice before checking. Passing no parameter is byte-identical to asking for xhigh, the template's maximum: the local arms were instructed to think carefully and validate their assumptions, and arm C spent 18k of its 26k tokens doing so before scoring 24.7. They were not handicapped. The control itself is three prompt strings rather than a budget — xhigh encourages, low discourages, medium says nothing at all — so nothing enforces it, which is why some blocks burned the whole ceiling thinking and emitted no answer. Those I repaired with /no_think, putting a minority of blocks at the bottom of the scale while the rest sat at the top. That inconsistency is the real defect, and llama.cpp's --reasoning-budget would have prevented it.

What this means if you are deciding where to spend engineering effort. Corpus plumbing is a small-model lever. On a frontier model it is dead weight: tooled access cost two to four times a cold draw in tokens and in time, every run (tables follow).

Tokens generated and wall-clock seconds, same reading order.

Cold, no tools ......... 79k/379s · 74k/432s · 74k/652s · 26k/859s
Open web only .......... 140k/509s · 127k/1143s · 84k/888s · 62k/2361s
PDFs + text search ..... 158k/701s · 241k/1246s · 122k/854s · 166k/6472s
Hand-built index ....... 253k/985s · 247k/905s · 227k/981s · 145k/7207s
One file per entry ..... 309k/911s · 540k/944s · 277k/1094s · 139k/6109s

Tokens generated / wall-clock seconds, for the same sixty questions. The two
time columns are not the same quantity: the local seconds are inference on
hardware I can see, the frontier seconds include queueing and agent-harness
overhead on machines I cannot. What they honestly measure is what I waited for. For the local machine the price is hours. The corpus arms took 6 100 to 7 200 seconds against 850 to 1 250 for the frontier arms — five to eight times longer for the same sixty questions. Two hours of a workstation already paid for (I have spare electricity in the afternoon from my rooftop PV panels), against a subscription. That is the trade, stated plainly.

The result I did not expect. The hand-built index lost to a directory of files. Cutting the corpus into one file per entry, so the filename is the index, beat my carefully constructed table of contents by 4.1 points for the local model and beat text search over the PDFs by 6.1. What pays is not cataloguing a corpus. It is cutting it at the right granularity, so the structure is the index and an absence is a fact about ls.

So what did I actually decide?

I am not swapping Claude Opus 5 for a local Qwen 3.8 27B plus a knowledge base yet. Fully equipped, the 27B scores 44.9. Opus 5 with no tools at all scores 56.0. The corpus closes about half that gap and leaves eleven points. Plus, my workstation is too slow.

The slowness deserves a more precise verdict. The issue lives in the tool loop, not in inference. Cold, the local model took 859 s against 432 s — a factor of two, hopefully less once I plug in that RTX 5060. But wire the corpus in, and the local answer time is 6 100–7 200 s against 905–1 250 s for the datacenter hosted models. The tool round-trip on two old GPUs is slow. That indicts my workstation and my harness, not the model class, and it will age.

I am not going to optimise corpus access for the strong models. Not because they are proven to know everything — see below — but because nothing measurable justifies spending two to four times the tokens and the time on every single run.

And here is what I cannot tell you, though I would like to. Whether Opus 5 and Fable 5 genuinely know as much as a scholarly reference work. Marks near 58/60 with 1.9-point spreads fit "they know it" and "my questions are too easy" equally well, and my own evidence leans toward the second: I had predicted a cold model would score at most 10/20 on the obscure stratum, and it scored 14.7. An instrument that saturates does not prove the examinee knows the material. It proves the instrument has a ceiling. Finding out needs harder questions.

I will keep the corpus wired for the strong models anyway — for provenance citations rather than for the score. Scientific writings need exact bibliographies. The corpus-armed copies gave exact page references that the judges verified, and flagged which of their answers rested on a page they had opened rather than on memory. A model that knows the material but cannot cite to the page leaves the whole verification to me, and in scholarly work that is most of the work.

What I am not claiming. One draw per arm, so no confidence interval — an order-of-magnitude result, twenty points against two, not a ranking. The local model ran at its maximum reasoning setting, but a minority of its blocks were repaired with thinking disabled, so its column mixes two regimes. One domain, one language, one rubric — and that rubric rewards honest abstention over confident error, a value judgement about research work that would reorder the arms if reversed.

The other forty questions stay sealed, because the thing being measured is what a model knows without the corpus, and that quantity dies the day the questions enter a training set.

Everything — protocol, harness, cost tables, the twenty published questions with
every model's answers and every judge's line — is at
👉 github.com/MinhHaDuong/corpus-access-bench

Next: if granularity is the lever, how far does it go? Structured re-extraction with headings and links, resolved identifiers, generated indexes and access instructions inside the corpus directory. There should be points left on the table for the small models.

Minh Ha-Duong, CNRS — CIRED.
