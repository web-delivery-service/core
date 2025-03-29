from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.dto.base_dto import (
    DTOType,
    CreateDTOType,
    UpdateDTOType,
)
from app.db.dao.crudbase_dao import CRUDBaseDAO

from app.utils.mapper import Mapper


class BaseService:

    def __init__(
        self,
        dto: DTOType,
        dao: CRUDBaseDAO,
    ):
        self.dao: CRUDBaseDAO = dao
        self.dto: DTOType = dto

    async def get_all(self) -> List[DTOType]:
        result = await self.dao.get_all()
        return [Mapper.model_to_dto(model=model, dto=self.dto) for model in result]

    async def get_by_id(self, *, id: int) -> Optional[DTOType]:
        result = await self.dao.get_by_id(entity_id=id)
        if result is None:
            return None
        return Mapper.model_to_dto(model=result, dto=self.dto)

    async def get_by_user_id(self, *, user_id: int, one_instance: bool = False) -> List[DTOType]:
        result = await self.dao.get_by_user_id(user_id=user_id, one_instance=one_instance)
        if one_instance:
            return Mapper.model_to_dto(model=result, dto=self.dto)
        return [Mapper.model_to_dto(model=model, dto=self.dto) for model in result]

    async def create(self, *, entity_in: CreateDTOType) -> Optional[DTOType]:
        result = await self.dao.create(entity_in=Mapper.dto_to_dict(dto=entity_in))
        return Mapper.model_to_dto(model=result, dto=self.dto)

    async def update(self, *, id: int, entity_in: UpdateDTOType) -> Optional[DTOType]:
        result = await self.dao.update(
            entity_id=id, entity_in=Mapper.dto_to_dict(dto=entity_in)
        )
        if result is None:
            return None
        return Mapper.model_to_dto(model=result, dto=self.dto)

    async def delete(self, *, id: int) -> Optional[int]:
        return await self.dao.delete(entity_id=id)
