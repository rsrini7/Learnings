# Jev (TypeSafe AI): internals and the open-source alternatives

> **Research note — 21 September 2026** (updated 22 September 2026)
>
> Companion to [Jev-System-One-Decision-Model-2026](Jev-System-One-Decision-Model-2026.md), which covers what Jev is, how to use it, where it breaks, and how to try it. This note is the advanced material: how the model probably works internally, how to grade the evidence behind each claim, and the projects that grew up around it — the quick replicas, plus **Laya** and **Kev**, the two that publish real comparisons against Jev.
>
> **Nothing here is published by TypeSafe except where explicitly marked.** The rest is inferred from black-box probing, reported by third parties, or speculative. Treat the confidence column, not the prose, as the load-bearing part.

## What is actually published

TypeSafe confirms three things about the mechanics:

1. **No autoregressive decoding.** Jev "outputs all probabilities in parallel instead of autoregressively generating by token."
2. **A parallel sampler**, described as part of a stack built specifically for automation and as "incredibly efficient and hardware-aware."
3. **RLCD** — Reinforcement Learning for Calibrated Decisions — as the training objective.

What is *not* published is the architecture. No public weights or technical architecture paper are cited in the reviewed sources. That gap is precisely what motivated both the reconstruction below and the replica ecosystem further down.

## The reconstruction

A third-party black-box reconstruction argues Jev is best understood as **a causal transformer repurposed for decisions**:

- A shared `state` is encoded once, and each question branch attends to it **but not to other questions**.
- There is no dependency chain between answers — the model does not need to finish classifying before estimating urgency. Both read the state; neither consumes the other's output.
- Instead of a decode loop, a **prediction head** maps the final hidden vector to logits over the allowed answers, and a softmax turns those into a distribution: `p_i = softmax(W·h + b)` across the K allowed answers.
- Option slots can be **positions** ("first", "second", "third") rather than fixed concepts, with the branch supplying each slot's meaning and application code mapping probabilities back to the caller's option keys. JSON formatting happens in ordinary code, not in the network.
- "Parallel" refers to **scheduling and the absence of answer dependencies**, not one GPU per question — branches can still be batched onto the same accelerator.

The author offers two candidate readout designs, both consistent with what can be observed: a **final-position head** that scores each option slot from the decision token's representation, or a **pointer-style scorer** that compares the decision representation against each option's own final hidden state. Because a language model's vocabulary head is itself a matrix plus softmax, reserving K label rows could replicate a dedicated K-class head — which is why the two cannot be told apart from outside.

**An open reimplementation has since settled part of this.** [Kev](#kev-train-your-own-wire-compatible-with-jev) is built as exactly a **pointer-style readout head** — it scores each option's hidden state against the question's decision token, then softmaxes. That does not prove Jev uses the same design, but it demonstrates the inferred mechanism is *sufficient* to produce the observed behaviour, and it gives the hypothesis a working reference implementation.

### The central conceptual point

Causal attention describes **which positions may use which information**, not the order in which input tokens must be executed. During prefill, all input tokens are already known; the model processes their positions together within a layer (the attention mask blocks access to later positions), while layers still run sequentially. Autoregressive decoding adds an *extra* dependency — the next token — and this design avoids it.

That distinction is also why **reading out a probability is not the same as generating text that describes a probability**. A generated "91%" is a token sequence; a classifier's `0.91` is a distribution entry. Either can be miscalibrated.

### Numbers from the probing

| Observation | Value | Confidence |
|---|---|---|
| Latency | ~30k tokens processed in ~160 ms | Observed (includes shared-service overhead; not a hardware benchmark) |
| Context per question branch (state + one question) | ~32,768 tokens | Observed |
| Context per whole request | ~65,536 tokens | Observed |
| Options per Choice | ≤ 255 (2⁸ − 1) | Vendor-stated |
| Backbone | Sparse mixture-of-experts transformer | **Speculative** |

The context numbers are the most revealing result: a 23k-token state with 5,000 questions fits, whereas per-question copies of the state would exceed 100 million tokens — which is what supports a **shared-prefix KV cache**. The author expects a **sparse MoE** backbone, supported by the benchmark references in use (DeepSeek-V3, Qwen3, GLM-4.5, Kimi K2, gpt-oss), but is explicit that nothing else in the design depends on it. No layer count is given.

Two probing experiments are worth citing because they pin down behaviour rather than architecture:

- **Visibility test** — moving a secret declaration out of a sibling question and into the state changed its reported probability from **0.00 to ~0.90**, supporting genuine behavioural isolation between questions.
- **Option-interaction test** — adding an irrelevant fifth option shifted the log-odds between two existing options from **+0.38 to +0.11**, with all ten blocks decreasing. That argues *against* fixed independent logits with an unchanged softmax: options interact.

### Caveats the author emphasises

- The reconstruction is speculative — "black box APIs make it shockingly easy to throw a blanket over the ghost."
- **No public tokenizer matched** (192 tested × 415 probes; closest was Qwen at 348/415). This rules out an *unchanged* public tokenizer, **not** a public base model.
- TypeSafe does not share research, and Jev is **not open-weight**.

## What the evidence actually supports

Because this ecosystem mixes vendor claims, third-party experiments, and speculation, it helps to grade every claim explicitly:

| Claim | Status |
|---|---|
| Direct probability outputs, no token-by-token generation; parallel sampling | **Published** by TypeSafe |
| RLCD training objective | **Named** by TypeSafe; exact recipe unpublished |
| Typed interface (`Choice` / `Score` / `Noul`), calibration, confidence semantics | **Published** in the docs |
| Documented failure modes and recommended fallbacks | **Published** (jaggedness page) |
| 70–500 ms latency, $0.042/MTok, 193.6×/444.6× workflow gains | **Vendor-published**, with the caveats in the companion note |
| Question isolation and option-interaction behaviour | **Observed** by third-party API probing |
| Shared-prefix KV cache, final-position vs. pointer-style readout, causal-attention reuse | **Inferred** — though the pointer-style readout now has a working open implementation (Kev), and Kev independently arrives at the same "encode the state once, answer questions independently" design |
| Sparse mixture-of-experts backbone | **Least certain / explicitly speculative** |
| Third-party experiment: top-1 retrieval accuracy 21% → 54% when using Jev as a reranker | **One creator's experiment**, not a benchmark |
| Browser control: **25/49** tasks solved by Jev alone vs. **49/49** with a WebMCP tool interface, at ~112× lower model cost than GPT-6 Astra using computer use | **Third-party open benchmark** — reproducible and harness-dependent, so a signal rather than a universal limit |
| Laya's head-to-head wins over Jev (latency, ECE, accuracy) | **A competitor's self-reported numbers** — Laya's side measured on a T4, Jev's side taken from third-party published figures the author never measured. Not a controlled comparison. |
| Kev's accuracy versus hosted Jev (0.852 vs 0.857) | **Third-party, self-reported, not independently reproduced** — and explicitly *not* a controlled architecture comparison, because Jev's training data is unknown. Its disclosed pre-registered criteria were missed. |
| Reachable via the **Vercel AI Gateway** | **Unverified** — reported in a supplied video, but not found in the official docs index or quick start. Confirm before relying on it. |

## The open-source ecosystem

**Within days of launch**, a wave of community projects appeared aiming to reproduce Jev's behaviour locally. The shared technical insight is that you do not need to train a model to classify: you can **read the option probabilities straight out of the prefill stage** — score each candidate answer's logits instead of generating a response. That makes local, near-free classification possible with existing open models.

These are **community implementations, not TypeSafe's weights**, and none is a drop-in equivalent. Six are *replicas* — fast reimplementations of the idea. Two are more consequential and get their own sections below: **Laya**, which claims to predate Jev and competes with it head-on, and **Kev**, which publishes open weights you can fine-tune and serve behind Jev's own API shape. Those two are also the only ones that publish reproducible comparisons against Jev.

| Project | Base / method | Reported character |
|---|---|---|
| **SemIf** (originally "OpenJev") | Frozen Qwen 3.5 4B; classification by reading prefill logits, **no training** | Simplest and most direct reproduction |
| **Nimble** | Qwen 3.5 9B + LoRA, ~3,000 examples using "contrastive data curation" (identical facts flipped to teach decision boundaries) | Trained decision boundaries |
| **Decider** | Qwen 3.5 2B; reads hidden states at the end of slots and projects them onto options | Extremely fast, ~33 ms per answer |
| **OpenJev** (Alex Wortega) | Entailment-focused, with multimodal input | Decisions over images; game demos |
| **DiffusionGemma** | 26B, diffusion-based | High-concurrency decision workloads |
| **NanoJev** | ~600M parameters | Tiny, simple classification |
| **Laya** | ModernBERT-large (421M) / mmBERT-base (322M), Apache 2.0 | Not a replica — see below |
| **Kev** | Qwen3.5 / Qwen3 bases + rank-16 LoRA + pointer head, Apache 2.0 | Not a replica — see below |

Two community resources are worth knowing about:

- **JevBench** — a benchmark platform that scores these implementations on **intelligence, calibration, and efficiency**, i.e. the three axes that actually matter for this use case.
- **awesome-jev** — the ecosystem index (see links below).

**Where the replicas fall short.** They perform respectably on standard, "easy" classification, but still struggle with **complex multihop reasoning and date arithmetic** — the same weak spots TypeSafe documents for Jev itself. The pragmatic recommendation from the community is a **cascaded approach**: run a fast local model for the simple classifications, and escalate complex or low-confidence cases to a more capable reasoning model. That is the same architecture the vendor recommends, just with the cheap tier self-hosted.

## Laya: the open alternative, and the priority dispute

**What it is.** [Laya](https://github.com/NandhaKishorM/laya) is an open-source (Apache 2.0) "System 1" decision engine from ConvAI Innovations, written by **Nandakishor Mukkunnoth**, and unaffiliated with TypeSafe. It uses **the same three primitive names** — `choice`, `score`, `noul` — over a `state`, in a single forward pass. Three checkpoints ship on Hugging Face:

| Checkpoint | Encoder | Params | Context | For |
|---|---|---|---|---|
| `laya` | ModernBERT-large | 421M | 512 | English |
| `laya-multilingual` | mmBERT-base | 322M | 1024 | 100+ languages |
| `laya-typed-decisions` | ModernBERT-large | 421M | 1024 | Typed-decision workflows |

A built-in **Router** detects script and language in under a millisecond and selects the checkpoint, preloading them to avoid a **7–10 second cold swap** when the language changes. Install is `pip install laya`; the video calls the option-scoring mechanism "Option Marker Scoring", though that term does not appear in the project's own README.

**The priority claim.** Mukkunnoth states he built non-autoregressive, RL-guided decision models about a year before Jev: a **March 2025** model using PPO over sequence representations to emit conversion probabilities, backed by [arXiv:2503.23303](https://arxiv.org/abs/2503.23303), a second paper formalising the framework ([arXiv:2510.01237](https://arxiv.org/abs/2510.01237)) in September 2025, plus open weights and a dataset. His grievance, in his own words: TypeSafe "proposed the exact same non-autoregressive decision concept as if it was a brand-new scientific breakthrough", and "launched without technical papers, without open weights, and with zero open training datasets". Note the scope — the 2025 work was a **domain-specific sales-conversion model**, not a general typed-decision engine, so the claim is about the concept and the mechanism rather than a like-for-like product.

**TypeSafe's side.** The docs call Jev "TypeSafe's flagship model and **the first System One model**", and the launch post says "our first System One Model". **No public response to the priority claim was found in the sources available here**, and the dispute looks unresolved — treat it as contested attribution, not settled fact.

**Why the head-to-head numbers should be discounted.** Laya's README publishes wins against Jev 1.13.0 (32.8 ms vs 236–276 ms p50; ECE 0.081 vs 0.246; higher accuracy on typed-decisions, AG News and DAIR Emotion). Two caveats outweigh the numbers: the two sides were **not measured the same way** — Laya's figures come from its own runs on a T4, while Jev's are third-party published numbers the author never measured, against a hosted API on unknown hardware — and a separate reviewer makes the mirror-image point that comparing local Laya to hosted Jev without accounting for hardware is misleading. Laya is also **far more useful for publishing its own failures than its wins**, which is where the real insight is:

| Laya's own limitation | Number |
|---|---|
| Choice accuracy on Banking77 (77 labels) | 0.425, against Jev's 0.870 |
| Zero-shot base checkpoints vs a 0.318 random baseline | 0.362 / 0.342 — near chance |
| Mean ECE before temperature fitting | 0.466 → 0.081 after |
| `laya-multilingual` | Ships with **no fitted temperatures at all** |

Laya's own summary: "a fast base to specialise, not a zero-shot decision engine." The headline 0.766 comes from a fine-tuned checkpoint.

**Three findings that generalise beyond Laya** — this is the most valuable part of the whole episode:

1. **Option count is an architectural constraint, not just a limit.** Laya scores options by packing their text into a fixed token budget (`head_max_len`). At 77 labels only 3–4 tokens remain per label, the labels become textually indistinguishable, and accuracy collapses. Jev's 255-option ceiling and its advice to decompose high-cardinality choices are the same pressure from the other side. **With many options, use a two-stage shortlist rather than one large Choice** — Laya ships `predict_shortlist` for exactly this.
2. **Confidence does not protect you from an input the model cannot read.** ModernBERT-large scored **0.000 accuracy on Khmer at 95% confidence**. A calibrated model can be confidently wrong when the input is outside its competence, so confidence gating needs an input-validity check next to it — which is why Laya ships a script-detection router.
3. **Calibration often needs repair even in a model trained for it.** Laya trains with RL against proper scoring rules and *still* ships over-confident; refitting **one temperature per (question type, option count)** on held-out data cut mean ECE from 0.466 to 0.081. The practical lesson for Jev users is the same: **measure ECE on your own data before trusting a threshold**, and refit if you can.

## Kev: train your own, wire-compatible with Jev

**What it is.** [Kev](https://github.com/jaredpalmer/kev) is described by its author as "small Jev-like decision models you can train and run yourself." It is built by **Jared Palmer** — VP of Engineering at Cognition, founder of Turborepo (acquired by Vercel), and credited with Vercel's v0 and AI SDK — with help from Devin, and it is explicitly **based on the architecture described in *Jev's Architecture Unmasked***, the same write-up this note draws on. Apache 2.0, weights on Hugging Face, Python 3.12+, served with `python -m kev.serve`. Unlike everything above, it is a *family you fine-tune*, not a fixed checkpoint.

**Why it matters more than the replicas: it is wire-compatible.** The API deliberately matches TypeSafe's System One — "so you can point their Python SDK at your local server." It exposes the same three primitives with the same ceilings (`choice` 1–255 options, `score` 2–255), the same `state` + `questions` request shape, and the same `noul` / `choice` / `score` response fields. Two endpoints go further than Jev: `/v1/systemone/permute` runs one Choice under several option orders, and `/v1/systemone/separate` runs each question in its own forward pass. Two cautions: the server binds to `127.0.0.1` with **no authentication**, so keep it local; and the README carries **no non-affiliation disclaimer** — TypeSafe is credited only for the API design, and "no Jev outputs were used for training."

**How it works — and what that confirms.** Each checkpoint is a **rank-16 LoRA adapter plus a small pointer head on a frozen Qwen base**. The head scores each option's hidden state against the question's decision token and softmaxes, which is the **pointer-style readout** the black-box reconstruction proposed as one of two candidates — so the inferred mechanism now has a working open implementation. One forced change is instructive: the Qwen3.5 bases mix attention with **recurrent Gated DeltaNet layers** that ignore the block attention mask, so Kev runs **each question as its own row**, computes the state once, and **reuses its cache**. That is the same "encode the state once, answer questions independently" design the probing inferred in Jev. Kev also reproduces the option-order effect: questions are isolated from each other, but **options within a question still interact**.

**The benchmarks, and why they are the best available.** Kev publishes accuracy on a locked, new-source test set alongside hosted Jev — with the caveat that matters: *"We don't know which datasets Jev was trained on, so this isn't a controlled comparison of the two architectures."*

| Model | Base | New-source accuracy (dev / test) |
|---|---|---|
| Kev-0.8B | Qwen3.5-0.8B-Base | 0.652 / 0.684 |
| Kev-4B | Qwen3.5-4B-Base | 0.797 / 0.837 |
| Kev-9B | Qwen3.5-9B-Base | 0.822 / **0.852** |
| **Jev (hosted)** | — | **0.857** (development comparison only) |

Two things make this credible rather than marketing: the port to Qwen3.5 cost about **$95 of Modal H100 time plus $0.03 of Jev API calls**, and Kev's **pre-registered development criteria were not met** even though the locked test favoured the new checkpoints — the repository publishes both outcomes instead of swapping the gate after seeing the data.

**Calibration, and where Jev's real advantage sits.** Each checkpoint stores a temperature fitted on its development set (~2.1–2.4) and applies it at load; calibration error on new sources drops **0.106 → 0.042**, and confidently-wrong answers (≥0.9 probability, incorrect) fall **8.7% → 4.0%**, close to Jev's 3.7%. But a single temperature cannot *reorder* confidences, so the share of decisions automatable at a 5% error budget is **0.45–0.57 for Kev against 0.70 for Jev**. That is the sharpest published statement of what Jev's calibration actually buys you, and it is more useful than any latency multiple.

**A directly reusable technique — and a warning.** Setting `KEV_DATE_FACTS=1` appends computed day-counts between absolute dates to the state ("June 26, 2026 is 8 days before July 4, 2026"), lifting deadline-policy accuracy from **0.80 → 0.90** (Jev 0.93). That is the concrete form of Jev's own advice to keep date arithmetic in code: precompute the deltas and put them *in the state*, rather than asking the model to compare dates. The warning is in the same result: fine-tuning **worsened** the base model's date arithmetic (Qwen3.5-9B base 0.82 → first Kev-9B 0.72) before the day-count examples recovered it — specialising a model can cost it general skills.

**Stated limits.** Knowledge gaps are base-model-bound: **MMLU 0.74 vs Jev's 0.90**, MMLU-Pro 0.52 vs 0.84. It is slow on Apple Silicon — Kev-4B measured 779 ms against 174 ms for its Qwen3 predecessor, and Kev-9B about 2 s, because there are no fast kernels for the DeltaNet layers; Palmer recommends the older Qwen3 checkpoints on Macs until an MLX backend lands. Training covered ≤384 state tokens, but serving allows 8,192 — beyond the trained range. The server is single-request with no cross-caller batching. And it is **confidently wrong on questions the supplied evidence cannot answer**, which is on the fix list.

**Why it belongs in this note.** Kev is the strongest evidence that the category is reproducible: one experienced engineer, a coding agent, and about **$95 of rented GPU time** produced an inspectable, API-compatible, Apache-2.0 implementation with published failure data. It converts the reconstruction above from inference into something you can run.

## Sources

**Primary (vendor)**

- [Introducing System One Models & Jev](https://typesafe.ai/blog/introducing-system-one-models-and-jev) — RLCD, the parallel sampler, the published mechanism claims, and the benchmark caveats.
- [TypeSafe workflow evaluations](https://evals.typesafe.ai/) — vendor workflow-eval design, reference models, and per-workflow detail.
- [Jev 1.13 jaggedness](https://docs.typesafe.ai/model-jaggedness/jev-1.13) — the officially documented failure modes.
- [Models](https://docs.typesafe.ai/models) — the authoritative context-window and token limits.
- [TypeSafe GitHub org](https://github.com/typesafe-ai) · [system-one-adapter-python](https://github.com/typesafe-ai/system-one-adapter-python) · [skills](https://github.com/typesafe-ai/skills)

**Third-party reconstruction and reporting**

- [Jev's architecture unmasked](https://archerhume.com/posts/jevs-architecture-unmasked/?v=3) — the black-box reconstruction this note draws on, which separates published, observed, and inferred evidence itself.
- [Open-source Jev alternatives](https://www.youtube.com/watch?v=53wDOI_7x8I) — the survey covering SemIf, Nimble, Decider, OpenJev, DiffusionGemma, NanoJev, Laya, and JevBench.
- [Jev benchmarks and limitations](https://www.youtube.com/watch?v=2XFXe-oGnrI) — the Jev-versus-Astra workflow comparison.

**Community projects**

- [awesome-jev](https://github.com/fatwang2/awesome-jev) (ecosystem index) · [SemIf](https://github.com/TheoLeeCJ/SemIf) · [building-with-jev-skill](https://github.com/dbreunig/building-with-jev-skill) · [localjev](https://github.com/githubnext/localjev) · [fast-jev-compaction](https://github.com/tamaratran/fast-jev-compaction) · [simple-jev](https://github.com/featherless-ai/simple-jev) ([playground](https://simple-jev.featherless.ai/)) · [Open-Jev on Hugging Face](https://huggingface.co/spaces/pngwn/open-jev)

**Community indexes and benchmarks**

- [Made with Jev](https://madewithjev.com/) — community index of builds and the source family for the supplied *"What are people building with Jev"* slide. A community compilation, not TypeSafe material.
- [WebMCP browser-agent benchmark](https://webmcp.com/benchmark) — open, reproducible benchmark behind the browser-control result (25/49 alone, 49/49 with a tool interface); harness at [WindTunnel](https://github.com/nekuda-ai/WindTunnel), browser agent at [jev-ultrafast](https://github.com/browser-use/jev-ultrafast).

**Laya and the priority dispute**

- [Laya repository](https://github.com/NandhaKishorM/laya) — Apache 2.0, `pip install laya`; the three checkpoints, the token-budget behaviour, the latency table, and — unusually — its own limitations.
- [Laya checkpoints on Hugging Face](https://huggingface.co/convaiinnovations/laya) — `laya`, `multilingual`, `typed-decisions`.
- [Laya project site](https://laya.convaiinnovations.com/) — Nandakishor Mukkunnoth's priority claim in his own words, plus the head-to-head benchmark table.
- [arXiv:2503.23303](https://arxiv.org/abs/2503.23303) (March 2025) and [arXiv:2510.01237](https://arxiv.org/abs/2510.01237) (September 2025) — the papers cited as prior art.
- [Open-source Laya challenges Jev](https://www.aipulse.it/en/news/laya-open-source-decision-model-jev-726343) — neutral summary of the dispute and Laya's technical claims.
- [The priority dispute, both sides](https://tonybai.com/2026/09/20/jev-laya-non-autoregressive-decision-model-priority-dispute/) — background on the open-source-versus-funded-lab argument.
- [TypeSafe privacy policy](https://typesafe.ai/privacy) — the "will not train or fine tune … on Input" and retention commitments.
- Supplied videos: [the dispute](https://www.youtube.com/watch?v=OLgiHBlDhWU) · [Laya technical deep dive](https://www.youtube.com/watch?v=ifMK3FfPPOw) · [Laya as a local Jev alternative](https://www.youtube.com/watch?v=BlQAw6P7kjY).

**Kev**

- [Kev repository](https://github.com/jaredpalmer/kev) — Apache 2.0; training recipes, dataset manifests, experiment plans, confidence intervals and *failed* decision gates published alongside the checkpoints.
- [Kev on Hugging Face](https://huggingface.co/collections/jaredpalmer/kev) — the collection; cards at [kev-0.8b](https://huggingface.co/jaredpalmer/kev-0.8b), [kev-4b](https://huggingface.co/jaredpalmer/kev-4b) and [kev-9b](https://huggingface.co/jaredpalmer/kev-9b).
- [Kev's experiment plan](https://github.com/jaredpalmer/kev/blob/main/PLAN.md) — the pre-registered criteria, and the disclosure that they were not met.
- [Jared Palmer ports Kev to Qwen3.5](https://runtimewire.com/article/jared-palmer-kev-qwen35-decision-models) — the author's background, the ~$95 training bill, and the release timeline.

**Related:**
- [Jev-System-One-Decision-Model-2026](Jev-System-One-Decision-Model-2026.md) — The main guide: what Jev is, how to use the primitives, its failure modes, and how to try it.
- [Auto-Regression](../../training/Auto-Regression.md) — The token-by-token decoding mechanism Jev abandons, and the alternatives to it.
- [LLM-Inference](../../architecture/LLM-Inference.md) — Why skipping the decode phase changes the latency and cost profile, and how the 70–500 ms budget is reached.
- [LLM-Benchmarks](../../architecture/LLM-Benchmarks.md) — How to read vendor-published evaluation numbers rather than trusting headline multipliers.
