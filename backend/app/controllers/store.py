from datetime import datetime
from typing import Annotated

from fastapi import Depends, status, APIRouter
from fastapi.responses import JSONResponse
from sqlmodel import Session

from app.repositories import get_session
from app.services.store import StoreService
from app.dtos.store import StoreListResponseDto


router = APIRouter(prefix="/store", tags=["상점 정보 API"])
storeService = StoreService()


@router.get(
    "/list",
    summary="현재 재고 상황과 함께 상점 리스트를 반환합니다.",
    response_model=StoreListResponseDto,
    status_code=status.HTTP_200_OK,
)
def list(session: Annotated[Session, Depends(get_session)]):
    data = storeService.get(session)

    return JSONResponse(
        {
            "code": "OPERATION_COMPLETE",
            "status": status.HTTP_200_OK,
            "data": data,
            "responseAt": datetime.now().isoformat(),
        }
    )
