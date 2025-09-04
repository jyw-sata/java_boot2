"""Cursor AI API용 래퍼."""
from __future__ import annotations

import json
import os
from urllib import request


class Agent:
    """간단한 Cursor API 래퍼."""

    def __init__(self) -> None:
        self.api_key = os.getenv("CURSOR_API_KEY")
        self.url = os.getenv("CURSOR_API_URL", "https://api.cursor.sh/v1/chat")

    def run(self, prompt: str) -> str:
        if not self.api_key:
            raise RuntimeError("CURSOR_API_KEY is not set")
        payload = json.dumps({"query": prompt}).encode()
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        req = request.Request(self.url, data=payload, headers=headers)
        with request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode())
        return data.get("response", "")

    def feedback(self, message: str) -> None:
        """파이프라인에서 전달된 피드백을 수신한다."""
        print(f"Cursor agent feedback: {message}")
