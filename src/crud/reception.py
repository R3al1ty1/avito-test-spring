from uuid import UUID
from asyncpg import Connection


async def create_reception_db(
    pvz_id: UUID,
    conn: Connection
) -> dict:
    """Create new reception"""
    new_reception = await conn.fetchrow(
        """
        INSERT INTO receptions (pvz_id, status)
        VALUES ($1, 'in_progress')
        RETURNING id, date_time, pvz_id, status
        """,
        str(pvz_id)
    )

    return dict(new_reception)


async def get_open_reception_db(
    pvz_id: UUID,
    conn: Connection
) -> dict:
    """Get open reception for PVZ"""
    reception = await conn.fetchrow(
        """
        SELECT id, date_time, pvz_id, status
        FROM receptions
        WHERE pvz_id = $1 AND status = 'in_progress'
        """,
        str(pvz_id)
    )

    return dict(reception) if reception else None


async def get_receptions_db(
    pvz_id: UUID,
    conn: Connection
) -> dict:
    receptions = await conn.fetch(
        """
        SELECT id, date_time, pvz_id, status
        FROM receptions
        WHERE pvz_id = $1
        ORDER BY date_time DESC
        """,
        pvz_id
    )

    return receptions


async def close_reception_db(
    reception_id: UUID,
    conn: Connection
) -> dict:
    """Close reception"""
    updated_reception = await conn.fetchrow(
        """
        UPDATE receptions
        SET status = 'close'
        WHERE id = $1
        RETURNING id, date_time, pvz_id, status
        """,
        str(reception_id)
    )

    return dict(updated_reception) if updated_reception else None
