from os import getenv
from datetime import datetime
from zoneinfo import ZoneInfo
from dotenv import load_dotenv

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException

from sqlmodel import SQLModel
from app.repositories import database_engine

from app.common.exceptions import StatusCode, APIException
from app.controllers import routers
from app.controllers.root import router as root

# Dotenv Loader
load_dotenv()


# Exception Loader
def init_exception_handler(app: FastAPI) -> bool:
    async def app_exception_handler(_: Request, ex: HTTPException) -> JSONResponse:
        return JSONResponse(
            status_code=ex.status_code,
            content={
                "code": StatusCode(ex.status_code).name,
                "status": ex.status_code,
                "message": ex.detail,
                "data": None,
                "responseAt": datetime.now(ZoneInfo("Asia/Seoul")).isoformat(),
            },
        )

    async def custom_exception_handler(_: Request, ex: APIException) -> JSONResponse:
        return JSONResponse(
            status_code=ex.status,
            content={
                "code": ex.code or StatusCode(ex.status).name,
                "status": ex.status,
                "message": ex.message,
                "data": ex.data,
                "responseAt": datetime.now(ZoneInfo("Asia/Seoul")).isoformat(),
            },
        )

    async def validation_exception_handler(_: Request, ex: RequestValidationError) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "code": StatusCode(status.HTTP_422_UNPROCESSABLE_ENTITY).name,
                "status": status.HTTP_422_UNPROCESSABLE_ENTITY,
                "message": "입력 값이 올바르지 않습니다.",
                "data": ex.errors(),
                "responseAt": datetime.now(ZoneInfo("Asia/Seoul")).isoformat(),
            },
        )

    app.add_exception_handler(RequestValidationError, validation_exception_handler)  # type: ignore

    app.add_exception_handler(HTTPException, app_exception_handler)  # type: ignore
    app.add_exception_handler(APIException, custom_exception_handler)  # type: ignore

    return True


def init_middlewares(app: FastAPI) -> bool:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=(
            [
                "http://127.0.0.1:5173",
                "http://localhost:5173",
                "http://samsung:5173",
            ]
            if getenv("ENVIRONMENT") == "development"
            else [
                "https://twozzim.lunaiz.com",
                "https://twozzim-inventory.vercel.app",
            ]
        ),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return True


# FastAPI Loader
def create_app() -> FastAPI:
    """Load and Create FastAPI Application"""

    app = FastAPI(
        title="Twozzim Inventory Status",
        description="이세계아이돌 X 두찜 실시간 굿즈 재고 현황 서비스",
        version="1.0",
    )

    init_exception_handler(app)
    init_middlewares(app)
    SQLModel.metadata.create_all(database_engine)

    app.include_router(root)  # for just / path support
    app.include_router(routers)

    return app


app = create_app()
