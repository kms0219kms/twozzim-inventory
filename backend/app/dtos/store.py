from pydantic import BaseModel


class StoreListResponseDto(BaseModel):
    data: list
    