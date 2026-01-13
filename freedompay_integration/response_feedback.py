from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class ResponseFeedBack:
    message: str | None = None
    data: Any = None
    status_code: int = None
    error: str = None
