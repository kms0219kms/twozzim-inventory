import asyncio
import traceback

from os import getenv
from dotenv import load_dotenv
from typing import Sequence

from aiohttp import ClientSession
from aiohttp.client_exceptions import ContentTypeError
from sqlmodel import Session, create_engine, select

from app.common.constants.wmpoplus import APP_HOST, API_HOST
from app.repositories import Store, Category, Product


async def get_products(stores: Sequence[Store]):
    categories: list[Category] = []
    products: list[Product] = []

    # 비동기 동시 실행을 위한 asyncio.gather() 사용
    tasks = []

    client = ClientSession()

    for store in stores:
        tasks.append(get_products_by_store(client, store))

    # 10개씩 쪼개 실행
    tasks = [tasks[i : i + 10] for i in range(0, len(tasks), 10)]
    data = []

    for task in tasks:
        data.extend(await asyncio.gather(*task))
        await asyncio.sleep(1)

    await client.close()

    for category, product in data:
        if category is not None:
            categories.append(category)
            products.extend(product)

    return categories, products


async def get_products_by_store(
    client: ClientSession, store: Store
) -> tuple[None, None] | tuple[Category, list[Product]]:
    # Base URL: https://api.thecupping.co.kr/ (constants/wmpoplus.py 내 API_HOST로 정의되어 있음)

    # Method: GET
    # Route: /stores/{wmpoplus_id}/products

    async with client.get(
        f"{API_HOST}/stores/{store.id}/products",
        headers={
            "Accept": "application/json, text/plain, */*",
            "Origin": APP_HOST,
            "Referer": f"{APP_HOST}/",
            "Token": "22cc5a10-3b47-4867-a82c-ef09ad116e7a",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
        },
    ) as response:
        if response.status != 200:
            print(f"Error: Store {store.name}, Status Code: {response.status}")
            return None, None

        try:
            data = await response.json()
            products = data["data"]["products"]

            for category in products:
                # if category["categoryName"] == "[두찜 X 이세계아이돌] 굿즈세트":
                # if category["categoryName"] == "[두찜 X 이세계아이돌 2탄] 굿즈세트":
                if category["categoryName"] == "":  # 2월 6일에 추가하기
                    print(f"Done: Store {store.name} with {len(category['products'])} products")

                    return Category(
                        id=category["categoryID"],
                        store_id=store.id,
                        name=category["categoryName"],
                        description=category["description"],
                    ), [  # type: ignore
                        Product(
                            id=product["productID"],
                            store_id=store.id,
                            category_id=category["categoryID"],
                            name=product["name"],
                            description=product["productDescription"],
                            image=product["imageUrl"],
                            is_soldout=product["isSoldout"],
                        )  # type: ignore
                        for product in category["products"]
                    ]
                else:
                    continue

            return None, None
        except ContentTypeError:
            print(f"Error: Store {store.name},", await response.text())
            return None, None
        except:
            print(f"Error: Store {store.name},", traceback.format_exc())
            return None, None


async def save():
    engine = create_engine(getenv("DATABASE_URL"), echo=True)

    with Session(engine) as session:
        stores = session.exec(select(Store)).all()

        categories, products = await get_products(stores)

        ### RESET DATABASE ###
        saved_categories = session.exec(select(Category)).all()
        saved_products = session.exec(select(Product)).all()

        for category in saved_categories:
            session.delete(category)
        for product in saved_products:
            session.delete(product)
        session.commit()
        ### RESET DATABASE ###

        session.add_all(categories)
        session.add_all(products)
        session.commit()

        print(f"Saved {len(products)} products into the database!")


if __name__ == "__main__":
    load_dotenv()
    asyncio.run(save())
