from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, Request
from typing import Annotated

from app.auth.jwt import JWTFactory
from app.auth.dto import AccessTokenPayload, RefreshTokenPayload
from app.dto.user_dto import UserDTO, UserWithPasswordDTO

from app.api.deps import get_user_service
from app.services.user_service import UserService

from app.auth.exceptions import (
    InvalidOrExpiredTokenException,
    TokenDoesNotExistException,
    UserDoesNotExist,
    LackOfPermisionsExceptions,
)
from app.settings.config import auth_settings

from app.db.models.user import RoleEnum


http_bearer = HTTPBearer()


async def get_validated_user_by_payload(
    payload: AccessTokenPayload | RefreshTokenPayload,
    user_service: UserService,
    is_admin: bool = False,
) -> UserDTO:
    try:
        user_id = int(payload.sub)
    except:
        raise InvalidOrExpiredTokenException

    try:
        user = await user_service.get_by_id(id=user_id)
    except:
        raise UserDoesNotExist

    if is_admin and user.role != RoleEnum.ADMIN:
        raise LackOfPermisionsExceptions

    return user


async def verify_token(
    token: str,
    user_service: UserService = Depends(get_user_service),
) -> UserDTO:
    access_token_pyload: AccessTokenPayload = JWTFactory.get_token_payload(
        token=token, token_type=JWTFactory.ACCESS_TOKEN_TYPE
    )
    user = await get_validated_user_by_payload(
        payload=access_token_pyload, user_service=user_service
    )

    return user


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(http_bearer)],
    user_service: UserService = Depends(get_user_service),
) -> UserDTO:
    token = credentials.credentials
    access_token_pyload: AccessTokenPayload = JWTFactory.get_token_payload(
        token=token, token_type=JWTFactory.ACCESS_TOKEN_TYPE
    )
    user = await get_validated_user_by_payload(
        payload=access_token_pyload, user_service=user_service
    )

    return user


async def get_admin(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(http_bearer)],
    user_service: UserService = Depends(get_user_service),
) -> UserDTO:
    token = credentials.credentials
    access_token_pyload: AccessTokenPayload = JWTFactory.get_token_payload(
        token=token, token_type=JWTFactory.ACCESS_TOKEN_TYPE
    )
    user = await get_validated_user_by_payload(
        payload=access_token_pyload,
        user_service=user_service,
        is_admin=True,
    )

    return user


async def get_current_user_for_refresh(
    request: Request,
    user_service: UserService = Depends(get_user_service),
) -> UserDTO:
    token = request.cookies.get(auth_settings.REFRESH_COOKIE_KEY)
    if not token:
        raise TokenDoesNotExistException

    refresh_token_pyload: RefreshTokenPayload = JWTFactory.get_token_payload(
        token=token, token_type=JWTFactory.REFRESH_TOKEN_TYPE
    )
    user = await get_validated_user_by_payload(
        payload=refresh_token_pyload, user_service=user_service
    )

    return user
