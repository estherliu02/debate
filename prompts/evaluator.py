def build_evaluator_prompt(
    dialogue_text: str,
    content_plan_json: str,
    trait_name: str,
    variant_name: str,
    include_trait_score: bool = True,
    trait_guidance: str | None = None,
) -> str:
    if include_trait_score:
        trait_score_detail = (
            f"  Specifically: {trait_guidance}"
            if trait_guidance
            else "  1 = the target trait is absent or clearly wrong\n"
                 "  3 = the target trait is somewhat present but weak/inconsistent\n"
                 "  5 = the target trait is clearly present and appropriately subtle"
        )
        return f"""
You are evaluating whether a generated debate dialogue matches its assigned content plan and target trait.

Target trait: {trait_name}
Target variant: {variant_name}

Content plan:
{content_plan_json}

Dialogue:
{dialogue_text}

Return valid JSON only, with exactly these keys:
{{
  "target_trait_score": <integer 1-5>,
  "content_alignment_score": <integer 1-5>,
  "naturalness_score": <integer 1-5>,
  "passed": <true or false>,
  "reason": "<short explanation>"
}}

Scoring guidance:
- target_trait_score:
{trait_score_detail}

- content_alignment_score:
  1 = the dialogue substantially drifts from the content plan
  3 = partial alignment, but some turns drift or miss intended goals
  5 = each turn stays faithful to the content plan

- naturalness_score:
  1 = unnatural, templated, or robotic
  3 = somewhat natural but uneven
  5 = realistic and natural discussion

Set "passed" to true if and only if:
- target_trait_score >= 4
- content_alignment_score >= 4
- naturalness_score >= 4

Important:
- Do not copy placeholder values.
- Fill in all scores based on your actual evaluation.
- Return JSON only, with no extra text.
""".strip()

    else:
        return f"""
You are evaluating whether a generated debate dialogue matches its assigned content plan.

Content plan:
{content_plan_json}

Dialogue:
{dialogue_text}

Return valid JSON only, with exactly these keys:
{{
  "content_alignment_score": <integer 1-5>,
  "naturalness_score": <integer 1-5>,
  "passed": <true or false>,
  "reason": "<short explanation>"
}}

Scoring guidance:
- content_alignment_score:
  1 = the dialogue substantially drifts from the content plan
  3 = partial alignment, but some turns drift or miss intended goals
  5 = each turn stays faithful to the content plan

- naturalness_score:
  1 = unnatural, templated, or robotic
  3 = somewhat natural but uneven
  5 = realistic and natural discussion

Set "passed" to true if and only if:
- content_alignment_score >= 4
- naturalness_score >= 4

Important:
- Do not copy placeholder values.
- Fill in all scores based on your actual evaluation.
- Return JSON only, with no extra text.
""".strip()