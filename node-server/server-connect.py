import asyncio
import ssl

HOST_IP = "127.0.0.1"
HOST_PORT = 4433

async def node_loop():
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)

    # Node identity (node certificate + key)
    context.load_cert_chain(
        certfile="certs/node/node.crt",
        keyfile="certs/node/node.key"
    )

    # Trusted CA (same CA the controller uses)
    context.load_verify_locations("certs/ca/ca.crt")

    while True:
        try:
            print("[Node] Connecting to controller...")

            reader, writer = await asyncio.open_connection(
                HOST_IP,  # controller address while testing
                HOST_PORT,  # controller port
                ssl=context,
                server_hostname="controller"  # must match certificate CN
            )

            print("[Node] Connected securely!")

            # Example initial handshake
            writer.write(b"HELLO_FROM_NODE")
            await writer.drain()

            # Main message loop
            while True:
                data = await reader.read(4096)
                if not data:
                    print("[Node] Controller disconnected.")
                    break

                message = data.decode()
                print(f"[Node received] {message}")

                # Example reply
                writer.write(b"ACK")
                await writer.drain()

        except Exception as e:
            print("[Node] Connection failed:", e)

        print("[Node] Reconnecting in 3 seconds...")
        await asyncio.sleep(3)


asyncio.run(node_loop())
