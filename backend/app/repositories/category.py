from typing import Annotated

from sqlmodel import Field, SQLModel


class Category(SQLModel, table=True):
    # Wmpoplus Category ID
    id: Annotated[int, Field(primary_key=True)]

    # Store relationships (by Wmpoplus Store ID)
    store_id: Annotated[int, Field(foreign_key="store.id")]

    # Category Name
    name: str

    # Category Description
    description: str
