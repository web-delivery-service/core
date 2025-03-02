from app.db.models.cart import Cart
from app.db.models.base import ModelType

from app.db.dao.crudbase_dao import CRUDBaseDAO


class CartDAO(CRUDBaseDAO):
    model: ModelType = Cart

    def __init__(self, session_factory):
        super().__init__(session_factory=session_factory)
