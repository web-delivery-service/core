from fastapi import HTTPException, status


class BaseException(HTTPException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Something goes wrong"

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)
