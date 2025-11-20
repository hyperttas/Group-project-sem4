import asyncio
from funcs import *
from async_funcs import *

#Current iteration of the program
version = 0.2

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
    return print("Startup checks successful!")

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
        await asyncio.sleep(10)

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
        await asyncio.sleep(8)

async def main():
    await startup()
    await asyncio.gather(
        read_jobs(),
        read_nodes(),
        
    )

if __name__ == "__main__":
    asyncio.run(main())