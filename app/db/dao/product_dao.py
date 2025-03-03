from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncResult

from app.db.models.product import Product
from app.db.models.base import ModelType

from app.db.dao.crudbase_dao import CRUDBaseDAO


class ProductDAO(CRUDBaseDAO):
    model: ModelType = Product

    def __init__(self, session_factory):
        super().__init__(session_factory=session_factory)

    async def get_by_category_id(self, *, category_id: int) -> List[Product]:
        async with self.session_factory() as conn:
            query = select(self.model).filter_by(category_id=category_id)
            result: AsyncResult = await conn.execute(query)
            return result.scalars().all()
