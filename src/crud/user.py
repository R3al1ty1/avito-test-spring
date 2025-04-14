from asyncpg import Connection


async def create_user_db(
    email: str,
    password_hash: str,
    role: str,
    conn: Connection
) -> dict:
    """Create new user"""
    new_user = await conn.fetchrow(
        """
        INSERT INTO users (email, password_hash, role)
        VALUES ($1, $2, $3)
        RETURNING id, email, role
        """,
        email, password_hash, role
    )

    return dict(new_user)


async def get_user_by_email_db(
    email: str,
    conn: Connection
) -> dict:
    """Get user by email"""
    user = await conn.fetchrow(
        "SELECT id, email, password_hash, role FROM users WHERE email = $1",
        email
    )

    return dict(user) if user else None


async def check_user_exists_db(
    email: str,
    conn: Connection
) -> bool:
    """Check if user exists by email"""
    user = await conn.fetchrow(
        "SELECT id FROM users WHERE email = $1",
        email
    )

    return bool(user)
