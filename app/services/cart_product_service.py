from app.services.base_service import BaseService

from app.db.dao.cart_product_dao import CartProductDAO
from app.dto.cart_product_dto import CartProductDTO


class CartProductService(BaseService):

    def __init__(
        self,
        session_factory,
    ):
        super().__init__(
            dto=CartProductDTO,
            dao=CartProductDAO(session_factory=session_factory),
        )
