from typing import List
from sqlalchemy import and_, select, func
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


    async def get_all_categories_stats(self, filter: StatsFilterDTO) -> dict[str, int]:
        async with self.session_factory() as conn:
            order_stats_subq = (
                select(
                    Product.category_id,
                    func.sum(OrderProduct.quantity).label("total_quantity")
                )
                .join(Product, OrderProduct.product_id == Product.id)
                .join(Order, OrderProduct.order_id == Order.id)
                .group_by(Product.category_id)
            )
 
            if filter.end_date:
                order_stats_subq = order_stats_subq.where(Order.created_at <= filter.end_date)
            if filter.start_date:
                order_stats_subq = order_stats_subq.where(Order.created_at >= filter.start_date)

            order_stats_subq = order_stats_subq.subquery()

            query = (
                select(
                    Category.title,
                    func.coalesce(order_stats_subq.c.total_quantity, 0).label("total_quantity")
                )
                .select_from(Category)
                .outerjoin(
                    order_stats_subq,
                    Category.id == order_stats_subq.c.category_id
                )
            )

            result = await conn.execute(query)
            return {row.title: row.total_quantity for row in result}

            