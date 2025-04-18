from typing import List
from fastapi import APIRouter, Depends, status

from app.api.controllers.controller_contract import ControllerContract

from app.dto.order_product_dto import (
    OrderProductCreateDTO,
    OrderProductDTO,
    OrderProductWithProductDTO
)
from app.services.order_product_service import OrderProductService

from app.api.deps import get_order_product_service


class OrderProductController(ControllerContract):

    router = APIRouter(prefix="/order-products")

    @router.get(
        "/{order_id}", 
        response_model=List[OrderProductDTO],
        summary="Get all order-products by order",
        description="Retrieve a list of all order-products by order.",
        response_description="A list of order-products.",
    )
    async def get_by_order(
        order_id: int,
        order_product_service: OrderProductService = Depends(get_order_product_service),
    ) -> List[OrderProductDTO]:
        return await order_product_service.get_by_order_id(order_id=order_id)
