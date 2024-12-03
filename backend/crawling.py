import asyncio
import time
import schedule

from os import getenv
from dotenv import load_dotenv

from sqlmodel import Session, create_engine, select

from scripts.get_stores import get_stores
from scripts.get_products import get_products

from app.repositories import Store, Category, Product


async def save():
    load_dotenv()
    engine = create_engine(getenv("DATABASE_URL"), echo=True)

    stores = await get_stores()

    with Session(engine) as session:
        ### RESET DATABASE ###
        saved_products = session.exec(select(Product)).all()
        for product in saved_products:
            session.delete(product)

        saved_categories = session.exec(select(Category)).all()
        for category in saved_categories:
            session.delete(category)

        saved_stores = session.exec(select(Store)).all()
        for store in saved_stores:
            session.delete(store)

        session.commit()
        ### RESET DATABASE ###

        session.add_all(stores)
        session.commit()

        stores_db = session.exec(select(Store)).all()
        categories, products = await get_products(stores_db)

        session.add_all(categories)
        session.add_all(products)
        session.commit()

        print(
            f"Saved: {len(stores)} stores, {len(categories)} categories and {len(products)} products"
        )


def main():
    asyncio.run(save())


if __name__ == "__main__":
    main()
    schedule.every(10).minutes.do(main)

    while True:
        schedule.run_pending()
        time.sleep(1)
