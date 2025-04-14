from typing import AsyncGenerator
import asyncpg
import os
from contextlib import asynccontextmanager
from asyncpg import Connection


DB_HOST = os.getenv('POSTGRES_HOST', 'db')
DB_PORT = os.getenv('POSTGRES_PORT', '5432')
DB_NAME = os.getenv('POSTGRES_DB', 'pvz_db')
DB_USER = os.getenv('POSTGRES_USER', 'postgres')
DB_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'postgres')

async def get_connection():
    """Create a new database connection"""
    return await asyncpg.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

@asynccontextmanager
async def get_db_pool():
    """Context manager for database connection pool"""
    pool = await asyncpg.create_pool(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    try:
        yield pool
    finally:
        await pool.close()

@asynccontextmanager
async def get_db_conn():
    """Context manager for single database connection"""
    conn = await get_connection()
    try:
        yield conn
    finally:
        await conn.close()


async def get_db_connection():
    async with get_db_conn() as conn:
        yield conn
