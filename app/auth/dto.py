from pydantic import BaseModel, EmailStr

from app.dto.base_dto import CreateDTO


class LoginUserDTO(CreateDTO):
    email: EmailStr
    password: str


class RegisterUserDTO(CreateDTO):
    email: EmailStr
    password: str


class TokenInfo(CreateDTO):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"


class AccessTokenPayload(CreateDTO):
    sub: str
    exp: int
    type: str


class RefreshTokenPayload(CreateDTO):
    sub: str
    exp: int
    jti: str
    type: str
