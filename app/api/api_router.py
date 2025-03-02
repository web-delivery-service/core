from fastapi import APIRouter

from app.api.controllers.category_controller import CategoryController
from app.api.controllers.product_controller import ProductController
from app.api.controllers.cart_product_controller import CartProductController
from app.api.controllers.cart_controller import CartController
from app.api.controllers.auth_controller import AuthController

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(AuthController.router, tags=["Auth"])
api_router.include_router(CategoryController.router, tags=["Categories"])
api_router.include_router(ProductController.router, tags=["Products"])
api_router.include_router(CartController.router, tags=["Carts"])
api_router.include_router(CartProductController.router, tags=["Cart-products"])
