from typing import List, Optional
from pydantic import BaseModel


class DialogueTurn(BaseModel):
    turn_id: int
    speaker: str
    utterance: str
    self_state_update: Optional[str] = None
    content_fidelity_note: Optional[str] = None


class Dialogue(BaseModel):
    topic: str
    trait_name: str
    variant_name_a: str
    variant_name_b: str
    turns: List[DialogueTurn]
