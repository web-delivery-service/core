from typing import List

from app.dto.base_dto import CreateDTO, BaseDTO
from app.db.models.order import StatusEnum

from app.dto.user_dto import UserDTO
from app.dto.order_product_dto import OrderProductDTO


class OrderCreateDTO(CreateDTO):
    user_id: int
    status: StatusEnum | None
    cost: int


class OrderDTO(OrderCreateDTO, BaseDTO):
    user: UserDTO | None
    products: List[OrderProductDTO] | None

class OrderUpdateDTO(OrderCreateDTO):
    pass

class OrderUpdateStatusDTO(CreateDTO):
    status: StatusEnum | str