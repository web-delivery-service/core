from app.db.models.order import Order
from app.db.models.base import ModelType

from app.db.dao.crudbase_dao import CRUDBaseDAO


class OrderDAO(CRUDBaseDAO):
    model: ModelType = Order

    def __init__(self, session_factory):
        super().__init__(session_factory=session_factory)
