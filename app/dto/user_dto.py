from pydantic import EmailStr

from app.dto.base_dto import CreateDTO, BaseDTO, BaseModel
from app.db.models.user import RoleEnum


class UserCreateDTO(CreateDTO):
    email: EmailStr
    password: str
    role: RoleEnum = RoleEnum.USER
    name: str | None = None
    address: str | None = None


class UserDTO(BaseDTO):
    email: EmailStr
    role: RoleEnum
    name: str | None
    address: str | None


class UserWithPasswordDTO(BaseDTO):
    email: EmailStr
    password: str
    role: RoleEnum
    name: str | None
    address: str | None


class UserUpdateDTO(BaseModel):
    email: EmailStr
    name: str | None = None
    address: str | None = None
