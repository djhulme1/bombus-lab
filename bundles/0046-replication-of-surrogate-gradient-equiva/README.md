# Replication of Surrogate Gradient Equivalence in Stochastic Perceptrons

A bundle of the Bombus lab for Ecdysis (https://ecdysis.me). Run it with
`ECDYSIS_SEED=<64 hex> python run.py` from the repository root; it writes `results/outputs.json`.
All randomness comes from the seed; no network, no files.

## Claims and their tests

- **C1.** In a single-neuron Perceptron, the surrogate derivative is equivalent to the derivative of the expected output of a stochastic neuron if the surrogate matches the derivative of the escape noise function.
  - Refuted if: refuted if max_diff > 0.02

## Outputs

| name | meaning | tolerance |
|---|---|---|
| `max_diff` | The maximum absolute difference between the empirically estimated gradient of the expected output and the matching surrogate derivative across tested points. | 1e-06 relative |
| `target_holds` | 1 if the empirical gradient matches the matching surrogate (within tolerance) and is closer than the mismatched surrogate, 0 otherwise. | exact |

## Design

1. Define the escape noise function $p(u) = \text{sigmoid}(u) = 1 / (1 + \exp(-u))$.
2. Define the matching surrogate $\sigma'_1(u) = p'(u) = p(u)(1 - p(u))$ and a mismatched surrogate $\sigma'_2(u) = 0.5 p'(u)$.
3. Select three membrane potential values $u \in \{-1.0, 0.0, 1.0$.
4. For each $u$:
   a. Sample $N = 10^7$ values of noise $\xi_i$ from a Logistic distribution (using $\xi = \ln(U) - \ln(1-U)$ where $U \sim \text{Uniform}(0, 1)$) using the provided seed.
   b. Compute the empirical gradient $\hat{g}(u)$ using the Common Random Numbers (CRN) method: $\hat{g}(u) = \frac{1}{2hN} \sum_{i=1}^N (\mathbb{I}(\xi_i > -u-h) - \mathbb{I}(\xi_i > -u+h))$ with $h = 10^{-3}$.
5. Calculate the absolute difference between the empirical gradient and the matching surrogate: $diff_1(u) = |\hat{g}(u) - \sigma'_1(u)|$.
6. Calculate the absolute difference between the empirical gradient and the mismatched surrogate: $diff_2(u) = |\hat{g}(u) - \sigma'_2(u)|$.
7. Output `max_diff` as the maximum of $diff_1(u)$ across the three $u$ values.
8. Output `target_holds = 1` if `max_diff <= 0.02` and $\text{mean}(diff_1) < \text{mean}(diff_2)$, otherwise 0.
