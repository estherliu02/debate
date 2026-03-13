from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Dict

from prompts.state_summarizer import build_state_summarizer_prompt
from configs.models import MODEL_CONFIGS


@dataclass
class AgentMemory:
    agent_name: str
    stance: str
    style_rules: list[str]
    dialogue_history: List[Dict[str, str]] = field(default_factory=list)
    private_state_summary: str | None = None


class MemoryManager:
    def __init__(self, client, max_visible_turns: int = 4):
        self.client = client
        self.max_visible_turns = max_visible_turns

    def add_turn(self, memories: dict[str, AgentMemory], speaker: str, utterance: str):
        for memory in memories.values():
            memory.dialogue_history.append({"speaker": speaker, "text": utterance})

    def get_visible_history(self, memory: AgentMemory) -> str:
        history = memory.dialogue_history[-self.max_visible_turns :]
        if not history:
            return "No previous turns."
        lines = []
        for item in history:
            lines.append(f"{item['speaker']}: {item['text']}")
        return "\n".join(lines)

    def update_private_summary(self, memory: AgentMemory):
        recent = self.get_visible_history(memory)
        prompt = build_state_summarizer_prompt(memory.agent_name, memory.private_state_summary, recent)
        summary = self.client.complete_text(
            model=MODEL_CONFIGS["summarizer"]["model"],
            prompt=prompt,
            temperature=MODEL_CONFIGS["summarizer"]["temperature"],
            max_tokens=180,
        )
        memory.private_state_summary = summary.strip()
