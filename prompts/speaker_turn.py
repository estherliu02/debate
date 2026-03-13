def build_speaker_turn_prompt(
    topic: str,
    question: str,
    speaker: str,
    stance: str,
    turn_id: int,
    content_goal: str,
    key_claim: str,
    response_target: str | None,
    style_rules: list[str],
    visible_history: str,
    self_state_summary: str | None,
    hard_constraint: str | None = None,
    retry_feedback: str | None = None,
    dialogue_eval_feedback: str | None = None,
) -> str:
    style_text = "\n".join(f"- {r}" for r in style_rules)
    response_line = response_target or "No direct response target for this turn."
    state_block = self_state_summary or "No prior private summary."
    constraint_block = f"\nHard constraint: {hard_constraint}" if hard_constraint else ""
    feedback_block = f"\nPrevious attempt was rejected — reason: {retry_feedback}\nFix this in your response." if retry_feedback else ""
    dialogue_feedback_block = f"\nThe previous full dialogue attempt was rejected — reason: {dialogue_eval_feedback}\nCorrect this throughout your response." if dialogue_eval_feedback else ""
    return f"""
You are generating one turn in a multi-turn debate.

Topic: {topic}
Question: {question}
You are speaker {speaker}.
Your stance: {stance}
Current turn id: {turn_id}

This turn's content goal:
{content_goal}

This turn's key claim:
{key_claim}

What you should respond to from the previous turn:
{response_line}

Your style rules:
{style_text}{constraint_block}{feedback_block}{dialogue_feedback_block}

Recent visible history:
{visible_history}

Your private running state summary:
{state_block}

Return valid JSON with this structure:
{{
  "turn_id": {turn_id},
  "speaker": "{speaker}",
  "utterance": "...",
  "self_state_update": "1-2 sentence summary of your current stance and what you want to emphasize next.",
  "content_fidelity_note": "1 short sentence about whether you followed the assigned content goal."
}}

Requirements:
- Keep the content aligned with the assigned turn goal.
- Do not change the core argument trajectory.
- Stay natural and realistic.
- Express the assigned style only through length and amount of elaboration.
- Do not mention style instructions explicitly.
""".strip()
