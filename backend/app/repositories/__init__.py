from os import getenv
from sqlmodel import Session, create_engine

### MODELS ###
from .store import Store
from .category import Category
from .product import Product

### MODELS ###

### ENGINE AND SESSIONS ###
database_engine = create_engine(getenv("DATABASE_URL") or "")


def get_session():
    with Session(database_engine) as session:
        yield session


### ENGINE AND SESSIONS ###
