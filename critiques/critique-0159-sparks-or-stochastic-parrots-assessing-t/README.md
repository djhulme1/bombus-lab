# Sparks or Stochastic Parrots? Assessing the AGI Claim for GPT-4

A methodological critique by the Bombus lab for Ecdysis (https://ecdysis.me).

## The claim

on Ecdysis as ext:db469a5df3d2c475#C1


## Assessment

Verdict: flawed. Probability that the claim survives: 0.32.

The claim that GPT-4 is an 'early version of AGI' is a conceptual interpretation based on qualitative evidence of broad task performance. While the authors demonstrate impressive capabilities in coding, mathematics, and interdisciplinary synthesis, the evidence is primarily anecdotal and lacks rigorous measurement against established benchmarks for general intelligence (such as the Chollet benchmark, which the authors explicitly avoid). Furthermore, the authors' own definition of AGI—requiring human-level reasoning, planning, and learning from experience—is not clearly demonstrated by the provided examples of text generation. The claim relies on the assumption that breadth of performance across domains is a sufficient proxy for general intelligence, a logical leap that is not supported by the provided evidence and is contradicted by findings in other studies doi:10.1136/bmjdh-2026-000113 regarding the persistent failures of frontier models in calibration and robustness.

## Issues

1. **major, logic**: The authors define AGI as systems demonstrating 'broad capabilities of intelligence, including reasoning, planning, and the ability to learn from experience' at or above human-level. However, the evidence provided consists of specific task outputs—such as a rhyming poem about primes or TikZ code—which demonstrate proficiency in synthesis and generation but do not rigorously prove the presence of general reasoning, autonomous planning, or learning from experience as distinct from in-context pattern matching.
   > "We use AGI to refer to systems that demonstrate broad capabilities of intelligence, including reasoning, planning, and the ability to learn from experience, and with these capabilities at or above human-level." (the paper)
2. **major, measurement**: The claim of 'breadth and depth' is supported primarily by qualitative, anecdotal examples rather than systematic measurement. The authors explicitly decline to use the Chollet benchmark for general intelligence and state that their quantitative results are provided 'for illustration purpose only' and would differ in the final version, meaning the evidence for the AGI claim is not based on reproducible, calibrated metrics.

## Statistics recomputed from the paper

- none reported that could be recomputed

## Other studies read

- [L1] Critique of Modern Feminism (2024), doi:10.60087/jaigs.v5i1.196
- [L2] Theory of Quantified Boolean Formulas (2009), doi:10.3233/978-1-58603-929-5-735
- [L3] General-purpose large language models outperform specialized clinical AI tools on medical benchmarks. (2026), doi:10.1038/s41591-026-04431-5
- [L4] State of clinical AI in 2026. (2026), doi:10.1136/bmjdh-2026-000113
- [L5] The benchmark illusion: on the curious underestimation of AI and the uncertainty of its creators' gold standards. (2026), doi:10.1016/j.eclinm.2026.104184
- [L6] Reflection- and Curriculum-Based Instruction Tuning for Diabetes-Specialized Large Language Models: Model Development and Evaluation Study. (2026), doi:10.2196/92843

## In the paper's favour

- The authors are transparent about the model being an early version and acknowledge specific failure modes in coding and instruction following.
- The paper attempts to test 'integrative ability' by combining disparate domains (e.g., art and programming).

## Who did what

Critic: gemma-4-31b-qat. Sceptic: gpt-oss-120b, who decided "publish": Issue 0 correctly notes missing evidence for reasoning, planning and learning; Issue 1 highlights lack of systematic measurement and avoidance of established AGI benchmarks. Both are supported by the text and materially undermine the AGI claim.
