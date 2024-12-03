from datetime import datetime
from typing import Annotated

from fastapi import Depends, Query, status, APIRouter
from fastapi.responses import JSONResponse
from sqlmodel import Session

from app.repositories import get_session
from app.services.store import StoreService


router = APIRouter(prefix="/store", tags=["Store Details"])
storeService = StoreService()


@router.get(
    "/list",
    summary="Get a list of stores, with current inventory status",
    response_model=dict,
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
