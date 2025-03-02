from app.exceptions.entity import EntityNotFoundException


class CartNotFoundException(EntityNotFoundException):
    detail = "Cart is not found"
