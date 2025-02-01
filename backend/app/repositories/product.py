from typing import Annotated

from sqlmodel import Field, SQLModel


class Product(SQLModel, table=True):
    # Wmpoplus Product ID
    id: Annotated[int, Field(primary_key=True)]

    # Store relationships
    store_id: Annotated[int, Field(foreign_key="store.id")]

    # Category relationships
    category_id: Annotated[int, Field(foreign_key="category.id")]

    # Product Name
    name: str

    # Product Description
    description: str

    # Product Image
    image: str

    # Sold Out
    is_soldout: Annotated[bool, Field(default=False)]
