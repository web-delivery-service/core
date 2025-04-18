from typing import List, Optional
from app.services.base_service import BaseService

from app.db.dao.order_dao import OrderDAO
from app.dto.order_dto import OrderDTO, OrderUpdateStatusDTO
from app.utils.mapper import Mapper

from app.services.user_service import UserService

from app.db.models.order import StatusEnum

from app.job_service.jobs import send_order_recieved_email, send_order_created_email, send_order_proccess_email
from app.dto.stats_dto import StatsFilterDTO


class OrderService(BaseService):

    def __init__(
        self,
        session_factory,
    ):
        super().__init__(
            dto=OrderDTO,
            dao=OrderDAO(session_factory=session_factory),
        )

        self.user_service = UserService(session_factory=session_factory)

    
    async def create(self, *, entity_in) -> Optional[int]:
        order = await self.dao.create(entity_in=entity_in)
        user = await self.user_service.get_by_id(id=order.user_id)

        print(user.email, user.name, order.cost, user.address)
    
        send_order_proccess_email.delay(email=user.email, name=user.name)
        send_order_created_email.delay(name=user.name, cost=order.cost, address=user.address)

        return order.id

    async def get_all(self) -> List[OrderDTO]:
        result = await self.dao.get_all()
        return [Mapper.model_to_dto_with_relations(model=model, dto=self.dto) for model in result]
    
    async def get_all_by_date(self, filter: StatsFilterDTO) -> List[OrderDTO]:
        result = await self.dao.get_all_by_date(filter=filter)
        return [Mapper.model_to_dto_with_relations(model=model, dto=self.dto) for model in result]
    
    async def update_status(self, *, order_id: int, entity_in: OrderUpdateStatusDTO) -> None:
        order = await self.dao.update_status(order_id=order_id, entity_in=entity_in)
        user = await self.user_service.get_by_id(id=order.user_id)

        if order.status == StatusEnum.DELIVERED:
            send_order_recieved_email.delay(email=user.email, name=user.name)        