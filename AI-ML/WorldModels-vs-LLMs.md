# World Models vs LLMs (with JEPA Family and VL‑JEPA vs Nvidia Cosmos)

World models let AI **imagine** and predict how the real world changes over time, like simulating what happens if you drop a ball (it falls due to gravity).  LLMs are not true world models—they're great at predicting the next word in text but don't natively represent physics, space, or causal dynamics of the physical world. 

---

## Simple World Model Analogy

Think of a world model like a video game engine inside an AI system.  It builds a compact internal version of reality from videos/images/sensors and then runs “what‑if” simulations: “If I push this block left, where does it roll?”  This enables robots or agents to plan safely in imagination before acting in the real world. 

---

## Why LLMs Aren’t World Models

- LLMs predict text patterns from internet-scale corpora (e.g., “rain follows clouds” as words), not grounded trajectories like water actually falling and wetting streets.
- They lack an explicit state-transition mechanism; small changes in a scenario can break their “understanding” because it is largely correlational, not a structured causal simulator of the environment.
- World models typically use multimodal data (video, 3D scenes, sensors) to learn dynamics; LLMs are text-first **statisticians**, not **simulators** of physical state.

---

## Core Differences: World Models vs LLMs

| Aspect        | World Models                                                                 | LLMs                                                                                 |
|--------------|-------------------------------------------------------------------------------|--------------------------------------------------------------------------------------|
| Predicts     | Next real-world state (e.g., object motion, scene evolution)  | Next word/token in a sequence of text or code                                |
| Data         | Videos, images, 3D scenes, robot sensors for physics and dynamics     | Massive text/code corpora, optionally images/audio as conditioning          |
| Strength     | Planning, robotics, “imagination” of futures, model predictive control  | Language tasks, chat, coding assistance, retrieval-augmented reasoning      |
| Weakness     | Needs large-scale real-world or simulated data; training is compute-heavy  | No built-in physical causality; brittle with novel real-world dynamics  |

Future systems are likely hybrids: LLMs parse language instructions, while world models handle grounded prediction and control in physical or simulated environments. 

---

## JEPA: World Models via Latent Prediction

JEPA (Joint Embedding Predictive Architecture) is Yann LeCun’s design for learning world models by predicting abstract **representations** of future data (e.g., video frames) instead of reconstructing pixels, yielding much more efficient and stable learning. 

### Intuition

Imagine watching a ball bounce in a video.  A pixel-level generative model tries to predict every pixel of the next frame, including random lighting flicker and background noise, which are fundamentally unpredictable and task-irrelevant.  JEPA instead compresses the scene into a latent summary (e.g., “ball at position X, moving right with velocity v”), and predicts the next latent (“ball lower, still moving”).  This focuses on predictable structure (dynamics, identities, motion) and ignores high-frequency noise, making scaling far easier. 

### Core Components

- **Context encoder**: Encodes the visible part of an input (image or video segment) into a latent representation capturing high-level structure. 
- **Target encoder**: Encodes the masked/hidden or future part into a target latent representation. 
- **Predictor network**: Learns to map from the context latent to the target latent, minimizing a distance (often L1) between prediction and target in representation space, with a stop‑gradient on the target encoder to avoid representation collapse. 

The key trick is the stop‑gradient on the target branch, which prevents the system from converging to trivial constant representations and forces genuine semantic structure to emerge in the encoder. 

---

## JEPA Family: I‑JEPA, V‑JEPA, VL‑JEPA

The JEPA family extends this latent prediction philosophy from images to video and then to joint vision–language reasoning. 

### I‑JEPA (Image JEPA)

- Operates on static images: masks out patches and predicts their abstract features rather than reconstructing raw pixels. 
- Removes the need for heavy, hand‑crafted data augmentations used in earlier self-supervised vision methods. 
- Produces robust high-level visual representations that transfer well to downstream tasks like classification and detection. 

### V‑JEPA and V‑JEPA 2 (Video JEPA)

- Extends JEPA to video, learning spatiotemporal dynamics by predicting representations of masked video segments from surrounding context. 
- Uses a mask‑denoising feature prediction objective: predict the representation of a masked chunk \(A\) from visible context \(X\), minimizing an L1 distance in latent space. 
- Applies stop‑gradient to the target encoder branch to avoid collapse, ensuring the predictor must match a rich, fixed target representation. 
- Architecturally built on Vision Transformers (ViTs); scaling to billion-parameter encoders required 3D rotary positional embeddings that separately encode time, height, and width to keep long video sequences stable. 
- Scaling recipe for V‑JEPA 2 includes:
  - Increasing data from about 2M to ~22M videos (plus static images treated as short clips). 
  - Scaling the encoder from ~300M to ~1B parameters while keeping the predictor small (~22M). 
  - Training for much longer (on the order of 252k iterations) to “bake in” world knowledge. 
  - Progressive higher‑resolution training: warm up at lower resolution and shorter clips, then only in the final phase ramp up resolution and clip length, yielding up to ~8.4× GPU efficiency vs full‑resolution training from scratch. 
- Achieves strong results such as ~77.3% top‑1 on Something-Something V2 for complex human motion understanding, validating the quality of the learned world representations. 

### V‑JEPA 2‑AC: Action‑Conditioned World Model for Robotics

- Takes a pretrained V‑JEPA 2 visual encoder (frozen as a “visual cortex”) and trains a separate ~300M‑parameter predictor for control. 
- Input to the predictor is an interleaved sequence of:
  - Encoded frames from the frozen visual encoder.
  - Robot state (e.g., a 7‑D end‑effector pose).
  - Candidate action vectors to be evaluated. 
- Trains with:
  - Teacher‑forcing loss: predict the next latent state given ground‑truth history. 
  - Rollout loss: repeatedly feed the model’s own predictions back in for multi‑step rollouts, and penalize divergence from ground truth at the end; this makes the model robust to compounded prediction errors in long horizons. 
- At inference, uses model predictive control (MPC) in latent space: search over action sequences that minimize an energy function defined as the L1 distance between the imagined future latent and the encoded goal latent (e.g., an image of a cleaned table). 
- Because everything runs in abstract representation space rather than pixels, V‑JEPA 2‑AC plans actions for manipulation tasks (like pick‑and‑place) with about 80% success in new environments and with roughly 15× speedup versus pixel‑generative baselines like Nvidia Cosmos (16 seconds vs ~4 minutes per action). 

### VL‑JEPA (Vision–Language JEPA)

- Combines a V‑JEPA 2 visual encoder with a text‑based predictor to build a non‑generative model for general vision–language tasks such as video question answering. 
- Crucial design choice: predicts continuous text **embeddings** (semantic representations) rather than discrete text tokens, separating semantic prediction from text generation. 
- This avoids modeling irrelevant linguistic surface details (style, exact phrasing, grammar quirks) and focuses on meaning: semantically equivalent sentences like “the lamp is turned off” and “the room will go dark” map to nearby points in embedding space, even though they are distant in token space. 
- Uses bidirectional contrastive losses (e.g., InfoNCE/E‑loss) between video and text pairs: push matched video–caption pairs together in embedding space and push mismatches apart, which also regularizes embeddings and prevents collapse. 
- With a V‑JEPA 2 backbone, VL‑JEPA attains state-of-the-art performance in the ~8B parameter regime on benchmarks like Perception Test and TempCompass, often surpassing models whose encoders were trained with explicit language supervision from the start. 
- Scaling alignment data from roughly 18M to ~90M video–text pairs further improves performance, reinforcing the idea that a strong world model baseline plus large‑scale alignment is highly effective. 

---

## JEPA Variants vs Other World Models

Several world-model families besides JEPA focus on learning environment dynamics for prediction, planning, and simulation, particularly in video, games, and robotics. 

### JEPA Family (LeCun / Meta AI)

- **I‑JEPA**: Image-based JEPA for self‑supervised vision. 
- **V‑JEPA / V‑JEPA 2**: Video-based JEPA; excels at physical reasoning, motion prediction, and zero‑shot robotics with large video corpora. 
- **LeJEPA**: A theoretical extension providing a more general non‑autoregressive predictive framework building on JEPA principles. 

### Other Leading Architectures

- **DreamerV3**: Latent world model for reinforcement learning; learns discrete/continuous latent dynamics to “imagine” trajectories, enabling sample-efficient control in domains like Atari and Minecraft. 
- **Genie 3 (Google DeepMind)**: Trains a generative world model that can produce diverse, interactive 2D environments from images and videos, useful for games and embodied AI research. 
- **GLP / PAN**: Energy-based architectures for latent dynamics and reconstruction‑free learning; often discussed alongside JEPA as alternative world-model formulations. 

### World-Model Family Comparison

| Model       | Core Focus                               | Key Strength                          | Domain                            |
|------------|-------------------------------------------|---------------------------------------|-----------------------------------|
| JEPA       | Latent embedding prediction  | Efficiency, multimodal scalability    | Images, video, robotics           |
| DreamerV3  | RL with latent world simulation   | Sample‑efficient planning             | Games (Atari, Minecraft, control) |
| Genie 3    | Generative interactive environments  | High diversity of simulated worlds   | 2D worlds, embodied agents        |
| GLP / PAN  | Energy-based latent dynamics      | Reconstruction‑free world modeling    | General interactive environments  |

---

## World Models vs Diffusion LLMs, Nested Learning, CTM, etc.

World models like JEPA explicitly learn an internal simulator of environment dynamics from multimodal data; several other buzzword concepts focus more on language reasoning, generation, or internal neuron dynamics. 

| Concept                    | Description                                                                                                       | Key Difference from World Models                                                               |
|---------------------------|-------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------|
| Diffusion LLMs            | Generate text via iterative denoising from noise into coherent sequences.                                 | Operate solely in text space; no explicit simulation of physical state transitions.   |
| Nested Learning           | Layered/meta-learning frameworks where models self-refine over time.                                      | Focus on adaptive learning strategy, not on explicit state‑to‑state dynamics for planning.     |
| Continuous Thought Machines (CTM) | Architectures where neurons track their own history and synchronization to form richer internal dynamics.  | Model internal thought trajectories; not grounded simulators of external physical worlds.      |
| Latent-Space Thinking     | Reasoning/planning in compressed latent spaces (often present inside world models themselves).            | A technique used inside many world models; not a standalone world‑model architecture.          |
| Private Chains of Thought | Hidden intermediate reasoning steps as in RL‑trained CoT for LLMs.                                       | Symbolic/linguistic step‑by‑step reasoning without explicit visual/spatial environment rollout. |

These methods can enhance LLM reasoning or efficiency but remain primarily symbolic/text‑centric, whereas world models are inherently about simulating how the **world** evolves. 

---

## VL‑JEPA vs Nvidia Cosmos (World Model vs Pixel Generator)

The podcast contrasts the JEPA family, especially V‑JEPA 2‑AC and VL‑JEPA, against pixel-generative baselines like Nvidia Cosmos. 

### Philosophical Difference

- **Cosmos and similar generative models**:
  - Must generate every pixel or token of the future, forcing the model to represent even fundamentally unpredictable details (every blade of grass, every shimmer of light). 
  - This wastes parameters and compute on noise that is irrelevant to decision-making. 
- **JEPA family (V‑JEPA / VL‑JEPA)**:
  - Only predicts abstract latent representations for the predictable components: object identities, trajectories, and coarse scene structure. 
  - Ignores high-frequency noise, making the learning objective simpler, more stable, and dramatically more scalable. 

### Practical Impact (V‑JEPA 2‑AC vs Cosmos)

- Planning a single robotic action:
  - V‑JEPA 2‑AC: approximately 16 seconds, operating in latent space. 
  - Cosmos: around 4 minutes per action, due to full pixel-level rollout of candidate futures. 
- This ~15× speed gap marks the line between a practical real-time robot and a slow, lab‑only experiment. 
- V‑JEPA 2‑AC achieves around 80% zero‑shot success on manipulation tasks in new environments, demonstrating the adequacy of abstract representation for robust control. 

### Vision–Language: VL‑JEPA vs Generative VLMs

- Traditional VLMs must generate exact text tokens for answers, requiring them to model style, phrasing, paraphrases, and grammar along with semantics. 
- VL‑JEPA instead predicts the semantic embedding of the answer:
  - Semantically equivalent answers map to nearby points even if token sequences differ widely. 
  - This greatly simplifies the learning target and improves robustness to linguistic ambiguity and paraphrasing. 
- With scaling (both in parameters and alignment data), VL‑JEPA reaches state-of-the-art in its size class on perception and temporal reasoning benchmarks, despite not being trained as a generative language model. 

---

## Big Picture: From Observation to Language-Driven Action

Putting this together:

- JEPA-based world models learn to **observe** and build internal simulators of how the world evolves, primarily from unlabeled video and image data. 
- V‑JEPA 2‑AC shows how to go from observation to **action**, using model predictive control in latent space for real-time robotics. 
- VL‑JEPA adds **language** alignment on top of learned world dynamics, enabling tasks like video QA and suggesting a path toward robots that plan complex multi-step actions given only high-level natural language goals. 
- As these models scale to tens of billions of parameters with large alignment datasets, the likely destination is AI agents that can define goals in high-level semantic space and plan efficiently in abstract latent world models instead of pixel space. 

This shifts the bottleneck from collecting task-specific labelled data to designing architectures that separate predictable signal from unpredictable noise, a central theme of the JEPA family and a key differentiator from traditional LLM-centric approaches. 


## References

- [JEPA-Models-VL-JEPA-I-JEPA-V-JEPA-Nvidia-Cosmos](../assets/JEPA-Models-VL-JEPA-I-JEPA-V-JEPA-Nvidia-Cosmos.pdf)