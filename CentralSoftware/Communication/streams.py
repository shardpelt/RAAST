import asyncio

async def handle_echo(reader, writer):
    while True:
        print("Waiting for message..")
        data = await reader.read(100)
        message = data.decode()
        addr = writer.get_extra_info('peername')
        print(f"Received {message!r} from {addr!r}")

async def main():
    server = await asyncio.start_server(
        handle_echo, '127.0.0.1', 8888)

    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'Serving on {addrs}')

    async with server:
        await server.serve_forever()

asyncio.run(main())



# print(f"Send: {message!r}")
# writer.write(data)
# await writer.drain()
#
# print("Close the connection")
# writer.close()


# import asyncio
#
# class AsyncSocket:
#     def __init__(self):
#         self.reader = None
#         self.writer = None
#
#     def start(self):
#         asyncio.run(self.configure())
#
#     def stop(self):
#         print("Close the connection")
#         self.writer.close()
#
#     async def configure(self):
#         server = await asyncio.start_server(
#             self.receive, '127.0.0.1', 8888)
#
#         async with server:
#             await server.serve_forever()
#
#     async def receive(self, reader, writer):
#         self.reader = reader
#         self.writer = writer
#
#         while True:
#             print("waiting for messages...")
#             data = await reader.read(100)
#             print(data.decode())
#
#     async def send(self, data):
#         self.writer.write(data)
#         await self.writer.drain()
#
# s = AsyncSocket()
# s.start()