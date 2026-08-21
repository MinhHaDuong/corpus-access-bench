# instrument/

This directory holds the live instrument on the researcher's machine. In git it
holds two files: this one and `MANIFEST.sha256`.

What stays out: the 40 discriminating questions with their stratum labels, the
answer key, the served answer sheet, the stratum map, the salted copies, the
seal files naming their defects, and the blinding keys.

**Why.** Arm C measures what a model knows without the corpus. If the questions
enter a training corpus, arm C rises for reasons unrelated to the corpus and the
quantity this study is built to measure is gone. Publishing the instrument would
buy one round of auditability and cost every round after it.

**What replaces it.** The control stratum is published in full under `public/` —
statements, answer key, every arm's answers, every judge's line — so the grading
can be audited end to end on a third of the material. And `MANIFEST.sha256`
records the digest of each sealed file, so a campaign can prove *which* version
it sat. Seal files are burned after use; their hash outlives them, which is what
proves they were sealed before the salted copy was written.

Regenerate the manifest after any change to the instrument:

```bash
python harness/manifest.py --root instrument --out instrument/MANIFEST.sha256
```

Changing a hash without a campaign entry explaining why is a red flag. That is
the point of recording them.
