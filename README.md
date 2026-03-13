# debate_gen

Minimal debate-generation pipeline for a single trait: **verbosity**.

## What it does
- Creates one shared **content plan**.
- Creates one **style plan** for each speaker.
- Runs **turn-by-turn rollout** with memory injection.
- Evaluates the generated dialogue with **rejection sampling**.
- Saves plans, dialogues, evals, and accepted outputs.

## Current MVP behavior
- Only supports the `verbosity` trait.
- Only changes **speaker A** to the target variant (`high` or `low`).
- Keeps **speaker B** at `baseline` verbosity.

## Setup
```bash
cd debate_gen
python -m venv .venv
source .venv/bin/activate
pip install pydantic pyyaml requests
export OPENROUTER_API_KEY="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"
python run_generate.py
```

## Main flow
1. `core/planner.py` generates a shared content plan.
2. `core/planner.py` also generates two style plans.
3. `core/rollout.py` performs turn-by-turn generation.
4. `core/memory.py` injects recent history and a short private state summary.
5. `core/evaluator.py` scores the dialogue.
6. `core/sampler.py` accepts or retries.

## Next extensions
- add `baseline` vs `high` pair generation in one run
- add word-count hard checks before LLM evaluation
- add pairwise evaluator to ensure only verbosity changes
- add more traits such as receptiveness or confirmation bias
