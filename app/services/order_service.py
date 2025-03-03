from app.services.base_service import BaseService

from app.db.dao.order_dao import OrderDAO
from app.dto.order_dto import OrderDTO


class OrderService(BaseService):

    def __init__(
        self,
        session_factory,
    ):
        super().__init__(
            dto=OrderDTO,
            dao=OrderDAO(session_factory=session_factory),
        )
