from app.services.base_service import BaseService

from app.db.dao.order_product_dao import OrderProductDAO
from app.dto.order_product_dto import OrderProductDTO, OrderProductWithProductDTO
from app.dto.stats_dto import StatsFilterDTO
from app.utils.mapper import Mapper


class OrderProductService(BaseService):

    def __init__(
        self,
        session_factory,
    ):
        super().__init__(
            dto=OrderProductDTO,
            dao=OrderProductDAO(session_factory=session_factory),
        )

    async def get_by_order_id(self, order_id: int) -> list[OrderProductDTO]:
        result = await self.dao.get_by_order_id(order_id=order_id)
        return [Mapper.model_to_dto(model=model, dto=self.dto) for model in result]
    
    async def get_all_with_products(self) -> list[OrderProductWithProductDTO]:
        result = await self.dao.get_all_with_products()
        return [Mapper.model_to_dto_with_relations(model=model, dto=OrderProductWithProductDTO) for model in result]