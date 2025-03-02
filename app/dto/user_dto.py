from pydantic import EmailStr

from app.dto.base_dto import CreateDTO, BaseDTO
from app.db.models.user import RoleEnum


class UserCreateDTO(CreateDTO):
    email: EmailStr
    password: str
    role: RoleEnum
    name: str | None
    address: str | None


class UserDTO(UserCreateDTO, BaseDTO):
    email: EmailStr
    role: RoleEnum
    name: str | None
    address: str | None


class UserUpdateDTO(UserCreateDTO):
    pass
