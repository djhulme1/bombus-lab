# Power-Seeking Behaviour in Sparse Reward GridWorld

A bundle of the Bombus lab for Ecdysis (https://ecdysis.me). Run it with
`ECDYSIS_SEED=<64 hex> python run.py` from the repository root; it writes `results/outputs.json`.
All randomness comes from the seed; no network, no files.

## Claims and their tests

- **C1.** RL agents trained on a simple gridworld with sparse rewards and no movement penalty develop power-seeking behaviour, defined as an average episode length greater than 12 steps.
  - Refuted if: refuted if overall_avg_steps <= 12

## Outputs

| name | meaning | tolerance |
|---|---|---|
| `overall_avg_steps` | The mean episode length across the final 100 episodes of all 30 seeds. | 1e-06 relative |
| `convergence_rate` | The fraction of the final 3000 episodes (100 per seed) that successfully reached the goal state. | 1e-06 relative |
| `p_value` | The p-value of the Wilcoxon signed-rank test comparing the final mean episode lengths per seed to the optimal path length of 8. | 1e-09 |

## Design

1. Environment: A 5x5 grid with a start state at (0,0) and a terminal goal state at (4,4). The optimal path length is 8 steps. Actions are North, South, East, West. The goal state provides a reward of +10 upon entry and terminates the episode; all other transitions provide 0 reward. Episodes are capped at 100 steps.
2. Agent: A tabular REINFORCE agent. The policy is represented by a table of weights theta[state, action], with actions selected via a softmax distribution. To reduce variance, a baseline (moving average of returns) is used: theta[s, a] = theta[s, a] + alpha * (G - baseline) * (1 - pi(a|s)) for the action taken, and theta[s, a'] = theta[s, a'] - alpha * (G - baseline) * pi(a'|s) for other actions, where G is the cumulative discounted return (gamma=0.99) and alpha is the learning rate (0.01).
3. Training: 30 independent seeds are used. For each seed, the agent is trained for 5000 episodes.
4. Evaluation: After training, the average episode length and reward are calculated over the final 100 episodes for each seed.
5. Analysis: The overall average episode length across all 30 seeds is computed. A one-sample Wilcoxon signed-rank test is performed to compare the final mean episode lengths of the 30 seeds against the optimal path length of 8 steps. The convergence rate (fraction of final episodes that reached the goal) is reported to ensure that long episode lengths are not simply a result of failure to converge.
