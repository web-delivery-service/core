from typing import List
from fastapi import APIRouter, Depends, status

from app.api.controllers.controller_contract import ControllerContract

from app.dto.product_dto import (
    ProductDTO,
    ProductCreateDTO,
    ProductUpdateDTO,
)
from app.services.product_service import ProductService

from app.api.deps import get_product_service
from app.exceptions.product import ProductNotFoundException


class ProductController(ControllerContract):

    router = APIRouter(prefix="/products")

    @router.get(
        "/",
        response_model=List[ProductDTO],
        summary="Get all products",
        description="Retrieve a list of all products.",
        response_description="A list of products.",
    )
    async def get_all(
        product_service: ProductService = Depends(get_product_service),
    ) -> List[ProductDTO]:
        return await product_service.get_all()

    @router.get(
        "/{id}",
        response_model=ProductDTO,
        summary="Get a product by ID",
        description="Retrieve a specific product by its ID.",
        response_description="The requested product.",
    )
    async def get_one(
        id: int,
        product_service: ProductService = Depends(get_product_service),
    ) -> ProductDTO:
        result = await product_service.get_by_id(id=id)
        if not result:
            raise ProductNotFoundException
        return result

    @router.post(
        "/",
        response_model=ProductDTO,
        status_code=status.HTTP_201_CREATED,
        summary="Create a new product",
        description="Create a new product with the provided data.",
        response_description="The created product.",
    )
    async def store(
        entity_in: ProductCreateDTO,
        product_service: ProductService = Depends(get_product_service),
    ) -> ProductDTO:
        return await product_service.create(entity_in=entity_in)

    @router.patch(
        "/{id}",
        response_model=ProductDTO,
        summary="Update a product",
        description="Update an existing product with the provided data.",
        response_description="The updated product.",
    )
    async def update(
        id: int,
        entity_in: ProductUpdateDTO,
        product_service: ProductService = Depends(get_product_service),
    ) -> ProductDTO:
        result = await product_service.update(id=id, entity_in=entity_in)
        if not result:
            raise ProductNotFoundException
        return result

    @router.delete(
        "/{id}",
        status_code=status.HTTP_204_NO_CONTENT,
        summary="Delete a product",
        description="Delete a product by its ID.",
        response_description="No content.",
    )
    async def delete(
        id: int,
        product_service: ProductService = Depends(get_product_service),
    ):
        result = await product_service.delete(id=id)
        if not result:
            raise ProductNotFoundException
