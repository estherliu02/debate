from __future__ import annotations

from dataclasses import dataclass

from configs.models import MODEL_CONFIGS
from prompts.content_planner import build_content_planner_prompt
from prompts.style_planner import build_style_prompt
from schemas.plan_schema import ContentPlan


@dataclass
class StylePlan:
    agent_name: str
    target_trait: str
    behavioral_rules: list[str]
    forbidden_patterns: list[str]


class Planner:
    def __init__(self, client):
        self.client = client
        
    def _normalize_content_plan_payload(self, payload: dict) -> dict:
            for turn in payload.get("turns", []):
                value = turn.get("target_response_to_previous")
                if isinstance(value, int):
                    turn["target_response_to_previous"] = f"Responds to turn {value}"
                elif value is not None and not isinstance(value, str):
                    turn["target_response_to_previous"] = str(value)
            return payload
        
    def generate_content_plan(self, topic_cfg: dict, turns_per_agent: int) -> ContentPlan:

        prompt = build_content_planner_prompt(
            topic=topic_cfg["topic"],
            question=topic_cfg["question"],
            stance_a=topic_cfg["agent_a_stance"],
            stance_b=topic_cfg["agent_b_stance"],
            turns_per_agent=turns_per_agent,
        )
        payload = self.client.complete_json(
            model=MODEL_CONFIGS["planner"]["model"],
            prompt=prompt,
            temperature=MODEL_CONFIGS["planner"]["temperature"],
            max_tokens=1800,
        )
        payload = self._normalize_content_plan_payload(payload)
        return ContentPlan(**payload)

    def generate_style_plan(self, agent_name: str, trait_name: str, variant_name: str, trait_rules: list[str], eval_feedback: str | None = None) -> StylePlan:
        prompt = build_style_prompt(agent_name, trait_name, variant_name, trait_rules, eval_feedback=eval_feedback)
        payload = self.client.complete_json(
            model=MODEL_CONFIGS["planner"]["model"],
            prompt=prompt,
            temperature=MODEL_CONFIGS["planner"]["temperature"],
            max_tokens=700,
        )
        return StylePlan(**payload)
