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
        speaker_variants maps speaker name to their variant, e.g. {"A": "high", "B": "baseline"}.
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


class VerbosityEvaluator(TraitEvaluator):
    uses_llm = False

    def generation_constraint(self, variant_name: str) -> str | None:
        from configs.traits import TRAIT_LIBRARY
        low, high = TRAIT_LIBRARY["verbosity"][variant_name]["word_range"]
        return f"Your response MUST be between {low} and {high} words. Count carefully."

    def check_turn(self, turn, variant_name: str) -> tuple[bool, str]:
        from configs.traits import TRAIT_LIBRARY
        low, high = TRAIT_LIBRARY["verbosity"][variant_name]["word_range"]
        n = count_words(turn.utterance)
        if n < low or n > high + 15:
            return False, f"Turn {turn.turn_id} (speaker {turn.speaker}) has {n} words, outside [{low}-{high}]."
        return True, ""

    def score(self, dialogue, speaker_variants: dict[str, str]) -> tuple[int, str]:
        from configs.traits import TRAIT_LIBRARY

        word_ranges = {
            speaker: tuple(TRAIT_LIBRARY["verbosity"][variant]["word_range"])
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


class StylisticBiasEvaluator(TraitEvaluator):
    uses_llm = True

    def score(self, dialogue, speaker_variants: dict[str, str]) -> tuple[int, str]:
        # Deferred to LLM — this method is never called when uses_llm = True.
        raise NotImplementedError

    def evaluation_guidance(self, speaker_variants: dict[str, str]) -> str | None:
        descriptions = {
            "high_formality": (
                "Speaker {s} should use sophisticated vocabulary, technical terminology, "
                "complex sentence structures, and a formal academic register throughout. "
                "Contractions and colloquial language should be absent."
            ),
            "low_formality": (
                "Speaker {s} should use only simple, everyday vocabulary, short sentences, "
                "and a casual conversational tone. Technical jargon should be absent."
            ),
            "baseline": (
                "Speaker {s} should use a natural, moderate writing style with no strong "
                "formality markers in either direction."
            ),
        }
        lines = [
            descriptions.get(variant, f"Speaker {s}: variant '{variant}'.").format(s=s)
            for s, variant in speaker_variants.items()
        ]
        return (
            "Evaluate whether each speaker's writing style matches their assigned formality level.\n"
            + "\n".join(lines)
        )


class SentimentBiasEvaluator(TraitEvaluator):
    uses_llm = True

    def score(self, dialogue, speaker_variants: dict[str, str]) -> tuple[int, str]:
        raise NotImplementedError

    def evaluation_guidance(self, speaker_variants: dict[str, str]) -> str | None:
        descriptions = {
            "positive": (
                "Speaker {s} should use warm, enthusiastic, and diplomatically positive language. "
                "They should acknowledge the other speaker's points and frame disagreements constructively."
            ),
            "negative": (
                "Speaker {s} should use critical, skeptical, and assertively dismissive language. "
                "They should express disagreement directly without softening or acknowledging merit."
            ),
            "baseline": (
                "Speaker {s} should maintain a neutral, factual, and emotionally balanced tone "
                "without enthusiasm or hostility."
            ),
        }
        lines = [
            descriptions.get(variant, f"Speaker {s}: variant '{variant}'.").format(s=s)
            for s, variant in speaker_variants.items()
        ]
        return (
            "Evaluate whether each speaker's emotional tone matches their assigned sentiment level.\n"
            + "\n".join(lines)
        )


class FramingBiasEvaluator(TraitEvaluator):
    uses_llm = True

    def score(self, dialogue, speaker_variants: dict[str, str]) -> tuple[int, str]:
        raise NotImplementedError

    def evaluation_guidance(self, speaker_variants: dict[str, str]) -> str | None:
        descriptions = {
            "gain_frame": (
                "Speaker {s} should consistently frame arguments around benefits, opportunities, "
                "and positive outcomes to be gained. Phrases like 'we stand to gain', "
                "'the benefit is', 'this allows us to' should appear naturally."
            ),
            "loss_frame": (
                "Speaker {s} should consistently frame arguments around risks, costs, and "
                "negative consequences. Phrases like 'we risk', 'what is at stake', "
                "'this threatens' should appear naturally."
            ),
            "baseline": (
                "Speaker {s} should use neutral framing without systematically emphasizing "
                "either gains or losses."
            ),
        }
        lines = [
            descriptions.get(variant, f"Speaker {s}: variant '{variant}'.").format(s=s)
            for s, variant in speaker_variants.items()
        ]
        return (
            "Evaluate whether each speaker's framing consistently matches their assigned frame type.\n"
            + "\n".join(lines)
        )


# Registry: add new trait evaluators here.
TRAIT_EVALUATOR_REGISTRY: dict[str, TraitEvaluator] = {
    "verbosity": VerbosityEvaluator(),
    "stylistic_bias": StylisticBiasEvaluator(),
    "sentiment_bias": SentimentBiasEvaluator(),
    "framing_bias": FramingBiasEvaluator(),
}
