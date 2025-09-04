"""Anthropic Claude API용 래퍼."""
from __future__ import annotations

import json
import os
from urllib import request


class Agent:
    """간단한 Claude API 래퍼."""

    def __init__(self) -> None:
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        self.url = os.getenv("ANTHROPIC_API_URL", "https://api.anthropic.com/v1/messages")

    def run(self, prompt: str) -> str:
        if not self.api_key:
            raise RuntimeError("ANTHROPIC_API_KEY is not set")
        payload = json.dumps(
            {
                "model": os.getenv("ANTHROPIC_MODEL", "claude-3-opus-20240229"),
                "messages": [{"role": "user", "content": prompt}],
            }
        ).encode()
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json",
        }
        req = request.Request(self.url, data=payload, headers=headers)
        with request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode())
        return data.get("content", [{}])[0].get("text", "")

    def feedback(self, message: str) -> None:
        """파이프라인에서 전달된 피드백을 수신한다."""
        print(f"Claude agent feedback: {message}")
