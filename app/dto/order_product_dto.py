from app.dto.base_dto import CreateDTO, BaseDTO


class OrderProductCreateDTO(CreateDTO):
    order_id: int
    product_id: int
    quantity: int


class OrderProductDTO(OrderProductCreateDTO):
    pass
