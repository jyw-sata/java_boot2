"""Wrapper for the OpenAI ChatGPT API."""
from __future__ import annotations

import os
import requests


class Agent:
    """Simple ChatGPT API wrapper."""

    def __init__(self) -> None:
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.url = os.getenv(
            "OPENAI_API_URL", "https://api.openai.com/v1/chat/completions"
        )

    def run(self, prompt: str) -> str:
        if not self.api_key:
            raise RuntimeError("OPENAI_API_KEY is not set")
        payload = {
            "model": os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
            "messages": [{"role": "user", "content": prompt}],
        }
        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = requests.post(self.url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()
        return data.get("choices", [{}])[0].get("message", {}).get("content", "")

    def feedback(self, message: str) -> None:
        """Receive feedback from pipeline."""
        print(f"ChatGPT agent feedback: {message}")
