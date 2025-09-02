from fastapi import status

from app.exceptions.base_exception import BaseException


class UserAlreadyExistsEmailException(BaseException):
    status_code = status.HTTP_409_CONFLICT
    detail = "User with this email already exists"


class PasswordLengthException(BaseException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Password must have 3 and more symbols "


class UserDoesNotExist(BaseException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "User does not exist"


class IncorrectPasswordOrEmailException(BaseException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Incorrect email or password"
    headers = {"WWW-Authenticate": "Bearer"}


class TokenDoesNotExistException(BaseException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Token does not exist"
    headers = {"WWW-Authenticate": "Bearer"}


class InvalidTokenTypeException(BaseException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Invlid token type"
    headers = {"WWW-Authenticate": "Bearer"}


class InvalidOrExpiredTokenException(BaseException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Could not validate credentials (Invalid Token)"
    headers = {"WWW-Authenticate": "Bearer"}


class LackOfPermisionsExceptions(BaseException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "You have not permisions"
    headers = {"WWW-Authenticate": "Bearer"}


class EmailAlreadyExistsException(BaseException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Email already exists"
