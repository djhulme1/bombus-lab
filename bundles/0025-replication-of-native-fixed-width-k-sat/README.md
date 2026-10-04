# Replication of Native Fixed-Width K-SAT Obstruction

A bundle of the Bombus lab for Ecdysis (https://ecdysis.me). Run it with
`ECDYSIS_SEED=<64 hex> python run.py` from the repository root; it writes `results/outputs.json`.
All randomness comes from the seed; no network, no files.

## Claims and their tests

- **C1.** Constant-width random K-SAT cannot achieve solution independence because the normalized second moment of the satisfying assignment count is exponentially large.
  - Refuted if: The run is refuted if the calculated normalized second moment S2 does not grow exponentially with N (i.e., if the slope of the linear regression of ln(S2) vs N is not significantly positive).

## Outputs

| name | meaning | tolerance |
|---|---|---|
| `n_values` | The values of N used for the calculation. | exact |
| `ln_s2_values` | The natural logarithms of the normalized second moment for each N. | exact |
| `slope` | The slope of the linear regression of ln(S2) vs N. | 1e-06 relative |
| `target_holds` | 1 if the normalized second moment grows exponentially (confirming the claim), 0 otherwise. | exact |

## Design

The study computes the normalized second moment S2 for a random 3-SAT ensemble (K=3). The probability of a clause being falsified by a single assignment is p = 2^-K. The number of clauses M is set to round(N * ln(2) / -ln(1-p)) to keep E[Z] ≈ 1. The normalized second moment is given by S2 = sum_{d=0}^N [comb(N, d) / 2^N * ((1 - 2p + p_both(d)) / (1-p)^2)^M], where p_both(d) = (comb(N-d, K) / comb(N, K)) * p. To avoid numerical overflow, the computation is performed in the log-domain using the log-sum-exp trick: ln(S2) = max_d(L_d) + ln(sum_d exp(L_d - max_d(L_d))), where L_d = ln(comb(N, d)) - N*ln(2) + M * ln((1 - 2p + p_both(d)) / (1-p)^2). We compute ln(S2) for N in [20, 40, 60, 80, 100, 120, 140, 160, 180, 200] and perform a linear regression of ln(S2) vs N. A positive slope confirms the exponential growth.
