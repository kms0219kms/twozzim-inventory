from fastapi.encoders import jsonable_encoder
from sqlmodel import Session, select

from app.repositories import Store, Product


class StoreService:
    def __init__(self):
        pass

    def get(self, session: Session) -> list:
        stores = session.exec(select(Store)).all()
        stores_with_status = jsonable_encoder(stores)

        for store in stores_with_status:
            # DB에서 product 테이블 조회, 같은 store_id를 가진 product들 중 하나라고 soldout이 아니면 soldout이 아님
            store["is_soldout"] = (
                not session.exec(
                    select(Product)
                    .where(Product.store_id == store["id"])
                    .where(Product.is_soldout == False)
                ).first()
                is not None
            )

        return stores_with_status
