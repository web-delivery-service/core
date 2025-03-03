from typing import List
from fastapi import APIRouter, Depends, status

from app.api.controllers.controller_contract import ControllerContract

from app.dto.cart_product_dto import (
    CartProductDTO,
    CartProductCreateDTO,
    CartProductUpdateDTO,
)
from app.services.cart_product_service import CartProductService

from app.api.deps import get_cart_product_service
from app.exceptions.category import CategoryNotFoundException

from app.dto.user_dto import UserDTO
from app.auth.deps import get_current_user


class CartProductController(ControllerContract):

    router = APIRouter(prefix="/cart-products")

    @router.post(
        "/",
        response_model=CartProductDTO,
        status_code=status.HTTP_201_CREATED,
        summary="Create a new cart-product",
        description="Create a new cart-product with the provided data.",
        response_description="The created cart-product.",
    )
    async def store(
        entity_in: CartProductCreateDTO,
        cart_product_service: CartProductService = Depends(get_cart_product_service),
        user: UserDTO = Depends(get_current_user),
    ) -> CartProductDTO:
        return await cart_product_service.create(entity_in=entity_in)
