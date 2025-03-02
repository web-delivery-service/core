import jwt, uuid
from datetime import timedelta, datetime, timezone

from app.dto.user_dto import UserDTO
from app.auth.dto import AccessTokenPayload, RefreshTokenPayload

from app.auth.exceptions import (
    InvalidOrExpiredTokenException,
    InvalidTokenTypeException,
)
from app.settings.config import auth_settings


class JWTFactory:

    ACCESS_TOKEN_TYPE = "access"
    REFRESH_TOKEN_TYPE = "refresh"

    @classmethod
    def create_access_token(cls, *, user: UserDTO) -> str:
        payload = {"sub": str(user.id), "type": cls.ACCESS_TOKEN_TYPE}
        token = cls.__encode_jwt(
            payload=payload,
        )
        return token

    @classmethod
    def create_refresh_token(cls, *, user: UserDTO) -> str:
        payload = {
            "sub": str(user.id),
            "jti": str(uuid.uuid4()),
            "type": cls.REFRESH_TOKEN_TYPE,
        }
        token = cls.__encode_jwt(
            payload=payload,
            expire_timedelta=timedelta(
                minutes=auth_settings.REFRESH_TOKEN_EXPIRE_MINUTES
            ),
        )
        return token

    @classmethod
    def get_token_payload(
        cls, *, token: str, token_type: str
    ) -> AccessTokenPayload | RefreshTokenPayload:
        payload = cls.__decode_jwt(token=token)

        if not cls.__validate_token_type(payload=payload, token_type=token_type):
            raise InvalidTokenTypeException

        if token_type == cls.ACCESS_TOKEN_TYPE:
            token_info = AccessTokenPayload.model_validate(payload)
        elif token_type == cls.REFRESH_TOKEN_TYPE:
            token_info = RefreshTokenPayload.model_validate(payload)

        return token_info

    @classmethod
    def __validate_token_type(cls, *, payload: dict, token_type) -> bool:
        try:
            is_validated = token_type == payload.get("type")
        except KeyError:
            raise InvalidOrExpiredTokenException
        return is_validated

    @classmethod
    def __encode_jwt(
        cls,
        *,
        payload: dict,
        expire_minutes: int = auth_settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        expire_timedelta: timedelta | None = None,
    ) -> str:
        to_encode = payload.copy()
        if expire_timedelta:
            expire = datetime.now(timezone.utc) + expire_timedelta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=expire_minutes)
        to_encode.update({"exp": expire})

        encoded = jwt.encode(
            payload=to_encode,
            key=auth_settings.JWT_PRIVATE_KEY_PATH.read_text(),
            algorithm=auth_settings.ALGORITHM,
        )
        return encoded

    @classmethod
    def __decode_jwt(cls, token: str) -> dict:
        try:
            decoded = jwt.decode(
                token,
                key=auth_settings.JWT_PUBLIC_KEY_PATH.read_text(),
                algorithms=[auth_settings.ALGORITHM],
            )
        except jwt.InvalidTokenError:
            raise InvalidOrExpiredTokenException

        return decoded
