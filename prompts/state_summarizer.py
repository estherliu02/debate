def build_state_summarizer_prompt(agent_name: str, prior_summary: str | None, recent_turns: str) -> str:
    prior_summary = prior_summary or "No previous summary."
    return f"""
Summarize the internal state of debate speaker {agent_name} after the recent turns.

Previous summary:
{prior_summary}

Recent turns:
{recent_turns}

Return one short paragraph only. Focus on:
- current stance
- which point they are emphasizing
- what they seem likely to do next
""".strip()
