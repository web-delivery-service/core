from typing import List
from app.services.base_service import BaseService

from app.db.dao.product_dao import ProductDAO
from app.dto.product_dto import ProductDTO, ProductFilterDTO
from app.utils.mapper import Mapper


class ProductService(BaseService):

    def __init__(
        self,
        session_factory,
    ):
        super().__init__(
            dto=ProductDTO,
            dao=ProductDAO(session_factory=session_factory),
        )

    async def get_by_category_id(self, *, category_id: int) -> List[ProductDTO]:
        result = await self.dao.get_by_category_id(category_id=category_id)
        return [Mapper.model_to_dto(model=model, dto=self.dto) for model in result]
    
    async def get_all(self, *, filter: ProductFilterDTO) -> List[ProductDTO]:
        result = await self.dao.get_all(filter=filter)
        return [Mapper.model_to_dto(model=model, dto=self.dto) for model in result]
