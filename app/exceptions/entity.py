from fastapi import status

from app.exceptions.base_exception import BaseException


class EntityNotFoundException(BaseException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Entity is not found"
