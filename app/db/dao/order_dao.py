from typing import List
from sqlalchemy import insert, select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncResult

from app.db.models.order import Order, StatusEnum
from app.db.models.base import ModelType

from app.db.dao.crudbase_dao import CRUDBaseDAO
from app.db.dao.cart_product_dao import CartProductDAO

from app.db.models.order_product import OrderProduct


class OrderDAO(CRUDBaseDAO):
    model: ModelType = Order

    def __init__(self, session_factory):
        super().__init__(session_factory=session_factory)
        self.cart_product_dao = CartProductDAO(session_factory=session_factory)


    # Works by pattern UnitOfWork
    async def create(self, *, entity_in):
        async with self.session_factory() as session:
            async with session.begin():
                order = Order(
                    user_id=entity_in['user_id'],
                    status=StatusEnum.PROCESS,
                    cost=entity_in['cost']   
                )
                session.add(order)
                await session.flush()

                cart_products = await self.cart_product_dao.get_by_user_id(user_id=entity_in['user_id'])
                
                order_products_data = [{
                    'order_id': order.id,
                    'product_id': cart_product.product_id,
                    'quantity': cart_product.quantity
                } for cart_product in cart_products]

                if order_products_data:
                    await session.execute(insert(OrderProduct).values(order_products_data))
                    
                    await self.cart_product_dao.delete_by_cart_id(
                        cart_id=cart_products[0].cart_id)

                return order
            
    
    async def get_all(self) -> List[Order]:
        async with self.session_factory() as conn:
            query = select(self.model).options(
                joinedload(self.model.products),
                joinedload(self.model.user)
            )
            result: AsyncResult = await conn.execute(query)
            return result.unique().scalars().all()


                