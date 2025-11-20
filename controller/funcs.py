import common
from common import client

def minio_check():
    print("Performing MinIO check...")
    try:
        if not client.bucket_exists("scripts"):
            print("000: Bucket 'scripts' does not exist")
            client.make_bucket("scripts")
            print("001: Bucket 'scripts' was created.")
        else:
            print("002: Bucket 'scripts' exists.")

        if not client.bucket_exists("tasks"):
            print("000: Bucket 'tasks' does not exist")
            client.make_bucket("tasks")
            print("001: Bucket 'tasks' was created.")
        else:
            print("002: Bucket 'tasks' exists.")
        return print("MinIO check complete.")
    except Exception as e:
        print("MinIO check failed:\n" + str(e))

def get_task():
    task = "test_task"
    if client.stat_object(
        bucket_name="tasks",
        object_name=task
    ):
        print(f"101: Getting task '{task}'...")
        if client.fget_object(
            bucket_name="tasks",
            object_name=task,
            file_path=f"tasks/{task}.json"
        ):
            return print(f"104: Task '{task}' successfully retrieved.")
        else:
            print(f"103: Task {task} exists but could not be retrieved.")
    else:
        return print(f"100: Task '{task}' does not exist.")

def get_script():
    script = "test_script"
    if client.stat_object(
        bucket_name="scripts",
        object_name=script
    ):
        print(f"101: Getting script '{script}'...")
        if client.fget_object(
            bucket_name="scripts",
            object_name=script,
            file_path=f"scripts/{script}.json"
        ):
            return print(f"104: Script '{script}' successfully retrieved.")
        else:
            print(f"103: Script '{script}' exists but could not be retrieved.")
    else:
        return print(f"100: Script '{script}' does not exist.")