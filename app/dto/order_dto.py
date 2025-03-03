from app.dto.base_dto import CreateDTO, BaseDTO
from app.db.models.order import StatusEnum


class OrderCreateDTO(CreateDTO):
    user_id: int
    status: StatusEnum
    cost: int


class OrderDTO(OrderCreateDTO, BaseDTO):
    pass


class OrderUpdateDTO(OrderCreateDTO):
    pass
