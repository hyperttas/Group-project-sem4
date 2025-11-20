import asyncpg
import common

async def init_jobs_pool():
    common.pool = await asyncpg.create_pool(
        user="postgres",
        password="Unholy31",
        database="postgres",
        host="localhost"
    )

async def ensure_db_exists():
    async with common.pool.acquire() as conn:
        exists = await conn.fetchval(
            "SELECT 1 FROM pg_database WHERE datname='postgres'"
        )

        if not exists:
            print("Database postgres does not exist, please fix the issue before proceeding.")
            return False
        else:
            print("Database postgres exists.")
            return True

async def ensure_jobs_table():
    async with common.pool.acquire() as conn:
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                id SERIAL PRIMARY KEY,
                task TEXT NOT NULL,
                script TEXT NOT NULL,
                status INTEGER NOT NULL DEFAULT 0
            );
        """)

async def ensure_nodes_table():
    async with common.pool.acquire() as conn:
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS nodes (
                id SERIAL PRIMARY KEY,
                address TEXT NOT NULL,
                status INTEGER NOT NULL DEFAULT 0
            );
        """)

async def get_jobs():
    async with common.pool.acquire() as conn:
        return await conn.fetch("SELECT * FROM jobs WHERE status = 0")

async def get_nodes():
    async with common.pool.acquire() as conn:
        return await conn.fetch("SELECT * FROM nodes")
