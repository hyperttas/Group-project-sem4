import ssl
import asyncio
from handlers import handle_node
import yaml

with open ("config.yaml") as f:
    config = yaml.safe_load(f)

ssl_conf = config["ssl"]
net_conf = config["network"]

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