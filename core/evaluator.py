from __future__ import annotations

import json

from configs.models import MODEL_CONFIGS
from core.trait_evaluators import TRAIT_EVALUATOR_REGISTRY
from prompts.evaluator import build_evaluator_prompt
from schemas.eval_schema import EvalResult
from utils.text_metrics import dialogue_to_text


class DialogueEvaluator:
    def __init__(self, client, thresholds: dict):
        self.client = client
        self.thresholds = thresholds

    def evaluate(self, dialogue, content_plan, trait_name: str, speaker_variants: dict[str, str]) -> EvalResult:
        trait_evaluator = TRAIT_EVALUATOR_REGISTRY.get(trait_name)
        programmatic = trait_evaluator is not None and not trait_evaluator.uses_llm

        trait_guidance = (
            trait_evaluator.evaluation_guidance(speaker_variants)
            if trait_evaluator else None
        )
        prompt = build_evaluator_prompt(
            dialogue_text=dialogue_to_text(dialogue),
            content_plan_json=json.dumps(content_plan.model_dump(), ensure_ascii=False, indent=2),
            trait_name=trait_name,
            variant_name=speaker_variants["A"],
            include_trait_score=not programmatic,
            trait_guidance=trait_guidance,
        )
        payload = self.client.complete_json(
            model=MODEL_CONFIGS["evaluator"]["model"],
            prompt=prompt,
            temperature=MODEL_CONFIGS["evaluator"]["temperature"],
            max_tokens=700,
        )
        print("[debug] evaluator payload:", payload)

        content_alignment_score = payload["content_alignment_score"]
        naturalness_score = payload["naturalness_score"]

        if programmatic:
            target_trait_score, reason = trait_evaluator.score(dialogue, speaker_variants)
            print(f"[{trait_name}] {reason}")
        else:
            target_trait_score = payload["target_trait_score"]
            reason = payload["reason"]
            if (
                target_trait_score == 1
                and content_alignment_score == 1
                and naturalness_score == 1
                and any(
                    phrase in reason.lower()
                    for phrase in [
                        "aligns well",
                        "flows naturally",
                        "appropriate to the target trait",
                        "faithful to the content plan",
                        "realistic discussion",
                    ]
                )
            ):
                print("[warning] evaluator scores look inconsistent with reason text.")

        passed = (
            target_trait_score >= self.thresholds["min_target_trait_score"]
            and content_alignment_score >= self.thresholds["min_content_alignment_score"]
            and naturalness_score >= self.thresholds["min_naturalness_score"]
        )
        return EvalResult(
            target_trait_score=target_trait_score,
            content_alignment_score=content_alignment_score,
            naturalness_score=naturalness_score,
            passed=passed,
            reason=reason,
        )
