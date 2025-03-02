from app.db.models.cart_product import CartProduct
from app.db.models.base import ModelType

from app.db.dao.crudbase_dao import CRUDBaseDAO


class CartProductDAO(CRUDBaseDAO):
    model: ModelType = CartProduct

    def __init__(self, session_factory):
        super().__init__(session_factory=session_factory)
