from app.services.base_service import BaseService

from app.db.dao.cart_dao import CartDAO
from app.dto.cart_dto import CartDTO


class CartService(BaseService):

    def __init__(
        self,
        session_factory,
    ):
        super().__init__(
            dto=CartDTO,
            dao=CartDAO(session_factory=session_factory),
        )