
import asyncio


class Client:
    def __init__(self):
        self.reader, self.writer = None, None

    async def setup(self):
        self.reader, self.writer = await asyncio.open_connection(
            '127.0.0.1', 8888)

    def send(self, message):
        print(f'Send: {message!r}')
        self.writer.write(message.encode())

c = Client()
asyncio.run(c.setup())


# async def tcp_echo_client(message):
#
#     print(f'Send: {message!r}')
#     writer.write(message.encode())
#
#     data = await reader.read(100)
#     print(f'Received: {data.decode()!r}')
#
#     print('Close the connection')
#    writer.close()




# import asyncio
#
# class Client:
#     def __init__(self):
#         self.reader = None
#         self.writer = None
#
#     async def setup(self):
#         self.reader, self.writer = await asyncio.open_connection(
#             '127.0.0.1', 8888)
#
#     def send(self, message):
#         self.writer.write(message.encode())
#
#
# client = Client()
# asyncio.run(client.setup())
#
# print(client.reader, client.writer)
#
# msg = input("send message >> ")
# client.send(msg)

