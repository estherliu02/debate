def build_content_planner_prompt(topic: str, question: str, stance_a: str, stance_b: str, turns_per_agent: int) -> str:
    total_turns = turns_per_agent * 2
    return f"""
You are creating a debate content plan.

Goal:
Create a content skeleton that is stable across later style variants.
The content should stay the same even when verbosity changes later.
Do not include any stylistic instructions. Do not mention verbosity.

For each turn, output:
- turn_id: integer
- speaker: "A" or "B"
- content_goal: short string
- key_claim: short string
- target_response_to_previous: null or a short natural-language string

Important:
- `target_response_to_previous` must NOT be a number.
- Do not output turn indices in that field.
- If the turn directly responds to a previous point, describe the point in words.

Debate topic: {topic}
Debate question: {question}
Agent A stance: {stance_a}
Agent B stance: {stance_b}
Total turns: {total_turns}, alternating strictly A/B starting with A.

Return valid JSON with this structure:
{{
  "topic": "...",
  "debate_question": "...",
  "agent_a_stance": "...",
  "agent_b_stance": "...",
  "turns": [
    {{
      "turn_id": 1,
      "speaker": "A",
      "content_goal": "...",
      "key_claim": "...",
      "target_response_to_previous": null
    }}
  ]
}}

Requirements:
- Make each turn content-specific and cumulative.
- Keep both sides thoughtful and realistic.
- Avoid convergence to full agreement.
- Make turn goals parallel enough that multiple style variants can reuse them.
""".strip()
