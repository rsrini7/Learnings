# microGPT Architecture — Complete Guide

![AI-ML/assets/microGPT-Complete-Architecture.png](assets/microGPT-Complete-Architecture.png)

> A comprehensive walkthrough of Andrej Karpathy's **microGPT**: the "most atomic" GPT implementation using **pure Python and math only** — no PyTorch, no NumPy, no GPU.

---

## High-Level Overview

```mermaid
flowchart TD
    A["📄 Raw Text\n(names.txt / shakespeare)"] --> B["🔤 Tokenizer\nChar → ID"]
    B --> C["📦 Embeddings\nToken + Position"]
    C --> D1["📐 RMSNorm ①\nAfter Embedding"]
    D1 --> D2["📐 RMSNorm ②\nBefore Attention"]
    D2 --> E["🔍 Causal Self-Attention\n4 Heads, KV Cache"]
    E --> D3["📐 RMSNorm ③\nBefore MLP"]
    D3 --> F["🧠 MLP Block\n16 → 64 → 16"]
    F --> G["📊 LM Head\nLogits (27 scores)"]
    G --> H["📈 Softmax\nProbabilities"]
    H -->|Training| I["⚖️ Loss + Backprop\n→ Adam Update"]
    H -->|Inference| J["🎲 Sample\nNext Character"]
    J -->|Loop until BOS| J
```

---

## 1. Data Loading and Preprocessing

The script begins by ensuring `input.txt` exists, defaulting to a dataset of names. Each line (name) is treated as an individual **document** and shuffled so the model learns character patterns — not a fixed ordering.

```python
if not os.path.exists('input.txt'):
    # downloads names.txt ...
docs = [l.strip() for l in open('input.txt').read().strip().split('\n') if l.strip()]
```

---

## 2. The Tokenizer — Text to Numbers

This is not a fancy library tokenizer. It finds every unique **character** in the text and uses that as the vocabulary.

```python
uchars = sorted(set(''.join(docs)))
BOS = len(uchars)   # Beginning of Sequence token (also acts as End-of-Sequence)
```

A special **BOS** token is added — it serves as both the start signal during generation and the stop signal when it's sampled as output.

**Example:**

```
"emma" → [BOS, e, m, m, a, BOS] → [26, 4, 12, 12, 0, 26]
```

```mermaid
flowchart LR
    T["'emma'"] --> C1["e → 4"]
    T --> C2["m → 12"]
    T --> C3["m → 12"]
    T --> C4["a → 0"]
    BOS1["BOS → 26"] --> E
    C1 --> E["[26, 4, 12, 12, 0, 26]"]
    C2 --> E
    C3 --> E
    C4 --> E
    BOS2["BOS → 26"] --> E
```

---

## 3. Embeddings — Numbers to Meaningful Vectors

Each token ID gets two 16-dimensional vectors that are **added together** to form one input vector:

| Embedding | Weight Matrix | Encodes |
|-----------|--------------|---------|
| **Token Embedding (wte)** | `state_dict['wte'][token_id]` | *What* this character is |
| **Position Embedding (wpe)** | `state_dict['wpe'][pos_id]` | *Where* this character sits in the sequence |

```mermaid
flowchart LR
    TID["token_id = 4 (e)"] --> WTE["wte lookup\n→ 16-dim vector"]
    PID["pos_id = 1"] --> WPE["wpe lookup\n→ 16-dim vector"]
    WTE --> ADD["➕ Element-wise Add"]
    WPE --> ADD
    ADD --> X["x: input vector\n[16 floats]"]
```

---

## 4. RMSNorm — Stabilize the Numbers

microGPT uses a **pre-norm Transformer design**: RMSNorm is applied before each sublayer (attention and MLP) inside each Transformer block, plus once at input after the combined embedding. This keeps values in a stable range and prevents exploding/vanishing gradients.

```python
x = rmsnorm(x)            # at input — after embedding, before the layer block
# inside each layer:
x = rmsnorm(x)            # before attention sublayer
x = rmsnorm(x)            # before MLP sublayer
```

**Formula:** `x / sqrt(mean(x²) + ε)`

> **Important:** This RMSNorm has **no learnable parameters** — no scale (γ) or shift (β). Unlike LayerNorm, it is purely a normalization operation with nothing added to `state_dict`.

---

## 5. The Autograd Engine — `Value` Class

Since there's no PyTorch, automatic differentiation is built from scratch. Every number (weight) in the model is a `Value` object.

```python
class Value:
    def backward(self):
        # topological sort + chain rule
```

```mermaid
flowchart LR
    FWD["Forward Pass\nBuilds computation graph"] --> GRAPH["🕸️ Computation Graph\n(Value objects linked)"]
    GRAPH --> BWD["backward()\nWalk graph in reverse"]
    BWD --> GRAD["∂loss/∂w for every weight\n(~4,192 gradients)"]
```

- **Forward pass**: every math operation records itself in the graph.
- **Backward pass**: walks the graph in reverse using the **chain rule** to compute how much each weight contributed to the error.

---

## 6. Model Architecture — `gpt()` Function

The `gpt` function is the Transformer. It processes **one token at a time** — there is no batching, no batch dimension, no parallel sequence processing. This single-token-at-a-time design is exactly why causality is structural: the KV cache simply hasn't seen future tokens yet when the current one is processed.

> **All linear projections (Q, K, V, attn_wo, mlp_fc1, mlp_fc2, lm_head) are bias-free** — the `linear()` function computes only `Wx`, never `Wx + b`. This matches modern GPT design.

```python
def gpt(token_id, pos_id, keys, values):
    tok_emb = state_dict['wte'][token_id]
    pos_emb = state_dict['wpe'][pos_id]
    # ... Attention and MLP blocks ...
```

### 6a. Causal Self-Attention

```mermaid
flowchart TD
    X["Input x [16-dim]"] --> Q["Query (Q)\n'What am I looking for?'"]
    X --> K["Key (K)\n'What info do I have?'"]
    X --> V["Value (V)\n'What do I share?'"]
    Q --> SCORE["Attention Scores\nQ·Kᵀ / √(head_dim)"]
    K --> SCORE
    SCORE --> SOFT["Softmax → weights\n⚠️ No mask tensor — KV cache\nonly holds past positions\n(implicit causality)"]
    SOFT --> OUT["Weighted sum of Values"]
    V --> OUT
    OUT --> HEADS["4 Heads concatenated\n(each head: 4-dim output)\n4 × 4 = 16-dim total"]
    HEADS --> PROJ["attn_wo: Linear 16 → 16\n(output projection)"]
    X --> RES["➕ Residual Connection\nx = x + Attention(x)"]
    PROJ --> RES
```

**Key insight on causality:** There is no explicit masking matrix. Causality is enforced *structurally* — at position 5, the KV cache only contains entries from positions 0–4 because they haven't been processed yet.

**Head dimension arithmetic:** `head_dim = n_embd // n_head = 16 // 4 = 4`. Each of the 4 heads independently attends over its own 4-dimensional slice of Q, K, V. Their outputs are concatenated back to 16 dims, then passed through `attn_wo` (a 16×16 linear projection) before the residual add.

**Implementation note:** There are no tensor `matmul` operations. Attention scores are computed via explicit Python loops over scalars: `sum(q_h[j] * k_h[t][j] for j in range(head_dim))`. Everything is scalar arithmetic on `Value` objects.

### 6b. MLP Block

```mermaid
flowchart LR
    X16["x [16-dim]"] --> FC1["Linear: 16 → 64"]
    FC1 --> RELU["ReLU\n(negatives → 0)"]
    RELU --> FC2["Linear: 64 → 16"]
    FC2 --> RES["➕ Residual\nx = x + MLP(x)"]
    X16 --> RES
```

The expansion to 64 dimensions gives the model more "room to think" before compressing back.

---

## 7. LM Head + Softmax — Scores to Probabilities

```mermaid
flowchart LR
    X16["x [16-dim]"] --> HEAD["Linear projection\n16 → 27 logits"]
    HEAD --> SOFT["Softmax"]
    SOFT --> PROBS["Probabilities\n'a':60%, 'o':20%, 'z':0.1%..."]
```

The 27 scores (one per character in the vocabulary) are converted to a probability distribution that sums to 100%.

---

## 8. Training Loop — Learning from Mistakes

**Task:** Next Token Prediction. If the model sees `"J"`, it tries to predict `"e"` for `"Jeffrey"`.

```python
losses = []
for pos_id in range(n):
    token_id, target_id = tokens[pos_id], tokens[pos_id + 1]  # current → next
    logits = gpt(token_id, pos_id, keys, values)
    probs = softmax(logits)
    loss_t = -probs[target_id].log()   # .log() is autograd-aware: defined on the Value class
    losses.append(loss_t)
loss = (1 / n) * sum(losses)           # per-token loss averaged across the document slice
```

```mermaid
flowchart TD
    A["Step 1–7: Forward Pass\n→ probabilities"] --> L["Step 8: Compute Loss\n-log(P(correct char))\nHigh surprise = High loss"]
    L --> B["Step 9: Backpropagation\nAutograd traces graph\n→ 4,192 gradients"]
    B --> O["Step 10: Adam Update\nNudge weights → lower loss"]
    O -->|Next token| A
```

**Loss intuition:** If the model predicts the correct next character with low confidence → loss is **high**. Perfect confidence → loss approaches **0**.

---

## 9. The Adam Optimizer

```python
lr_t = learning_rate * (1 - step / num_steps)  # linear decay
for i, p in enumerate(params):
    m[i] = beta1 * m[i] + (1 - beta1) * p.grad        # 1st moment (mean)
    v[i] = beta2 * v[i] + (1 - beta2) * p.grad ** 2   # 2nd moment (variance)
    m_hat = m[i] / (1 - beta1 ** (step + 1))           # bias correction
    v_hat = v[i] / (1 - beta2 ** (step + 1))           # bias correction
    p.data -= lr_t * m_hat / (v_hat ** 0.5 + eps_adam) # weight update
    p.grad = 0                                          # zero out gradient
```

```mermaid
flowchart LR
    G["Gradient p.grad"] --> M["1st Moment Buffer m\n(smoothed mean)"]
    G --> V["2nd Moment Buffer v\n(smoothed variance)"]
    M --> ADAM["Adam Update\nw = w - lr * m̂/√v̂"]
    V --> ADAM
    ADAM --> W["Updated Weight"]
```

The moment buffers act as **memory** for training — they smooth out updates so learning doesn't wobble, ensuring convergence.

- **Learning rate** starts at `0.01` and follows **linear decay** to 0: `lr_t = 0.01 × (1 − step/1000)`. Gradient is zeroed after each update (`p.grad = 0`) since the `Value` engine accumulates.

---

## 10. Inference — Generating New Names

```python
temperature = 0.5  # controls randomness: low = conservative, high = creative
for pos_id in range(block_size):
    logits = gpt(token_id, pos_id, keys, values)
    probs = softmax([l / temperature for l in logits])  # temperature applied to logits BEFORE softmax
    token_id = random.choices(range(vocab_size), weights=[p.data for p in probs])[0]
```

> **Note on temperature:** dividing logits by a value < 1 *sharpens* the distribution (more confident), while > 1 *flattens* it (more random). The source uses `temperature = 0.5` by default.

```mermaid
flowchart TD
    START["Start: BOS token"] --> FWD["Forward Pass\n→ probabilities"]
    FWD --> SAMPLE["Sample next character\n(weighted random)"]
    SAMPLE --> CHECK{Is it BOS\nor max length?}
    CHECK -->|No| APPEND["Append to sequence"]
    APPEND --> FWD
    CHECK -->|Yes| OUT["Output generated name\ne.g. 'emma', 'oliver'"]
```

Inference is identical to the forward pass during training — but **no loss is calculated and no weights are updated**. The model "babbles" by feeding its own output back in as the next input (autoregressive generation).

---

## 11. Full Training Pipeline — End to End

```mermaid
sequenceDiagram
    participant D as Data
    participant T as Tokenizer
    participant M as Model (gpt)
    participant A as Autograd
    participant O as Adam

    D->>T: Raw characters
    T->>M: Token IDs [BOS, e, m, m, a]
    loop For each position
        M->>M: Embed + Norm + Attention + MLP
        M->>A: Logits → Loss
        A->>A: backward() — compute all gradients
        A->>O: Gradients for 4,192 params
        O->>M: Updated weights
    end
    M-->>D: Repeat for 1,000 steps
```

---

## 12. Model Capacity & Experiments

| Experiment | Result |
|---|---|
| **1,000 steps on names** | Learns basic name structures — common endings, typical lengths |
| **Shakespeare (small model)** | Captures basic words ("then", "me") and formatting, but lacks long-range memory |

**Why?** The model is intentionally **tiny**: 1 Transformer layer, 16-dimensional embeddings, 4 attention heads, ~**4,192 total parameters**. This keeps it readable and runnable in pure Python.

> **Scaling note:** Larger GPTs increase `n_layer`, `n_embd`, and `vocab_size` — but the core algorithm here is **identical**. Everything else is just efficiency.

---

## 13. Key Design Principle

> The entire architecture runs on **pure Python scalars**. Every number is wrapped in a custom `Value` object that tracks both its value and its gradient, building a computation graph that enables learning via the chain rule.

```
Characters get personalities (embeddings)
    → talk to each other (attention)
    → think deeply (MLP)
    → predict what comes next (LM head + softmax)
    → learn from mistakes (loss + backprop + Adam)
    → repeat
```

---

*Based on Andrej Karpathy's microGPT implementation.*
