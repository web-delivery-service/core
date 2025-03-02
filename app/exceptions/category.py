from app.exceptions.entity import EntityNotFoundException


class CategoryNotFoundException(EntityNotFoundException):
    detail = "Category is not found"
