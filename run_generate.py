from pathlib import Path
from core.pipeline import PipelineRunner

if __name__ == "__main__":
    print("[start] launching debate generation pipeline...")

    config_path = Path(__file__).parent / "configs" / "generation.yaml"

    runner = PipelineRunner(config_path=str(config_path))

    result = runner.run()

    print("[done] pipeline finished.")
    print(result)