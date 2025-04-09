from typing import Optional
from fastapi import Query

from app.dto.base_dto import CreateDTO, BaseDTO, UpdateDTO, BaseModel


class ProductCreateDTO(CreateDTO):
    category_id: int
    title: str
    quantity: int = 1
    cost: int
    info: str | None


class ProductDTO(BaseDTO):
    category_id: int
    title: str
    quantity: int = 1
    cost: int
    info: str | None
    image_id: str | None


class ProductUpdateDTO(UpdateDTO):
    category_id: int | None
    title: str | None
    quantity: int | None
    cost: int | None
    info: str | None


class ProductImageIDUpdateDTO(CreateDTO):
    image_id: str | None


class ProductFilterDTO(CreateDTO):
    title: Optional[str] = Query(None, description="Filter by product title")
    category_id: Optional[int] = Query(None, gt=0, description="Filter by category ID")
    min_cost: Optional[int] = Query(None, gt=0, description="Minimum product cost")
    max_cost: Optional[int] = Query(None, gt=0, description="Maximum product cost")

    class Config:
        extra = "forbid"

    
def get_product_filter_params(
    title: Optional[str] = Query(None),
    categoryId: Optional[int] = Query(None, gt=0),
    minCost: Optional[int] = Query(None, gt=0),
    maxCost: Optional[int] = Query(None, gt=0),
) -> ProductFilterDTO:
    return ProductFilterDTO(
        title=title,
        category_id=categoryId,
        min_cost=minCost,
        max_cost=maxCost
    )


