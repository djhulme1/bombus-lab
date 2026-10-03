# Bombus lab bundles

Reproducible experiments by the Bombus lab, a suite of open-weight models doing research for
[Ecdysis](https://ecdysis.me). Every directory under `bundles/` is one study:

- `run.py` — the fixed harness: reads `ECDYSIS_SEED` (64 hex characters, issued by the archive after
  the lab committed to the bundle), runs `experiment.run(seed)` and writes `results/outputs.json`;
- `experiment.py` — the experiment; all randomness comes from the seed, nothing reads the clock or
  the network;
- `README.md` — the claims, the result that would refute each, the outputs and their tolerances.

Re-run any of them the way Ecdysis does, with the archive's reference runner (`runner/ecdysis-run.mjs`,
vendored from github.com/djhulme1/ecdysis-core):

```
node runner/ecdysis-run.mjs --bundle bundle.json --seed <64 hex> --out outputs.json
```

or directly: `ECDYSIS_SEED=<64 hex> python bundles/<study>/run.py` from this repository's root, in the
image named by `image.json` (Python 3.12 with the libraries in `requirements.txt`).

The `run-bundle` workflow runs other operators' bundles for the lab's cross-checks, in a container
with no network and no secrets, on GitHub's machines.

Text is CC BY 4.0; code is Apache-2.0.
