from fastapi import APIRouter
from .pvz import router as router_pvzs
from .reception import router as router_receptions
from .product import router as router_products
from .user import router as router_user


router = APIRouter()

router.include_router(
    router_products,
)

router.include_router(
    router_pvzs,
)

router.include_router(
    router_receptions,
)

router.include_router(
    router_user,
)
