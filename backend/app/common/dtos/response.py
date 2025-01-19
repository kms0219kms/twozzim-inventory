from typing import Any
from pydantic import BaseModel
from datetime import datetime

from fastapi import status

from app.common.exceptions import StatusCode


class APIResponse(BaseModel):
    code: str = StatusCode(status.HTTP_200_OK).name
    status: int = StatusCode(status.HTTP_200_OK).value

    data: Any
    responseAt: datetime = datetime.fromisoformat("2022-01-01T00:00:00+09:00")
