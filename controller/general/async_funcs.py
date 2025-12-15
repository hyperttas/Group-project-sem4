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

async def ensure_tables():
    async with pool.acquire() as conn:
        jobs_columns = await conn.fetch("""
                                   SELECT column_name, data_type
                                   FROM information_schema.columns
                                   WHERE table_name = 'jobs'
                                     AND table_schema = 'public'
                                   ORDER BY ordinal_position;
                                   """)
        nodes_columns = await conn.fetch("""
                                   SELECT column_name, data_type
                                   FROM information_schema.columns
                                   WHERE table_name = 'nodes'
                                     AND table_schema = 'public'
                                   ORDER BY ordinal_position;
                                   """)

        if jobs_columns and nodes_columns:
            print("jobs columns:", [dict(row) for row in jobs_columns],"\n","nodes columns:", [dict(row) for row in nodes_columns])
        else:
            print(f"ERROR: One or both tables could not be found.")

async def get_jobs():
    async with pool.acquire() as conn:
        return await conn.fetch("SELECT * FROM jobs")

async def get_nodes():
    async with pool.acquire() as conn:
        return await conn.fetch("SELECT * FROM nodes")

async def job_active(job_id):
    async with pool.acquire() as conn:
        await conn.fetchrow("UPDATE jobs SET status = 1 WHERE job_id = $1", job_id)

async def save_result(job_id, result):
    async with pool.acquire() as conn:
        await conn.execute("UPDATE jobs SET result = $1 WHERE job_id = $2", result, job_id)

async def node_online(node_ip):
    async with pool.acquire() as conn:
        await conn.execute("UPDATE nodes SET status = $2 WHERE node_name = $1", node_ip, "online")

async def register_node(node_ip):
    async with pool.acquire() as conn:
        await conn.execute("INSERT INTO nodes (node_name, ip_addresses) VALUES ($1, $2)", node_ip, [node_ip])