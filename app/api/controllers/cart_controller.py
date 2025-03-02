from typing import List
from fastapi import APIRouter, Depends, status

from app.api.controllers.controller_contract import ControllerContract

from app.dto.cart_dto import (
    CartDTO,
    CartCreateDTO,
)
from app.dto.product_dto import ProductDTO

from app.services.product_service import ProductService
from app.services.cart_product_service import CartProductService

from app.api.deps import get_cart_service, get_product_service, get_cart_product_service
from app.exceptions.category import CategoryNotFoundException


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
        product_service: ProductService = Depends(get_product_service),
    ) -> List[ProductDTO]:
        return await product_service.get_all()
