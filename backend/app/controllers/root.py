from fastapi import status, APIRouter

router = APIRouter(tags=["Health Checker"])


@router.get("/", summary="", response_model=dict, status_code=status.HTTP_200_OK)
def root():
    return {"happy": "hacking"}
