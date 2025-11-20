async def handle_node(reader, writer):
    addr = writer.get_extra_info("peername")
    print(f"[+] Node connected: {addr}")

    try:
        while True:
            data = await reader.read(4096)
            if not data:
                break

            message = data.decode()
            print(f"[Node {addr}] {message}")

            writer.write(b"ACK")
            await writer.drain()

    finally:
        writer.close()
        await writer.wait_closed()
