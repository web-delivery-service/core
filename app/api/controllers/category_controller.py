from typing import List
from fastapi import APIRouter, Depends, status

from app.api.controllers.controller_contract import ControllerContract

from app.dto.category_dto import (
    CategoryDTO,
    CategoryCreateDTO,
    CategoryUpdateDTO,
)
from app.services.category_service import CategoryService

from app.api.deps import get_category_service
from app.exceptions.category import CategoryNotFoundException


class CategoryController(ControllerContract):

    router = APIRouter(prefix="/categories")

    @router.get(
        "/",
        response_model=List[CategoryDTO],
        summary="Get all categories",
        description="Retrieve a list of all categories.",
        response_description="A list of categories.",
    )
    async def get_all(
        category_service: CategoryService = Depends(get_category_service),
    ) -> List[CategoryDTO]:
        return await category_service.get_all()

    @router.get(
        "/{id}",
        response_model=CategoryDTO,
        summary="Get a category by ID",
        description="Retrieve a specific category by its ID.",
        response_description="The requested category.",
    )
    async def get_one(
        id: int,
        category_service: CategoryService = Depends(get_category_service),
    ) -> CategoryDTO:
        result = await category_service.get_by_id(id=id)
        if not result:
            raise CategoryNotFoundException
        return result

    @router.post(
        "/",
        response_model=CategoryDTO,
        status_code=status.HTTP_201_CREATED,
        summary="Create a new category",
        description="Create a new category with the provided data.",
        response_description="The created category.",
    )
    async def store(
        entity_in: CategoryCreateDTO,
        category_service: CategoryService = Depends(get_category_service),
    ) -> CategoryDTO:
        return await category_service.create(entity_in=entity_in)

    @router.patch(
        "/{id}",
        response_model=CategoryDTO,
        summary="Update a category",
        description="Update an existing category with the provided data.",
        response_description="The updated category.",
    )
    async def update(
        id: int,
        entity_in: CategoryUpdateDTO,
        category_service: CategoryService = Depends(get_category_service),
    ) -> CategoryDTO:
        result = await category_service.update(id=id, entity_in=entity_in)
        if not result:
            raise CategoryNotFoundException
        return result

    @router.delete(
        "/{id}",
        status_code=status.HTTP_204_NO_CONTENT,
        summary="Delete a category",
        description="Delete a category by its ID.",
        response_description="No content.",
    )
    async def delete(
        id: int,
        category_service: CategoryService = Depends(get_category_service),
    ) -> None:
        result = await category_service.delete(id=id)
        if not result:
            raise CategoryNotFoundException
