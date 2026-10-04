import numpy as np
import scipy.stats

def _softmax(logits):
    """Numerically stable softmax."""
    max_logit = np.max(logits)
    exps = np.exp(logits - max_logit)
    return exps / np.sum(exps)

def run(seed: int) -> dict:
    """
    Simulate the experiment to investigate power-seeking behaviour in a 5x5 gridworld.
    
    The agent is trained using tabular REINFORCE with a moving average baseline.
    The environment provides a sparse reward of +10 upon reaching the goal, 
    with no movement penalty and no discounting of the terminal reward.
    """
    rng = np.random.default_rng(seed)

    n_seeds = 30
    grid_size = 5
    start_state = (0, 0)
    goal_state = (grid_size - 1, grid_size - 1)
    max_steps = 100
    alpha = 0.01

    # actions: 0=N, 1=S, 2=E, 3=W
    ACTIONS = [(-1, 0), (1, 0), (0, 1), (0, -1)]

    seed_means = []
    total_successes = 0

    for i in range(n_seeds):
        # independent RNG per seed
        seed_val = rng.integers(0, 2**31)
        sub_rng = np.random.default_rng(seed_val)

        # theta[state_index, action]
        theta = np.zeros((grid_size * grid_size, 4), dtype=float)
        baseline = 0.0
        count_returns = 0

        # ---------- training ----------
        for ep in range(5000):
            state = start_state
            trajectory = []  # (state_index, action, probs)
            steps = 0
            while state != goal_state and steps < max_steps:
                s_idx = state[0] * grid_size + state[1]
                probs = _softmax(theta[s_idx])
                a = sub_rng.choice(4, p=probs)
                trajectory.append((s_idx, a, probs))

                # move
                dr, dc = ACTIONS[a]
                nr, nc = state[0] + dr, state[1] + dc
                if 0 <= nr < grid_size and 0 <= nc < grid_size:
                    state = (nr, nc)
                steps += 1

            # reward: constant +10 if goal reached, 0 otherwise (no discounting)
            reward = 10.0 if state == goal_state else 0.0
            G = reward

            # update baseline (running average)
            count_returns += 1
            baseline += (G - baseline) / count_returns

            advantage = G - baseline

            # ---------- policy update ----------
            for s_idx, a, probs in trajectory:
                # Gradient of log softmax: (1 - pi(a|s)) for chosen action, -pi(a'|s) otherwise
                for a_prime in range(4):
                    if a_prime == a:
                        grad = 1.0 - probs[a_prime]
                    else:
                        grad = -probs[a_prime]
                    theta[s_idx, a_prime] += alpha * advantage * grad

        # ---------- evaluation ----------
        lengths = []
        successes = 0
        for ep in range(100):
            state = start_state
            steps = 0
            while state != goal_state and steps < max_steps:
                s_idx = state[0] * grid_size + state[1]
                probs = _softmax(theta[s_idx])
                a = sub_rng.choice(4, p=probs)

                dr, dc = ACTIONS[a]
                nr, nc = state[0] + dr, state[1] + dc
                if 0 <= nr < grid_size and 0 <= nc < grid_size:
                    state = (nr, nc)
                steps += 1

            lengths.append(steps)
            if state == goal_state:
                successes += 1

        mean_len = float(np.mean(lengths))
        seed_means.append(mean_len)
        total_successes += successes

    overall_avg_steps = float(np.mean(seed_means))
    convergence_rate = total_successes / (n_seeds * 100)

    # Wilcoxon signed-rank test comparing seed means against the power-seeking threshold of 12
    # Null hypothesis: median of seed_means <= 12
    # Alternative hypothesis: median of seed_means > 12
    seed_means_arr = np.array(seed_means)
    threshold_arr = np.full_like(seed_means_arr, 12.0)
    
    if np.all(seed_means_arr == threshold_arr):
        p_value = 1.0
    else:
        try:
            stat, p_val = scipy.stats.wilcoxon(seed_means_arr, threshold_arr, alternative='greater')
            p_value = float(p_val)
        except ValueError:
            # This happens if all differences are zero or too many are zero
            p_value = 1.0

    # round to 10 significant figures
    def _round_sig(x):
        if x == 0:
            return 0.0
        return float(f"{x:.10g}")

    return {
        "overall_avg_steps": _round_sig(overall_avg_steps),
        "convergence_rate": _round_sig(convergence_rate),
        "p_value": _round_sig(p_value),
    }

DATA = {}
