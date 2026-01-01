# VL-JEPA: Joint Embedding Predictive Architecture for Vision-Language Understanding
## A Comprehensive White Paper

**Authors:** Delong Chen, Mustafa Shukor, Théo Moutakanni, Willy Chung, Jade Yu, Tejaswi Kasarla, Allen Bolourchi, Yann LeCun, Pascale Fung

**Organization:** Meta FAIR, HKUST, Sorbonne Université, NYU

**Date:** December 2025

**arXiv:** 2512.10942

---

## Executive Summary

VL-JEPA represents a fundamental paradigm shift in vision-language modeling. Instead of following the established pattern of autoregressively[A1] generating text tokens, VL-JEPA predicts continuous semantic embeddings[A2] directly in an abstract latent space[A3]. This architectural innovation delivers three critical advantages:

1. **Training Efficiency**: 50% fewer trainable parameters while achieving superior performance compared to token-based vision-language models (VLMs)[A4]
2. **Sample Efficiency**: Demonstrably faster learning curves—reaching performance parity with baseline models in half the training iterations
3. **Inference Scalability**: Non-autoregressive[A1] design enables selective decoding, reducing computational cost by ~2.85× for real-time video applications

This white paper provides a complete technical exposition of VL-JEPA's architecture, methodology, experimental validation, and implications for future vision-language AI systems.

---

## 1. Introduction

### 1.1 Problem Statement

Current vision-language models struggle with fundamental inefficiencies:

**Training Inefficiency**: Generative VLMs[A4] trained with cross-entropy loss[A5] must learn two distinct aspects simultaneously: (1) task-relevant semantic understanding and (2) task-irrelevant surface-level linguistic variation (word choice, phrasing, grammar). For example, when asked "What happens if I flip this light switch down?", valid answers include "the lamp is turned off," "the room goes dark," and "the light disappears." In discrete token space, these orthogonal[A6] sequences require the model to fit multiple disjoint high-density regions in sparse token space, dramatically increasing training cost.

**Inference Latency**: Autoregressive token generation is inherently sequential. The model must complete the entire output sequence before the underlying semantic meaning becomes apparent. For real-time applications (wearables, robotics, live video analysis), this introduces unacceptable latency and prevents efficient selective decoding[A7].

**Parameter Inefficiency**: Token-based VLMs require large language decoders[A8] to handle autoregressive generation, adding substantial trainable parameters without improving core semantic understanding.

### 1.2 Solution: Joint Embedding Predictive Architecture

VL-JEPA addresses these limitations by shifting the training objective from token space to embedding space. The key insight: if multiple valid answers naturally cluster nearby in a continuous semantic embedding space, the learning problem becomes single-mode and substantially simpler.

**Core Innovation**: Train a predictor[A9] to map visual embeddings[A10] and text queries directly to semantic embeddings[A2] of target text, bypassing autoregressive token generation entirely during training. Text decoding[A11] becomes an optional post-processing step invoked only when human-readable output is required.

### 1.3 Contributions

- **First non-generative[A12] general-domain vision-language model** capable of real-time task execution
- **Controlled empirical validation** demonstrating embedding-space supervision outperforms token-space supervision under identical training conditions
- **Efficient streaming inference** via selective decoding, reducing computational overhead by ~2.85× for video understanding
- **Unified multi-task architecture** seamlessly handling generation, classification, retrieval, and visual question answering without task-specific modifications

---

## 2. Methodology

### 2.1 Architecture Overview

VL-JEPA comprises four components processing triplets ⟨X_V, X_Q, Y⟩:
- X_V: Visual input (image or video frames)
- X_Q: Textual query (prompt or question)
- Y: Textual target (expected answer)

#### 2.1.1 X-Encoder (Vision Encoder)

**Component**: Frozen V-JEPA 2[A13] Vision Transformer (ViT-L) with 304M parameters

**Function**: Compresses high-dimensional visual input into a sequence of visual embeddings[A10], analogous to "visual tokens" in classical VLMs but represented as continuous vectors rather than discrete symbols.

**Input Processing**:
- Image inputs: 256² resolution; duplicated to match temporal sequence format
- Video inputs: 16 frames uniformly sampled at 256² resolution per frame
- Output: Sequence of continuous visual embeddings S_V

**Design Rationale**: V-JEPA 2 is frozen (parameters not updated during VL-JEPA training) because it produces inherently robust semantic visual representations through self-supervised learning[A14]. By freezing it, the training budget focuses on vision-language alignment rather than re-learning basic visual features.

#### 2.1.2 Predictor (Core Learning Module)

**Component**: Last 8 Transformer layers from Llama-3.2-1B, initialized from this pretrained language model

**Trainable Parameters**: ~490M (substantially fewer than typical VLM decoders)

**Function**: Core module that learns to map visual embeddings and text queries to predicted semantic embeddings of target text. This is where the primary learning occurs.

**Input Handling**:
- Visual embeddings S_V from X-Encoder
- Text query X_Q: Tokenized using Llama-3.2-1B tokenizer, maximum 512 tokens, padded with [PAD] tokens if shorter
- Attention Mechanism: Bidirectional attention (causal masking[A15] disabled), enabling free interaction between vision and text tokens

**Output Processing**:
- Transformer layer outputs pooled (average pooling over non-[PAD] tokens)
- Linear projection into shared embedding space
- Final output: Ŝ_Y (predicted semantic embedding)

**Design Rationale**: Using final layers of a pretrained language model rather than training from scratch leverages existing knowledge about semantic and causal reasoning, achieving better sample efficiency[A16].

#### 2.1.3 Y-Encoder (Target Embedding)

**Component**: EmbeddingGemma-300M, initialized from this pretrained text embedding model

**Function**: Encodes ground-truth target text Y into semantic embeddings S_Y, serving as the learning target during training.

**Input Processing**:
- Target text Y (answer)
- Maximum context length: 512 tokens to handle detailed captions
- Frozen during initialization, trainable with reduced learning rate multiplier (×0.05)

**Output**: S_Y—continuous semantic embedding in shared 1,536-dimensional space

**Design Rationale**: Using a dedicated, visually-aligned text encoder ensures the target embedding captures semantic meaning rather than arbitrary linguistic form. The reduced learning rate multiplier (×0.05) prevents destabilization early in training when embedding quality is suboptimal.

#### 2.1.4 Y-Decoder (Text Reconstruction)

**Component**: Lightweight text decoder for inference-time use only

**Function**: Converts predicted semantic embeddings Ŝ_Y into human-readable text ˆY

**Critical Distinction**: Y-Decoder is **not involved in the main training loop**. It is only invoked at inference time when explicit text output is required. This is a key efficiency advantage over traditional generative VLMs that require large decoders throughout training.

### 2.2 Training Objective

#### 2.2.1 Loss Function Formulation

**Token-Space Loss (Classical VLMs)**:
$$\mathcal{L}_{VLM} = -\sum_t \log P(\hat{y}_t | y_{1:t-1}, x_V, x_Q)$$

Cross-entropy loss over predicted token sequences. Penalizes exact sequence mismatch even when semantic meaning is identical.

**Embedding-Space Loss (VL-JEPA)**:
$$\mathcal{L}_{VL-JEPA} = D(\hat{S}_Y, S_Y) + \lambda \cdot \text{Regularization}$$

Where:
- D(·,·): Distance metric in embedding space
- Regularization: Anti-collapse mechanism preventing all embeddings from collapsing to a single point

#### 2.2.2 InfoNCE Loss with Bidirectional Learning

VL-JEPA adopts **bidirectional InfoNCE loss**, decomposed into two complementary objectives:

**1. Representation Alignment** (Brings prediction and target together):
$$\mathcal{L}_{align} = -\log \frac{\exp(\text{sim}(\hat{S}_Y, S_Y) / \tau)}{\sum_{i=1}^{N} \exp(\text{sim}(\hat{S}_Y, S_{Y,i}) / \tau)}$$

Where sim(·,·) is cosine similarity, τ is temperature[A17], and {S_{Y,i}} are target embeddings in batch.

**2. Uniformity Regularization** (Pushes different embeddings apart):
$$\mathcal{L}_{uniform} = -\mathbb{E}_{i,j \sim \text{batch}} \log \left(\frac{\exp(\text{sim}(S_{Y,i}, S_{Y,j}) / \tau)}{N}\right)$$

Prevents representation collapse[A18] where the model learns to map all inputs to nearly identical points.

**Bidirectional Optimization**: Predictor and Y-Encoder trained jointly, enabling mutual learning. This contrasts with approaches using frozen target encoders (via EMA[A19] or parameter freezing), allowing the target representation to adapt as the predictor improves.

#### 2.2.3 Why Embedding-Space Supervision Is Superior

**Problem Formulation**: Vision-language tasks are inherently **ill-posed** (multiple valid outputs for single input). In raw one-hot token space:
- Different plausible answers are nearly orthogonal (minimal token overlap)
- Model must simultaneously fit multiple disjoint high-density regions
- Training focuses on surface-level variation rather than core semantics

**Solution in Embedding Space**:
- The Y-Encoder maps all semantically equivalent answers to nearby points
- Dense, unimodal distribution in continuous embedding space
- Learning task reduces to single-mode prediction
- Model focuses exclusively on task-relevant semantics, ignoring surface linguistic variation

**Empirical Validation**: Controlled experiments (Section 4.4) confirm that embedding-space training achieves 2× better performance than token-space training under matched conditions.

### 2.3 Multi-Task Capability

VL-JEPA's unified architecture naturally supports four distinct task types without modification:

#### 2.3.1 Vision-Text-to-Text Generation (Captioning, Open-Ended VQA)

**Workflow**:
1. Predictor generates Ŝ_Y from visual input and captioning prompt
2. Y-Decoder translates Ŝ_Y → ˆY (natural language text)
3. Suitable for image captioning, video description, open-ended visual question answering

#### 2.3.2 Open-Vocabulary Classification

**Workflow**:
1. Encode all candidate class labels {L_1, ..., L_k} into embeddings {S_{L,1}, ..., S_{L,k}} using Y-Encoder
2. Predictor generates Ŝ_Y from visual input
3. Select class with minimum cosine distance: argmin_i ||Ŝ_Y - S_{L,i}||
4. No task-specific classifier heads required

#### 2.3.3 Discriminative Visual Question Answering

**Workflow**:
1. Candidate answers {A_1, ..., A_m} pre-encoded to embeddings
2. Predictor generates Ŝ_Y from visual input and question
3. Select answer: argmin_j ||Ŝ_Y - S_{A,j}||
4. Treats VQA as nearest-neighbor matching in semantic space

#### 2.3.4 Text-to-Video Retrieval

**Workflow**:
1. Text query encoded to embedding S_Q using Y-Encoder
2. All candidate videos processed through X-Encoder + Predictor to generate embeddings
3. Videos ranked by cosine similarity to S_Q
4. Retrieval becomes efficient embedding similarity search

**Architectural Elegance**: Single model, no task-specific adaptations, unified inference pipeline.

### 2.4 Selective Decoding for Real-Time Streaming

#### 2.4.1 Problem in Classical Streaming VLMs

Traditional VLMs require autoregressive token generation, forcing models to:
- Decode continuously (expensive for long videos)
- Decode at fixed intervals (inefficient when visual content is static)
- Maintain complex memory mechanisms (KV-cache[A20] optimizations) for efficiency

#### 2.4.2 VL-JEPA's Non-Autoregressive Advantage

Because VL-JEPA predicts semantic embeddings in a single forward pass (no autoregression), it naturally produces a **continuous semantic stream** Ŝ_Y as new frames arrive. This enables **intelligent selective decoding**:

**Algorithm**:
1. Maintain sliding window of recent predicted embeddings {Ŝ_Y(t-w), ..., Ŝ_Y(t)}
2. Apply smoothing (e.g., average pooling) to stabilize embeddings: Ŝ̄_Y = mean({Ŝ_Y(t-w), ..., Ŝ_Y(t)})
3. Compute local variance: σ² = var({Ŝ_Y(t-w), ..., Ŝ_Y(t)})
4. Decode when significant semantic shift detected: **if σ² > threshold, invoke Y-Decoder**
5. Output text description only when scene semantically changes

**Intuition**: Analogous to a professional transcriber at a lengthy meeting—constantly monitoring conversation meaning, only producing text when substantively new information emerges.

#### 2.4.3 Efficiency Gains

**Empirical Result** (EgoExo4D procedural video benchmark, ~6 min videos, ~143 action annotations):
- Uniform decoding at 1 Hz: baseline decoding cost
- Selective decoding: achieves **2.85× fewer decoding operations** while maintaining identical average CIDEr[A21] scores
- Practical implication: For 1-hour video stream, selective decoding requires ~1,264 decode operations vs. 3,600 uniform operations

**Real-World Applications**:
- Smart glasses: Always-on semantic monitoring without continuous language generation
- Robotics: Real-time action tracking with minimal latency
- Live video analysis: Efficient procedural action understanding for activity recognition

---

## 3. Implementation Details

### 3.1 Model Configuration

| Component | Model | Parameters | Status | Role |
|-----------|-------|-----------|--------|------|
| X-Encoder | V-JEPA 2 ViT-L | 304M | Frozen | Visual feature extraction |
| Predictor | Llama-3.2-1B (layers 8-16) | 490M | Trainable | Core learning module |
| Y-Encoder | EmbeddingGemma-300M | 300M | Trainable (×0.05 LR) | Target embedding |
| Y-Decoder | Custom lightweight decoder | ~100M | Frozen during training | Text generation (inference-only) |
| **Total Trainable** | — | **~1.6B** | — | — |

### 3.2 Two-Stage Training Protocol

#### 3.2.1 Stage 1: Large-Scale Pretraining (Query-Free)

**Objective**: Establish robust vision-language alignment without task-specific queries.

**Data Composition**:
- **Image-text**: PLM-Image-Auto, Datacomp, YFCC-100M
- **Video-text**: PLM-Video-Auto, Ego4D atomic action descriptions, Action100M (captions on HowTo100M)
- **Total Scale**: ~2 billion image/video samples

**Training Schedule**:
1. **Phase 1A - Image-Only** (100k iterations):
   - Single frame per sample (larger batch size viable)
   - Batch size: 24,000
   - Samples seen: 2B
   - Learning rate: 5×10⁻⁵ (constant)
   - **Checkpoint Result**: 61.6% ImageNet-1k zero-shot accuracy (no prompt ensembling)

2. **Phase 1B - Joint Image-Video** (subsequent iterations):
   - 16 frames per video sample
   - Batch size: 24,000
   - Continued constant learning rate
   - **Hardware**: 24 nodes × 8 NVIDIA H200 GPUs
   - **Wall-clock Time**: ~2 weeks
   - **Model Checkpoint**: VL-JEPA_BASE

**Output**: VL-JEPA_BASE (used for zero-shot evaluation on classification and retrieval)

#### 3.2.2 Stage 2: Supervised Finetuning (Query-Conditioned)

**Objective**: Add visual question answering capabilities while preserving pretrained vision-language alignment.

**Data Composition**:
- 25M VQA samples
- 2.8M captioning samples
- 1.8M classification samples
- Downsampled pretraining data (mitigates catastrophic forgetting[A22])
- **Total Scale**: ~5 billion samples (~2 days @ batch 6k)

**Training Configuration**:
- Batch size: 6,000
- Steps: 35,000
- Learning rate: Cosine annealing[A23] from initial rate
- **Hardware**: 24 nodes × 8 NVIDIA H200 GPUs
- **Wall-clock Time**: ~2 days

**Model Checkpoint**: VL-JEPA_SFT (used for VQA evaluation and comparison with specialist models)

### 3.3 Hyperparameter Specification

| Parameter | Value | Justification |
|-----------|-------|---|
| X-Encoder learning rate | Frozen (0) | Preserve pretrained semantic features |
| Predictor learning rate | 5×10⁻⁵ | Stable training of large Transformer |
| Y-Encoder learning rate | 5×10⁻⁵ × 0.05 | Reduced multiplier prevents instability early training |
| Embedding dimension | 1,536 | Balance expressiveness and efficiency |
| Query max length | 512 tokens | Accommodate detailed questions/prompts |
| Target max length | 512 tokens | Accommodate lengthy captions |
| Temperature (InfoNCE) | (not specified in paper) | Typically 0.07-0.1; affects hardness of negatives[A24] |
| Batch normalization | Applied post-projection | Stabilize embedding space before loss calculation |

---

## 4. Experimental Validation

### 4.1 Benchmark Results: Classification and Retrieval

VL-JEPA_BASE evaluated on **8 video classification** and **8 video retrieval** datasets in zero-shot mode (no in-domain fine-tuning).

#### 4.1.1 Video Classification Results

| Dataset Category | Examples | VL-JEPA_BASE Avg | Best Baseline (PE-Core) | Performance Gap |
|---|---|---|---|---|
| **Motion-Centric** | SSv2, EK100, EgoExo4D | 16.8% avg | 9.8% avg | **+7.0%** |
| **Appearance-Centric** | Kinetics-400, COIN, CrossTask | 62.5% avg | 67.9% avg | -5.4% |
| **Overall Average** | 8 datasets | **46.4%** | 44.6% | **+1.8%** |

**Key Insight**: VL-JEPA_BASE excels on motion-heavy benchmarks (SSv2: 16.1%, EK100: 13.3%, EgoExo4D: 21.1%), indicating the architecture captures temporal dynamics effectively. Relatively weaker on appearance-centric tasks due to fewer vision-language training samples (2B vs. PE-Core's 86B).

#### 4.1.2 Text-to-Video Retrieval Results (Recall@1)

| Dataset | VL-JEPA_BASE | PE-Core | CLIP ViT-L | SigLIP2 ViT-L |
|---------|---|---|---|---|
| MSR-VTT | 37.6% | 51.6% | 41.6% | 48.9% |
| ActivityNet | 55.4% | 49.1% | 32.7% | 41.7% |
| DiDeMo | 49.2% | 44.5% | 35.1% | 40.8% |
| MSVD | 47.9% | 58.7% | 53.5% | 56.2% |
| **Average (8 datasets)** | **58.4%** | 58.1% | 45.4% | 50.2% |

**Key Insight**: VL-JEPA_BASE achieves parity or superiority to PE-Core (largest baseline) despite training on 43× fewer samples, indicating exceptional sample efficiency[A16].

#### 4.1.3 Post-Finetuning Performance (VL-JEPA_SFT)

After supervised finetuning on in-domain data:
- **Classification average**: 70.6% (approaches specialist model SoTA of 77.5%)
- **Retrieval average**: Improved (specific values shown in Table 1 of paper)
- **Status**: Single generalist model approaching performance of individually-optimized specialist models

### 4.2 Visual Question Answering Benchmarks

#### 4.2.1 Benchmark Descriptions

| Benchmark | Purpose | Metric | Difficulty |
|-----------|---------|--------|------------|
| **GQA** | Compositional visual reasoning on real images | Accuracy | Balanced splits require understanding relationships, attributes |
| **TallyQA** | Complex object counting in images | Weighted accuracy | Counts of 1-100+ objects |
| **POPE** | Object hallucination detection (MS-COCO) | Accuracy across random/popular/adversarial | Detects false object predictions |
| **POPEv2** | Extended hallucination detection | Accuracy | Improved benchmark with refined annotations |

#### 4.2.2 VL-JEPA_SFT Results

| Benchmark | VL-JEPA_SFT | InstructBLIP | QwenVL | Performance vs. Baselines |
|-----------|---|---|---|---|
| **GQA** | 60.8% | 49.5% (Vicuna-13B) | 59.3% (7B) | Competitive; outperforms smaller InstructBLIP |
| **TallyQA** | 67.4% | 68.0% (Vicuna-13B) | 65.8% (3B) | Slightly below but close |
| **POPE** | 84.2% | 79.0% (Vicuna-13B) | ~80% | **Strong hallucination detection** |
| **POPEv2** | 82.2% | 83.8% (SmolVLM-500M) | ~87% (2B) | Competitive, fewer parameters |

**Critical Context**: VL-JEPA_SFT uses **1.6B parameters total**, while many baselines employ multi-stage instruction tuning on 7B–13B backbone language models. Despite significant parameter reduction, VL-JEPA_SFT achieves **comparable or superior performance**.

### 4.3 World Modeling: Inverse Dynamics Task

#### 4.3.1 WorldPrediction-WM Benchmark

**Task Description**: Given two images representing initial state (e.g., closed door) and final state (e.g., open door), select the action from four video clip candidates that explains the state transition.

**Significance**: Tests whether model learns causal relationships and can reason about how actions transform world states—a proxy for world model[A25] understanding.

#### 4.3.2 Results (Top-1 Accuracy)

| Model Category | Model | Size | Accuracy |
|---|---|---|---|
| **Vision-Language Models** | InternVL2 | 26B | 29.8% |
| | Qwen2.5-VL | 72B | 63.9% |
| **Socratic LLMs** (captioning-based) | GPT-4o | ~400B | 53.3% |
| | Claude-3.5-Sonnet | ~400B | 55.6% |
| | Gemini-2.0 | ~400B | (not listed separately) |
| **VL-JEPA** | VL-JEPA_BASE | 1.6B | 63.9% |
| | **VL-JEPA_SFT** | **1.6B** | **65.7%** ← **New SoTA** |

**Critical Finding**: VL-JEPA_SFT (1.6B parameters) **outperforms frontier language models** (GPT-4o, Claude-3.5, Gemini-2.0 with 100–400B parameters) despite being ~100× smaller.

**Interpretation**: 
- Frontier LLMs use captioning-based reasoning (describe scene → reason over text)
- VL-JEPA predicts semantics directly without intermediate language
- Direct latent prediction produces more robust world models than textual narration-based reasoning
- Suggests embedding-space reasoning captures causal dynamics more effectively than linguistic reasoning

### 4.4 Controlled Comparison: Embedding Prediction vs. Token Prediction

#### 4.4.1 Experimental Design

**Critical Constraint**: All variables held constant except prediction target:

| Aspect | Configuration |
|--------|---|
| Vision Encoder | Perception Encoder ViT-L-14 (frozen) |
| Resolution | 336² (no tiling) |
| Frame Rate | 16 frames per video |
| Training Data | Identical pretraining mixture |
| Batch Size | 128 effective |
| Learning Rate Schedule | Identical |
| Training Iterations | Same steps, same data throughput |
| **Key Difference** | VL-JEPA: 490M predictor → embeddings; VLM: 1B LLM → tokens |

#### 4.4.2 Results

**Video Captioning (CIDEr, averaged over YouCook2, MSR-VTT, PVD-Bench):**

| Training Stage | Samples Seen | VL-JEPA | Token-VLM | Δ |
|---|---|---|---|---|
| Early | 500K | 1.23 | 1.35 | -0.12 |
| Mid | 5M | **14.7** | 7.1 | **+2.07×** |
| Late | 15M | 14.8 | 7.1 | **+2.08×** |

**Video Classification (Top-5 Accuracy, averaged over CrossTask-Step, CrossTask-Task, EgoExo4D):**

| Training Stage | Samples Seen | VL-JEPA | Token-VLM | Δ |
|---|---|---|---|---|
| Early | 500K | 14.9% | 14.0% | +0.9% |
| Mid | 5M | **35.3%** | 27.2% | **+8.1%** |
| Late | 15M | 41.0% | 27.2% | **+13.8%** |

**Interpretation**:
1. **Early Training Parity**: Both approaches start similarly (token and embedding predictions both difficult initially)
2. **Rapid Divergence**: After ~1M samples, VL-JEPA learning curve steepens dramatically
3. **Persistent Gap**: At 15M samples (representing weeks of training), VL-JEPA maintains **2× performance advantage** despite using **50% fewer trainable parameters**
4. **Inference Latency**: Both models show comparable per-token latency when decoding text, but VL-JEPA's decoupling enables selective decoding (unused in token-VLM)

**Conclusion**: Embedding-space supervision is structurally superior to token-space supervision for vision-language tasks.

### 4.5 Selective Decoding Efficiency Evaluation

#### 4.5.1 Experimental Setup

**Dataset**: EgoExo4D procedural activity recognition
- Video duration: ~6 minutes average
- Annotations: ~143 action labels per video
- Task: Recover full annotation sequence while minimizing decode operations

**Baseline Strategy**: Uniform decoding at fixed intervals
**VL-JEPA Strategy**: Adaptive selection based on embedding variance

#### 4.5.2 Algorithm: Agglomerative Clustering on Embeddings

1. Collect predicted embedding stream: {Ŝ_Y(t_0), Ŝ_Y(t_1), ..., Ŝ_Y(t_T)}
2. Apply temporal smoothing: Ŝ̄_Y(t) = mean(Ŝ_Y(t-w:t))
3. Apply agglomerative hierarchical clustering[A26] with Ward linkage[A27]:
   - Similarity metric: Ward distance (minimizes within-cluster variance)
   - Constraint: Temporal connectivity (clusters must be contiguous)
   - Objective: Partition stream into semantically coherent segments
4. Select midpoint of each cluster as decoding point
5. Optional: Use average-pooled embedding within segment for robustness

#### 4.5.3 Results

| Decoding Strategy | Frequency (Hz) | Avg Interval (sec) | CIDEr Score | Relative Cost |
|---|---|---|---|---|
| **Uniform Sampling** | 1.0 | 1.0 | 28.3 | 1.0× (baseline) |
| | 0.5 | 2.0 | 27.8 | 0.5× |
| | 0.25 | 4.0 | 24.5 | 0.25× |
| **Adaptive Selection** | 0.35 | **2.85** | **28.1** | **0.35×** |
| | 0.20 | 5.0 | 27.3 | 0.20× |

**Key Metric**: Selective decoding at **0.35 Hz** achieves **parity with uniform 1 Hz** (both ≈28 CIDEr) while requiring **2.85× fewer decode operations**.

**Practical Implication**: For continuous 1-hour video monitoring:
- Uniform decoding: 3,600 decode operations
- Selective decoding: ~1,260 operations (**65% reduction**)

**Trade-offs**:
- Average pooling within segments consistently improves both strategies
- Aggressive clustering (fewer decodes) reduces latency but risks missing brief actions
- Sweet spot appears near 2–3 second intervals for procedural activities

### 4.6 Y-Encoder Quality Analysis

#### 4.6.1 Benchmarks: Hard-Negative Detection

Two challenging benchmarks test whether the Y-Encoder produces semantically sharp embeddings:

**SugarCrepe++**: Triplet-based accuracy
- Triplets: (positive_description, positive_description', negative_description)
- Task: Verify sim(positive, positive') > sim(positive, negative)
- Negatives: Created by swapping object attributes, relationships, or object identities

**VISLA**: Spatial relationship understanding
- Tests sensitivity to spatial prepositions and fine-grained scene relationships
- Distinguishes "cat on table" vs. "cat under table"

#### 4.6.2 Results

| Model | Parameters (Text) | SugarCrepe++ | VISLA | Average |
|---|---|---|---|---|
| **CLIP ViT-L** | 85M | 44.5% | 34.5% | 39.5% |
| **SigLIP2 ViT-g** | 708M | 56.5% | 40.4% | 48.5% |
| **PE-Core ViT-G** | 537M | 58.6% | 38.3% | 48.5% |
| **VL-JEPA_BASE** | 300M | **63.9%** | **42.9%** | **53.4%** |
| **VL-JEPA_SFT** | 300M | 58.4% | 39.5% | 49.0% |

**Key Finding**: 
- VL-JEPA_BASE Y-Encoder outperforms all baselines on both benchmarks
- Substantially higher than PE-Core (+5.3% SugarCrepe++, +4.6% VISLA)
- **Despite 300M parameters (58% reduction vs. PE-Core's 537M)**
- Indicates VL-JEPA jointly learning sharper, more semantically structured embeddings

**Post-SFT Degradation**: VL-JEPA_SFT shows slight decline on hard negatives, likely due to SFT data mixture containing easier examples that don't require fine-grained semantic distinctions.

### 4.7 Ablation Studies

Ablations performed on SFT stage data (5M samples, constant learning rate) to isolate component contributions.

#### 4.7.1 Pretraining Importance

| Configuration | Classification Acc. | Retrieval R@1 | VQA Acc. |
|---|---|---|---|
| With Pretraining (default) | 49.0% | 47.5% | 46.1% |
| Without Pretraining | 27.3% | 30.2% | 42.5% |
| **Δ** | **-21.7%** | **-17.3%** | **-3.6%** |

**Interpretation**: Large-scale caption pretraining is **critical for classification/retrieval**. VQA degrades less (task-specific fine-tuning mitigates). Two-stage training essential for strong zero-shot performance.

#### 4.7.2 Y-Encoder Learning Rate Multiplier

| Multiplier | Classification Δ | Retrieval Δ | VQA Δ |
|---|---|---|---|
| 0.01 | -1.7% | -2.5% | -1.5% |
| **0.05 (default)** | **0%** (baseline) | **0%** (baseline) | **0%** |
| 0.10 | -0.4% | -0.0% | +0.4% |
| 1.00 | -3.6% | -1.4% | -1.8% |

**Interpretation**: ×0.05 multiplier is optimal. Lower multiplier (0.01) slightly hurts; higher multiplier (1.00) substantially hurts stability. **Small learning rate critical** for text encoder when embedding quality is initially poor.

#### 4.7.3 Loss Function Selection

| Loss | Classification Δ | Retrieval Δ | VQA Δ |
|---|---|---|---|
| **InfoNCE (default)** | **0%** | **0%** | +0% (tied) |
| Cosine (MSE) | -6.8% | -10.1% | +2.3% |
| L1 (MAE) | -8.5% | -14.8% | -2.4% |
| L2 (Euclidean) | -9.8% | -18.6% | -0.6% |

**Interpretation**: InfoNCE loss is significantly superior for classification/retrieval. Cosine loss shows interesting trade-off (hurts classification/retrieval but helps VQA). InfoNCE's alignment + uniformity terms critical for structured embedding space.

#### 4.7.4 Predictor Architecture and Initialization

| Configuration | Classification Δ | Retrieval Δ | VQA Δ |
|---|---|---|---|
| **Layers 8-16 (default)** | **0%** | **0%** | -1.9% |
| Layers 0-2 (early) | -3.0% | -2.4% | -2.4% |
| Layers 0-4 | -2.2% | -1.3% | +1.1% |
| Layers 0-8 | -0.1% | -0.9% | +0.9% |
| Layers 0-16 (full model) | +0.1% | +0.8% | **+3.0%** |
| Full model, bidirectional OFF | -0.6% | +1.0% | -1.9% |
| Full model, Llama-3 init OFF | +0.8% | +0.2% | -1.9% |

**Interpretation**: 
- Layers 8-16 (final 8 layers) optimal for classification/retrieval
- Using all layers (0-16) slightly helps VQA
- Llama-3 initialization provides consistent benefit (~0.8% classification)
- Bidirectional attention important for VQA (-1.9% when disabled)

#### 4.7.5 Y-Encoder Selection

| Y-Encoder Variant | Total Size | Classification Δ | Retrieval Δ | VQA Δ |
|---|---|---|---|---|
| **EmbeddingGemma-300M (default)** | 1.6B | **0%** | **0%** | **0%** |
| Qwen3-Embedding-0.6B | 1.9B | +5.0% | +0.4% | -1.0% |
| Qwen3-Embedding-4B | 2.9B | +8.2% | +2.5% | -4.4% |
| Qwen3-Embedding-8B | 3.9B | +10.1% | +5.4% | -0.6% |
| PEcore-B (356M) | 1.6B | +9.9% | +10.4% | **-6.6%** |
| PEcore-L (356M) | 1.6B | +9.5% | +10.1% | +0.4% |
| **PEcore-G (539M)** | **1.8B** | **+14.4%** | **+7.9%** | **-0.7%** |

**Interpretation**: 
- Larger text encoders (Qwen, PEcore variants) substantially improve classification/retrieval
- PEcore-G provides best overall gains for classification/retrieval (+14.4%)
- VQA performance more robust to encoder choice
- Trade-off between encoder quality and model size

---

## 5. Analysis and Discussion

### 5.1 Why Embedding Prediction Outperforms Token Prediction

#### 5.1.1 Theoretical Foundation: Ill-Posed Problem Formulation

**Classical VLM Dilemma**:
- Input x (image/video) has multiple valid outputs Y = {y₁, y₂, ..., y_k}
- Example: "What happens if I flip the light switch?" → {response₁: "lamp turns off", response₂: "room darkens", response₃: "light disappears", ...}
- In discrete token space, these responses are nearly orthogonal (minimal token overlap)
- Training distribution becomes multimodal and highly scattered in sparse token space
- Model must simultaneously fit k separate, disjoint high-density regions
- Computational cost scales with number of valid responses

**VL-JEPA Solution**:
- Y-Encoder maps all responses {y₁, y₂, ..., y_k} to a single unimodal cluster in continuous embedding space
- Semantically equivalent responses → nearby embeddings
- Training distribution becomes single-mode
- Prediction becomes standard unimodal regression in dense space
- **Result**: Dramatically reduced complexity, faster convergence

#### 5.1.2 Information-Theoretic Perspective

**Token-Space Entropy**: 
- Vocabulary size V (e.g., 100K tokens)
- Average response length L (e.g., 20 tokens)
- Possible sequences: V^L (astronomically large)
- Model must distinguish between valid sequences (correct answers) and invalid sequences (wrong answers)
- Cross-entropy loss operates over sparse, high-dimensional space

**Embedding-Space Entropy**:
- Continuous embedding dimension D (e.g., 1,536)
- Meaningful responses cluster in low-dimensional manifold[A28]
- Intrinsic dimensionality substantially lower than D
- Unimodal target distribution
- Distance loss operates over dense, low-dimensional space
- **Result**: More stable gradients, faster learning

### 5.2 Sample Efficiency Analysis

**Empirical Observation** (Fig. 3, Controlled Comparison):
- VL-JEPA reaches 14.7 CIDEr after 5M samples
- Token-VLM reaches 7.1 CIDEr after 5M samples
- **2.07× performance difference at identical training cost**

**Mechanisms Contributing to Efficiency**:

1. **Reduced Target Complexity**: Learning single semantic target vs. multiple surface realizations
2. **Implicit Data Augmentation**: All paraphrases of target treated identically (no need to memorize each variant)
3. **Smaller Predictor**: 490M parameters vs. 1B LLM decoder, easier to optimize
4. **Faster Convergence**: Embedding-space gradients more stable than sparse token gradients
5. **No Decoding Overhead**: Y-Decoder not trained, focus on core prediction task

**Broader Implication**: Embedding-based learning may represent a more fundamental approach to multimodal understanding than token-based autoregression.

### 5.3 Limitations and Trade-offs

#### 5.3.1 Scenarios Where Generative Models Remain Superior

VL-JEPA's paper explicitly acknowledges that **token-generative VLMs excel at**:

1. **Multi-Step Reasoning**: Complex reasoning paths where model needs to "think out loud"
   - Example: "What objects are in the image and how do they relate?"
   - Requires intermediate reasoning steps
   - Embedding space lacks explicit reasoning "scratchpad"

2. **Tool Use and Planning**: Agent-style behavior requiring sequential decision-making
   - Tool selection, parameter binding, interaction sequences
   - Token-based models can express plans explicitly
   - Embedding-based planning remains open research question

3. **Knowledge-Heavy Tasks**: Questions requiring external knowledge bases
   - VL-JEPA untrained on general knowledge
   - Generative models can integrate knowledge through language

4. **Compositional Generalization**: Understanding novel combinations of learned concepts
   - Initial evidence suggests embeddings strong here
   - Not comprehensively evaluated

#### 5.3.2 Architectural Limitations

1. **Fixed Embedding Dimensionality**: Semantic compression into 1,536 dimensions may lose fine-grained distinctions
   - Mitigation: Evaluate on hard-negative benchmarks (SugarCrepe++/VISLA) shows resilience
   - Further analysis of failure modes needed

2. **Lack of Explicit Uncertainty**: Continuous embeddings don't easily express model uncertainty
   - Token logits naturally encode confidence (via entropy)
   - Embedding-space confidence quantification underdeveloped

3. **Grounding in Language**: Y-Decoder still required for human interpretability
   - Some tasks benefit from intermediate language representations
   - End-to-end embedding solutions remain area for future work

### 5.4 World Modeling and Causal Reasoning

**Surprising Result**: VL-JEPA_SFT surpasses GPT-4o/Claude-3.5/Gemini-2.0 on WorldPrediction-WM (inverse dynamics task).

**Hypothesis**: 
- Frontier LLMs rely on image captioning (convert image → text description)
- Then apply language-based reasoning (reason over text)
- Two-step process introduces information bottlenecks
- VL-JEPA directly predicts latent state embeddings
- Bypasses linguistic narration, preserves direct causal structure

**Implication**:
- Embedding-space representations may be more natural for world models
- Aligns with cognitive science literature on implicit world understanding
- Suggests future integration of VL-JEPA with sequential prediction architectures (e.g., predicting future embeddings conditioned on actions)

**Open Questions**:
- Can VL-JEPA's architecture extend to sequential causal prediction?
- How to architecturally support multi-step reasoning in embedding space?
- What is relationship between world models and unsupervised video prediction?

---

## 6. Conclusion

VL-JEPA represents a fundamental architectural innovation in vision-language AI, shifting the center of gravity from **token-centric autoregression** to **embedding-centric prediction**.

### 6.1 Key Achievements

1. **Demonstrated Efficiency Gains**: 50% parameter reduction, 2× faster learning, 2.85× inference speedup via selective decoding
2. **Unified Multi-Task Architecture**: Single model handles generation, classification, retrieval, VQA without task-specific modifications
3. **Strong Empirical Results**: Competitive with or superior to significantly larger models on comprehensive benchmarks
4. **Surprising Capability**: Outperforms frontier LLMs (GPT-4o, Claude-3.5) on world modeling despite being 100× smaller
5. **Architectural Clarity**: Non-autoregressive design enables intelligent selective decoding for real-time applications

### 6.2 Implications for Future Research

**Direction 1: Scaling Laws for Embedding Prediction**
- How do performance and efficiency scale with model size?
- Is embedding-space prediction fundamentally more efficient than token-space?
- What is sample-efficiency frontier compared to generative approaches?

**Direction 2: Sequential Reasoning in Latent Space**
- Can multi-step planning be performed in embedding space?
- How to implement tree-search or beam-search over embeddings?
- Can latent-space reasoning match or exceed token-based approaches?

**Direction 3: World Models and Causal Understanding**
- Extend VL-JEPA to predict future state embeddings conditioned on actions
- Evaluate on longer-horizon planning tasks (robotics, navigation)
- Combine with hierarchical world models for abstract reasoning

**Direction 4: Modality Expansion**
- Extend architecture to audio, depth, proprioception, other sensory modalities
- Joint embedding predictive architecture for multimodal fusion
- Applications in embodied AI and robotic control

**Direction 5: Human-AI Alignment**
- Use embedding space structure for interpretability
- Leverage continuous embeddings for value alignment and safety
- Investigate causal structure of learned representations

### 6.3 Practical Applications Ready Today

1. **Smart Glasses & Wearables**: Always-on semantic monitoring with minimal latency
2. **Robotics & Manipulation**: Real-time scene understanding and action selection
3. **Video Surveillance**: Efficient action recognition in long-form video streams
4. **Content Creation**: Image/video captioning with lower inference cost
5. **Information Retrieval**: Efficient text-to-video search across large databases
6. **Embodied AI**: Navigation and task planning with continuous semantic feedback

### 6.4 Final Remarks

The shift from autoregressive token generation to embedding-space prediction mirrors broader movements in AI toward latent-variable and world-modeling approaches. VL-JEPA demonstrates that this shift is not merely complementary but potentially foundational for next-generation vision-language systems.

By eliminating the costly scaffolding of sequential token generation, VL-JEPA achieves both **practical efficiency gains** and **theoretical simplification** of the vision-language problem. For practitioners building real-time systems, the selective decoding capability alone provides immediate value. For researchers, the strong performance on causal reasoning tasks suggests embedding-based representations may be more fundamental to AI understanding than previously assumed.

As the field moves beyond the LLM era, architectures like VL-JEPA will likely become increasingly central to building AI systems capable of robust, efficient understanding and interaction with the visual world.

---

## References

[1] Chen, D., Shukor, M., Moutakanni, T., et al. (2025). VL-JEPA: Joint Embedding Predictive Architecture for Vision-Language. arXiv:2512.10942

[2] Assran, M., et al. (2025). V-JEPA 2: Towards Unified Foundation Models for Self-Supervised Video Understanding. arXiv preprint.

[3] Radford, A., et al. (2021). Learning transferable models for unsupervised visual representation learning. ICML.

[4] Bardes, A., et al. (2021). VICReg: Variance-Invariance-Covariance Regularization for Self-Supervised Learning. NeurIPS.

[5] Balestriero, R., LeCun, Y. (2025). Contrastive Learning and Self-Training for Unsupervised Clustering. arXiv preprint.

[6] Bolya, D., et al. (2025). Perception Encoder for Zero-Shot Transfer. arXiv preprint.

[7] LeCun, Y. (2022). A path towards autonomous machine intelligence. OpenReview.net.

[8] Vera, S., et al. (2025). EmbeddingGemma: Fast and Efficient Text Embedding Models. arXiv preprint.

---

## Appendix: AI Terminology Reference

[A1] **Autoregressive Generation**
A sequence generation process where each new token is predicted conditioned on all previously generated tokens. Like reading left-to-right, each word depends on all prior words. Inherently sequential and computationally slow for long outputs. Contrast: non-autoregressive approaches predict entire sequences in parallel.

[A2] **Semantic Embeddings**
Continuous vector representations that encode meaning of text, images, or other data. Unlike discrete tokens (one-hot vectors), embeddings are dense vectors where proximity reflects semantic similarity. Semantically similar concepts map to nearby points in embedding space.

[A3] **Latent Space**
Abstract, lower-dimensional representation of data learned by neural networks. Latent space typically encodes meaningful features and structure of data. Contrasts with "data space" (original pixel/token space). Latent variables often capture essential information while discarding noise.

[A4] **Vision-Language Models (VLMs)**
Neural networks trained to understand both images/videos and text. Process visual input (images or video frames) and textual queries to generate text outputs or perform classification/retrieval. Examples: CLIP, InstructBLIP, Qwen-VL. Typically use vision encoder + language decoder architecture.

[A5] **Cross-Entropy Loss**
Standard loss function for classification and token prediction. For token prediction: measures how well predicted token probability distribution matches one-hot target distribution. Low loss when model assigns high probability to correct token. Used in nearly all autoregressive language models.

[A6] **Orthogonal**
In geometry: perpendicular (right angles). In linear algebra: vectors are orthogonal if dot product is zero. Two orthogonal vectors share no similarity. Used metaphorically in this paper: different token sequences often share minimal overlap, making them nearly orthogonal in token space.

[A7] **Selective Decoding**
Strategy where expensive decoding operations (token-to-text conversion) only occur when necessary (e.g., when semantic content changes significantly), rather than at every timestep. Reduces computational cost for streaming applications while maintaining output quality.

[A8] **Language Decoder**
Neural network module that converts hidden representations (embeddings) into predicted text tokens. Typically uses autoregressive transformer layers. Large language model decoders (e.g., 1B parameters) can be computationally expensive to train and run.

[A9] **Predictor**
Core neural network module in VL-JEPA that learns to map visual embeddings and text queries to predicted semantic embeddings. Acts as the "brain" of the system where learning occurs. Initialized from transformer layers of pretrained language models for efficiency.

[A10] **Visual Embeddings**
Continuous vector representations of image/video content produced by vision encoders. Unlike pixels (raw data), embeddings capture high-level visual concepts. Sequence of visual embeddings is analogous to "visual tokens" in classical VLMs but represented as dense vectors.

[A11] **Text Decoding**
Process of converting semantic embeddings back into human-readable text. In VL-JEPA, performed by lightweight Y-Decoder at inference time. Computationally expensive, so VL-JEPA's selective decoding only decodes when semantically necessary.

[A12] **Non-Generative Models**
Models that don't generate new tokens autoregressively. Instead of predicting next token sequentially, non-generative models predict end states, embeddings, or classifications directly. More efficient but sometimes less flexible for tasks requiring explicit reasoning or knowledge integration.

[A13] **V-JEPA 2**
Video-based Joint Embedding Predictive Architecture, version 2. Self-supervised vision model trained to predict representations of video content. Produces robust semantic visual features without supervised labels. Used as frozen encoder in VL-JEPA.

[A14] **Self-Supervised Learning**
Training approach where models learn from unlabeled data by constructing supervision signal from data itself (e.g., predicting missing parts of images). No human annotation required. Enables learning from large unlabeled datasets.

[A15] **Causal Masking**
Attention mechanism modification preventing tokens from attending to future tokens (positions that come later). Used in language models to maintain causality (output token only depends on prior input). VL-JEPA disables causal masking to allow vision and text to freely interact.

[A16] **Sample Efficiency**
Measure of how quickly models learn from training data. Sample-efficient models achieve good performance with fewer training examples. VL-JEPA demonstrates ~2× better sample efficiency than token-based VLMs (reaches target performance using 50% of samples).

[A17] **Temperature**
Hyperparameter in softmax function controlling sharpness of probability distributions. High temperature: soft probabilities (nearly uniform). Low temperature: sharp probabilities (concentrated on maximum). In contrastive learning, controls how "hard" negative examples are.

[A18] **Representation Collapse**
Pathological state where neural network learns to map all inputs to nearly identical representations, losing discriminative information. Prevents learning meaningful distinctions. Anti-collapse mechanisms (e.g., uniformity regularization in InfoNCE) prevent this failure mode.

[A19] **Exponential Moving Average (EMA)**
Technique maintaining slowly-updated copy of network parameters using weighted average. Formula: θ_EMA ← τ × θ_EMA + (1-τ) × θ_current. Used in contrastive learning to stabilize target representations while allowing predictor to improve.

[A20] **KV-Cache**
Optimization technique for autoregressive decoding. Caches Key and Value matrices from previous attention steps to avoid recomputation. Reduces latency during token-by-token generation but requires memory. Complex to maintain and optimize.

[A21] **CIDEr Score**
Metric for evaluating image/video captioning quality. Based on consensus similarity between generated captions and human reference captions. Ranges 0-10, higher is better. Specifically measures consensus of n-grams in image descriptions.

[A22] **Catastrophic Forgetting**
Phenomenon where neural networks trained sequentially on new tasks "forget" previously learned tasks. When VL-JEPA fine-tunes on VQA data, model risks losing strong zero-shot classification performance. Mitigated by including downsampled pretraining data in SFT mixture.

[A23] **Cosine Annealing**
Learning rate scheduling strategy where learning rate follows cosine curve, smoothly decreasing from initial value to near-zero. Contrasts with fixed learning rate or linear decay. Often improves convergence for deep networks.

[A24] **Hardness of Negatives**
In contrastive learning, difficulty of negative examples. Hard negatives are similar to positive (confusing for model). Temperature controls which negatives are "hard"—low temperature emphasizes hard negatives, high temperature softens them. Affects gradient magnitudes during training.

[A25] **World Model**
Neural network that learns to predict future sensory observations conditioned on actions, implicitly understanding object physics and causal dynamics. Acts as internal simulator of environment. Enables planning and reasoning without explicit language.

[A26] **Agglomerative Clustering**
Bottom-up hierarchical clustering algorithm. Starts with each point in own cluster, iteratively merges closest clusters until convergence. In VL-JEPA's selective decoding: clusters embedding stream into semantically coherent segments based on temporal proximity and embedding distance.

[A27] **Ward Linkage**
Agglomerative clustering criterion minimizing within-cluster variance. When merging two clusters, selects merge that increases within-cluster variance least. Produces compact, balanced clusters. Appropriate for VL-JEPA's selective decoding to segment coherent semantic regions.

[A28] **Manifold**
In mathematics: smooth geometric structure (generalization of curves/surfaces). Manifold hypothesis: high-dimensional data often lies on low-dimensional manifold. In neural networks: learned representations often lie on low-dimensional manifold even if embedding space is high-dimensional. Explains why continuous embeddings can be effective.

---

## Document Information

**Document Type**: Technical White Paper
**Target Audience**: ML researchers, AI engineers, practitioners
**Reading Time**: ~45 minutes
**Depth Level**: Advanced (assumes familiarity with transformers, attention mechanisms, vision-language models)
**Last Updated**: January 2026
**Citation Format**: Chen et al. (2025). VL-JEPA: Joint Embedding Predictive Architecture for Vision-Language. arXiv:2512.10942