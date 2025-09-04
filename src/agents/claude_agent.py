"""Wrapper for the Anthropic Claude API."""
from __future__ import annotations

import os
import requests


class Agent:
    """Simple Claude API wrapper."""

    def __init__(self) -> None:
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        self.url = os.getenv("ANTHROPIC_API_URL", "https://api.anthropic.com/v1/messages")

    def run(self, prompt: str) -> str:
        if not self.api_key:
            raise RuntimeError("ANTHROPIC_API_KEY is not set")
        payload = {
            "model": os.getenv("ANTHROPIC_MODEL", "claude-3-opus-20240229"),
            "messages": [{"role": "user", "content": prompt}],
        }
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
        }
        response = requests.post(self.url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()
        return data.get("content", [{}])[0].get("text", "")

    def feedback(self, message: str) -> None:
        print(f"Claude agent feedback: {message}")
