import ssl
import asyncio
import yaml
import json

from networking.dispatcher import dispatch

with open ("config.yaml") as f:
    config = yaml.safe_load(f)

ssl_conf = config["ssl"]
net_conf = config["network"]

async def handle_node(reader, writer):
    addr = writer.get_extra_info("peername")
    print(f"[+] Node connected: {addr}")

    ctx = {"addr": addr}  # per-connection state

    try:
        while True:
            raw = await reader.readline()
            if not raw:
                break

            try:
                message = json.loads(raw.decode())
            except json.JSONDecodeError:
                writer.write(b'{"status":"error","error":"invalid_json"}\n')
                await writer.drain()
                continue

            response = await dispatch(message, ctx)

            writer.write((json.dumps(response) + "\n").encode())
            await writer.drain()

    finally:
        writer.close()
        await writer.wait_closed()

async def run_secure_server():
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.verify_mode = ssl.CERT_REQUIRED

    context.load_cert_chain(
        ssl_conf["cert"],
        ssl_conf["key"],
    )
    context.load_verify_locations(ssl_conf["ca_cert"])

    server = await asyncio.start_server(
        handle_node,
        host=net_conf["host"],
        port=net_conf["port"],
        ssl=context
    )

    print("[*] Secure Controller Server online at port 4433")

    async with server:
        await server.serve_forever()