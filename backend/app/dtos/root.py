from pydantic import BaseModel


class RootResponseDto(BaseModel):
    happy: str = "hacking"
