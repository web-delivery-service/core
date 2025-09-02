from typing import List
from app.db.dao.stats_dao import StatsDAO

from app.dto.stats_dto import StatsFilterDTO, StatsDTO

from app.services.category_service import CategoryService
from app.services.order_service import OrderService
from app.services.product_service import ProductService
from app.services.order_product_service import OrderProductService
from app.dto.order_product_dto import OrderProductWithProductDTO

class StatsService:

    def __init__(
        self,
        session_factory
    ):
        self.dao = StatsDAO(session_factory=session_factory)
        self.category_service = CategoryService(session_factory=session_factory)
        self.order_service = OrderService(session_factory=session_factory)
        self.order_product_service = OrderProductService(session_factory=session_factory)
        self.product_service = ProductService(session_factory=session_factory)


    async def get_stats(self, filter: StatsFilterDTO) -> StatsDTO:
        product_quantity = await self.dao.get_product_quantity()
        category_quantity = await self.dao.get_category_quantity()
        order_quantity = await self.dao.get_order_quantity(filter=filter)
        total_cost = await self.dao.get_order_total_cost(filter=filter)

        categories_stats = await self.dao.get_all_categories_stats(filter=filter)

        return StatsDTO(
            order_quantity=order_quantity,
            total_cost=total_cost,
            product_quantity=product_quantity,
            category_quantity=category_quantity,
            categories_stats=categories_stats
        )