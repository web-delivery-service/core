from app.db.models.user import User
from app.db.models.base import ModelType

from app.db.dao.crudbase_dao import CRUDBaseDAO


class UserDAO(CRUDBaseDAO):
    model: ModelType = User

    def __init__(self, session_factory):
        super().__init__(session_factory=session_factory)
