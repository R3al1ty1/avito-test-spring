from uuid import UUID
from asyncpg import Connection


async def create_product_db(
    product_type: str,
    reception_id: UUID,
    conn: Connection
) -> dict:
    """Create new product"""
    new_product = await conn.fetchrow(
        """
        INSERT INTO products (type, reception_id)
        VALUES ($1, $2)
        RETURNING id, date_time, type, reception_id
        """,
        product_type, str(reception_id)
    )

    return dict(new_product)


async def get_products_by_reception_id(
    reception_id: UUID,
    conn: Connection
) -> dict:
    products = await conn.fetch(
        """
        SELECT id, date_time, type, reception_id
        FROM products
        WHERE reception_id = $1
        ORDER BY order_in_reception ASC
        """,
        reception_id
    )

    return products

async def delete_last_product_db(
    reception_id: UUID,
    conn: Connection
) -> bool:
    """Delete last product from reception"""
    product = await conn.fetchrow(
        """
        DELETE FROM products
        WHERE id = (
            SELECT id FROM products
            WHERE reception_id = $1
            ORDER BY order_in_reception DESC
            LIMIT 1
        )
        RETURNING id
        """,
        str(reception_id)
    )

    return bool(product)
