from app.dto.base_dto import CreateDTO, BaseDTO


class CartCreateDTO(CreateDTO):
    user_id: int


class CartDTO(CartCreateDTO, BaseDTO):
    pass
