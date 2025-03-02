from app.dto.base_dto import CreateDTO, BaseDTO


class CategoryCreateDTO(CreateDTO):
    title: str


class CategoryDTO(CategoryCreateDTO, BaseDTO):
    pass


class CategoryUpdateDTO(CategoryCreateDTO):
    pass
