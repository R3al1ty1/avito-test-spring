from uuid import UUID
from datetime import datetime
from typing import List, Optional
from asyncpg import Connection


async def create_pvz_db(
    city: str,
    conn: Connection
) -> dict:
    """Функция для создания нового ПВЗ."""
    new_pvz = await conn.fetchrow(
        """
        INSERT INTO pvz (city)
        VALUES ($1)
        RETURNING id, registration_date, city
        """,
        city
    )

    return dict(new_pvz)


async def get_pvz_db(
    pvz_id: UUID,
    conn: Connection
) -> dict:
    """Функция для получения ПВЗ по ID."""
    pvz = await conn.fetchrow(
        "SELECT id, registration_date, city FROM pvz WHERE id = $1",
        str(pvz_id)
    )

    return dict(pvz) if pvz else None


async def get_pvz_list_db(
    conn: Connection,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    limit: int = 10,
    offset: int = 0
) -> List[dict]:
    """Функция для получения списка ПВЗ с фильтрацией по дате регистрации."""
    query = "SELECT id, registration_date, city FROM pvz"
    params = []

    if start_date or end_date:
        query += " WHERE id IN (SELECT pvz_id FROM receptions WHERE 1=1"
        if start_date:
            query += f" AND date_time >= ${len(params) + 1}"
            params.append(start_date)
        if end_date:
            query += f" AND date_time <= ${len(params) + 1}"
            params.append(end_date)
        query += ")"

    query += f" ORDER BY registration_date DESC LIMIT ${len(params) + 1}"
    params.append(limit)
    query += f" OFFSET ${len(params) + 1}"
    params.append(offset)

    return [dict(row) for row in await conn.fetch(query, *params)]


async def get_pvz_with_receptions_db(
    pvz_id: UUID,
    conn: Connection
) -> dict:
    """Функция для получения ПВЗ с его приемками и продуктами."""
    pvz = await get_pvz_db(pvz_id=pvz_id, conn=conn)
    if not pvz:
        return None
        
    receptions = await conn.fetch(
        """
        SELECT id, date_time, pvz_id, status
        FROM receptions
        WHERE pvz_id = $1
        ORDER BY date_time DESC
        """,
        str(pvz_id)
    )
    
    pvz["receptions"] = []
    for reception in receptions:
        reception_dict = dict(reception)
        products = await conn.fetch(
            """
            SELECT id, date_time, type, reception_id
            FROM products
            WHERE reception_id = $1
            ORDER BY order_in_reception ASC
            """,
            reception["id"]
        )
        reception_dict["products"] = [dict(p) for p in products]
        pvz["receptions"].append(reception_dict)
        
    return pvz
