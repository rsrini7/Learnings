# Complete AI/ML Technical Glossary

## 1. Foundational Concepts

**Token**
A small piece of text (word or part of a word) that the model processes. Examples: "Hello" → 1 token, "understand" → might be 2 tokens ("under" + "stand").

**Token Embedding**
A numeric vector that represents a token so the model can work with text mathematically. Converts words into lists of numbers like [0.23, -0.45, 0.89...].

**Embedding Vector**
A list of numbers (typically 512-4096 values) that captures the meaning and relationships of a word or token in multi-dimensional space.

**Latent Space**
Compressed, abstract representation of data where similar concepts are positioned close together (e.g., "ball moving right" instead of raw pixels).

**Feature**
An individual dimension in an embedding vector. A 512-dimensional embedding has 512 features.

**Hidden Dimension**
The size of internal representations in a layer. Typically 2048-8192 in large models.

**Parameter**
A learnable value (weight or bias) inside the model that gets updated during training. A 27B model has 27 billion parameters.

**Vector Norm (Magnitude)**
The "size" or "length" of a vector, calculated as the square root of the sum of squared values. Represents signal strength.

---

## 2. Transformer Architecture

**Transformer**
A neural network architecture used in modern language models (GPT, LLaMA, Claude) that processes tokens using attention and feed-forward layers.

**Transformer Layer / Block**
One repeated block inside a transformer model that refines token representations step by step. Large models have 60-100+ layers.

**Attention (Self-Attention)**
A mechanism that lets the model decide which other tokens in the sequence are important when processing the current token. Like reading "bank" and checking if previous words mentioned "river" or "money."

**Attention Complexity (O(n²))**
The quadratic scaling of self-attention with respect to context length, imposing fundamental computational limits.

**KV Cache**
Cached Key and Value vectors from attention mechanism to avoid recomputation during generation.

**Feed Forward Network (FFN)**
A neural network block that processes each token independently to transform its representation. Operates pointwise on embedding values.

**Residual Connection / Skip Connection**
A shortcut that adds a layer's input directly to its output (x + f(x)), helping deep models train reliably by creating information highways.

**Layer Normalization**
A technique that keeps values well-scaled across features so training stays stable and efficient. Prevents any single feature from dominating.

**RMS Normalization (Root Mean Square)**
A specific normalization method that scales values based on their root-mean-square magnitude. Used in mHC to ensure mixing depends only on relative features.

---

## 3. Advanced Architectures

### Hyper-Connections & Multi-Stream

**Hyper-Connections (HC)**
An architecture that splits data into multiple parallel streams and mixes them using learnable matrices. More expressive than single residual connections but unstable.

**Manifold-Constrained Hyper-Connections (mHC)**
A stabilized version of hyper-connections that mathematically limits how signals can mix and grow using doubly stochastic constraints.

**Streams (Communication Channels)**
Parallel pathways through which information flows inside a model layer. mHC typically uses 4 streams per token instead of 1.

**Multi-Stream Architecture**
A design where data flows through multiple parallel paths simultaneously, enabling richer information processing.

**H_pre (Read Matrix)**
A learnable matrix that merges multiple streams into one before processing. Size: (n_streams → 1). Uses sigmoid activation in mHC.

**H_post (Write Matrix)**
A learnable matrix that splits processed information back into multiple streams. Size: (1 → n_streams). Uses sigmoid activation in mHC.

**H_res (Residual Mixing Matrix)**
A matrix that mixes streams along the residual (skip) path. In mHC, this is constrained to be doubly stochastic using Sinkhorn-Knopp algorithm.

### State Space Models

**SSM (State Space Model)**
Mathematical framework for sequence modeling with linear-time complexity, offering an alternative to quadratic attention mechanisms.

### Predictive Architectures

**JEPA (Joint Embedding Predictive Architecture)**
Learning framework that predicts abstract representations instead of raw data, enabling efficient world modeling.

**World Model**
AI system that simulates how environments evolve over time (physics, dynamics, causality).

---

## 4. Training Concepts

**Gradient**
The signal used during training to tell the model how to change its parameters to reduce errors. Calculated via backpropagation.

**Backpropagation**
The algorithm that calculates gradients by working backward through the network from output to input.

**Forward Pass**
The process of sending input data through the model to produce an output. Goes from input → layers → output.

**Backward Pass**
The process of calculating gradients by working backward through the model. Used during training.

**Gradient Flow**
How gradients travel backward through the network during training. Good flow means training is stable.

**Gradient Explosion**
When gradients grow extremely large during training (e.g., 10^100), causing numerical errors and training failure.

**Gradient Vanishing**
When gradients become too small (near zero), preventing learning in deep networks.

**Stop-Gradient**
Training technique that freezes part of a network to prevent trivial solutions.

**Teacher Forcing**
Training technique where the model is shown the correct token at each step.

**Knowledge Distillation**
Training a smaller model to mimic a larger model's behavior.

---

## 5. Stability & Initialization

**Training Stability**
How reliably a model can train without crashing or producing invalid values. Measured by absence of loss spikes and NaN errors.

**Training Collapse**
When a model's training suddenly fails, producing NaN values and making further training impossible.

**Loss Spike**
A sudden jump in the training loss value, indicating instability. Common in hyper-connections, rare in mHC.

**NaN (Not a Number)**
A numerical error value that appears when calculations overflow (e.g., dividing by zero, infinite values). Indicates training failure.

**Signal Amplification / Gain**
How much the magnitude of values grows as they pass through layers. Safe: 1.0-1.6x. Dangerous: 3000x (explosion).

**Signal Explosion**
When signal magnitude grows exponentially through layers, leading to numerical overflow and training collapse.

**Initialization**
How model parameters are set before training starts. Critical for stability - mHC uses 2×sigmoid(0) = 1.0 to start as identity.

**Identity Mapping / Function**
A behavior where a layer simply passes its input forward unchanged (output = input). The function f(x) = x.

---

## 6. Mathematical Constraints & Algorithms

**Doubly Stochastic Matrix**
A matrix where: (1) all values are non-negative, (2) every row sums to 1, (3) every column sums to 1. Ensures stable, bounded mixing.

**Birkhoff Polytope**
The mathematical space (set) of all doubly stochastic matrices. A geometric shape in high-dimensional space.

**Conservation Constraint**
The principle that the total amount of signal must be preserved - no creating or destroying information during mixing.

**Row Sum Constraint**
The requirement that all values in each row of a matrix must add up to exactly 1.0.

**Column Sum Constraint**
The requirement that all values in each column of a matrix must add up to exactly 1.0.

**Weighted Average**
A combination where inputs are multiplied by weights that sum to 1. Output cannot exceed largest input when using non-negative weights.

**Sinkhorn-Knopp Algorithm**
An iterative method that converts any positive matrix into a doubly stochastic one by alternating between normalizing rows and columns. Typically converges in 5-10 iterations.

**Iterative Normalization**
The process of repeatedly adjusting values until they meet desired constraints (used in Sinkhorn-Knopp).

**Convergence**
When an iterative algorithm reaches a stable solution and stops changing significantly.

---

## 7. Activation Functions

**Sigmoid Function**
A mathematical function σ(x) = 1/(1+e^(-x)) that squashes any input value into the range (0, 1). Shaped like an S-curve.

**Tanh Function**
Another squashing function that outputs values in range (-1, 1). Used in original hyper-connections but not in mHC.

**ReLU (Rectified Linear Unit)**
An activation function that outputs max(0, x) - passes positive values unchanged, zeros out negatives.

---

## 8. Generation & Inference

### Generation Modes

**Auto-regression (AR)**
Generating text one token at a time, where each token depends on all previous tokens.

**Non-Autoregressive (NAR)**
Generating all tokens simultaneously in parallel.

**Speculative Decoding**
Using a draft model to predict multiple tokens, then verifying with the target model.

**Action Chunking**
Predicting multiple future actions at once, then overlapping predictions for smooth motion (robotics).

### Inference Phases

**Prefill Phase**
Initial prompt processing where all tokens are processed in parallel. Compute-bound.

**Decode Phase**
Autoregressive token generation, one token at a time. Memory-bound.

**Inference**
Using a trained model to generate outputs without updating its parameters. The "production" use of a model.

### Inference Challenges

**Exposure Bias**
The mismatch between training (using correct tokens) and inference (using model's own predictions).

**Context Window Limit**
The maximum number of tokens a model can attend to simultaneously. Increasing this alone does not solve context rot.

**Context Rot**
The degradation of reasoning accuracy as context length increases, especially for complex reasoning tasks. Even when models technically support long contexts, their reasoning reliability collapses beyond a threshold.

---

## 9. Optimization & Efficiency

**Activation Recomputation (Gradient Checkpointing)**
A memory-saving trick where intermediate results are deleted after the forward pass and recomputed during backpropagation. Trades compute for memory.

**Fused Kernel**
A GPU optimization that combines multiple operations into one for speed and efficiency. Reduces memory transfers between operations.

**Quantization**
Reducing numerical precision (FP16 → INT8 → INT4) to save memory and increase throughput.

**Tensor Parallelism**
Sharding model layers across multiple GPUs for parallel execution.

**PagedAttention**
Memory management technique applying OS virtual memory paging to KV cache.

**Continuous Batching**
Dynamic batching strategy that adds/removes requests at the token level rather than waiting for entire batch completion.

**Arithmetic Intensity**
Ratio of FLOPs to memory access (operations/byte). High = compute-bound, Low = memory-bound.

---

## 10. Performance Metrics

**Throughput**
How many tokens or samples a model can process per second.

**Latency**
The time delay between input and output during inference.

**Training Time**
How long it takes to train a model from scratch, typically measured in GPU-hours or days.

**Computational Overhead**
Extra computation required by an optimization. mHC adds ~6.7% overhead compared to standard residual networks.

**Memory Footprint**
The amount of RAM/GPU memory a model requires to train or run.

**Inference Cost per Query**
The total compute cost of running all reasoning steps, sub-calls, and aggregation for a single task.

---

## 11. Model Properties

**Expressivity**
How complex and rich the representations a model can learn. More expressive models can capture more nuanced patterns.

**Capacity**
The total amount of information a model can store and process. Related to parameter count and architecture.

**Representation**
The internal numerical encoding a model creates for input data. Higher-quality representations lead to better performance.

**Depth**
The number of layers in a neural network. Deeper networks can learn more complex functions.

**Width**
The size of hidden dimensions (embedding size, FFN size). Wider networks can represent more information per layer.

**Model Size**
Total number of parameters, typically measured in millions (M) or billions (B). Example: 27B = 27 billion parameters.

**Scaling**
Increasing model size, depth (layers), width (hidden dimensions), or information pathways to improve performance.

**Inference-Time Scaling**
Improving model performance by increasing reasoning steps, decomposition, or tool use at inference time rather than by training larger models.

---

## 12. Matrix & Operation Types

**Static Weights**
Parameters that don't depend on the input data. Fixed for all examples.

**Dynamic Weights**
Parameters that change based on input features. Computed during the forward pass.

**Learnable Matrix**
A matrix whose values are parameters that get updated during training.

**Mixing Matrix**
A matrix that combines multiple streams by computing weighted combinations.

**Matrix Multiplication**
The mathematical operation of multiplying matrices. Forms the basis of neural network computations.

**Affine Transformation**
A linear transformation plus a bias: y = Wx + b. Used in neural networks.

**Pointwise Operation**
An operation applied independently to each element or position. No mixing between positions.

**Contextual Processing**
Processing that takes surrounding information into account (e.g., attention looking at previous tokens).

---

## 13. Recursive Language Models (RLMs)

### Core RLM Concepts

**Recursive Language Model (RLM)**
An inference-time architecture where a language model repeatedly decomposes a problem into smaller subproblems, explores data programmatically, invokes sub-models, and aggregates results recursively.

**Root LLM (Orchestrator Model)**
The primary model responsible for strategy, planning, decomposition, and aggregation. Controls exploration through code.

**Sub-LLM (Worker Model)**
A secondary model invoked by the Root LLM to perform semantic reasoning on small, focused chunks.

**Externalized Context**
Storing large documents outside the model's token window (e.g., in variables, files, or memory) so the model interacts with them indirectly via code.

### RLM Strategies

**Recursive Decomposition**
Breaking a large task into smaller subtasks, which may themselves be decomposed further until each unit is tractable.

**Aggregation Step**
The deterministic process of combining results from sub-LLMs into a final answer, usually via code.

**Code-as-Control**
Using executable code to control data access, filtering, looping, and aggregation instead of relying solely on neural attention.

**Semantic Chunking**
Splitting data into chunks based on meaning or structure rather than fixed token length.

**Recursive Reasoning Loop**
A repeated cycle of: inspect → filter → chunk → analyze → aggregate → repeat.

**Programmatic Filtering**
Using deterministic rules (regex, string search, metadata checks) to narrow data before invoking semantic reasoning.

**Peek Operation**
Inspecting a small prefix of the context (e.g., first 1–2%) to infer structure without reading the entire dataset.

### RLM Environment

**Python REPL Environment**
A persistent execution environment where the model can store variables, run code, and maintain state across reasoning steps.

**Persistent State**
Variables and intermediate results that remain available across multiple reasoning iterations.

**Deterministic Coverage**
A property of RLMs where all relevant data is guaranteed to be examined, unlike probabilistic retrieval systems.

**Selective Compute**
Only spending compute on relevant portions of data rather than the entire context.

### RLM Behavior

**Over-Verification**
Excessive repeated checking of results by a model, increasing cost without proportional accuracy gains.

**Under-Exploration**
Failing to examine enough of the data, leading to missed answers.

**Model-Specific Strategy Bias**
Different models exhibit different exploration behaviors (e.g., conservative vs exhaustive) even under identical prompts.

**Unbounded Output Generation**
Producing outputs larger than the model's maximum token limit by generating and storing sections incrementally.

---

## 14. Retrieval & Long-Context Methods

**Retrieval-Augmented Generation (RAG)**
An approach where a vector database retrieves top-K relevant documents to feed into an LLM. Fast but probabilistic and lossy for exhaustive tasks.

**Top-K Retrieval**
Selecting the K most similar items based on embedding similarity. Can miss relevant items outside the top-K set.

**Context Compression / Summarization**
Reducing large inputs into smaller summaries before reasoning. Irreversible and prone to information loss.

**Lossy vs Lossless Processing**
Lossy methods (summarization, RAG) discard information; lossless methods (RLMs) retain the ability to re-examine original data.

**Hybrid RAG + RLM**
Using RAG for fast initial filtering and RLMs for deep, exhaustive reasoning on the filtered subset.

**Coverage Guarantee**
Assurance that every relevant item has been checked. RLMs provide deterministic coverage; RAG does not.

---

## 15. Computational Complexity

**Constant-Time Task (O(1))**
A task whose difficulty does not increase with input size, such as finding a single known token.

**Linear-Time Task (O(n))**
A task requiring one pass over all elements, such as classifying each document or counting occurrences.

**Quadratic-Time Task (O(n²))**
A task requiring comparison of all pairs of elements, such as finding all matching user pairs. These tasks cause catastrophic failures in standard LLMs.

**Search Space Reduction**
Reducing the number of comparisons or operations by filtering or grouping data before deeper analysis.

**Reasoning Density**
A measure of how much logical computation is required per token. High reasoning density causes failures much earlier than low-density tasks.

**Parallel Processing**
Handling multiple information paths at the same time instead of sequentially. Enables richer reasoning.

**Multi-Path Reasoning**
The ability to process different aspects of information through separate pathways simultaneously.

---

## 16. Benchmarks & Evaluation

**Benchmark**
A standardized test used to compare model performance objectively.

**MMLU (Massive Multitask Language Understanding)**
A benchmark testing general knowledge across 57 subjects like math, history, science, and law.

**BBH (Big-Bench Hard)**
A challenging benchmark focusing on complex reasoning tasks that require multi-step thinking.

**DROP (Discrete Reasoning Over Paragraphs)**
A reading comprehension benchmark requiring numerical reasoning and multi-hop inference.

**GSM8K (Grade School Math 8K)**
A dataset of 8,500 grade school math word problems requiring multi-step arithmetic reasoning.

**Long-Context Benchmark**
A benchmark designed to test reasoning over extremely large inputs (100K–10M+ tokens).

**Quadratic Reasoning Benchmark**
A benchmark that explicitly tests pairwise or combinatorial reasoning (e.g., OOLONG-Pairs).

**Reasoning Tasks**
Benchmarks that test multi-step thinking, logic, and understanding rather than simple memorization.

**Multi-Hop Reasoning**
Tasks requiring reasoning across multiple documents or steps where intermediate conclusions influence later steps.

**Zero-Shot**
Performing tasks without specific training examples (generalization from pre-training).

---

## 17. Data Processing & Compression

**BPE (Byte-Pair Encoding)**
Compression technique that merges frequently occurring token sequences.

**DCT (Discrete Cosine Transform)**
Frequency-based compression used in JPEG, effective for smooth signals.

---

## 18. Multimodal & Embodied AI

**VLM (Vision-Language Model)**
Models that process both images and text for understanding/generation.

**VLA (Vision-Language-Action)**
Models that understand images and text, then generate robot actions.

**Embodied AI**
AI integrated into physical bodies (robots, vehicles) that perceive and act in the real world.

**MPC (Model Predictive Control)**
Planning technique that searches over action sequences to minimize cost.

---

## 19. System Design & Deployment

**Production Ready**
Software that is stable, tested, and reliable enough for real-world deployment.

**Battle-Tested**
An architecture that has been proven reliable through extensive real-world use.

**RLM-to-Fine-Tuning Pipeline**
Using RLM outputs to generate high-quality training data for fine-tuned models that run faster later.

**Agentic Reasoning**
A style of reasoning where the model behaves like an agent—planning, acting, observing, and iterating.

**Latency–Accuracy Tradeoff**
RLMs trade higher latency (seconds) for dramatically higher accuracy and completeness.

---

## 20. Physical & Scaling Limits

**Physics Limit of Attention**
The practical memory and compute ceiling caused by quadratic attention growth, making very large context windows impractical.