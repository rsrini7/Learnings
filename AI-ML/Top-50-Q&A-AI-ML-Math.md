# Top 50 Interview Q/A for AI/ML Math

## A. Optimization & Training Dynamics (Q1–10)

**1. Why does gradient descent sometimes fail even with a convex loss?**
**Answer:** Poor conditioning, bad learning rate, numerical precision, or feature scaling.
**Signal:** Knows about Hessian condition number.

**2. What’s the difference between local minima and saddle points?**
**Answer:** High-dimensional losses mostly fail at saddle points, not minima.
**Reason:** Explains why momentum and noise help.

**3. Why do residual connections help deep networks?**
**Answer:** They improve gradient flow by shortening effective paths.
**Red flag:** “They make training faster” (too shallow).

**4. When does SGD outperform Adam?**
**Answer:** Often generalizes better in late training due to implicit regularization.

**5. What breaks when learning rate is too small?**
**Answer:** Training stalls, stuck in flat regions, poor generalization.

**6. How do you debug exploding gradients in production?**
**Answer:** Gradient clipping, normalization, activation changes.

**7. Why does batch size affect convergence quality?**
**Answer:** Noise scale affects implicit regularization.

**8. What does “loss landscape sharpness” mean?**
**Answer:** Sharp minima generalize worse.

**9. Why does fine-tuning sometimes degrade performance?**
**Answer:** Catastrophic forgetting, distribution mismatch.

**10. What math explains early stopping as regularization?**
**Answer:** Limits effective capacity.

---

## B. Probability & Statistics (Q11–20)

**11. Why does accuracy fail as a metric?**
**Answer:** Ignores confidence, imbalance, and cost asymmetry.

**12. When is log-loss preferred over accuracy?**
**Answer:** When probability calibration matters.

**13. What distribution shift hurts models the most?**
**Answer:** Label shift and concept drift.

**14. Why is Gaussian assumption dangerous?**
**Answer:** Real data is heavy-tailed and multimodal.

**15. How do you detect data drift mathematically?**
**Answer:** KL divergence, PSI, Wasserstein distance.

**16. What’s the difference between aleatoric and epistemic uncertainty?**
**Answer:** Noise vs model ignorance.

**17. Why does overconfidence kill production models?**
**Answer:** Bad decisions without fallback.

**18. When does MLE fail?**
**Answer:** Model misspecification, small data regimes.

**19. Why does class imbalance distort probabilities?**
**Answer:** Prior mismatch.

**20. How do you recalibrate a model?**
**Answer:** Platt scaling, isotonic regression.

---

## C. Linear Algebra & Geometry (Q21–30)

**21. Why does PCA sometimes destroy signal?**
**Answer:** Variance ≠ relevance.

**22. What does an eigenvalue close to zero mean?**
**Answer:** Redundant or degenerate dimensions.

**23. Why are embeddings anisotropic?**
**Answer:** Collapse toward dominant directions.

**24. Why does cosine similarity outperform Euclidean in NLP?**
**Answer:** Direction matters more than magnitude.

**25. When does cosine similarity fail?**
**Answer:** Near-duplicate vectors, dense clusters.

**26. Why do high-dimensional distances concentrate?**
**Answer:** Curse of dimensionality.

**27. How does SVD help debugging embeddings?**
**Answer:** Detects rank collapse.

**28. Why do normalized embeddings help retrieval?**
**Answer:** Stabilizes geometry.

**29. Why does PCA help noise removal?**
**Answer:** Noise lives in low-variance directions.

**30. When should you not reduce dimensions?**
**Answer:** When interpretability matters.

---

## D. Loss Functions & Divergence (Q31–40)

**31. Why is cross-entropy equivalent to MLE?**
**Answer:** Minimizes KL divergence.

**32. When is KL divergence asymmetric a problem?**
**Answer:** Mode collapse.

**33. Why is MSE bad for classification?**
**Answer:** Poor gradient behavior near extremes.

**34. What’s label smoothing mathematically doing?**
**Answer:** Reduces overconfidence, adds entropy.

**35. Why does softmax saturate?**
**Answer:** Exponential dominance.

**36. How do you stabilize softmax?**
**Answer:** Log-sum-exp trick.

**37. Why do ranking losses differ from classification losses?**
**Answer:** Optimizes relative order, not absolute labels.

**38. Why does KL show up in RL and LLM fine-tuning?**
**Answer:** Controls policy deviation.

**39. Why does minimizing loss not guarantee business success?**
**Answer:** Objective mismatch.

**40. How do you design a custom loss?**
**Answer:** Encode business constraints mathematically.

---

## E. Production Reality Checks (Q41–50)

**41. Why do models fail silently?**
**Answer:** Distribution shift + confidence miscalibration.

**42. What math explains hallucinations?**
**Answer:** Likelihood maximization under uncertainty.

**43. Why does more data sometimes hurt?**
**Answer:** Noisy or misaligned labels.

**44. Why does quantization change accuracy?**
**Answer:** Precision loss affects geometry.

**45. Why does batch inference differ from online inference?**
**Answer:** Numerical ordering + statefulness.

**46. What breaks first under latency pressure?**
**Answer:** Softmax, attention, I/O.

**47. Why does caching work mathematically?**
**Answer:** High semantic redundancy.

**48. Why do embeddings drift over time?**
**Answer:** Model updates change vector space.

**49. Why do explainability methods disagree?**
**Answer:** Different local approximations.

**50. What math skill separates seniors from juniors?**
**Answer:** Knowing *what assumptions you’re violating*.
