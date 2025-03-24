from app.exceptions.entity import EntityNotFoundException


class S3ConnectionException(EntityNotFoundException):
    detail = "S3 connection error"
