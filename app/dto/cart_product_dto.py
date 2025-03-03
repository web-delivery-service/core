from app.dto.base_dto import CreateDTO, BaseDTO


class CartProductCreateDTO(CreateDTO):
    cart_id: int
    product_id: int
    quantity: int


class CartProductDTO(CartProductCreateDTO):
    pass


class CartProductUpdateDTO(CartProductCreateDTO):
    pass
