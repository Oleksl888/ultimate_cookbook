import socket
import asyncio
import datetime


async def server_run():
    mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mysocket.bind(('127.0.0.1', 8888))
    print('http://127.0.0.1:8888')
    while True:
        print('Waiting for connection...')
        mysocket.listen(5)
        try:
            sock_client, address = await loop.sock_accept(mysocket)
            print(f'Connected to {address} at {datetime.datetime.now()}')
        except:
            print('Could not retrieve data')
        else:
            loop.create_task(request_handle(sock_client))


async def request_handle(client):
        print('Retrievening data from user...')
        try:
            received = await loop.sock_recv(client, 5000)
        except:
            print('Couldnt retrieve data. Closing connection...')
            client.close()
        else:
            received = received.decode()
            print(received)
            data = "HTTP/1.1 200 OK\r\n"
            data += "Content-Type: text/html; charset=utf-8\r\n"
            data += "\r\n"
            data += f"<html><body>Hello World</body></html>\r\n\r\n"
            print(data)
            await loop.sock_sendall(client, data.encode())
            client.close()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(server_run())
    loop.run_forever()

