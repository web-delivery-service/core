from app.services.base_service import BaseService

from app.db.dao.category_dao import CategoryDAO
from app.dto.category_dto import CategoryDTO


class ProductService(BaseService):

    def __init__(
        self,
        dto: CategoryDTO,
        dao: CategoryDAO,
        session_factory,
    ):
        super().__init__(dto, dao(session_factory=session_factory))
