from typing import Optional
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncResult

from app.db.models.user import User
from app.db.models.base import ModelType

from app.db.dao.crudbase_dao import CRUDBaseDAO


class UserDAO(CRUDBaseDAO):
    model: ModelType = User

    def __init__(self, session_factory):
        super().__init__(session_factory=session_factory)

    async def get_by_email(self, *, email: str) -> Optional[User]:
        async with self.session_factory() as conn:
            query = select(self.model).where(self.model.email == email)
            result: AsyncResult = await conn.execute(query)
            return result.scalar_one_or_none()
        

    async def delete_test_user(self) -> None:
        async with self.session_factory() as conn:
            async with conn.begin():
                query = (
                    delete(self.model).filter_by(email='test@example.com')
                )
                await conn.execute(query)

