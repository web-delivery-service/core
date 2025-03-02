from app.db.models.product import Product
from app.db.models.base import ModelType

from app.db.dao.crudbase_dao import CRUDBaseDAO


class ProductDAO(CRUDBaseDAO):
    model: ModelType = Product

    def __init__(self, session_factory):
        super().__init__(session_factory=session_factory)
