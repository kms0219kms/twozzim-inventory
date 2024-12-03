from typing import Annotated

from sqlmodel import Field, SQLModel


class Store(SQLModel, table=True):
    # Auto Incremented ID
    id: Annotated[int, Field(primary_key=True)]

    # Store Name
    name: str

    # lat and lng
    lat: float
    lng: float

    # Operating now
    operating: Annotated[bool, Field(default=False)]

    # Event participation
    parcipating: Annotated[bool, Field(default=True)]

    # Wmpoplus ID
    wmpoplus_id: Annotated[int, Field(unique=True)]

    # Baemin ID
    # baemin_id: Annotated[str, Field(unique=True)]

    # Coupang Eats ID
    # coupang_id: Annotated[str, Field(unique=True)]
