"""파이프라인 동작과 재시도 로직을 테스트한다."""
from __future__ import annotations

import importlib
import os
import sys
import types
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from multi_agent_pipeline import AGENT_MODULES, run_pipeline


def test_run_pipeline_success(monkeypatch):
    class DummyAgent:
        def run(self, prompt: str) -> str:
            return "ok"

        def feedback(self, message: str) -> None:
            self.message = message

    def fake_import(name: str):
        return types.SimpleNamespace(Agent=DummyAgent)

    monkeypatch.setattr(importlib, "import_module", fake_import)
    monkeypatch.setattr("multi_agent_pipeline.notify", lambda msg: None)

    responses = run_pipeline("hello")
    assert set(responses) == set(AGENT_MODULES)
    assert all(responses.values())


def test_run_pipeline_retry(monkeypatch):
    class FlakyAgent:
        def __init__(self) -> None:
            self.count = 0

        def run(self, prompt: str) -> str:
            if self.count == 0:
                self.count += 1
                raise RuntimeError("boom")
            return "ok"

        def feedback(self, message: str) -> None:
            self.last_feedback = message

    def fake_import(name: str):
        return types.SimpleNamespace(Agent=FlakyAgent)

    monkeypatch.setattr(importlib, "import_module", fake_import)
    monkeypatch.setattr("multi_agent_pipeline.notify", lambda msg: None)

    responses = run_pipeline("hi", max_retries=2)
    assert all(responses.values())
