from asyncpg import Connection
from fastapi import APIRouter, HTTPException, status, Depends
from core.schemas.reception import ReceptionCreate, ReceptionResponse
from core.db_helper import get_db_connection
from auth.jwt import check_employee_role
from src.crud.pvz import get_pvz_db
from src.crud.reception import create_reception_db, get_open_reception_db


router = APIRouter(tags=["reception"])


@router.post("/receptions", response_model=ReceptionResponse, status_code=status.HTTP_201_CREATED)
async def create_reception(
    reception_data: ReceptionCreate,
    conn: Connection = Depends(get_db_connection),
    user = Depends(check_employee_role)
):
    """Create a new reception for products at a PVZ."""
    pvz = await get_pvz_db(pvz_id=reception_data.pvz_id, conn=conn)
    if not pvz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="PVZ not found"
        )
    
    existing_reception = await get_open_reception_db(pvz_id=reception_data.pvz_id, conn=conn)
    if existing_reception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="There is already an open reception for this PVZ"
        )
    
    new_reception = await create_reception_db(pvz_id=reception_data.pvz_id, conn=conn)
    
    return new_reception
