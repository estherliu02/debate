from pydantic import BaseModel


class EvalResult(BaseModel):
    target_trait_score: int
    content_alignment_score: int
    naturalness_score: int
    passed: bool
    reason: str
