from typing import List
from fastapi import APIRouter, Depends, status

from app.api.controllers.controller_contract import ControllerContract

from app.dto.cart_dto import (
    CartDTO,
    CartCreateDTO,
)

from app.dto.user_dto import UserDTO
from app.dto.product_dto import ProductDTO

from app.services.product_service import ProductService
from app.services.cart_product_service import CartProductService
from app.services.cart_service import CartService

from app.api.deps import get_cart_service, get_product_service, get_cart_product_service
from app.auth.deps import get_current_user

from app.exceptions.cart import CartNotFoundException


class CartController(ControllerContract):

    router = APIRouter(prefix="/carts")

    @router.get(
        "/{id}/products",
        response_model=List[ProductDTO],
        summary="Get all products by cart",
        description="Retrieve a list of all categories.",
        response_description="A list of categories.",
    )
    async def get_products_by_cart(
        id: int,
        product_service: ProductService = Depends(get_product_service),
        user: UserDTO = Depends(get_current_user),
    ) -> List[ProductDTO]:
        return await product_service.get_by_category_id(category_id=id)
    
    @router.get(
        "",
        response_model=CartDTO,
        summary="Get cart by user",
        description="Retrieve a cart by user.",
        response_description="The requested cart.",
    )
    async def get_one(
        cart_service: CartService = Depends(get_cart_service),
        user: UserDTO = Depends(get_current_user),
    ) -> CartDTO:
        result = await cart_service.get_by_user_id(user_id=user.id, one_instance=True)
        if not result:
            raise CartNotFoundException
        return result
