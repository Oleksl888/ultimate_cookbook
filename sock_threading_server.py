import socket
import threading
import time


def server_run():
    mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mysocket.bind(('127.0.0.1', 8888))
    print('http://127.0.0.1:8888')
    while True:
        print('Waiting for connection...')
        mysocket.listen(5)
        try:
            client, address = mysocket.accept()
            print(f'Connected to {address} at {time.time()}')
        except:
            print('Could not retrieve data')
        else:
            task = threading.Thread(target=request_handle(client))
            task.start()
            print(f'Curently {threading.active_count()} active threads')


def request_handle(client):
        print('Retrievening data from user...')
        try:
            received = client.recv(5000).decode()
        except:
            print('Couldnt retrieve data. Closing connection...')
            client.close()
        else:
            print(received)
            data = "HTTP/1.1 200 OK\r\n"
            data += "Content-Type: text/html; charset=utf-8\r\n"
            data += "\r\n"
            data += f"<html><body>Hello World</body></html>\r\n\r\n"
            print(data)
            client.sendall(data.encode())
            print(client)
            client.close()


if __name__ == '__main__':
    server_run()
