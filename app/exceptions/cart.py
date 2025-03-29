from fastapi import status

from app.exceptions.entity import EntityNotFoundException
from app.exceptions.base_exception import BaseException


class CartNotFoundException(EntityNotFoundException):
    detail = "Cart is not found"

class CartProductNotFoundException(EntityNotFoundException):
    detail = "Cart product is not found"

class CartProductQuantityLimitException(BaseException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Cart product quantity limit exceeded"
