from common import client
import base64

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

def get_task(task):
    if client.stat_object(
        bucket_name="tasks",
        object_name=task
    ):
        #print(f"101: Getting task '{task}'...")
        response = client.get_object(
            bucket_name="tasks",
            object_name=task
        )
        task_bytes = response.read()
        response.close()
        response.release_conn()
        if task_bytes:
            #print(f"104: Task '{task}' successfully retrieved.")
            return base64.b64encode(task_bytes).decode("ascii")
        else:
            print(f"103: Task {task} exists but could not be retrieved.")
    else:
        print(f"100: Task '{task}' does not exist.")
    return None

def get_script(script):
    if client.stat_object(
        bucket_name="scripts",
        object_name=script
    ):
        #print(f"101: Getting script '{script}'...")
        response = client.get_object(
            bucket_name="scripts",
            object_name=script
        )
        script_bytes = response.read()
        response.close()
        response.release_conn()
        if script_bytes:
            #print(f"104: Script '{script}' successfully retrieved.")
            return base64.b64encode(script_bytes).decode("ascii")
        else:
            print(f"103: Script '{script}' exists but could not be retrieved.")
    else:
        print(f"100: Script '{script}' does not exist.")
    return None