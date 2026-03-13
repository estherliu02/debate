def build_content_check_prompt(utterance: str, content_goal: str, key_claim: str) -> str:
    return f"""
Does the following debate utterance address its assigned content goal and make its key claim?

Content goal: {content_goal}
Key claim: {key_claim}

Utterance:
{utterance}

Return valid JSON only:
{{
  "content_followed": true or false,
  "reason": "one sentence explanation"
}}

Return true only if the utterance clearly addresses the content goal and makes the key claim.
Return false if the utterance drifts, ignores the goal, or omits the key claim entirely.
""".strip()
