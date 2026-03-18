"""Batch data generation — runs all traits against baseline for both speaker orderings.

For each trait in TRAIT_LIBRARY two runs are executed:
    active   vs baseline  (speaker A has the biased variant)
    baseline vs active    (speaker B has the biased variant)

The content plan is generated once per topic and reused across all runs.
All other settings are read from configs/generation.yaml.

Usage:
    python run_batch.py
"""

import copy
from datetime import datetime
from pathlib import Path

import yaml

from configs.traits import TRAIT_LIBRARY
from core.pipeline import PipelineRunner

CONFIG_PATH = Path(__file__).parent / "configs" / "generation.yaml"


def main() -> None:
    base_config = yaml.safe_load(CONFIG_PATH.read_text())

    # Use a single date-stamped output folder for the whole batch.
    date_tag = datetime.now().strftime("%m%d")
    base_config["run"]["output_root"] = f"outputs/{date_tag}"

    # Remove any hardcoded reuse_plan_path from the yaml — the batch manages this.
    base_config["run"].pop("reuse_plan_path", None)

    topic_key = base_config["run"]["topic_key"]

    # Build run list: (trait_name, variant_a, variant_b)
    runs = []
    for trait_name in TRAIT_LIBRARY:
        runs.append((trait_name, "active",   "baseline"))
        runs.append((trait_name, "baseline", "active"))

    total = len(runs)
    print(f"[batch] {total} runs scheduled for topic '{topic_key}' → outputs/{date_tag}/")
    print(f"[batch] traits: {', '.join(TRAIT_LIBRARY)}\n")

    # plan_paths[topic_key] is set after the first run generates a plan.
    plan_paths: dict[str, str] = {}

    for i, (trait_name, variant_a, variant_b) in enumerate(runs, 1):
        print(f"[batch] ── run {i}/{total}: {trait_name}  A={variant_a}  B={variant_b} ──")

        config = copy.deepcopy(base_config)
        config["run"]["trait_name"]     = trait_name
        config["run"]["variant_name_a"] = variant_a
        config["run"]["variant_name_b"] = variant_b

        if topic_key in plan_paths:
            config["run"]["reuse_plan_path"] = plan_paths[topic_key]

        result = PipelineRunner(config=config).run()

        # Capture plan path from first run so all subsequent runs reuse it.
        if topic_key not in plan_paths:
            plan_paths[topic_key] = result["plan_path"]
            print(f"[batch] plan saved → {result['plan_path']}")

        status = "accepted" if result["accepted"] else "REJECTED"
        print(f"[batch] run {i}/{total} {status}\n")

    print(f"[batch] done. outputs in outputs/{date_tag}/")


if __name__ == "__main__":
    main()
