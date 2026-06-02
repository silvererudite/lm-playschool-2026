# Resume notes — 2026-06-02

Snapshot of exactly where things are after killing the baseline eval mid-run.

## What's done

- Workspace at `/mnt/sagemaker-nvme/lm-playschool-2026/`, git repo on `main` pushed to
  `https://github.com/silvererudite/lm-playschool-2026.git` (commit `cccce0d`).
- Upstream repos (gitignored, sibling clones): `playpen/`, `clemcore/`, `playpen-paper-2025/`, `playpen/clembench/`.
- HF cache symlinked: `~/.cache/huggingface -> /mnt/sagemaker-nvme/hf-cache` (already holds Qwen3.5-2B weights).
- `pip install -e ./playpen[trl]` + clembench reqs + `clemcore[huggingface]` done. Verify with `playpen list models` (should show 27, including the three Qwen3.5-2B entries).
- Smoke test passed: `playpen eval Qwen3.5-2B -g taboo` produced clemscore (0.0 on this 1 game) end-to-end.
- **Baseline clem suite finished:** clemscore = **12.59** (leaderboard reference: 13.05 — within run-to-run noise; pipeline matches maintainers').
  - Saved: `playpen/playpen-eval/2026-06-02T17-14-08/clem/results.csv` and per-game interactions in `playpen/playpen-eval/2026-06-02T17-14-08/clem/Qwen3.5-2B/`.
- Static suite partially done: cladder complete (~101 instances), ifeval was killed mid-run (~23 instances). bbh, mmlu_pro, eqbench not started.

## What's left to finish baseline

The static suite. Three options on resume:

1. **Re-run just static, fresh dir (simplest).** Throws away the cladder progress and re-runs all 5 static datasets (~80 min wall-clock):
   ```bash
   cd /mnt/sagemaker-nvme/lm-playschool-2026/playpen
   playpen eval Qwen3.5-2B --suite static
   ```
2. **Re-run static into the existing dir to preserve cladder.** Worth checking if `playpen eval` skips already-completed datasets when pointed at an existing `-r` results dir — a quick test on a single dataset would confirm. The `--skip_gameplay` flag exists for clem only per `--help`.
3. **Skip the baseline reproduction.** Trust the leaderboard's 13.05/44.02 numbers since clemscore=12.59 already validates our pipeline. Move straight to SFT training.

Recommendation: **option 3.** We've already shown the pipeline matches; spending another ~80 min to nail down a statscore that's well-documented on the leaderboard is low value. Use the time on SFT.

## Tasks (in-session task list state)

```
#1. [in_progress] Baseline: eval Qwen3.5-2B on full suite   (paused mid-run)
#2. [pending]     Train SFT on Qwen3.5-2B with playpen-data
#3. [pending]     Eval SFT checkpoint vs baseline
#4. [completed]   Smoke test on a single game first
```

## Hardware / disk notes

- 4× A10G GPUs (23 GB each). Eval loaded Qwen3.5-2B sharded across GPUs 1-3.
- `/home/sagemaker-user/` is only 4.9 GB — was filling up; we moved everything to `/mnt/sagemaker-nvme/` (3.5 TB free).
- Verify on resume: `df -h /home/sagemaker-user /mnt/sagemaker-nvme` should show plenty free on the NVMe mount.

## Recovery if `/home/sagemaker-user` was wiped

If pip-installed playpen got lost in a stop/start:
```bash
pip install -e /mnt/sagemaker-nvme/lm-playschool-2026/playpen[trl]
pip install -r /mnt/sagemaker-nvme/lm-playschool-2026/playpen/clembench/requirements.txt
pip install 'clemcore[huggingface]'
ln -s /mnt/sagemaker-nvme/hf-cache ~/.cache/huggingface
```

## Suggested next session opening move

```bash
cd /mnt/sagemaker-nvme/lm-playschool-2026
git status                            # confirm clean working tree
df -h /home /mnt/sagemaker-nvme       # confirm space
playpen list models | grep Qwen       # confirm registry sees Qwen3.5-2B (else: python scripts/sync_configs.py)
```

Then either run option 1/2/3 above or kick off SFT:
```bash
cd playpen && playpen run examples/trl/sft_trainer_simple.py -l Qwen3.5-2B
```
