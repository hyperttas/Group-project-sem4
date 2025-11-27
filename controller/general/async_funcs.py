import asyncpg
import common
import os
from dotenv import load_dotenv

load_dotenv()
user = os.environ.get("db_user")
db_pass = os.environ.get("db_pass")
db = os.environ.get("db_name")
host = os.environ.get("db_host")

pool = common.pool

async def init_jobs_pool():
    global pool
    pool = await asyncpg.create_pool(
        user=user,
        password=db_pass,
        database=db,
        host=host
    )

async def ensure_db_exists():
    async with pool.acquire() as conn:
        exists = await conn.fetchval(
            "SELECT 1 FROM pg_database WHERE datname = $1 LIMIT 1;",
            db
        )

        if not exists:
            print("Database postgres does not exist, please fix the issue before proceeding.")
            return False
        else:
            print("Database postgres exists.")
            return True

async def ensure_jobs_table():
    async with pool.acquire() as conn:
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                id SERIAL PRIMARY KEY,
                task TEXT NOT NULL,
                script TEXT NOT NULL,
                status INTEGER NOT NULL DEFAULT 0
            );
        """)

async def ensure_nodes_table():
    async with pool.acquire() as conn:
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS nodes (
                id SERIAL PRIMARY KEY,
                address TEXT NOT NULL,
                status INTEGER NOT NULL DEFAULT 0
            );
        """)

async def get_jobs():
    async with pool.acquire() as conn:
        return await conn.fetch("SELECT * FROM jobs WHERE status = 0")

async def get_nodes():
    async with pool.acquire() as conn:
        return await conn.fetch("SELECT * FROM nodes")
