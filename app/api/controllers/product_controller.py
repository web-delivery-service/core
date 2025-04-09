from typing import List
from uuid import uuid4
from fastapi import APIRouter, Depends, UploadFile, status, File

from app.api.controllers.controller_contract import ControllerContract

from app.dto.product_dto import (
    ProductDTO,
    ProductCreateDTO,
    ProductUpdateDTO,
    ProductImageIDUpdateDTO,
    ProductFilterDTO    
)

from app.dto.product_dto import get_product_filter_params

from app.services.product_service import ProductService

from app.api.deps import get_product_service
from app.exceptions.product import ProductNotFoundException
from app.exceptions.S3 import S3ConnectionException
from app.S3.service import s3_service


class ProductController(ControllerContract):

    router = APIRouter(prefix="/products")

    @router.get(
        "",
        response_model=List[ProductDTO],
        summary="Get all products",
        description="Retrieve a list of all products.",
        response_description="A list of products.",
    )
    async def get_all(
        filter: ProductFilterDTO = Depends(get_product_filter_params),
        product_service: ProductService = Depends(get_product_service),
    ) -> List[ProductDTO]:
        return await product_service.get_all(filter=filter)
    
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
        "",
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
        
    @router.post(
        "/{id}/image",
        status_code=status.HTTP_201_CREATED,
        summary="Upload an image for a product",
        description="Upload an image for a product by its ID.",
        response_description="details",
    )
    async def upload_image(
        id: int,
        image: UploadFile = File(...),
        product_service: ProductService = Depends(get_product_service),
    ):
        uuid = uuid4().hex
        try:
            await s3_service.upload_file(file=image, object_name=uuid)
        except Exception as e:
            raise S3ConnectionException
        
        await product_service.update(id=id, entity_in=ProductImageIDUpdateDTO(image_id=uuid))

        return {
            "message": "Image uploaded successfully"
        }

    @router.delete(
        "/{id}/image",
        status_code=status.HTTP_204_NO_CONTENT,
        summary="Delete an image for a product",
        description="Delete an image for a product by its ID.",
        response_description="No content.",
    )
    async def delete_image(
        id: int,
        product_service: ProductService = Depends(get_product_service),
    ):
        result: ProductDTO = await product_service.get_by_id(id=id)
        if not result:
            raise ProductNotFoundException
        
        try:
            await s3_service.delete_file(object_name=result.image_id)
        except Exception as e:
            raise S3ConnectionException
        
        await product_service.update(id=id, entity_in=ProductImageIDUpdateDTO(image_id=None))