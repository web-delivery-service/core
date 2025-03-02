from app.db.dao.category_dao import CategoryDAO
from app.services.category_service import CategoryService
from app.dto.category_dto import CategoryDTO

from app.db.dao.product_dao import ProductDAO
from app.services.product_service import ProductService
from app.dto.product_dto import ProductDTO

from app.db.dao.cart_dao import CartDAO
from app.services.cart_service import CartService
from app.dto.cart_dto import CartDTO

from app.db.dao.cart_product_dao import CartProductDAO
from app.services.cart_product_service import CartProductService
from app.dto.cart_product_dto import CartProductDTO

from app.db.dao.user_dao import UserDAO
from app.services.user_service import UserService
from app.dto.user_dto import UserDTO

from app.db.db_manager import db_manager


def get_category_service():
    return CategoryService(
        dto=CategoryDTO,
        dao=CategoryDAO,
        session_factory=db_manager.session_factory,
    )


def get_product_service():
    return ProductService(
        dto=ProductDTO,
        dao=ProductDAO,
        session_factory=db_manager.session_factory,
    )


def get_cart_service():
    return CartService(
        dto=CartDTO,
        dao=CartDAO,
        session_factory=db_manager.session_factory,
    )


def get_cart_product_service():
    return CartProductService(
        dto=CartProductDTO,
        dao=CartProductDAO,
        session_factory=db_manager.session_factory,
    )


def get_user_service():
    return UserService(
        dto=UserDTO,
        dao=UserDAO,
        session_factory=db_manager.session_factory,
    )
