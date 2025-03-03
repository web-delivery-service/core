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


class OrderProductController(ControllerContract):

    router = APIRouter(prefix="/order-products")
