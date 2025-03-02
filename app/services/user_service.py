from app.services.base_service import BaseService

from app.db.dao.user_dao import UserDAO
from app.dto.user_dto import UserDTO


class UserService(BaseService):

    def __init__(
        self,
        dto: UserDTO,
        dao: UserDAO,
        session_factory,
    ):
        super().__init__(dto, dao(session_factory=session_factory))
