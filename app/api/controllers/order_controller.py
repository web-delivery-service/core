from typing import List
from fastapi import APIRouter, Depends, status

from app.api.controllers.controller_contract import ControllerContract

from app.dto.order_dto import (
    OrderDTO,
    OrderCreateDTO,
    OrderUpdateDTO,
    OrderUpdateStatusDTO
)
from app.dto.user_dto import UserDTO
from app.services.order_service import OrderService

from app.api.deps import get_order_service
from app.exceptions.order import OrderNotFoundException

from app.auth.deps import get_admin, get_current_user


class OrderController(ControllerContract):

    router = APIRouter(prefix="/orders")

    @router.get(
        "",
        response_model=List[OrderDTO],
        summary="Get all orders",
        description="Retrieve a list of all orders.",
        response_description="A list of orders.",
    )
    async def get_all(
        order_service: OrderService = Depends(get_order_service),
        admin: UserDTO = Depends(get_admin),
    ) -> List[OrderDTO]:
        return await order_service.get_all()

    @router.get(
        "/{id}",
        response_model=OrderDTO,
        summary="Get a order by ID",
        description="Retrieve a specific order by its ID.",
        response_description="The requested order.",
    )
    async def get_one(
        id: int,
        order_service: OrderService = Depends(get_order_service),
        user: UserDTO = Depends(get_current_user),
    ) -> OrderDTO:
        result = await order_service.get_by_id(id=id)
        if not result:
            raise OrderNotFoundException
        return result

    @router.post(
        "",
        status_code=status.HTTP_201_CREATED,
        summary="Create a new order",
        description="Create a new order with the provided data.",
        response_description="The created order ID.",
    )
    async def store(
        entity_in: OrderCreateDTO,
        order_service: OrderService = Depends(get_order_service),
        user: UserDTO = Depends(get_current_user),
    ) -> int:
        return await order_service.create(entity_in=entity_in)

    @router.patch(
        "/{id}",
        response_model=OrderDTO,
        summary="Update a order",
        description="Update an existing order with the provided data.",
        response_description="The updated order.",
    )
    async def update(
        id: int,
        entity_in: OrderUpdateDTO,
        order_service: OrderService = Depends(get_order_service),
        admin: UserDTO = Depends(get_admin),
    ) -> OrderDTO:
        result = await order_service.update(id=id, entity_in=entity_in)
        if not result:
            raise OrderNotFoundException
        return result
    
    @router.patch(
        "/{id}/status",
        summary="Update a order status",
        description="Update an existing order status with the provided data.",
        response_description="The updated order.",
    )
    async def update_status(
        id: int,
        entity_in: OrderUpdateStatusDTO,
        order_service: OrderService = Depends(get_order_service),
        admin: UserDTO = Depends(get_admin),
    ) -> None:
        await order_service.update_status(order_id=id, entity_in=entity_in)

    @router.delete(
        "/{id}",
        status_code=status.HTTP_204_NO_CONTENT,
        summary="Delete a order",
        description="Delete a order by its ID.",
        response_description="No content.",
    )
    async def delete(
        id: int,
        order_service: OrderService = Depends(get_order_service),
        admin: UserDTO = Depends(get_admin),
    ) -> None:
        result = await order_service.delete(id=id)
        if not result:
            raise OrderNotFoundException
