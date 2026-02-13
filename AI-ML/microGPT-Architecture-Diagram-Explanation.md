# microGPT Architecture — Diagram Explanation

![AI-ML/assets/microGPT-Architecture.png](assets/microGPT-Architecture.png)

This diagram visualizes the complete microGPT model — a minimal, dependency-free implementation of a GPT-style Transformer. It shows how data flows forward to produce predictions and how gradients flow backward to update parameters.

We’ll walk through it from **top to bottom (forward pass)** and then explain the **backpropagation flow**.

---

# 1️⃣ Scalar Autograd Engine (Top Section)

At the very top is the **Value Class Module**.

This is microGPT’s custom scalar automatic differentiation engine.

Each number in the model is wrapped in a `Value` object that stores:

* `data` → the numerical value
* `grad` → the gradient (∂loss/∂value)

Unlike PyTorch tensors, microGPT operates on **pure Python scalars**.
Every multiplication, addition, and activation builds a computation graph.

When training finishes a forward pass, gradients are computed using:

> Chain rule over a scalar computation graph

This is what the orange “Global Backpropagation Flow” arrow represents.

---

# 2️⃣ Input and Tokenization

The model begins with a single character input.

Example shown:

```
[BOS, e, m, m, a, BOS]
```

Important details:

* The model uses **character-level tokenization**
* There is a single special token: **BOS**
* BOS is used for both beginning and end of sequence
* Vocabulary size ≈ 27 (a–z + BOS)

Each character is converted into an integer token ID.

---

# 3️⃣ Embeddings

Two embeddings are learned:

### Token Embedding (wte)

Maps each character ID to a 16-dimensional vector.

Shape:

```
vocab_size (27) × 16
```

### Position Embedding (wpe)

Adds positional information (since Transformers have no recurrence).

Shape:

```
block_size (16) × 16
```

Both embeddings produce 16-dimensional vectors, which are:

> Added elementwise

This produces the initial representation for each token.

---

# 4️⃣ RMSNorm (Normalization)

Before entering the Transformer block, the representation is normalized using **RMSNorm**:

[
x \leftarrow \frac{x}{\sqrt{\text{mean}(x^2)} + \epsilon}
]

Important differences from GPT-2:

* No mean subtraction
* No learnable scale (γ)
* No bias (β)

This keeps the model minimal and dependency-free.

---

# 5️⃣ Transformer Block (n_layer = 1)

microGPT uses **one Transformer block** by default.

Each block has two sublayers:

---

## 5A️⃣ Multi-Head Self-Attention

There are:

* 4 heads
* head_dim = 4
* n_embd = 16

Each head computes:

[
\text{Attention}(x) = \text{softmax}\left(\frac{QK^T}{\sqrt{\text{head_dim}}}\right)V
]

### Key details:

* Q, K, V are linear projections of the input
* No bias terms
* Causality is enforced structurally

Instead of using a mask matrix, microGPT:

* Processes tokens sequentially
* Stores previous keys and values in a **growing KV cache**

This ensures tokens only attend to past tokens.

After all heads:

* Outputs are concatenated
* A linear projection maps 16 → 16

Then comes the first residual connection:

[
x \leftarrow x + \text{Attention}(x)
]

---

## 5B️⃣ MLP Block (Feedforward Network)

This is the second sublayer.

Structure:

```
Linear 1: 16 → 64
ReLU activation
Linear 2: 64 → 16
```

Expansion ratio: 4×

Important:

* Uses **ReLU**, not GeLU
* No bias terms

Then second residual connection:

[
x \leftarrow x + \text{MLP}(x)
]

---

# 6️⃣ LM Head

After the Transformer block:

A final linear layer maps:

```
16 → vocab_size (27)
```

This produces **logits** — one score per character.

---

# 7️⃣ Softmax & Cross-Entropy Loss

Softmax converts logits into probabilities:

[
p = \text{softmax}(logits)
]

Then training uses:

[
\text{loss} = -\log(p_{\text{target}})
]

This measures how wrong the model’s prediction was.

---

# 8️⃣ Backpropagation (Orange Arrow)

The orange arrow shows gradients flowing backward through:

* Cross-entropy
* Softmax
* LM Head
* MLP
* Attention
* RMSNorm
* Embeddings
* Back to the Value objects

Because every scalar is tracked in a computation graph, gradients are computed using the **chain rule**.

Finally:

* Adam optimizer updates each parameter
* Gradients are reset
* Training repeats

---

# 🔑 What This Diagram Demonstrates

This diagram captures the **five irreducible ideas of GPT**:

1. Embed tokens
2. Attend (scaled dot-product)
3. Transform (MLP)
4. Predict (softmax + cross-entropy)
5. Learn (backprop + Adam)

Everything in large modern LLMs is built from these same core components — just scaled and optimized.

---

# 🧠 Why microGPT Matters

* No PyTorch
* No NumPy
* No GPU
* No tensor libraries

Just pure Python and scalar math.

It proves:

> The Transformer algorithm itself is small.
> Engineering scale is what makes modern LLMs complex.
