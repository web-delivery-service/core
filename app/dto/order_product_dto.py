from app.dto.base_dto import CreateDTO, BaseDTO
from app.dto.product_dto import ProductDTO


class OrderProductCreateDTO(CreateDTO):
    order_id: int
    product_id: int
    quantity: int

class OrderProductWithProductDTO(OrderProductCreateDTO):
    product: ProductDTO

class OrderProductDTO(OrderProductCreateDTO):
    pass
