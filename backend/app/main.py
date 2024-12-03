from os import getenv
from datetime import datetime
from dotenv import load_dotenv

from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from sqlmodel import SQLModel

from app.repositories import database_engine
from app.common.exceptions import error_code, APIException

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
                "code": error_code.get(str(ex.status_code)),
                "status": ex.status_code,
                "message": ex.detail,
                "responseAt": datetime.now().isoformat(),
            },
        )

    async def custom_exception_handler(_: Request, ex: APIException) -> JSONResponse:
        return JSONResponse(
            status_code=ex.status,
            content={
                "code": ex.code or error_code.get(str(ex.status)),
                "status": ex.status,
                "message": ex.message,
                "responseAt": datetime.now().isoformat(),
            },
        )

    async def validation_exception_handler(_: Request, ex: RequestValidationError) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "code": error_code.get(str(status.HTTP_422_UNPROCESSABLE_ENTITY)),
                "status": status.HTTP_422_UNPROCESSABLE_ENTITY,
                "message": ex.errors(),
                "responseAt": datetime.now().isoformat(),
            },
        )

    app.add_exception_handler(RequestValidationError, validation_exception_handler)

    app.add_exception_handler(HTTPException, app_exception_handler)
    app.add_exception_handler(APIException, custom_exception_handler)

    return True


# FastAPI Loader
def create_app() -> FastAPI:
    """Load and Create FastAPI Application"""

    app = FastAPI(
        title="Twozzim Inventory Status",
        description="이세계아이돌 X 두찜 실시간 굿즈 재고 현황 서비스",
        version="1.0",
    )

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

    init_exception_handler(app)
    SQLModel.metadata.create_all(database_engine)

    app.include_router(root)  # for just / path support
    app.include_router(routers)

    return app


app = create_app()
