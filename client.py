import socket
import sys

HEADER_LENGTH = 10
SERVER = ('localhost', 10000)

username = input('enter your name').encode('UTF-8')
srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

srv.connect(SERVER)
srv.setblocking(0)

header = f'{len(username):<{HEADER_LENGTH}}'.encode('UTF-8')
srv.send(header+username)

while True:
    print('enter your message')
    msg = input().encode('UTF-8')
    if msg:
        msg_header = f'{len(msg):<{HEADER_LENGTH}}'.encode("UTF-8")
        srv.send(msg_header+msg)
        print(msg_header, msg)

    try:
        while True:
            user_header = srv.recv(HEADER_LENGTH)
            if not len(user_header):
                sys.exit()
            user_length = int(user_header.decode('UTF-8').strip())
            username = srv.recv()

            msg_header = srv.recv(HEADER_LENGTH)
            msg_length = int(msg_header.decode('UTF-8').strip())

            data = srv.recv(msg_length).decode('UTF-8')
            print(f'new message from {username} - {data}')
    except IOError as _ex:
        pass
