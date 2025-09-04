"""OpenAI ChatGPT API용 래퍼."""
from __future__ import annotations

import json
import os
from urllib import request


class Agent:
    """간단한 ChatGPT API 래퍼."""

    def __init__(self) -> None:
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.url = os.getenv(
            "OPENAI_API_URL", "https://api.openai.com/v1/chat/completions"
        )

    def run(self, prompt: str) -> str:
        if not self.api_key:
            raise RuntimeError("OPENAI_API_KEY is not set")
        payload = json.dumps(
            {
                "model": os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
                "messages": [{"role": "user", "content": prompt}],
            }
        ).encode()
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        req = request.Request(self.url, data=payload, headers=headers)
        with request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode())
        return data.get("choices", [{}])[0].get("message", {}).get("content", "")

    def feedback(self, message: str) -> None:
        """파이프라인에서 전달된 피드백을 수신한다."""
        print(f"ChatGPT agent feedback: {message}")
