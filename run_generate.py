from pathlib import Path

import yaml

from core.pipeline import PipelineRunner

if __name__ == "__main__":
    print("[start] launching debate generation pipeline...")

    config_path = Path(__file__).parent / "configs" / "generation.yaml"
    config = yaml.safe_load(config_path.read_text())

    runner = PipelineRunner(config=config)

    result = runner.run()

    print("[done] pipeline finished.")
    print(result)
