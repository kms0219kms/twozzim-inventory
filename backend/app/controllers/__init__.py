from fastapi import APIRouter

from .root import router as root_controller
from .store import router as store_controller

routers = APIRouter(prefix="/v1", dependencies=[])

routers.include_router(root_controller)
routers.include_router(store_controller)
