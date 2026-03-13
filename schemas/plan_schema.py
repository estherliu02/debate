from pydantic import BaseModel
from typing import List

class TurnPlan(BaseModel):
    turn_id: int
    speaker: str
    content_goal: str
    key_claim: str
    target_response_to_previous: str | None = None

class ContentPlan(BaseModel):
    topic: str
    debate_question: str
    agent_a_stance: str
    agent_b_stance: str
    turns: List[TurnPlan]