# Jev / System One — Recent Video Evidence Log (2026)

**Scope:** evidence log for the three supplied videos, checked on 28 September 2026. This file is intentionally separate from the main Jev note. The video pages exposed titles, dates, descriptions, and chapters, but no usable transcript; claims below are therefore split into **video claim** and **primary-source check**.

## 1. The three videos

| Video | YouTube metadata | What can be established safely |
|---|---|---|
| [Decision Model Showdown: CLM vs Laya vs OpenJev vs Kev vs Jev](https://www.youtube.com/watch?v=UF0z3afz9V8) | Fahd Mirza · 26 Sep 2026 · 8:38 | Description says five models, an angry-customer test, a security-trap test, and “only two passed.” Chapters show a showdown table and verdict. No winner, model versions, prompts, sample size, or scores are exposed in the description. |
| [Julia-1: The Tiny AI That Decides in 10 Languages on CPU Locally](https://www.youtube.com/watch?v=Ty7Riayb78w) | Fahd Mirza · 28 Sep 2026 · 8:28 | Chapters cover angry-customer, security-trap, phishing, relationship-red-flag, Julia-vs-Jev benchmark, and a live 10-language demo. The description says Julia-1 maps state + question + possible answers to one decision. |
| [This New AI Architecture Makes Decisions 13x Faster](https://www.youtube.com/watch?v=eSuMmMMMrm0) | Prompt Engineering · 26 Sep 2026 · 16:29 | Description presents CLM as a System One model using state/action embeddings, a frozen 8B backbone plus small heads, and a DGX Spark demo with 1,080 tools. It reports ~80 ms latency and accuracy falling from 86% with 8 tools to 17% with 1,080. These are creator-reported figures. |

**Transcript uncertainty:** YouTube reported captions unavailable for the first two pages, and transcript export did not return text. The third page exposed a transcript control but no transcript was retrievable. The descriptions and chapter labels are evidence of what each video claims to cover, not a substitute for a transcript or reproducible run.

## 2. Primary-source checks

### Julia-1 — the clearest new local model

The [Julia-1 model card](https://huggingface.co/SupersonicLabs/Julia-1) verifies the core description:

- 144.3M parameters, based on `jhu-clsp/mmBERT-small`, Apache-2.0 artifacts, and CPU inference without a GPU.
- Native interface: state + question + 2–20 supplied answers; it returns a decision rather than generated text.
- Author-reported evaluation, measured 24 Sep 2026 on H200 BF16: typed decisions **1,463/2,000 = 73.15%** versus a supplied Jev reference of **72.70%**; AG News **94% vs 91%**; DAIR Emotion **86% vs 48%**; Banking77 **64% vs 87%**.
- The Jev column is a supplied reference, not a fresh Jev run; Banking77 uses a 72-label shortlist rather than a native 72-option call. These results do not establish that Julia-1 is generally better than Jev.
- The card also reports MASSIVE scenario classification at **71.50% macro accuracy across 52 locales**. This supports the multilingual direction, but it is not proof that every “10-language” demo language has equal quality.

**Integration reading:** Julia-1 is a promising small, local decision encoder. Treat its broad benchmark comparison as an author evaluation, and test long option lists and the actual languages in production.

### CLM — a real open implementation of the same interface

The [Contrastive-LM repository](https://github.com/Contrastive-LM/CLM) and [CLM-v0.1-8B model card](https://huggingface.co/Contrastive-LM/CLM-v0.1-8B) verify these points:

- `CLM-v0.1-8B` uses a Qwen3-8B pooling encoder plus small trainable state/action projection heads and exposes a TypeSafe-compatible API.
- It scores candidate actions by state/action embedding similarity; a softmax supplies the answer distribution. This is contrastive retrieval/classification, not autoregressive text generation.
- The published recipe has roughly **60M** Nemotron Q&A pairs, **30M** synthetic hard negatives, and **1M** agentic trajectories, using bidirectional InfoNCE and later hard-negative/agentic stages.
- The repository reports “on par with Jev” on its own computer-use, gaming, and tool-calling tests, up to **9× lower latency**, plus fine-tuned verifier results of **81.6% DeepSWE** and **87.6% Terminal-Bench 2.1**. These are project results, not an independent common benchmark of all five video models.

The video’s **“13× faster,” “~80 ms,” and 1,080-tool 86%→17%** details are not visible in the repository evidence checked here. Keep them as creator claims unless the project publishes the exact script, hardware, checkpoint, prompts, and raw results.

### Laya — current family, routing, and calibration caveat

The [Convai Innovations Laya model hub](https://huggingface.co/convaiinnovations/laya) currently documents three useful checkpoints: English `laya` (421M, ModernBERT-large), `laya-multilingual` (322M, mmBERT-base, 100+ languages), and `laya-typed-decisions` (421M, specialised typed-decision workflows). The [typed-decisions card](https://huggingface.co/convaiinnovations/laya-typed-decisions) reports **0.766 accuracy** versus a published Jev reference of **0.727**, but explicitly says the comparison is indicative because it was not measured through the Jev API with identical conditions.

The current runtime also documents a Router that chooses English versus multilingual checkpoints, long-document support up to 8,192 tokens when configured, and version `0.3.20` runtime fixes. The same card warns that the specialised checkpoint is English-only, was tuned for four workflows, and should be recalibrated on held-out data before using its probabilities for automation.

### Kev — the most inspectable Qwen-based family

The [Kev repository](https://github.com/jaredpalmer/kev) now lists **Kev-0.8B, 4B, 9B, and 27B**. The first three use Qwen3.5 bases; Kev-27B uses Qwen3.8. The API supports `noul`, `choice`, and `score`, and the repository states that TypeSafe’s Python SDK can be pointed at a local Kev server.

Its own new-source table reports test accuracy of **0.697 / 0.838 / 0.852 / 0.896** for Kev-0.8B / 4B / 9B / 27B, with Jev at **0.857** on a development comparison. The repository itself warns this is not a controlled architecture comparison: Jev’s training data is unknown and Jev was not evaluated on the same locked test. Preserve that caveat whenever quoting the numbers.

### OpenJev — a name, not one canonical model

The first video does not expose which OpenJev implementation it tested. That matters because the name currently refers to multiple independent projects, for example:

- [razorback16/openjev](https://github.com/razorback16/openjev): a server built around DiffusionGemma 26B-A4B, with routed Laya, Verdict, CLM, and other models; its README says it is independent and not endorsed by TypeSafe.
- [openjev/openjev](https://huggingface.co/openjev/openjev): a separate open-weights decision model described as one forward pass per question, with up to 52 options and an H100 latency example.
- [lookski/openjev](https://github.com/lookski/openjev): a local adapter that turns a selectable causal LLM into a Jev-style softmax decision engine and explicitly warns that its probabilities are not RLCD-calibrated like Jev’s.

These should not be merged into one “OpenJev” benchmark result. Identify the exact repository, checkpoint, backend, option count, and version before importing the showdown’s result into the main note.

### Jev — current official reference

TypeSafe’s [current model page](https://docs.typesafe.ai/models) lists `jev-1.13.0` as the current model and `jev-latest` as its stable alias. It documents 64k tokens per request, a 32k state-plus-longest-question limit, text-only input, and input pricing of **$0.042 per million tokens** with free output tokens. The [Jev 1.13 jaggedness guide](https://docs.typesafe.ai/model-jaggedness/jev-1.13) explicitly warns about literal reading, numeric/date arithmetic, indirection, irrelevant context, adversarial state, contradictory criteria, and generation.

## 3. Simple comparison for integration

| Model | Main strength | Local/open? | Important caution |
|---|---|---:|---|
| Jev 1.13 | Hosted, calibrated typed decisions; broad option support | No | Versioned API and alias can change; vendor/hosted comparison numbers are not universal. |
| CLM-8B | Contrastive state/action scoring; cached candidates; TypeSafe-compatible API | Yes | Repo benchmarks and speed claims are project-owned; the 1,080-tool result needs reproduction. |
| Laya family | Small local encoders; multilingual routing; RLCD-style probabilities | Yes | Calibration and accuracy vary by checkpoint, language, option count, and fine-tuning. |
| Kev family | Qwen-based 0.8B–27B family; trainable and API-compatible | Yes | Published Jev comparisons are not controlled same-run comparisons. |
| Julia-1 | Very small multilingual CPU model; 2–20 native options | Yes | Long/large label sets are a known weak point; Jev references are supplied, not re-run. |
| OpenJev projects | Several independent local implementations under one name | Usually | “OpenJev” is ambiguous; never quote a result without the exact repo/checkpoint. |

## 4. Safe conclusions to carry into the main note

1. The category is expanding from one hosted Jev model into several open, local families: CLM, Laya, Kev, Julia-1, and multiple OpenJev projects.
2. The strongest common idea is bounded decision output: state + question + caller-supplied options → typed answer probabilities. The architectures and calibration quality differ substantially.
3. The videos are useful discovery material and test-design prompts, but their rankings are not interchangeable benchmarks. Re-run every comparison with fixed prompts, versions, hardware, option counts, language, cold/warm cache policy, accuracy, calibration, and failure handling.
4. A practical deployment pattern remains: local model for cheap, fast first-pass routing; Jev or a larger LLM for uncertain or high-impact cases; ordinary code for arithmetic, dates, schema validation, and execution permissions.

## Sources

**Video evidence**

- [UF0z3afz9V8 — CLM vs Laya vs OpenJev vs Kev vs Jev](https://www.youtube.com/watch?v=UF0z3afz9V8)
- [Ty7Riayb78w — Julia-1](https://www.youtube.com/watch?v=Ty7Riayb78w)
- [eSuMmMMMrm0 — CLM architecture](https://www.youtube.com/watch?v=eSuMmMMMrm0)

**Primary model sources**

- [TypeSafe models](https://docs.typesafe.ai/models) · [Jev 1.13 limitations](https://docs.typesafe.ai/model-jaggedness/jev-1.13)
- [Contrastive-LM/CLM](https://github.com/Contrastive-LM/CLM) · [CLM-v0.1-8B](https://huggingface.co/Contrastive-LM/CLM-v0.1-8B)
- [Convai Innovations Laya](https://huggingface.co/convaiinnovations/laya) · [Laya typed-decisions](https://huggingface.co/convaiinnovations/laya-typed-decisions) · [Laya source](https://github.com/NandhaKishorM/laya)
- [Jared Palmer’s Kev](https://github.com/jaredpalmer/kev)
- [SupersonicLabs Julia-1](https://huggingface.co/SupersonicLabs/Julia-1)
- [OpenJev server](https://github.com/razorback16/openjev) · [OpenJev model](https://huggingface.co/openjev/openjev) · [OpenJev adapter](https://github.com/lookski/openjev)

---

**Related:**
- [Jev-System-One-Decision-Model-2026](Jev-System-One-Decision-Model-2026.md) — concise Jev guide and official limitations.
- [Jev-Internals-and-Open-Source-Alternatives-2026](Jev-Internals-and-Open-Source-Alternatives-2026.md) — deeper architecture, replicas, and benchmark caveats.
- [LLM-Benchmarks](../../architecture/LLM-Benchmarks.md) — how to interpret non-equivalent model comparisons.
