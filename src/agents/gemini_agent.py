"""Wrapper for the Google Gemini API."""
from __future__ import annotations

import os
import requests


class Agent:
    """Simple Gemini API wrapper."""

    def __init__(self) -> None:
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.url = os.getenv(
            "GEMINI_API_URL",
            "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent",
        )

    def run(self, prompt: str) -> str:
        if not self.api_key:
            raise RuntimeError("GEMINI_API_KEY is not set")
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        params = {"key": self.api_key}
        response = requests.post(self.url, params=params, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        return (
            data.get("candidates", [{}])[0]
            .get("content", {})
            .get("parts", [{}])[0]
            .get("text", "")
        )

    def feedback(self, message: str) -> None:
        print(f"Gemini agent feedback: {message}")
