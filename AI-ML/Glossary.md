
### Core Concepts

**Token**
A small piece of text (word or part of a word) that the model processes. Examples: "Hello" → 1 token, "understand" → might be 2 tokens ("under" + "stand").

**Token Embedding**
A numeric vector that represents a token so the model can work with text mathematically. Converts words into lists of numbers like [0.23, -0.45, 0.89...].

**Embedding Vector**
A list of numbers (typically 512-4096 values) that captures the meaning and relationships of a word or token in multi-dimensional space.

**Vector Norm (Magnitude)**
The "size" or "length" of a vector, calculated as the square root of the sum of squared values. Represents signal strength.

### Architecture Components

**Transformer**
A neural network architecture used in modern language models (GPT, Llama) that processes tokens using attention and feed-forward layers.

**Transformer Layer**
One repeated block inside a transformer model that refines token representations step by step. Large models have 60-100+ layers.

**Transformer Block**
Same as transformer layer - the complete unit containing attention, feed-forward network, and normalization components.

**Attention (Self-Attention)**
A mechanism that lets the model decide which other tokens in the sequence are important when processing the current token. Like reading "bank" and checking if previous words mentioned "river" or "money."

**Feed Forward Network (FFN)**
A neural network block that processes each token independently to transform its representation. Operates pointwise on embedding values.

**Layer Normalization**
A technique that keeps values well-scaled across features so training stays stable and efficient. Prevents any single feature from dominating.

**RMS Normalization (Root Mean Square)**
A specific normalization method that scales values based on their root-mean-square magnitude. Used in mHC to ensure mixing depends only on relative features.

### Connection Types

**Residual Connection**
A shortcut that adds a layer's input directly to its output (x + f(x)), helping deep models train reliably by creating information highways.

**Skip Connection**
Another name for residual connection - a path that "skips" over a layer to carry information directly.

**Identity Mapping**
A behavior where a layer simply passes its input forward unchanged (output = input). Critical for training deep networks.

**Identity Function**
The mathematical function f(x) = x that returns its input unchanged.

**Hyper-Connections (HC)**
An architecture that splits data into multiple parallel streams and mixes them using learnable matrices. More expressive than single residual connections but unstable.

**Manifold-Constrained Hyper-Connections (mHC)**
A stabilized version of hyper-connections that mathematically limits how signals can mix and grow using doubly stochastic constraints.

### Stream Architecture

**Streams (Communication Channels)**
Parallel pathways through which information flows inside a model layer. mHC typically uses 4 streams per token instead of 1.

**Multi-Stream Architecture**
A design where data flows through multiple parallel paths simultaneously, enabling richer information processing.

**H_pre (Read Matrix / Pre-Processing Matrix)**
A learnable matrix that merges multiple streams into one before processing. Size: (n_streams → 1). Uses sigmoid activation in mHC.

**H_post (Write Matrix / Post-Processing Matrix)**
A learnable matrix that splits processed information back into multiple streams. Size: (1 → n_streams). Uses sigmoid activation in mHC.

**H_res (Residual Mixing Matrix)**
A matrix that mixes streams along the residual (skip) path. In mHC, this is constrained to be doubly stochastic using Sinkhorn-Knopp algorithm.

### Training Concepts

**Parameter**
A learnable value (weight or bias) inside the model that gets updated during training. A 27B model has 27 billion parameters.

**Gradient**
The signal used during training to tell the model how to change its parameters to reduce errors. Calculated via backpropagation.

**Gradient Flow**
How gradients travel backward through the network during training. Good flow means training is stable.

**Gradient Explosion**
When gradients grow extremely large during training (e.g., 10^100), causing numerical errors and training failure. The main problem with original hyper-connections.

**Gradient Vanishing**
The opposite problem where gradients become too small (near zero), preventing learning in deep networks.

**Backpropagation**
The algorithm that calculates gradients by working backward through the network from output to input.

**Forward Pass**
The process of sending input data through the model to produce an output. Goes from input → layers → output.

**Backward Pass**
The process of calculating gradients by working backward through the model. Used during training.

### Stability Issues

**Signal Amplification**
How much the magnitude of values grows as they pass through layers. Safe: 1.0-1.6x. Dangerous: 3000x (explosion).

**Signal Gain**
Same as signal amplification - the multiplicative factor by which signal strength increases.

**Signal Explosion**
When signal magnitude grows exponentially through layers, leading to numerical overflow and training collapse.

**Training Collapse**
When a model's training suddenly fails, producing NaN values and making further training impossible.

**Loss Spike**
A sudden jump in the training loss value, indicating instability. Common in hyper-connections, rare in mHC.

**NaN (Not a Number)**
A numerical error value that appears when calculations overflow (e.g., dividing by zero, infinite values). Indicates training failure.

**Training Stability**
How reliably a model can train without crashing or producing invalid values. Measured by absence of loss spikes and NaN errors.

### Mathematical Constraints

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

**Affine Transformation**
A linear transformation plus a bias: y = Wx + b. Used in neural networks.

### Algorithms

**Sinkhorn-Knopp Algorithm**
An iterative method that converts any positive matrix into a doubly stochastic one by alternating between normalizing rows and columns. Typically converges in 5-10 iterations.

**Iterative Normalization**
The process of repeatedly adjusting values until they meet desired constraints (used in Sinkhorn-Knopp).

**Convergence**
When an iterative algorithm reaches a stable solution and stops changing significantly.

**Sigmoid Function**
A mathematical function σ(x) = 1/(1+e^(-x)) that squashes any input value into the range (0, 1). Shaped like an S-curve.

**Tanh Function**
Another squashing function that outputs values in range (-1, 1). Used in original hyper-connections but not in mHC.

**ReLU (Rectified Linear Unit)**
An activation function that outputs max(0, x) - passes positive values unchanged, zeros out negatives.

### Optimization Techniques

**Activation Recomputation (Gradient Checkpointing)**
A memory-saving trick where intermediate results are deleted after the forward pass and recomputed during backpropagation. Trades compute for memory.

**Fused Kernel**
A GPU optimization that combines multiple operations into one for speed and efficiency. Reduces memory transfers between operations.

**Memory Footprint**
The amount of RAM/GPU memory a model requires to train or run.

**Initialization**
How model parameters are set before training starts. Critical for stability - mHC uses 2×sigmoid(0) = 1.0 to start as identity.

**Initialization Strategy**
The specific method chosen to set initial parameter values (e.g., Xavier, He, or mHC's identity-preserving approach).

### Performance Metrics

**Inference**
Using a trained model to generate outputs without updating its parameters. The "production" use of a model.

**Training Time**
How long it takes to train a model from scratch, typically measured in GPU-hours or days.

**Computational Overhead**
Extra computation required by an optimization. mHC adds ~6.7% overhead compared to standard residual networks.

**Throughput**
How many tokens or samples a model can process per second.

**Latency**
The time delay between input and output during inference.

### Model Properties

**Expressivity**
How complex and rich the representations a model can learn. More expressive models can capture more nuanced patterns.

**Capacity**
The total amount of information a model can store and process. Related to parameter count and architecture.

**Representation**
The internal numerical encoding a model creates for input data. Higher-quality representations lead to better performance.

**Parallel Processing**
Handling multiple information paths at the same time instead of sequentially. Enables richer reasoning.

**Multi-Path Reasoning**
The ability to process different aspects of information through separate pathways simultaneously.

### Scaling Concepts

**Scaling**
Increasing model size, depth (layers), width (hidden dimensions), or information pathways to improve performance.

**Depth**
The number of layers in a neural network. Deeper networks can learn more complex functions.

**Width**
The size of hidden dimensions (embedding size, FFN size). Wider networks can represent more information per layer.

**Model Size**
Total number of parameters, typically measured in millions (M) or billions (B). Example: 27B = 27 billion parameters.

**27B Parameter Model**
A very large neural network with 27 billion learnable parameters. Used in DeepSeek's mHC experiments.

### Evaluation Benchmarks

**MMLU (Massive Multitask Language Understanding)**
A benchmark testing general knowledge across 57 subjects like math, history, science, and law.

**BBH (Big-Bench Hard)**
A challenging benchmark focusing on complex reasoning tasks that require multi-step thinking.

**DROP (Discrete Reasoning Over Paragraphs)**
A reading comprehension benchmark requiring numerical reasoning and multi-hop inference.

**GSM8K (Grade School Math 8K)**
A dataset of 8,500 grade school math word problems requiring multi-step arithmetic reasoning.

**Reasoning Tasks**
Benchmarks that test multi-step thinking, logic, and understanding rather than simple memorization or pattern matching.

**Benchmark**
A standardized test used to compare model performance objectively.

### Technical Terms

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

**Pointwise Operation**
An operation applied independently to each element or position. No mixing between positions.

**Contextual Processing**
Processing that takes surrounding information into account (e.g., attention looking at previous tokens).

**Feature**
An individual dimension in an embedding vector. A 512-dimensional embedding has 512 features.

**Hidden Dimension**
The size of internal representations in a layer. Typically 2048-8192 in large models.

**Production Ready**
Software that is stable, tested, and reliable enough for real-world deployment.

**Battle-Tested**
An architecture that has been proven reliable through extensive real-world use.