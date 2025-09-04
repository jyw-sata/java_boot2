"""간단한 텔레그램 알림 도우미."""
from __future__ import annotations

import os
from typing import Optional
from urllib import parse, request


def notify(message: str) -> None:
    """자격 정보가 주어지면 텔레그램으로 메시지를 보낸다.

    필요한 환경 변수는 `TELEGRAM_BOT_TOKEN`과 `TELEGRAM_CHAT_ID`이다.
    설정이 없거나 요청이 실패하면 조용히 종료한다.
    """
    token: Optional[str] = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id: Optional[str] = os.getenv("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        return
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = parse.urlencode({"chat_id": chat_id, "text": message}).encode()
    try:
        request.urlopen(url, data=data, timeout=30)
    except Exception:
        pass
