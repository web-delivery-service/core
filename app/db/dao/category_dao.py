from app.db.models.category import Category
from app.db.models.base import ModelType

from app.db.dao.crudbase_dao import CRUDBaseDAO


class CategoryDAO(CRUDBaseDAO):
    model: ModelType = Category

    def __init__(self, session_factory):
        super().__init__(session_factory=session_factory)
