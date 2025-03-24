from app.dto.base_dto import CreateDTO, BaseDTO, UpdateDTO


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


class ProductImageIDUpdateDTO(BaseDTO):
    image_id: str