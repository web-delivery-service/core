from typing import Optional
from app.services.base_service import BaseService

from app.db.dao.user_dao import UserDAO
from app.dto.user_dto import UserDTO, UserWithPasswordDTO
from app.auth.dto import RegisterUserDTO

from app.auth.password_manager import PasswordManager
from app.utils.mapper import Mapper

from app.auth.exceptions import UserAlreadyExistsEmailException


class UserService(BaseService):

    def __init__(
        self,
        session_factory,
    ):
        super().__init__(
            dto=UserDTO,
            dao=UserDAO(session_factory=session_factory),
        )

    async def create(self, *, credentials: RegisterUserDTO) -> Optional[UserDTO]:
        user = await self.get_user_by_email(email=credentials.email)
        if user:
            raise UserAlreadyExistsEmailException

        credentials.password = PasswordManager.get_hashed_password(
            password=credentials.password
        )
        return await super().create(entity_in=credentials)

    async def get_user_by_email(self, *, email: str) -> Optional[UserWithPasswordDTO]:
        user = await self.dao.get_by_email(email=email)
        return Mapper.model_to_dto(model=user, dto=UserWithPasswordDTO)
