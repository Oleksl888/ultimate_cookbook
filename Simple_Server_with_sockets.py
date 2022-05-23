import socket


def server_run():
    mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mysocket.bind(('127.0.0.1', 8888))
    mysocket.listen(5)
    request_handle(mysocket)


def request_handle(server):
    while True:
        print('Waiting for connection...')
        try:
            client, address = server.accept()
            print(f'Connected to {address}')
        except:
            print('Could not retrieve data')
        else:
            print('Retrievening data from user...')
            received = client.recv(5000).decode()
            print(received)
            data = "HTTP/1.1 200 OK\r\n"
            data += "Content-Type: text/html; charset=utf-8\r\n"
            data += "\r\n"
            data += f"<html><body>Hello World{address}</body></html>\r\n\r\n"
            print(data)
            client.sendall(data.encode())
            print(client)
            client.close()


if __name__ == '__main__':
    server_run()