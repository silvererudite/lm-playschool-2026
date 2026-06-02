"""Merge our config overrides into the upstream playpen repo.

Reads `configs/qwen-model-entries.json` (our entries) and merges them into
`playpen/model_registry.json` (upstream), keyed by `model_name`. Existing
entries with the same name are replaced; everything else upstream is preserved.

Run from workspace root:
    python scripts/sync_configs.py
"""
import json
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent
OURS = WORKSPACE / "configs" / "qwen-model-entries.json"
UPSTREAM = WORKSPACE / "playpen" / "model_registry.json"


def main() -> None:
    ours = json.loads(OURS.read_text())
    upstream = json.loads(UPSTREAM.read_text())

    our_names = {e["model_name"] for e in ours}
    merged = [e for e in upstream if e["model_name"] not in our_names] + ours

    UPSTREAM.write_text(json.dumps(merged, indent=2) + "\n")
    print(f"Synced {len(ours)} entries into {UPSTREAM}")
    for e in ours:
        print(f"  - {e['model_name']}")


if __name__ == "__main__":
    main()
