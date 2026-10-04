"""Ecdysis bundle harness (Bombus lab). Do not edit: the experiment is in experiment.py.

Reads ECDYSIS_SEED (64 hex characters, issued by the archive after the commitment),
derives the integer seed from its first 16 hex digits, runs experiment.run(seed),
and writes results/outputs.json: a flat object of 1 to 20 finite numbers or short strings.
"""
import json
import math
import numbers
import os
import pathlib
import re
import sys

if os.environ.get("PYTHONHASHSEED") != "0" and os.environ.get("BOMBUS_NO_REEXEC") != "1":
    # Hash randomisation would make set iteration order vary between runs of the same seed.
    os.execve(sys.executable, [sys.executable] + sys.argv, {**os.environ, "PYTHONHASHSEED": "0", "BOMBUS_NO_REEXEC": "1"})

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import experiment  # noqa: E402

# Data committed with the bundle (data/ beside this file), by file name: the only files an experiment reads.
_DATA = HERE / "data"
experiment.DATA = {p.name: str(p) for p in sorted(_DATA.iterdir()) if p.is_file()} if _DATA.is_dir() else {}

if "torch" in sys.modules:
    # One thread: the same seed gives the same numbers here, and as nearly the same as a CPU's arithmetic allows on
    # another machine. (torch.use_deterministic_algorithms is for GPUs, and would load the compiler stack.)
    import torch
    torch.set_num_threads(1)

NAME = re.compile(r"[A-Za-z][A-Za-z0-9_.-]{0,39}")


def main() -> None:
    seed_hex = os.environ.get("ECDYSIS_SEED", "")
    if not re.fullmatch(r"[0-9a-f]{64}", seed_hex):
        sys.exit("ECDYSIS_SEED must be 64 lower-case hex characters")
    out = experiment.run(int(seed_hex[:16], 16))
    if not isinstance(out, dict) or not 1 <= len(out) <= 20:
        sys.exit("experiment.run must return 1 to 20 named outputs")
    clean = {}
    for k, v in out.items():
        if not isinstance(k, str) or not NAME.fullmatch(k):
            sys.exit(f"bad output name: {k!r}")
        if isinstance(v, bool):
            v = int(v)
        if isinstance(v, numbers.Integral):
            v = int(v)
            if abs(v) > 2 ** 53:
                v = float(v)
        elif isinstance(v, numbers.Real):
            v = float(v)
            if not math.isfinite(v):
                sys.exit(f"output {k} is not finite")
        elif isinstance(v, str):
            if len(v) > 200:
                sys.exit(f"output {k} is longer than 200 characters")
        else:
            sys.exit(f"output {k} must be a number or a short string")
        clean[k] = v
    pathlib.Path("results").mkdir(exist_ok=True)
    with open(pathlib.Path("results") / "outputs.json", "w", encoding="utf-8") as f:
        json.dump(clean, f, sort_keys=True)


if __name__ == "__main__":
    main()
