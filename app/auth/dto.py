# from pydantic import BaseModel, EmailStr

# from app.common.dto.user_dto import UserDTO
# from app.common.dto.base_dto import CreateDTO


# class LoginUserDTO(CreateDTO):
#     username: str
#     password: str


# class LoginUserByEmailDTO(CreateDTO):
#     email: EmailStr
#     password: str


# class RegisterUserDTO(CreateDTO):
#     email: EmailStr
#     username: str
#     password: str


# class TokenInfo(CreateDTO):
#     access_token: str
#     refresh_token: str | None = None
#     token_type: str = "Bearer"


# class AccessTokenPayload(CreateDTO):
#     sub: str
#     exp: int
#     type: str


# class RefreshTokenPayload(CreateDTO):
#     sub: str
#     exp: int
#     jti: str
#     type: str


# class NewPassordDataDTO(CreateDTO):
#     hashed_password: str


# class TwoFactorKeywordData(CreateDTO):
#     keyword_auth: bool
#     keyword: str | None = None


# class EmailOTPData(CreateDTO):
#     email: EmailStr
#     otp: str


# class EmailData(CreateDTO):
#     email: EmailStr


# class UsernameData(CreateDTO):
#     username: str


# class KeywordData(CreateDTO):
#     keyword: str


# class PasswordData(CreateDTO):
#     password: str
