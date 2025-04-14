from fastapi import APIRouter, HTTPException, status, Depends
from core.schemas.product import ProductCreate, ProductResponse
from core.db_helper import get_db_connection
from auth.jwt import check_employee_role
from asyncpg import Connection

from crud.product import create_product_db
from crud.pvz import get_pvz_db
from crud.reception import get_open_reception_db


router = APIRouter(tags=["products"])


@router.post("/products", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    product_data: ProductCreate,
    conn: Connection = Depends(get_db_connection),
    user = Depends(check_employee_role)
):
    """Эндпоинт создания нового продукта."""
    if product_data.type not in ["электроника", "одежда", "обувь"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid product type, must be 'электроника', 'одежда', or 'обувь'"
        )
    pvz = await get_pvz_db(pvz_id=product_data.pvz_id, conn=conn)
    if not pvz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="PVZ not found"
        )

    reception = await get_open_reception_db(pvz_id=product_data.pvz_id, conn=conn)
    if not reception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No open reception found for this PVZ"
        )

    new_product = await create_product_db()
    
    return new_product
