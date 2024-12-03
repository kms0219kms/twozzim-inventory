from typing import Annotated

from sqlmodel import Field, SQLModel


class Category(SQLModel, table=True):
    # Auto Incremented ID
    id: Annotated[int, Field(primary_key=True)]

    # Store relationships
    store_id: Annotated[int, Field(foreign_key="store.id")]

    # Category Name
    name: str

    # Category Description
    description: str

    # Wmpoplus ID
    wmpoplus_id: Annotated[int, Field(unique=True)]

    # Baemin ID
    # baemin_id: Annotated[str, Field(unique=True)]

    # Coupang Eats ID
    # coupang_id: Annotated[str, Field(unique=True)]
