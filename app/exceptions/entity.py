from app.exceptions.base_exception import BaseException


class EntityNotFoundException(BaseException):
    status_code = 404
    detail = "Entity is not found"
