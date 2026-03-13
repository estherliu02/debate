from __future__ import annotations

import json
from pathlib import Path

import yaml

from configs.topics import TOPICS
from configs.traits import TRAIT_LIBRARY
from core.evaluator import DialogueEvaluator
from core.openrouter_client import OpenRouterClient
from core.planner import Planner
from core.rollout import DebateRolloutEngine
from core.sampler import RejectionSampler
from schemas.plan_schema import ContentPlan
from utils.ids import make_run_id
from utils.json_utils import dump_json


class PipelineRunner:
    def __init__(self, config_path: str):
        self.config = yaml.safe_load(Path(config_path).read_text())
        self.client = OpenRouterClient()
        self.planner = Planner(self.client)
        self.rollout = DebateRolloutEngine(
            self.client,
            max_visible_turns=self.config["rollout"]["max_visible_turns"],
            use_state_summary=self.config["rollout"]["use_state_summary"],
            max_turn_retries=self.config["rollout"]["max_turn_retries"],
        )
        self.evaluator = DialogueEvaluator(self.client, self.config["evaluation"])
        self.sampler = RejectionSampler(self.config["run"]["max_attempts"])

    def run(self) -> dict:
        run_id = make_run_id()
        print(f"[{run_id}] Starting pipeline run...")
        
        topic_cfg = TOPICS[self.config["run"]["topic_key"]]
        trait_name = self.config["run"]["trait_name"]
        variant_name_a = self.config["run"]["variant_name_a"]
        variant_name_b = self.config["run"]["variant_name_b"]
        speaker_variants = {"A": variant_name_a, "B": variant_name_b}
        output_root = Path(__file__).resolve().parents[1] / self.config["run"]["output_root"]
        print(f"[{run_id}] Topic: {self.config['run']['topic_key']}, Trait: {trait_name}, A: {variant_name_a}, B: {variant_name_b}")

        reuse_plan_path = self.config["run"].get("reuse_plan_path")
        if reuse_plan_path:
            plan_path = Path(reuse_plan_path)
            if not plan_path.is_absolute():
                plan_path = Path(__file__).resolve().parents[1] / plan_path
            print(f"[{run_id}] Reusing content plan from: {plan_path}")
            content_plan = ContentPlan(**json.loads(plan_path.read_text()))
            plan_source = plan_path.name
        else:
            print(f"[{run_id}] Generating content plan...")
            content_plan = self.planner.generate_content_plan(
                topic_cfg=topic_cfg,
                turns_per_agent=self.config["run"]["turns_per_agent"],
            )
            topic_key = self.config["run"]["topic_key"]
            plan_source = f"{topic_key}_{run_id}.json"
            dump_json(output_root / "plans" / plan_source, content_plan.model_dump())
            print(f"[{run_id}] Content plan saved.")

        accepted = None
        last_eval = None
        eval_feedback = None
        max_attempts = self.config["run"]["max_attempts"]
        for attempt in range(1, max_attempts + 1):
            print(f"[{run_id}] Attempt {attempt}/{max_attempts}: Generating style plans...")
            style_bundle = {
                speaker: self.planner.generate_style_plan(
                    speaker, trait_name, variant, TRAIT_LIBRARY[trait_name][variant]["rules"],
                    eval_feedback=eval_feedback,
                )
                for speaker, variant in speaker_variants.items()
            }
            print(f"[{run_id}] Attempt {attempt}/{max_attempts}: Generating dialogue...")
            dialogue = self.rollout.generate_dialogue(
                topic_cfg=topic_cfg,
                content_plan=content_plan,
                style_bundle=style_bundle,
                trait_name=trait_name,
                speaker_variants=speaker_variants,
                eval_feedback=eval_feedback,
            )
            dump_json(output_root / "dialogues" / f"{run_id}_attempt{attempt}_dialogue.json", dialogue.model_dump())
            print(f"[{run_id}] Attempt {attempt}/{max_attempts}: Dialogue saved. Evaluating...")

            eval_result = self.evaluator.evaluate(
                dialogue=dialogue,
                content_plan=content_plan,
                trait_name=trait_name,
                speaker_variants=speaker_variants,
            )
            dump_json(output_root / "evals" / f"{run_id}_attempt{attempt}_eval.json", eval_result.model_dump())
            last_eval = eval_result
            if not self.sampler.should_accept(eval_result):
                eval_feedback = eval_result.reason
            print(f"[{run_id}] Attempt {attempt}/{max_attempts}: Evaluation complete. Accepted: {self.sampler.should_accept(eval_result)}")

            if self.sampler.should_accept(eval_result):
                accepted = dialogue
                accepted_payload = dialogue.model_dump()
                accepted_payload["content_plan_source"] = plan_source
                dump_json(output_root / "accepted" / f"{run_id}_accepted_dialogue.json", accepted_payload)
                print(f"[{run_id}] Dialogue accepted and saved!")
                break

        if accepted is None:
            print(f"[{run_id}] No dialogue accepted after {max_attempts} attempts.")
        print(f"[{run_id}] Pipeline run complete.")

        return {
            "run_id": run_id,
            "accepted": accepted is not None,
            "last_eval": None if last_eval is None else last_eval.model_dump(),
            "output_root": str(output_root),
            "plan_reused": bool(reuse_plan_path),
        }
