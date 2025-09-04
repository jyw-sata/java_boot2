"""JSON 스키마 검증을 포함한 동적 멀티 에이전트 파이프라인."""
from __future__ import annotations

import importlib
import json
from pathlib import Path
from typing import Dict, List

from src.telegram_notifier import notify

AGENT_MODULES: List[str] = [
    "chatgpt_agent",
    "claude_agent",
    "gemini_agent",
    "cursor_agent",
]


def validate(data: Dict[str, object], schema: Dict[str, object]) -> None:
    """아주 단순한 JSON 스키마 검증 함수."""
    for key in schema.get("required", []):
        if key not in data:
            raise ValueError(f"필수 항목 누락: {key}")
    for key, spec in schema.get("properties", {}).items():
        if key in data and spec.get("type") == "string" and not isinstance(data[key], str):
            raise TypeError(f"{key} 필드는 문자열이어야 합니다")

INPUT_SCHEMA = {
    "type": "object",
    "properties": {"prompt": {"type": "string"}},
    "required": ["prompt"],
}

OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {"response": {"type": "string"}},
    "required": ["response"],
}


def sync_documents() -> None:
    """요구사항을 기반으로 설계, 코드, 테스트를 동기화한다."""
    req_path = Path("docs/requirements.md")
    if not req_path.exists():
        return
    content = req_path.read_text(encoding="utf-8")

    def _update_with_markers(path: Path, header: str) -> None:
        marker_start = "<!-- AUTO-GENERATED-START -->"
        marker_end = "<!-- AUTO-GENERATED-END -->"
        generated = f"요구사항에서 생성됨.\n\n{content}\n"
        if path.exists():
            text = path.read_text(encoding="utf-8")
        else:
            text = f"# {header}\n\n"
        if marker_start in text and marker_end in text:
            pre = text.split(marker_start)[0]
            post = text.split(marker_end)[1]
            new_text = f"{pre}{marker_start}\n{generated}{marker_end}{post}"
        else:
            new_text = f"{text}\n{marker_start}\n{generated}{marker_end}\n"
        path.write_text(new_text, encoding="utf-8")

    # 설계 및 테스트 문서 갱신
    design_path = Path("docs/design.md")
    test_doc_path = Path("docs/tests.md")
    _update_with_markers(design_path, "Design")
    _update_with_markers(test_doc_path, "Test Plan")

    # 코드와 테스트 플레이스홀더 생성
    code_path = Path("src/requirements_generated.py")
    test_path = Path("tests/test_requirements_generated.py")
    code_path.parent.mkdir(parents=True, exist_ok=True)
    test_path.parent.mkdir(parents=True, exist_ok=True)
    code_path.write_text(
        (
            '"""요구사항에서 자동 생성된 모듈."""\n'
            'REQUIREMENTS = """\n'
            f"{content}\n"
            '"""\n'
        ),
        encoding="utf-8",
    )
    test_path.write_text(
        (
            '"""요구사항에서 자동 생성된 테스트."""\n'
            'REQUIREMENTS = """\n'
            f"{content}\n"
            '"""\n\n'
            'def test_requirements_placeholder():\n'
            '    assert REQUIREMENTS\n'
        ),
        encoding="utf-8",
    )


def run_pipeline(prompt: str, max_retries: int = 2) -> Dict[str, str]:
    validate({"prompt": prompt}, INPUT_SCHEMA)
    sync_documents()
    responses: Dict[str, str] = {}
    for module_name in AGENT_MODULES:
        notify(f"Starting {module_name}")
        module = importlib.import_module(f"src.agents.{module_name}")
        agent = module.Agent()
        for attempt in range(max_retries):
            try:
                result = agent.run(prompt)
                validate({"response": result}, OUTPUT_SCHEMA)
                responses[module_name] = result
                notify(f"{module_name} success")
                break
            except Exception as exc:  # noqa: BLE001
                agent.feedback(str(exc))
                notify(f"{module_name} failed: {exc}")
                if attempt == max_retries - 1:
                    responses[module_name] = ""
    notify(f"Pipeline complete: {responses}")
    return responses


def auto_pr(body: str) -> None:
    """REST API를 사용해 GitHub 풀 리퀘스트를 생성한다."""
    import os
    import requests

    token = os.getenv("GITHUB_TOKEN")
    repo = os.getenv("GITHUB_REPO")
    head = os.getenv("GIT_BRANCH", "main")
    base = os.getenv("BASE_BRANCH", "main")
    if not token or not repo:
        print("Missing GitHub configuration")
        return
    url = f"https://api.github.com/repos/{repo}/pulls"
    payload = {"title": "Automated PR", "head": head, "base": base, "body": body}
    headers = {"Authorization": f"token {token}"}
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        pr_number = response.json().get("number")
        print(f"Created PR #{pr_number}")
    except requests.RequestException as exc:  # noqa: BLE001
        print(f"Failed to create PR: {exc}")


if __name__ == "__main__":
    import sys

    input_prompt = sys.argv[1] if len(sys.argv) > 1 else "Hello"
    results = run_pipeline(input_prompt)
    if all(results.values()):
        auto_pr(json.dumps(results, indent=2))
    print(json.dumps(results, indent=2))
