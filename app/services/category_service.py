from app.services.base_service import BaseService

from app.db.dao.category_dao import CategoryDAO
from app.dto.category_dto import CategoryDTO


class CategoryService(BaseService):

    def __init__(
        self,
        session_factory,
    ):
        super().__init__(
            dto=CategoryDTO,
            dao=CategoryDAO(session_factory=session_factory),
        )
