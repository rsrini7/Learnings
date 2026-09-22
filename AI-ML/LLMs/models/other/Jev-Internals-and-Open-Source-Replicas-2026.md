# Jev (TypeSafe AI): internals and the open-source replicas

> **Research note — 21 September 2026**
>
> Companion to [Jev-System-One-Decision-Model-2026](Jev-System-One-Decision-Model-2026.md), which covers what Jev is, how to use it, where it breaks, and how to try it. This note is the advanced material: how the model probably works internally, how to grade the evidence behind each claim, and the ecosystem that grew up around it.
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
| Shared-prefix KV cache, final-position vs. pointer-style readout, causal-attention reuse | **Inferred** from black-box behaviour |
| Sparse mixture-of-experts backbone | **Least certain / explicitly speculative** |
| Third-party experiment: top-1 retrieval accuracy 21% → 54% when using Jev as a reranker | **One creator's experiment**, not a benchmark |
| Browser control: **25/49** tasks solved by Jev alone vs. **49/49** with a WebMCP tool interface, at ~112× lower model cost than GPT-6 Astra using computer use | **Third-party open benchmark** — reproducible and harness-dependent, so a signal rather than a universal limit |
| Reachable via the **Vercel AI Gateway** | **Unverified** — reported in a supplied video, but not found in the official docs index or quick start. Confirm before relying on it. |

## The open-source replica ecosystem

**Within days of launch**, a wave of community projects appeared aiming to reproduce Jev's behaviour locally. The shared technical insight is that you do not need to train a model to classify: you can **read the option probabilities straight out of the prefill stage** — score each candidate answer's logits instead of generating a response. That makes local, near-free classification possible with existing open models.

These are **community implementations and replicas, not TypeSafe's weights**, and they are not drop-in equivalents:

| Project | Base / method | Reported character |
|---|---|---|
| **SemIf** (originally "OpenJev") | Frozen Qwen 3.5 4B; classification by reading prefill logits, **no training** | Simplest and most direct reproduction |
| **Nimble** | Qwen 3.5 9B + LoRA, ~3,000 examples using "contrastive data curation" (identical facts flipped to teach decision boundaries) | Trained decision boundaries |
| **Decider** | Qwen 3.5 2B; reads hidden states at the end of slots and projects them onto options | Extremely fast, ~33 ms per answer |
| **OpenJev** (Alex Wortega) | Entailment-focused, with multimodal input | Decisions over images; game demos |
| **DiffusionGemma** | 26B, diffusion-based | High-concurrency decision workloads |
| **NanoJev** | ~600M parameters | Tiny, simple classification |
| **Laya** | BERT-Large class (~420M) | Multilingual classification in a single forward pass |

Two community resources are worth knowing about:

- **JevBench** — a benchmark platform that scores these implementations on **intelligence, calibration, and efficiency**, i.e. the three axes that actually matter for this use case.
- **awesome-jev** — the ecosystem index (see links below).

**Where the replicas fall short.** They perform respectably on standard, "easy" classification, but still struggle with **complex multihop reasoning and date arithmetic** — the same weak spots TypeSafe documents for Jev itself. The pragmatic recommendation from the community is a **cascaded approach**: run a fast local model for the simple classifications, and escalate complex or low-confidence cases to a more capable reasoning model. That is the same architecture the vendor recommends, just with the cheap tier self-hosted.

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

**Related:**
- [Jev-System-One-Decision-Model-2026](Jev-System-One-Decision-Model-2026.md) — The main guide: what Jev is, how to use the primitives, its failure modes, and how to try it.
- [Auto-Regression](../../training/Auto-Regression.md) — The token-by-token decoding mechanism Jev abandons, and the alternatives to it.
- [LLM-Inference](../../architecture/LLM-Inference.md) — Why skipping the decode phase changes the latency and cost profile, and how the 70–500 ms budget is reached.
- [LLM-Benchmarks](../../architecture/LLM-Benchmarks.md) — How to read vendor-published evaluation numbers rather than trusting headline multipliers.
