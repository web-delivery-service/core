from app.db.models.base import ModelType
from app.dto.base_dto import DTOType

from app.dto.user_dto import UserDTO
from app.dto.order_product_dto import OrderProductDTO, OrderProductWithProductDTO
from app.dto.product_dto import ProductDTO


class Mapper:

    @classmethod
    def dto_to_dict(cls, *, dto: DTOType):
        return dto.model_dump()

    @classmethod
    def model_to_dto(cls, *, model: ModelType, dto: DTOType):
        if model is None:
            return None
        return dto.model_validate(model)
    

    @classmethod
    def model_to_dto_with_relations(cls, *, model: ModelType, dto: DTOType):
        if model is None:
            return None
        
        model_dict = {c.name: getattr(model, c.name) for c in model.__table__.columns}
        
        if hasattr(model, 'user'):
            model_dict['user'] = cls.model_to_dto(model=model.user, dto=UserDTO)
        
        if hasattr(model, 'products'):
            model_dict['products'] = [
                cls.model_to_dto(model=order_product, dto=OrderProductDTO)
                for order_product in model.products
            ]

        if hasattr(model, 'product'):
            model_dict['product'] = cls.model_to_dto(model=model.product, dto=ProductDTO)
        
        return dto.model_validate(model_dict)


    @classmethod
    def dto_to_dto(cls, *, dto_from: DTOType, dto_to: DTOType):
        return dto_to.model_validate(dto_from)
