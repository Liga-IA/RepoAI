# Evaluation & Ablation Suite

This folder houses the evaluation scripts and metrics validating the framework.

### Methodology
The scripts herein are designed to compare the SCA-Lex Hybrid Fusion ($\alpha=0.5$) against the baseline Voting Ensemble benchmark, proving its empirical superiority in handling complex distractors.

### Files
- `ablation_study.py`: Evaluates the Hybrid Fusion approach against single-modality baseline strategies.
- `benchmark_forensics.py`: Runs comprehensive precision and recall evaluations across the forensic dataset.
- `evaluate_ensemble.py`: Benchmarks the traditional Voting Ensemble implementation.
- `ablation_results.json`: Cached outputs of the latest ablation study run.
- `forensic_ensemble_results.json`: Cached benchmark logs.
