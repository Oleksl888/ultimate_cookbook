'''Commented is the html pages that do not load properly'''
'''Try using executor for sync functions'''
# async def main(value):
#     # выполнение синхронной задачм в pool-е и получение результата.
#     result = await loop.run_in_executor(None, highload_operation, value)
#     print('Result is {}'.format(result))


import socket
import asyncio
import datetime
from html_loader import *
import re


async def server_run():
    mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mysocket.bind(('127.0.0.1', 8888))
    print('http://127.0.0.1:8888')
    print('Waiting for connection...')
    mysocket.listen(1)
    while True:
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
            print(client, received)
            page = re.findall('^\S+\s(/.*?)\s', received)
            method = re.findall('(^\S+)\s', received)
            headers = "HTTP/1.1 200 OK\r\n"
            headers += "Content-Type: text/html; charset=utf-8\r\n"
            headers += "\r\n"
            # if method[0] == 'GET':
            #     if page[0] == '/' or page[0] == '/index.html':
            #         with open('pages/index.html') as file:
            #             response = file.read()
            #         newdata = re.split('</body>', response)
            #         html_body = f"<html><body>{make_html_table(extract_recepies(read_csv('cookbook.csv')))}</body></html>"
            #         data = headers + newdata[0] + html_body + '<body>' + newdata[1] + '\r\n\r\n'
            #     elif page[0] == '/feedback':
            #         with open('pages' + page[0]) as file:
            #             response = file.read()
            #         newdata = re.split('</body>', response)
            #         html_body = "<html><body>We will have feedback here with a form to submit</body></html>"
            #         data = headers + newdata[0] + html_body + '<body>' + newdata[1] + '\r\n\r\n'
            #     elif page[0] == '/gallery':
            #         with open('pages' + page[0]) as file:
            #             response = file.read()
            #         newdata = re.split('</body>', response)
            #         html_body = "<html><body>We will have picture gallery here, maybe with flickr API</body></html>"
            #         data = headers + newdata[0] + html_body + '<body>' + newdata[1] + '\r\n\r\n'
            #     elif page[0] == '/ingridients':
            #         with open('pages' + page[0]) as file:
            #             response = file.read()
            #         newdata = re.split('</body>', response)
            #         html_body = "<html><body>We will have list of ingridients here</body></html>"
            #         data = headers + newdata[0] + html_body + '<body>' + newdata[1] + '\r\n\r\n'
            #     elif page[0] == '/recepies':
            #         with open('pages' + page[0]) as file:
            #             response = file.read()
            #         newdata = re.split('</body>', response)
            #         html_body = "<html><body>We will have list of recepies here</body></html>"
            #         data = headers + newdata[0] + html_body + '<body>' + newdata[1] + '\r\n\r\n'
            #     elif page[0] == '/search':
            #         with open('pages' + page[0]) as file:
            #             response = file.read()
            #         data = headers + response + '\r\n\r\n'
            if method[0] == 'POST':
                posted_data = re.findall('search=(\S+)', received)
                lookup_word = posted_data[0]
                html_body = f"<html><body>{make_html_table(make_search(lookup_word))}</body></html>"
                with open('pages' + page[0]) as file:
                    response = file.read()
                newdata = re.split('</body>', response)
                data = headers + newdata[0] + html_body + '<body>' + newdata[1] + '\r\n\r\n'
            # with open('pages/index.html') as file:
            #     response = file.read()
            # newdata = re.split('</body>', response)
            # html_body = f"<html><body>{make_html_table(extract_recepies(read_csv('cookbook.csv')))}</body></html>"
            # data = headers + newdata[0] + html_body + '<body>' + newdata[1] + '\r\n\r\n'
            await loop.sock_sendall(client, data.encode())
            client.close()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    task = loop.create_task(server_run())
    loop.run_until_complete(task)


    # async def _race_with_page_close(self, future: Coroutine) -> None:
    #     if hasattr(self.request.frame, "_page"):
    #         page = self.request.frame._page
    #         # When page closes or crashes, we catch any potential rejects from this Route.
    #         # Note that page could be missing when routing popup's initial request that
    #         # does not have a Page initialized just yet.
    #         fut = asyncio.create_task(future)
    #         await asyncio.wait(
    #             [fut, page._closed_or_crashed_future],
    #             return_when=asyncio.FIRST_COMPLETED,
    #         )
    #         if page._closed_or_crashed_future.done():
    #             await asyncio.gather(fut, return_exceptions=True)
    #     else:
    #         await future