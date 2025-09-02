from typing import Optional
from app.services.base_service import BaseService

from app.db.dao.user_dao import UserDAO
from app.dto.user_dto import UserDTO, UserWithPasswordDTO, UserCreateDTO
from app.auth.dto import RegisterUserDTO

from app.dto.cart_dto import CartCreateDTO

from app.auth.password_manager import PasswordManager
from app.utils.mapper import Mapper

from app.auth.exceptions import UserAlreadyExistsEmailException, PasswordLengthException

from app.settings.config import auth_settings
from app.db.models.user import RoleEnum

from app.services.cart_service import CartService


class UserService(BaseService):

    def __init__(
        self,
        session_factory,
    ):
        super().__init__(
            dto=UserDTO,
            dao=UserDAO(session_factory=session_factory),
        )

        self.cart_service = CartService(session_factory=session_factory)

    async def create(self, *, credentials: RegisterUserDTO) -> Optional[UserDTO]:
        if len(credentials.password) < 3:
            raise PasswordLengthException

        user = await self.get_user_by_email(email=credentials.email)
        if user:
            raise UserAlreadyExistsEmailException

        credentials.password = PasswordManager.get_hashed_password(
            password=credentials.password
        )

        user_in: UserCreateDTO = Mapper.dto_to_dto(
            dto_from=credentials, dto_to=UserCreateDTO
        )

        if user_in.email == auth_settings.ADMIN_EMAIL:
            user_in.role = RoleEnum.ADMIN

        user = await super().create(entity_in=user_in)
        cart_in = CartCreateDTO(user_id=user.id)
        await self.cart_service.create(entity_in=cart_in)

        return user

    async def get_user_by_email(self, *, email: str) -> Optional[UserWithPasswordDTO]:
        user = await self.dao.get_by_email(email=email)
        return Mapper.model_to_dto(model=user, dto=UserWithPasswordDTO)
    
    async def delete_test_user(self) -> None:
        await self.dao.delete_test_user()
