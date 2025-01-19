from fastapi import status, APIRouter

from app.dtos.root import RootResponseDto

router = APIRouter(tags=["헬스 체크 API (default)"])


@router.get("/", summary="", response_model=RootResponseDto, status_code=status.HTTP_200_OK)
async def root() -> RootResponseDto:
    return RootResponseDto(
        happy="hacking"
    )
