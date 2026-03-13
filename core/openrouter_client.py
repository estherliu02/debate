from __future__ import annotations

import json
import os
import time
from typing import Any, Dict

import requests


_RETRY_ATTEMPTS = 3
_RETRY_DELAY = 5  # seconds between retries


class OpenRouterClient:
    def __init__(self, api_key: str | None = None, base_url: str = "https://openrouter.ai/api/v1"):
        self.api_key = api_key or os.environ.get("OPENROUTER_API_KEY")
        if not self.api_key:
            raise ValueError("Missing OPENROUTER_API_KEY. Set it in your environment.")
        self.base_url = base_url.rstrip("/")

    def _post(self, payload: dict) -> requests.Response:
        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        last_exc = None
        for attempt in range(1, _RETRY_ATTEMPTS + 1):
            try:
                resp = requests.post(url, headers=headers, json=payload, timeout=120)
                resp.raise_for_status()
                return resp
            except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
                last_exc = e
                print(f"[openrouter] attempt {attempt}/{_RETRY_ATTEMPTS} failed ({type(e).__name__}). Retrying in {_RETRY_DELAY}s...")
                if attempt < _RETRY_ATTEMPTS:
                    time.sleep(_RETRY_DELAY)
        raise last_exc

    def complete_json(self, model: str, prompt: str, temperature: float = 0.2, max_tokens: int = 1200) -> Dict[str, Any]:
        payload = {
            "model": model,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "messages": [
                {"role": "system", "content": "You are a careful assistant that always returns valid JSON when asked."},
                {"role": "user", "content": prompt},
            ],
            "response_format": {"type": "json_object"},
        }
        resp = self._post(payload)
        content = resp.json()["choices"][0]["message"]["content"]
        return json.loads(content)

    def complete_text(self, model: str, prompt: str, temperature: float = 0.2, max_tokens: int = 400) -> str:
        payload = {
            "model": model,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "messages": [
                {"role": "system", "content": "You are a careful assistant."},
                {"role": "user", "content": prompt},
            ],
        }
        resp = self._post(payload)
        return resp.json()["choices"][0]["message"]["content"]
