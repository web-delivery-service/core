from typing import List
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncResult

from app.db.models.category import Category
from app.db.models.product import Product
from app.db.models.order import Order

from app.dto.order_dto import OrderDTO
from app.dto.order_product_dto import OrderProductDTO, OrderProductWithProductDTO
from app.dto.product_dto import ProductDTO

from app.services.order_product_service import OrderProductService


from app.dto.stats_dto import StatsFilterDTO
from app.db.models.order_product import OrderProduct

class StatsDAO:
    """
    Data Access Object for stats
    """

    def __init__(self, session_factory):
        self.session_factory = session_factory
        self.order_product_service = OrderProductService(session_factory=session_factory)


    async def get_category_quantity(self) -> int:
        async with self.session_factory() as conn:
            query = select(func.count()).select_from(Category)
            result: AsyncResult = await conn.execute(query)
            return result.scalar()
        

    async def get_product_quantity(self) -> int:
        async with self.session_factory() as conn:
            query = select(func.count()).select_from(Product)
            result: AsyncResult = await conn.execute(query)
            return result.scalar()
        

    async def get_order_quantity(self, filter: StatsFilterDTO) -> int:
        """
        Get count of orders matching filter criteria
        
        Args:
            filter: StatsFilterDTO with date range and other filters
        
        Returns:
            int: Number of matching orders (0 if none match)
        
        Raises:
            MultipleResultsFound: If query returns multiple results (should never happen with COUNT)
        """
        async with self.session_factory() as conn:
            query = select(func.count()).select_from(Order)
            
            if filter.start_date:
                query = query.where(Order.created_at >= filter.start_date)
            if filter.end_date:
                query = query.where(Order.created_at <= filter.end_date)
            
            result: AsyncResult = await conn.execute(query)
            return result.scalar_one()
        

    async def get_order_total_cost(self, filter: StatsFilterDTO) -> int:
        """
        Calculate total order cost within specified date range.
        
        Args:
            filter: StatsFilterDTO with start_date and end_date
        
        Returns:
            int: Total cost of orders (0 if no orders match criteria)
        """
        async with self.session_factory() as conn:
            query = select(func.sum(Order.cost))
            
            if filter.start_date:
                query = query.where(Order.created_at >= filter.start_date)
            if filter.end_date:
                query = query.where(Order.created_at <= filter.end_date)
            
            result: AsyncResult = await conn.execute(query)
            total = result.scalar() or 0
            
            return int(total)


    async def get_category_order_quantity(self, category_id: int, order_ids: List[int], order_products: List[OrderProductWithProductDTO]) -> int:
        """
        Get count of orders for a category
        
        Args:
            category_id: ID of category
            orders: List of all orders
            order_products: List of all order_products
        
        Returns:
            int: Number of orders for category
        """

        category_quantity = 0

        for order_product in order_products:
            if order_product.product.category_id == category_id and order_product.order_id in order_ids:
                category_quantity += order_product.quantity

        return category_quantity

        