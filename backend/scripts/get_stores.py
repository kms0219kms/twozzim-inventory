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
    total_page = 1  # 초기값

    stores: list[Store] = []

    # 미참여 매장 (오산시청점 제외: WMPO 전산에 없음)
    non_participating_stores: list[int] = [
        96631,
        111192,
        881879,
        119773,
        33916,
        34279,
        121805,
        108298,
        123307,
        114220,
        121285,
        115554,
        35848,
        102096,
        33659,
        33646,
        119877,
        106342,
        33634,
        89409,
        119456,
        123574,
    ]

    async with AsyncClient() as client:
        while page < total_page:
            page += 1

            response = await client.get(
                f"{API_HOST}/stores",
                params={"page": page, "searchKeyWord": "", "useSearch": 1},
                headers={
                    "Accept": "application/json, text/plain, */*",
                    "Origin": APP_HOST,
                    "Referer": f"{APP_HOST}/",
                    "Token": "22cc5a10-3b47-4867-a82c-ef09ad116e7a",
                    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_7_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Mobile/15E148 Safari/604.1",
                },
            )
            response.raise_for_status()

            data = response.json()
            if total_page == 1:
                total_page = data["paging"]["totalPage"]

            # stores.extend(data["data"])
            for store in data["data"]:
                stores.append(
                    Store(
                        id=store["ID"],
                        name=store["name"],
                        lat=store["lat"],
                        lng=store["lon"],
                        operating=store["enableReception"],
                        parcipating=store["ID"] not in non_participating_stores,
                    )  # type: ignore
                )

            print(f"Done: Page {page} / {total_page}")

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
