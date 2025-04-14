from asyncpg import Connection
from fastapi import APIRouter, HTTPException, status, Depends, Query
from core.schemas.pvz import PVZCreate, PVZResponse, PVZWithReceptions
from core.db_helper import get_db_connection
from auth.jwt import check_employee_role, check_moderator_role, check_any_role
from typing import List, Optional
from datetime import datetime
from uuid import UUID

from src.crud.product import delete_last_product_db, get_products_by_reception_id
from src.crud.pvz import create_pvz_db, get_pvz_db, get_pvz_list_db
from src.crud.reception import close_reception_db, get_open_reception_db, get_receptions_db


router = APIRouter(tags=["pvz"])


@router.post("/pvz", response_model=PVZResponse, status_code=status.HTTP_201_CREATED)
async def create_pvz(
    pvz_data: PVZCreate,
    conn: Connection = Depends(get_db_connection),
    user = Depends(check_moderator_role)
):
    """Create a new PVZ (Pickup Point). Only moderators can create PVZs."""
    if pvz_data.city not in ["Москва", "Санкт-Петербург", "Казань"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="PVZ can only be created in Moscow, Saint Petersburg, or Kazan"
        )

    new_pvz = await create_pvz_db(city=pvz_data.city, conn=conn)
        
    return new_pvz


@router.get("/pvz", response_model=List[PVZWithReceptions])
async def get_pvz_list(
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=30),
    conn: Connection = Depends(get_db_connection),
    user = Depends(check_any_role)
):
    """Get a list of PVZs with their receptions and products."""
    offset = (page - 1) * limit
    pvz_list = await get_pvz_list_db(
        conn=conn,
        start_date=start_date,
        end_date=end_date,
        limit=limit,
        offset=offset
    )

    result = []
    
    for pvz in pvz_list:
        receptions = await get_receptions_db(
            pvz_id=pvz["id"],
            conn=conn
        )
        
        pvz_with_receptions = dict(pvz)
        pvz_with_receptions["receptions"] = []
        
        for reception in receptions:
            products = await get_products_by_reception_id(
                reception_id=reception["id"],
                conn=conn
            )
            
            reception_with_products = dict(reception)
            reception_with_products["products"] = [dict(p) for p in products]
            pvz_with_receptions["receptions"].append(reception_with_products)
        
        result.append(pvz_with_receptions)
    
    return result


@router.post("/pvz/{pvz_id}/close_last_reception", response_model=dict)
async def close_last_reception(
    pvz_id: UUID,
    conn: Connection = Depends(get_db_connection),
    user = Depends(check_employee_role)
):
    """Close the last open reception for a PVZ."""
    pvz = await get_pvz_db(pvz_id=pvz_id, conn=conn)
    if not pvz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="PVZ not found"
        )

    reception = await get_open_reception_db(pvz_id=pvz_id, conn=conn)
    if not reception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No open reception found for this PVZ"
        )
    
    closed_reception = await close_reception_db(reception_id=reception["id"], conn=conn)
    
    return closed_reception


@router.post("/pvz/{pvz_id}/delete_last_product", status_code=status.HTTP_200_OK)
async def delete_last_product(
    pvz_id: UUID,
    conn: Connection = Depends(get_db_connection),
    user = Depends(check_employee_role)
):
    """Delete the last added product from an open reception (LIFO)."""
    pvz = await get_pvz_db(pvz_id=pvz_id, conn=conn)
    if not pvz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="PVZ not found"
        )

    reception = await get_open_reception_db(pvz_id=pvz_id, conn=conn)
    if not reception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No open reception found for this PVZ"
        )

    product_deleted = await delete_last_product_db(reception_id=reception["id"], conn=conn)
    if not product_deleted:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No products to delete in this reception"
        )

    return {"message": "Product successfully deleted"}
