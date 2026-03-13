from __future__ import annotations

from configs.models import MODEL_CONFIGS
from core.trait_evaluators import TRAIT_EVALUATOR_REGISTRY
from prompts.content_checker import build_content_check_prompt
from prompts.speaker_turn import build_speaker_turn_prompt
from schemas.dialogue_schema import Dialogue, DialogueTurn
from core.memory import AgentMemory, MemoryManager


class DebateRolloutEngine:
    def __init__(self, client, max_visible_turns: int = 4, use_state_summary: bool = True, max_turn_retries: int = 3):
        self.client = client
        self.memory_manager = MemoryManager(client, max_visible_turns=max_visible_turns)
        self.use_state_summary = use_state_summary
        self.max_turn_retries = max_turn_retries

    def _check_content_plan(self, turn: DialogueTurn, turn_plan) -> tuple[bool, str]:
        prompt = build_content_check_prompt(
            utterance=turn.utterance,
            content_goal=turn_plan.content_goal,
            key_claim=turn_plan.key_claim,
        )
        payload = self.client.complete_json(
            model=MODEL_CONFIGS["content_checker"]["model"],
            prompt=prompt,
            temperature=MODEL_CONFIGS["content_checker"]["temperature"],
            max_tokens=150,
        )
        return bool(payload["content_followed"]), payload["reason"]

    def generate_dialogue(self, topic_cfg: dict, content_plan, style_bundle: dict, trait_name: str, speaker_variants: dict[str, str], eval_feedback: str | None = None) -> Dialogue:
        memories = {
            "A": AgentMemory(
                agent_name="A",
                stance=topic_cfg["agent_a_stance"],
                style_rules=style_bundle["A"].behavioral_rules,
            ),
            "B": AgentMemory(
                agent_name="B",
                stance=topic_cfg["agent_b_stance"],
                style_rules=style_bundle["B"].behavioral_rules,
            ),
        }

        trait_evaluator = TRAIT_EVALUATOR_REGISTRY.get(trait_name)

        turns: list[DialogueTurn] = []
        for turn_plan in content_plan.turns:
            speaker = turn_plan.speaker
            memory = memories[speaker]
            speaker_variant = speaker_variants[speaker]
            hard_constraint = (
                trait_evaluator.generation_constraint(speaker_variant)
                if trait_evaluator else None
            )

            turn = None
            retry_feedback = None
            for attempt in range(1, self.max_turn_retries + 1):
                prompt = build_speaker_turn_prompt(
                    topic=content_plan.topic,
                    question=content_plan.debate_question,
                    speaker=speaker,
                    stance=memory.stance,
                    turn_id=turn_plan.turn_id,
                    content_goal=turn_plan.content_goal,
                    key_claim=turn_plan.key_claim,
                    response_target=turn_plan.target_response_to_previous,
                    style_rules=memory.style_rules,
                    visible_history=self.memory_manager.get_visible_history(memory),
                    self_state_summary=memory.private_state_summary,
                    hard_constraint=hard_constraint,
                    retry_feedback=retry_feedback,
                    dialogue_eval_feedback=eval_feedback,
                )
                payload = self.client.complete_json(
                    model=MODEL_CONFIGS["speaker"]["model"],
                    prompt=prompt,
                    temperature=MODEL_CONFIGS["speaker"]["temperature"],
                    max_tokens=700,
                )
                turn = DialogueTurn(**payload)

                # Phase 1: content plan check
                content_ok, content_reason = self._check_content_plan(turn, turn_plan)
                if not content_ok:
                    print(f"[turn {turn_plan.turn_id} attempt {attempt}/{self.max_turn_retries}] Content plan: {content_reason}")
                    if attempt < self.max_turn_retries:
                        retry_feedback = f"Content plan not followed: {content_reason}"
                    continue

                # Phase 2: trait check (programmatic only; LLM traits checked at dialogue level)
                if trait_evaluator:
                    trait_ok, trait_reason = trait_evaluator.check_turn(turn, speaker_variant)
                    if not trait_ok:
                        print(f"[turn {turn_plan.turn_id} attempt {attempt}/{self.max_turn_retries}] Trait: {trait_reason}")
                        if attempt < self.max_turn_retries:
                            retry_feedback = (
                                f"Trait not demonstrated: {trait_reason}. "
                                "Also ensure the content plan is still followed."
                            )
                        continue

                break  # both checks passed (or retries exhausted)

            turns.append(turn)
            self.memory_manager.add_turn(memories, speaker=turn.speaker, utterance=turn.utterance)
            if self.use_state_summary:
                self.memory_manager.update_private_summary(memories[speaker])

        return Dialogue(
            topic=content_plan.topic,
            trait_name=trait_name,
            variant_name_a=speaker_variants["A"],
            variant_name_b=speaker_variants["B"],
            turns=turns,
        )
