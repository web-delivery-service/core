from app.services.base_service import BaseService

from app.db.dao.product_dao import ProductDAO
from app.dto.product_dto import ProductDTO


class ProductService(BaseService):

    def __init__(
        self,
        session_factory,
    ):
        super().__init__(
            dto=ProductDTO,
            dao=ProductDAO(session_factory=session_factory),
        )
