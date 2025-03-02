from app.db.models.base import ModelType
from app.dto.base_dto import DTOType


class Mapper:

    @classmethod
    def dto_to_dict(cls, *, dto: DTOType):
        return dto.model_dump()

    @classmethod
    def model_to_dto(cls, *, model: ModelType, dto: DTOType):
        return dto.model_validate(model)
