from typing import List, Optional
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncResult

from app.db.models.cart_product import CartProduct
from app.db.models.base import ModelType

from app.db.dao.crudbase_dao import CRUDBaseDAO

from app.db.dao.product_dao import ProductDAO
from app.db.dao.cart_dao import CartDAO

from app.db.models.product import Product

from app.dto.cart_product_dto import CartProductDeleteDTO, CartProductUpdateDTO

from app.exceptions.cart import CartProductQuantityLimitException

from app.utils.mapper import Mapper


class CartProductDAO(CRUDBaseDAO):
    model: ModelType = CartProduct

    def __init__(self, session_factory):
        super().__init__(session_factory=session_factory)
        self.product_dao = ProductDAO(session_factory=session_factory)
        self.cart_dao = CartDAO(session_factory=session_factory)

    async def get_by_cart_id(self, *, cart_id: int) -> List[CartProduct]:
        async with self.session_factory() as conn:
            query = select(self.model).filter_by(cart_id=cart_id)
            result: AsyncResult = await conn.execute(query)
            return result.scalars().all()
        
    async def get_by_user_id(self, *, user_id: int) -> List[CartProduct]:
        async with self.session_factory() as conn:
            cart = await self.cart_dao.get_by_user_id(user_id=user_id, one_instance=True)
            query = select(self.model).filter_by(cart_id=cart.id)
            result: AsyncResult = await conn.execute(query)
            return result.scalars().all()
        
    async def delete(self, *, entity_in: CartProductDeleteDTO) -> Optional[int]:
        async with self.session_factory() as conn:
            async with conn.begin():
                query = (
                    delete(self.model)
                    .filter_by(cart_id=entity_in.cart_id, product_id=entity_in.product_id)
                    .returning(self.model.product_id)
                )
                result: AsyncResult = await conn.execute(query)
                return result.scalar_one_or_none()
            
    async def increase_quantity(self, *, entity_in: CartProductUpdateDTO) -> Optional[int]:
        async with self.session_factory() as conn:
            query = select(Product).filter_by(id=entity_in.product_id)
            result: AsyncResult = await conn.execute(query)
            product: Product = result.scalar_one_or_none()

            if product.quantity < entity_in.quantity:
                raise CartProductQuantityLimitException

        async with self.session_factory() as conn:
            async with conn.begin():
                query = (
                    update(self.model)
                    .filter_by(cart_id=entity_in.cart_id, product_id=entity_in.product_id)
                    .values(quantity=self.model.quantity + 1)
                    .returning(self.model.product_id)
                )
                result: AsyncResult = await conn.execute(query)
                return result.scalar_one_or_none()
            
    async def decrease_quantity(self, *, entity_in: CartProductUpdateDTO) -> Optional[int]:
        if entity_in.quantity < 1:
            return await self.delete(entity_in=Mapper.dto_to_dto(dto_from=entity_in, dto_to=CartProductDeleteDTO))
        
        async with self.session_factory() as conn:
            async with conn.begin():
                query = (
                    update(self.model)
                    .filter_by(cart_id=entity_in.cart_id, product_id=entity_in.product_id)
                    .values(quantity=self.model.quantity - 1)
                    .returning(self.model.product_id)
                )
                result: AsyncResult = await conn.execute(query)
                return result.scalar_one_or_none()
            

    async def delete_by_cart_id(self, *, cart_id: int):
        async with self.session_factory() as conn:
            async with conn.begin():
                query = (
                    delete(self.model)
                    .filter_by(cart_id=cart_id)
                    .returning(self.model.product_id)
                )
                await conn.execute(query)