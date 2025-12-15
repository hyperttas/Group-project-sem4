from general.async_funcs import get_nodes, get_jobs, job_active, save_result, node_online, register_node
from general.funcs import get_task, get_script
import json
async def acknowledge(data, ctx):
    node_ip = ctx['addr'][0]
    result = await get_nodes()
    known_nodes = []
    for node in result:
        known_nodes.extend(node['ip_addresses'])
    if ctx['addr'][0] in known_nodes:
        await node_online(node_ip)
    else:
        await register_node(node_ip)
        await node_online(node_ip)
    return {"status": "ok", "message": "ACK"}

async def ping(data, ctx):
    print(f"Ping received from node {ctx}")
    all_jobs = await get_jobs()
    jobs = [job for job in all_jobs if job.get("status") == 0]

    if len(jobs) > 0:
        earliest_job = min(jobs, key=lambda job: job["job_id"])
        node_package = {
            'task': get_task(earliest_job['task']),
            'script': get_script(earliest_job['script']),
            'job_id':earliest_job['job_id']}
        await job_active(earliest_job['job_id'])
        return node_package
    else:
        resp = {"status": "error", "message": "No jobs found"}
        return resp

async def job_get_ok(data, ctx):
    resp = {"status": "ok", "message": "OK"}
    print(f"Preparing to receive job data from node {ctx}")
    return resp

async def job_receive(data, ctx):
    if len(data[1]) > 0:
        resp = {"status": "ok", "message": "Received data successfully"}
        job_id = data[0]
        result = json.dumps(data[1])
        print("Received job result:",result)
        await save_result(job_id, result)
        return resp
    else:
        resp = {"status": "error", "message": "No data received"}
        return resp

ACTION_MAP = {
    "ack": acknowledge,
    "ping": ping,
    "job_complete": job_get_ok,
    "job_payload": job_receive,
}

async def dispatch(message, ctx):
    req_id = message.get("id")
    action = message.get("action")
    data = message.get("data", {})

    if action not in ACTION_MAP:
        return {"id": req_id, "status": "error", "error": "unknown_action"}

    result = await ACTION_MAP[action](data, ctx)

    if not isinstance(result, dict):
        result = {"result": result}

    result["id"] = req_id
    return result