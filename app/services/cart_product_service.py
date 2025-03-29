from typing import List, Optional
from app.services.base_service import BaseService

from app.db.dao.cart_product_dao import CartProductDAO
from app.dto.cart_product_dto import CartProductDTO, CartProductDeleteDTO, CartProductUpdateDTO
from app.utils.mapper import Mapper


class CartProductService(BaseService):

    def __init__(
        self,
        session_factory,
    ):
        super().__init__(
            dto=CartProductDTO,
            dao=CartProductDAO(session_factory=session_factory),
        )

    async def get_by_cart_id(self, *, cart_id: int) -> List[CartProductDTO]:
        result = await self.dao.get_by_cart_id(cart_id=cart_id)
        return [Mapper.model_to_dto(model=model, dto=self.dto) for model in result]
    
    async def delete(self, *, entity_in: CartProductDeleteDTO) -> Optional[int]:
        return await self.dao.delete(entity_in=entity_in)
    
    async def increase_quantity(self, *, entity_in: CartProductUpdateDTO) -> Optional[int]:
        result = await self.dao.increase_quantity(
            entity_in=entity_in
        )
        if result is None:
            return None
        return result
    
    async def decrease_quantity(self, *, entity_in: CartProductUpdateDTO) -> Optional[int]:
        result = await self.dao.decrease_quantity(
            entity_in=entity_in
        )
        if result is None:
            return None
        return result