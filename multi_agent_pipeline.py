"""
멀티 에이전트 파이프라인 예제.
ChatGPT, Claude, Gemini, Cursor AI를 단계별로 호출하는 흐름을 시뮬레이션한다.
실제 API 대신 간단한 핸들러 함수로 입력과 출력을 흉내 낸다.
"""

from dataclasses import dataclass
from typing import Dict, Any, Callable, Optional
import os

try:
    from dotenv import load_dotenv

    # .env 파일을 읽어 API 키를 환경 변수로 로드
    load_dotenv()
except ImportError:
    # 라이브러리가 없으면 환경 변수만 사용
    pass


@dataclass
class Agent:
    """각 단계에서 호출되는 에이전트 추상화."""

    name: str
    key_name: str
    handler: Callable[[Dict[str, Any], Optional[str]], Dict[str, Any]]

    def run(self, data: Dict[str, Any]) -> Dict[str, Any]:
        api_key = os.getenv(self.key_name)
        masked = f"{api_key[:4]}..." if api_key else "키 미설정"
        print(f"[{self.name}] 입력: {data}")
        result = self.handler(data, api_key)
        print(f"[{self.name}] API 키: {masked}")
        print(f"[{self.name}] 출력: {result}\n")
        return result


def chatgpt_handler(data: Dict[str, Any], key: Optional[str]) -> Dict[str, Any]:
    """ChatGPT가 요구사항을 정리한다고 가정."""
    return {"requirements": "기능 목록 초안", **data}


def claude_handler(data: Dict[str, Any], key: Optional[str]) -> Dict[str, Any]:
    """Claude가 설계와 검증을 수행한다고 가정."""
    return {"design": "설계 및 위험 분석", **data}


def gemini_handler(data: Dict[str, Any], key: Optional[str]) -> Dict[str, Any]:
    """Gemini가 프런트/백엔드 코드를 생성한다고 가정."""
    return {"code": "모듈별 코드", **data}


def cursor_handler(data: Dict[str, Any], key: Optional[str]) -> Dict[str, Any]:
    """Cursor가 빌드와 테스트를 실행한다고 가정."""
    return {"build": "빌드 및 테스트 결과", **data}


def run_pipeline(spec: str) -> Dict[str, Any]:
    """전체 파이프라인을 순서대로 실행."""
    state: Dict[str, Any] = {"spec": spec}

    plan = Agent("ChatGPT", "OPENAI_API_KEY", chatgpt_handler)
    design = Agent("Claude", "ANTHROPIC_API_KEY", claude_handler)
    develop = Agent("Gemini", "GEMINI_API_KEY", gemini_handler)
    build = Agent("Cursor", "CURSOR_API_KEY", cursor_handler)

    state = plan.run(state)
    state = design.run(state)
    state = develop.run(state)
    state = build.run(state)
    return state


if __name__ == "__main__":
    final_state = run_pipeline("예시 요구사항")
    print("최종 결과:", final_state)
