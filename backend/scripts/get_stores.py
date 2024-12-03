import asyncio

from os import getenv
from dotenv import load_dotenv

from httpx import AsyncClient
from sqlmodel import Session, create_engine, select

from app.common.constants.wmpoplus import APP_HOST, API_HOST
from app.repositories import Store


async def get_stores():
    # Base URL: https://api.thecupping.co.kr/ (constants/wmpoplus.py 내 API_HOST로 정의되어 있음)

    # Method: GET
    # Route: /stores
    # Query Params: page, searchKeyWord(항상 공백), useSearch(항상 1)
    # 응답 값 내 paging.page와 paging.totalPage가 같을 때 까지 반복 호출

    page = 0
    totalPage = 1  # 초기값

    stores: list[Store] = []
    non_participating_stores: list[int] = [
        98553,
        119773,
        96631,
        90395,
        113672,
        33847,
        90130,
        33754,
        33668,
        108298,
        90518,
        121805,
        33645,
        59616,
        33941,
        114220,
        102096,
        46126,
        33646,
        35848,
        119544,
        54960,
        42341,
        33653,
        33659,
        89409,
        106342,
        119550,
        33634,
        110365,
    ]

    async with AsyncClient() as client:
        while page < totalPage:
            page += 1

            response = await client.get(
                f"{API_HOST}/stores",
                params={"page": page, "searchKeyWord": "", "useSearch": 1},
                headers={
                    "Accept": "application/json, text/plain, */*",
                    "Origin": APP_HOST,
                    "Referer": f"{APP_HOST}/",
                    "Token": "22cc5a10-3b47-4867-a82c-ef09ad116e7a",
                    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
                },
            )
            response.raise_for_status()

            data = response.json()
            if totalPage == 1:
                totalPage = data["paging"]["totalPage"]

            # stores.extend(data["data"])
            for store in data["data"]:
                stores.append(
                    Store(
                        name=store["name"],
                        lat=store["lat"],
                        lng=store["lon"],
                        operating=store["enableReception"],
                        parcipating=store["ID"] not in non_participating_stores,
                        wmpoplus_id=store["ID"],
                    )  # type: ignore
                )

            print(f"Done: Page {page} / {totalPage}")

    return stores


async def save():
    stores = await get_stores()

    engine = create_engine(getenv("DATABASE_URL"), echo=True)
    with Session(engine) as session:
        ### RESET DATABASE ###
        saved_stores = session.exec(select(Store)).all()

        for store in saved_stores:
            session.delete(store)
        session.commit()
        ### RESET DATABASE ###

        session.add_all(stores)
        session.commit()
        print(f"Saved {len(stores)} stores into the database!")


if __name__ == "__main__":
    load_dotenv()
    asyncio.run(save())
