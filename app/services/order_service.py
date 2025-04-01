from typing import List
from app.services.base_service import BaseService

from app.db.dao.order_dao import OrderDAO
from app.dto.order_dto import OrderDTO
from app.utils.mapper import Mapper


class OrderService(BaseService):

    def __init__(
        self,
        session_factory,
    ):
        super().__init__(
            dto=OrderDTO,
            dao=OrderDAO(session_factory=session_factory),
        )


    async def get_all(self) -> List[OrderDTO]:
        result = await self.dao.get_all()
        return [Mapper.model_to_dto_with_relations(model=model, dto=self.dto) for model in result]
