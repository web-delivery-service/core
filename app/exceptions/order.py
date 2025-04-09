from app.exceptions.entity import EntityNotFoundException


class OrderNotFoundException(EntityNotFoundException):
    detail = "Order is not found"
