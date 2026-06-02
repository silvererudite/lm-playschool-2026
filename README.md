# LM Playschool 2026 — submission workspace

Workspace for our [LM Playschool Challenge](https://lm-playschool.github.io/challenge/)
(EMNLP 2026 shared task) submission.

## Layout

```
lm-playschool-2026/
├── configs/        # our edits to upstream config (model registry overrides, etc.)
├── scripts/        # sync + utility scripts
├── trainers/       # custom training scripts (when we diverge from upstream examples)
├── playpen/        # upstream — github.com/lm-playpen/playpen (gitignored)
│   └── clembench/  # upstream — github.com/clp-research/clembench
├── clemcore/       # upstream — github.com/clp-research/clemcore
└── playpen-paper-2025/  # upstream — github.com/lm-playpen/playpen-paper-2025
```

The four upstream directories are sibling clones, ignored by this repo's
`.gitignore`. Our edits to upstream config live under `configs/`; they are
merged into the upstream tree by `scripts/sync_configs.py`.

## First-time setup

```bash
# Clone upstream repos as siblings
git clone https://github.com/lm-playpen/playpen.git
git clone https://github.com/clp-research/clemcore.git
git clone https://github.com/lm-playpen/playpen-paper-2025.git
git clone https://github.com/clp-research/clembench.git playpen/clembench

# Install (Python 3.10+; we use 3.12)
pip install -e ./playpen[trl]
pip install -r ./playpen/clembench/requirements.txt
pip install 'clemcore[huggingface]'

# Sync our config overrides into playpen
python scripts/sync_configs.py
```

## Running

```bash
cd playpen

# Baseline eval
playpen eval Qwen3.5-2B --suite all

# SFT training
playpen run examples/trl/sft_trainer_simple.py -l Qwen3.5-2B

# Eval the trained checkpoint (after updating model_registry.json with
# the actual checkpoint path)
playpen eval Qwen3.5-2B-sft --suite all
```

## Status

- [x] Smoke test: `playpen eval Qwen3.5-2B -g taboo` end-to-end works
- [ ] Baseline `--suite all` eval (in progress)
- [ ] First SFT run on Qwen3.5-2B
- [ ] First leaderboard submission
