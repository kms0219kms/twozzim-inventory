from typing import Annotated

from sqlmodel import Field, SQLModel


class Product(SQLModel, table=True):
    # Auto Incremented ID
    id: Annotated[int, Field(primary_key=True)]

    # Store relationships
    store_id: Annotated[int, Field(foreign_key="store.id")]

    # Category relationships
    category_id: Annotated[int, Field(foreign_key="category.wmpoplus_id")]

    # Product Name
    name: str

    # Product Description
    description: str

    # Product Image
    image: str

    # Sold Out
    is_soldout: Annotated[bool, Field(default=False)]

    # Wmpoplus ID
    wmpoplus_id: Annotated[int, Field(unique=True)]

    # Baemin ID
    # baemin_id: Annotated[str, Field(unique=True)]

    # Coupang Eats ID
    # coupang_id: Annotated[str, Field(unique=True)]
