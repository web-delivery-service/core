from app.services.user_service import UserService

from app.dto.user_dto import UserDTO, UserWithPasswordDTO
from app.auth.dto import (
    LoginUserDTO,
    TokenInfo,
)

from app.auth.password_manager import PasswordManager
from app.auth.jwt import JWTFactory
from app.utils.mapper import Mapper
from app.auth.exceptions import UserDoesNotExist, IncorrectPasswordOrEmailException


class AuthService:

    def __init__(self, session_factory):
        self.user_service = UserService(session_factory=session_factory)

    async def authenticate_user(self, credentials: LoginUserDTO) -> bool | UserDTO:
        user: UserWithPasswordDTO | None = await self.user_service.get_user_by_email(
            email=credentials.email
        )
        if not user:
            raise UserDoesNotExist
        if not PasswordManager.verify_password(
            plain_password=credentials.password, hashed_password=user.password
        ):
            raise IncorrectPasswordOrEmailException

        return Mapper.dto_to_dto(dto_from=user, dto_to=UserDTO)

    async def create_tokens(self, user: UserDTO) -> TokenInfo:
        access_token = JWTFactory.create_access_token(user=user)
        refresh_token = JWTFactory.create_refresh_token(user=user)

        return TokenInfo(access_token=access_token, refresh_token=refresh_token)

    async def refresh_access_token(self, user: UserDTO) -> TokenInfo:
        access_token = JWTFactory.create_access_token(user=user)
        return TokenInfo(access_token=access_token)
