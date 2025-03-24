from typing import List
from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer

from app.dto.user_dto import UserUpdateDTO, UserDTO
from app.dto.order_dto import OrderDTO

from app.services.user_service import UserService
from app.services.order_service import OrderService

from app.api.deps import get_user_service, get_order_service
from app.auth.deps import get_current_user


class UserController:

    router = APIRouter(prefix="/users")
    http_bearer = HTTPBearer()

    @router.get(
        "/",
        response_model=List[UserDTO],
        summary="Get all users",
        description="Retrieve a list of all users.",
    )
    async def get_all(
        user_service: UserService = Depends(get_user_service),
    ) -> List[UserDTO]:
        return await user_service.get_all()

    @router.patch(
        "/",
        response_model=UserDTO,
        summary="Update a user",
        description="Update an existing user with the provided data.",
        response_description="The updated user.",
    )
    async def update(
        self,
        id: int,
        user_in: UserUpdateDTO,
        user_service: UserService = Depends(get_user_service),
        user: UserDTO = Depends(get_current_user),
    ) -> UserDTO:
        return await user_service.update(id=id, entity_in=user_in)

    @router.get(
        "/orders",
        response_model=List[OrderDTO],
        summary="Get orders by user",
        description="Retrieve a list of orders by user.",
        response_description="A list of orders.",
    )
    async def get_orders_by_user(
        self,
        id: int,
        order_service: OrderService = Depends(get_order_service),
        user: UserDTO = Depends(get_current_user),
    ) -> List[OrderDTO]:
        return await order_service.get_by_user_id(user_id=id)
