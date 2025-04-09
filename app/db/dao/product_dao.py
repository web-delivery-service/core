from typing import List
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncResult

from app.db.models.product import Product
from app.db.models.base import ModelType

from app.db.dao.crudbase_dao import CRUDBaseDAO
from app.dto.product_dto import ProductFilterDTO


class ProductDAO(CRUDBaseDAO):
    model: ModelType = Product

    def __init__(self, session_factory):
        super().__init__(session_factory=session_factory)

    async def get_by_category_id(self, *, category_id: int) -> List[Product]:
        async with self.session_factory() as conn:
            query = select(self.model).filter_by(category_id=category_id)
            result: AsyncResult = await conn.execute(query)
            return result.scalars().all()
        
    async def get_all(self, *, filter: ProductFilterDTO) -> List[Product]:
        async with self.session_factory() as conn:
            query = select(self.model)
            
            if filter.title is not None:
                query = query.where(self.model.title.ilike(f"%{filter.title}%"))
                
            if filter.category_id is not None:
                query = query.where(self.model.category_id == filter.category_id)
                
            if filter.min_cost is not None:
                query = query.where(self.model.cost >= filter.min_cost)
                
            if filter.max_cost is not None:
                query = query.where(self.model.cost <= filter.max_cost)
            
            result: AsyncResult = await conn.execute(query)
            return result.scalars().all()
        
    
    async def decrease_quantity(self, *, product_id: int, quantity: int) -> None:
        async with self.session_factory() as conn:
            async with conn.begin():
                query = select(self.model).filter_by(id=product_id)
                result: AsyncResult = await conn.execute(query)
                product: Product = result.scalar_one_or_none()

                if quantity < 1 or quantity > product.quantity:
                    return

                query = (
                    update(self.model)
                    .filter_by(id=product_id)
                    .values(quantity=product.quantity - quantity)
                )
                await conn.execute(query)
