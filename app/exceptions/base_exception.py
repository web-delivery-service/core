from fastapi import HTTPException


class BaseException(HTTPException):
    status_code = 500
    detail = "Something goes wrong"

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)
