from typing import List
from fastapi import APIRouter, Depends, status

from app.api.controllers.controller_contract import ControllerContract

from app.dto.cart_product_dto import (
    CartProductDTO,
    CartProductCreateDTO,
    CartProductUpdateDTO,
    CartProductDeleteDTO
)
from app.services.cart_product_service import CartProductService

from app.api.deps import get_cart_product_service
from app.exceptions.cart import CartNotFoundException, CartProductNotFoundException

from app.dto.user_dto import UserDTO
from app.auth.deps import get_current_user


class CartProductController(ControllerContract):

    router = APIRouter(prefix="/cart-products")

    @router.post(
        "",
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


    @router.get(
        "/{cart_id}",
        response_model=List[CartProductDTO],
        summary="Get all cart-products by cart",
        description="Retrieve a list of all cart-products by cart.",
        response_description="A list of cart-products.",
    )
    async def get_by_cart(
        cart_id: int,
        cart_product_service: CartProductService = Depends(get_cart_product_service),
        user: UserDTO = Depends(get_current_user),
    ) -> List[CartProductDTO]:
        return await cart_product_service.get_by_cart_id(cart_id=cart_id)
    

    @router.delete(
        "",
        status_code=status.HTTP_204_NO_CONTENT,
        summary="Delete a cart-product",
        description="Delete a cart-product by its ID.",
        response_description="No content.",
    )
    async def delete(
        entity_in: CartProductDeleteDTO,
        cart_product_service: CartProductService = Depends(get_cart_product_service),
        user: UserDTO = Depends(get_current_user),
    ) -> None:
        result = await cart_product_service.delete(entity_in=entity_in)
        if not result:
            raise CartProductNotFoundException
        

    @router.patch(
        "/increase",
        summary="increase cart-product quantity",
        description="increase cart-product quantity",
        response_description="The updated cart-product ID",
    )
    async def increase_quantity(
        entity_in: CartProductUpdateDTO,
        cart_product_service: CartProductService = Depends(get_cart_product_service),
        user: UserDTO = Depends(get_current_user),
    ) -> int:
        result = await cart_product_service.increase_quantity(
            entity_in=entity_in
        )

        if result is None:
            raise CartProductNotFoundException
        
        return result
    

    @router.patch(
        "/decrease",
        summary="decrease cart-product quantity",
        description="decrease cart-product quantity",
        response_description="The updated cart-product ID.",
    )
    async def decrease_quantity(
        entity_in: CartProductUpdateDTO,
        cart_product_service: CartProductService = Depends(get_cart_product_service),
        user: UserDTO = Depends(get_current_user),
    ) -> int:
        result = await cart_product_service.decrease_quantity(
            entity_in=entity_in
        )
        if result is None:
            raise CartProductNotFoundException
        
        return result