from app.exceptions.entity import EntityNotFoundException


class ProductNotFoundException(EntityNotFoundException):
    detail = "Product is not found"
