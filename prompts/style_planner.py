def build_style_prompt(agent_name: str, trait_name: str, variant_name: str, trait_rules: list[str], eval_feedback: str | None = None) -> str:
    bullets = "\n".join(f"- {r}" for r in trait_rules)
    feedback_block = (
        f"\nA previous dialogue using this style plan was rejected for the following reason:\n"
        f"{eval_feedback}\n"
        f"Generate stronger, more concrete behavioral rules that directly fix this failure."
    ) if eval_feedback else ""
    return f"""
You are writing a style plan for one debate speaker.

Agent: {agent_name}
Trait: {trait_name}
Variant: {variant_name}

Behavioral rules:
{bullets}
{feedback_block}
Return valid JSON with this structure:
{{
  "agent_name": "{agent_name}",
  "target_trait": "{trait_name}:{variant_name}",
  "behavioral_rules": ["..."],
  "forbidden_patterns": ["..."]
}}

The forbidden patterns should prevent the speaker from reverting to neutral or balanced behavior.
""".strip()
