# Inside a Neuron: The Building Blocks of a Neural Network

*By Srinivasan Ragothaman (@rsrini7)*

![Inside-a-single-Neuron-House-Prediction](assets/Inside-a-single-Neuron-House-Prediction.png)

---

You've heard the word "neural network" thrown around in every AI conversation for the past few years. You've probably seen the diagrams — circles connected by lines, data going in on the left, predictions coming out on the right. But has anyone ever stopped to explain what those circles are *actually doing*?

That's what this article is about. Not the whole network. Not the training pipeline. Not deployment. Just one neuron — what it sees, what it computes, and why any of it produces something useful.

To make this concrete, let's use a running example throughout: **predicting the price of a house**.

---

## What Does a Neuron Actually See?

A neuron doesn't see a house. It doesn't see walls or windows or a garden. It sees a list of numbers.

When we feed housing data into a neural network, we first convert every property of a house into a numerical feature. In our example, we'll use four: square footage, number of bedrooms, number of bathrooms, and zip code. Each of these gets *normalized* — scaled to a consistent decimal range so the model can process them evenly. A large house with four bedrooms might produce a feature list that looks like this:

```
[0.85, 0.60, 0.40, 0.72]
```

This ordered list is called an **input vector**. It's the machine's encoding of what the house *is*. The neuron doesn't know that 0.85 represents 2,400 square feet — it only knows the number 0.85. All the meaning lives in the structure the network learns, not in the raw values themselves.

---

## Weights: What the Neuron Pays Attention To

Once the neuron has its input vector, it does something surprisingly simple: it multiplies each feature by a number called a **weight**.

A weight represents learned importance. If the network has figured out that square footage is a powerful predictor of price, it will assign a high weight to that feature — something like 0.9. Bathrooms, while relevant, might matter less to the final price prediction in a particular market, so they might earn a weight of only 0.2.

The computation looks like this:

```
x₁ × w₁  →  0.85 × 0.9  =  0.765   (Square Footage)
x₂ × w₂  →  0.60 × 0.5  =  0.300   (Bedrooms)
x₃ × w₃  →  0.40 × 0.2  =  0.080   (Bathrooms)
x₄ × w₄  →  0.72 × 0.7  =  0.504   (Zip Code)
```

Each of these products is then **added together** to produce a single number called the weighted sum — formally written as Σ(xᵢ × wᵢ). This is also called a dot product. It's a compact mathematical way of saying: "given what I know about this house, here is my overall signal strength."

The weights are not set by a human. They are *learned* during training — starting as random values and gradually being tuned to minimize prediction error. We'll come back to that.

---

## The Bias: A Quiet but Important Offset

There's one more term added to the weighted sum before the neuron finishes computing: the **bias**, represented as *b*.

```
Output = Σ(xᵢ × wᵢ) + b
```

The bias is a learnable offset that shifts the neuron's activation threshold. Think of it this way: without a bias, a neuron whose inputs are all near zero would always produce the same near-zero output, regardless of what pattern it's supposed to detect. The bias gives the neuron freedom to fire even when the inputs are small. It's a simple addition, but it's what allows neurons to express a much wider range of behaviors.

---

## Multiple Neurons, Multiple Specializations

Here's where things get interesting. In a real neural network layer, many neurons all receive the *same* input vector simultaneously. Every neuron sees the same features for the same house. But each neuron has its *own* set of weights.

This means different neurons attend to different aspects of the data:

- **Neuron A** might develop a strong reaction to large square footage and premium zip codes — it becomes a detector for high-end suburban homes.
- **Neuron B** might focus on bedroom and bathroom counts — it specializes in recognizing multi-family properties.
- **Neuron C** might pick up on some combination you didn't design intentionally — a pattern the data itself revealed.

Nobody programs these specializations. They *emerge* over training. Neurons that consistently help the network make better predictions grow stronger. Those that don't, fade. Over thousands of training steps, a layer of neurons becomes a layer of pattern detectors, each sensitive to a different signal in the data.

---

## The Activation Function: Making Sense of the Number

After computing the weighted sum, the neuron has a raw number that could be anything — very large, very small, positive, or negative. That's not very useful on its own. So we pass it through an **activation function**, which compresses it into a standardized range.

The classic example is the **sigmoid function**:

```
σ(z) = 1 / (1 + e⁻ᶻ)
```

No matter what number you feed into sigmoid, it outputs a value strictly between 0 and 1. Feed in a very large positive number and you get something close to 1. Feed in a very large negative number and you get something close to 0. The rest falls gracefully on the S-shaped curve in between. This "squishifying" effect makes the neuron's output interpretable: a value close to 1 means the pattern is strongly present; a value close to 0 means it isn't.

Modern neural networks typically use **ReLU (Rectified Linear Unit)** instead of sigmoid, because it's computationally cheaper and avoids some training problems that sigmoid creates at scale. ReLU is simpler: it passes positive values through unchanged and zeros out anything negative. The core idea is the same — transform the raw weighted sum into a meaningful, bounded signal.

---

## Why Nonlinearity Changes Everything

The activation function does more than just compress a number. It introduces **nonlinearity** into the network — and this is arguably the most important property of a neural network.

Without an activation function, stacking multiple layers of neurons together is mathematically equivalent to just having a single layer. You can stack 100 layers of pure linear transformations and end up with exactly the same expressive power as one. The math collapses. No depth, no complexity, no ability to learn anything beyond a straight line.

The activation function breaks this. It bends the math. Suddenly, neurons in later layers can learn combinations and compositions of patterns from earlier layers, building up increasingly abstract representations of the data. This is what allows a neural network to eventually learn something as nuanced as "this house has the layout signature of a high-value urban property," even though no human ever defined what that signature looks like.

---

## The Activation Level: The Neuron's Final Vote

After passing through the activation function, the neuron produces its output — a single number called the **activation level**. This is the neuron's "vote" on whether its particular pattern is present in the input.

For our house example, if a neuron has learned to detect large suburban homes and our input vector represents exactly that kind of property, it might output an activation level of 0.87 — close to 1, brightly lit, strongly activated. It's saying: *yes, I see what I'm looking for here*.

This activation value then becomes part of the input to the neurons in the next layer. Activations flow forward through the network, layer by layer, each layer building on the patterns detected by the previous one, until the final layer produces the prediction: a house price.

---

## Stacking It All Together: The Dense Network

A single neuron captures only one relationship. Stack hundreds of them across multiple layers and the network can represent combinations of combinations — a hierarchy of learned patterns.

In a typical **dense (fully connected) network**, every neuron in one layer is connected to every neuron in the next. Each connection carries its own weight and bias. For a network predicting housing prices, the architecture might look like:

- **Input Layer** → 4 features (our vector)
- **Hidden Layer 1** → 64 neurons, each with 4 weights + 1 bias
- **Hidden Layer 2** → 32 neurons, building on the patterns above
- **Output Layer** → 1 neuron, outputting the predicted price (e.g., $412,000)

Every one of those weights and biases is a "dial" — a parameter that gets adjusted during training to minimize the gap between what the network predicts and what the actual prices are.

---

## How the Dials Get Tuned: A Glimpse of Training

When training begins, all those weights are initialized to random values. The network makes terrible predictions. But after each prediction, the error is calculated and a process called **backpropagation** works backward through the network, computing how much each weight contributed to the error and adjusting each one slightly in the direction that would reduce it.

Repeat this tens of thousands of times across thousands of houses, and the weights gradually converge on values that make the network accurate. Neurons that found useful patterns get reinforced. Neurons that were tracking noise get downweighted.

Tracking this process is where tools like **MLflow** become invaluable. MLflow is an open-source platform that lets you log every training run — the weights, the loss curves, the hyperparameters — so you can visualize how the model evolves, compare different configurations, and diagnose when training goes wrong.

---

## What Comes Next: Backpropagation

We've walked through the entire forward pass of a neuron: input vector → weighted sum → bias → activation function → activation level → passed to the next layer. This is how a trained network makes a prediction.

But we haven't covered the most fascinating part: how does the network *become* trained in the first place? How does it know which direction to nudge each of those thousands of weights?

That's the job of **backpropagation** — an elegant application of calculus that propagates the prediction error backward through the network, assigning responsibility to each weight, and updating them all in one coordinated step. It's the engine that makes learning possible.

That's a story for the next article.

---

## The Takeaway

A neural network is, at its core, a very large collection of very simple calculators — neurons — each doing a tiny bit of arithmetic and passing a single number forward. No individual neuron is intelligent. No individual neuron "understands" housing prices. But arranged in layers, trained over data, and guided by backpropagation, they collectively learn to detect patterns that no human explicitly programmed.

The next time someone tells you AI is a black box, you can tell them: it's actually just a lot of weighted sums, a bias term, and a sigmoid curve. The magic isn't mysterious — it's mathematical.

---

*Follow along for the next post in this series: **Backpropagation — How a Neural Network Actually Learns.***
