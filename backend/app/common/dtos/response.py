from typing import Any
from zoneinfo import ZoneInfo
from pydantic import BaseModel
from datetime import datetime

from fastapi import status

from app.common.exceptions import StatusCode


class APIResponse(BaseModel):
    code: str = StatusCode(status.HTTP_200_OK).name
    status: int = StatusCode(status.HTTP_200_OK).value

    message: None = None
    data: Any
    responseAt: datetime = datetime.now(ZoneInfo("Asia/Seoul"))
