from app.db.dao.stats_dao import StatsDAO

from app.dto.stats_dto import StatsFilterDTO, StatsDTO

class StatsService:

    def __init__(
        self,
        session_factory
    ):
        self.dao = StatsDAO(session_factory=session_factory)


    async def get_stats(self, filter: StatsFilterDTO) -> StatsDTO:
        product_quantity = await self.dao.get_product_quantity()
        category_quantity = await self.dao.get_category_quantity()
        order_quantity = await self.dao.get_order_quantity(filter=filter)
        total_cost = await self.dao.get_order_total_cost(filter=filter)

        return StatsDTO(
            order_quantity=order_quantity,
            total_cost=total_cost,
            product_quantity=product_quantity,
            category_quantity=category_quantity,
        )