from typing import List, Optional
from sqlalchemy import select, delete, insert, update
from sqlalchemy.ext.asyncio import AsyncResult, AsyncSession


from app.db.models.base import ModelType


class CRUDBaseDAO:
    model: ModelType = None

    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def get_by_id(self, *, entity_id: int) -> ModelType:
        async with self.session_factory() as conn:
            query = select(self.model).filter_by(id=entity_id)
            result: AsyncResult = await conn.execute(query)
            return result.scalar_one_or_none()

    async def get_all(self) -> List[ModelType]:
        async with self.session_factory() as conn:
            query = select(self.model)
            result: AsyncResult = await conn.execute(query)
            return result.scalars().all()

    async def get_by_user_id(self, *, user_id: int, one_instance: bool = False) -> List[ModelType]:
        async with self.session_factory() as conn:
            query = select(self.model).filter_by(user_id=user_id)
            result: AsyncResult = await conn.execute(query)
            if one_instance:
                return result.scalar_one_or_none()
            return result.scalars().all()

    async def create(self, *, entity_in: dict) -> Optional[ModelType]:
        async with self.session_factory() as conn:
            async with conn.begin():
                query = insert(self.model).values(**entity_in).returning(self.model)
                result: AsyncResult = await conn.execute(query)
                return result.scalar_one_or_none()

    async def update(self, *, entity_in: dict, entity_id: int) -> Optional[ModelType]:
        async with self.session_factory() as conn:
            async with conn.begin():
                query = (
                    update(self.model)
                    .values(**entity_in)
                    .filter_by(id=entity_id)
                    .returning(self.model)
                )
                result: AsyncResult = await conn.execute(query)
                return result.scalar_one_or_none()

    async def delete(self, *, entity_id: int) -> Optional[int]:
        async with self.session_factory() as conn:
            async with conn.begin():
                query = (
                    delete(self.model).filter_by(id=entity_id).returning(self.model.id)
                )
                result: AsyncResult = await conn.execute(query)
                return result.scalar()
