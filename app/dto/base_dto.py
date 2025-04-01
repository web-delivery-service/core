from pydantic import BaseModel, ConfigDict
from typing import TypeVar

from app.utils.camel import to_camel


class CreateDTO(BaseModel):
    model_config = ConfigDict(
        from_attributes=True, alias_generator=to_camel, populate_by_name=True, arbitrary_types_allowed=True
    )


class BaseDTO(CreateDTO):
    id: int


class UpdateDTO(CreateDTO):
    pass


DTOType = TypeVar("DTOType", bound=BaseDTO)
CreateDTOType = TypeVar("CreateDTOType", bound=CreateDTO)
UpdateDTOType = TypeVar("UpdateDTOType", bound=UpdateDTO)
