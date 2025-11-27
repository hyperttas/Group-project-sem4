import asyncio
from general.funcs import *
from general.async_funcs import *
from networking.secure_server import run_secure_server
from api.api import run_api_server

#Current iteration of the program
version = 0.5

delay_jobs = 10
delay_node = 10

async def startup(): #make it so startup() checks if they actually return True or return False
    print(f"Node & Job Controller V{version} Program startup...")
    print(50*"-" + "\n")
    minio_check()
    print("\n")

    await init_jobs_pool()
    await ensure_db_exists()
    print("\n")
    await ensure_jobs_table()
    await ensure_nodes_table()

    return print("All checks successful!")

async def read_jobs():
    while True:
        jobs = await get_jobs()

        if len(jobs) > 0:
            print("\nNew jobs found:\n" + 50*"-")
            for job in jobs:
                print(job)
            print(50*"-")
        else:
            print("\nNo new jobs found.\n")
        await asyncio.sleep(delay_jobs)

async def read_nodes():
    while True:
        nodes = await get_nodes()

        if len(nodes) > 0:
            print("Available nodes:")
            for node in nodes:
                if node[2] == 0:
                    print(node)
            print("\nCurrently busy nodes:")
            for node in nodes:
                if node[2] == 1:
                    print(node)
        else:
            print("Database does not contain any nodes, or there was an error connecting to the database.\n")
        await asyncio.sleep(delay_node)

async def main():
    await startup()
    await asyncio.gather(
        read_jobs(),
        read_nodes(),
        run_secure_server(),
        run_api_server(),
    )

if __name__ == "__main__":
    asyncio.run(main())