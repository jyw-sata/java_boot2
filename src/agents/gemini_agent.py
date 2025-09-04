"""Google Gemini API용 래퍼."""
from __future__ import annotations

import json
import os
from urllib import parse, request


class Agent:
    """간단한 Gemini API 래퍼."""

    def __init__(self) -> None:
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.url = os.getenv(
            "GEMINI_API_URL",
            "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent",
        )

    def run(self, prompt: str) -> str:
        if not self.api_key:
            raise RuntimeError("GEMINI_API_KEY is not set")
        payload = json.dumps({"contents": [{"parts": [{"text": prompt}]}]}).encode()
        params = parse.urlencode({"key": self.api_key})
        url = f"{self.url}?{params}"
        req = request.Request(
            url, data=payload, headers={"Content-Type": "application/json"}
        )
        with request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode())
        return (
            data.get("candidates", [{}])[0]
            .get("content", {})
            .get("parts", [{}])[0]
            .get("text", "")
        )

    def feedback(self, message: str) -> None:
        """파이프라인에서 전달된 피드백을 수신한다."""
        print(f"Gemini agent feedback: {message}")
