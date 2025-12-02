import asyncio
import ssl

async def connect_to_controller():
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)

    # Updated paths
    context.load_cert_chain("certs/node/node.crt", "certs/node/node.key")
    context.load_verify_locations("certs/ca/ca.crt")

    reader, writer = await asyncio.open_connection(
        "your-controller-ip",
        9000,
        ssl=context
    )

    writer.write(b"hello controller!\n")
    await writer.drain()

    response = await reader.read(4096)
    print("Received:", response)

    writer.close()
    await writer.wait_closed()


if __name__ == "__main__":
    asyncio.run(connect_to_controller())
