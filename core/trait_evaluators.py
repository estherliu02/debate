from __future__ import annotations

from abc import ABC, abstractmethod

from utils.text_metrics import count_words


class TraitEvaluator(ABC):
    """Base class for per-trait evaluation logic.

    Subclasses that evaluate programmatically set uses_llm = False.
    The main evaluator will skip asking the LLM for target_trait_score
    and call score() instead.

    Subclasses that delegate to the LLM set uses_llm = True, and
    score() will never be called — the LLM handles it via the prompt.

    generation_constraint() returns a hard instruction injected into the
    speaker turn prompt so generation and evaluation use the same rule.
    """

    uses_llm: bool = False

    @abstractmethod
    def score(self, dialogue, speaker_variants: dict[str, str]) -> tuple[int, str]:
        """Return (target_trait_score 1-5, reason string).
        speaker_variants maps speaker name to their variant, e.g. {"A": "active", "B": "baseline"}.
        """
        ...

    def generation_constraint(self, variant_name: str) -> str | None:
        """Return a hard constraint string to inject into the speaker turn prompt.
        Return None if no extra constraint is needed beyond the style rules."""
        return None

    def check_turn(self, turn, variant_name: str) -> tuple[bool, str]:
        """Validate a single generated turn against the trait constraint.
        Return (passed, reason). Default: always pass (no per-turn check needed)."""
        return True, ""

    def evaluation_guidance(self, speaker_variants: dict[str, str]) -> str | None:
        """Return trait-specific scoring guidance to inject into the evaluator prompt.
        Describes what the LLM should look for when scoring target_trait_score.
        Return None to use the generic guidance."""
        return None


class GenericLLMTraitEvaluator(TraitEvaluator):
    """LLM-evaluated trait that reads all guidance from TRAIT_LIBRARY.

    To add a new LLM-evaluated trait, just add it to TRAIT_LIBRARY with
    eval_guidance per variant and an optional eval_header at the trait level.
    No code changes needed here.
    """

    uses_llm = True

    def __init__(self, trait_name: str):
        self.trait_name = trait_name

    def score(self, dialogue, speaker_variants: dict[str, str]) -> tuple[int, str]:
        raise NotImplementedError

    def evaluation_guidance(self, speaker_variants: dict[str, str]) -> str | None:
        from configs.traits import TRAIT_LIBRARY
        trait = TRAIT_LIBRARY[self.trait_name]
        header = trait.get(
            "eval_header",
            f"Evaluate whether each speaker demonstrates '{self.trait_name}' as assigned.",
        )
        lines = [
            trait[variant]["eval_guidance"].format(s=s)
            for s, variant in speaker_variants.items()
        ]
        return header + "\n" + "\n".join(lines)


class VerbosityEvaluator(TraitEvaluator):
    """Programmatic evaluator for verbosity_bias — checks word counts directly."""

    uses_llm = False

    def generation_constraint(self, variant_name: str) -> str | None:
        from configs.traits import TRAIT_LIBRARY
        low, high = TRAIT_LIBRARY["verbosity_bias"][variant_name]["word_range"]
        return f"Your response MUST be between {low} and {high} words. Count carefully."

    def check_turn(self, turn, variant_name: str) -> tuple[bool, str]:
        from configs.traits import TRAIT_LIBRARY
        low, high = TRAIT_LIBRARY["verbosity_bias"][variant_name]["word_range"]
        n = count_words(turn.utterance)
        if n < low or n > high + 15:
            return False, f"Turn {turn.turn_id} (speaker {turn.speaker}) has {n} words, outside [{low}-{high}]."
        return True, ""

    def score(self, dialogue, speaker_variants: dict[str, str]) -> tuple[int, str]:
        from configs.traits import TRAIT_LIBRARY
        word_ranges = {
            speaker: tuple(TRAIT_LIBRARY["verbosity_bias"][variant]["word_range"])
            for speaker, variant in speaker_variants.items()
        }
        for turn in dialogue.turns:
            if turn.speaker not in word_ranges:
                continue
            low, high = word_ranges[turn.speaker]
            n = count_words(turn.utterance)
            if n < low or n > high + 15:
                return 1, (
                    f"Turn {turn.turn_id} (speaker {turn.speaker}) has {n} words, "
                    f"outside [{low}-{high}]."
                )
        return 5, "All turns within expected word-count range."


# Registry is auto-populated from TRAIT_LIBRARY.
# Traits with a programmatic evaluator override the generic entry below.
def _build_registry() -> dict[str, TraitEvaluator]:
    from configs.traits import TRAIT_LIBRARY
    registry = {
        trait_name: GenericLLMTraitEvaluator(trait_name)
        for trait_name in TRAIT_LIBRARY
    }
    registry["verbosity_bias"] = VerbosityEvaluator()
    return registry


TRAIT_EVALUATOR_REGISTRY: dict[str, TraitEvaluator] = _build_registry()
