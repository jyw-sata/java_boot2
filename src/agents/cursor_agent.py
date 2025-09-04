"""Wrapper for the Cursor AI API."""
from __future__ import annotations

import os
import requests


class Agent:
    """Simple Cursor API wrapper."""

    def __init__(self) -> None:
        self.api_key = os.getenv("CURSOR_API_KEY")
        self.url = os.getenv("CURSOR_API_URL", "https://api.cursor.sh/v1/chat")

    def run(self, prompt: str) -> str:
        if not self.api_key:
            raise RuntimeError("CURSOR_API_KEY is not set")
        payload = {"query": prompt}
        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = requests.post(self.url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()
        return data.get("response", "")

    def feedback(self, message: str) -> None:
        print(f"Cursor agent feedback: {message}")
