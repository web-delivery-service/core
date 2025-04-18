from typing import List, Optional
from sqlalchemy import delete, select, update
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncResult

from app.db.models.order_product import OrderProduct
from app.db.models.base import ModelType

from app.db.dao.crudbase_dao import CRUDBaseDAO
from app.dto.stats_dto import StatsFilterDTO



class OrderProductDAO(CRUDBaseDAO):
    model: ModelType = OrderProduct

    def __init__(self, session_factory):
        super().__init__(session_factory=session_factory)


    async def get_by_order_id(self, order_id: int) -> List[OrderProduct]:
        async with self.session_factory() as session:
            query = select(self.model).filter_by(order_id=order_id)
            result: AsyncResult = await session.execute(query)
            return result.scalars().all()
        
    async def get_all_with_products(self) -> List[OrderProduct]:
        async with self.session_factory() as session:
            query = select(self.model).options(joinedload(self.model.product))
            result: AsyncResult = await session.execute(query)
            return result.unique().scalars().all()