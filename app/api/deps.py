from app.auth.auth_service import AuthService
from app.services.category_service import CategoryService
from app.services.product_service import ProductService
from app.services.cart_service import CartService
from app.services.cart_product_service import CartProductService
from app.services.user_service import UserService
from app.services.order_service import OrderService
from app.services.order_product_service import OrderProductService
from app.services.stats_service import StatsService

from app.db.db_manager import db_manager


def get_auth_service():
    return AuthService(
        session_factory=db_manager.session_factory,
    )


def get_category_service():
    return CategoryService(
        session_factory=db_manager.session_factory,
    )


def get_product_service():
    return ProductService(
        session_factory=db_manager.session_factory,
    )


def get_cart_service():
    return CartService(
        session_factory=db_manager.session_factory,
    )


def get_cart_product_service():
    return CartProductService(
        session_factory=db_manager.session_factory,
    )


def get_user_service():
    return UserService(
        session_factory=db_manager.session_factory,
    )


def get_order_service():
    return OrderService(
        session_factory=db_manager.session_factory,
    )


def get_order_product_service():
    return OrderProductService(
        session_factory=db_manager.session_factory,
    )


def get_stats_service():
    return StatsService(
        session_factory=db_manager.session_factory,
    )