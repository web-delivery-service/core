from typing import Annotated
from fastapi import APIRouter, Depends, Response, status
from fastapi.security import HTTPBearer

from app.auth.dto import (
    RegisterUserDTO,
    LoginUserDTO,
    TokenInfo,
)
from app.dto.user_dto import UserDTO

from app.services.user_service import UserService
from app.auth.auth_service import AuthService

from app.api.controllers.controller_contract import ControllerContract

from app.api.deps import get_user_service, get_auth_service

from app.auth.deps import get_current_user, get_current_user_for_refresh, get_admin
from app.settings.config import auth_settings

from app.auth.exceptions import UserDoesNotExist


class AuthController:

    router = APIRouter(prefix="/auth")
    http_bearer = HTTPBearer()

    @router.get(
        "/me",
        response_model=UserDTO,
        summary="Get current user",
        response_description="The current user's information.",
    )
    async def get_current_user(user: UserDTO = Depends(get_current_user)) -> UserDTO:
        return user

    @router.post(
        "/register",
        response_model=UserDTO,
        summary="Register a new user",
        response_description="The registered user's information.",
    )
    async def register(
        credentials: RegisterUserDTO,
        user_service: UserService = Depends(get_user_service),
    ) -> UserDTO:
        return await user_service.create(credentials=credentials)

    @router.post(
        "/login",
        response_model_exclude_none=True,
        summary="Login a user",
        response_description="Access token",
    )
    async def login(
        response: Response,
        credentials: LoginUserDTO,
        auth_service: AuthService = Depends(get_auth_service),
    ) -> TokenInfo:
        user = await auth_service.authenticate_user(credentials=credentials)

        token_pair = await auth_service.create_tokens(user=user)
        response.set_cookie(
            key=auth_settings.REFRESH_COOKIE_KEY,
            value=token_pair.refresh_token,
            httponly=True,
        )

        return TokenInfo(access_token=token_pair.access_token, refresh_token=token_pair.refresh_token)

    @router.post(
        "/refresh",
        response_model_exclude_none=True,
        summary="Refresh access token",
        response_description="Access token.",
    )
    async def refresh(
        user: UserDTO = Depends(get_current_user_for_refresh),
        auth_service: AuthService = Depends(get_auth_service),
    ) -> TokenInfo:
        access_token: TokenInfo = await auth_service.refresh_access_token(user=user)

        return access_token

    @router.post(
        "/logout",
        summary="Logout a user",
        response_description="Logout message.",
    )
    async def logout(
        response: Response,
        user: UserDTO = Depends(get_current_user),
    ):
        response.delete_cookie(
            key=auth_settings.REFRESH_COOKIE_KEY,
            httponly=True,
            domain=auth_settings.COOKIE_DOMAIN,
        )

        return {"message": "User successfully logged out"}

    @router.delete(
        "/{id}",
        status_code=status.HTTP_204_NO_CONTENT,
        summary="Delete user",
        description="Delete user by its ID.",
        response_description="No content.",
    )
    async def delete(
        id: int,
        user_service: UserService = Depends(get_user_service),
        # admin: UserDTO = Depends(get_admin),
    ) -> None:
        result = await user_service.delete(id=id)
        if not result:
            raise UserDoesNotExist
